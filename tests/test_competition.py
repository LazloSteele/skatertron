from Skatertron.database import Base, session_manager, get_db_session
from Skatertron.models import Competition, Event, Skate, File


class TestCompetition:
    def setup_class(self):
        Base.metadata.create_all(session_manager.engine)

        self.session = get_db_session().__next__()
        self.valid_competition = Competition(
            competition_name="Denver International",
            competition_year=2055,
            host_club="Denver FSC"
        )

        self.valid_event = Event(
            competition_id=2,
            event_number="2055b",
            event_name="Chacha Slide"
        )

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_competition_valid(self):
        self.session.add(self.valid_competition)
        self.session.commit()

        denver_international = self.session.query(Competition).filter_by(
            competition_name="Denver International").first()

        assert denver_international.competition_year == 2055
        assert denver_international.competition_name != "Enver Invitational"
        assert denver_international.host_club == "Denver FSC"

    '''
    def test_event_valid(self):
        self.session.add(self.valid_event)
        self.session.commit()

        chacha_slide = self.session.query(Event).filter_by(
            event_number="2055b").first()

        assert chacha_slide.competition_id == 1
        assert chacha_slide.event_name != "Enver Invitational"
        assert chacha_slide.event_number == "2055b"
    '''
