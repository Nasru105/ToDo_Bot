import sqlite3
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from commands import commands
from handlers import register_handlers
from messages import welcome_text, help_text
from config import bot

# Подключение к базе данных
conn = sqlite3.connect('tasks.db', check_same_thread=False)
cursor = conn.cursor()


# Адаптер для конвертации datetime в строку
def adapt_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')


# Конвертер для конвертации строки в объект datetime
def convert_datetime(s):
    return datetime.strptime(s.decode('utf-8'), '%Y-%m-%d %H:%M:%S')


# Регистрация адаптера и конвертера для работы с datetime
sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("DATETIME", convert_datetime)

# Подключение к базе данных с указанием конвертера для datetime
conn = sqlite3.connect('tasks.db', detect_types=sqlite3.PARSE_DECLTYPES)

# Создание таблицы задач, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    title TEXT NOT NULL,
                    description TEXT,
                    deadline DATETIME,
                    priority INTEGER,
                    status TEXT DEFAULT 'in_progress',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
conn.commit()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, welcome_text)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, help_text)


# Функция для уведомлений о приближении дедлайна
def send_deadline_reminders():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    now = datetime.now()
    one_hour_before = now + timedelta(hours=1)
    one_day_before = now + timedelta(days=1)

    # Запрашиваем задачи с дедлайнами через 1 час и через 1 день
    cursor.execute(
        """
        SELECT user_id, title, deadline 
        FROM tasks 
        WHERE (deadline BETWEEN ? AND ? OR deadline BETWEEN ? AND ?) 
        AND status = 'in_progress'
        """,
        (now, one_hour_before, now, one_day_before)
    )
    tasks = cursor.fetchall()

    for task in tasks:
        user_id, title, deadline_str = task

        # Преобразуем строку deadline в объект datetime
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")

        # Вычисляем разницу во времени
        time_to_deadline = deadline - now

        # Проверяем, если до дедлайна 1 час или 1 день
        if timedelta(minutes=59, seconds=30) <= time_to_deadline <= timedelta(hours=1, seconds=30,microseconds=1):
            bot.send_message(user_id,
                             f"Напоминание: Задача '{title}' приближается к дедлайну через 1 час ({deadline})!")
        elif timedelta(hours=23, minutes=59,seconds=30) <= time_to_deadline <= timedelta(days=1, seconds=30,microseconds=1):
            bot.send_message(user_id,
                             f"Напоминание: Задача '{title}' приближается к дедлайну через 1 день ({deadline})!")

    conn.close()


# Запуск планировщика для проверки задач каждую минуту
scheduler = BackgroundScheduler()
scheduler.add_job(send_deadline_reminders, 'interval', minutes=1)
scheduler.start()

# Запуск бота
if __name__ == "__main__":
    bot.set_my_commands(commands)
    register_handlers(bot)
    bot.infinity_polling(
        skip_pending=True,
        allowed_updates=[],
    )
