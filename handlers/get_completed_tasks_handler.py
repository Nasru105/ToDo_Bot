import sqlite3
from telebot import types

from config import bot


@bot.message_handler(commands=['completed'])
def completed_tasks(message):
    # Подключаемся к базе данных
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Получаем задачи для текущего пользователя
    cursor.execute(
        "SELECT title, description, deadline, priority, status FROM tasks WHERE user_id = ? AND status = 'completed'",
        (message.chat.id,))
    tasks = cursor.fetchall()
    conn.close()

    if tasks:
        bot.send_message(message.chat.id, "Ваши текущие задачи:")
        task_list = []
        for idx, (title, description, deadline, priority, status) in enumerate(tasks, 1):
            task_list.append(f"{idx}. {title}\n"
                             f"Описание: {description}\n"
                             f"Дедлайн: {deadline}\n"
                             f"Приоритет: {priority}\n"
                             f"Статус: {status}\n\n")
    else:
        task_list = "У вас нет активных задач."

    # Отправляем список задач пользователю
    for task in task_list:
        bot.send_message(message.chat.id, task)
