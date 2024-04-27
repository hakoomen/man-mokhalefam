from attr import dataclass
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, delete
from contextlib import asynccontextmanager

from env import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()


class MessagePoll(Base):
    __tablename__ = "message_polls"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, index=True)
    audio_message_id = Column(String, index=True)
    poll_message_id = Column(String, index=True)
    poll_id = Column(String, index=True, unique=True)
    audio_name = Column(String)


@dataclass
class MessagePollDataClass:
    chat_id: str
    audio_message_id: str
    poll_message_id: str
    poll_id: str
    audio_name: str


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise


async def get_message_info(poll_id: str) -> None | MessagePollDataClass:
    async with get_session() as session:
        statement = select(MessagePoll).where(MessagePoll.poll_id == poll_id)
        result = await session.execute(statement)
        message_poll = result.scalars().first()
        if not message_poll:
            return None
        return MessagePollDataClass(
            chat_id=message_poll.chat_id,
            audio_message_id=message_poll.audio_message_id,
            poll_message_id=message_poll.poll_message_id,
            poll_id=message_poll.poll_id,
            audio_name=message_poll.audio_name,
        )


async def delete_message(poll_id: str):
    async with get_session() as session:
        statement = delete(MessagePoll).where(MessagePoll.poll_id == poll_id)
        await session.execute(statement)


async def add_message(
    chat_id: int | str,
    audio_message_id: int | str,
    poll_message_id: int | str,
    poll_id: int | str,
    audio_name: str,
):
    async with get_session() as session:
        new_mapping = MessagePoll(
            chat_id=str(chat_id),
            audio_message_id=str(audio_message_id),
            poll_message_id=str(poll_message_id),
            poll_id=str(poll_id),
            audio_name=str(audio_name),
        )
        session.add(new_mapping)
