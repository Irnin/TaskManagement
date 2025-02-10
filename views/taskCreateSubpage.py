import tkinter as tk
from tkinter import messagebox, ttk

from views.modules.BetterText import BetterText
from views.modules.IconButton import IconButton

from tkcalendar import Calendar, DateEntry

class TaskCreateSubpage(tk.Frame):

	def __init__(self, parent, controller, is_admin: bool):
		super().__init__(parent)

		self.is_admin = is_admin
		self.controller = controller

		# Tkinter variables
		self.tkv_title = tk.StringVar()
		self.tkv_description = tk.StringVar()

		self.tkv_category_id = tk.StringVar()
		self.tkv_category_name = tk.StringVar()

		self.setup_ui()

	def setup_ui(self):
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)

		self.rowconfigure(0, weight=1)

		# Left panel
		left_panel = tk.Frame(self)
		left_panel.grid(row=0, column=0, sticky=tk.NSEW)

		# Title
		tk.Label(left_panel, text="Title:", anchor="w").pack(side=tk.TOP, fill=tk.X)
		tk.Entry(left_panel, textvariable=self.tkv_title).pack(side=tk.TOP, fill=tk.X)

		# Description
		tk.Label(left_panel, text="Description:", anchor="w").pack(side=tk.TOP, fill=tk.X)
		BetterText(left_panel, textvariable=self.tkv_description).pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		# Right panel
		right_panel = tk.Frame(self)
		right_panel.grid(row=0, column=1, sticky=tk.NSEW)

		# Category
		tk.Label(right_panel, text="Category:", anchor="w").pack(side=tk.TOP, fill=tk.X)
		tk.Button(right_panel, textvariable=self.tkv_category_name, command=lambda: self.controller.select_category(self.tkv_category_id, self.tkv_category_name)).pack(side=tk.TOP, fill=tk.X)

		# Due date
		tk.Label(right_panel, text="Due date:", anchor="w").pack(side=tk.TOP, fill=tk.X)

		calendar = Calendar(right_panel, font="Arial 14", selectmode='day', style='style.clam', bg="darkblue", fg="white")
		calendar.pack(side=tk.TOP)
