from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Events(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    evt_number: Mapped[str] = mapped_column(String(4), unique=True)
    evt_title: Mapped[str] = mapped_column(String(60))
    
    def __repr__(self) -> str:
        return f"Entry {self.id!r}: #{self.evt_number!r} {self.evt_title!r}"

class Skates(Base):
    __tablename__ = "skates"

    id: Mapped[int] = mapped_column(primary_key=True)
    evt_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    skater: Mapped[str] = mapped_column(String(40))
    
    def __repr__(self) -> str:
        return f"Entry {self.id!r}: Event ID = {self.evt_id!r} skater = {self.skater!r}"

class Files(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    skate_id: Mapped[int] = mapped_column(ForeignKey("skates.id"))
    file: Mapped[str] = mapped_column(String(255))
    
    def __repr__(self) -> str:
        return f"Entry {self.id!r}: Skate ID = {self.evt_id!r} filepath = {self.skater!r})"

engine = create_engine("sqlite://", echo=True)
