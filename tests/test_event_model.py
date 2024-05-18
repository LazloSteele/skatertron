from Skatertron.models import Event
from sqlalchemy.exc import IntegrityError
from . import db_session, valid_event

import pytest


class TestEvent:
    def test_event_valid(self, db_session, valid_event):
        db_session.add(valid_event)
        db_session.commit()

        chacha_slide = db_session.query(Event).filter_by(
            event_number="205b").first()

        assert chacha_slide.competition_id == 1
        assert chacha_slide.event_name != "Enver Invitational"
        assert chacha_slide.event_number == "205b"

    def test_competition_delete(self, db_session, valid_event):
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
    def test_competition_no_name(self, db_session):
        event = Event(
            competition_id=1,
            event_number="44"
        )

        db_session.add(event)
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
