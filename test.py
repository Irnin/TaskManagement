import tkinter as tk
from tkinter import messagebox

def handle_menu_action(action):
    messagebox.showinfo("Action Triggered", f"You clicked {action}")

root = tk.Tk()
root.title("Menu Action Button")
root.geometry("300x200")

# Create a button with a dropdown menu
menu_button = tk.Menubutton(root, text="Options", relief=tk.RAISED)
menu = tk.Menu(menu_button, tearoff=0)
menu_button.configure(menu=menu)

# Add menu items
menu.add_command(label="Edit", command=lambda: handle_menu_action("Edit"))
menu.add_command(label="Delete", command=lambda: handle_menu_action("Delete"))
menu.add_command(label="View Details", command=lambda: handle_menu_action("View Details"))

# Position the button
menu_button.pack(pady=50)

root.mainloop()