from Backend.avl_books_iter import AvBooksItr
from Backend.book_manager import BookManager
from Backend.lend_book_iter import LendBookItr
import tkinter as tk
from tkinter import messagebox
from LogConfigurator.log_decorator import log_activity


class TreeViewLoader:
    @classmethod
    @log_activity("displayed all books")
    def load_all_books(cls, treeview):
        """
        Load all books into the treeview widget. If no books are available, raise a ValueError.
        :param treeview:  The treeview widget to load the books into.
        :return:  None
        """
        if not BookManager.books:
            raise ValueError("Error loading books: No books available in the library.")
        for book in BookManager.books:
            treeview.insert("", tk.END, values=(book.get_title(), book.get_author(), book.get_year(),
                                                book.get_genre(), book.get_copies(),
                                                book.get_is_lent(), book.get_available_books_num()))

    @classmethod
    @log_activity("displayed available books")
    def load_available_books(cls, treeview):
        """
        Load available books into the treeview widget. If no available books are found, raise a ValueError.
        :param treeview:  The treeview widget to load the books into.
        :return:  None
        """
        iterator = iter(AvBooksItr(BookManager.books))
        found = False
        for book in iterator:
            treeview.insert("", tk.END, values=(book.get_title(), book.get_author(), book.get_year(),
                                                book.get_genre(), book.get_copies(),
                                                book.get_is_lent(), book.get_available_books_num()))
            found = True
        if not found:
            raise ValueError("Error loading available books: No available books found.")

    @classmethod
    @log_activity("displayed borrowed books")
    def load_borrowed_books(cls, treeview):
        """
        Load borrowed books into the treeview widget. If no borrowed books are found, raise a ValueError.
        :param treeview:  The treeview widget to load the books into.
        :return:  None
        """
        iterator = iter(LendBookItr(BookManager.books))
        found = False
        for book in iterator:
            treeview.insert("", tk.END, values=(book.get_title(), book.get_author(), book.get_year(),
                                                book.get_genre(), book.get_copies(),
                                                book.get_is_lent(), book.get_available_books_num()))
            found = True
        if not found:
            raise ValueError("Error loading borrowed books: No borrowed books found.")

    @classmethod
    @log_activity("displayed books by category")
    def load_books_by_category(cls, treeview):
        """
        Load books by category into the treeview widget. If no books are found by category, raise a ValueError.
        :param treeview:  The treeview widget to load the books into.
        :return:  None
        """
        srt_cat_books = sorted(BookManager.books, key=lambda book: book.get_genre())
        if not srt_cat_books:
            raise ValueError("Error loading books by category: No books found by category.")
        for book in srt_cat_books:
            treeview.insert("", tk.END, values=(book.get_title(), book.get_author(), book.get_year(),
                                                book.get_genre(), book.get_copies(),
                                                book.get_is_lent(), book.get_available_books_num()))

    @classmethod
    @log_activity("displayed popular books")
    def load_popular_books(cls, treeview):
        """
        Load popular books into the treeview widget. If no popular books are found, raise a ValueError.
        :param treeview:  The treeview widget to load the books into.
        :return:  None
        """
        popular_books = [book for book in BookManager.books if int(book.get_lent_count()) > 0]
        if not popular_books:
            raise ValueError("Error loading popular books: No popular books found.")
        popular_books.sort(key=lambda book: (int(book.get_lent_count()) + int(book.get_watch_list_size())),
                           reverse=True)
        for book in popular_books[:10]:
            treeview.insert("", tk.END, values=(book.get_title(), book.get_author(), book.get_year(),
                                                book.get_genre(), int(book.get_lent_count()) +
                                                int(book.get_watch_list_size())))

    @classmethod
    def load_books_into_treeview(cls, treeview, filter=0):
        """
        Load books into the treeview widget based on the filter. If no books are found, display an error message.
        :param treeview:  The treeview widget to load the books into.
        :param filter:  0: All Books, 1: Available Books, 2: Borrowed Books, 3: Books By Category, 4: Popular Books
        :return:  None
        """
        try:
            # Clear existing rows
            for row in treeview.get_children():
                treeview.delete(row)

            # Call the appropriate method based on the filter
            match filter:
                case 0:
                    try:
                        cls.load_all_books(treeview)
                    except ValueError:
                        tk.messagebox.showinfo(
                            "Loading All Books Fail",
                        "No books available in the library. Please try again later."
                        )
                case 1:
                    try:
                        cls.load_available_books(treeview)
                    except ValueError:
                        tk.messagebox.showinfo(
                            "Loading Available Books Fail",
                        "No available books found in the library. Please try again later."
                        )
                case 2:
                    try:
                        cls.load_borrowed_books(treeview)
                    except ValueError:
                        tk.messagebox.showinfo(
                            "Loading Borrowed Books Fail",
                        "No borrowed books found in the library. Please try again later."
                        )
                case 3:
                    try:
                        cls.load_books_by_category(treeview)
                    except ValueError:
                        tk.messagebox.showinfo(
                            "Loading Books By Category Fail",
                            "No books found in the library. Please try again later."
                        )
                case 4:
                    try:
                        cls.load_popular_books(treeview)
                    except ValueError:
                        tk.messagebox.showinfo(
                        "Loading Popular Books Fail",
                        "No available books found in the library. Please try again later."
                        )
                case default:
                    messagebox.showwarning("Invalid Filter", "No valid filter selected.")
        except Exception as e:
            # Display the error visually only here
            messagebox.showerror("Error", f"An error occurred: {e}")
            treeview.insert("", tk.END, values=("Error loading books", "", "", "", "", "", ""))

    def on_treeview_select(event, treeview, parent):
        """
        Get the selected item from the treeview and update the selected_item attribute in the parent class.
        :param treeview:  The treeview widget
        :param parent:  The parent class
        :return:  None
        """
        selected = treeview.focus()  # Get the focused item
        parent.selected_item = treeview.item(selected)  # Update selected_item directly in the parent class

    @classmethod
    def refresh_treeview(cls, treeview, filter=0):
        """
        Refresh the treeview widget based on the filter.
        :param treeview:  The treeview widget to refresh
        :param filter:  0: All Books, 1: Available Books, 2: Borrowed Books, 3: Books By Category, 4: Popular Books
        :return:  None
        """
        cls.load_books_into_treeview(treeview, filter)