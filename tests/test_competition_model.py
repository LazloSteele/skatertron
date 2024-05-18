from Skatertron.models import Competition
from sqlalchemy.exc import IntegrityError
from . import db_session, valid_competition

import pytest


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

    def test_competition_delete(self, db_session, valid_competition):
        denver_international = db_session.query(Competition).filter_by(
            id=valid_competition.id).first()
        di_id = denver_international.id

        db_session.delete(denver_international)
        db_session.commit()

        try:
            db_session.query(Competition).filter_by(
                id=di_id).first()
        except IntegrityError:
            db_session.rollback()

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
