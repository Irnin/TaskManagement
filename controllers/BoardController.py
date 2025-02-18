from controllers.TaskController import TaskController
from models.BoardModel import BoardModel
from views.BoardView import BoardView

class BoardController:
	def __init__(self, controller):
		self.masterController = controller
		self.masterModel = controller.model
		self.masterView = controller.view

		self.model = BoardModel(self.masterModel)
		self.view = BoardView(self.masterView, self)

	def fetch_assigned_tasks(self, page: int, page_size: int):
		user_id = self.masterModel.user.id

		return self.model.fetch_assigned_tasks(page, page_size, user_id)

	def open_task(self, task):
		task_controller = TaskController(self.view, self, task['idTask'], self.masterModel.is_admin())

		self.view.update_header(f"Task [{task['idTask']}] - {task['title']}")

		self.view.load_subpage(task_controller.view)

	def unassigne_task(self, task_id: int):
		self.model.unassigne_task(task_id)

		self.view.table.load_data()

	def finish_task(self, task_id: int):
		self.model.finish_task(task_id)

		self.view.table.load_data()

	def update_subpage(self, view):
		self.view.load_subpage(view)