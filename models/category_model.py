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

	def fetch_data(self):
		""" Fetch data from the database and store it in self.data """
		try:
			response = self.masterModel.send_request("api/categories", "GET")

			response.raise_for_status()
			self.data = response.json()

		except requests.RequestException as e:
			Logging.log_error(f"Request failed: {e}")

	def get_categories(self):
		""" Convert categories saved in self.data to Category objects and return them """
		if not self.data or "content" not in self.data:
			print("No data available")
			return []

		categories = []

		for category in self.data.get("content", []):
			idCat = category.get("idCat")
			name = category.get("name")
			description = category.get("description")

			categories.append(Category(idCat, name, description))

		return categories

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