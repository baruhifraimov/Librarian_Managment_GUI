import os
import tkinter as tk
from tkinter import messagebox
import csv

from Backend.Encryption import Encryption
from ConfigFiles.LogDecorator import log_activity
from Exceptions.ExceptionBlankFieldsError import BlankFieldsError
from Exceptions.ExceptionUserAlreadyInList import UserAlreadyInListError


class Register:
    def __init__(self, root):
        self.root = root  # Store the root window
        root.geometry("500x400")
        self.root.title("Register Menu")


        self.frame = tk.Frame(self.root)  # Create a frame inside the root window
        headline_label = tk.Label(self.frame, text="Register", font=("Arial", 32))
        username_label = tk.Label(self.frame, text="Username:", font=("Arial", 16))
        password_label = tk.Label(self.frame, text="Password:", font=("Arial", 16))
        self.username_box = tk.Entry(self.frame, font=("Arial", 16))
        self.password_box = tk.Entry(self.frame, show="*", font=("Arial", 16))
        self.register_button = tk.Button(self.frame, text="REGISTER", font=('Arial', 18), width=8, bg="#FF3399", command=self.register_user)
        self.back_button = tk.Button(self.frame, text="Back", font=('Arial', 16), width=4, command=self.switch_to_login)

        headline_label.grid(row=0, column=1, columnspan=1, sticky="news", pady=15)
        username_label.grid(row=1, column=0, pady=10)
        password_label.grid(row=2, column=0, pady=10)
        self.username_box.grid(row=1, column=1)
        self.password_box.grid(row=2, column=1)
        self.register_button.grid(row=3, column=1, columnspan=1)
        self.back_button.grid(row=4, column=0)

        self.frame.pack()

    def search_user_in_csv(self, username,password):
        if os.path.exists("../ConfigFiles/users.csv"): # check if the file exists
            with open('../ConfigFiles/users.csv', 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if row[0] == username:
                        return True
                return False
        return False

    def register_user(self):
        """
        Handle user registration with messagebox feedback and exception raising:
        - Username or password is blank.
        - Username already exists.
        """
        # Get the username and password
        username = self.username_box.get().lower()
        username = ''.join(username.split())  # Remove white spaces
        password = self.password_box.get()

        # Encrypt the password
        encrypted_password = Encryption.encrypt_password(password)

        try:
            self.register_verifier(username, password,encrypted_password)
        except BlankFieldsError as error:
            if str(error) == "Invalid Username: Username is blank.":
                messagebox.showerror("Invalid Username", "Please enter your username again.")
            else:
                messagebox.showerror("Invalid Password", "Please enter your password again.")
        except UserAlreadyInListError as error:
            messagebox.showerror("Register Failed", "Username already exists!")

    @log_activity("register")
    def register_verifier(self,username,password,encrypted_password):
        # Check if username is blank
        if username == "":
            raise BlankFieldsError("Invalid Username: Username is blank.")

        # Check if password is blank
        if password == "":
            raise BlankFieldsError("Invalid Password: Password is blank.")

        # Check if the user already exists
        if self.search_user_in_csv(username, encrypted_password):
            raise UserAlreadyInListError(f"Register Failed: Username '{username}' already exists.")

        # Save user info and show success message
        self.export_to_file(username, encrypted_password)
        messagebox.showinfo("Register Success", "Registered successfully!")
        self.switch_to_login()  # Switch to Login screen

    def export_to_file(self, username, password):
        """
        Append the username and password to the users.csv file.
        Create the file and add headers if it does not exist or is empty.
        :param username: The username to save
        :param password: The password to save
        """
        try:
            file_path = "../ConfigFiles/users.csv"

            # Ensure the parent directory exists
            if not os.path.exists(os.path.dirname(file_path)):
                raise FileNotFoundError(f"The directory for the file '{file_path}' does not exist.")

            # Open the file in append mode
            with open(file_path, 'a+', newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                # Write headers if the file is empty
                if os.stat(file_path).st_size == 0:  # Check if the file is empty
                    writer.writerow(["Username", "Password"])

                # Write the new user's data
                writer.writerow([username, password])

        except Exception as e:
            # Raise a runtime error for unexpected issues
            raise RuntimeError(f"Failed to export user data to file: {e}")

    def switch_to_login(self):
        self.frame.destroy()  # Destroy the current register frame
        from Login import Login  # Import the Login class here
        Login(self.root)  # Pass the root window to Login screen