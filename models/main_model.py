import requests

from utility.logging import Logging


class Model:

	def __init__(self):
		self.app_url = "http://127.0.0.1:8080"

	def _send_request(self, endpoint, method="GET", data=None, params=None):
		url = f"{self.app_url}/{endpoint.lstrip('/')}"
		headers = {"Content-Type": "application/json"}

		if hasattr(self, 'user') and self.user is not None:
			headers.update({"Authorization": f"Bearer {self.user.token}"})

		try:
			if method.upper() == "GET":
				response = requests.get(url, params=params, headers=headers)
			elif method.upper() == "POST":
				response = requests.post(url, json=data, headers=headers)
			elif method.upper() == "PUT":
				response = requests.put(url, json=data, headers=headers)
			elif method.upper() == "DELETE":
				response = requests.delete(url, headers=headers)
			else:
				raise ValueError(f"Unsupported HTTP method: {method}")

			response.raise_for_status()
			return response.json()
		except requests.RequestException as e:
			Logging.log_warning(f"Request failed: {e}")
			return None

	def login(self, email, password) -> bool:
		request_data = {
			"email": email,
			"password": password
		}

		response = self._send_request(
			endpoint="/auth/login",
			method="POST",
			data=request_data
		)

		if response:
			token = response.get("token")
			self.user = User(token)

			return True
		else:
			return False

	def get_user_details(self):
		response = self._send_request(
			endpoint="/api/users/myAccount",
			method="GET",
		)

		if response:
			id = response.get("id")
			first_name = response.get("firstName")
			last_name = response.get("lastName")
			email = response.get("email")
			role = response.get("role")
			phone_number = response.get("phoneNumber")
			address = response.get("address")
			zipcode = response.get("zipcode")
			city = response.get("city")

			self.user.update_details(id, first_name, last_name, email, role, phone_number, address, zipcode, city)

			return True
		else:
			return False

	def get_tasks(self):
		response = self._send_request(
			endpoint="/api/tasks",
			method="GET"
		)

		return response

class User:
	def __init__(self, token):
		self.token = token

	def update_details(self, id, first_name, last_name, email, role, phone_number=None, address=None, zipcode=None, city=None):
		self.id = id
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.role = role
		self.phone_number = phone_number
		self.address = address
		self.zipcode = zipcode
		self.city = city

class Task:
	def __init__(self, id, title, description, finished, due_date):
		self.id = id
		self.title = title
		self.description = description
		self.finished = finished
		self.due_date = due_date