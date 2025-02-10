import tkinter as tk
from tkinter import ttk

from views.modules.BetterText import BetterText
from views.modules.PageFrame import PageFrame
from views.modules.PaginatedTableFrame import PaginatedTableFrame
from views.modules.Panel import Panel


class CategoryView(Panel):
    def __init__(self, parent, controller):
        super().__init__(parent, "Categories")

        self.controller = controller

        self.setup_tkinker_variable()
        self.setup_content()
        self.setup_tkinker_events()

    def setup_tkinker_variable(self):
        self.id = tk.StringVar()
        self.name = tk.StringVar()
        self.description = tk.StringVar()

    def setup_tkinker_events(self):
        self.table.table.bind('<<TreeviewSelect>>', self.item_select)

    def item_select(self, event):
        try:
            table = self.table.table
            selected_item = table.selection()[0]

            self.id.set(table.item(selected_item)['values'][0])
            self.name.set(table.item(selected_item)['values'][1])
            self.description.set(table.item(selected_item)['values'][2])

        except IndexError:
            pass

    # GUI
    def setup_content(self):
        content = tk.Frame(self)
        content.pack(fill='both', expand=True)
        self.setup_table(content)
        self.setup_details(content)

    def setup_table(self, parent):
        self.table = PaginatedTableFrame(parent, columns=('id', 'name', 'description'))
        self.table.pack(side='left', fill='y')

    def setup_details(self, parent):
        self.details = tk.Frame(parent)
        self.details.pack(side='left', fill='both', expand=True, padx=10)

        self.setup_category_detail(self.details)

    def setup_category_detail(self, parent):
        tk.Label(parent, text="Details:", font=("Helvetica", 16, "bold"), anchor='w').pack(fill='x', pady=5)

        details_frame = tk.Frame(parent)
        details_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(details_frame, text='ID:', anchor='w').pack(fill='x')
        tk.Entry(details_frame, textvariable=self.id, state='readonly').pack(fill='x')

        tk.Label(details_frame, text='Name', anchor='w').pack(fill='x')
        tk.Entry(details_frame, textvariable=self.name).pack(fill='x')

        tk.Label(details_frame, text='Description', anchor='w').pack(fill='x')
        BetterText(details_frame, textvariable=self.description).pack(fill='x')

        tk.Label(parent, text="Actions:", font=("Helvetica", 16, "bold"), anchor='w').pack(fill='x', pady=5)

        tk.Button(parent, text='Update', command=self.update_category).pack(fill='x', pady=5)

    def select_category(self, tk_id, tk_name):
        self.select_category_window = tk.Toplevel(self)

        self.selected_category_id = tk_id
        self.selected_category_name = tk_name

        self.select_category_window.title("Select Category")

        self.table = PageFrame(self.select_category_window, self.controller.fetch_categories, self.return_selected_category)
        self.table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        columns = [{'column_name': 'idCat', 'column_label': 'ID', 'visible': False},
                   {'column_name': 'name', 'column_label': 'Name', 'visible': True},
                   {'column_name': 'description', 'column_label': 'Description', 'visible': True}]

        self.table.configure_columns(columns)
        self.table.load_data()

    def return_selected_category(self, category):
        self.select_category_window.destroy()

        self.selected_category_id.set(category['idCat'])
        self.selected_category_name.set(category['name'])

    # Actions
    def insert_categories(self, categories):
        self.table.clear_data()

        for category in categories:
            self.table.insert_row((category.id, category.name, category.description))

    def update_category(self):
        id = self.id.get()
        name = self.name.get()
        description = self.description.get()

        if not id:
            return

        self.controller.update_category(id, name, description)