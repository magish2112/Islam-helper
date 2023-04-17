# Токен бота
BOT_TOKEN = 'ВТСАВЬТЕ СЮДА ТОКЕН'

# Список пользователей, которым будут отправляться уведомления
USERS = [1234567890, 9876543210]

# Настройки времени молитв
PRAYER_TIMES = {
    'fajr': 'Fajr',
    'sunrise': 'Sunrise',
    'dhuhr': 'Dhuhr',
    'asr': 'Asr',
    'maghrib': 'Maghrib',
    'isha': 'Isha',
}

# Время уведомлений перед молитвами
NOTIFY_TIMES = {
    '5': '5 минут',
    '10': '10 минут',
    '15': '15 минут',
}

# Опции тайм-аута для запроса времени молитв
TIMEOUT_OPTIONS = {
    '30': '30 секунд',
    '60': '1 минута',
    '120': '2 минуты',
}

# Имя базы данных
DB_NAME = 'my_database_name'

def get_bot_token():
    return BOT_TOKEN

def get_users():
    return USERS

def get_prayer_times():
    return PRAYER_TIMES

def get_notify_times():
    return NOTIFY_TIMES

def get_timeout_options():
    return TIMEOUT_OPTIONS
