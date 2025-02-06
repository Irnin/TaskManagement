import tkinter as tk
from tkinter import ttk

from views.modules.BetterText import BetterText
from views.modules.PaginatedTableFrame import PaginatedTableFrame

class CategoryView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.setup_tkinker_variable()
        self.setup_ui()
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
    def setup_ui(self):
        self.setup_header()
        self.setup_content()

    def setup_header(self):
        tk.Label(self, text="Categories", font=("Helvetica", 20, "bold"), anchor='w').pack(fill='x')
        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=10)

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