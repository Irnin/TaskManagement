import tkinter as tk

from views.modules.IconButton import IconButton
from views.modules.PageFrame import PageFrame


class CategorySubpage(tk.Frame):

	def __init__(self, parent, controller):
		super().__init__(parent)

		self.controller = controller
		self.setup_ui()

	def setup_ui(self):
		main_frame = tk.Frame(self)
		main_frame.pack(fill=tk.BOTH, expand=True)

		main_frame.columnconfigure(0, weight=1)
		main_frame.columnconfigure(1, weight=0)
		main_frame.rowconfigure(0, weight=1)

		data_frame = tk.Frame(main_frame, padx=10)
		data_frame.grid(row=0, column=0, sticky=tk.NSEW)

		action_frame = tk.Frame(main_frame)
		action_frame.grid(row=0, column=1, sticky=tk.NS)

		# Configure the table
		self.table = PageFrame(data_frame, self.controller.fetch_categories, self.controller.open_task)
		self.table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		columns = [{'column_name': 'idCat', 'column_label': 'ID', 'visible': True},
		           {'column_name': 'name', 'column_label': 'Title', 'visible': True},
		           {'column_name': 'description', 'column_label': 'Description', 'visible': True}]

		self.table.configure_columns(columns)
		self.table.load_data()

		# Action Buttons
		category_button = IconButton(action_frame, "tasks.png", "Create category", self.create_category)
		category_button.pack(side=tk.TOP, fill=tk.X)

	def create_category(self):
		self.create_category_window = tk.Toplevel(self)
		self.create_category_window.title("Create category")

		frame = tk.Frame(self.create_category_window, pady=10, padx=10)
		frame.pack(fill=tk.BOTH, expand=True)

		frame.columnconfigure((0, 1), weight=1)
		frame.rowconfigure((0, 1, 2), weight=1)

		tkv_category_name = tk.StringVar()
		tkv_category_description = tk.StringVar()

		tk.Label(frame, text="Name").grid(row=0, column=0)
		tk.Entry(frame, textvariable=tkv_category_name).grid(row=0, column=1)

		tk.Label(frame, text="Description").grid(row=1, column=0)
		tk.Entry(frame, textvariable=tkv_category_description).grid(row=1, column=1)

		tk.Button(frame, text="Create", command=lambda: self.controller.create_category(tkv_category_name.get(), tkv_category_description.get())).grid(row=2, column=0, columnspan=2)

	def destroy_create_category_window(self):
		self.create_category_window.destroy()