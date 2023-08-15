import sqlite_backend
import skatertron_exceptions as sk8_exc
import os

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

    def read_event_name(self, event_number):
        return sqlite_backend.select_event_name(self.connection, event_number)

    def read_skaters_in_event(self, event_number):
        return sqlite_backend.select_skates_by_event(self.connection, event_number)

    def read_all(self, table_name):
        return sqlite_backend.select_all(self.connection, table_name)

    def read_events_by_skater(self, skater_name):
        return sqlite_backend.select_events_by_skater(self.connection, skater_name)

    def delete_event(self, event_number):
        sqlite_backend.delete_event(self.connection, event_number)

    def delete_skate(self, event_number, skater_name):
        sqlite_backend.delete_skate(self.connection, event_number, skater_name)

class Event_Table():
    def __init__(self):
        self.cwd = os.getcwd()

    

        
    '''
    @property
    def server(self):
        return self.server

    def connect_to_server(self, connection_name):
        server_path = f"{connection_name}.db"

        try:
            print(f"successfully loaded: {server_path}")
            self._server = sqlite3.connect(server_path)
            self._cursor = self.server.cursor()
        except OSError as e:
            print(e)

    @property
    def cursor(self):
        return(self._cursor)        

    def create_table(self, create_table_sql):        
        try:
            self.cursor.execute(create_table_sql)
        except Error as e:
            print(e)

    
    def add_event(self, event_dict):
        event_number = event_dict["num"]
        event_name = event_dict["name"]
        skaters = event_dict["skaters"]

        event_exists = self.cursor.execute("SELECT FROM events WHERE evt_number = (?)", (event_number,)).fetchall()

        if not event_exists:
            self.cursor.execute("INSERT INTO events VALUES(?,?)", (event_number, event_name))
        
        event_id = self.cursor.execute("SELECT FROM events WHERE evt_number = (?)", (event_number,)).fetchall()
        
        for skater in skaters:
            self.cursor.execute("INSERT INTO skates VALUES(?,?)", (event_id, skater))
        print(f"inserted {event_number} {event_name} into table")

    def get_skates_all(self):
        skates = self.cursor.execute("SELECT event_name, skater, file FROM skates")

        return(skates.fetchall())

    def get_skates_by_evt(self, evt):
        skates = self.cursor.execute("SELECT event_name, skater, file FROM skates WHERE event_name = (?)", (evt,))

        return(skates.fetchall())

    def get_skates_by_skater(self, skater):
        skates = self.cursor.execute("SELECT event_name, skater, file FROM skates WHERE skater = (?)", (skater,))

        return(skates.fetchall())

    def get_skates_with_files(self):
        skates = self.cursor.execute("SELECT * FROM skates WHERE file IS NOT NULL")

        return(skates.fetchall())

    def process_files(self):
        skates = self.get_skates_with_files()

        for skate in skates:
            evt = skate[0]
            sk8r = skate[1]
            fn = f"{sk8r} - {evt[6:]}.txt"
            path = f"{evt}/{fn}"
            
            try:
                os.mkdir(evt)
                print("making directory")
            except FileExistsError:
                print("directory exists")
            
            os.rename(skate[2],path)
            print("renamed")
            self.assign_file(evt,sk8r,path)
            
        self.server.commit()
        print("server updated")


    def assign_file(self, evt, skater, file):
        self.cursor.execute(f"UPDATE skates SET file = (?) WHERE event_name = (?) AND skater = (?)", (file, evt, skater))

    def delete(self):
        self.cursor.execute("DELETE FROM skates")

    def export_events(self):
        self.server.commit()


    '''

if __name__ == '__main__':
    m = ModelSQLite()
