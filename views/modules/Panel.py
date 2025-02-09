import tkinter as tk
from tkinter import ttk

from views.modules.IconButton import IconButton


class Panel(tk.Frame):
	"""Creates a panel for each category"""

	def __init__(self, parent, header):
		super().__init__(parent)

		self.main_page: tk.Frame

		# Tkinter variables
		self.tkv_header = tk.StringVar()
		self.tkv_header.set(header)
		self._setup_panel_ui()

	def _setup_panel_ui(self):
		self.top_bar = tk.Frame(self)
		self.top_bar.pack(side='top', fill='x')

		tk.Label(self.top_bar, textvariable=self.tkv_header, font=("Helvetica", 20, "bold"), anchor='w').pack(side='left', fill='x')

		ttk.Separator(self, orient='horizontal').pack(fill='x', pady=10)

	def update_header(self, header):
		"""Method updates header"""
		self.tkv_header.set(header)

	def load_main_page(self, page: tk.Frame):
		"""Method loads main page"""
		self.main_page = page
		self._show_main_page()

	def load_subpage(self, page: tk.Frame):
		"""Method loads subpage"""
		self.main_page.pack_forget()

		self.sub_page = page
		self.sub_page.pack(side='top', fill='both', expand=True)

		self.close_button = IconButton(self.top_bar, "close.png", "Close", command=self.close)
		self.close_button.pack(side='right')

	def _show_main_page(self):
		"""Method shows main page"""
		self.main_page.pack(side='top', fill='both', expand=True)

	def close(self):
		self.sub_page.pack_forget()

		if hasattr(self, 'close_button'):
			self.close_button.destroy()

		self._show_main_page()