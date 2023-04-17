import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from aiogram.utils import executor

import config

# Инициализация бота и хранилища состояний
bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Обработчик команды /start
async def on_start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text='Привет! Я бот для оповещений о молитвах.')

# Регистрация обработчиков событий
dp.register_message_handler(on_start_command, commands='start')  # Регистрируем обработчик на команду /start

# Функция запуска бота
async def on_startup(dp):
    await bot.send_message(chat_id=config.CHAT_ID, text='Бот запущен')
    await bot.send_message(chat_id=config.CHAT_ID, text='Отправьте /start для начала использования')
    await bot.send_message(chat_id=config.CHAT_ID, text='Подключение к базе данных...')

    # Подключение к базе данных SQLite
    conn = sqlite3.connect('prayer_notifications.db')
    c = conn.cursor()

    # Создание таблицы для хранения данных о подписках
    c.execute('''CREATE TABLE IF NOT EXISTS subscriptions
                 (chat_id INTEGER PRIMARY KEY, fajr INTEGER, dhuhr INTEGER, asr INTEGER, maghrib INTEGER, isha INTEGER)''')
    conn.commit()

    # Закрываем соединение с базой данных
    conn.close()

async def on_shutdown(dp):
    # Закрываем соединение с базой данных при завершении работы бота
    conn = sqlite3.connect('prayer_notifications.db')
    conn.close()

async def notify_users(prayer_time):
    # Реализация логики оповещения пользователей о времени молитвы
    pass

if __name__ == '__main__':
    from aiogram import executor

    # Запускаем бота с зарегистрированными обработчиками
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
