import sqlite_backend
import skatertron_exceptions as sk8_exc

class ModelSQLite(object):

    def __init__(self):
        self._config = [
    "CREATE TABLE IF NOT EXISTS events(id integer PRIMARY KEY, evt_number text UNIQUE, evt_title text NOT NULL)",
    "CREATE TABLE IF NOT EXISTS skates(id integer PRIMARY KEY, evt_id integer NOT NULL, skater text NOT NULL)",
    "CREATE TABLE IF NOT EXISTS files(id integer PRIMARY KEY, skate_id integer NOT NULL, file text NOT NULL)",
    "CREATE TABLE IF NOT EXISTS orders(id integer PRIMARY KEY, name text NOT NULL, email text NOT NULL)",
    "CREATE TABLE IF NOT EXISTS order_items(id integer PRIMARY KEY, order_id integer NOT NULL, file_name text NOT NULL)"
    ]
        self._connection = self.connection = None
        self._comp_name = self.comp_name = None
        self._application_state = self.application_state = 'init'

    @property
    def application_state(self):
        return self._application_state

    @application_state.setter
    def application_state(self, new_state):
        self._application_state = new_state

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, connection):
        self._connection = sqlite_backend.connect_to_db(connection)
        self.comp_name = connection

        for table_sql in self._config:
            sqlite_backend.create_table(self.connection, table_sql)

    @property
    def comp_name(self):
        return self._comp_name

    @comp_name.setter
    def comp_name(self, new_name):
        self._comp_name = new_name

    def create_event(self, event_dict):
        sqlite_backend.add_event(self.connection, event_dict)

    def add_file(self, skate, file):
        skate_filenames = self.read_files_by_skate(skate)
        if file in self.read_files_by_skate(skate):
            raise sk8_exc.FileExistsInSkate()
        else:
            sqlite_backend.add_file(self.connection, skate, file)
        
    def read_files(self, event_number):
        return sqlite_backend.select_files_by_event(self.connection, event_number)

    def read_files_by_skate(self, skate):
        return sqlite_backend.select_files_by_skate(self.connection, skate)

    def read_file_id(self, skate_id):
        file_ids = []

        file_ids = sqlite_backend.select_file_id_by_skate(self.connection, skate_id)

        return (file_ids)

    def rename_file(self, file_id):
        pass

    def read_event_name(self, event_number):
        return sqlite_backend.select_event_name(self.connection, event_number)

    def read_skaters_in_event(self, event_number):
        return sqlite_backend.select_skates_by_event(self.connection, event_number)

    def read_all(self, table_name):
        return sqlite_backend.select_all(self.connection, table_name)

    def read_events_by_skater(self, skater_name):
        return sqlite_backend.select_events_by_skater(self.connection, skater_name)

    def read_skate(self, event_number, skater):
        return sqlite_backend.select_skate(self.connection, event_number, skater)

    def delete_event(self, event_number):
        sqlite_backend.delete_event(self.connection, event_number)

    def delete_skate(self, event_number, skater_name):
        sqlite_backend.delete_skate(self.connection, event_number, skater_name)

    def delete_file(self, file_id):
        sqlite_backend.delete_file(self.connection, file_id)

if __name__ == '__main__':

    m = ModelSQLite()

