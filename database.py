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
            status TEXT NOT NULL DEFAULT 'TODO',
            theme TEXT NOT NULL,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES tasks(id))
    """)
    conn.commit()
    conn.close()

def get_status(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status
        FROM tasks
        WHERE id = ?
    """, (id))

    tasks = cursor.fetchall()
    conn.close()
    row = cursor.fetchone()
    return row["status"] if row else None

def mark_task_done(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status = 'done' WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()


def get_main_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tasks
        WHERE parent_id IS NULL
        ORDER BY due_date ASC
    """)

    tasks = cursor.fetchall()
    conn.close()
    return tasks

def insert_task(title, due_date, theme, parent_id=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, due_date, theme, parent_id)
        VALUES (?, ?, ?, ?)
        """,
        (title, due_date, theme, parent_id)
    )

    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = ? OR parent_id = ?
        """,
        (task_id, task_id)
    )

    conn.commit()
    conn.close()

def update_task(task_id, title, due_date, theme, parent_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, due_date = ?, theme = ?, parent_id = ?
        WHERE id = ?
        """,
        (title, due_date, theme, parent_id, task_id)
    )

    conn.commit()
    conn.close()

def get_subtasks(parent_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE parent_id = ?
        ORDER BY due_date ASC
        """,
        (parent_id,)
    )

    subtasks = cursor.fetchall()
    conn.close()
    return subtasks
