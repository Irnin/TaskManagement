import requests

from utility.logging import Logging


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

	def assign_task(self, taskId, userId):
		response = self.masterModel.send_request(
			endpoint=f"/api/tasks/assigne/{taskId}/to/{userId}",
			method="PATCH"
		)

		return response

	def get_task(self, taskId):
		return self.masterModel.send_request(
			endpoint=f"/api/task/{taskId}",
			method="GET"
		)

	def assigned_user(self, taskId):
		return self.masterModel.send_request(
			endpoint=f"/api/task/{taskId}/assignedUser",
			method="GET"
		)

	def rate_task(self, task_id, rate):
		return self.masterModel.send_request(
			endpoint=f"/api/rate/tasks/{task_id}/rate",
			method="PATCH",
			data={"score": rate}
		)

	def fetch_review(self, taskId):
		return self.masterModel.send_request(
			endpoint=f"/api/task/{taskId}/rate",
			method="GET"
		)

	def fetch_achievements(self, taskId):
		return self.masterModel.send_request(
			endpoint=f"api/achievements/task/{taskId}",
			method="GET"
		)

	def finish_task(self, task_id):
		self.masterModel.send_request(
			endpoint=f"/api/tasks/complete/{task_id}",
			method="PATCH"
		)

	def get_categories(self, page: int = 0, page_size: int = 25):
		""" Fetch data from the database and store it in self.data """
		try:
			response = self.masterModel.send_request(
				endpoint="/api/categories",
				method="GET",
				params={"page": page, "size": page_size})

			response.raise_for_status()
			return response

		except requests.RequestException as e:
			Logging.log_error(f"Request failed: {e}")

	def grant_achievement(self, task_id, title, description, score):

		print(task_id, title, description, score)

		self.masterModel.send_request(
			endpoint=f"api/achievements/create/forTask/{task_id}",
			method="POST",
			data={
				"title": title,
				"description": description,
				"valueScore": score
			}
		)

	def accept_achievement(self, achievementId):
		self.masterModel.send_request(
			endpoint=f"api/achievements/confirm/{achievementId}",
			method="PATCH"
		)

	def reject_achievement(self, achievementId):
		self.masterModel.send_request(
			endpoint=f"api/achievements/{achievementId}",
			method="DELETE"
		)

	def fetch_finished_tasks(self, page, page_size):
		return self.masterModel.send_request(
			endpoint=f"api/tasks/finished",
			method="GET"
		)

	def find_users_for_task(self, task_id):
		return self.masterModel.send_request(
			endpoint=f"api/tasks/findUsersForTask/{task_id}",
			method="GET"
		)

	def assign_task_to_user(self, taskId, userId):
		return self.masterModel.send_request(
			endpoint=f"api/tasks/assigne/{taskId}/to/{userId}",
			method="PATCH"
		)
