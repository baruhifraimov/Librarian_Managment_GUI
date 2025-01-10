import tkinter as tk
from tkinter import messagebox, ttk
from Backend.BookManager import BookManager


class AddBook:
    @classmethod
    def book_adder(self, title, author, genre, year, copies, book_frame):
        if BookManager.add_book(title, author, genre, year, copies):
            add_scss = tk.Label(book_frame, text="Book added successfully!", font=("Arial", 16), fg="green")
            add_scss.grid(row=11, column=1, columnspan=2, pady=10)  # Positioned at row 5, under everything
            add_scss.after(2000, add_scss.destroy)

        else:
            add_fail = tk.Label(book_frame,
                                text="Book addition failed.\nOne or more fields are blank.\nPlease fill them in "
                                     "and try again!",
                                font=("Arial", 16),
                                fg="red")
            add_fail.grid(row=11, column=1, columnspan=2, pady=10)
            add_fail.after(2000, add_fail.destroy)
