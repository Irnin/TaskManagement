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

	def change_password(self, current_password, new_password, confirm_password):
		if not current_password.strip():
			return

		if not new_password.strip():
			return

		if not confirm_password.strip():
			return

		if new_password != confirm_password:
			return

		self.model.change_password(current_password, new_password)