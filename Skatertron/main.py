from fastapi import FastAPI, HTTPException
from models import Competition as CompetitionDBModel
from database import session_manager, get_db_session
from schemas.competition import Competition
from contextlib import contextmanager
from config import settings
from sqlalchemy.exc import IntegrityError

app = FastAPI(title="Skatertron", docs_url="/api/docs")


def valid_competition():
    valid_competition = CompetitionDBModel(
        competition_name="Denver International",
        competition_year=2055,
        host_club="Denver FSC"
    )
    return valid_competition


@app.get("/")
def root():
    return {"Hello": "Skaters"}


@app.get("/competitions", response_model=list[Competition])
def get_all_competitions():
    all_competitions = get_db_session().__next__().query(CompetitionDBModel).all()

    return all_competitions


@app.get("/competitions/{competition_id}", response_model=Competition)
def get_competition_by_id(competition_id: int):
    try:
        with get_db_session().__next__() as session:
            competition = session.query(CompetitionDBModel).filter_by(id=competition_id).first()

            return competition
    except IntegrityError:
        raise HTTPException(404, f"Competition with id#{competition_id} not found.")


@app.put("/competitions/{competition_id}")
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
        except IntegrityError:
            raise HTTPException(404, f"Competition with id#{competition_id} not found.")


@app.post("/competitions")
def create_competition(competition_schema: Competition):
    try:
        competition = CompetitionDBModel(competition_name=competition_schema.competition_name,
                                         competition_year=competition_schema.competition_year,
                                         host_club=competition_schema.host_club
                                         )
    except IntegrityError:
        raise HTTPException(422, "Missing data from competition model.")

    with get_db_session().__next__() as session:
        session.add(competition)
        session.commit()

    return get_db_session().__next__().query(CompetitionDBModel).all()


