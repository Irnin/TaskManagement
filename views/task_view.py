import tkinter as tk

from views.modules.Panel import Panel


class TaskView(Panel):
    def __init__(self, parent, controller):
        super().__init__(parent, "Tasks")

        self.controller = controller
