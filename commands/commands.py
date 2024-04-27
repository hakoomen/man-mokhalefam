from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message, ContentType, Poll
from config.settings import settings
from db.schemas.message_poll import MessagePollBase
from db.utils.message_poll import create_poll_info, get_poll_info, delete_poll_info
from . import dp, bot


@dp.message(CommandStart())
async def send_welcome(message: Message):
    if str(message.chat.id) not in settings.ALLOWED_CHANNEL_IDS:
        await message.answer("ای سینای اااااحححمققق. الحق که عمت خرابه")
        await bot.leave_chat(message.chat.id)
        print("kooni detected")
        return
    print("added to group")
    await message.answer("من برای مخالفت اومدم")


@dp.message(F.content_type.is_(ContentType.AUDIO))
async def handle_music(message: Message):
    # Send a poll as a reply to the music message
    options = ["من موافقم", "من مخالفم"]
    poll = await message.reply_poll(
        question=f"با {message.audio.file_name} مخالفی؟",
        options=options,
        is_anonymous=False,
        allows_multiple_answers=False,
    )
    await create_poll_info(
        MessagePollBase.model_validate(
            {
                "chat_id": str(message.chat.id),
                "audio_message_id": str(message.message_id),
                "poll_message_id": str(poll.message_id),
                "poll_id": str(poll.poll.id),
                "audio_name": str(message.audio.file_name),
            }
        )
    )
    print("music poll created")


@dp.poll()
async def handle_poll(poll: Poll):
    if poll.bot.id != bot.id:
        return

    dislike_count = poll.options[1].voter_count
    like_count = poll.options[0].voter_count

    poll_info = await get_poll_info(poll.id)
    if poll_info is None:
        return

    # Fetch the chat to find out the number of members
    chat = await bot.get_chat(poll_info.chat_id)
    member_count = await chat.get_member_count() - 1  # -1 for the bot

    if dislike_count >= member_count / 2:
        # Check if the majority dislikes the song
        await bot.delete_message(
            poll_info.chat_id,
            poll_info.audio_message_id,
        )
        await bot.stop_poll(poll_info.chat_id, poll_info.poll_message_id)
        await delete_poll_info(poll_info.poll_id)
        print("mokhalefat accepted")
    elif like_count > member_count / 2:
        # Check if majority likes the song
        await bot.delete_message(poll_info.chat_id, poll_info.poll_message_id)
        print("mofaveghat accepted")
