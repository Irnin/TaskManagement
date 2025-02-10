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
            "categories": IconButton(self.top_bar, "admin.png", "Admin", command=lambda: self.controller.open_page("categories"))}

        self.menu_buttons["categories"].configure(state="disabled")

        for button in self.menu_buttons.values():
            button.pack(side="left")

    def open_login_window(self):
        self.login_window = tk.Toplevel(self)
        #self.login_window.geometry("400x200")

        # Login frame
        login_frame = tk.Frame(self.login_window)

        email = tk.StringVar()
        password = tk.StringVar()

        # Quick login
        quick_login = tk.Frame(self.login_window)
        tk.Button(quick_login, text="User", command=lambda: self.handle_login("jane.smith@example.com", "Aa444444")).pack()
        tk.Button(quick_login, text="Admin", command=lambda: self.handle_login("john.doe@example.com", "Aa444444")).pack()

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

            self.logged_user_label = tk.Label(self.top_bar, text=f"{logged_user.first_name} {logged_user.last_name}", bg="gray", padx=10)
            self.logged_user_label.pack(side="right")

            if logged_user.role == "ADMIN":
                self.admin_logged()

            self.controller.open_page("tasks")

        else:
            tk.messagebox.showwarning("Error", "Can not login")

    def admin_logged(self):
        self.logged_user_label.configure(foreground="yellow")
        self.menu_buttons["categories"].configure(state="normal")

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

    def run(self):
        self.open_login_window()
        self.mainloop()