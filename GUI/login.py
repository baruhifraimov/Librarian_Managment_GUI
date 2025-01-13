import os
import tkinter as tk
from tkinter import messagebox
import csv

from Backend.encryption import Encryption
from Backend.librarian import Librarian
from Backend.librarian_manager import LibrarianManager
from Exceptions.ExceptionBlankFieldsError import BlankFieldsError
from Exceptions.ExceptionUserNotFound import UserNotFoundError
from GUI.menu import Menu  # Import the Login class here
from ConfigFiles.log_decorator import log_activity


class Login:
    def __init__(self, root):
        self.root = root  # Store the root window
        root.geometry("500x400")
        self.root.title("Login Menu")

        # self.background_image = tk.PhotoImage(file="background.png")
        # self.background_label = tk.Label(root, image=self.background_image)
        # self.background_label.place(relwidth=1, relheight=1)

        self.frame = tk.Frame(self.root)  # Create a frame inside the root window

        headline_label = tk.Label(self.frame, text="Login", font=("Arial", 32))
        username_label = tk.Label(self.frame, text="Username:", font=("Arial", 16))
        password_label = tk.Label(self.frame, text="Password:", font=("Arial", 16))
        self.username_box = tk.Entry(self.frame, font=("Arial", 16))
        self.password_box = tk.Entry(self.frame, show="*", font=("Arial", 16))
        self.login_button = tk.Button(self.frame, text="Login", font=('Arial', 18), width=8, command=self.login)
        self.register_button = tk.Button(self.frame, text="Register", font=('Arial', 18), width=8, bg="#FF3399",
                                         command=self.switch_to_register)
        self.exit_button = tk.Button(self.frame, text="Exit", font=('Arial', 18), width=8, command=self.root.destroy)

        headline_label.grid(row=1, column=1, columnspan=1, sticky="news", pady=15)
        username_label.grid(row=2, column=0, pady=10)
        password_label.grid(row=3, column=0, pady=10)
        self.username_box.grid(row=2, column=1)
        self.password_box.grid(row=3, column=1)
        self.login_button.grid(row=4, column=1, pady=10, columnspan=2)
        self.register_button.grid(row=5, column=1, columnspan=2)
        self.exit_button.grid(row=6, column=1, columnspan=1)

        self.frame.pack()

    def login(self):
        """
        Handle user login with messagebox feedback and exception raising:
        - Username or password are empty.
        - Librarian file cannot be found.
        - Librarian cannot be found in the file.
        """
        username = self.username_box.get().lower()
        username = ''.join(username.split())  # Remove white spaces
        password = self.password_box.get()
        try:
            self.login_verifier(username, password)
        except BlankFieldsError:
            messagebox.showwarning("Input Error", "Please fill out all fields!")
        except ValueError:
            messagebox.showerror("Librarian Error", "Login Failed!\nLibrarian does not exist.")
        except FileNotFoundError:
            messagebox.showerror("File Error", "user.csv file does not exist.")
        except UserNotFoundError:
            messagebox.showerror("Librarian 404", "user is not registered in the System.")

    @log_activity("login")
    def login_verifier(self, username, password):
        if username == "" or password == "":
            raise BlankFieldsError()
        if not os.path.exists("../csv_files/librarians_users.csv"):
            raise FileNotFoundError("Librarian file does not exist.")
        try:
            password = Encryption.encrypt_password(password)
            user = LibrarianManager.search_in_user_csv(username, password)
            # Login successful
            user.activate_user()
            messagebox.showinfo("Login Successful", f"Welcome back, {username}!")
            self.frame.after(333, self.switch_to_menu)# Switch to the next screen
            return True
        except UserNotFoundError:
            raise UserNotFoundError(f"{username}")

    def switch_to_register(self):
        self.frame.destroy()  # Destroy the current login frame
        from register import Register  # Import the Register class here
        Register(self.root)  # Pass the root window to Register screen

    def switch_to_menu(self):
        logged_user = LibrarianManager.extracting_user(self.username_box.get())
        self.frame.destroy()  # Destroy the current register frame
        Menu(self.root, logged_user)  # Pass the root window to Login screen

   # def get_current_user(self):
        #return self.cur