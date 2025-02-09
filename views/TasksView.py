import tkinter as tk

from views.modules.PageFrame import PageFrame
from views.modules.Panel import Panel

class TasksView(Panel):
    def __init__(self, parent, controller, is_admin: bool = False):
        super().__init__(parent, "Tasks")

        self.controller = controller

        self._setup_ui()

    def _setup_ui(self):
        main_frame = tk.Frame(self)
        self.load_main_page(main_frame)

        self.table = PageFrame(main_frame, self.controller.fetch_unassigned_tasks, self.controller.open_task)
        self.table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        columns = [{'column_name': 'idTask', 'column_label': 'ID', 'visible': False},
                   {'column_name': 'title', 'column_label': 'Title', 'visible': True},
                   {'column_name': 'description', 'column_label': 'Description', 'visible': False},
                   {'column_name': 'taskScore', 'column_label': 'Score', 'visible': True},
                   {'column_name': 'taskCreated', 'column_label': 'Created', 'visible': False},
                   {'column_name': 'startDate', 'column_label': 'Start date', 'visible': True},
                   {'column_name': 'dueDate', 'column_label': 'Due date', 'visible': True},
                   {'column_name': 'category', 'column_label': 'Category', 'visible': True}]

        self.table.configure_columns(columns)
        self.table.load_data()

