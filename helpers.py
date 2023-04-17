from datetime import datetime, timedelta
import pytz

# Функция для преобразования локального времени во временную зону пользователя
def localize_user_time(user_tz, dt):
    """
    Функция для преобразования локального времени во временную зону пользователя

    :param user_tz: Временная зона пользователя (str), например 'Europe/Moscow'
    :param dt: Дата и время в локальной временной зоне (datetime.datetime)
    :return: Дата и время в временной зоне пользователя (datetime.datetime)
    """
    local_tz = pytz.timezone(user_tz)
    localized_dt = local_tz.localize(dt)
    return localized_dt

# Функция для форматирования времени в строку в формате HH:MM
def format_time(dt):
    """
    Функция для форматирования времени в строку в формате HH:MM

    :param dt: Дата и время (datetime.datetime)
    :return: Время в строковом формате HH:MM
    """
    return dt.strftime('%H:%M')

# Функция для получения времени через определенный интервал от текущего времени
def get_time_after_minutes(minutes):
    """
    Функция для получения времени через определенный интервал от текущего времени

    :param minutes: Интервал в минутах (int)
    :return: Время через указанный интервал от текущего времени (datetime.datetime)
    """
    now = datetime.now()
    time_after_minutes = now + timedelta(minutes=minutes)
    return time_after_minutes
