from Skatertron.database import Base, session_manager, get_db_session
from Skatertron.models import Event


class TestEvent:
    def setup_class(self):
        Base.metadata.create_all(session_manager.engine)

        self.session = get_db_session().__next__()

        self.valid_event = Event(
            competition_id=2,
            event_number="205b",
            event_name="Chacha Slide"
        )

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_event_valid(self):
        self.session.add(self.valid_event)
        self.session.commit()

        chacha_slide = self.session.query(Event).filter_by(
            event_number="205b").first()

        assert chacha_slide.competition_id == 2
        assert chacha_slide.event_name != "Enver Invitational"
        assert chacha_slide.event_number == "205b"
