from models.TaskModel import TaskModel
from utility.logging import Logging
from views.TaskSubpage import TaskSubpage
import tkinter as tk

class TaskController:

	def __init__(self, root: tk.Frame, master_controller, taskId: int, is_admin: bool):
		self.model = TaskModel(master_controller.masterModel)
		self.master_controller = master_controller

		self.taskId = taskId
		self.get_task_details()
		self.is_admin = is_admin
		self.root = root

		self.view = TaskSubpage(root, self, is_admin)

	def delete_task(self):
		Logging.log_info(f"Deleting task with id {self.taskId}")
		self.model.delete_task(self.taskId)

		self.master_controller.reload_data()
		self.master_controller.view.close()

	def get_task_details(self):
		self.task = self.model.get_task(self.taskId).json()

		self.is_assigned()
		self.has_review()
		self.is_my_task()

	def is_assigned(self):
		""" Check if the task is assigned to a user """
		assigned_user = self.model.assigned_user(self.taskId)
		self.task['assigned'] = False

		try:
			assigned_user.raise_for_status()

			data = assigned_user.json()
			if data:
				self.task['assigned'] = True
				self.task['assigned_user'] = data

		except Exception as e:
			Logging.log_info(f"Failed to get assigned user: {e}")

	def has_review(self):
		review = self.model.fetch_review(self.taskId)

		self.task['rate'] = False

		try:
			review.raise_for_status()

			data = review.json()
			if data:
				self.task['rate'] = True
				self.task['rate_data'] = data

				self.task['ratedBy'] = data['createdBy']['firstName'] + " " + data['createdBy']['lastName']

				print(data)

		except Exception as e:
			Logging.log_info(f"Failed to get assigned user: {e}")

	def is_my_task(self):
		self.task['myTask'] = False

		my_id = self.master_controller.masterModel.get_user_id()
		task_assigned_user = self.task.get('assigned_user', {}).get('idUser', -1)

		if my_id == task_assigned_user:
			self.task['myTask'] = True

	# Actions
	def assign_task(self):
		self.master_controller.assign_task(self.taskId)

		self.reset_view()

	def rate_task(self, rate: int):
		self.master_controller.rate_task(self.taskId, rate)

		self.reset_view()

	def finish_task(self):
		self.model.finish_task(self.taskId)

		self.reset_view()

	def reset_view(self):
		self.get_task_details()

		for widget in self.view.winfo_children():
			widget.destroy()

		self.view.destroy()

		self.view = TaskSubpage(self.root, self, self.is_admin)
		self.master_controller.update_subpage(self.view)