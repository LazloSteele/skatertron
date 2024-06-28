from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    skate_id: Mapped[int] = mapped_column(ForeignKey("skates.id"))
    file_name: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"Entry {self.id!r}: Skate ID = {self.skate_id!r} filepath = {self.file_name!r}"
