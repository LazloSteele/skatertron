from fastapi import APIRouter, HTTPException, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from typing import Annotated

from Skatertron.models.event import Event as EventDBModel
from Skatertron.schemas.event import Event as EventSchema
from Skatertron.models.skate import Skate as SkateDBModel
from Skatertron.models.competition import Competition as CompetitionDBModel
from Skatertron.database import get_db_session
from Skatertron.utils.pdf_scraper import PDFScraper


router = APIRouter(
    prefix="/events",
    tags=["events"]
)


templates = Jinja2Templates(directory="templates")


@router.post("/", status_code=201, response_class=HTMLResponse)
def create_event(event_name: Annotated[str, Form()],
                 event_number: Annotated[str, Form()],
                 competition_id: Annotated[int, Form()],
                 request: Request):
    try:
        event = EventDBModel(event_name=event_name,
                             event_number=event_number,
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
def create_event_by_pdf(request: Request,
                        event_type: Annotated[str, Form()],
                        competition_id: Annotated[int, Form()],
                        pdf_file: UploadFile = File(...)
                        ):
    event = PDFScraper.stage_pdf(pdf_file, event_type)

    try:
        event = EventDBModel(event_name=event.event_name,
                             event_number=event.event_number,
                             competition_id=competition_id
                             )

        with get_db_session().__next__() as session:
            session.add(event)
            session.commit()

        for skater in event.skaters:
            skate = SkateDBModel(event_id=event.id, skater_name=skater)
            with get_db_session().__next__() as session:
                session.add(skate)
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


@router.get("/{event_id}", response_model=EventSchema)
def get_event_by_id(event_id: int):
    try:
        with get_db_session().__next__() as session:
            event = session.query(EventDBModel).filter_by(id=event_id).first()

            return event
    except IntegrityError:
        raise HTTPException(404, f"Event with id #{event_id} not found.")


@router.get("/{event_id}/skates/", response_class=HTMLResponse)
def get_skates_by_event_id(event_id: int, request: Request):
    try:
        with get_db_session().__next__() as session:
            skates = session.query(SkateDBModel).filter_by(event_id=event_id).all()

            current_event = get_event_by_id(event_id)
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


@router.put("/{event_id}")
def update_event(event_id: int,
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

            session.delete(event)
            session.commit()
        except UnmappedInstanceError:
            raise HTTPException(404, f"Event with id: #{event_id} not found.")
