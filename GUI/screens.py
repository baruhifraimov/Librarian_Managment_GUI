import logging
import tkinter as tk

from Backend.librarian_manager import LibrarianManager
from GUI.register import Register  # Import Register screen


def show_register_screen(root):
    Register(root)  # Pass the root window to Register screen

def show_login_screen(root):
    from login import Login  # Import Login screen
    return Login(root)# Pass the root window to Login screen


def main():
    root = tk.Tk()  # Create the Tkinter root window
    root.geometry("500x400")
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
    LibrarianManager.load_users()
    show_login_screen(root)  # Initially show the Login screen
    root.mainloop()  # Start the Tkinter main loop

def on_close(root):
    print("Application is closing.")
    user = LibrarianManager.extracting_online_user()
    user.deactivate_user()
    LibrarianManager.set_user_status_csv(user.get_username(), 1)
    root.destroy()

if __name__ == "__main__":
    main()