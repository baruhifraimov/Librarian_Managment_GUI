import os
import time
import tkinter as tk
from tkinter import messagebox, ttk
from Book import Book
from BookManager import BookManager
from AvBooksItr import AvBooksItr
from LntBooksItr import LntBooksItr

import csv


class Menu:
    def __init__(self, root, user_name=""):
        self.root = root  # Store the root window
        root.geometry("800x600")
        self.load_books()
        # self.background_image = tk.PhotoImage(file="background.png")
        # self.background_label = tk.Label(root, image=self.background_image)
        # self.background_label.place(relwidth=1, relheight=1)

        self.menu_frame = tk.Frame(self.root)  # Create a frame inside the root window
        self.book_frame = tk.Frame(self.menu_frame, bg="red")
        self.root.title("Menu")
        self.headline_label = tk.Label(self.menu_frame, text=f"Welcome {user_name}", font=("Arial", 32))
        self.add_book_button = tk.Button(self.menu_frame, text="Add Book", font=('Arial', 18), width=8,
                                         command=self.add_book)
        self.remove_book_button = tk.Button(self.menu_frame, text="Remove Book", font=('Arial', 18), width=8,
                                            command=self.remove_book)
        self.search_book_button = tk.Button(self.menu_frame, text="Search Books", font=('Arial', 18), width=8,
                                            command=self.search_book)

        self.view_book_button = tk.Button(self.menu_frame, text="View Books", font=('Arial', 18), width=8,
                                          command=self.view_book)
        self.lend_book_button = tk.Button(self.menu_frame, text="Lend Book", font=('Arial', 18), width=8,
                                          command=self.lend_book)
        self.return_book_button = tk.Button(self.menu_frame, text="Return Book", font=('Arial', 18), width=8,
                                            command=self.return_book)
        self.popular_books_button = tk.Button(self.menu_frame, text="Popular Books", font=('Arial', 18), width=8,
                                              command=self.popular_books())

        self.exit_button = tk.Button(self.menu_frame, text="Exit", font=('Arial', 18), width=8,
                                     command=self.root.destroy)
        self.lgout_button = tk.Button(self.menu_frame, text="Logout", font=('Arial', 18), width=8,
                                      command=self.logout_button_func)

        self.headline_label.grid(row=0, column=1, rowspan=2, sticky="news", pady=15)

        self.add_book_button.grid(row=2, column=0, padx=5, pady=30)
        self.remove_book_button.grid(row=2, column=1, padx=5, pady=30)
        self.search_book_button.grid(row=2, column=2, padx=5, pady=30)
        self.view_book_button.grid(row=3, column=0, padx=5, pady=0)
        self.lend_book_button.grid(row=3, column=1, padx=5, pady=0)
        self.return_book_button.grid(row=3, column=2, padx=5, pady=0)
        self.popular_books_button.grid(row=3, column=3, padx=5, pady=0)

        self.lgout_button.grid(row=0, column=0)
        self.exit_button.grid(row=1, column=0)

        self.menu_frame.pack()

    def load_books(self):
        with open('books.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows[1:]:
                b = Book(row[0], row[1], row[4], row[5], row[3], row[2])
                BookManager.books.append(b)

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
            self.add_scss.after(2000, self.rmv_scss.destroy)

        else:
            self.add_fail = tk.Label(self.book_frame, text="Book addition failed.\nOne or more fields are blank.\nPlease fill them in and try again!", font=("Arial", 16),
                                     fg="red")
            self.add_fail.grid(row=11, column=1, columnspan=2, pady=10)
            self.add_fail.after(2000, self.add_fail.destroy)

    def book_remover(self):
        if BookManager.remove_book(self.entry_title.get(), self.entry_author.get(), self.entry_genre.get(),self.entry_year.get()):
            self.rmv_scss = tk.Label(self.book_frame, text="Removed Succesfuly!", font=("Arial", 16), fg="green")
            self.rmv_scss.grid(row=10, column=1, columnspan=2, pady=10)  # Positioned at row 5, under everything
            self.rmv_scss.after(2000,self.rmv_scss.destroy)
        else:
            self.rmv_fail = tk.Label(self.book_frame, text="Removed Failed! Book does not exists.", font=("Arial", 16),
                                      fg="red")
            self.rmv_fail.grid(row=10, column=1, columnspan=2, pady=10)
            self.rmv_fail.after(2000, self.rmv_fail.destroy)

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
        # TODO implement search books by using Strategy pattern .
        self.book_frame.destroy()
        self.book_frame = tk.Frame(self.menu_frame)
        self.text_box = tk.Label(self.book_frame, text="Search books", font=('David', 28), width=15, pady=10)
        self.search_box_label = tk.Label(self.book_frame, text="search:", font=('Arial', 15))
        self.entry_search = tk.Entry(self.book_frame, width=15)
        self.search_button = tk.Button(self.book_frame, text="Search", font=('Arial', 18), width=8) #,command=pass)
        self.text_box.grid(row=4, column=1)
        self.treeview = ttk.Treeview(self.book_frame, columns=("Title", "Author", "Year", "Genre", "Copies", "is_loaned"),show="headings")

        # Here the search begins
        value = self.entry_search.get()


        n = tk.StringVar()
        monthchoosen = ttk.Combobox(self.book_frame, width=27, textvariable=n)
        # Adding combobox drop down list
        monthchoosen['values'] = (' Title',
                                  ' Author',
                                  ' Year',
                                  ' Genre',)

        monthchoosen.grid(column=2, row=5)
        monthchoosen.current()

        # set titles
        self.treeview.heading("Title", text="Title")
        self.treeview.heading("Author", text="Author")
        self.treeview.heading("Year", text="Year")
        self.treeview.heading("Genre", text="Genre")
        self.treeview.heading("Copies", text="Copies")
        self.treeview.heading("is_loaned", text="Is lent?")
        self.load_books_into_treeview()

        self.book_frame.grid(row=4, column=0, columnspan=3, pady=40)
        self.search_box_label.grid(row=5, column=0)
        self.entry_search.grid(row=5, column=1)
        self.search_button.grid(row=5, column=3)
        self.treeview.grid(row=7, column=1, pady=20)




    def view_book(self):
        self.book_frame.destroy()
        self.book_frame = tk.Frame(self.menu_frame)
        self.text_box = tk.Label(self.book_frame, text="List of Books", font=('David', 28), width=15, pady=10)
        self.text_box.grid(row=4, column=1)
        self.treeview = ttk.Treeview(self.book_frame,
                                     columns=("Title", "Author", "Year", "Genre", "Copies", "is_loaned"),
                                     show="headings")
        # set titles
        self.treeview.heading("Title", text="Title")
        self.treeview.heading("Author", text="Author")
        self.treeview.heading("Year", text="Year")
        self.treeview.heading("Genre", text="Genre")
        self.treeview.heading("Copies", text="Copies")
        self.treeview.heading("is_loaned", text="Is lent?")



        # books showcase in treeview method
        self.load_books_into_treeview()

        # filter button to move between different views
        self.Available_button = tk.Button(self.book_frame, text="Available Books", font=('Arial', 18), width=15,
                                          command=lambda: self.load_books_into_treeview(1))
        self.All_Books_button = tk.Button(self.book_frame, text="All Books", font=('Arial', 18), width=15,
                                          command=lambda: self.load_books_into_treeview(0))
        self.Lend_button = tk.Button(self.book_frame, text="Lended Books", font=('Arial', 18), width=15,
                                     command=lambda: self.load_books_into_treeview(2))
        self.by_category = tk.Button(self.book_frame, text="By Category", font=('Arial', 18), width=15,
                                     command=lambda: self.load_books_into_treeview(3))

        self.book_frame.grid(row=4, column=0, columnspan=3, pady=40)
        self.Available_button.grid(row=5, column=0, pady=10)
        self.All_Books_button.grid(row=5, column=1, pady=10)
        self.Lend_button.grid(row=5, column=2, pady=10)
        self.by_category.grid(row=5, column=3, pady=10)
        self.treeview.grid(row=7, column=1, pady=20)

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
                    book.get_is_lend()))
            case 1:
                # case 1 , sort by only available books.
                iterator = iter(AvBooksItr(BookManager.books))
                for book in iterator:
                    self.treeview.insert("", tk.END, values=(
                    book.get_title(), book.get_author(), book.get_year(), book.get_genre(), book.get_copies(),
                    book.get_is_lend()))
            case 2:
                # case 2 , sort by only lent books.
                iterator = iter(LntBooksItr(BookManager.books))
                for book in iterator:
                    self.treeview.insert("", tk.END, values=(
                    book.get_title(), book.get_author(), book.get_year(), book.get_genre(), book.get_copies(),
                    book.get_is_lend()))
            case 3:
                # case 2 , sort by only lent books.
                # sorted takes the current list and duplicates (and sorts) it to a new list
                sorted_books = sorted(BookManager.books, key=lambda x: x.get_genre())
                for book in sorted_books:
                    self.treeview.insert("", tk.END, values=(
                        book.get_title(), book.get_author(), book.get_year(), book.get_genre(), book.get_copies(),
                        book.get_is_lend()))

            case default:
                return "something"

    def lend_book(self):
        self.book_frame.destroy()
        self.book_frame = tk.Frame(self.menu_frame)
        self.text_box = tk.Button(self.book_frame, text="THIS IS LEND BOOK", font=('David', 36), width=15)
        self.book_frame.grid(row=4, column=0, columnspan=3, pady=40)
        self.text_box.grid(row=4, column=1)

    def return_book(self):
        self.book_frame.destroy()
        self.book_frame = tk.Frame(self.menu_frame)
        self.text_box = tk.Button(self.book_frame, text="THIS IS RETURN BOOK", font=('David', 36), width=15)
        self.book_frame.grid(row=4, column=0, columnspan=3, pady=40)
        self.text_box.grid(row=4, column=1)

    def popular_books(self):
        self.book_frame.destroy()
        self.book_frame = tk.Frame(self.menu_frame)
        self.text_box = tk.Button(self.book_frame, text="THIS IS POPULAR BOOKS", font=('David', 36), width=15)
        self.book_frame.grid(row=4, column=0, columnspan=3, pady=40)
        self.text_box.grid(row=4, column=1)

    def logout_button_func(self):
        self.menu_frame.destroy()  # Destroy the current register frame
        from Login import Login  # Import the Login class here
        Login(self.root)  # Pass the root window to Login screen