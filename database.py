import sqlite3

DB_NAME = "tasks.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            due_date TEXT NOT NULL,
            theme TEXT NOT NULL,
            parent_task TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_task(title, due_date, theme, parent_task="main"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, due_date, theme, parent_task)
        VALUES (?, ?, ?, ?)
        """,
        (title, due_date, theme, parent_task)
    )

    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM tasks WHERE id = ?
        """,
        (task_id,)
    )

    conn.commit()
    conn.close()

def update_task(task_id, title, due_date, theme, parent_task):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, due_date = ?, theme = ?, parent_task = ?
        WHERE id = ?
        """,
        (title, due_date, theme, parent_task, task_id)
    )

    conn.commit()
    conn.close()
