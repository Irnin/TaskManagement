class TaskModel:
	def __init__(self, masterModel):
		self.masterModel = masterModel

	def fetch_unassigned_tasks(self, page, page_size):
		return self.masterModel.send_request(
			endpoint="/api/tasks/unassigned",
			method="GET",
			params={"page": page, "size": page_size}
		)

	def delete_task(self, taskId):
		return self.masterModel.send_request(
			endpoint="/api/task/" + str(taskId),
			method="DELETE"
		)

	def create_task(self, title, description, category_id, task_score, due_date):
		response = self.masterModel.send_request(
			endpoint=f"/api/createTask/category/{category_id}",
			method="POST",
			data={
				"title": title,
				"description": description,
				"taskScore": task_score,
				"dueDate": due_date
			}
		)

		return response