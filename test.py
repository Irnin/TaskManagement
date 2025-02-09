import tkinter as tk

class App:
    def __init__(self, root):
        self.root = root

        # Example pages
        self.main_page = tk.Frame(root, bg="blue")
        self.sub_page = tk.Frame(root, bg="green")

        # Load the main page initially
        self.load_main_page(self.main_page)

    def load_main_page(self, page: tk.Frame):
        """Method loads main page"""
        # Hide any current subpage if it's present
        if hasattr(self, 'sub_page') and self.sub_page.winfo_ismapped():
            self.sub_page.pack_forget()

        # Show main page
        self.main_page = page
        self._show_main_page()

    def load_subpage(self, page: tk.Frame):
        """Method loads subpage"""
        # Hide the main page if it's currently visible
        if self.main_page.winfo_ismapped():
            self.main_page.pack_forget()

        # Show subpage
        self.sub_page = page
        self.sub_page.pack(side='top', fill='both', expand=True)

    def _show_main_page(self):
        """Method shows main page"""
        self.main_page.pack(side='top', fill='both', expand=True)


# Example usage
root = tk.Tk()
app = App(root)

# Button to toggle pages
button_subpage = tk.Button(app.main_page, text="Go to Subpage", command=lambda: app.load_subpage(app.sub_page))
button_subpage.pack(pady=20)

button_main_page = tk.Button(app.sub_page, text="Back to Main Page", command=lambda: app.load_main_page(app.main_page))
button_main_page.pack(pady=20)

root.mainloop()