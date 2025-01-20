from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"))
    event_number: Mapped[str] = mapped_column(String(4))
    event_name: Mapped[str] = mapped_column(String(60))
    event_rink: Mapped[str] = mapped_column(String(25))
    event_position: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"#{self.event_number} {self.event_name}"
