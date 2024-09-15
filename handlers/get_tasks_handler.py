import sqlite3


from config import bot


@bot.message_handler(commands=['tasks'])
def tasks(message):
    # Подключаемся к базе данных
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Получаем задачи для текущего пользователя
    cursor.execute("SELECT title, description, deadline, priority, status FROM tasks WHERE user_id = ? AND status = 'in_progress'", (message.chat.id,))
    tasks = cursor.fetchall()
    conn.close()

    if tasks:
        task_list = "Ваши текущие задачи:\n"
        for idx, (title, description, deadline, priority, status) in enumerate(tasks, 1):
            task_list += (f"{idx}. {title}\n"
                          f"Описание: {description}\n"
                          f"Дедлайн: {deadline}\n"
                          f"Приоритет: {priority}\n"
                          f"Статус: {status}\n\n")
    else:
        task_list = "У вас нет активных задач."

    # Отправляем список задач пользователю
    bot.send_message(message.chat.id, task_list)
