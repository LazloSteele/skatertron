from Skatertron.database import Base, session_manager, get_db_session
from Skatertron.models import Skate
from sqlalchemy.exc import IntegrityError


class TestSkate:
    def setup_class(self):
        Base.metadata.create_all(session_manager.engine)

        self.session = get_db_session().__next__()

        self.valid_skate = Skate(
            event_id=1,
            skater_name="Buhbula"
        )

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_skate_valid(self):
        self.session.add(self.valid_skate)
        self.session.commit()

        buhbula = self.session.query(Skate).filter_by(
            skater_name="Buhbula").first()

        assert buhbula.event_id == 1
        assert buhbula.skater_name != "Enver Invitational"

    def test_skate_delete(self):
        test_skate = self.session.query(Skate).filter_by(
            id=self.valid_skate.id).first()
        test_id = test_skate.id

        self.session.delete(test_skate)
        self.session.commit()

        try:
            self.session.query(Skate).filter_by(
                id=test_id).first()
        except IntegrityError:
            self.session.rollback()
