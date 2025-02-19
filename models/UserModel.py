class UserModel:
	def __init__(self, masterModel):
		self.masterModel = masterModel

	def change_password(self, current_password, new_password):
		return self.masterModel.send_request(
			endpoint=f"/api/users/update/password",
			method="Patch",
			data={
				"currentPassword": current_password,
				"newPassword": new_password
			}
		)