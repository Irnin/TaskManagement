import tkinter as tk
from tkinter import ttk

class CategoryView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
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
        table = self.table.table
        selected_item = table.selection()[0]

        self.id.set(table.item(selected_item)['values'][0])
        self.name.set(table.item(selected_item)['values'][1])
        self.description.set(table.item(selected_item)['values'][2])

        self.text_widget.delete('1.0', tk.END)
        self.text_widget.insert(tk.END, table.item(selected_item)['values'][2])

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
        self.description_text = self.create_multiline_text(details_frame, self.description).pack(fill='x')

    def create_multiline_text(self, parent, text_var):
        """Creates a multi-line text input with a scrollbar and binding to StringVar."""
        # Frame for text and scrollbar
        frame = tk.Frame(parent)

        # Text widget
        self.text_widget = tk.Text(frame, height=5, wrap='word', width=30, font=("Helvetica", 12))
        self.text_widget.pack(side='left', fill='both', expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(frame, command=self.text_widget.yview)
        scrollbar.pack(side='right', fill='y')
        self.text_widget.config(yscrollcommand=scrollbar.set)

        # Insert initial text
        self.text_widget.insert('1.0', text_var.get())

        # Update StringVar on focus out
        def update_text_var(event=None):
            text_var.set(self.text_widget.get('1.0', 'end-1c'))

        self.text_widget.bind('<FocusOut>', update_text_var)

        # Return frame that contains the Text widget
        return frame

    # Actions
    def insert_categories(self, categories):
        for category in categories:
            self.table.insert_row((category.id, category.name, category.description))

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