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

	def fetch_data(self, page=None, page_size=None):
		""" Fetch data from the database and store it in self.data """
		try:
			response = self.masterModel._send_request("api/categories", "GET", page=page, page_size=page_size)

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

		print(request_data)

		response = self.masterModel._send_request(f"api/categories/{id}", "PUT", data=request_data)

		if response:
			return True
		else:
			return False