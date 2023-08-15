import sqlite3
from sqlite3 import OperationalError, IntegrityError, ProgrammingError
import skatertron_exceptions

DB_name = None

def connect_to_db(db=None):
    """Connect to a sqlite DB. Create the database if there isn't one yet.

    Open a connection to a SQLite DB (either a DB file or an in-memory DB).
    When a database is accessed by multiple connections, and one of the
    processes modifies the database, the SQLite database is locked until that
    transaction is committed.

    Parameters
    ----------
    db : str
        database name (without .db extension). If None, create an In-Memory DB.

    Returns
    -------
    connection : sqlite3.Connection
        connection object
    """
    if db is None:
        mydb = ':memory:'
        print('New connection to in-memory SQLite DB...')
    else:
        mydb = f'competitions\\{db}.db'
        print('New connection to SQLite DB...')
    connection = sqlite3.connect(mydb)
    return connection

def connect(func):
    
    """Decorator to (re)open a sqlite database connection when needed.

    A database connection must be open when we want to perform a database query
    but we are in one of the following situations:
    1) there is no connection
    2) the connection is closed

    Parameters
    ----------
    func : function
        function which performs the database query

    Returns
    -------
    inner func : function
    """
    
    def inner_func(conn, *args, **kwargs):
        try:
            # I don't know if this is the simplest and fastest query to try
            conn.execute(
                'SELECT name FROM sqlite_temp_master WHERE type="table";')
        except (AttributeError, ProgrammingError):
            conn = connect_to_db(DB_name)
        return func(conn, *args, **kwargs)
    return inner_func

def disconnect_from_db(db=None, conn=None):
    if db is not DB_name:
        print("You are trying to disconnect from the wrong DB")
    if conn is not None:
        conn.close()

@connect
def create_table(conn, create_table_sql):
    try:
        conn.execute(create_table_sql)
    except OperationalError as e:
        print(e)

def scrub(input_string):
    """Clean an input string (to prevent SQL injection).

    Parameters
    ----------
    input_string : str

    Returns
    -------
    str
    """
    return ''.join(k for k in input_string if k.isalnum())

@connect
def add_event(conn, event_dict):
    event_number = event_dict["num"]
    event_name = event_dict["name"]
    skaters = event_dict["skaters"]

    try:
        conn.execute("INSERT INTO events VALUES(NULL, ?, ?)", (event_number, event_name))
        print(f"inserted {event_number} {event_name} into the events table")
        event_id = conn.execute("SELECT id FROM events WHERE evt_number = (?)", (event_number,)).fetchone()[0]
        
        for skater in skaters:
            conn.execute("INSERT INTO skates VALUES(NULL, ?, ?)", (event_id, skater))
            print(f"inserted {skater} into the skates table under event id {event_id}")
    except IntegrityError as e:
        print(f"{e}: event number {event_number} was already stored in the events table as {event_name}")

    conn.commit()

@connect
def add_file(conn, skate, file):
    try:
        conn.execute("INSERT INTO files VALUES(NULL, ?, ?)", (skate, file))
        print(f"inserted {file} into the files table")
    except IntegrityError as e:
        print(f"{e}: {file} was already stored in the files table under skate id {skate}")
    conn.commit()

@connect
def delete_event(conn, event_number):
    c = conn.execute('SELECT EXISTS(SELECT 1 FROM events WHERE evt_number=? LIMIT 1)', (event_number,))
    result = c.fetchone()

    if result[0]:
        event_id = conn.execute("SELECT id FROM events WHERE evt_number = (?)", (event_number,)).fetchone()[0]
        
        conn.execute('DELETE FROM events WHERE evt_number=?', (event_number,))
        conn.execute('DELETE FROM skates WHERE evt_id=?', (event_id,))   
        
        conn.commit()
    else:
        raise skatertron_exceptions.EventNotExists(f"Cannot delete event #{event_number} because it does not exist in the events table.")

@connect
def delete_skate(conn, event_number, skater_name):
    c = conn.execute('SELECT EXISTS(SELECT 1 FROM events WHERE evt_number=? LIMIT 1)', (event_number,))
    result = c.fetchone()

    if result[0]:
        event_id = conn.execute("SELECT id FROM events WHERE evt_number = (?)", (event_number,)).fetchone()[0]
        
        conn.execute('DELETE FROM skates WHERE evt_id=? AND skater=?', (event_id,skater_name))   
        
        conn.commit()
    else:
        raise skatertron_exceptions.EventNotExists(f"Cannot delete event #{event_number} because it does not exist in the events table.")

@connect
def select_skate(conn, event_number, skater):
    result = None

    try:
        event_id = conn.execute(f'SELECT id FROM events WHERE evt_number="{event_number}"').fetchone()[0] 
        result = conn.execute(f'SELECT id FROM skates WHERE evt_id="{event_id} AND skater="{skater}"').fetchone()[0]
    except TypeError as e:
        print(e)

    if result is not None:
        return result
    else:
        raise skatertron_exceptions.EventNotExists(
            'Can\'t read event number "{event_number}" because it\'s not stored in table'
            )    

