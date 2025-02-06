import tkinter as tk
from tkinter import ttk

class PaginatedTableFrame(tk.Frame):
    def __init__(self, parent, columns: [str]):
        super().__init__(parent)
        self.setup_ui(columns)

    def setup_ui(self, columns):
        self.tableFrame = tk.Frame(self)
        self.tableFrame.columnconfigure((0, 1), weight=1)
        self.tableFrame.rowconfigure(0, weight=1)

        self.table = ttk.Treeview(self.tableFrame, columns=columns, show='headings', selectmode='browse')

        scrollbar_y = ttk.Scrollbar(self.tableFrame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar_y.set)

        for column in columns:
            self.table.heading(column, text=self._get_heading(column))

        self.table.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')

        self.tableFrame.pack(fill='both', expand=True)

    def _get_heading(self, title: str):
        heading = title.upper()
        heading = heading.replace("_", " ")
        return heading

    def insert_row(self, data):
        self.table.insert(parent='', index=tk.END, values=data)

    def clear_data(self):
        for item in self.table.get_children():
            self.table.delete(item)