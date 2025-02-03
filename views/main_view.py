import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageColor

from views.board_view import BoardView
from views.category_view import CategoryView
from views.task_view import TasksView

class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.current_view = None
        self.setup_ui()

    def icon_button(self, root, iconName: str, text: str) -> tk.Button:
        original_image = Image.open(iconName)
        resized_image = original_image.resize((30, 30))
        icon = ImageTk.PhotoImage(resized_image)

        button = tk.Button(root, image=icon, text=text, compound="left", pady=5, font=("Arial", 12), borderwidth=0, relief="flat", padx=5)
        button.image = icon

        return button

    def setup_ui(self):
        self.geometry("1000x600")
        self.title("Task Management")

        # Pasek nawigacji
        self.top_bar = tk.Frame(self, bg="gray")
        self.top_bar.pack(fill='x')

        # Przyciski do przełączania widoków
        board_button = self.icon_button(self.top_bar, "key.png", "Board")
        board_button.configure(command=self.show_board_view)
        board_button.pack(side="left")

        tasks_button = self.icon_button(self.top_bar, "key.png", "Tasks")
        tasks_button.configure(command=self.show_tasks_view)
        tasks_button.pack(side="left")

        self.category_button = self.icon_button(self.top_bar, "key.png", "Category")
        self.category_button.configure(command=lambda: self.controller.show_categories())
        self.category_button.pack(side="left")
        self.category_button.config(state="disabled")

    def login(self):
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

        # === DEBUG ===
        # Quick login
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

            # Displaying board view
            self.show_board_view()

        else:
            tk.messagebox.showwarning("Error", "Invalid credentials")

    def admin_logged(self):
        self.logged_user_label.configure(foreground="yellow")

        self.category_button.config(state="normal")

    def remove_current_view(self):
        """Usuwa obecnie wyświetlany widok."""
        if self.current_view is not None:
            self.current_view.destroy()
            self.current_view = None

    def show_board_view(self):
        """Ładuje widok tablicy."""
        self.remove_current_view()
        self.current_view = BoardView(self)
        self.current_view.pack(fill="both", expand=True)

    def show_tasks_view(self):
        """Ładuje widok zadań."""
        self.remove_current_view()
        self.current_view = TasksView(self)
        self.current_view.pack(fill="both", expand=True)

    def show_category_view(self, category_frame):
        """Ładuje widok kategorii."""
        self.remove_current_view()
        self.current_view = category_frame
        self.current_view.pack(fill="both", expand=True)

    def run(self):
        self.login()
        self.mainloop()