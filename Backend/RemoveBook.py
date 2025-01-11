from Exceptions.ExceptionBlankFieldsError import BlankFieldsError
from Exceptions.ExceptionWatchedBookRemovalError import WatchedBookRemovalError
import tkinter as tk
from tkinter import messagebox
from Backend.BookManager import BookManager


class RemoveBook:

    @classmethod
    def book_remover(self, title, author, genre, year, book_frame):
        try:
            if BookManager.remove_book(title, author, genre, year):
                rmv_scss = tk.Label(book_frame, text="Removed Succesfuly!", font=("Arial", 16), fg="green")
                rmv_scss.grid(row=10, column=1, columnspan=2, pady=10)  # Positioned at row 5, under everything
                rmv_scss.after(2000, rmv_scss.destroy)
            else:
                rmv_fail = tk.Label(book_frame, text="Removed Failed! Book does not exists.",
                                    font=("Arial", 16),
                                    fg="red")
                rmv_fail.grid(row=10, column=1, columnspan=2, pady=10)
                rmv_fail.after(2000, rmv_fail.destroy)
        except BlankFieldsError:
            tk.messagebox.showinfo(
                "Fields Are Blank",
                "At least one of the fields are blank!"
            )
        except WatchedBookRemovalError:
            tk.messagebox.showinfo(
                "Watched Book Removal Error",
                "The selected book is currently being watched and cannot be removed."
            )
