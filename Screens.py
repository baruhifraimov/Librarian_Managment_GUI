import tkinter as tk
from Register import Register  # Import Register screen
from Login import Login  # Import Login screen


def show_register_screen(root):
    Register(root)  # Pass the root window to Register screen


def show_login_screen(root):
    Login(root)  # Pass the root window to Login screen


if __name__ == "__main__":
    root = tk.Tk()  # Create the Tkinter root window
    root.geometry("500x400")
    show_login_screen(root)  # Initially show the Login screen
    root.mainloop()  # Start the Tkinter main loop
    logging.debug("CLOSING APP")

