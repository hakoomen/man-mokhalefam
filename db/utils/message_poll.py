from sqlalchemy import delete, select, update
from db import get_session
from db.models.message_poll import MessagePoll as MessagePollModel
from db.schemas.message_poll import (
    MessagePollCreate,
    MessagePollRead as MessagePollSchema,
    MessagePollUpdate,
)


async def get_poll_info(poll_id: str) -> None | MessagePollSchema:
    async with get_session() as session:
        statement = select(MessagePollModel).where(MessagePollModel.poll_id == poll_id)
        result = await session.execute(statement)
        message_poll = result.scalars().first()
        if not message_poll:
            return None

        return MessagePollSchema.model_validate(message_poll)


async def set_audio_owner_vote(update_info: MessagePollUpdate):
    async with get_session() as session:
        statement = (
            update(MessagePollModel)
            .where(MessagePollModel.poll_id == update_info.poll_id)
            .values(
                {"audio_owner_selected_option": update_info.audio_owner_selected_option}
            )
        )
        await session.execute(statement)


async def delete_poll_info(poll_id: str):
    async with get_session() as session:
        statement = delete(MessagePollModel).where(MessagePollModel.poll_id == poll_id)
        await session.execute(statement)


async def create_poll_info(info: MessagePollCreate):
    async with get_session() as session:
        new_mapping = MessagePollModel(**info.model_dump())
        session.add(new_mapping)
