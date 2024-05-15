from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Competition(Base):
    __tablename__ = "competitions"

    id: Mapped[int] = mapped_column(primary_key=True)
    competition_name: Mapped[str] = mapped_column(String(60))
    competition_year: Mapped[int] = mapped_column(Integer)
    host_club: Mapped[str] = mapped_column(String(60))

    def __repr__(self) -> str:
        return f"Entry {self.id!r}: {int(self.competition_year)!r} {self.competition_name!r}"
