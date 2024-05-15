from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Skate(Base):
    __tablename__ = "skates"

    id: Mapped[int] = mapped_column(primary_key=True)
    evt_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    skater: Mapped[str] = mapped_column(String(40))

    def __repr__(self) -> str:
        return f"Entry {self.id!r}: Event ID = {self.evt_id!r} skater = {self.skater!r}"
