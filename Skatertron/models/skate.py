from sqlalchemy import ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class Skate(Base):
    __tablename__ = "skates"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    skater_name: Mapped[str] = mapped_column(String(40))
    no_video: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='false')
    skate_position: Mapped[int] = mapped_column(Integer)

    event = relationship("Event", backref="skates")

    def to_dict(self):
        obj_dict = {column.key: getattr(self, column.key) for column in self.__mapper__.columns}
        return obj_dict

    def __repr__(self) -> str:
        return f"Entry {self.id!r}: Event ID = {self.event_id!r} skater = {self.skater_name!r}"
