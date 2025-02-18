import tkinter as tk
from views.modules.Panel import Panel


class UserView(Panel):
    def __init__(self, parent, controller, is_admin: bool = False):
        super().__init__(parent, "User")

        self.controller = controller

        self._setup_ui()

    def _setup_ui(self):

        tk.Button(self, text="Test", command=self.controller.test_method).pack()