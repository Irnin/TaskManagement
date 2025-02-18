import sys

from controllers.BoardController import BoardController
from controllers.AdminController import AdminController
from controllers.TasksController import TasksController
from controllers.UserController import UserController
from models.MainModel import Model
from utility.logging import Logging
from views.MainView import View

class Controller:
	def __init__(self):
		Logging.log_info(f"Python: {sys.version}")
		self.model = Model()
		self.view = View(self)

	def run(self):
		self.view.run()

	def open_page(self, page: str):
		""" Method loads page to the main window"""
		Logging.log_info(f"Open page: {page}")
		self.view.remove_current_page()

		if page == "board":
			board_controller = BoardController(self)
			self.view.open_page(board_controller.view, page)

		elif page == "tasks":
			self.task_controller = TasksController(self)
			self.view.open_page(self.task_controller.view, page)

		elif page == "admin":
			admin_controller = AdminController(self)
			self.view.open_page(admin_controller.view, page)

		elif page == "account":
			user_controller = UserController(self)
			self.view.open_page(user_controller.view, page)

	def login(self, email, password):
		Logging.log_info(f"{email} tries to login")

		if not self.model.login(email, password):
			Logging.log_error(f"Can not login user with email: {email}")
			return False

		Logging.log_success(f"{email} logged in")
		self.model.get_user_details()
		return True

	def get_user(self):
		return self.model.user

	def open_task(self, task_id):
		self.open_page("tasks")

		self.task_controller.open_task_with_id(task_id)