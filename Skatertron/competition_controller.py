from sqlalchemy_backend import connect_to_db, Base, Event, Skate, File

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from skatertron_exceptions import EventExists, EventNotExists, SkaterExistsInEvent, SkaterNotInEvent


class EventController(object):
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

    def read_all_events(self):
        events = []

        query = self.session.execute(select(Event)).scalars()

        for event in query:
            events.append(event)
        return events

    def read_event_by_id(self, event_id):
        event = self.session.get(Event, event_id)
        return event

    def read_event_by_number(self, event_number):
        event = self.session.execute(select(Event).filter_by(evt_number=event_number)).one_or_none()[0]
        return event

    def read_events_by_title(self, event_title):
        events = []
        query = self.session.execute(select(Event).where(Event.evt_title.contains(event_title))).all()

        for event in query:
            events.append(event[0])

        return events

    def update_event(self, event_id, new_event_number=None, new_event_title=None):
        event = self.session.get(Event, event_id)

        if new_event_number:
            event.evt_number = new_event_number

        if new_event_title:
            event.evt_title = new_event_title

        self.session.commit()

    def delete_event(self, event_id):

        event = self.session.get(Event, event_id)

        try:
            self.session.delete(event)

            self.session.commit()
        except UnmappedInstanceError:
            raise EventNotExists


class SkateController(object):
    def __init__(self, competition = "test"):
        self.competition = competition

        self.engine = connect_to_db(self.competition)

        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_skate(self, event_id, skater_name):
        skate = Skate(evt_id=event_id, skater=skater_name)

        try:
            self.session.add(skate)

            self.session.commit()
        except IntegrityError:
            raise EventNotExists

    def read_all_skates(self):
        skates = []

        query = self.session.execute(select(Skate)).scalars()

        for skate in query:
            skates.append(skate)
        return skates

    def read_skate_by_id(self, skate_id):
        skate = self.session.get(Skate, skate_id)
        return skate

    def read_skates_by_event(self, event_id):
        skates = []
        query = self.session.execute(select(Skate).filter_by(evt_id=event_id)).all()

        for skate in query:
            skates.append(skate[0])
        return skates

    def read_events_by_title(self, event_title):
        events = []
        query = self.session.execute(select(Event).where(Event.evt_title.contains(event_title))).all()

        for event in query:
            events.append(event[0])

        return events

    def update_event(self, event_id, new_event_number=None, new_event_title=None):
        event = self.session.get(Event, event_id)

        if new_event_number:
            event.evt_number = new_event_number

        if new_event_title:
            event.evt_title = new_event_title

        self.session.commit()

    def delete_event(self, event_id):

        event = self.session.get(Event, event_id)

        try:
            self.session.delete(event)

            self.session.commit()
        except UnmappedInstanceError:
            raise EventNotExists