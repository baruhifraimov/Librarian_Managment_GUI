import tkinter as tk
from tkinter import ttk

import main
from Backend.add_book import AddBook
from Backend.lend_book import LendBook
from Backend.remove_book import RemoveBook
from Backend.search_book import SearchBook
from Backend.book_manager import BookManager
from Backend.tree_view_loader import TreeViewLoader
from Backend.return_book import ReturnBook
from tkinter import messagebox

from Backend.librarian_manager import LibrarianManager
from LogConfigurator.log_decorator import log_activity


class Menu:
    def __init__(self, root, user):
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
        self.headline_label = tk.Label(self.menu_frame, text=f"Welcome {user.get_username()}", font=("Arial", 32))
        self.headline_label.grid(row=0, column=0, columnspan=4, pady=20)

        # Menu buttons
        self.add_book_button = tk.Button(self.menu_frame, text="Add Book", font=('Arial', 16), width=8,
                                         command=self.add_book_widget)
        self.remove_book_button = tk.Button(self.menu_frame, text="Remove Book", font=('Arial', 16), width=8,
                                            command=self.remove_book_widget)
        self.search_book_button = tk.Button(self.menu_frame, text="Search Books", font=('Arial', 16), width=8,
                                            command=self.search_book_widget)
        self.view_book_button = tk.Button(self.menu_frame, text="View Books", font=('Arial', 16), width=8,
                                          command=self.view_book_widget)
        self.lend_book_button = tk.Button(self.menu_frame, text="Lend Book", font=('Arial', 16), width=8,
                                          command=self.loan_book_widget)
        self.return_book_button = tk.Button(self.menu_frame, text="Return Book", font=('Arial', 16), width=8,
                                            command=self.return_book_widget)
        self.popular_books_button = tk.Button(self.menu_frame, text="Popular Books", font=('Arial', 16), width=8,
                                              command=self.popular_books_widget)
        self.logout_button = tk.Button(self.menu_frame, text="Logout", font=('Arial', 16), width=8,
                                       command=lambda: self.logout_button_func(user))
        self.exit_button = tk.Button(self.menu_frame, text="Exit", font=('Arial', 16), width=8,
                                     command=self.exit_func)

        # Arrange buttons in a visually appealing grid
        self.add_book_button.grid(row=1, column=0, pady=2, padx=2)
        self.remove_book_button.grid(row=1, column=1, pady=2, padx=2)
        self.search_book_button.grid(row=1, column=2, pady=2, padx=2)
        self.view_book_button.grid(row=1, column=3, pady=2, padx=2)
        self.lend_book_button.grid(row=2, column=0, pady=2, padx=2)
        self.return_book_button.grid(row=2, column=1, pady=2, padx=2)
        self.popular_books_button.grid(row=2, column=2, pady=2, padx=2)
        self.logout_button.grid(row=2, column=3, pady=2, padx=2)
        self.exit_button.grid(row=3, column=0, columnspan=4, pady=2)

        self.menu_frame.pack()

        # Display user notifications
        self.display_user_notifications(user)

    @log_activity('display notification to user')
    def display_user_notifications(self, user):
        """
        Display user notifications in a messagebox.
        :param user: The user to display the notifications for.
        """
        while user.get_user_messages_size() > 0:
            message = user.pop_user_message()
            tk.messagebox.showinfo(f"Notifications[{user.get_user_messages_size() + 1}]", message=message)
        else:
            tk.messagebox.showinfo("No Notifications", "You have no notifications.")

    def exit_func(self):
        """
        Close the application.
        """
        main.on_close(self.root)

    def add_book_widget(self):
        """
        Display the add book widget.
        """
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
        self.add_button = tk.Button(self.book_frame, text="Add", font=('Arial', 18), width=8,
                                    command=lambda: AddBook.book_adder(self.entry_title.get(), self.entry_author.get(),
                                                                       self.entry_genre.get(),
                                                                       self.entry_year.get(), self.entry_copies.get(),
                                                                       self.book_frame))

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

    def remove_book_widget(self):
        """
        Display the remove book widget.
        """
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
                                       command=lambda: RemoveBook.book_remover(self.entry_title.get(),
                                                                               self.entry_author.get(),
                                                                               self.entry_genre.get(),
                                                                               self.entry_year.get(), self.book_frame))

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

    def search_book_widget(self):
        """
        Display the search book widget.
        """
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
            command=lambda: SearchBook.perform_search(self.selected_option.get(), self.entry_search.get(),
                                                      self.treeview)
        )
        self.search_button.grid(row=1, column=3, padx=10)

        # Treeview setup
        self.treeview = ttk.Treeview(
            self.book_frame,
            columns=("Title", "Author", "Year", "Genre", "Copies", "is_loaned", "is_Available"),
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
        TreeViewLoader.load_books_into_treeview(self.treeview)

        # Place Treeview
        self.treeview.grid(row=2, column=0, columnspan=4, pady=10, padx=10)

        # Bind selection event
        self.treeview.bind("<<TreeviewSelect>>",
                           lambda event: TreeViewLoader.on_treeview_select(event, self.treeview, self))
        self.selected_item = None  # Initialize selected item

    def view_book_widget(self):
        """
        Display the view book widget.
        """
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
            columns=("Title", "Author", "Year", "Genre", "Copies", "is_loaned", "is_Available"),
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
        TreeViewLoader.load_books_into_treeview(self.treeview)

        # Place Treeview
        self.treeview.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

        # Filter buttons
        self.Available_button = tk.Button(self.book_frame, text="Available Books", font=('Arial', 14), width=15,
                                          command=lambda: TreeViewLoader.load_books_into_treeview(self.treeview, 1))
        self.All_Books_button = tk.Button(self.book_frame, text="All Books", font=('Arial', 14), width=15,
                                          command=lambda: TreeViewLoader.load_books_into_treeview(self.treeview, 0))
        self.Lend_button = tk.Button(self.book_frame, text="Lended Books", font=('Arial', 14), width=15,
                                     command=lambda: TreeViewLoader.load_books_into_treeview(self.treeview, 2))
        self.by_category = tk.Button(self.book_frame, text="By Category", font=('Arial', 14), width=15,
                                     command=lambda: TreeViewLoader.load_books_into_treeview(self.treeview, 3))

        # Place filter buttons in a centered row
        self.Available_button.grid(row=2, column=0, pady=10, padx=5)
        self.All_Books_button.grid(row=2, column=1, pady=10, padx=5)
        self.Lend_button.grid(row=2, column=2, pady=10, padx=5)
        self.by_category.grid(row=2, column=3, pady=10, padx=5)

    def loan_book_widget(self):
        """
        Display the lend book widget.
        """
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
            columns=("Title", "Author", "Year", "Genre", "Copies", "is_loaned", "is_Available"),
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
        TreeViewLoader.load_books_into_treeview(self.treeview)

        # Place Treeview
        self.treeview.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

        # Bind selection event
        self.treeview.bind("<<TreeviewSelect>>",
                           lambda event: TreeViewLoader.on_treeview_select(event, self.treeview, self))
        self.selected_item = None  # Initialize selected item


        # Button to perform the lend action
        self.lend_button = tk.Button(self.book_frame, text="Lend!", font=('Arial', 16), width=10,
                                     command=lambda : LendBook.book_lending(self.selected_item,self.treeview,self.root))
        self.lend_button.grid(row=2, column=1, columnspan=2, pady=10)

    def return_book_widget(self):
        """
        Display the return book widget.
        """
        self.book_frame.destroy()
        self.book_frame = tk.Frame(self.menu_frame)
        self.book_frame.grid(row=4, column=0, columnspan=3, pady=20, padx=20)
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
            columns=("Title", "Author", "Year", "Genre", "Copies", "is_loaned", "is_Available"),
            show="headings",
            height=8  # Matches the height of the view_book table
        )


        # Reload updated data
        TreeViewLoader.load_books_into_treeview(self.treeview, 2)

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
        TreeViewLoader.load_books_into_treeview(self.treeview, 2)
        # Place Treeview
        self.treeview.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

        self.button_return_book = tk.Button(self.book_frame, text="Return Book", font=('Arial', 16), width=10,
                                            command=lambda: ReturnBook.book_returner(self.selected_item,self.treeview))
        # Place filter buttons in a centered row
        self.button_return_book.grid(row=2, column=1, columnspan=2, pady=10)

        # Bind selection event
        self.treeview.bind("<<TreeviewSelect>>",
                           lambda event: TreeViewLoader.on_treeview_select(event, self.treeview, self))
        self.selected_item = None  # Initialize selected item

    def popular_books_widget(self):
        """
        Display the most popular books in the library.
        """
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
        TreeViewLoader.load_books_into_treeview(self.treeview, 4)

        # Place Treeview
        self.treeview.grid(row=1, column=0, columnspan=4, pady=10, padx=10)


    @log_activity("logout")
    def logout_button_func(self,user):
        """
        Log out the user and return to the login screen.
        :param user: librarian
        """
        try:
            self.menu_frame.destroy()  # Destroy the current menu frame
            #logout - change the user is_connected to False.
            LibrarianManager.log_out_user(user)
            from login import Login  # Import the Login class
            Login(self.root)  # Pass the root window to the Login screen
        except ImportError:
            tk.messagebox.showerror(
                "Logout Failed",
                "There was an error loading the Login module. Please try again."
            )
        except AttributeError:
            tk.messagebox.showerror(
                "Logout Failed",
                "There was an error accessing the menu frame. Please try again."
            )
        except Exception:
            tk.messagebox.showerror(
                "Logout Failed",
                "An unexpected error occurred while logging out. Please try again."
            )
