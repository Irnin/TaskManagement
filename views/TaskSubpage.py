import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from views.modules.BetterText import BetterText
from views.modules.IconButton import IconButton
from views.modules.ScrollableFrame import ScrollableFrame


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

		if self.controller.task['hasAchievement']:
			ttk.Separator(task_workflow_frame, orient='horizontal').pack(fill='x', pady=5)
			tk.Label(task_workflow_frame, text="Achievements:", anchor='w').pack(fill='x')

			achivements_frame = ScrollableFrame(task_workflow_frame)
			achivements_frame.pack(fill='both', expand=True)

			for achivement in self.controller.task['achievements']:
				self.achievement_widget(achivements_frame.scrollable_frame, achivement).pack(fill='x')

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
		if self.is_admin and not self.controller.task['finished']:
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
		self.grant_achievement_window = tk.Toplevel(self)
		self.grant_achievement_window.title("Grant Achievement")

		frame = tk.Frame(self.grant_achievement_window)
		frame.pack(fill='both', expand=True, padx=10, pady=10)

		tkv_title = tk.StringVar()
		tkv_description = tk.StringVar()
		tkv_score = tk.IntVar()

		frame.columnconfigure((0,1), weight=1)
		frame.rowconfigure((0, 1, 2, 3), weight=1)

		tk.Label(frame, text="Title").grid(row=0, column=0, sticky='nsew')
		tk.Entry(frame, textvariable=tkv_title).grid(row=0, column=1, sticky='nsew')

		tk.Label(frame, text="Description").grid(row=1, column=0, sticky='nsew')
		BetterText(frame, textvariable=tkv_description).grid(row=1, column=1, sticky='nsew')

		tk.Label(frame, text="Score").grid(row=2, column=0, sticky='nsew')
		tk.Scale(frame, from_=1, to=5, orient='horizontal', variable=tkv_score).grid(row=2, column=1, sticky='nsew')

		tk.Button(frame, text="Grant", command=lambda: self.controller.grant_achievement(tkv_title.get(), tkv_description.get(), tkv_score.get())).grid(row=3, column=0, columnspan=2, sticky='nsew')

	def destroy_grant_achievement_window(self):
		self.grant_achievement_window.destroy()
		self.controller.reset_view()

	def achievement_widget(self, root, achievement):
		frame = tk.Frame(root)

		frame.columnconfigure((0, 1), weight=1)
		frame.rowconfigure((0, 1, 2, 3), weight=1)

		tk.Label(frame, text=achievement['title'], anchor='w').grid(row=0, column=0, sticky='nsew')
		tk.Label(frame, text=achievement['description'], anchor='w').grid(row=1, column=0, sticky='nsew')
		tk.Label(frame, text="Score: " + str(achievement['valueScore']), anchor='w').grid(row=2, column=0, sticky='nsew')

		if achievement['confirmedBy'] is None:
			tk.Label(frame, text="Pending", anchor='w').grid(row=0, column=1, sticky='nsew')

			if self.is_admin:
				tk.Button(frame, text="Confirm", command= lambda: self.controller.confirm_achievement(achievement['idAchiev'])).grid(row=1, column=1, sticky='nsew')
				tk.Button(frame, text="Reject", command= lambda:self.controller.reject_achievement(achievement['idAchiev'])).grid(row=2, column=1, sticky='nsew')

		ttk.Separator(frame, orient='horizontal').grid(row=3, column=0, columnspan=2, sticky='ew')

		return frame