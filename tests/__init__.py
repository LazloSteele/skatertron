from Skatertron.database import Base, session_manager, get_db_session
from Skatertron.models import Competition, Event, Skate, File

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


@pytest.fixture(scope="module")
def valid_event():
    valid_event = Event(
        competition_id=1,
        event_number="205b",
        event_name="Chacha Slide"
    )

    return valid_event

@pytest.fixture(scope="module")
def valid_skate():
    valid_skate = Skate(
        event_id=1,
        skater_name="Buhbula"
    )

    return valid_skate


@pytest.fixture(scope="module")
def valid_file():
    valid_file = File(
        skate_id=1,
        file_name="109231093.mp4"
    )

    return valid_file
