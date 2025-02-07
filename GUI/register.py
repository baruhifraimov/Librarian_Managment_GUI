import os
import tkinter as tk
from tkinter import messagebox
import csv

from Backend.encryption import Encryption
from Backend.librarian_factory import LibrarianFactory
from Backend.librarian_manager import LibrarianManager
from LogConfigurator.log_decorator import log_activity
from Exceptions.ExceptionBlankFieldsError import BlankFieldsError
from Exceptions.ExceptionUserAlreadyInList import UserAlreadyInListError
from Backend.librarian import Librarian

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

    @staticmethod
    def search_user_in_csv(username):
        """
        Search for a user in the csv file. Return True if the user exists, False otherwise.
        :param username:  The username to search for in the csv file
        :return: True if the user exists, False otherwise
        """
        if os.path.exists("../csv_files/librarians_users.csv"): # check if the file exists
            with open('../csv_files/librarians_users.csv', 'r') as file:
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


        try:
            self.register_verifier(username, password)
        except BlankFieldsError as error:
            if str(error) == "Invalid Username: Username is blank.":
                messagebox.showerror("Invalid Username", "Please enter your username again.")
            else:
                messagebox.showerror("Invalid Password", "Please enter your password again.")
        except UserAlreadyInListError as error:
            messagebox.showerror("Register Failed", "Username already exists!")
        except FileNotFoundError:
            messagebox.showerror("File Error", "librarians.csv file does not exist.")
        except Exception as e:
            messagebox.showerror("Register Error", f"Failed to register user: {e}")

    @log_activity("register")
    def register_verifier(self,username,password):
        """
        Verify the user registration credentials. If the username or password is empty, raise a BlankFieldsError.
        If the user is already in the csv file, raise a UserAlreadyInListError.
        If the registration is successful, add the user to the csv file and show a success message.
        :param username: str
        :param password: str
        """
        # Check if username is blank
        if username == "":
            raise BlankFieldsError("Invalid Username: Username is blank.")

        # Check if password is blank
        if password == "":
            raise BlankFieldsError("Invalid Password: Password is blank.")

        # Encrypt the password
        encrypted_password = Encryption.encrypt_password(password)
        # Check if the user already exists in the csv file
        if self.search_user_in_csv(username):
            raise UserAlreadyInListError(f"Register Failed: Username '{username}' already exists.")

        #create a user object using user factory.

        user = LibrarianFactory.create_librarian(username, encrypted_password)

        # Add user info to csv and show success message
        try:
            LibrarianManager.add_user_csv(user)
            messagebox.showinfo("Register Success", "Registered successfully!")
            self.switch_to_login()  # Switch to Login screen
        except FileNotFoundError:
            raise FileNotFoundError
        except Exception as e:
             raise e


    def switch_to_login(self):
        self.frame.destroy()  # Destroy the current register frame
        from login import Login  # Import the Login class here
        Login(self.root)  # Pass the root window to Login screen