import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler

# Определение функции-обработчика команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я твой бот-помощник по Исламу!")

# Определение функции-обработчика сообщений
def echo(update, context):
    if update.message.text:  # Фильтрация сообщений только с текстом
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text, parse_mode=telegram.ParseMode.HTML)

def main():
    # Создание экземпляра Updater
    updater = Updater("6036464057:AAGnxuVNu8kLhugL6GdFlmYkY1la2qN68XI")

    # Получение диспетчера (dispatcher) от Updater
    dispatcher = updater.dispatcher

    # Регистрация обработчиков команд и сообщений
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(telegram.ext.Update, echo))  # Установка обработчика для всех типов сообщений

    # Запуск бота
