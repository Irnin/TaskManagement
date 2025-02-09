from models.TaskModel import TaskModel
from utility.logging import Logging
from views.TaskSubpage import TaskSubpage
import tkinter as tk

class TaskController:

	def __init__(self, root: tk.Frame, master_controller, taskId: int, is_admin: bool):
		self.model = master_controller.model
		self.master_controller = master_controller
		self.view = TaskSubpage(root, self, is_admin)

		self.taskId = taskId

		self.master_controller = master_controller

	def delete_task(self):
		Logging.log_info(f"Deleting task with id {self.taskId}")
		self.model.delete_task(self.taskId)

		self.master_controller.reload_data()
		self.master_controller.view.close()