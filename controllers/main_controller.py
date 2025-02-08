import sys

from controllers.board_controller import BoardController
from controllers.category_controller import CategoryController
from controllers.task_controller import TaskController
from models.main_model import Model
from utility.logging import Logging
from views.main_view import View

class Controller:
	def __init__(self):
		Logging.log_info(f"Python: {sys.version}")
		self.model = Model()
		self.view = View(self)

	def run(self):
		self.view.run()

	def open_page(self, page: str):
		self.view.remove_current_page()

		if page == "board":
			board_controller = BoardController(self)
			self.view.open_page(board_controller.view, page)

		elif page == "tasks":
			task_controller = TaskController(self)
			self.view.open_page(task_controller.view, page)

		elif page == "categories":
			category_controller = CategoryController(self)
			self.view.open_page(category_controller.view, page)

	def login(self, email, password):
		Logging.log_info(f"Logging user with email: {email}")

		if not self.model.login(email, password):
			Logging.log_error(f"Can not login user with email: {email}")
			return False

		self.model.get_user_details()
		return True

	def get_user(self):
		return self.model.user
