from telebot.types import BotCommand

commands = [
    BotCommand("start", "Запустить бота"),
    BotCommand("add", "Добавить новую задачу"),
    BotCommand("tasks", "Посмотреть список задач"),
    BotCommand("edit", "Редактировать задачу"),
    BotCommand("delete", "Удалить задачу"),
    BotCommand("completed", "Посмотреть выполненные задачи"),
    BotCommand("sort", "Сортировать задачи по приоритету или дедлайну"),
    BotCommand("help", "Получить помощь по командам"),
]
