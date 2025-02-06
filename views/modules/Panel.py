import tkinter as tk
from tkinter import ttk

class Panel(tk.Frame):
	"""Creates a panel for each category"""

	def __init__(self, parent, header):
		super().__init__(parent)
		self.setup_header(header)

	def setup_header(self, header):
		tk.Label(self, text=header, font=("Helvetica", 20, "bold"), anchor='w').pack(fill='x')
		ttk.Separator(self, orient='horizontal').pack(fill='x', pady=10)