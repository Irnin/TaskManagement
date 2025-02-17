import tkinter as tk
from tkinter import messagebox

from views.modules.BetterText import BetterText
from views.modules.IconButton import IconButton

class TaskSubpage(tk.Frame):

	def __init__(self, parent, controller, is_admin: bool):
		super().__init__(parent)

		self.is_admin = is_admin
		self.controller = controller
		self.setup_ui()

	def setup_ui(self):
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=0)
		self.rowconfigure(0, weight=0)

		details_frame = tk.Frame(self)
		details_frame.grid(row=0, column=0, sticky="nswe")
		tk.Label(details_frame, text="Task Details", font=("Helvetica", 16), anchor='w').pack(fill='x')

		tkv_desctiption = tk.StringVar()
		tkv_desctiption.set(self.controller.task["description"])
		BetterText(details_frame, textvariable=tkv_desctiption).pack(fill='both', expand=True)

		tk.Label(details_frame, text="Category: " + self.controller.task["category"]['name'], anchor='w').pack(fill='x')
		tk.Label(details_frame, text="Created: " + self.controller.task['taskCreated'], anchor='w').pack(fill='x')
		tk.Label(details_frame, text="Due: " + self.controller.task['dueDate'], anchor='w').pack(fill='x')
		tk.Label(details_frame, text="Score: " + str(self.controller.task['taskScore']), anchor='w').pack(fill='x')

		action_frame = tk.Frame(self)
		action_frame.grid(row=0, column=2, sticky="ns")

		if self.is_admin:
			IconButton(action_frame, iconName="delete.png", text="Delete Task", command=self.confirm_delete_task).pack(side='bottom', fill='x')

	def confirm_delete_task(self):
		# response = tk.messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?", icon=tk.messagebox.WARNING)
		# if response:
		# 	self.controller.delete_task()

		self.controller.delete_task()