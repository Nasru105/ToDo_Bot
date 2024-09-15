
from handlers.create_task_handler import create_task
from handlers.get_tasks_handler import tasks


def register_handlers(bot):
    bot.register_message_handler(create_task, commands=['add'])
    bot.register_message_handler(tasks, commands=['tasks'])