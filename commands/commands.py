from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message, ContentType, Poll
from db.schemas.message_poll import (
    MessagePollCreate,
    MessagePollRead,
)
from db.schemas.music import MusicCreate
from db.schemas.poll_options import PollOptions
from db.utils.message_poll import (
    create_poll_info,
    get_poll_info,
    delete_poll_info,
)
from db.utils.music import create_music
from .utils import authenticate_chat_id, is_music_already_sent
from . import dp, bot


@dp.message(CommandStart())
async def send_welcome(message: Message):
    if not await authenticate_chat_id(message):
        return

    print(f"added to group: {message.chat.id}")
    await message.answer("من برای مخالفت اومدم")


@dp.message(F.content_type.is_(ContentType.AUDIO))
async def handle_music(message: Message):
    if (
        not await authenticate_chat_id(message)
        or not message.audio
        or not message.audio.file_name
    ):
        return

    if await is_music_already_sent(message.chat.id, message.audio.file_name):
        await bot.send_message(
            message.chat.id, "آهنگ تکراریه", reply_to_message_id=message.message_id
        )
        await bot.delete_message(message.chat.id, message.message_id)
        return

    music = await create_music(
        MusicCreate.model_validate(
            {
                "chat_id": str(message.chat.id),
                "audio_name": str(message.audio.file_name),
            }
        )
    )

    # Send a poll as a reply to the music message
    poll = await message.reply_poll(
        question=f"با {message.audio.file_name} مخالفی؟ (کسی که فرستاده اگه با خودشم مخالف نیست لطفا موافقت کنه)",
        options=PollOptions.as_list(),  # type: ignore
        is_anonymous=False,
        allows_multiple_answers=False,
    )

    if (
        poll is None
        or poll.poll is None
        or message.audio is None
        or message.from_user is None
    ):
        return

    await create_poll_info(
        MessagePollCreate.model_validate(
            {
                "chat_id": str(message.chat.id),
                "audio_message_id": str(message.message_id),
                "poll_message_id": str(poll.message_id),
                "poll_id": str(poll.poll.id),
                "audio_owner_user_id": str(message.from_user.id),
                "music_id": music.id,
            }
        )
    )

    print("music poll created")


# TODO: poll_answer and poll events are called concurrently so doing this is useless
# @dp.poll_answer()
# async def handle_poll_answer(poll_answer: PollAnswer):
#     if poll_answer.bot.id != bot.id:
#         return

#     poll_info = await get_poll_info(poll_answer.poll_id)
#     if poll_info is None:
#         return

#     if str(poll_answer.user.id) != poll_info.audio_owner_user_id:
#         return

#     selected_option: PollOptions = PollOptions.NONE
#     if PollOptions.agree_index() in poll_answer.option_ids:
#         selected_option = PollOptions.AGREE
#         print("dude agrees with himself")

#     if PollOptions.disagree_index() in poll_answer.option_ids:
#         selected_option = PollOptions.DISAGREE
#         print("dude disagrees with himself")

#     await set_audio_owner_vote(
#         MessagePollUpdate.model_validate(
#             {
#                 "poll_id": poll_info.poll_id,
#                 "audio_owner_selected_option": selected_option,
#             }
#         )
#     )


@dp.poll()
async def handle_poll(poll: Poll):
    if not poll.bot or poll.bot.id != bot.id:
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
            int(poll_info.audio_message_id),
        )
        await bot.stop_poll(poll_info.chat_id, int(poll_info.poll_message_id))
        await delete_poll_info(poll_info.poll_id)
        print("mokhalefat accepted")
    elif votes[PollOptions.agree_index()] > member_count / 2:
        # Check if majority likes the song
        await bot.delete_message(poll_info.chat_id, int(poll_info.poll_message_id))
        await delete_poll_info(poll_info.poll_id)
        print("mofaveghat accepted")


def _get_agree_and_disagree_vote_count(poll: Poll, poll_info: MessagePollRead):
    number_of_voters_agreed = 0
    number_of_voters_disagreed = 0

    for option in poll.options:
        if option.text == PollOptions.DISAGREE:
            number_of_voters_disagreed = option.voter_count

        if option.text == PollOptions.AGREE:
            number_of_voters_agreed = option.voter_count

    # TODO:
    # if poll_info.audio_owner_selected_option == PollOptions.AGREE:
    #     number_of_voters_agreed -= 1

    # if poll_info.audio_owner_selected_option == PollOptions.DISAGREE:
    #     number_of_voters_disagreed -= 1
    result = [0, 0]
    result[PollOptions.agree_index()] = number_of_voters_agreed
    result[PollOptions.disagree_index()] = number_of_voters_disagreed
    return result
