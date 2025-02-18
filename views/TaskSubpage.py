import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

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
		self.rowconfigure(0, weight=1)

		details_frame = tk.Frame(self)
		details_frame.grid(row=0, column=0, sticky="nswe")
		tk.Label(details_frame, text="Task Details:", font=("Helvetica", 16), anchor='w').pack(fill='x')

		tkv_desctiption = tk.StringVar()
		tkv_desctiption.set(self.controller.task["description"])
		BetterText(details_frame, textvariable=tkv_desctiption).pack(fill='both', expand=True)

		tk.Label(details_frame, text="Category: " + self.controller.task["category"]['name'], anchor='w').pack(fill='x')
		tk.Label(details_frame, text="Created: " + self.controller.task['taskCreated'], anchor='w').pack(fill='x')
		tk.Label(details_frame, text="Due: " + self.controller.task['dueDate'], anchor='w').pack(fill='x')
		tk.Label(details_frame, text="Score: " + str(self.controller.task['taskScore']), anchor='w').pack(fill='x')

		# Workflow
		task_workflow_frame = tk.Frame(self, padx=10)
		task_workflow_frame.grid(row=0, column=1, sticky="nswe")

		if self.controller.task['assigned']:
			tk.Label(task_workflow_frame, text="Assigned to: " + self.controller.task['assigned_user']['firstName'] + " " + self.controller.task['assigned_user']['lastName'], anchor='w').pack(fill='x')
		else:
			tk.Label(task_workflow_frame, text="Not Assigned", anchor='w').pack(fill='x')

		if self.controller.task['finished']:
			tk.Label(task_workflow_frame, text="Completed: " + self.controller.task['finishedDate'], anchor='w').pack(fill='x')
			ttk.Separator(task_workflow_frame, orient='horizontal').pack(fill='x', pady=5)

		if self.controller.task['finished'] and not self.controller.task['rate']:
			tk.Label(task_workflow_frame, text="Not Rated", anchor='w').pack(fill='x')

		if self.controller.task['rate']:
			tk.Label(task_workflow_frame, text="Rated: " + str(self.controller.task['rate_data']['score']), anchor='w').pack(fill='x')
			tk.Label(task_workflow_frame, text="Reviewer: " + self.controller.task['ratedBy'] , anchor='w').pack(fill='x')


		# Action
		action_frame = tk.Frame(self)
		action_frame.grid(row=0, column=2, sticky="ns")

		# Assigne Button for all users if task is not assigned
		if not self.controller.task['assigned']:
			IconButton(action_frame, iconName="assign.png", text="Assign Task", command=self.controller.assign_task).pack(side='top', fill='x')

		if not self.controller.task['finished'] and self.controller.task['myTask']:
			IconButton(action_frame, iconName="finish.png", text="Finish Task", command=self.controller.finish_task).pack(side='top', fill='x')

		# Grand Achievement Button if task is finished
		if self.controller.task['finished']:
			IconButton(action_frame, iconName="assign.png", text="Grand Achievement", command=self.grant_achievement).pack(side='top', fill='x')

		# Rate Task Button if task is finished and not rated for admin
		if self.is_admin and self.controller.task['finished'] and not self.controller.task['rate']:
			IconButton(action_frame, iconName="assign.png", text="Rate Task", command=self.rate_task).pack(side='top', fill='x')

		# Delete Task Button for admin
		if self.is_admin:
			IconButton(action_frame, iconName="delete.png", text="Delete Task", command=self.confirm_delete_task).pack(side='bottom', fill='x')

	def confirm_delete_task(self):
		# response = tk.messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?", icon=tk.messagebox.WARNING)
		# if response:
		# 	self.controller.delete_task()

		self.controller.delete_task()

	def rate_task(self):
		rate_task_window = tk.Toplevel(self)
		rate_task_window.title("Rate Task")

		frame = tk.Frame(rate_task_window)
		frame.pack(fill='both', expand=True, padx=10, pady=10)

		rate = tk.IntVar()
		rate.set(3)

		tk.Label(frame, text="Provide rate 1-5", font=("Helvetica", 16)).pack(fill='x')
		tk.Scale(frame, from_=1, to=5, orient='horizontal', variable=rate).pack(fill='x')
		tk.Button(frame, text="Rate", command=lambda: self.controller.rate_task(rate.get())).pack(fill='x')

	def grant_achievement(self):
		pass