from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import mapped_column, Mapped

from db.schemas.poll_options import PollOptions

from .base import Base


class MessagePoll(Base):
    __tablename__ = "message_polls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chat_id: Mapped[str] = mapped_column(String, index=True)
    audio_message_id: Mapped[str] = mapped_column(String, index=True)
    poll_message_id: Mapped[str] = mapped_column(String, index=True)
    poll_id: Mapped[str] = mapped_column(String, index=True, unique=True)
    audio_name: Mapped[str] = mapped_column(String)
    audio_owner_user_id: Mapped[str] = mapped_column(String)
    audio_owner_selected_option: Mapped[PollOptions] = mapped_column(
        Enum(PollOptions, validate_strings=True), default=PollOptions.NONE
    )  # -1 -> didn't select anything [0,1] are based on poll_options.py
