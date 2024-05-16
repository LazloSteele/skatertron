from Skatertron.database import Base, session_manager, get_db_session
from Skatertron.models import Skate


class TestSkate:
    def setup_class(self):
        Base.metadata.create_all(session_manager.engine)

        self.session = get_db_session().__next__()

        self.valid_skate = Skate(
            event_id=91,
            skater_name="Buhbula"
        )

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_event_valid(self):
        self.session.add(self.valid_skate)
        self.session.commit()

        buhbula = self.session.query(Skate).filter_by(
            skater_name="Buhbula").first()

        assert buhbula.event_id == 91
        assert buhbula.skater_name != "Enver Invitational"
