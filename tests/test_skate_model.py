from . import db_session, valid_skate

from Skatertron.models import Skate
from sqlalchemy.exc import IntegrityError


class TestSkate:
    def test_skate_valid(self, db_session, valid_skate):
        db_session.add(valid_skate)
        db_session.commit()

        buhbula = db_session.query(Skate).filter_by(
            skater_name="Buhbula").first()

        assert buhbula.event_id == 1
        assert buhbula.skater_name != "Enver Invitational"

    def test_skate_delete(self, db_session, valid_skate):
        test_skate = db_session.query(Skate).filter_by(
            id=valid_skate.id).first()
        test_id = test_skate.id

        db_session.delete(test_skate)
        db_session.commit()

        try:
            db_session.query(Skate).filter_by(
                id=test_id).first()
        except IntegrityError:
            db_session.rollback()
