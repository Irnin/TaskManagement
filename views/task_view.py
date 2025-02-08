import tkinter as tk

from views.modules.PageFrame import PageFrame
from views.modules.Panel import Panel


class TaskView(Panel):
    def __init__(self, parent, controller):
        super().__init__(parent, "Tasks")

        self.controller = controller

        self._setup_ui()

    def _setup_ui(self):
        table = PageFrame(self)
        table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        columns = [{'column_name': 'idTask', 'column_label': 'ID', 'visible': False},
                   {'column_name': 'title', 'column_label': 'Title', 'visible': True},
				   {'column_name': 'description', 'column_label': 'Description', 'visible': False},
				   {'column_name': 'taskScore', 'column_label': 'Score', 'visible': True},
				   {'column_name': 'taskCreated', 'column_label': 'Created', 'visible': True},
				   {'column_name': 'startDate', 'column_label': 'Start date', 'visible': True},
				   {'column_name': 'dueDate', 'column_label': 'Due date', 'visible': True},
				   {'column_name': 'category', 'column_label': 'Category', 'visible': True}]

        table.configure_columns(columns)
        table.insert_row({'idTask': 1, 'title': 'Task 1', 'description': 'Description 1', 'taskScore': 1, 'taskCreated': '2021-01-01', 'startDate': '2021-01-01', 'dueDate': '2021-01-01', 'category': 'Category 1'})
