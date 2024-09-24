from telebot import types
import sqlite3
from config import bot


# Шаг 1: Запрос задачи для удаления
@bot.message_handler(commands=['delete'])
def delete_task(message):
    user_id = message.chat.id
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Получаем список задач пользователя
    cursor.execute("SELECT id, title FROM tasks WHERE user_id = ?", (user_id,))
    tasks = cursor.fetchall()

    if tasks:
        markup = types.InlineKeyboardMarkup()
        for task_id, title in tasks:
            button = types.InlineKeyboardButton(text=title, callback_data=f"delete_task_{task_id}")
            markup.add(button)

        bot.send_message(user_id, "Выберите задачу для удаления:", reply_markup=markup)
    else:
        bot.send_message(user_id, "У вас нет задач для удаления.")

    conn.close()

# Шаг 2: Обработка выбора задачи для удаления
@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_task_"))
def confirm_task_deletion(call):
    user_id = call.message.chat.id
    task_id = call.data.split("_")[-1]

    # Подтверждение удаления
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text="Да", callback_data=f"confirm_delete_{task_id}"),
        types.InlineKeyboardButton(text="Нет", callback_data="cancel_delete")
    )

    bot.send_message(user_id, "Вы уверены, что хотите удалить эту задачу?", reply_markup=markup)

# Шаг 3: Подтверждение удаления
@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_delete_"))
def delete_task(call):
    user_id = call.message.chat.id
    task_id = call.data.split("_")[-1]

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "Задача успешно удалена.")

# Шаг 4: Отмена удаления
@bot.callback_query_handler(func=lambda call: call.data == "cancel_delete")
def cancel_task_deletion(call):
    user_id = call.message.chat.id
    bot.send_message(user_id, "Удаление отменено.")
