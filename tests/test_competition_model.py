from Skatertron.models import Competition, Event
from sqlalchemy.exc import IntegrityError
from . import db_session, valid_competition, valid_event, valid_skate, valid_file

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


class TestEvent:
    def test_event_valid(self, db_session, valid_event):
        db_session.add(valid_event)
        db_session.commit()

        chacha_slide = db_session.query(Event).filter_by(
            event_number="205b").first()

        assert chacha_slide.competition_id == 1
        assert chacha_slide.event_name != "Enver Invitational"
        assert chacha_slide.event_number == "205b"

    def test_event_renumber(self, db_session):
        fs1 = db_session.query(Event).filter_by(
            event_name="Test Skate"
        ).first()

        fs1_id = fs1.id
        fs1.event_number = "2056"
        db_session.commit()
        fs1 = db_session.query(Event).filter_by(
            id=fs1_id
        ).first()

        assert fs1.event_number == "2056"

    def test_event_rename(self, db_session):
        fs1 = db_session.query(Event).filter_by(
            event_name="Test Skate"
        ).first()

        fs1_id = fs1.id
        fs1.event_name = "New Name"
        db_session.commit()
        fs1 = db_session.query(Event).filter_by(
            id=fs1_id).first()

        assert fs1.event_name == "New Name"

    def test_event_delete(self, db_session, valid_event):
        chacha_slide = db_session.query(Event).filter_by(
            id=valid_event.id).first()
        chacha_slide_id = chacha_slide.id

        db_session.delete(chacha_slide)
        db_session.commit()

        try:
            db_session.query(Event).filter_by(
                id=chacha_slide_id).first()
        except IntegrityError:
            db_session.rollback()

    @pytest.mark.xfail(raises=IntegrityError)
    def test_event_no_name(self, db_session):
        event = Event(
            competition_id=1,
            event_number="44"
        )

        db_session.add(event)
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()

    @pytest.mark.xfail(raises=IntegrityError)
    def test_competition_no_competition(self, db_session):
        competition = Event(
            event_name="Flippy Skate",
            event_number="44"
        )

        db_session.add(competition)
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()

    @pytest.mark.xfail(raises=IntegrityError)
    def test_competition_no_number(self, db_session):
        competition = Event(
            event_name="Flippy Skate",
            competition_id=1
        )

        db_session.add(competition)
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
