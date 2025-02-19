import secrets
import string
import tkinter as tk
from random import random
from tkinter import messagebox

from views.modules.IconButton import IconButton
from views.modules.PageFrame import PageFrame


class UsersSubpage(tk.Frame):

	def __init__(self, parent, controller):
		super().__init__(parent)

		self.controller = controller
		self.setup_ui()

	def setup_ui(self):
		main_frame = tk.Frame(self)
		main_frame.pack(fill=tk.BOTH, expand=True)

		main_frame.columnconfigure(0, weight=1)
		main_frame.columnconfigure(1, weight=0)
		main_frame.rowconfigure(0, weight=1)

		data_frame = tk.Frame(main_frame, padx=10)
		data_frame.grid(row=0, column=0, sticky=tk.NSEW)

		action_frame = tk.Frame(main_frame)
		action_frame.grid(row=0, column=1, sticky=tk.NS)

		# Configure the table
		self.table = PageFrame(data_frame, self.controller.fetch_users, self.controller.open_task)
		self.table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		columns = [{'column_name': 'idUser', 'column_label': 'ID', 'visible': True},
		           {'column_name': 'email', 'column_label': 'Email', 'visible': True},
		           {'column_name': 'firstName', 'column_label': 'Name', 'visible': True},
		           {'column_name': 'lastName', 'column_label': 'Surname', 'visible': True},
		           {'column_name': 'role', 'column_label': 'Role', 'visible': True}]

		self.table.configure_columns(columns)
		self.table.load_data()

		# Action Buttons
		category_button = IconButton(action_frame, "tasks.png", "Create user", self.create_user)
		category_button.pack(side=tk.TOP, fill=tk.X)

		grant_admin_role = IconButton(action_frame, "tasks.png", "Grant admin role", self.grant_admin_role)
		grant_admin_role.pack(side=tk.TOP, fill=tk.X)

		grant_employee_role = IconButton(action_frame, "tasks.png", "Grant employee role", self.grant_employee_role)
		grant_employee_role.pack(side=tk.TOP, fill=tk.X)

	def generate_simple_password(self):
		characters = string.ascii_letters + string.digits
		return ''.join(secrets.choice(characters) for _ in range(12))

	def create_user(self):
		self.create_user_window = tk.Toplevel(self)
		self.create_user_window.title("Create user")

		frame = tk.Frame(self.create_user_window, pady=10, padx=10)
		frame.pack(fill=tk.BOTH, expand=True)

		frame.columnconfigure((0, 1), weight=1)
		frame.rowconfigure((0, 1, 2, 3), weight=1)

		tkv_email = tk.StringVar()
		tkv_first_name = tk.StringVar()
		tkv_last_name = tk.StringVar()
		tkv_password = tk.StringVar()
		tkv_password.set(self.generate_simple_password())

		tk.Label(frame, text="Email").grid(row=0, column=0)
		tk.Entry(frame, textvariable=tkv_email).grid(row=0, column=1)

		tk.Label(frame, text="First name").grid(row=1, column=0)
		tk.Entry(frame, textvariable=tkv_first_name).grid(row=1, column=1)

		tk.Label(frame, text="Last name").grid(row=2, column=0)
		tk.Entry(frame, textvariable=tkv_last_name).grid(row=2, column=1)

		tk.Label(frame, text="Password").grid(row=3, column=0)
		tk.Entry(frame, textvariable=tkv_password).grid(row=3, column=1)

		tk.Button(frame, text="Create", command=lambda: self.controller.create_user(tkv_email.get(), tkv_first_name.get(), tkv_last_name.get(), tkv_password.get())).grid(row=4, column=0, columnspan=2)

	def destroy_create_user_window(self):
		self.create_user_window.destroy()

	def grant_admin_role(self):
		user = self.table.get_selected_item()
		if user:
			self.controller.grant_admin_role(user['idUser'])

		else:
			messagebox.showinfo("Error", "No user selected")

	def grant_employee_role(self):
		user = self.table.get_selected_item()
		if user:
			self.controller.grant_employee_role(user['idUser'])

		else:
			messagebox.showinfo("Error", "No user selected")