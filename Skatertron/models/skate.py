from sqlalchemy import ForeignKey, String, Integer, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from Skatertron.enums.footage_exceptions import FootageExceptions

from . import Base


class Skate(Base):
    __tablename__ = "skates"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    skater_name: Mapped[str] = mapped_column(String(40))
    footage_exceptions: Mapped[FootageExceptions] = mapped_column(SQLEnum(FootageExceptions), nullable=True)
    skate_position: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"Entry {self.id!r}: Event ID = {self.event_id!r} skater = {self.skater_name!r}"
