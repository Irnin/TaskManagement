from models.category_model import CategoryModel
from views.category_view import CategoryView


class CategoryController:
	def __init__(self, controller):
		self.masterController = controller
		self.masterModel = controller.model
		self.masterView = controller.view

		self.view = CategoryView(self.masterView)
		self.model = CategoryModel(self.masterModel)

		self.model.fetch_data()
		categories = self.model.get_categories()

		self.view.insert_categories(categories)



