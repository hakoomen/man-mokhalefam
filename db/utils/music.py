from sqlalchemy import select
from db import get_session
from db.models.music import Music
from db.schemas.music import MusicRead, MusicCreate


async def get_music(music: MusicRead) -> None | MusicRead:
    async with get_session() as session:
        result = await session.execute(
            select(Music).filter(
                Music.chat_id == music.chat_id,
                Music.audio_name == music.audio_name.strip().lower(),
            )
        )
        first_row = result.scalars().first()
        if not first_row:
            return None
        return MusicRead.model_validate(first_row)


async def create_music(music: MusicCreate):
    async with get_session() as session:
        new_music = Music(**music.model_dump())
        session.add(new_music)
