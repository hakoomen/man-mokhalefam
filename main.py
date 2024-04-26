import asyncio
import json
import os

from aiogram import F, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ContentType, Poll

from db import add_message, delete_message, get_message_info, init_db
from env import TELEGRAM_TOKEN, ALLOWED_CHANNEL_IDS


dp = Dispatcher()
bot = Bot(token=TELEGRAM_TOKEN)

message_to_poll_id = {}


@dp.message(CommandStart())
async def send_welcome(message: Message):
    if str(message.chat.id) not in ALLOWED_CHANNEL_IDS:
        await message.answer("ای سینای اااااحححمققق. الحق که عمت خرابه")
        await bot.leave_chat(message.chat.id)
        return
    await message.answer("من برای مخالفت اومدم")


@dp.message(F.content_type.is_(ContentType.AUDIO))
async def handle_music(message: Message):
    # Send a poll as a reply to the music message
    options = ["من موافقم", "من مخالفم"]
    poll = await message.reply_poll(
        question=f"با {message.audio.file_name} مخالفی?",
        options=options,
        is_anonymous=False,
        allows_multiple_answers=False,
    )
    await add_message(
        message.chat.id, message.message_id, poll.message_id, poll.poll.id
    )


@dp.poll()
async def handle_poll(poll: Poll):
    if poll.bot.id != bot.id:
        return

    dislike_count = poll.options[1].voter_count
    like_count = poll.options[0].voter_count

    audio_message_id, chat_id, poll_message_id, _ = await get_message_info(poll.id)
    if not audio_message_id or not chat_id or not poll_message_id:
        return

    # Fetch the chat to find out the number of members
    chat = await bot.get_chat(chat_id)
    member_count = await chat.get_member_count() - 1

    # Check if the majority dislikes the song
    if dislike_count >= member_count / 2:
        await bot.delete_messages(chat_id, [audio_message_id, poll_message_id])
        await delete_message(poll.id)
    elif like_count > member_count / 2:
        await bot.delete_message(chat_id, poll_message_id)
        await delete_message(poll.id)


async def main() -> None:
    # And the run events dispatching
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
