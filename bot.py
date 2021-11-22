import os
import time
import logging

import textwrap
from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from model.model_generate import generate


START = """
Привет, %s!\nДавай сгенерируем новые правила настольной игры!?
Напиши что-нибудь и модель сгенерирует какую-нибудь чушь :)
Список возможных команд:
    /start - Запуск/перезапуск бота.
    /about - Краткая информация.
"""
ABOUT = "Основано на правилах игры, взятых с Мосигры."
INPUT_ERROR = """
Запрос должен быть в текстовом виде.
Напомню, что /help выведет список доступных команд.
"""
STICKER = "CAACAgIAAxkBAAEDH3ZhcPwuk8_ea46pVXd7kcKtuJaJCgACeSUAAp7OCwABlPU3foy-CJwhBA"

# Включаем логирование
logging.basicConfig(
    filename='log.log', 
    level=logging.INFO
)

# Загрузка токена через env
# load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    logging.info(f'{user_id} запустил бота в {time.asctime()}')
    await message.reply(START % user_name)


@dp.message_handler(commands=['about'])
async def about(message: types.Message):
    await message.reply(ABOUT)


@dp.message_handler()
async def main(message: types.Message):
    user_id = message.from_user.id
    try:
        await bot.send_sticker(user_id, STICKER)
        await message.reply(textwrap.fill(generate(message.text), 120))
    except Exception as e:
        await message.reply(f'Возникла ошибка {e.args}')


# Обработчик на случай, если был прислан не текст, а стикер, фото или любой другой тип данных.
@dp.message_handler(content_types='any')
async def unknown_message(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(user_id, INPUT_ERROR)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
