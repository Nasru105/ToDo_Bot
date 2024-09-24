import sqlite3
from telebot import types

from config import bot


@bot.message_handler(commands=['tasks'])
def tasks(message):
    # Подключаемся к базе данных
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Получаем задачи для текущего пользователя
    cursor.execute(
        "SELECT id, title, description, deadline, priority, status FROM tasks WHERE user_id = ? AND status = 'in_progress'",
        (message.chat.id,))
    tasks = cursor.fetchall()
    conn.close()

    if tasks:
        bot.send_message(message.chat.id, "Ваши текущие задачи:")
        for idx, (id, title, description, deadline, priority, status) in enumerate(tasks, 1):
            task = (f"{idx}. {title}\n"
                       f"Описание: {description}\n"
                       f"Дедлайн: {deadline}\n"
                       f"Приоритет: {priority}\n"
                       f"Статус: {status}\n\n")
            markup = types.InlineKeyboardMarkup()
            b1 = types.InlineKeyboardButton(text="выполнено", callback_data=f"complete_task_{id}")
            b2 = types.InlineKeyboardButton(text="изменить", callback_data=f"edit_task_{id}")
            b3 = types.InlineKeyboardButton(text="удалить", callback_data=f"delete_task_{id}")
            markup.row(b1, b2, b3)
            bot.send_message(message.chat.id, task, reply_markup=markup)
    else:
        task_list = "У вас нет активных задач."

    # Отправляем список задач пользователю


@bot.callback_query_handler(func=lambda call: call.data.startswith("complete_task_"))
def complete_task(call):
    # Извлекаем идентификатор задачи из callback_data
    task_id = call.data.split("_")[-1]

    # Подключаемся к базе данных
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Обновляем статус задачи на "выполнено"
    cursor.execute("UPDATE tasks SET status = 'completed' WHERE id = ? AND user_id = ?",
                   (task_id, call.message.chat.id))
    conn.commit()
    conn.close()

    # Отправляем сообщение пользователю, что задача завершена
    bot.send_message(call.message.chat.id, "Задача успешно отмечена как выполненная.")

    # Удаляем сообщение с кнопками, чтобы пользователь не мог повторно нажать "выполнено"
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
