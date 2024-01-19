from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import urllib.parse

import config.config as user_data

from enum import Enum


class UserConfig(Enum):
    USER = user_data.Config.user()
    PW = urllib.parse.quote_plus(user_data.Config.pw())


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    evt_number: Mapped[str] = mapped_column(String(4), unique=True)
    evt_title: Mapped[str] = mapped_column(String(60))

    def __repr__(self) -> str:
        return f"Entry {self.id!r}: #{int(self.evt_number)!r} {self.evt_title!r}"


class Skate(Base):
    __tablename__ = "skates"

    id: Mapped[int] = mapped_column(primary_key=True)
    evt_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    skater: Mapped[str] = mapped_column(String(40))

    def __repr__(self) -> str:
        return f"Entry {self.id!r}: Event ID = {self.evt_id!r} skater = {self.skater!r}"



class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    skate_id: Mapped[int] = mapped_column(ForeignKey("skates.id"))
    file: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"Entry {self.id!r}: Skate ID = {self.evt_id!r} filepath = {self.skater!r})"

def connect_to_db(competition):
    engine = create_engine(
        f"postgresql+psycopg://{UserConfig.USER.value}:{UserConfig.PW.value}@localhost:5432/{competition}"
    )
    if not database_exists(engine.url):
        create_database(engine.url)

    return engine
