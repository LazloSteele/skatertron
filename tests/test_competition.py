from Skatertron.database import Base, session_manager, get_db_session
from Skatertron.models import Competition
from sqlalchemy.exc import IntegrityError
import pytest


@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(session_manager.engine)
    session = get_db_session().__next__()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="module")
def valid_competition():
    valid_competition = Competition(
        competition_name="Denver International",
        competition_year=2055,
        host_club="Denver FSC"
    )
    return valid_competition


class TestCompetition:
    def test_competition_valid(self, db_session, valid_competition):
        db_session.add(valid_competition)
        db_session.commit()

        denver_international = db_session.query(Competition).filter_by(
            competition_name="Denver International").first()

        assert denver_international.competition_year == 2055
        assert denver_international.competition_name != "Enver Invitational"
        assert denver_international.host_club == "Denver FSC"

    def test_competition_renumber(self, db_session):
        denver_international = db_session.query(Competition).filter_by(
            competition_name="Denver International").first()

        di_id = denver_international.id
        denver_international.competition_year = 2056
        db_session.commit()
        denver_international = db_session.query(Competition).filter_by(
            id=di_id).first()

        assert denver_international.competition_year == 2056

    def test_competition_rename(self, db_session):
        denver_international = db_session.query(Competition).filter_by(
            competition_name="Denver International").first()

        di_id = denver_international.id
        denver_international.competition_name = "Schmlenver International"
        db_session.commit()
        denver_international = db_session.query(Competition).filter_by(
            id=di_id).first()

        assert denver_international.competition_name == "Schmlenver International"


    @pytest.mark.xfail(raises=IntegrityError)
    def test_competition_no_name(self, db_session):
        competition = Competition(
            competition_year=2055,
            host_club="Denver FSC"
        )

        db_session.add(competition)
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()

    @pytest.mark.xfail(raises=IntegrityError)
    def test_competition_no_year(self, db_session):
        competition = Competition(
            competition_name="Denver Invitational",
            host_club="Denver FSC"
        )

        db_session.add(competition)
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()

    @pytest.mark.xfail(raises=IntegrityError)
    def test_competition_no_host(self, db_session):
        competition = Competition(
            competition_year=2055,
            competition_name="Denver FSC"
        )

        db_session.add(competition)
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
