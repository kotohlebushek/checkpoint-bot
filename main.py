from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import NetworkError
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from random import randint
import requests
import sqlite3

# Приветственное сообщение
hello = """👋Привет! Ты используешь демонстрационный бот

✅В данном боте ты можешь получить фото для прохождения чекпоинта

Краткая инструкция:
1. Нажми кнопку "👨Получить фото для прохода чекпоинта"
2. Обновляй фото пока не получишь нужное тебе лицо
3. Загрузи файл себе на устройство
4. Загрузи файл с устройства в аккаунт к Цукеру (Facebook)"""

# Тексты кнопок
first = '👨Получить фото для прохода чекпоинта'
reload = '🔄Обновить'

# Токен бота
TOKEN = '5403965855:AAEfs0zZVw1upFsVYsBVy_4fQcd03rR76ys'

# Telegram ID администраторов
admins = []

# Создание бота
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Создание/подключение к базе данных
connect = sqlite3.connect('database.db')
cursor = connect.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id text)")
connect.commit()


# Класс для машины состояния
class States(StatesGroup):
    text = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Проверка наличия поользователя в базе данных
    if cursor.execute(f"SELECT * FROM users WHERE id='{message.chat.id}'").fetchone() == None:
        cursor.execute(f"INSERT INTO users VALUES('{message.chat.id}')")
        connect.commit()
    # Отправка приветственного сообщения с кнопкой
    keyboard = types.ReplyKeyboardMarkup([[types.KeyboardButton(first)]],
                                         resize_keyboard=True)
    await bot.send_message(message.chat.id, hello, reply_markup=keyboard)


@dp.message_handler()
async def else_messages(message: types.Message):
    # Проверка нажатия на кнопку
    if message.text in [first, reload]:
        # Создание сессии
        with requests.Session() as session:
            # Получение фото с сайта
            data = session.get('https://thispersondoesnotexist.com/image')
            photo = (f'image{randint(1000, 9999)}.jpeg', data.content)
        # Отправка фотографии
        keyboard = types.ReplyKeyboardMarkup([[types.KeyboardButton(reload)]], resize_keyboard=True)
        await bot.send_document(message.chat.id, photo, reply_markup=keyboard)
    else:
        # Отправка приветственного сообщения с кнопкой
        keyboard = types.ReplyKeyboardMarkup([[types.KeyboardButton(first)]],
                                             resize_keyboard=True)
        await bot.send_message(message.chat.id, hello, reply_markup=keyboard)


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
