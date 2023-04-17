import logging
from aiogram import executor
from aiogram.types import ParseMode
from aiogram.utils import markdown as md
from aiogram import Bot, Dispatcher, types
import asyncio
from datetime import datetime
from config import BOT_TOKEN
import config
from database import Database
from notification import notify_users
from praytimes_lib import get_prayer_times


logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Инициализация базы данных
db = Database(config.DB_NAME)

# Обработчик команды "/start"
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text='Привет! Я бот для получения времени намаза. '
                                                     'Отправь мне свою локацию, чтобы начать.')

# Обработчик локации
@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def process_location(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    location = message.location

    # Сохранение местоположения в базу данных
    db.save_location(user_id, location.latitude, location.longitude)

    # Запрос времени уведомления у пользователя
    await bot.send_message(chat_id=chat_id, text='Отлично! Теперь выбери время, когда ты хочешь получать '
                                                 'уведомления о времени намаза:')
    await bot.send_message(chat_id=chat_id, text='1. За 5 минут до начала намаза', reply_markup=types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True).add(types.KeyboardButton('5 минут')))
    await bot.send_message(chat_id=chat_id, text='2. За 10 минут до начала намаза', reply_markup=types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True).add(types.KeyboardButton('10 минут')))
    await bot.send_message(chat_id=chat_id, text='3. За 15 минут до начала намаза', reply_markup=types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True).add(types.KeyboardButton('15 минут')))

# Обработчик времени уведомления
@dp.message_handler(lambda message: message.text in ['5 минут', '10 минут', '15 минут'])
async def process_notification_time(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    notification_time = message.text

    # Сохранение времени уведомления в базу данных
    db.save_notification_time(user_id, notification_time)

    # Получение текущего местоположения пользователя
    location = db.get_location(user_id)
    latitude = location['latitude']
    longitude = location['longitude']

    # Получение времени намаза
    prayer_times = get_prayer_times(latitude, longitude)

    # Вычисление разницы времени для уведомления
    time_delta = get_time_delta(prayer_times, notification_time)

    # Установка цикла уведомлений с заданным временем
    loop = asyncio.get_event_loop()
    loop.create_task(notify_users(bot, db, chat_id, time_delta))

    # Отправка подтверждения пользователю
    await bot.send_message(chat_id=chat_id, text=f'Отлично! Теперь ты будешь получать уведомления о времени намаза за {notification_time} до начала намаза.')

# Обработчик команды "/help"
@dp.message_handler(commands='help')
async def cmd_help(message: types.Message):
    help_text = "Привет! Я бот для получения времени намаза. Для начала, отправь мне свою локацию. " \
                "Затем выбери время, когда ты хочешь получать уведомления о времени намаза. " \
                "Я буду присылать уведомления за выбранное количество минут до начала намаза. " \
                "Доступные команды:\n" \
                "/start - начать процесс настройки уведомлений\n" \
                "/help - получить справку\n" \
                "/cancel - отменить настройку уведомлений"
    await bot.send_message(chat_id=message.chat.id, text=help_text, parse_mode=ParseMode.MARKDOWN)

# Обработчик команды "/cancel"
@dp.message_handler(commands='cancel')
async def cmd_cancel(message: types.Message):
    user_id = message.from_user.id
    db.delete_user(user_id)  # Удаление данных пользователя из базы данных
    await bot.send_message(chat_id=message.chat.id, text='Настройки уведомлений отменены.')

if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
