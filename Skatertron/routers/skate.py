from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from typing import Annotated

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from Skatertron.models.skate import Skate as SkateDBModel
from Skatertron.schemas.skate import Skate as SkateSchema
from Skatertron.database import get_db_session

router = APIRouter(
    prefix="/skates",
    tags=["skates"]
)

templates = Jinja2Templates(directory="templates")


@router.post("/", status_code=201, response_class=HTMLResponse)
def create_skate(event_id: Annotated[int, Form()],
                 skater_name: Annotated[str, Form()],
                 request: Request):
    try:
        skate = SkateDBModel(event_id=event_id,
                             skater_name=skater_name
                             )

        with get_db_session().__next__() as session:
            session.add(skate)
            session.commit()

        return templates.TemplateResponse(
            request=request,
            name="new_skate.html",
            context={
                "skate": skate
            }
        )

    except IntegrityError:
        raise HTTPException(422, "Missing data from skate model.")


@router.get("/", response_model=list[SkateSchema])
def get_all_skates():
    all_skates = get_db_session().__next__().query(SkateDBModel).all()

    return all_skates


@router.get("/{skate_id}", response_model=SkateSchema)
def get_skate_by_id(skate_id: int):
    try:
        with get_db_session().__next__() as session:
            skate = session.query(SkateDBModel).filter_by(id=skate_id).first()

            return skate
    except IntegrityError:
        raise HTTPException(404, f"Skate with id #{skate_id} not found.")


@router.get("/get_skates_by_event_id/{event_id}", response_class=HTMLResponse)
def get_skates_by_event_id(event_id: int, request: Request):
    try:
        with get_db_session().__next__() as session:
            skates = session.query(SkateDBModel).filter_by(event_id=event_id).all()

            return templates.TemplateResponse(
                request=request,
                name="skates_by_event.html",
                context={
                    "current_event_id": event_id,
                    "skates_list": skates
                }
            )
    except IntegrityError:
        raise HTTPException(404, f"Event with id #{event_id} not found.")


@router.put("/{skate_id}")
def update_event(skate_id: int,
                 new_event_id: int | None = None,
                 new_skater_name: str | None = None,
                 ):
    with get_db_session().__next__() as session:
        try:
            skate = session.query(SkateDBModel).filter_by(id=skate_id).first()
            if new_event_id:
                skate.event_id = new_event_id
            if new_skater_name:
                skate.skater_name = new_skater_name

            session.commit()
        except UnmappedInstanceError:
            raise HTTPException(404, f"Skate with id: #{skate_id} not found.")


@router.delete("/{skate_id}")
def delete_event(skate_id: int):
    with get_db_session().__next__() as session:
        try:
            skate = session.query(SkateDBModel).filter_by(id=skate_id).first()

            session.delete(skate)
            session.commit()
        except UnmappedInstanceError:
            raise HTTPException(404, f"Skate with id: #{skate_id} not found.")
