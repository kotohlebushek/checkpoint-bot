from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import NetworkError
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from random import randint
import requests
import sqlite3

hello = """👋Привет! Ты используешь демонстрационный бот

✅В данном боте ты можешь получить фото для прохождения чекпоинта

Краткая инструкция:
1. Нажми кнопку "👨Получить фото для прохода чекпоинта"
2. Обновляй фото пока не получишь нужное тебе лицо
3. Загрузи файл себе на устройство
4. Загрузи файл с устройства в аккаунт к Цукеру (Facebook)"""

first = '👨Получить фото для прохода чекпоинта'
reload = '🔄Обновить'

TOKEN = '5403965855:AAEfs0zZVw1upFsVYsBVy_4fQcd03rR76ys'

admins = [983265598]

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

connect = sqlite3.connect('database.db')
cursor = connect.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id text)")
connect.commit()


class States(StatesGroup):
    text = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if cursor.execute(f"SELECT * FROM users WHERE id='{message.chat.id}'").fetchone() == None:
        cursor.execute(f"INSERT INTO users VALUES('{message.chat.id}')")
        connect.commit()
    keyboard = types.ReplyKeyboardMarkup([[types.KeyboardButton(first)]],
                                         resize_keyboard=True)
    await bot.send_message(message.chat.id, hello, reply_markup=keyboard)


@dp.message_handler()
async def else_messages(message: types.Message):
    if message.text in [first, reload]:
        with requests.Session() as session:
            data = session.get('https://thispersondoesnotexist.com/image')
            photo = (f'image{randint(1000, 9999)}.jpeg', data.content)
        keyboard = types.ReplyKeyboardMarkup([[types.KeyboardButton(reload)]], resize_keyboard=True)
        await bot.send_document(message.chat.id, photo, reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup([[types.KeyboardButton(first)]],
                                             resize_keyboard=True)
        await bot.send_message(message.chat.id, hello, reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
