from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, relationship, Mapped


from .base import Base


if TYPE_CHECKING:
    from db.models.message_poll import MessagePoll


class Music(Base):
    __tablename__ = "music"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chat_id: Mapped[str] = mapped_column(String, index=True)
    audio_name: Mapped[str] = mapped_column(String)

    polls: Mapped[List["MessagePoll"]] = relationship(
        back_populates="music", cascade="all, delete-orphan"
    )
