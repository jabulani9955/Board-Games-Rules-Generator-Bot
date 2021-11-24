import os
import time
import logging

from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode

from model.model_generate import generate
from model.text_processing import processing


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
# TOKEN = os.getenv('TELEGRAM_TOKEN')
TOKEN = '2119124064:AAE3NlfKfaOTgxXYicCBG2CJ4_0C0I69Bc4'

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
    msg = message.text.capitalize().strip()
    try:
        await bot.send_sticker(user_id, STICKER)
        generated_text = processing(generate(msg))
        await message.reply(
            bold(msg) + generated_text.replace(msg, ''),
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await message.reply(f'Возникла ошибка {e.args}')


# Обработчик на случай, если был прислан не текст, а стикер, фото или любой другой тип данных.
@dp.message_handler(content_types='any')
async def unknown_message(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(user_id, INPUT_ERROR)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
