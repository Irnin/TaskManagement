import tkinter as tk

class TaskSubpage(tk.Frame):

	def __init__(self, parent, controller):
		super().__init__(parent)

		self.controller = controller
		self.setup_ui()

	def setup_ui(self):
		tk.Label(self, text="Task Subpage").pack()