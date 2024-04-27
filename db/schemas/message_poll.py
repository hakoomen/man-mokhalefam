from pydantic import (
    BaseModel,
    ConfigDict,
)

from db.schemas.poll_options import PollOptions


class MessagePollBase(BaseModel):
    chat_id: str
    audio_message_id: str
    poll_message_id: str
    poll_id: str
    audio_name: str
    audio_owner_user_id: str


class MessagePollRead(MessagePollBase):
    id: int
    audio_owner_selected_option: PollOptions

    model_config = ConfigDict(from_attributes=True)


class MessagePollUpdate(BaseModel):
    poll_id: str
    audio_owner_selected_option: PollOptions


class MessagePollCreate(MessagePollBase):
    pass
