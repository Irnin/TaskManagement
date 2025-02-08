import tkinter as tk
from tkinter import ttk

class PageFrame(tk.Frame):

	def __init__(self, root):
		self.root = root

		super().__init__(self.root)

		self._setup_ui()

	def _setup_ui(self):
		self.tableFrame = tk.Frame(self)
		self.tableFrame.columnconfigure(0, weight=1)
		self.tableFrame.columnconfigure(1, weight=0)
		self.tableFrame.rowconfigure(0, weight=1)
		self.tableFrame.pack(fill='both', expand=True)

		self.table = ttk.Treeview(self.tableFrame, show='headings', selectmode='browse')
		self.table.grid(row=0, column=0, sticky='nsew')

		scrollbar_y = ttk.Scrollbar(self.tableFrame, orient="vertical", command=self.table.yview)
		self.table.configure(yscrollcommand=scrollbar_y.set)
		scrollbar_y.grid(row=0, column=1, sticky='ns')

		# Control panel
		self.control_panel = ControlPanel(self, 4)
		self.control_panel.pack(side=tk.BOTTOM, fill=tk.X)

	def configure_columns(self, columns):

		self.table.configure(columns=[column['column_name'] for column in columns])

		for column in columns:
			self.table.heading(column['column_name'], text=column['column_label'])

			if not column['visible']:
				self.table.column(column['column_name'], width=0, stretch=tk.NO)

	def insert_row(self, data):
		columns = self.table['columns']

		values = [data.get(column, "") for column in columns]

		self.table.insert(parent='', index=tk.END, values=values)

	def _get_heading(self, title: str):
		heading = title.upper()
		heading = heading.replace("_", " ")
		return heading


class ControlPanel(tk.Frame):
	def __init__(self, root, totalPages):
		self.root = root
		self.page = 0
		self.totalPages = totalPages

		super().__init__(self.root)

		self._setup_ui()

	def _setup_ui(self):
		# Previous buttons
		self.previous_buttons = tk.Frame(self)
		self.previous_buttons.pack(side=tk.LEFT)

		self.first_page_button = tk.Button(self.previous_buttons, text="<<")
		self.first_page_button.pack(side=tk.LEFT)

		self.previous_button = tk.Button(self.previous_buttons, text="<")
		self.previous_button.pack(side=tk.LEFT)

		# Page number
		self.page_number = tk.Label(self, text=self._page_format())
		self.page_number.pack(side=tk.LEFT, expand=True)

		# Next buttons
		self.next_buttons = tk.Frame(self)
		self.next_buttons.pack(side=tk.RIGHT)

		self.next_button = tk.Button(self.next_buttons, text=">")
		self.next_button.pack(side=tk.RIGHT)

		self.last_page_button = tk.Button(self.next_buttons, text=">>")
		self.last_page_button.pack(side=tk.RIGHT)

	def _page_format(self) -> str:
		return f" {self.page + 1} / {self.totalPages}"

	def toggle_previous_buttons(self, available: bool):
		if available:
			self.first_page_button.config(state=tk.NORMAL)
			self.previous_button.config(state=tk.NORMAL)
		else:
			self.first_page_button.config(state=tk.DISABLED)
			self.previous_button.config(state=tk.DISABLED)

	def toggle_next_buttons(self, state):
		if state:
			self.next_button.config(state=tk.NORMAL)
			self.last_page_button.config(state=tk.NORMAL)
		else:
			self.next_button.config(state=tk.DISABLED)
			self.last_page_button.config(state=tk.DISABLED)