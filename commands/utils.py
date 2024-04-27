from aiogram.types import Message

from config.settings import settings
from . import bot


async def authenticate_chat_id(message: Message):
    if str(message.chat.id) in settings.ALLOWED_CHANNEL_IDS:
        return True

    await message.answer("ای سینای اااااحححمققق. الحق که عمت خرابه")
    await bot.leave_chat(message.chat.id)
    print(f"kooni detected, leaving: {message.chat.id}")
    return False
