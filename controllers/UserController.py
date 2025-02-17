from models.UserModel import UserModel
from views.UserView import UserView


class UserController:
	def __init__(self, controller):
		self.masterController = controller
		self.masterModel = controller.model
		self.masterView = controller.view

		self.model = UserModel(self.masterModel)
		self.view = UserView(self.masterView, self)

		user_name = f"{self.masterModel.user.first_name} {self.masterModel.user.last_name}"
		self.view.update_header(f"Account - {user_name}")

		self.is_admin = self.masterModel.is_admin()

	def test_method(self):
		print("test method")