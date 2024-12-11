from aiogram.types import Message

from config.settings import settings
from db.schemas.music import Base as BaeMusic
from db.utils.music import get_music
from . import bot


async def authenticate_chat_id(message: Message):
    if str(message.chat.id) in settings.ALLOWED_CHANNEL_IDS:
        return True

    await message.answer(
        "ااییییی اااااحححمققق. الحق که عمت خرابه، قرار بود به کسی منو ندی که چاقال"
        + f"\n chatid: {message.chat.id}"
    )
    await bot.leave_chat(message.chat.id)
    print(f"kooni detected, leaving: {message.chat.id}")
    return False


async def is_music_already_sent(chat_id: int | str, audio_name: str):
    music = await get_music(
        BaeMusic.model_validate({"chat_id": str(chat_id), "audio_name": audio_name})
    )

    return music is not None
