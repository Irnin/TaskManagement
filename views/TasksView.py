import tkinter as tk

from PIL.ImageOps import expand

from views.modules.IconButton import IconButton
from views.modules.PageFrame import PageFrame
from views.modules.Panel import Panel

class TasksView(Panel):
    def __init__(self, parent, controller, is_admin: bool = False):
        super().__init__(parent, "Tasks")

        self.controller = controller
        self.selected_task = None

        self._setup_ui()

    def _setup_ui(self):
        main_frame = tk.Frame(self)
        self.load_main_page(main_frame)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=0)
        main_frame.rowconfigure(0, weight=1)

        data_frame = tk.Frame(main_frame, padx=10)
        data_frame.grid(row=0, column=0, sticky=tk.NSEW)

        action_frame = tk.Frame(main_frame)
        action_frame.grid(row=0, column=1, sticky=tk.NS)

        # Configure the table
        self.table = PageFrame(data_frame, self.controller.fetch_unassigned_tasks, self.controller.open_task, self.task_selected, self.task_unselected)
        self.table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        columns = [{'column_name': 'idTask', 'column_label': 'ID', 'visible': False},
                   {'column_name': 'title', 'column_label': 'Title', 'visible': True},
                   {'column_name': 'description', 'column_label': 'Description', 'visible': False},
                   {'column_name': 'taskScore', 'column_label': 'Score', 'visible': True},
                   {'column_name': 'taskCreated', 'column_label': 'Created', 'visible': False},
                   {'column_name': 'dueDate', 'column_label': 'Due date', 'visible': True},
                   {'column_name': 'categoryName', 'column_label': 'Category', 'visible': True}]

        self.table.configure_columns(columns)
        self.table.load_data()

        # Configure the buttons
        create_task_button = IconButton(action_frame, "add.png", "Create task", lambda: self.controller.open_create_task())
        create_task_button.pack(side=tk.TOP)

        self.assign_task_button = IconButton(action_frame, "assign.png", "Assign task", lambda: self.controller.assign_task(self.selected_task['idTask']))
        self.assign_task_button.pack(side=tk.TOP)
        self.assign_task_button.configure(state=tk.DISABLED)

        if self.controller.masterModel.is_admin():
            self.delete_task_button = IconButton(action_frame, "delete.png", "Delete task", lambda: self.controller.delete_task(self.selected_task['idTask']))
            self.delete_task_button.pack(side=tk.BOTTOM)
            self.delete_task_button.configure(state=tk.DISABLED)

    def task_selected(self, task):
        self.selected_task = task

        self.assign_task_button.configure(state=tk.NORMAL)

        if self.controller.masterModel.is_admin():
            self.delete_task_button.configure(state=tk.NORMAL)

    def task_unselected(self):
        self.selected_task = None

        self.assign_task_button.configure(state=tk.DISABLED)

        if self.controller.masterModel.is_admin():
            self.delete_task_button.configure(state=tk.DISABLED)