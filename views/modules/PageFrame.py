import json
import tkinter as tk
from tkinter import ttk

class PageFrame(tk.Frame):

	def __init__(self, root, data_source, double_click_method=None):
		self.root = root

		super().__init__(self.root)

		self._setup_ui()
		self.fetch_data = data_source

		self.table.bind("<Double-1>", self.double_click)
		self.double_click_method = double_click_method

	def _setup_ui(self):
		self.tableFrame = tk.Frame(self)
		self.tableFrame.columnconfigure(0, weight=1)
		self.tableFrame.columnconfigure(1, weight=0)

		self.tableFrame.rowconfigure(0, weight=1)
		self.tableFrame.rowconfigure(1, weight=0)

		self.tableFrame.pack(fill='both', expand=True)

		self.table = ttk.Treeview(self.tableFrame, show='headings', selectmode='browse')
		self.table.grid(row=0, column=0, sticky='nsew')

		scrollbar_y = ttk.Scrollbar(self.tableFrame, orient="vertical", command=self.table.yview)
		self.table.configure(yscrollcommand=scrollbar_y.set)
		scrollbar_y.grid(row=0, column=1, sticky='ns')

		scrollbar_x = ttk.Scrollbar(self.tableFrame, orient="horizontal", command=self.table.xview)
		self.table.configure(xscrollcommand=scrollbar_x.set)
		scrollbar_x.grid(row=1, column=0, sticky='ew')

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
		self.remove_all_rows()

		loaded_data = self.fetch_data(page=page, page_size=page_size)
		loaded_data = loaded_data.json()

		print(loaded_data)

		for row in loaded_data.get("content", []):
			self.insert_row(row)

		# Update control panel
		first = loaded_data.get("first")
		last = loaded_data.get("last")
		number = loaded_data.get("number")
		total_pages = loaded_data.get("totalPages")
		total_elements = loaded_data.get("totalElements")

		self.control_panel.update_ui(first, last, number, total_pages, total_elements)

	def reload_data(self):
		page = self.control_panel.page
		page_size = self.control_panel.elements_per_page

		self.load_data(page=page, page_size=page_size)

	def insert_row(self, data):
		columns = self.table['columns']

		values = [data.get(column, "") for column in columns]

		self.table.insert(parent='', index=tk.END, values=values)

	def remove_all_rows(self):
		for row in self.table.get_children():
			self.table.delete(row)

	def double_click(self, event):
		item = self.table.selection()[0]

		values = self.table.item(item, 'values')
		column_names = self.table['columns']

		# Create a dictionary with column names as keys and their corresponding values
		item_dict = {column: value for column, value in zip(column_names, values)}

		self.double_click_method(item_dict)

class ControlPanel(tk.Frame):
	def __init__(self, root, reload_data=None):
		self.root = root
		self.page = 0
		self.elements_per_page = 25

		super().__init__(self.root)

		# TK variables
		self.tkv_elements_info = tk.StringVar(value="Elements: 0")
		self.tkv_pagination_info = tk.StringVar(value="0 / 0")
		self.tkv_elements_per_page = tk.StringVar(value="Elements per page: 25")

		# Methods
		self.reload_data = reload_data

		self._setup_ui()

	def _setup_ui(self):
		# Elements per page
		menu_button = tk.Menubutton(self, textvariable=self.tkv_elements_per_page, relief=tk.RAISED)
		menu = tk.Menu(menu_button, tearoff=0)
		menu_button.configure(menu=menu)
		menu_button.pack(side=tk.LEFT)

		menu.add_command(label="10", command=lambda: self._update_elements_per_page(10))
		menu.add_command(label="25", command=lambda: self._update_elements_per_page(25))
		menu.add_command(label="50", command=lambda: self._update_elements_per_page(50))
		menu.add_command(label="75", command=lambda: self._update_elements_per_page(75))
		menu.add_command(label="100", command=lambda: self._update_elements_per_page(100))

		# Previous buttons
		self.previous_buttons = tk.Frame(self)
		self.previous_buttons.pack(side=tk.LEFT, expand=True)

		self.first_page_button = tk.Button(self.previous_buttons, text="<<", command=self._go_to_first_page)
		self.first_page_button.pack(side=tk.LEFT)

		self.previous_button = tk.Button(self.previous_buttons, text="<", command=self._go_to_previous_page)
		self.previous_button.pack(side=tk.LEFT)

		# Page number
		self.page_number = tk.Label(self, textvariable=self.tkv_pagination_info)
		self.page_number.pack(side=tk.LEFT, expand=True)

		# Elements
		tk.Label(self, textvariable=self.tkv_elements_info).pack(side=tk.RIGHT)

		# Next buttons
		self.next_buttons = tk.Frame(self)
		self.next_buttons.pack(side=tk.RIGHT, expand=True)

		self.last_page_button = tk.Button(self.next_buttons, text=">>", command=self._go_to_last_page)
		self.last_page_button.pack(side=tk.RIGHT)

		self.next_button = tk.Button(self.next_buttons, text=">", command=self._go_to_next_page)
		self.next_button.pack(side=tk.RIGHT)

	def update_ui(self, first: bool, last: bool, page: int, total_pages: int, total_elements: int):
		self.toggle_previous_buttons(not first)
		self.toggle_next_buttons(not last)

		self.page = page
		self.total_pages = total_pages

		page_format = f" {self.page + 1} / {total_pages}"
		self.tkv_pagination_info.set(page_format)

		self.tkv_elements_info.set(f"Elements: {total_elements}")

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

	# Actions
	def _go_to_previous_page(self):
		self.page -= 1
		self.reload_data(page=self.page, page_size=self.elements_per_page)

	def _go_to_next_page(self):
		self.page += 1
		self.reload_data(page=self.page, page_size=self.elements_per_page)

	def _go_to_first_page(self):
		self.page = 0
		self.reload_data(page=self.page, page_size=self.elements_per_page)

	def _go_to_last_page(self):
		self.page = self.total_pages - 1
		self.reload_data(page=self.page, page_size=self.elements_per_page)

	def _update_elements_per_page(self, elements_per_page):
		self.elements_per_page = elements_per_page
		self.tkv_elements_per_page.set(f"Elements per page: {elements_per_page}")
		self.reload_data(page=self.page, page_size=self.elements_per_page)