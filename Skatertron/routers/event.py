from fastapi import APIRouter, HTTPException, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.exc import UnmappedInstanceError

from typing import Annotated
from io import BytesIO

from Skatertron.models.event import Event as EventDBModel
from Skatertron.schemas.event import Event as EventSchema
from Skatertron.schemas.update_position_request import UpdateEventPositionRequest as PutPositionRequest
from Skatertron.models.skate import Skate as SkateDBModel
from Skatertron.models.competition import Competition as CompetitionDBModel
from Skatertron.models.file import File as FileDBModel
from Skatertron.database import get_db_session
from Skatertron.utils.pdf_scraper import PDFScraper


router = APIRouter(
    prefix="/events",
    tags=["events"]
)


templates = Jinja2Templates(directory="templates")


@router.post("/", status_code=201, response_class=HTMLResponse)
async def create_event(
        event_name: Annotated[str, Form()],
        event_number: Annotated[str, Form()],
        event_rink: Annotated[str, Form()],
        competition_id: Annotated[int, Form()],
        request: Request
):
    try:
        event = await EventDBModel(
            event_name=event_name,
            event_number=event_number,
            event_rink=event_rink,
            competition_id=competition_id
        )
        with get_db_session().__next__() as session:
            session.add(event)
            session.commit()

        return templates.TemplateResponse(
            request=request,
            name="new_event.html",
            context={
                "current_competition": competition_id,
                "event": event
            }
        )

    except IntegrityError:
        raise HTTPException(422, "Missing data from event model.")


@router.post("/pdf_scraper", status_code=201, response_class=HTMLResponse)
async def create_event_by_pdf(
        request: Request,
        event_type: Annotated[str, Form()],
        competition_id: Annotated[int, Form()],
        event_rink: Annotated[str, Form()],
        pdf_file_list: list[UploadFile] = File(...)
):
    for pdf_file in pdf_file_list:
        content = BytesIO(pdf_file.file.read())
        print(content)
        event_scraped = PDFScraper.stage_pdf(content, event_type)

        try:
            event = EventDBModel(event_name=event_scraped["event_name"],
                                 event_number=event_scraped["event_number"],
                                 event_rink=event_rink,
                                 competition_id=competition_id
                                 )

            with get_db_session().__next__() as session:
                session.add(event)
                session.commit()

            for skater in event_scraped["skaters"]:
                skate = SkateDBModel(event_id=event.id, skater_name=skater)
                with get_db_session().__next__() as session:
                    session.add(skate)
                    session.commit()

        except IntegrityError:
            raise HTTPException(422, "Missing data from event model.")

    with get_db_session().__next__() as session:
        events_list = session.query(EventDBModel).filter_by(competition_id=competition_id).all()
        current_competition = session.query(CompetitionDBModel).filter_by(id=competition_id).first()

    return templates.TemplateResponse(
        request=request,
        name="events_by_competition.html",
        context={
            "events_list": events_list,
            "current_competition": current_competition
        }
    )


@router.get("/{event_id}", response_model=EventSchema)
async def get_event_by_id(event_id: int):
    try:
        with get_db_session().__next__() as session:
            event = session.query(EventDBModel).filter_by(id=event_id).first()

            return event
    except IntegrityError:
        raise HTTPException(404, f"Event with id #{event_id} not found.")


@router.get("/{event_id}/skates/", response_class=HTMLResponse)
async def get_skates_by_event_id(event_id: int, request: Request):
    try:
        with get_db_session().__next__() as session:
            skates = session.query(SkateDBModel).filter_by(
                event_id=event_id
            ).order_by(
                SkateDBModel.skate_position
            ).all()

            current_event = await get_event_by_id(event_id)
            current_competition = session.query(CompetitionDBModel).filter_by(id=current_event.competition_id)

            return templates.TemplateResponse(
                request=request,
                name="skates_by_event.html",
                context={
                    "current_competition": current_competition,
                    "current_event": current_event,
                    "skates_list": skates
                }
            )
    except IntegrityError:
        raise HTTPException(404, f"Event with id #{event_id} not found.")


@router.put("/update_position")
def update_event_position(request: PutPositionRequest):
    print("\n\n\nUpdating event positions!\n\n\n")

    event_list = request.event_id_list

    print(event_list)

    with get_db_session().__next__() as session:
        try:
            i = 0
            for event_id in event_list:
                event = session.query(EventDBModel).filter_by(id=int(event_id)).first()

                print(event_id)
                event.event_position = i

                i += 1

            session.commit()

        except UnmappedInstanceError:
            raise HTTPException(404, f"Event with id: #{event_id} not found.")
        except SQLAlchemyError as e:
            session.rollback()  # Rollback on error
            raise HTTPException(status_code=500, detail=f"Database update failed: {e}")


@router.put("/{event_id}")
def update_event(
        event_id: int,
        new_event_name: str | None = None,
        new_event_number: str | None = None,
        new_competition_id: int | None = None
):
    with get_db_session().__next__() as session:
        try:
            event = session.query(EventDBModel).filter_by(id=event_id).first()
            if new_event_name:
                event.event_name = new_event_name
            if new_event_number:
                event.event_number = new_event_number
            if new_competition_id:
                event.competition_id = new_competition_id

            session.commit()
        except UnmappedInstanceError:
            raise HTTPException(404, f"Event with id: #{event_id} not found.")


@router.delete("/{event_id}")
def delete_event(event_id: int):
    with get_db_session().__next__() as session:
        try:
            event = session.query(EventDBModel).filter_by(id=event_id).first()
            skates = session.query(SkateDBModel).filter_by(event_id=event.id).all()

            for skate in skates:
                files = session.query(FileDBModel).filter_by(skate_id=skate.id).all()
                for my_file in files:
                    session.delete(my_file)
                session.delete(skate)

            session.delete(event)
            session.commit()
        except UnmappedInstanceError:
            raise HTTPException(404, f"Event with id: #{event_id} not found.")


@router.get("/{event_id}/details/json", response_class=JSONResponse)
def get_event_details_json(event_id:int):
    try:
        with get_db_session().__next__() as session:
            event = session.query(EventDBModel).filter_by(id=event_id).first()

            content = {
                "id": event.id,
                "competition_id": event.competition_id,
                "event_number": event.event_number,
                "event_name": event.event_name,
                "event_rink": event.event_rink,
                "event_position": event.event_position
            }
            print(content)

            return JSONResponse(
                content=content,
                status_code=200
            )

    except IntegrityError:
        raise HTTPException(404, f"Event with id #{event_id} not found.")
