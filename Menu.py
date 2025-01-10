import os
import time
import tkinter as tk
from tkinter import messagebox, ttk

from ExceptionBorrowingLimitExceeded import BorrowingLimitExceeded
from ExceptionReturnLimitExceeded import ReturnLimitExceeded
from ExceptionUserAlreadyInList import *
import SearchStrategy
from ExceptionWatchedBookRemovalError import WatchedBookRemovalError
from SearchStrategy import *
from Book import Book
from BookManager import BookManager
from AvBooksItr import AvBooksItr
from LntBooksItr import LntBooksItr
from LendBookItr import LendBookItr

import csv

from WaitingListManager import WaitingListManager


class Menu:
    def __init__(self, root, user_name=""):
        self.root = root  # Store the root window
        root.geometry("800x600")

        # sync books.csv with internal app books list
        BookManager.load_books()
        BookManager.load_watch_list()

        self.root.title("Menu")

        # Main menu frame
        self.menu_frame = tk.Frame(self.root)  # Create a frame inside the root window
        self.menu_frame.pack(fill="both", expand=True)

        # Book frame (used for Treeview and other contents)
        self.book_frame = tk.Frame(self.root)
        self.book_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Configure grid for consistent alignment
        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_columnconfigure(1, weight=1)
        self.menu_frame.grid_columnconfigure(2, weight=1)
        self.menu_frame.grid_columnconfigure(3, weight=1)

        # Headline
        self.headline_label = tk.Label(self.menu_frame, text=f"Welcome {user_name}", font=("Arial", 32))
        self.headline_label.grid(row=0, column=0, columnspan=4, pady=20)

        # Menu buttons
        self.add_book_button = tk.Button(self.menu_frame, text="Add Book", font=('Arial', 16), width=8,
                                         command=self.add_book)
        self.remove_book_button = tk.Button(self.menu_frame, text="Remove Book", font=('Arial', 16), width=8,
                                            command=self.remove_book)
        self.search_book_button = tk.Button(self.menu_frame, text="Search Books", font=('Arial', 16), width=8,
                                            command=self.search_book)
        self.view_book_button = tk.Button(self.menu_frame, text="View Books", font=('Arial', 16), width=8,
                                          command=self.view_book)
        self.lend_book_button = tk.Button(self.menu_frame, text="Lend Book", font=('Arial', 16), width=8,
                                          command=self.loan_book)
        self.return_book_button = tk.Button(self.menu_frame, text="Return Book", font=('Arial', 16), width=8,
                                            command=self.return_book)
        self.popular_books_button = tk.Button(self.menu_frame, text="Popular Books", font=('Arial', 16), width=8,
                                              command=self.popular_books)
        self.lgout_button = tk.Button(self.menu_frame, text="Logout", font=('Arial', 16), width=8,
                                       command=self.logout_button_func)
        self.exit_button = tk.Button(self.menu_frame, text="Exit", font=('Arial', 16), width=8,
                                      command=self.root.destroy)

        # Arrange buttons in a visually appealing grid
        self.add_book_button.grid(row=1, column=0, pady=2, padx=2)
        self.remove_book_button.grid(row=1, column=1, pady=2, padx=2)
        self.search_book_button.grid(row=1, column=2, pady=2, padx=2)
        self.view_book_button.grid(row=1, column=3, pady=2, padx=2)
        self.lend_book_button.grid(row=2, column=0, pady=2, padx=2)
        self.return_book_button.grid(row=2, column=1, pady=2, padx=2)
        self.popular_books_button.grid(row=2, column=2, pady=2, padx=2)
        self.lgout_button.grid(row=2, column=3, pady=2, padx=2)
        self.exit_button.grid(row=3, column=0, columnspan=4, pady=2)

        self.menu_frame.pack()

    def add_book(self):
        self.book_frame.destroy()
        self.book_frame = tk.Frame(self.menu_frame)
        self.text_box = tk.Label(self.book_frame, text="ADD A BOOK", font=('David', 28), width=15, pady=10)
        self.label_title = tk.Label(self.book_frame, text="Book Title:", font=('Arial', 15))
        self.label_author = tk.Label(self.book_frame, text="Author:", font=('Arial', 15))
        self.label_genre = tk.Label(self.book_frame, text="Genre:", font=('Arial', 15))
        self.label_year = tk.Label(self.book_frame, text="Year:", font=('Arial', 15))
        self.label_copies = tk.Label(self.book_frame, text="Copies:", font=('Arial', 15))

        self.entry_title = tk.Entry(self.book_frame, width=15, )
        self.entry_author = tk.Entry(self.book_frame, width=15)
        self.entry_genre = tk.Entry(self.book_frame, width=15)
        self.entry_year = tk.Entry(self.book_frame, width=15)
        self.entry_copies = tk.Entry(self.book_frame, width=15)
        self.add_button = tk.Button(self.book_frame, text="Add", font=('Arial', 18), width=8, command=self.book_adder)

        self.book_frame.grid(row=4, column=0, columnspan=3, pady=40)
        self.label_title.grid(row=5, column=0)
        self.label_author.grid(row=6, column=0)
        self.label_genre.grid(row=7, column=0)
        self.label_year.grid(row=8, column=0)
        self.label_copies.grid(row=9, column=0)
        self.text_box.grid(row=4, column=1)
        self.entry_title.grid(row=5, column=1)
        self.entry_author.grid(row=6, column=1)
        self.entry_genre.grid(row=7, column=1)
        self.entry_year.grid(row=8, column=1)
        self.entry_copies.grid(row=9, column=1)
        self.add_button.grid(row=10, column=1, pady=20)

    def book_adder(self):
        # b = Book(self.entry_title.get(), self.entry_author.get(), self.entry_genre.get(), self.entry_year.get(),self.entry_copies.get())
        # Book.add(b,self.entry_title.get(), self.entry_author.get(), self.entry_genre.get(), self.entry_year.get(),self.entry_copies.get())
        if BookManager.add_book(self.entry_title.get(), self.entry_author.get(), self.entry_genre.get(),
                                self.entry_year.get(), self.entry_copies.get()):
            self.add_scss = tk.Label(self.book_frame, text="Book added successfully!", font=("Arial", 16), fg="green")
            self.add_scss.grid(row=11, column=1, columnspan=2, pady=10)  # Positioned at row 5, under everything
            self.add_scss.after(2000, self.add_scss.destroy)

        else:
            self.add_fail = tk.Label(self.book_frame,
                                     text="Book addition failed.\nOne or more fields are blank.\nPlease fill them in and try again!",
                                     font=("Arial", 16),
                                     fg="red")
            self.add_fail.grid(row=11, column=1, columnspan=2, pady=10)
            self.add_fail.after(2000, self.add_fail.destroy)

    def book_remover(self):
        try:
            if BookManager.remove_book(self.entry_title.get(), self.entry_author.get(), self.entry_genre.get(),
                                       self.entry_year.get()):
                self.rmv_scss = tk.Label(self.book_frame, text="Removed Succesfuly!", font=("Arial", 16), fg="green")
                self.rmv_scss.grid(row=10, column=1, columnspan=2, pady=10)  # Positioned at row 5, under everything
                self.rmv_scss.after(2000, self.rmv_scss.destroy)
            else:
                self.rmv_fail = tk.Label(self.book_frame, text="Removed Failed! Book does not exists.", font=("Arial", 16),
                                         fg="red")
                self.rmv_fail.grid(row=10, column=1, columnspan=2, pady=10)
                self.rmv_fail.after(2000, self.rmv_fail.destroy)
        except WatchedBookRemovalError:
            tk.messagebox.showinfo(
                "Watched Book Removal Error",
                "The selected book is currently being watched and cannot be removed."
            )
    def remove_book(self):
        self.book_frame.destroy()
        self.book_frame = tk.Frame(self.menu_frame)
        self.text_box = tk.Label(self.book_frame, text="REMOVE A BOOK:", font=('David', 28), width=15, pady=10)
        self.label_title = tk.Label(self.book_frame, text="Book Title:", font=('Arial', 15))
        self.label_author = tk.Label(self.book_frame, text="Author:", font=('Arial', 15))
        self.label_genre = tk.Label(self.book_frame, text="Genre:", font=('Arial', 15))
        self.label_year = tk.Label(self.book_frame, text="Year:", font=('Arial', 15))

        self.entry_title = tk.Entry(self.book_frame, width=15, )
        self.entry_author = tk.Entry(self.book_frame, width=15)
        self.entry_genre = tk.Entry(self.book_frame, width=15)
        self.entry_year = tk.Entry(self.book_frame, width=15)
        self.remove_button = tk.Button(self.book_frame, text="Remove", font=('Arial', 18), width=8,
                                       command=self.book_remover)

        self.book_frame.grid(row=4, column=0, columnspan=3, pady=40)
        self.label_title.grid(row=5, column=0)
        self.label_author.grid(row=6, column=0)
        self.label_genre.grid(row=7, column=0)
        self.label_year.grid(row=8, column=0)
        self.text_box.grid(row=4, column=1)
        self.entry_title.grid(row=5, column=1)
        self.entry_author.grid(row=6, column=1)
        self.entry_genre.grid(row=7, column=1)
        self.entry_year.grid(row=8, column=1)
        self.remove_button.grid(row=9, column=1, pady=20)

    def search_book(self):
        # Clear and set up the frame
        self.book_frame.destroy()
        self.book_frame = tk.Frame(self.menu_frame)
        self.book_frame.grid(row=4, column=0, columnspan=3, pady=20, padx=20)

        # Configure the grid for centering
        self.book_frame.grid_columnconfigure(0, weight=1)
        self.book_frame.grid_columnconfigure(1, weight=1)
        self.book_frame.grid_columnconfigure(2, weight=1)
        self.book_frame.grid_columnconfigure(3, weight=1)

        # Title for the section
        self.text_box = tk.Label(self.book_frame, text="Search Books", font=('David', 28), pady=10)
        self.text_box.grid(row=0, column=1, columnspan=2, pady=10)

        # Search input and filter
        self.search_box_label = tk.Label(self.book_frame, text="Search:", font=('Arial', 15))
        self.search_box_label.grid(row=1, column=0, padx=10, sticky="e")

        self.entry_search = tk.Entry(self.book_frame, width=20)
        self.entry_search.grid(row=1, column=1, padx=10, sticky="w")

        self.selected_option = tk.StringVar(value="Title")  # Default filter option
        self.search_filter = ttk.Combobox(
            self.book_frame,
            width=15,
            textvariable=self.selected_option,
            state="readonly"
        )
        self.search_filter['values'] = ('Title', 'Author', 'Year', 'Genre')
        self.search_filter.grid(row=1, column=2, padx=10, sticky="w")

        # Search button
        self.search_button = tk.Button(
            self.book_frame,
            text="Search",
            font=('Arial', 18),
            width=10,
            command=lambda: self.perform_search(self.selected_option.get(), self.entry_search.get())
        )
        self.search_button.grid(row=1, column=3, padx=10)

        # Treeview setup
        self.treeview = ttk.Treeview(
            self.book_frame,
            columns=("Title", "Author", "Year", "Genre", "Copies", "is_loaned","is_Available"),
            show="headings",
            height=8  # Matches the height of the view_book table
        )

        # Configure columns
        self.treeview.column("Title", width=150, anchor="center")
        self.treeview.column("Author", width=120, anchor="center")
        self.treeview.column("Year", width=80, anchor="center")
        self.treeview.column("Genre", width=120, anchor="center")
        self.treeview.column("Copies", width=60, anchor="center")
        self.treeview.column("is_loaned", width=100, anchor="center")
        self.treeview.column("is_Available", width=100, anchor="center")
        # Set column headers
        self.treeview.heading("Title", text="Title")
        self.treeview.heading("Author", text="Author")
        self.treeview.heading("Year", text="Year")
        self.treeview.heading("Genre", text="Genre")
        self.treeview.heading("Copies", text="Copies")
        self.treeview.heading("is_loaned", text="Is Lent?")
        self.treeview.heading("is_Available", text="Available copies")

        # Load books into Treeview
        self.load_books_into_treeview()

        # Place Treeview
        self.treeview.grid(row=2, column=0, columnspan=4, pady=10, padx=10)

        # Bind selection event
        self.treeview.bind("<<TreeviewSelect>>", self.on_treeview_select)
        self.selected_item = None  # Initialize selected item

    def perform_search(self, query, strategy):
        context = None
        #strategy selection to classes
        if query == 'Title':
            context = StrategySearchByTitle.search(strategy)
        elif query == 'Author':
            context = StrategySearchByAuthor.search(strategy)
        elif query == 'Genre':
            context = StrategySearchByGenre.search(strategy)
        elif query == 'Year':
            context = StrategySearchByYear.search(strategy)

        if context:
            # results = context.search(BookManager.books, query)
            # Display results in the UI
            self.treeview.delete(*self.treeview.get_children())  # Clear existing rows
            for book in context:
                self.treeview.insert("", "end", values=(
                    book.get_title(), book.get_author(), book.get_year(), book.get_genre(), book.get_copies(),
                    book.get_is_lent()))

        else:
            self.treeview.delete(*self.treeview.get_children())  # Clear existing rows

    def view_book(self):
        # Clear and set up the frame
        self.book_frame.destroy()
        self.book_frame = tk.Frame(self.menu_frame)
        self.book_frame.grid(row=4, column=0, columnspan=3, pady=20, padx=20)

        # Configure the grid for centering
        self.book_frame.grid_columnconfigure(0, weight=1)
        self.book_frame.grid_columnconfigure(1, weight=1)
        self.book_frame.grid_columnconfigure(2, weight=1)
        self.book_frame.grid_columnconfigure(3, weight=1)

        # Title for the section
        self.text_box = tk.Label(self.book_frame, text="List of Books", font=('David', 28), pady=10)
        self.text_box.grid(row=0, column=1, columnspan=2, pady=10)

        # Treeview setup
        self.treeview = ttk.Treeview(
            self.book_frame,
            columns=("Title", "Author", "Year", "Genre", "Copies", "is_loaned","is_Available"),
            show="headings",
            height=8  # Matches the height of the view_book table
        )

        # Configure columns
        self.treeview.column("Title", width=150, anchor="center")
        self.treeview.column("Author", width=120, anchor="center")
        self.treeview.column("Year", width=80, anchor="center")
        self.treeview.column("Genre", width=120, anchor="center")
        self.treeview.column("Copies", width=60, anchor="center")
        self.treeview.column("is_loaned", width=100, anchor="center")
        self.treeview.column("is_Available", width=100, anchor="center")
        # Set column headers
        self.treeview.heading("Title", text="Title")
        self.treeview.heading("Author", text="Author")
        self.treeview.heading("Year", text="Year")
        self.treeview.heading("Genre", text="Genre")
        self.treeview.heading("Copies", text="Copies")
        self.treeview.heading("is_loaned", text="Is Lent?")
        self.treeview.heading("is_Available", text="Available copies")

        # Load books into Treeview
        self.load_books_into_treeview()

        # Place Treeview
        self.treeview.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

        # Filter buttons
        self.Available_button = tk.Button(self.book_frame, text="Available Books", font=('Arial', 14), width=15,
                                          command=lambda: self.load_books_into_treeview(1))
        self.All_Books_button = tk.Button(self.book_frame, text="All Books", font=('Arial', 14), width=15,
                                          command=lambda: self.load_books_into_treeview(0))
        self.Lend_button = tk.Button(self.book_frame, text="Lended Books", font=('Arial', 14), width=15,
                                     command=lambda: self.load_books_into_treeview(2))
        self.by_category = tk.Button(self.book_frame, text="By Category", font=('Arial', 14), width=15,
                                     command=lambda: self.load_books_into_treeview(3))

        # Place filter buttons in a centered row
        self.Available_button.grid(row=2, column=0, pady=10, padx=5)
        self.All_Books_button.grid(row=2, column=1, pady=10, padx=5)
        self.Lend_button.grid(row=2, column=2, pady=10, padx=5)
        self.by_category.grid(row=2, column=3, pady=10, padx=5)

    def load_books_into_treeview(self, filter=0):
        # delete all exist books
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        match filter:
            case 0:
                # base case , show all books
                for book in BookManager.books:
                    self.treeview.insert("", tk.END, values=(
                        book.get_title(), book.get_author(), book.get_year(), book.get_genre(), book.get_copies(),
                        book.get_is_lent(),book.get_Available_books_num()))
            case 1:
                # case 1 , sort by only available books.
                iterator = iter(AvBooksItr(BookManager.books))
                for book in iterator:
                    self.treeview.insert("", tk.END, values=(
                        book.get_title(), book.get_author(), book.get_year(), book.get_genre(), book.get_copies(),
                        book.get_is_lent(),book.get_Available_books_num()))

            case 2:
                # case 2 , sort by the books that are being lent.
                # sorted takes the current list and duplicates (and sorts) it to a new list
                iterator = iter(LendBookItr(BookManager.books))
                for book in iterator:
                    self.treeview.insert("", tk.END, values=(
                        book.get_title(), book.get_author(), book.get_year(), book.get_genre(), book.get_copies(),
                        book.get_is_lent(),book.get_Available_books_num()))

            case 3:
                # case 3 , sort by only lent books.
                srt_cat_books = sorted(BookManager.books, key=lambda book: book.get_genre())
                for book in srt_cat_books:
                    self.treeview.insert("", tk.END, values=(
                        book.get_title(), book.get_author(), book.get_year(), book.get_genre(), book.get_copies(),
                        book.get_is_lent(),book.get_Available_books_num()))

            case 4:
                popular_books = []
                # case 3 , sort by only popularity books.
                for book in BookManager.books:
                        if int(book.get_lent_count()) > 0:
                            popular_books.append(book)
                popular_books.sort(key=lambda book: (int(book.get_lent_count())+int(book.get_watch_list_size())), reverse=True)
                for book in popular_books[:10]:
                    self.treeview.insert("", tk.END, values=(
                        book.get_title(), book.get_author(), book.get_year(), book.get_genre(),
                        int(book.get_lent_count())+int(book.get_watch_list_size())))

            case default:
                return "no filter"

    def loan_book(self):
        # Clear and set up the frame
        self.book_frame.destroy()
        self.book_frame = tk.Frame(self.menu_frame)
        self.book_frame.grid(row=4, column=0, columnspan=3, pady=20, padx=20)

        # Configure the grid for centering
        self.book_frame.grid_columnconfigure(0, weight=1)
        self.book_frame.grid_columnconfigure(1, weight=1)
        self.book_frame.grid_columnconfigure(2, weight=1)
        self.book_frame.grid_columnconfigure(3, weight=1)

        # Title for the section
        self.text_box = tk.Label(self.book_frame, text="Lend A Book", font=('David', 28), pady=10)
        self.text_box.grid(row=0, column=1, columnspan=2, pady=10)

        # Treeview setup
        self.treeview = ttk.Treeview(
            self.book_frame,
            columns=("Title", "Author", "Year", "Genre", "Copies", "is_loaned","is_Available"),
            show="headings",
            height=8  # Matches the height of the view_book table
        )

        # Configure columns
        self.treeview.column("Title", width=150, anchor="center")
        self.treeview.column("Author", width=120, anchor="center")
        self.treeview.column("Year", width=80, anchor="center")
        self.treeview.column("Genre", width=120, anchor="center")
        self.treeview.column("Copies", width=60, anchor="center")
        self.treeview.column("is_loaned", width=100, anchor="center")
        self.treeview.column("is_Available", width=100, anchor="center")
        # Set column headers
        self.treeview.heading("Title", text="Title")
        self.treeview.heading("Author", text="Author")
        self.treeview.heading("Year", text="Year")
        self.treeview.heading("Genre", text="Genre")
        self.treeview.heading("Copies", text="Copies")
        self.treeview.heading("is_loaned", text="Is Lent?")
        self.treeview.heading("is_Available", text="Available copies")
        # Load books into Treeview
        self.load_books_into_treeview()

        # Place Treeview
        self.treeview.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

        # Bind selection event
        self.treeview.bind("<<TreeviewSelect>>", self.on_treeview_select)

        # Button to perform the lend action
        self.lend_button = tk.Button(self.book_frame, text="Lend!", font=('Arial', 16), width=10,
                                     command=self.book_lending)
        self.lend_button.grid(row=2, column=1, columnspan=2, pady=10)

        # Initialize selected item
        self.selected_item = None

    def on_treeview_select(self, event):
        selected = self.treeview.focus()  # Get the focused item
        self.selected_item = self.treeview.item(selected)  # Store the selected item's details

    def book_lending(self):
        # check if there are available books to borrow
        # if True , let me borrow the book.
        #if False , The safran has to fill the details of the borrower to add it to the waiting list.
        if self.selected_item:
            selected_values = self.selected_item['values']
            selected_title = selected_values[0]
            selected_author = selected_values[1]
            selected_year = selected_values[2]
            selected_genre = selected_values[3]
            #selected_copies = int(selected_values[4])  # Convert copies to int if necessary

            for book in BookManager.books:
                if (book.get_title() == str(selected_title) and
                        book.get_author() == str(selected_author) and
                        book.get_year() == str(selected_year) and
                        book.get_genre() == str(selected_genre)):

                    if book.get_is_lent() == "No":
                        try:
                            book.borrow_action()  # Borrow the book and add +1 to book lent
                            #TODO implement update CSV file with filter 1
                            BookManager.update_in_csv(book,1)
                            tk.messagebox.showinfo(
                                "Success",
                                f"Book '{selected_title}' is available! Lending now."
                            )
                        except BorrowingLimitExceeded:
                            tk.messagebox.showinfo(
                                "Failed",
                                f"Selected book: '{selected_title}' cannot be borrowed!\n"
                                f"No. of Book Copies Available: {book.get_copies() -book.get_lent_count()}\n"
                            )
                    else:
                        self.show_waiting_list_form(book)
                    break
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

    def show_waiting_list_form(self, book):
        # Create a new popup window
        popup = tk.Toplevel(self.root)
        popup.title("Add to Waiting List")
        popup.geometry("450x280")

        tk.Label(popup, text=f"Book '{book.get_title()}' is not available. fill details to join waiting list:", font=("Arial", 14)).grid(row=0, column=1, pady=10, padx=10)

        # Form fields
        tk.Label(popup, text="Full Name:", font=("Arial", 14)).grid(row=1, column=0, pady=10, padx=2)
        self.name_entry = tk.Entry(popup, font=("Arial", 14))
        self.name_entry.grid(row=1, column=1, pady=10, padx=2)

        tk.Label(popup, text="Email:", font=("Arial", 14)).grid(row=2, column=0, pady=10, padx=2)
        self.email_entry = tk.Entry(popup, font=("Arial", 14))
        self.email_entry.grid(row=2, column=1, pady=10, padx=2)

        tk.Label(popup, text="Phone:", font=("Arial", 14)).grid(row=3, column=0, pady=10, padx=2)
        self.phone_entry = tk.Entry(popup, font=("Arial", 14))
        self.phone_entry.grid(row=3, column=1, pady=10, padx=2)
        tk.Button(popup, text="Add to Waiting List", font=("Arial", 14), command=lambda: WaitingListManager.add_to_waiting_list(popup,book,self.name_entry.get(),self.phone_entry.get(),self.email_entry.get())).grid(row=4,
                                                                                                           column=0,
                                                                                                           columnspan=2,
                                                                                                           pady=20)
    def return_book(self):
        self.book_frame.destroy()
        self.book_frame = tk.Frame(self.menu_frame)
        self.book_frame.grid(row=4, column=0, columnspan=3, pady=40)
       # Configure the grid for centering
        self.book_frame.grid_columnconfigure(0, weight=1)
        self.book_frame.grid_columnconfigure(1, weight=1)
        self.book_frame.grid_columnconfigure(2, weight=1)
        self.book_frame.grid_columnconfigure(3, weight=1)

        # Title for the section
        self.text_box = tk.Label(self.book_frame, text="Return of Books", font=('David', 28), pady=10)
        self.text_box.grid(row=0, column=1, columnspan=2, pady=10)

        # Treeview setup
        self.treeview = ttk.Treeview(
            self.book_frame,
            columns=("Title", "Author", "Year", "Genre", "Copies", "is_loaned","is_Available"),
            show="headings",
            height=8  # Matches the height of the view_book table
        )

        # Configure columns
        self.treeview.column("Title", width=150, anchor="center")
        self.treeview.column("Author", width=120, anchor="center")
        self.treeview.column("Year", width=80, anchor="center")
        self.treeview.column("Genre", width=120, anchor="center")
        self.treeview.column("Copies", width=60, anchor="center")
        self.treeview.column("is_loaned", width=100, anchor="center")
        self.treeview.column("is_Available", width=100, anchor="center")
        # Set column headers
        self.treeview.heading("Title", text="Title")
        self.treeview.heading("Author", text="Author")
        self.treeview.heading("Year", text="Year")
        self.treeview.heading("Genre", text="Genre")
        self.treeview.heading("Copies", text="Copies")
        self.treeview.heading("is_loaned", text="Is Lent?")
        self.treeview.heading("is_Available", text="Available copies")

        # Load books into Treeview
        self.load_books_into_treeview(2)
        # Place Treeview
        self.treeview.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

        self.button_return_book = tk.Button(self.book_frame, text="Return Book", font=('Arial', 14), width=15,
                                     command=lambda: self.book_returner(self.selected_item))
        # Place filter buttons in a centered row
        self.button_return_book.grid(row=2, column=0, pady=10, padx=5)

        # Bind selection event
        self.treeview.bind("<<TreeviewSelect>>", self.on_treeview_select)
        self.selected_item = None  # Initialize selected item



    def popular_books(self):
        # Clear and set up the frame
        self.book_frame.destroy()
        self.book_frame = tk.Frame(self.menu_frame)
        self.book_frame.grid(row=4, column=0, columnspan=3, pady=20, padx=20)

        # Configure the grid for centering
        self.book_frame.grid_columnconfigure(0, weight=1)
        self.book_frame.grid_columnconfigure(1, weight=1)
        self.book_frame.grid_columnconfigure(2, weight=1)
        self.book_frame.grid_columnconfigure(3, weight=1)

        # Title for the section
        self.text_box = tk.Label(self.book_frame, text="Popular Books", font=('David', 28), pady=10)
        self.text_box.grid(row=0, column=1, columnspan=2, pady=10)

        # Treeview setup
        self.treeview = ttk.Treeview(
            self.book_frame,
            columns=("Title", "Author", "Year", "Genre", "Popular Rate"),
            show="headings",
            height=8  # Matches the height of the view_book table
        )

        # Configure columns
        self.treeview.column("Title", width=150, anchor="center")
        self.treeview.column("Author", width=120, anchor="center")
        self.treeview.column("Year", width=80, anchor="center")
        self.treeview.column("Genre", width=120, anchor="center")
        self.treeview.column("Popular Rate", width=120, anchor="center")

        # Set column headers
        self.treeview.heading("Title", text="Title")
        self.treeview.heading("Author", text="Author")
        self.treeview.heading("Year", text="Year")
        self.treeview.heading("Genre", text="Genre")
        self.treeview.heading("Popular Rate", text="Popular Rate")


        # Load books into Treeview
        self.load_books_into_treeview(4)

        # Place Treeview
        self.treeview.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

    def logout_button_func(self):
        self.menu_frame.destroy()  # Destroy the current register frame
        from Login import Login  # Import the Login class here
        Login(self.root)  # Pass the root window to Login screen

    def book_returner(self, selected_item):
        if self.selected_item:
            selected_values = self.selected_item['values']
            selected_title = str(selected_values[0])
            selected_author =str(selected_values[1])
            selected_year = str(selected_values[2])
            selected_genre =str(selected_values[3])
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

