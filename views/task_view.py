import tkinter as tk

from views.modules.PageFrame import PageFrame
from views.modules.Panel import Panel


class TaskView(Panel):
    def __init__(self, parent, controller):
        super().__init__(parent, "Tasks")

        self.controller = controller

        self._setup_ui()

    def _setup_ui(self):
        table = PageFrame(self)
        table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
