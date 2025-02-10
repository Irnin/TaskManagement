from models.CategoryModel import CategoryModel
from views.CategoryView import CategoryView

class CategoryController:
	def __init__(self, controller):
		self.masterController = controller
		self.masterModel = controller.model
		self.masterView = controller.view

		self.view = CategoryView(self.masterView, self)
		self.model = CategoryModel(self.masterModel)

	def fetch_categories(self, page: int = 0, page_size: int = 25):
		return self.model.get_categories(page=page, page_size=page_size)

	def update_category(self, id, name, description):
		self.model.update_category(id, name, description)
		self.model.get_categories()

		categories = self.model.get_categories()
		self.view.insert_categories(categories)

	def select_category(self, category):

		self.place_for_category = category
		self.view.select_category()

	def selected_category(self, category):
		self.place_for_category = category
		self.view.return_selected_category(category)



