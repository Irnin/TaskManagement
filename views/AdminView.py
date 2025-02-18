import tkinter as tk
from tkinter import ttk

from views.modules.BetterText import BetterText
from views.modules.PageFrame import PageFrame
from views.modules.PaginatedTableFrame import PaginatedTableFrame
from views.modules.Panel import Panel


class AdminView(Panel):
    def __init__(self, parent, controller):
        super().__init__(parent, "Admin panel")

        self.controller = controller

        self._setup_ui()

    def _setup_ui(self):
        pass
