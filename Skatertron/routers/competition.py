from fastapi import APIRouter, HTTPException, Form, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from Skatertron.models.competition import Competition as CompetitionDBModel
from Skatertron.schemas.competition import Competition as CompetitionSchema
from Skatertron.database import get_db_session

router = APIRouter(
    prefix="/competitions",
    tags=["competitions"]
)


templates = Jinja2Templates(directory="templates")


@router.post("/", status_code=201, response_class=HTMLResponse)
def create_competition(competition_name: Annotated[str, Form()],
                       competition_year: Annotated[int, Form()],
                       host_club: Annotated[str, Form()],
                       request: Request
                       ):
    try:
        competition = CompetitionDBModel(competition_name=competition_name,
                                         competition_year=competition_year,
                                         host_club=host_club
                                         )

        with get_db_session().__next__() as session:
            session.add(competition)
            session.commit()

        return templates.TemplateResponse(
            request=request,
            name="new_competition.html",
            context={
                "competition": competition
            }
        )

    except IntegrityError:
        raise HTTPException(422, "Missing data from competition model.")


@router.get("/", response_model=list[CompetitionSchema])
def get_all_competitions():
    all_competitions = get_db_session().__next__().query(CompetitionDBModel).all()

    return all_competitions


@router.get("/{competition_id}", response_model=CompetitionSchema)
def get_competition_by_id(competition_id: int):
    try:
        with get_db_session().__next__() as session:
            competition = session.query(CompetitionDBModel).filter_by(id=competition_id).first()

            return competition
    except IntegrityError:
        raise HTTPException(404, f"Competition with id#{competition_id} not found.")


@router.put("/{competition_id}")
def update_competition(competition_id: int,
                       new_competition_name: str | None = None,
                       new_competition_year: int | None = None,
                       new_competition_host_name: str | None = None
                       ):
    with get_db_session().__next__() as session:
        try:
            competition = session.query(CompetitionDBModel).filter_by(id=competition_id).first()
            if new_competition_name:
                competition.competition_name = new_competition_name
            if new_competition_year:
                competition.competition_year = new_competition_year
            if new_competition_host_name:
                competition.host_club = new_competition_host_name

            session.commit()
        except UnmappedInstanceError:
            raise HTTPException(404, f"Competition with id: #{competition_id} not found.")


@router.delete("/{competition_id}")
def delete_competition(competition_id: int):
    with get_db_session().__next__() as session:
        try:
            competition = session.query(CompetitionDBModel).filter_by(id=competition_id).first()

            session.delete(competition)
            session.commit()
        except UnmappedInstanceError:
            raise HTTPException(404, f"Competition with id: #{competition_id} not found.")
