from archive.sqlalchemy_backend import connect_to_db, Base, Event, Skate, File

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from skatertron_exceptions import EventExists, EventNotExists, SkateIDNotExists, FileNotExist


class BaseController(object):
    def __init__(self, competition="test"):
        self.competition = competition

        self.engine = connect_to_db(self.competition)

        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()


class EventController(object):
    def __init__(self, session):
        self.session = session

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
        query = self.session.execute(select(Event).where(Event.event_name.contains(event_title))).all()

        for event in query:
            events.append(event[0])

        return events

    def update_event(self, event_id, new_event_number=None, new_event_title=None):
        event = self.session.get(Event, event_id)

        if new_event_number:
            event.event_number = new_event_number

        if new_event_title:
            event.event_name = new_event_title

        self.session.commit()

    def delete_event(self, event_id):

        event = self.session.get(Event, event_id)

        try:
            self.session.delete(event)

            self.session.commit()
        except UnmappedInstanceError:
            raise EventNotExists


class SkateController(object):
    def __init__(self, session):
        self.session = session

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

    def read_skates_by_skater(self, skater_name):
        skates = []
        query = self.session.execute(select(Skate).where(Skate.skater_name.contains(skater_name))).all()

        for skate in query:
            skates.append(skate[0])

        return skates

    def update_skate(self, skate_id, new_event_id=None, new_skater_name=None):
        skate = self.session.get(Skate, skate_id)

        if new_event_id:
            skate.event_id = new_event_id

        if new_skater_name:
            skate.skater_name = new_skater_name

        self.session.commit()

    def delete_skate(self, skate_id):

        skate = self.session.get(Skate, skate_id)

        try:
            self.session.delete(skate)

            self.session.commit()
        except UnmappedInstanceError:
            raise SkateIDNotExists


class FileController(object):
    def __init__(self, session):
        self.session = session
        self.skate_controller = SkateController(self.session)

    def create_file(self, skate_id, filepath):
        file = File(skate_id=skate_id, file=filepath)

        try:
            self.session.add(file)

            self.session.commit()
        except IntegrityError:
            raise EventNotExists

    def read_all_files(self):
        files = []

        query = self.session.execute(select(File)).scalars()

        for file in query:
            files.append(file)
        return files

    def read_file_by_id(self, file_id):
        file = self.session.get(File, file_id)
        return file

    def read_files_by_skate(self, skate_id):
        files = []
        query = self.session.execute(select(File).filter_by(skate_id=skate_id)).all()

        for skate in query:
            files.append(skate[0])
        return files

    def read_files_by_skater_name(self, skater_name):
        files = []

        skates = self.skate_controller.read_skates_by_skater(skater_name)

        for skate in skates:
            print(skate.id)
            query = self.session.execute(select(File).filter_by(skate_id=skate.id)).all()

            for file in query:
                files.append(file[0])

        return files

    def update_file(self, file_id, new_skate_id=None, new_filepath=None):
        file = self.session.get(File, file_id)

        if new_skate_id:
            file.skate_id = new_skate_id

        if new_filepath:
            file.file_name = new_filepath

        self.session.commit()

    def delete_file(self, file_id):

        file = self.session.get(File, file_id)

        try:
            self.session.delete(file)

            self.session.commit()
        except UnmappedInstanceError:
            raise FileNotExist