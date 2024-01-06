from random import randint
from aiogram.types import URLInputFile

def get_photo():
    photo = URLInputFile(url='https://thispersondoesnotexist.com/', filename=f'image_{randint(10000000, 99999999)}.jpeg')

    return photo