@connect
def select_event_name(conn, event_number):
    result = None

    try:
        result = conn.execute(f'SELECT * FROM events WHERE evt_number="{event_number}"').fetchone()[2]
    except TypeError as e:
        print(e)

    if result is not None:
        return result
    else:
        raise skatertron_exceptions.EventNotExists(
            'Can\'t read event number "{event_number}" because it\'s not stored in table'
            )

@connect
def select_skates_by_event(conn, event_number):
    result = None

    try:
        event_id = conn.execute(f'SELECT * FROM events WHERE evt_number="{event_number}"').fetchone()[0]
        result_tuple = conn.execute(f'SELECT * FROM skates WHERE evt_id="{event_id}"').fetchall()

        result = []
        
        for event in result_tuple:
            result.append(event[2])
    except TypeError as e:
        print(e)
    
    if result is not None:
        return result
    else:
        raise skatertron_exceptions.EventNotExists(
            'Can\'t read event number "{event_number}" because it\'s not stored in table'
            )

@connect
def select_events_by_skater(conn, skater_name):
    result = None

    try:
        event_id_list = conn.execute(f'SELECT evt_id FROM skates WHERE skater="{skater_name}"').fetchall()
        result = []
        print(event_id_list)
        for event in event_id_list:
            result += conn.execute(f'SELECT evt_number, evt_title FROM events WHERE id="{event[0]}"').fetchall()
            print(result)
    except TypeError as e:
        print(e)
    
    if result is not None:
        return result
    else:
        raise skatertron_exceptions.EventNotExists(
            'Can\'t read event number "{event_number}" because it\'s not stored in table'
            )

@connect
def select_all(conn, table_name):
    table_name = scrub(table_name)
    sql = f'SELECT * FROM {table_name}'
    c = conn.execute(sql)
    results = c.fetchall()
    return results

def main():

    '''
    This main function is meant to sloppily test the functionality of this module without wiring it up to the model.
    '''


    conn = connect_to_db()  # in-memory database
    # conn = connect_to_db(DB_name)  # physical database (i.e. a .db file)

    table_config = [
    "CREATE TABLE IF NOT EXISTS events(id integer PRIMARY KEY, evt_number text UNIQUE, evt_title text NOT NULL)",
    "CREATE TABLE IF NOT EXISTS skates(id integer PRIMARY KEY, evt_id integer NOT NULL, skater text NOT NULL)",
    "CREATE TABLE IF NOT EXISTS files(id integer PRIMARY KEY, skate_id integer NOT NULL, file text NOT NULL)",
    "CREATE TABLE IF NOT EXISTS orders(id integer PRIMARY KEY, name text NOT NULL, email text NOT NULL)",
    "CREATE TABLE IF NOT EXISTS order_items(id integer PRIMARY KEY, order_id integer NOT NULL, file_name text NOT NULL)"
    ]

    for table_sql in table_config:
        print(table_sql)
        create_table_sql = table_sql
        create_table(conn, create_table_sql)

    evt_41 = {
            "num": "41",
            "name": "Test Event",
            "skaters": ["Sarah Flubber", "Farah Schlubber", "Tarah Tubber"]
            }
    evt_42 = {
            "num": "42",
            "name": "Test Event Freeskate",
            "skaters": ["Sarafsaah Faas", "Farasdfah Scasss", "Tarasdfah Tasdf"]
            }
    
    # CREATE
    add_event(conn, evt_41)
    add_event(conn, evt_42)
    
    # if we try to insert an object already stored we get an ItemAlreadyStored
    # exception
    add_event(conn, evt_41)

    # READ
    print('SELECT evt 41')
    print(select_skates_by_event(conn, '41'))
    print('SELECT evt 42')
    print(select_skates_by_event(conn, '42'))
    print('SELECT all')
    print(select_all(conn, 'events'))
    print(select_all(conn, 'skates'))
    # if we try to select an object not stored we get an ItemNotStored exception
    # print(select_one(conn, 'pizza', table_name='items'))

    # conn.close()  # the decorator @connect will reopen the connection

    # UPDATE
    print('UPDATE coming soon')
    #update_one(conn, 'bread', price=1.5, quantity=5, table_name='items')
    #print(select_one(conn, 'bread', table_name='items'))
    # if we try to update an object not stored we get an ItemNotStored exception
    # print('UPDATE pizza')
    # update_one(conn, 'pizza', price=1.5, quantity=5, table_name='items')

    # DELETE
    print('DELETE evt 42, SELECT evt 42')
    delete_event(conn, '42')
    #print(select_skates_by_event(conn, '42'))
    # if we try to delete an object not stored we get an ItemNotStored exception
    # print('DELETE fish')
    # delete_one(conn, 'fish', table_name='items')

    # save (commit) the changes
    # conn.commit()

    # close connection
    conn.close()
    
if __name__ == '__main__':
    main()
