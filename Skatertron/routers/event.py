from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from typing import Annotated

from Skatertron.models.event import Event as EventDBModel
from Skatertron.schemas.event import Event as EventSchema
from Skatertron.database import get_db_session


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
                "event": event
            }
        )

    except IntegrityError:
        raise HTTPException(422, "Missing data from event model.")



@router.get("/", response_model=list[EventSchema])
def get_all_events():
    all_events = get_db_session().__next__().query(EventDBModel).all()

    return all_events


@router.get("/by_competition/{competition_id}", response_class=HTMLResponse)
def get_events_by_competition_id(request: Request, competition_id: int):
    with get_db_session().__next__() as session:
        events_list = session.query(EventDBModel).filter_by(competition_id=competition_id).all()

    return templates.TemplateResponse(
        request=request,
        name="events_by_competition.html",
        context={
            "events_list": events_list,
            "current_competition_id": competition_id
        })


@router.get("/{event_id}", response_model=EventSchema)
def get_event_by_id(event_id: int):
    try:
        with get_db_session().__next__() as session:
            event = session.query(EventDBModel).filter_by(id=event_id).first()

            return event
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
