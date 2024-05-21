from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from Skatertron.models.event import Event as EventDBModel
from Skatertron.schemas.event import Event as EventSchema
from Skatertron.database import get_db_session

router = APIRouter(
    prefix="/events",
    tags=["events"]
)


@router.post("/")
def create_event(event_schema: EventSchema):
    try:
        event = EventDBModel(event_name=event_schema.event_name,
                             event_number=event_schema.event_number,
                             competition_id=event_schema.competition_id
                             )
    except IntegrityError:
        raise HTTPException(422, "Missing data from event model.")

    with get_db_session().__next__() as session:
        session.add(event)
        session.commit()


@router.get("/", response_model=list[EventSchema])
def get_all_events():
    all_events = get_db_session().__next__().query(EventDBModel).all()

    return all_events


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


@router.delete("/{event_id")
def delete_event(event_id: int):
    with get_db_session().__next__() as session:
        try:
            event = session.query(EventDBModel).filter_by(id=event_id).first()

            session.delete(event)
            session.commit()
        except UnmappedInstanceError:
            raise HTTPException(404,f"Event with id: #{event_id} not found.")
