import tkinter as tk

from views.modules.PageFrame import PageFrame


class Archive(tk.Frame):

	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller

		self.setup_ui()

	def setup_ui(self):
		frame = tk.Frame(self)
		frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		self.table = PageFrame(frame, self.controller.fetch_finished_tasks, self.controller.open_task)
		self.table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		columns = [{'column_name': 'idTask', 'column_label': 'ID', 'visible': True},
		           {'column_name': 'title', 'column_label': 'Title', 'visible': True},
		           {'column_name': 'description', 'column_label': 'Description', 'visible': False},
		           {'column_name': 'taskScore', 'column_label': 'Score', 'visible': True},
		           {'column_name': 'taskCreated', 'column_label': 'Created', 'visible': False},
		           {'column_name': 'dueDate', 'column_label': 'Due date', 'visible': True},
		           {'column_name': 'categoryName', 'column_label': 'Category', 'visible': True}]

		self.table.configure_columns(columns)
		self.table.load_data()
