from typing import TypedDict
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message, ContentType, Poll, PollAnswer
from config.settings import settings
from db.schemas.message_poll import MessagePollBase, MessagePollUpdate, MessagePollRead
from db.schemas.poll_options import PollOptions
from db.utils.message_poll import (
    create_poll_info,
    get_poll_info,
    delete_poll_info,
    set_audio_owner_vote,
)
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
    poll = await message.reply_poll(
        question=f"با {message.audio.file_name} مخالفی؟ (نظر کسی که آهنگو فرستاده اندازه پشم مهم نیست، لذا رای شخص گرامی به حساب نمیاد)",
        options=PollOptions.as_list(),
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
                "audio_owner_user_id": str(message.from_user.id),
            }
        )
    )
    print("music poll created")


@dp.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer):
    if poll_answer.bot.id != bot.id:
        return

    poll_info = await get_poll_info(poll_answer.poll_id)
    if poll_info is None:
        return

    if poll_answer.user.id != poll_info.audio_owner_user_id:
        return

    selected_option: PollOptions = PollOptions.NONE
    if PollOptions.agree_index in poll_answer.option_ids:
        selected_option = PollOptions.AGREE

    if PollOptions.disagree_index in poll_answer.option_ids:
        selected_option = PollOptions.DISAGREE

    await set_audio_owner_vote(
        MessagePollUpdate.model_validate(
            {
                "poll_id": poll_info.poll_id,
                "audio_owner_selected_option": selected_option,
            }
        )
    )


@dp.poll()
async def handle_poll(poll: Poll):
    if poll.bot.id != bot.id:
        return

    if len(poll.options) != len(PollOptions.as_list()):
        return

    poll_info = await get_poll_info(poll.id)
    if poll_info is None:
        return

    # Fetch the chat to find out the number of members
    chat = await bot.get_chat(poll_info.chat_id)
    member_count = await chat.get_member_count() - 1  # -1 for the bot

    votes = _get_agree_and_disagree_vote_count(poll, poll_info)

    if votes[PollOptions.disagree_index()] >= member_count / 2:
        # Check if the majority dislikes the song
        await bot.delete_message(
            poll_info.chat_id,
            poll_info.audio_message_id,
        )
        await bot.stop_poll(poll_info.chat_id, poll_info.poll_message_id)
        await delete_poll_info(poll_info.poll_id)
        print("mokhalefat accepted")
    elif votes[PollOptions.agree_index()] > member_count / 2:
        # Check if majority likes the song
        await bot.delete_message(poll_info.chat_id, poll_info.poll_message_id)
        print("mofaveghat accepted")


def _get_agree_and_disagree_vote_count(poll: Poll, poll_info: MessagePollRead):
    number_of_voters_agreed = 0
    number_of_voters_disagreed = 0

    for option in poll.options:
        if option.text == PollOptions.DISAGREE:
            number_of_voters_disagreed = option.voter_count

        if option.text == PollOptions.AGREE:
            number_of_voters_agreed = option.voter_count

    if poll_info.audio_owner_selected_option == PollOptions.AGREE:
        number_of_voters_agreed -= 1

    if poll_info.audio_owner_selected_option == PollOptions.DISAGREE:
        number_of_voters_disagreed -= 1

    return [number_of_voters_agreed, number_of_voters_disagreed]
