from pydantic import (
    BaseModel,
    ConfigDict,
)


class MessagePollBase(BaseModel):
    chat_id: str
    audio_message_id: str
    poll_message_id: str
    poll_id: str
    audio_name: str


class MessagePollRead(MessagePollBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MessagePollCreate(MessagePollBase):
    pass
