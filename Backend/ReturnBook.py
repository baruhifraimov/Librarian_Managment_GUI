from Exceptions.ExceptionReturnLimitExceeded import ReturnLimitExceeded
import tkinter as tk
from tkinter import messagebox
from Backend.BookManager import BookManager
from Backend.TreeViewLoader import TreeViewLoader


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

            book = BookManager.search_book(selected_title, selected_author, selected_genre, selected_year)
            if book:
                try:
                    book.return_action()  # Return the book and sub -1 to book lent counter
                    BookManager.update_in_csv(book, 1)
                    tk.messagebox.showinfo(
                        "Success",
                        f"Book '{selected_title}' has been returned!"
                    )
                    TreeViewLoader.refresh_treeview(treeview,2)
                except ReturnLimitExceeded:
                    tk.messagebox.showinfo(
                        "Failed",
                        f"Selected book: '{selected_title}' cannot be returned!\n"
                    )
            else:
                tk.messagebox.showinfo(
                    "Failed",
                    f"Selected book: '{selected_title}'  not found in the book list!"
                )
        else:
            tk.messagebox.showinfo(
                "Failed",
                "No book Selected!"
            )