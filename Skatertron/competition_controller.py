from sqlalchemy_backend import connect_to_db, Base, Event, Skate, File

from sqlalchemy import select, delete
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

    def read_event(self, event_id=None, event_number=None, event_title=None):
        events = []
        statement = select(Event)

        if event_id:
            statement = statement.where(Event.id == event_id)

        if event_number:
            statement = statement.where(Event.evt_number == event_number)

        if event_title:
            statement = statement.where(Event.evt_title == event_title)

        my_query = self.session.execute(statement)

        for event in my_query.scalars():
            events.append(event)

        return events

    def update_event(self, event_id, new_event_num, new_event_title):
        pass

    def delete_event(self, event_id=None, event_number=None, event_title=None):

        if event_id:
            event = self.session.query(Event).filter_by(id=event_id).one_or_none()


        if event_number:
            event = self.session.query(Event).filter_by(evt_number=event_number).one_or_none()

        if event_title:
            event = self.session.query(Event).filter_by(evt_title=event_title).one_or_none()

        try:
            self.session.delete(event)

            self.session.commit()
        except UnmappedInstanceError:
            raise EventNotExists
