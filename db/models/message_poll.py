from sqlalchemy import Column, Integer, String

from .base import Base


class MessagePoll(Base):
    __tablename__ = "message_polls"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, index=True)
    audio_message_id = Column(String, index=True)
    poll_message_id = Column(String, index=True)
    poll_id = Column(String, index=True, unique=True)
    audio_name = Column(String)
