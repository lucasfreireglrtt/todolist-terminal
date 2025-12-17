from database import init_db, insert_task, delete_task, update_task, get_main_tasks, get_subtasks
from textual.app import App, ComposeResult
from textual.widgets import Tree, Input
from textual.widgets.tree import TreeNode
from textual.containers import Vertical

init_db()

class TodoApp(App):
    BINDINGS = [
        ("q", "quit", "Sair"),
        ("r", "reload", "Recarregar"),
    ]

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
            node = tree.root.add(
                f"{task['title']} ({task['due_date']})",
                expand=False,
                data=task["id"],
            )
        return tree
    
    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        node: TreeNode = event.node

        if node.children:
            return

        parent_title = node.data
        subtasks = get_subtasks(parent_title)

        for sub in subtasks:
            node.add(
                f"{sub['title']} ({sub['due_date']})",
                data=sub["id"]  
        )

    def action_reload(self):
        tree = self.query_one(Tree)
        tree.clear()
        self.mount(self.build_tree(), replace=True)

    def on_key(self, event):
        if event.key == "enter":
            node = self.query_one(Tree).cursor_node
            if node:
                node.set_label(f"[green]{node.label}[/green]")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        event.input.value = ""  # limpa a linha

        if command.startswith("add "):
            self.handle_add(command)
        elif command.startswith("del "):
            self.handle_delete(command)
        elif command.startswith("edit "):
            self.handle_edit(command)
        else:
            self.notify("Comando desconhecido", severity="warning")

        self.reload_tree()
    
    def reload_tree(self):
        tree = self.query_one(Tree)
        tree.clear()
        for task in get_main_tasks():
            tree.root.add(
                f"{task['title']} ({task['due_date']})",
                data=task["title"],
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
        parent_task = "main"

        if len(parts) == 4:
            parent_task = parts[3].strip()

        insert_task(title, due_date, theme, parent_task)

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
        parent_task = "main"

        if len(fields) == 4:
            parent_task = fields[3].strip()

        update_task(task_id, title, due_date, theme, parent_task)
        print(f"Tarefa {task_id} atualizada.")


TodoApp().run()