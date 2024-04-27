from sqlalchemy import delete, select
from db import get_session
from db.models.message_poll import MessagePoll as MessagePollModel
from db.schemas.message_poll import MessagePoll as MessagePollSchema


async def get_message_info(poll_id: str) -> None | MessagePollSchema:
    async with get_session() as session:
        statement = select(MessagePollModel).where(MessagePollModel.poll_id == poll_id)
        result = await session.execute(statement)
        message_poll = result.scalars().first()
        if not message_poll:
            return None

        return MessagePollSchema.model_validate(message_poll)


async def delete_message(poll_id: str):
    async with get_session() as session:
        statement = delete(MessagePollModel).where(MessagePollModel.poll_id == poll_id)
        await session.execute(statement)


async def add_message(
    chat_id: int | str,
    audio_message_id: int | str,
    poll_message_id: int | str,
    poll_id: int | str,
    audio_name: str,
):
    async with get_session() as session:
        new_mapping = MessagePollModel(
            chat_id=str(chat_id),
            audio_message_id=str(audio_message_id),
            poll_message_id=str(poll_message_id),
            poll_id=str(poll_id),
            audio_name=str(audio_name),
        )
        session.add(new_mapping)
