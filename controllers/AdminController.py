from controllers.TaskController import TaskController
from models.CategoryModel import CategoryModel
from views.AdminView import AdminView

class AdminController:
	def __init__(self, controller):
		self.masterController = controller
		self.masterModel = controller.model
		self.masterView = controller.view

		self.model = CategoryModel(self.masterModel)
		self.view = AdminView(self.masterView, self)

	def fetch_categories(self, page: int = 0, page_size: int = 25):
		return self.model.get_categories(page=page, page_size=page_size)

	def update_category(self, id, name, description):
		self.model.update_category(id, name, description)
		self.model.get_categories()

		categories = self.model.get_categories()
		self.view.insert_categories(categories)

	def select_category(self, category):

		self.place_for_category = category
		self.view.select_category()

	def selected_category(self, category):
		self.place_for_category = category
		self.view.return_selected_category(category)

	def fetch_admin_jobs(self, page: int = 0, page_size: int = 25):
		return self.model.get_admin_jobs(page=page, page_size=page_size)

	def open_task(self, task):
		task_controller = TaskController(self.view, self, task['idTask'], self.masterModel.is_admin())

		self.view.update_header(f"Task [{task['idTask']}] - {task['title']}")

		self.view.load_subpage(task_controller.view)
