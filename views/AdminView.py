import tkinter as tk
from errno import EUSERS
from tkinter import ttk

from views.modules.BetterText import BetterText
from views.modules.IconButton import IconButton
from views.modules.PageFrame import PageFrame
from views.modules.PaginatedTableFrame import PaginatedTableFrame
from views.modules.Panel import Panel


class AdminView(Panel):
    def __init__(self, parent, controller):
        super().__init__(parent, "Admin panel")

        self.controller = controller

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
        self.table = PageFrame(data_frame, self.controller.fetch_admin_jobs, self.controller.open_task)
        self.table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        columns = [{'column_name': 'idTask', 'column_label': 'ID', 'visible': True},
                   {'column_name': 'title', 'column_label': 'Title', 'visible': True},
                   {'column_name': 'description', 'column_label': 'Description', 'visible': False},
                   {'column_name': 'taskScore', 'column_label': 'Score', 'visible': True},
                   {'column_name': 'taskCreated', 'column_label': 'Created', 'visible': False},
                   {'column_name': 'dueDate', 'column_label': 'Due date', 'visible': False},
                   {'column_name': 'categoryName', 'column_label': 'Category', 'visible': True}]

        self.table.configure_columns(columns)
        self.table.load_data()

        # Action Buttons
        category_button = IconButton(action_frame, "adminCategories.png", "Categories", self.controller.open_category)
        category_button.pack(side=tk.TOP, fill=tk.X)

        users_button = IconButton(action_frame, "admin.png", "Users", self.controller.open_users)
        users_button.pack(side=tk.TOP, fill=tk.X)


