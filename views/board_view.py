import tkinter as tk

from views.modules.Panel import Panel

class BoardView(Panel):
    def __init__(self, parent, controller):
        super().__init__(parent, "Board")
        self.controller = controller