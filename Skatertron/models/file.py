from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    skate_id: Mapped[int] = mapped_column(ForeignKey("skates.id"))
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String)
    file_type: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"{self.file_type} for Skate ID#{self.skate_id!r} filepath = {self.file_path}/{self.file_name!r}"
