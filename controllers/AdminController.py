from controllers.TaskController import TaskController
from models.CategoryModel import CategoryModel
from views.AdminView import AdminView
from views.CategorySubpage import CategorySubpage


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

	def create_category(self, name, description):

		if not name.strip() or not description.strip():
			return

		self.model.create_category(name, description)
		self.category_view.table.reload_data()
		self.category_view.destroy_create_category_window()


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

	def open_category(self):
		self.category_view = CategorySubpage(self.view, self)
		self.view.update_header("Categories")
		self.view.load_subpage(self.category_view)