from models.task_model import TaskModel
from views.task_view import TaskView

class TaskController:
	def __init__(self, controller):
		self.masterController = controller
		self.masterModel = controller.model
		self.masterView = controller.view

		self.view = TaskView(self.masterView, self)
		self.model = TaskModel(self.masterModel)