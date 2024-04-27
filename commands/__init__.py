from aiogram import Bot, Dispatcher
from config.settings import settings

dp = Dispatcher()
bot = Bot(token=settings.TELEGRAM_TOKEN)


async def start():
    from . import commands

    await dp.start_polling(bot)
