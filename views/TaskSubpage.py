import tkinter as tk
from tkinter import messagebox

from views.modules.IconButton import IconButton


class TaskSubpage(tk.Frame):

	def __init__(self, parent, controller, is_admin: bool):
		super().__init__(parent)

		self.is_admin = is_admin
		self.controller = controller
		self.setup_ui()

	def setup_ui(self):
		tk.Label(self, text="Task Subpage").pack()

		if self.is_admin:
			IconButton(self, iconName="delete.png", text="Delete Task", command=self.confirm_delete_task).pack()

	def confirm_delete_task(self):
		response = tk.messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?", icon=tk.messagebox.WARNING)
		if response:
			self.controller.delete_task()