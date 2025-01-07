import time
import tkinter as tk
from tkinter import messagebox
import csv


class Menu:
    def __init__(self, root,user_name =""):
        self.root = root  # Store the root window
        root.geometry("800x600")

        self.background_image = tk.PhotoImage(file="background.png")
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.menu_frame = tk.Frame(self.root)  # Create a frame inside the root window
        self.book_frame = tk.Frame(self.menu_frame)
        self.root.title("Menu")
        headline_label = tk.Label(self.menu_frame, text=f"Welcome {user_name}", font=("Arial", 32))
        self.add_book_button = tk.Button(self.menu_frame, text="Add Book", font=('Arial', 18), width=8, command=self.add_book)
        self.remove_book_button = tk.Button(self.menu_frame, text="Remove Book", font=('Arial', 18), width=8, command=self.remove_book)
        self.update_book_button = tk.Button(self.menu_frame, text="Update Book", font=('Arial', 18), width=8, command=self.update_book)


        headline_label.grid(row=0, column=1,rowspan = 2,sticky="news", pady=15)

        self.add_book_button.grid(row=2, column=0, padx=5,pady=15)
        self.remove_book_button.grid(row=2, column=1, padx=5,pady=15)
        self.update_book_button.grid(row=2, column=2, padx=5,pady=15)
        self.exit_button = tk.Button(self.menu_frame, text="Exit", font=('Arial', 18), width=8, command = self.root.destroy)
        self.lgout_button = tk.Button(self.menu_frame, text="Log-Out", font=('Arial', 18), width=8, command = self.logout_button_func)

        self.lgout_button.grid(row=0, column=0)
        self.exit_button.grid(row=1, column=0)

        self.menu_frame.pack()

    def add_book(self):
        self.book_frame.destroy()
        self.book_frame = tk.Frame(self.menu_frame)
        self.text_box = tk.Button(self.book_frame, text="THIS IS ADD BOOK", font=('David', 36), width=15)
        self.book_frame.grid(row=3, column=0,columnspan=3)
        self.text_box.grid(row=3, column=1)


    def remove_book(self):
        self.book_frame.destroy()
        self.book_frame = tk.Frame(self.menu_frame)
        self.text_box = tk.Button(self.book_frame, text="THIS IS REMOVE BOOK", font=('David', 36), width=15)
        self.book_frame.grid(row=3, column=0,columnspan=3)
        self.text_box.grid(row=3, column=1)

    def update_book(self):
        self.book_frame.destroy()
        self.book_frame = tk.Frame(self.menu_frame)
        self.text_box = tk.Button(self.book_frame, text="THIS IS UPDATE BOOK", font=('David', 36), width=15)
        self.book_frame.grid(row=3, column=0,columnspan=3)
        self.text_box.grid(row=3, column=1)

    def logout_button_func(self):
        self.menu_frame.destroy()  # Destroy the current register frame
        from Login import Login  # Import the Login class here
        Login(self.root)  # Pass the root window to Login screen