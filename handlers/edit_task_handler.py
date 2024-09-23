from telebot import types
import sqlite3
from datetime import datetime
from config import bot

# Храним временные данные редактируемых задач для пользователей
edit_task_data = {}

# Шаг 1: Запрос задачи для редактирования
@bot.message_handler(commands=['edit_task'])
def edit_task(message):
    user_id = message.chat.id
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Получаем список задач пользователя
    cursor.execute("SELECT id, title FROM tasks WHERE user_id = ? AND status = 'in_progress'", (user_id,))
    tasks = cursor.fetchall()

    if tasks:
        markup = types.InlineKeyboardMarkup()
        for task_id, title in tasks:
            button = types.InlineKeyboardButton(text=title, callback_data=f"edit_task_{task_id}")
            markup.add(button)

        bot.send_message(user_id, "Выберите задачу для редактирования:", reply_markup=markup)
    else:
        bot.send_message(user_id, "У вас нет активных задач.")

    conn.close()

    # Шаг 2: Выбор поля для редактирования


@bot.callback_query_handler(func=lambda call: call.data.startswith("edit_task_"))
def choose_field_to_edit(call):
    user_id = call.message.chat.id

    task_id = call.data.split("_")[-1]

    # Сохраняем task_id для последующего редактирования
    edit_task_data[user_id] = {"task_id": task_id}

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Название", callback_data="edit_field_title"))
    markup.add(types.InlineKeyboardButton(text="Описание", callback_data="edit_field_description"))
    markup.add(types.InlineKeyboardButton(text="Дедлайн", callback_data="edit_field_deadline"))
    markup.add(types.InlineKeyboardButton(text="Приоритет", callback_data="edit_field_priority"))

    bot.send_message(user_id, "Что вы хотите изменить?", reply_markup=markup)


# Шаг 3: Ввод новых данных
@bot.callback_query_handler(func=lambda call: call.data.startswith("edit_field_"))
def process_field_edit(call):
    user_id = call.message.chat.id
    field_to_edit = call.data.split("_")[-1]

    if user_id not in edit_task_data or "task_id" not in edit_task_data[user_id]:
        bot.send_message(user_id, "Ошибка! Сначала выберите задачу для редактирования.")
        return

    edit_task_data[user_id]["field"] = field_to_edit

    if field_to_edit == "title":
        bot.send_message(user_id, "Введите новое название задачи:")
    elif field_to_edit == "description":
        bot.send_message(user_id, "Введите новое описание задачи:")
    elif field_to_edit == "deadline":
        bot.send_message(user_id, "Введите новый дедлайн (в формате ГГГГ-ММ-ДД ЧЧ:ММ):")
    elif field_to_edit == "priority":
        bot.send_message(user_id, "Введите новый приоритет задачи (например, 1-5):")

    bot.register_next_step_handler(call.message, update_task_field)


# Шаг 4: Обновление данных в базе
def update_task_field(message):
    user_id = message.chat.id
    new_value = message.text
    task_id = edit_task_data[user_id]["task_id"]
    field_to_edit = edit_task_data[user_id]["field"]

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Валидация и обновление поля
    if field_to_edit == "title":
        cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (new_value, task_id))
    elif field_to_edit == "description":
        cursor.execute("UPDATE tasks SET description = ? WHERE id = ?", (new_value, task_id))
    elif field_to_edit == "deadline":
        try:
            new_deadline = datetime.strptime(new_value, "%Y-%m-%d %H:%M")
            cursor.execute("UPDATE tasks SET deadline = ? WHERE id = ?", (new_deadline, task_id))
        except ValueError:
            bot.send_message(user_id, "Неправильный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД ЧЧ:ММ")
            return
    elif field_to_edit == "priority":
        if new_value.isdigit() and 1 <= int(new_value) <= 5:
            cursor.execute("UPDATE tasks SET priority = ? WHERE id = ?", (new_value, task_id))
        else:
            bot.send_message(user_id, "Приоритет должен быть числом от 1 до 5.")
            return

    conn.commit()
    conn.close()

    bot.send_message(user_id, "Задача успешно обновлена.")

    if user_id in edit_task_data:
        del edit_task_data[user_id]
