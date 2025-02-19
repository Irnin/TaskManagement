from controllers.TaskController import TaskController
from models.CategoryModel import CategoryModel
from views.AdminView import AdminView
from views.CategorySubpage import CategorySubpage
from views.UsersSubpage import UsersSubpage


class AdminController:
	def __init__(self, controller):
		self.masterController = controller
		self.masterModel = controller.model
		self.masterView = controller.view

		self.model = CategoryModel(self.masterModel)
		self.view = AdminView(self.masterView, self)

	def fetch_categories(self, page: int = 0, page_size: int = 25):
		return self.model.get_categories(page=page, page_size=page_size)

	def fetch_users(self, page: int = 0, page_size: int = 25):
		print(self.model.get_users(page=page, page_size=page_size))
		return self.model.get_users(page=page, page_size=page_size)

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
		self.masterController.open_task(task['idTask'])

	def open_category(self):
		self.category_view = CategorySubpage(self.view, self)
		self.view.update_header("Categories")
		self.view.load_subpage(self.category_view)

	def open_users(self):
		self.users_view = UsersSubpage(self.view, self)
		self.view.update_header("Users")
		self.view.load_subpage(self.users_view)

	def update_subpage(self, view):
		self.view.load_subpage(view)

	def create_user(self, email, first_name, last_name, password):
		if not email.strip() or not first_name.strip() or not last_name.strip() or not password.strip():
			return

		self.model.create_user(email, first_name, last_name, password)
		self.users_view.table.reload_data()
		self.users_view.destroy_create_user_window()

	def grant_admin_role(self, user_id):
		self.model.update_role(user_id, 0)
		self.users_view.table.reload_data()

	def grant_employee_role(self, user_id):
		self.model.update_role(user_id, 1)
		self.users_view.table.reload_data()
