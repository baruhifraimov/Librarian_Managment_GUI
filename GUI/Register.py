import os
import tkinter as tk
from tkinter import messagebox
import csv

from Backend.Encryption import Encryption


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
        username = self.username_box.get().lower()
        username = ''.join(username.split()) #no white spaces
        password = self.password_box.get()
        password = Encryption.encrypt_password(password)
        # if the username is blank
        if username == "":
            messagebox.showinfo("Invalid Username", "Please enter your username again")
        # if the password is blank
        elif password == "":
            messagebox.showinfo("Invalid Password", "Please enter your password again")
        # checking if user exists
        elif self.search_user_in_csv(username,password):
            messagebox.showinfo("Register Failed", "Username already exists!")
        # saving user info
        else:
            self.export_to_file(username, password)
            messagebox.showinfo("Register Success", "Registered successfully!")
            self.switch_to_login()  # Switch to Login screen

    def export_to_file(self,username,password):
        if os.path.exists("../ConfigFiles/users.csv"): # check if the file exists
            # with open("users.csv","r") as file:  # Open in read mode
            #     first_line = file.readline().strip()  # Read the first row
            #     lines = file.readlines()  # Read all lines into a list

            with open("../ConfigFiles/users.csv", 'a+', newline="") as file:
                writer = csv.writer(file)
                if os.stat("../ConfigFiles/users.csv").st_size == 0:  # check if the file is empty
                    writer.writerow(["Username", "Password"])
                writer.writerow([username, password])
        else:
            with open('../ConfigFiles/users.csv', 'w', newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Username", "Password"])
                    writer.writerow([username, password])

    def switch_to_login(self):
        self.frame.destroy()  # Destroy the current register frame
        from Login import Login  # Import the Login class here
        Login(self.root)  # Pass the root window to Login screen