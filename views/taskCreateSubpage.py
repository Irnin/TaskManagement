import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from django.template.defaultfilters import title
from django.utils.termcolors import background

from views.modules.BetterText import BetterText
from views.modules.IconButton import IconButton

from tkcalendar import Calendar, DateEntry

from views.modules.PageFrame import PageFrame


class TaskCreateSubpage(tk.Frame):

	def __init__(self, parent, controller, is_admin: bool):
		super().__init__(parent)

		self.parent = parent
		self.is_admin = is_admin
		self.controller = controller

		# Tkinter variables
		self.tkv_title = tk.StringVar()
		self.tkv_description = tk.StringVar()

		self.tkv_category_id = tk.StringVar()
		self.tkv_category_name = tk.StringVar()

		now = datetime.now()
		self.tkv_due_date = tk.StringVar()
		self.tkv_due_date.set(now.strftime("%Y-%m-%d"))

		self.tkv_hours = tk.StringVar()
		self.tkv_hours.set(str(now.hour))
		self.tkv_minutes = tk.StringVar()
		self.tkv_minutes.set(str(now.minute))

		self.tkv_task_score = tk.StringVar()
		self.tkv_task_score.set("3")

		self.setup_ui()

	def setup_ui(self):
		# Style customization
		style = ttk.Style()
		style.configure(
			"Custom.TSpinbox",
			background='#4E4E4E',
			fieldbackground='#4E4E4E',
			foreground='white',
			font=("Arial", 14),
			arrowsize=15,
			padding=5
		)
		style.configure(
			"Custom.TLabel",
			background='#4E4E4E',
			foreground='white',
			font=("Arial", 16)
		)

		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=0)
		self.columnconfigure(2, weight=0)

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

		# Separator
		ttk.Separator(self, orient="vertical").grid(row=0, column=1, sticky="ns", padx=15)

		# Right panel
		right_panel = tk.Frame(self)
		right_panel.grid(row=0, column=2, sticky=tk.NSEW)

		# Category
		tk.Label(right_panel, text="Category:", anchor="w").pack(side=tk.TOP, fill=tk.X)
		tk.Button(right_panel, textvariable=self.tkv_category_name, command= self.select_category).pack(side=tk.TOP, fill=tk.X)

		# Task score
		tk.Label(right_panel, text="Task score:", anchor="w").pack(side=tk.TOP, fill=tk.X)
		ttk.Spinbox(right_panel, textvariable=self.tkv_task_score, from_=1, to=5, width=4, format='%02.0f', style="Custom.TSpinbox", justify='center').pack(side=tk.TOP, fill=tk.X)

		# Due date
		tk.Label(right_panel, text="Due date:", anchor="w").pack(side=tk.TOP, fill=tk.X)

		self.calendar = Calendar(right_panel, font="Arial 14", selectmode='day', date_pattern='yyyy-mm-dd')
		self.calendar.pack(side=tk.TOP)
		self.calendar.bind("<<CalendarSelected>>", lambda e: self._update_due_date())

		# Time frame setup
		time_frame = tk.Frame(right_panel, background='#4E4E4E')
		time_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

		# Configure frame layout
		time_frame.columnconfigure(0, weight=1)
		time_frame.columnconfigure(1, weight=0)
		time_frame.columnconfigure(2, weight=1)
		time_frame.rowconfigure(0, weight=1)

		# Spinbox for Hours (1 to 24)
		hour_spinbox = ttk.Spinbox(time_frame, textvariable=self.tkv_hours, from_=0, to=23, width=4, format='%02.0f', style="Custom.TSpinbox", justify='center')
		hour_spinbox.grid(row=0, column=0, pady=5, padx=5, sticky=tk.E)

		# Separator Label for time (colon)
		separator_label = ttk.Label(time_frame, text=":", style="Custom.TLabel")
		separator_label.grid(row=0, column=1, pady=5, padx=5)

		# Spinbox for Minutes (0 to 59)
		minute_spinbox = ttk.Spinbox(time_frame, textvariable=self.tkv_minutes, from_=0, to=59, width=4, format='%02.0f', style="Custom.TSpinbox", justify='center')
		minute_spinbox.grid(row=0, column=2, pady=5, padx=5, sticky=tk.W)

		# Create button
		IconButton(right_panel, "add.png", "Create task", self._create_task).pack(side=tk.BOTTOM, fill=tk.X)

	def _update_due_date(self):
		date = self.calendar.get_date()
		self.tkv_due_date.set(date)

	def select_category(self):
		self.select_category_window = tk.Toplevel(self)

		self.select_category_window.title("Select Category")

		self.table = PageFrame(self.select_category_window, self.controller.fetch_categories, self.return_selected_category)
		self.table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		columns = [{'column_name': 'idCat', 'column_label': 'ID', 'visible': False},
		           {'column_name': 'name', 'column_label': 'Name', 'visible': True},
		           {'column_name': 'description', 'column_label': 'Description', 'visible': True}]

		self.table.configure_columns(columns)
		self.table.load_data()

	def return_selected_category(self, category):
		self.select_category_window.destroy()

		self.tkv_category_id.set(category['idCat'])
		self.tkv_category_name.set(category['name'])

	def _create_task(self):
		title = self.tkv_title.get()
		description = self.tkv_description.get()
		category_id = self.tkv_category_id.get()
		task_score = int(self.tkv_task_score.get())
		due_date = self.tkv_due_date.get()
		hours = self.tkv_hours.get().zfill(2)
		minutes = self.tkv_minutes.get().zfill(2)

		full_date = f"{due_date} {hours}:{minutes}"
		full_date_dt = datetime.strptime(full_date, "%Y-%m-%d %H:%M")
		full_date += ":00"

		if full_date_dt < datetime.now():
			messagebox.showerror("Error", "Due date must be in the future!")
			return

		if not title or not description or not category_id or not task_score:
			messagebox.showerror("Error", "All fields are required!")
			return

		# Create task
		self.controller.create_task(title, description, category_id, task_score, full_date)

		self.controller.reload_data()
		self.parent.close()