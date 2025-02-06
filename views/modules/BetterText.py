import tkinter as tk

class BetterText(tk.Frame):
	"""A multi-line text input with a scrollbar and binding to StringVar."""

	def __init__(self, parent, textvariable: tk.StringVar):
		super().__init__(parent)
		self.textvariable = textvariable

		self._setup_ui()
		self._setup_events()

	def _setup_ui(self):
		"""Creates a multi-line text input with a scrollbar and binding to StringVar."""

		self.text_widget = tk.Text(self, height=5, wrap='word', width=30, font=("Helvetica", 12))
		self.text_widget.pack(side='left', fill='both', expand=True)

		scrollbar = tk.Scrollbar(self, command=self.text_widget.yview)
		scrollbar.pack(side='right', fill='y')
		self.text_widget.config(yscrollcommand=scrollbar.set)

		self.text_widget.insert('1.0', self.textvariable.get())

	def _setup_events(self):
		self.text_widget.bind('<KeyRelease>', self._update_text_var)
		self.textvariable.trace_add('write', self._update_text_widget)

	def _update_text_var(self, event=None):
		self.textvariable.set(self.text_widget.get('1.0', 'end-1c'))

	def _update_text_widget(self, *args):
		self.text_widget.delete('1.0', tk.END)
		self.text_widget.insert(tk.END, self.textvariable.get())

	def get(self):
		return self.textvariable.get()

	def set(self, value):
		self.text_widget.delete('1.0', tk.END)
		self.text_widget.insert(tk.END, value)
