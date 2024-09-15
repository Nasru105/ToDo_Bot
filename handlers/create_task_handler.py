from datetime import datetime

from handlers.helper_handlers import add_task
from config import bot


# Команда для создания задачи
@bot.message_handler(commands=['add'])
def create_task(message):
    msg = bot.send_message(message.chat.id, "Введите название задачи:")
    bot.register_next_step_handler(msg, process_title_step)


def process_title_step(message):
    title = message.text
    msg = bot.send_message(message.chat.id, "Введите описание задачи:")
    bot.register_next_step_handler(msg, process_description_step, title)


def process_description_step(message, title):
    description = message.text
    msg = bot.send_message(message.chat.id, "Введите дедлайн задачи (в формате ГГГГ-ММ-ДД ЧЧ:ММ):")
    bot.register_next_step_handler(msg, process_deadline_step, title, description)


def process_deadline_step(message, title, description):
    deadline = message.text
    try:
        deadline_dt = datetime.strptime(deadline, '%Y-%m-%d %H:%M')
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный формат даты. Попробуйте снова.\n Введите дедлайн задачи (в формате ГГГГ-ММ-ДД ЧЧ:ММ):")
        bot.register_next_step_handler(message, process_deadline_step, title,description)
        return

    msg = bot.send_message(message.chat.id, "Введите приоритет задачи (1-5):")
    bot.register_next_step_handler(msg, process_priority_step, title, description, deadline_dt)


def process_priority_step(message, title, description, deadline):
    priority = int(message.text)
    add_task(message.chat.id, title, description, deadline, priority)
    bot.send_message(message.chat.id, "Задача успешно добавлена!")