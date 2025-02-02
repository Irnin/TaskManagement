import sys

from models.main_model import Model
from utility.logging import Logging
from views.main_view import View

class Controller:
	def __init__(self):
		Logging.log_info(f"Python: {sys.executable}")
		self.model = Model()
		self.view = View(self)

	def run(self):
		self.view.run()

	def login(self, email, password):
		Logging.log_info(f"Logging user with email: {email}")

		if not self.model.login(email, password):
			Logging.log_error(f"Can not login user with email: {email}")
			return False

		self.model.get_user_details()
		return True

	def get_user(self):
		return self.model.user

	def get_tasks(self):
		return self.model.get_tasks()
