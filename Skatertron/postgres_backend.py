import psycopg


def connect_to_db(pw, db="skatertron"):
    conn = psycopg.connect(fr"dbname={db} user=postgres password={pw}")

    return conn
