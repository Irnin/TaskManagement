from models.BoardModel import BoardModel
from views.BoardView import BoardView

class BoardController:
	def __init__(self, controller):
		self.masterController = controller
		self.masterModel = controller.model
		self.masterView = controller.view

		self.view = BoardView(self.masterView, self)
		self.model = BoardModel(self.masterModel)