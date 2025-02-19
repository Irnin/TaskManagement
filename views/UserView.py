import tkinter as tk

from views.modules.IconButton import IconButton
from views.modules.Panel import Panel

class UserView(Panel):
    def __init__(self, parent, controller, is_admin: bool = False):
        super().__init__(parent, "User")

        self.controller = controller

        self._setup_ui()

    def _setup_ui(self):

        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)

        update_password_button = IconButton(frame, "add.png", "Change password", self._update_password)
        update_password_button.grid(row=0, column=1, sticky=tk.N)

    def _update_password(self):

        self.update_password_window = tk.Toplevel(self)
        self.update_password_window.title("Change password")

        frame = tk.Frame(self.update_password_window, pady=10, padx=10)
        frame.pack(fill=tk.BOTH, expand=True)

        frame.rowconfigure((0, 1, 2, 3), weight=1)
        frame.columnconfigure((0, 1), weight=1)

        tkv_current_password = tk.StringVar()
        tkv_new_password = tk.StringVar()
        tkv_confirm_password = tk.StringVar()

        tk.Label(frame, text="Current password").grid(row=0, column=0, sticky=tk.W)
        tk.Entry(frame, textvariable=tkv_current_password, show="*").grid(row=0, column=1, sticky=tk.EW)

        tk.Label(frame, text="New password").grid(row=1, column=0, sticky=tk.W)
        tk.Entry(frame, textvariable=tkv_new_password, show="*").grid(row=1, column=1, sticky=tk.EW)

        tk.Label(frame, text="Confirm password").grid(row=2, column=0, sticky=tk.W)
        tk.Entry(frame, textvariable=tkv_confirm_password, show="*").grid(row=2, column=1, sticky=tk.EW)

        tk.Button(frame, text="Change password", command=lambda: self.controller.change_password(tkv_current_password.get(), tkv_new_password.get(), tkv_confirm_password.get())).grid(row=3, column=0, columnspan=2, sticky=tk.EW)

    def close_update_password_window(self):
        self.update_password_window.destroy()