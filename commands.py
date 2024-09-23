from telebot.types import BotCommand

commands = [
    BotCommand("start", "Запустить бота"),
    BotCommand("add", "Добавить новую задачу"),
    BotCommand("tasks", "Посмотреть список задач"),
    BotCommand("edit_task", "Редактировать задачу"),
    BotCommand("delete", "Удалить задачу"),
    BotCommand("completed", "Посмотреть выполненные задачи"),
    BotCommand("reminders", "Включить/выключить напоминания о задачах"),
    BotCommand("sort", "Сортировать задачи по приоритету или дедлайну"),
    BotCommand("status", "Изменить статус задачи (выполнено/в работе)"),
    BotCommand("help", "Получить помощь по командам"),
]
