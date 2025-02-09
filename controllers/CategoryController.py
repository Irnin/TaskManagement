from models.CategoryCodel import CategoryModel
from views.CategoryView import CategoryView

class CategoryController:
	def __init__(self, controller):
		self.masterController = controller
		self.masterModel = controller.model
		self.masterView = controller.view

		self.view = CategoryView(self.masterView, self)
		self.model = CategoryModel(self.masterModel)

		self.model.fetch_data()
		categories = self.model.get_categories()

		self.view.insert_categories(categories)

	def update_category(self, id, name, description):
		self.model.update_category(id, name, description)
		self.model.fetch_data()

		categories = self.model.get_categories()
		self.view.insert_categories(categories)


