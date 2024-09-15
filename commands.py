from telebot.types import BotCommand

commands = [
    BotCommand("start", "Запустить бота"),
    BotCommand("help", "Получить помощь по командам"),
    BotCommand("add", "Добавить новую задачу"),
    BotCommand("edit", "Редактировать задачу"),
    BotCommand("delete", "Удалить задачу"),
    BotCommand("tasks", "Посмотреть список задач"),
    BotCommand("completed", "Посмотреть выполненные задачи"),
    BotCommand("reminders", "Включить/выключить напоминания о задачах"),
    BotCommand("sort", "Сортировать задачи по приоритету или дедлайну"),
    BotCommand("status", "Изменить статус задачи (выполнено/в работе)")
]
