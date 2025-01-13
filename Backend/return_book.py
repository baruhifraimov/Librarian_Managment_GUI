from Exceptions.ExceptionBookNotFound404 import BookNotFound404Error
from Exceptions.ExceptionReturnLimitExceeded import ReturnLimitExceededError
import tkinter as tk
from tkinter import messagebox
from Backend.book_manager import BookManager
from Backend.tree_view_loader import TreeViewLoader


class ReturnBook:
    @classmethod
    def book_returner(self, selected_item,treeview):
        if selected_item:
            selected_values = selected_item['values']
            selected_title = str(selected_values[0])
            selected_author = str(selected_values[1])
            selected_year = str(selected_values[2])
            selected_genre = str(selected_values[3])
            # selected_copies = int(selected_values[4])  # Convert copies to int if necessary
            try:
                book = BookManager.extracting_book(selected_title, selected_author, selected_genre, selected_year)
                try:
                    book.return_action()  # Return the book and sub -1 to book lent counter
                    # now , when someone returns a book , i would like to check if the book has a waiting list so:
                    BookManager.update_in_csv(book, 1)
                    tk.messagebox.showinfo(
                        "Success",
                        f"Book '{selected_title}' has been returned!"
                    )
                    TreeViewLoader.refresh_treeview(treeview,2)



                except ReturnLimitExceededError:
                    tk.messagebox.showinfo(
                        "Failed",
                        f"Selected book: '{selected_title}' cannot be returned!\n"
                    )
            except BookNotFound404Error:
                tk.messagebox.showinfo(
                    "Failed",
                    f"Selected book: '{selected_title}'  not found in the book list!"
                )
        else:
            tk.messagebox.showinfo(
                "Failed",
                "No book Selected!"
            )