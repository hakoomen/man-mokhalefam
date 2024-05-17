from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

from config.settings import settings

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL, echo=settings.IS_SQLALCHEMY_LOG_ENABLED
)

AsyncSessionLocal: sessionmaker[AsyncSession] = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def init_db():
    from db.models.music import Music
    from db.models.message_poll import MessagePoll  # TODO: find a way to dont need this
    from db.models.base import Base

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
