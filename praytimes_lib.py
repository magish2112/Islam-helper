from geopy.geocoders import Nominatim
from praytimes import PrayTimes
from datetime import datetime, timedelta
import time

# Определение функции get_prayer_times
def get_prayer_times(city_name):
    # Создаем объект геокодера
    geolocator = Nominatim(user_agent="my_app")

    # Определяем координаты города
    location = geolocator.geocode(city_name)
    if location is None:
        print("Не удалось найти координаты для указанного города")
        return None
    else:
        latitude = location.latitude
        longitude = location.longitude
        print("Координаты города {} (широта, долгота): {}, {}".format(city_name, latitude, longitude))

        # Создаем объект PrayTimes
        pray_times = PrayTimes('ISNA')

        # Получаем текущую дату и время
        now = datetime.now()

        # Определяем временную зону
        tz_offset = -time.timezone // 60 # смещение в минутах относительно UTC
        tz = timedelta(minutes=tz_offset)

        # Преобразуем время в указанную временную зону
        now_tz = now + tz

        # Получаем время молитв с учетом определенной временной зоны
        prayer_times = pray_times.getTimes(now_tz.date(), (latitude, longitude), tz.total_seconds() / 3600)

        return prayer_times

# Вводим название города
city_name = input("Введите название города: ")

# Получаем время молитв
prayer_times = get_prayer_times(city_name)

if prayer_times is not None:
    print("Время молитв для города {}: ".format(city_name))
    print("Фаджр (заря):", prayer_times['fajr'])
    print("Восход (рассвет):", prayer_times['sunrise'])
    print("Зухр (полдень):", prayer_times['dhuhr'])
    print("Аср (после полудня):", prayer_times['asr'])
    print("Магриб (закат):", prayer_times['maghrib'])
    print("Иша (полночь):", prayer_times['isha'])
    # Продолжаем с остальными временами молитв по аналогии
    # ...
