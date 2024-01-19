from sqlalchemy_backend import connect_to_db, Base, Event, Skate, File

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from skatertron_exceptions import EventExists, EventNotExists


class Controller(object):
    def __init__(self, competition = "test"):
        self.competition = competition

        self.engine = connect_to_db(self.competition)

        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_event(self, event_num, event_title):
        event = Event(evt_number=event_num, evt_title=event_title)

        try:
            self.session.add(event)

            self.session.commit()
        except IntegrityError:
            raise EventExists

    def read_event(self, **kwargs):
        events = []

        if "event_number" in kwargs:
            statement = select(Event).where(Event.evt_number == kwargs["event_number"])
            my_query = self.session.execute(statement)

        else:
            statement = select(Event)
            my_query = self.session.execute(statement)

        for event in my_query.scalars():
            events.append({
                "id": event.id,
                "number": event.evt_number,
                "title": event.evt_title
            })

        return events

    def update_event(self, event_id, new_event_num, new_event_title):
        pass

    def delete_event(self, event_num):
        event = self.session.query(Event).filter_by(evt_number=event_num).one_or_none()

        try:
            self.session.delete(event)

            self.session.commit()
        except UnmappedInstanceError:
            raise EventNotExists
