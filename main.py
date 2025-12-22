from database import init_db, insert_task, delete_task, update_task, get_main_tasks, get_subtasks, mark_task_done, get_status, mark_task_todo
from textual.app import App, ComposeResult
from textual.widgets import Tree, Input
from textual.widgets.tree import TreeNode
from textual.containers import Vertical
from datetime import datetime, date

init_db()

class TodoApp(App):
    BINDINGS = [
        ("q", "quit", "Sair"),
        ("r", "reload", "Recarregar"),
    ]

    def process_task(self, task):
        due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
        today = date.today()
        status = (task["status"] or "")

        if status == "DONE" and due < today:
            delete_task(task["id"])
            return None

        title = task["title"]

        status_label = "[green]DONE[/green]" if status == "DONE" else "TODO"

        if status != "DONE" and due < today:
            title = f"[red]LATE[/red] {title}"

        elif status != "DONE" and (due - today).days <= 1:
            title = f"*{status_label} {title}"

        else:
            title = f"{status_label} {title}"

        return title

    def compose(self) -> ComposeResult:
        with Vertical():
            yield self.build_tree()
            yield Input(
                placeholder=">",
                id="command_input"
            )

    def build_tree(self) -> Tree:
        tree = Tree(label="", id="tasks_tree")

        main_tasks = get_main_tasks()

        for task in main_tasks:
            label_title = self.process_task(task)
            if label_title is None:
                continue

            node = tree.root.add(
                f"{label_title} ({task['due_date']})",
                expand=False,
                data=task["id"],
            )
        return tree
    
    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        node: TreeNode = event.node

        if node.children:
            return

        parent_id = node.data
        subtasks = get_subtasks(parent_id)

        for sub in subtasks:
            label_title = self.process_task(sub)
            if label_title is None:
                continue

            node.add(
                f"{label_title} ({sub['due_date']})",
                data=sub["id"]  
        )

    def action_reload(self):
        self.reload_tree()

    def on_key(self, event):
        if event.key == "enter":
            node = self.query_one(Tree).cursor_node
            if node and node.data:
                if get_status(node.data) != "DONE":
                    mark_task_done(node.data)
                else:
                    mark_task_todo(node.data)
                self.reload_tree()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        event.input.value = ""

        if command.startswith("add "):
            self.handle_add(command)
        elif command.startswith("del "):
            self.handle_delete(command)
        elif command.startswith("edit "):
            self.handle_edit(command)
        else:
            self.notify("unknown command", severity="error")

        self.reload_tree()
    
    def reload_tree(self):
        tree = self.query_one(Tree)
        tree.clear()
        for task in get_main_tasks():
            label_title = self.process_task(task)
            if label_title is None:
                continue

            tree.root.add(
                f"{label_title} ({task['due_date']})",
                data=task['id'],
                expand=False
            )

    def list_tasks():
        tasks = get_main_tasks()

        if not tasks:
            print("Nenhuma tarefa encontrada.")
            return

        for task in tasks:
            print(f"ID: {task['id']}, Título: {task['title']}, Data: {task['due_date']}, Tema: {task['theme']}")

    def handle_add(self,command):
        data = command[4:]
        parts = data.split(";")

        if len(parts) < 3:
            print("Formato inválido. Use: add titulo;data;tema")
            return

        title = parts[0].strip()
        due_date = parts[1].strip()
        theme = parts[2].strip()

        parent_id = None

        if len(parts) == 4:
            p = parts[3].strip()
            parent_id = int(p) if p else None

        insert_task(title, due_date, theme, parent_id)

        print("Tarefa adicionada.")

    def handle_delete(self,command):
        parts = command.split()
        
        try:
            task_id = int(parts[1])
        except ValueError:
            print("ID inválido.")
            return

        delete_task(task_id)
        print(f"Tarefa {task_id} removida.")

    def handle_edit(self,command):
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

        if len(fields) == 4:
            parent_id = fields[3].strip()

        update_task(task_id, title, due_date, theme, parent_id)
        print(f"Tarefa {task_id} atualizada.")


TodoApp().run()
