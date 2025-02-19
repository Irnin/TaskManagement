import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageColor

class IconButton(tk.Button):

	def __init__(self, root, iconName: str, text: str, command=None):
		super().__init__(root)

		self.active = False

		icon_path = f"assets/{iconName}"
		original_image = Image.open(icon_path)
		resized_image = original_image.resize((30, 30))
		icon = ImageTk.PhotoImage(resized_image)

		self.tkv_text = tk.StringVar()
		self.tkv_text.set(text)

		self.config(image=icon, textvariable=self.tkv_text, compound="left", pady=5, font=("Arial", 12), borderwidth=0, relief="flat", padx=5, anchor="w")
		self.image = icon

		self.configure(command=command)

	def mark_active(self):
		self.config(highlightbackground="green")

	def set_bg(self, color: str):
		self.config(highlightbackground=color)

	def reset(self):
		self.config(highlightbackground=self.cget("background"))

	def set_text(self, text: str):
		self.tkv_text.set(text)