from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"))
    event_number: Mapped[str] = mapped_column(String(4))
    event_name: Mapped[str] = mapped_column(String(60))

    def __repr__(self) -> str:
        return f"Entry {self.id!r}: #{int(self.event_number)!r} {self.event_name!r}"
