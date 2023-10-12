from hypothesis import given
from hypothesis.strategies import text

import Skatertron.postgres_backend as pg_backend
import Skatertron.sqlalchemy_backend as sqlalchemy_backend
import config.config as user_data


def test_postgres_connection():
    pw = user_data.Config.pw()
    con = pg_backend.connect_to_db(pw)
    cur = con.cursor()

    print(con)
    print(cur)


def test_sqlalchemy_connection():
    engine = sqlalchemy_backend.connect_to_db()

    print(engine)


if __name__ == "__main__":
    test_postgres_connection()
    test_sqlalchemy_connection()
