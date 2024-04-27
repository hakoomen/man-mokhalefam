from sqlalchemy import select, update, delete
from db import get_session
from db.models.message_poll import MessagePoll as MessagePollModel
from db.schemas.message_poll import (
    MessagePollCreate,
    MessagePollRead as MessagePollSchema,
    MessagePollUpdate,
)


async def get_poll_info(poll_id: str) -> None | MessagePollSchema:
    async with get_session() as session:
        result = await session.execute(
            select(MessagePollModel).filter(MessagePollModel.poll_id == poll_id)
        )
        message_poll = result.scalars().first()
        if not message_poll:
            return None
        return MessagePollSchema.model_validate(message_poll)


async def set_audio_owner_vote(update_info: MessagePollUpdate):
    async with get_session() as session:
        await session.execute(
            update(MessagePollModel)
            .filter(MessagePollModel.poll_id == update_info.poll_id)
            .values(audio_owner_selected_option=update_info.audio_owner_selected_option)
        )


async def delete_poll_info(poll_id: str):
    async with get_session() as session:
        await session.execute(
            delete(MessagePollModel).where(MessagePollModel.poll_id == poll_id)
        )


async def create_poll_info(info: MessagePollCreate):
    async with get_session() as session:
        new_poll = MessagePollModel(**info.model_dump())
        session.add(new_poll)
