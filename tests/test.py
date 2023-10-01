from hypothesis import given
from hypothesis.strategies import text

import Skatertron.postgres_backend as pg_backend
import config.config as user_data


def test_postgres_connection():
    pw = user_data.Config.pw()
    conn = pg_backend.connect_to_db(pw)

    print(conn)

if __name__ == "__main__":
    test_postgres_connection()
