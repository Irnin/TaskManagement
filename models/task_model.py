class TaskModel:
	def __init__(self, masterModel):
		self.masterModel = masterModel

	def fetch_unassigned_tasks(self, page, page_size):
		return self.masterModel.send_request(
			endpoint="/api/tasks/unassigned",
			method="GET",
			params={"page": page, "pageSize": page_size}
		)