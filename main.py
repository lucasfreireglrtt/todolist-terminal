from database import init_db, insert_task, delete_task, update_task

init_db()
command = input("> ").strip()

def handle_add(command):
    data = command[4:]
    parts = data.split(";")

    if len(parts) < 3:
        print("Formato inválido. Use: add titulo;data;tema")
        return

    title = parts[0].strip()
    due_date = parts[1].strip()
    theme = parts[2].strip()
    parent_task = "main"

    if len(parts) == 4:
        parent_task = parts[3].strip()

    insert_task(title, due_date, theme, parent_task)

    print("Tarefa adicionada.")

def handle_delete(command):
    parts = command.split()
    
    try:
        task_id = int(parts[1])
    except ValueError:
        print("ID inválido.")
        return

    delete_task(task_id)
    print(f"Tarefa {task_id} removida.")

def handle_edit(command):
    parts = command.split(maxsplit=2)

    try:
        task_id = int(parts[1])
    except ValueError:
        print("ID inválido.")
        return

    data = parts[2]
    fields = data.split(";")

    title = fields[0].strip()
    due_date = fields[1].strip()
    theme = fields[2].strip()
    parent_task = "main"

    if len(fields) == 4:
        parent_task = fields[3].strip()

    update_task(task_id, title, due_date, theme, parent_task)
    print(f"Tarefa {task_id} atualizada.")
