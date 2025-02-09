from views.TaskSubpage import TaskSubpage
import tkinter as tk

class TaskController:

	def __init__(self, root: tk.Frame, master_controller):
		#self.model = TaskModel()
		self.view = TaskSubpage(root, self)

		self.master_controller = master_controller