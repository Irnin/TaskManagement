import requests

from utility.logging import Logging

class Category:
	def __init__(self, id, name, description):
		self.id = id
		self.name = name
		self.description = description

	def __str__(self):
		return f"Category: {self.name} ({self.id})"

class CategoryModel:
	def __init__(self, masterModel):
		self.masterModel = masterModel

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

	def update_category(self, id, name, description):
		""" Update category with id with new name and description """
		request_data = {
			"idCat": id,
			"name": name,
			"description": description
		}

		response = self.masterModel.send_request(f"api/updateCategory/{id}", "PUT", data=request_data)

		if response:
			Logging.log_success(f"Category {name} updated")
			return True
		else:
			Logging.log_error(f"Failed to update category {name}")
			return False

	def get_admin_jobs(self, page, page_size):
		return self.masterModel.send_request(
			endpoint="/api/tasks/adminJobs",
			method="GET",
			params={"page": page, "size": page_size}
		)