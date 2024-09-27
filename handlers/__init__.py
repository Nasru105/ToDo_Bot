
from handlers.create_task_handler import create_task
from handlers.delete_task_handler import delete_task
from handlers.edit_task_handler import edit_task
from handlers.filter_handler import ask_filter_criteria
from handlers.get_completed_tasks_handler import completed_tasks
from handlers.get_tasks_handler import tasks
from handlers.sorting_handler import ask_sorting_criteria


def register_handlers(bot):
    bot.register_message_handler(create_task, commands=['add'])
    bot.register_message_handler(tasks, commands=['tasks'])
    bot.register_message_handler(edit_task, commands=['edit'])
    bot.register_message_handler(delete_task, commands=['delete'])
    bot.register_message_handler(completed_tasks, commands=['completed'])
    bot.register_message_handler(ask_sorting_criteria, commands=['sort'])
    bot.register_message_handler(ask_filter_criteria, commands=['filter'])