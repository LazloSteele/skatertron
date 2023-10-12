from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

import urllib.parse

import config.config as user_data

my_config = {
    "user": user_data.Config.user(),
    "pw": urllib.parse.quote_plus(user_data.Config.pw())
}


def connect_to_db():
    engine = create_engine(f"postgresql+psycopg://{my_config['user']}:{my_config['pw']}@localhost:5432/skatertron ")
    if not database_exists(engine.url):
        create_database(engine.url)

    return engine.url