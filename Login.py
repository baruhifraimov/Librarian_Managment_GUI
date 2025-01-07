import os
import tkinter as tk
from tkinter import messagebox
import csv

from Encryption import Encryption
from Menu import Menu  # Import the Login class here


class Login:
    def __init__(self, root):
        self.root = root  # Store the root window
        root.geometry("500x400")
        self.root.title("Login Menu")


        self.background_image = tk.PhotoImage(file="background.png")
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.frame = tk.Frame(self.root,bg="")  # Create a frame inside the root window

        headline_label = tk.Label(self.frame, text="Login", font=("Arial", 32))
        username_label = tk.Label(self.frame, text="Username:", font=("Arial", 16))
        password_label = tk.Label(self.frame, text="Password:", font=("Arial", 16))
        self.username_box = tk.Entry(self.frame, font=("Arial", 16))
        self.password_box = tk.Entry(self.frame, show="*", font=("Arial", 16))
        self.login_button = tk.Button(self.frame, text="LOGIN", font=('Arial', 18), width=8, command=self.login)
        self.register_button = tk.Button(self.frame, text="REGISTER", font=('Arial', 18), width=8, bg="#FF3399", command=self.switch_to_register)
        self.exit_button = tk.Button(self.frame, text="Exit", font=('Arial', 18), width=8,command = self.root.destroy)

        headline_label.grid(row=0, column=1, columnspan=1, sticky="news", pady=15)
        username_label.grid(row=1, column=0, pady=10)
        password_label.grid(row=2, column=0, pady=10)
        self.username_box.grid(row=1, column=1)
        self.password_box.grid(row=2, column=1)
        self.login_button.grid(row=3, column=1, pady=10, columnspan=2)
        self.register_button.grid(row=4, column=1, columnspan=2)
        self.exit_button.grid(row=6, column=1, columnspan=1)

        self.frame.pack()

    def search_in_csv(self, username, password):
        password = Encryption.encrypt_password(password)
        with open('users.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                if row[0] == username and row[1] == password:
                    return True
            return False

    def login(self):
        username = self.username_box.get()
        password = self.password_box.get()
        if username == "" or password == "":
            messagebox.showerror("Error", "Username or Password is empty")
            return
        if os.path.exists("users.csv"): # check if the file exists
            if self.search_in_csv(username,password):
                self.login_msg = tk.Label(self.frame, text="Login Successful!", font=("Arial", 16), fg="green")
                self.login_msg.grid(row=5, column=1, columnspan=2, pady=10)  # Positioned at row 5, under everything
                self.frame.after(1000, self.remove_label_and_switch) # Use after() to remove the label after a delay (e.g., 1000 ms = 1 second)
            else:
                self.login_msg = tk.Label(self.frame, text="Login Failed! User does not exists.", font=("Arial", 16), fg="red")
                self.login_msg.grid(row=5, column=1, columnspan=2, pady=10)
                self.login_msg.after(2000,self.login_msg.destroy)
        else:
            messagebox.showinfo("ERROR", "USER FILE DOES NOT EXIST")

    def remove_label_and_switch(self):
        # Destroy the label
        self.login_msg.destroy()

        # Call switch_to_menu function
        self.switch_to_menu()

    def switch_to_register(self):
        self.frame.destroy()  # Destroy the current login frame
        from Register import Register  # Import the Register class here
        Register(self.root)  # Pass the root window to Register screen

    def switch_to_menu(self):
        logged_user = str(self.username_box.get())
        self.frame.destroy()# Destroy the current register frame
        Menu(self.root,logged_user)  # Pass the root window to Login screen