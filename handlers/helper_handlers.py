import sqlite3


# Функция для добавления задачи
def add_task(user_id, title, description, deadline, priority):
    conn = sqlite3.connect('tasks.db')  # Создаем новое соединение
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks (user_id, title, description, deadline, priority) VALUES (?, ?, ?, ?, ?)",
                   (user_id, title, description, deadline, priority))
    conn.commit()
    conn.close()  # Закрываем соединение