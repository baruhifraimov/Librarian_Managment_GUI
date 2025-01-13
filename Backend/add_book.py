import tkinter as tk
from Backend.book_manager import BookManager
from ConfigFiles.log_decorator import log_activity
from Exceptions.ExceptionBlankFieldsError import BlankFieldsError


class AddBook:
    """
    Add Book widget function, allows you to use the button as a function and not just for beauty
    """
    @classmethod
    def book_adder(self, title, author, genre, year, copies, book_frame):
        """
        Add a book to the library. If one or more fields are blank, raise a BlankFieldsError.
        :param title:  The title of the book.
        :param author:  The author of the book.
        :param genre:  The genre of the book.
        :param year:  The year of the book.
        :param copies:  The number of copies of the book.
        :param book_frame:  The frame to display the success/failure message in.
        :return:  None
        """
        try:
            BookManager.add_book(title, author, genre, year, copies)
            add_scss = tk.Label(book_frame, text="Book added successfully!", font=("Arial", 16), fg="green")
            add_scss.grid(row=11, column=1, columnspan=2, pady=10)  # Positioned at row 5, under everything
            add_scss.after(2000, add_scss.destroy)

        except BlankFieldsError:
            add_fail = tk.Label(book_frame,
                                text="Book addition failed.\nOne or more fields are blank.\nPlease fill them in "
                                     "and try again!",
                                font=("Arial", 16),
                                fg="red")
            add_fail.grid(row=11, column=1, columnspan=2, pady=10)
            add_fail.after(2000, add_fail.destroy)
        except ValueError:
            add_fail = tk.Label(book_frame,
                                text="Year is only allowed to be a number!",
                                font=("Arial", 16),
                                fg="red")
            add_fail.grid(row=11, column=1, columnspan=2, pady=10)
            add_fail.after(2000, add_fail.destroy)