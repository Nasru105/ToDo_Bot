from telebot import types
import sqlite3
from config import bot

@bot.message_handler(commands=['sort'])
def ask_sorting_criteria(message):
    # Создаем кнопки для выбора критерия сортировки
    markup = types.InlineKeyboardMarkup()
    btn_deadline = types.InlineKeyboardButton("По дедлайну", callback_data="sort_by_deadline")
    btn_priority = types.InlineKeyboardButton("По приоритету", callback_data="sort_by_priority")
    markup.add(btn_deadline, btn_priority)

    bot.send_message(message.chat.id, "Выберите критерий сортировки:", reply_markup=markup)

# Обработчик выбора сортировки по дедлайну
@bot.callback_query_handler(func=lambda call: call.data == "sort_by_deadline")
def sort_tasks_by_deadline(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)

    sort_tasks(call, "deadline")

# Обработчик выбора сортировки по приоритету
@bot.callback_query_handler(func=lambda call: call.data == "sort_by_priority")
def sort_tasks_by_priority(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    sort_tasks(call, "priority")

def sort_tasks(call, criteria):
    user_id = call.message.chat.id
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Сортируем задачи по указанному критерию (дедлайн или приоритет)
    cursor.execute(f"SELECT title, description, deadline, priority, status FROM tasks WHERE user_id = ? AND status = 'in_progress' ORDER BY {criteria} ASC", (user_id,))
    tasks = cursor.fetchall()
    conn.close()

    if tasks:
        bot.send_message(user_id, f"Ваши задачи, отсортированные по {criteria}:")
        task_list = []
        for idx, (title, description, deadline, priority, status) in enumerate(tasks, 1):
            task_list.append(f"{idx}. {title}\n"
                             f"Описание: {description}\n"
                             f"Дедлайн: {deadline}\n"
                             f"Приоритет: {priority}\n"
                             f"Статус: {status}\n\n")
        # Отправляем задачи пользователю
        for task in task_list:
            markup = types.InlineKeyboardMarkup()
            b1 = types.InlineKeyboardButton(text="выполнено", callback_data=f"complete_task_")
            b2 = types.InlineKeyboardButton(text="изменить", callback_data=f"edit_task_")
            b3 = types.InlineKeyboardButton(text="удалить", callback_data=f"delete_task_")
            markup.row(b1, b2, b3)
            bot.send_message(user_id, task, reply_markup=markup)
    else:
        bot.send_message(user_id, "У вас нет активных задач.")
