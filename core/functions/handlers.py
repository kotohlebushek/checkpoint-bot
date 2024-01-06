from aiogram import Bot
from aiogram.types import Message
from core.utils.messages import start_message
from core.functions.functions import get_photo

async def start_handler(message: Message, bot: Bot):
    await bot.send_message(message.chat.id, start_message)

async def send_handler(message: Message, bot: Bot):
    photo = get_photo()
    await bot.send_document(message.chat.id, photo)