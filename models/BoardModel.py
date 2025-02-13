class BoardModel:
	def __init__(self, masterModel):
		self.masterModel = masterModel

	def fetch_assigned_tasks(self, page, page_size, id):

		return self.masterModel.send_request(
			endpoint=f"/api/tasks/user/{id}",
			method="GET",
			params={"page": page, "size": page_size}
		)

	def unassigne_task(self, id):
		self.masterModel.send_request(
			endpoint=f"/api/tasks/unassigne/{id}",
			method="PATCH"
		)

	def finish_task(self, id):
		self.masterModel.send_request(
			endpoint=f"/api/tasks/complete/{id}",
			method="PATCH"
		)