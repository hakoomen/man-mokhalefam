from pydantic import (
    BaseModel,
    ConfigDict,
)


class MessagePollBase(BaseModel):
    pass


class MessagePoll(MessagePollBase):
    id: int
    chat_id: str
    audio_message_id: str
    poll_message_id: str
    poll_id: str
    audio_name: str

    model_config = ConfigDict(from_attributes=True)
