import json
import tkinter as tk
from tkinter import ttk

class PageFrame(tk.Frame):

	def __init__(self, root, data_source):
		self.root = root

		super().__init__(self.root)

		self._setup_ui()
		self.fetch_data = data_source

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
		self.control_panel = ControlPanel(self, reload_data=self.load_data)
		self.control_panel.pack(side=tk.BOTTOM, fill=tk.X)

	def configure_columns(self, columns):

		self.table.configure(columns=[column['column_name'] for column in columns])

		for column in columns:
			self.table.heading(column['column_name'], text=column['column_label'])

			if not column['visible']:
				self.table.column(column['column_name'], width=0, stretch=tk.NO)

	def load_data(self, page=0, page_size=25):
		print("Loading data")
		self.remove_all_rows()

		loaded_data = self.fetch_data(page=page, page_size=page_size)
		loaded_data = loaded_data.json()
		self.loaded_data = loaded_data

		for row in loaded_data.get("content", []):
			self.insert_row(row)

		# Update control panel
		first = loaded_data.get("first")
		last = loaded_data.get("last")
		number = loaded_data.get("number")
		total_pages = loaded_data.get("totalPages")
		number_of_elements = loaded_data.get("numberOfElements")

		self.control_panel.update_ui(first, last, number, total_pages, number_of_elements)

	def insert_row(self, data):
		columns = self.table['columns']

		values = [data.get(column, "") for column in columns]

		self.table.insert(parent='', index=tk.END, values=values)

	def remove_all_rows(self):
		for row in self.table.get_children():
			self.table.delete(row)

	def _get_heading(self, title: str):
		heading = title.upper()
		heading = heading.replace("_", " ")
		return heading


class ControlPanel(tk.Frame):
	def __init__(self, root, reload_data=None):
		self.root = root
		self.page = 0

		super().__init__(self.root)

		# TK variables
		self.elements_info = tk.StringVar(value="Elements: 0")
		self.pagination_info = tk.StringVar(value="0 / 0")

		# Methods
		self.reload_data = reload_data

		self._setup_ui()

	def on_selection_change(self, event):
		page = self.page
		self.elemets_per_page = event.widget.get()

		print(f"Page: {page}, Elements per page: {self.elemets_per_page}")

	def _setup_ui(self):
		# Elements per page
		combo_box = ttk.Combobox(self, values=["10", "25", "50", "100"])
		combo_box.set("25")
		combo_box.pack(side=tk.LEFT)

		combo_box.bind("<<ComboboxSelected>>", self.on_selection_change)

		# Previous buttons
		self.previous_buttons = tk.Frame(self)
		self.previous_buttons.pack(side=tk.LEFT)

		self.first_page_button = tk.Button(self.previous_buttons, text="<<", command=self.go_to_first_page)
		self.first_page_button.pack(side=tk.LEFT)

		self.previous_button = tk.Button(self.previous_buttons, text="<", command=self.go_to_previous_page)
		self.previous_button.pack(side=tk.LEFT)

		# Page number
		self.page_number = tk.Label(self, textvariable=self.pagination_info)
		self.page_number.pack(side=tk.LEFT, expand=True)

		# Elements
		tk.Label(self, textvariable=self.elements_info).pack(side=tk.RIGHT)

		# Next buttons
		self.next_buttons = tk.Frame(self)
		self.next_buttons.pack(side=tk.RIGHT)

		self.last_page_button = tk.Button(self.next_buttons, text=">>", command=self.go_to_last_page)
		self.last_page_button.pack(side=tk.RIGHT)

		self.next_button = tk.Button(self.next_buttons, text=">", command=self.go_to_next_page)
		self.next_button.pack(side=tk.RIGHT)

	def update_ui(self, first: bool, last: bool, page: int, total_pages: int, number_of_elements: int):
		self.toggle_previous_buttons(not first)
		self.toggle_next_buttons(not last)

		self.page = page
		self.total_pages = total_pages

		page_format = f" {self.page + 1} / {total_pages}"
		self.pagination_info.set(page_format)

		self.elements_info.set(f"Elements: {number_of_elements}")

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

	def go_to_next_page(self):
		self.page += 1
		self.reload_data(page=self.page, page_size=25)

	def go_to_previous_page(self):
		self.page -= 1
		self.reload_data(page=self.page, page_size=25)

	def go_to_first_page(self):
		self.page = 0
		self.reload_data(page=self.page, page_size=25)

	def go_to_last_page(self):
		self.page = self.total_pages - 1
		self.reload_data(page=self.page, page_size=25)