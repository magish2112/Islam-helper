import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Создание таблицы для сохранения локации
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS location (
                user_id INTEGER PRIMARY KEY,
                latitude REAL,
                longitude REAL
            )
        ''')

        # Создание таблицы для сохранения времени уведомлений
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notification_time (
                user_id INTEGER PRIMARY KEY,
                time TEXT
            )
        ''')

        self.conn.commit()

    def save_location(self, user_id, latitude, longitude):
        # Сохранение локации в базе данных
        self.cursor.execute('''
            INSERT OR REPLACE INTO location (user_id, latitude, longitude)
            VALUES (?, ?, ?)
        ''', (user_id, latitude, longitude))
        self.conn.commit()

    def get_location(self, user_id):
        # Получение локации из базы данных
        self.cursor.execute('SELECT * FROM location WHERE user_id = ?', (user_id,))
        location = self.cursor.fetchone()
        if location:
            return {'latitude': location[1], 'longitude': location[2]}
        else:
            return None

    def save_notification_time(self, user_id, time):
        # Сохранение времени уведомлений в базе данных
        self.cursor.execute('''
            INSERT OR REPLACE INTO notification_time (user_id, time)
            VALUES (?, ?)
        ''', (user_id, time))
        self.conn.commit()

    def get_notification_time(self, user_id):
        # Получение времени уведомлений из базы данных
        self.cursor.execute('SELECT time FROM notification_time WHERE user_id = ?', (user_id,))
        time = self.cursor.fetchone()
        if time:
            return time[0]
        else:
            return None

    def close(self):
        # Закрытие соединения с базой данных
        self.conn.close()
