import tkinter as tk
from tkinter import ttk, messagebox

from views.modules.IconButton import IconButton
from views.modules.Panel import Panel

class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.top_bar = None
        self.menu_buttons = None
        self.current_view = None

        self.setup_ui()

    def setup_ui(self):
        self.geometry("1000x600")
        self.minsize(800, 400)
        self.title("Task Management")

        style = ttk.Style()
        style.theme_use("clam")

        self.top_bar = tk.Frame(self, bg="#808080")
        self.top_bar.pack(fill='x')

        self.menu_buttons: dict[str, IconButton] = {
            "board": IconButton(self.top_bar, "board.png", "Board", command=lambda: self.controller.open_page("board")),
            "tasks": IconButton(self.top_bar, "tasks.png", "Tasks", command=lambda: self.controller.open_page("tasks")),
            "account": IconButton(self.top_bar, "account.png", "", command=lambda: self.controller.open_page("account")),
            "admin": IconButton(self.top_bar, "admin.png", "Admin", command=lambda: self.controller.open_page("admin"))}

        for key, button in self.menu_buttons.items():

            if key == "admin":
                continue

            if key == "account":
                button.pack(side='right')
            else:
                button.pack(side="left")

        menu = tk.Menu(self)
        self.config(menu=menu)

        task_menu = tk.Menu(menu)
        menu.add_cascade(label="Tasks", menu=task_menu)
        task_menu.add_command(label="My tasks", command=lambda: self.controller.open_page("board"))
        task_menu.add_command(label="Open task", command=self.open_task)

    def open_login_window(self):
        self.login_window = tk.Toplevel(self)
        self.login_window.geometry("450x150")

        # Login frame
        login_frame = tk.Frame(self.login_window)

        email = tk.StringVar()
        password = tk.StringVar()

        # Quick login
        quick_login = tk.Frame(self.login_window)
        tk.Button(quick_login, text="User", command=lambda: self.handle_login("jane.smith@example.com", "Aa444444"), pady=5).pack()
        tk.Button(quick_login, text="Admin", command=lambda: self.handle_login("john.doe@example.com", "Aa444444"), pady=5).pack()

        quick_login.place(x=10, y=10)

        # Common login
        login_frame.columnconfigure((0, 1), weight=1)
        login_frame.rowconfigure((0, 1, 2), weight=1)

        tk.Label(login_frame, text="Login:").grid(column=0, row=0, columnspan=2)
        tk.Label(login_frame, text="Email").grid(column=0, row=1)
        tk.Label(login_frame, text="Password").grid(column=0, row=2)

        email_entry = ttk.Entry(login_frame, textvariable=email)
        email_entry.grid(column=1, row=1)

        password_entry = ttk.Entry(login_frame, textvariable=password, show="*")
        password_entry.grid(column=1, row=2)

        login_button = ttk.Button(login_frame, text="Login", command=lambda: self.handle_login(email.get(), password.get()))
        login_button.grid(column=1, row=3, stick='nsew')

        login_frame.pack(padx=10, pady=10)

        # # === DEBUG ===
        # # Quick login
        self.handle_login("john.doe@example.com", "Aa444444")

    def handle_login(self, email, password):
        if self.controller.login(email, password):
            self.login_window.destroy()

            # Displaying logged user
            logged_user = self.controller.get_user()

            self.menu_buttons['account'].set_text(f"{logged_user.first_name} {logged_user.last_name}")

            if logged_user.role == "ADMIN":
                self.admin_logged()

            self.controller.open_page("board")

        else:
            tk.messagebox.showwarning("Error", "Can not login")

    def admin_logged(self):
        self.menu_buttons["account"].set_bg("yellow")
        self.menu_buttons["admin"].pack(side="left")

    def remove_current_page(self):
        """
        Reset all buttons and remove current view
        """

        for button in self.menu_buttons.values():
            button.reset()

        if self.current_view is not None:
            self.current_view.destroy()
            self.current_view = None

    def open_page(self, page: Panel, header: str):
        """
        Open page in main view and mark tab as active
        """

        self.menu_buttons[header].mark_active()

        self.current_view = page
        self.current_view.pack(fill="both", expand=True, padx=10, pady=10)

    def open_task(self):
        top_window = tk.Toplevel(self)
        top_window.title("Task")

        tk.Label(top_window, text="Provide task ID").pack()
        task_id = tk.StringVar()
        tk.Entry(top_window, textvariable=task_id).pack()
        tk.Button(top_window, text="Open task", command=lambda: self.controller.open_task(task_id.get())).pack()

    def run(self):
        self.open_login_window()
        self.mainloop()