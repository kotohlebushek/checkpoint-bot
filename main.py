from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import asyncio
from core.settings import settings
from core.functions.handlers import start_handler, send_handler
from core.utils.commands import set_commands

async def start_bot():
    bot = Bot(token=settings.bot.bot_token)
    await set_commands(bot)

    dp = Dispatcher()

    dp.message.register(start_handler, Command(commands=['start']))
    dp.message.register(send_handler, Command(commands=['send']))

    try:
        await dp.start_polling(bot)
    except:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start_bot())