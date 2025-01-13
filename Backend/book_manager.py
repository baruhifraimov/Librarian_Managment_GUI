import csv
import os
import tkinter as tk
from tkinter import messagebox
from ConfigFiles.log_decorator import log_activity
from Exceptions.ExceptionBlankFieldsError import BlankFieldsError
from Exceptions.ExceptionBookNotFound404 import BookNotFound404Error
from Exceptions.ExceptionWatchedBookRemovalError import WatchedBookRemovalError
from Exceptions.RecordNotFoundError import RecordNotFoundError
from Backend.book_factory import BookFactory


class BookManager:
    # This class manages the list of books
    books = []  # The list of books is now managed by the BookManager class

    @classmethod
    @log_activity("book added")
    def add_book(self, title, author, genre, year, copies):
        """
        Adds a book to the list of books and exports it to the books.csv
        file if it doesn't already exist in the list of books or the file itself
        :param title: The title of the book
        :param author: The author of the book
        :param genre: The genre of the book
        :param year: The year the book was published
        :param copies: The number of copies of the book
        :return: None
        """

        # Check if copies is a valid number, if not set to 1
        if copies == '' or not copies.isdigit():
            copies = 1  # Default value if it's empty or invalid
        else:
            copies = int(copies)  # Convert copies to integer if it's a valid number

        # if the book fields are blank
        if title == "" or author == "" or genre == "" or year == "":
            raise BlankFieldsError

        #check if year is a number
        for a in year:
            if not a.isdigit():
                raise ValueError


        # Check if the book already exists in the list
        try:
            existing_book = self.extracting_book(title, author, genre, year)
            existing_book.update_copies(int(copies))
            self.update_in_csv(existing_book,0)
        except BookNotFound404Error:
            book = BookFactory.create_book(title, author, genre, year, copies)
            self.export_to_file(book)


    @classmethod
    @log_activity("book removed")
    def remove_book(self, title, author, genre, year):
        """
        Removes a book from the list of books and exports the updated list to the books.csv file
        if it exists in the list of books and the file itself and if it's not
        borrowed by any user or in the watch list of any user or if the fields are blank
        :param title:  The title of the book
        :param author:  The author of the book
        :param genre:  The genre of the book
        :param year:  The year the book was published
        :return:  True if the book was removed successfully
        """
        if title == "" or author == "" or genre == "" or year == "":
            raise BlankFieldsError
        book_to_remove = self.extracting_book(title, author, genre, year)
        if book_to_remove is None:
                raise BookNotFound404Error
        if book_to_remove.get_watch_list_size() > 0:
                raise WatchedBookRemovalError
        # check if the book is still borrowed, raise exception


        else:
            self.books.remove(book_to_remove)
            self.remove_book_in_csv(book_to_remove)
            return True


    @classmethod
    def remove_book_in_csv(cls, book):
        """
        Removes a book from the books.csv file if it exists in the file
        and if it's not borrowed by any user or in the watch list of any user
        :param book: The book to remove
        :return: None
        """
        try:
            # Read the CSV file
            with open('../csv_files/books.csv', 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)

                # Search for the book to remove
                row_to_remove = None
                for row in rows:
                    if row[0] == book.title and row[1] == book.author and row[4] == book.genre and row[5] == str(
                            book.year):
                        row_to_remove = row
                        break

                if row_to_remove is None:
                    tk.messagebox.showinfo(
                        title="404",
                        message=f"The book '{book.title}' by {book.author} was not found"
                    )

            # Write back the updated rows
            with open('../csv_files/books.csv', 'w', newline="") as file:
                writer = csv.writer(file)
                for row in rows:
                    if row != row_to_remove:
                        writer.writerow(row)

        except FileNotFoundError as fnf_error:
            tk.messagebox.showinfo(
                title="404",
                message="FILE NOT FOUND"
            )

    @classmethod
    # @log_activity("Extracting Book")
    def extracting_book(self, title, author, genre, year):
        """
        Extracts a book from the list of books based on the title, author, genre, and year
        :param title:  The title of the book
        :param author:  The author of the book
        :param genre:  The genre of the book
        :param year:  The year the book was published
        :return:  The book if found, otherwise raises a BookNotFound404Error exception
        """
        for book in self.books:
            if book.get_title() == title and book.get_author() == author and book.get_genre() == genre and str(book.get_year()) == str(year):
                return book
        raise BookNotFound404Error(title, author, genre, year) # Return None if no book is found

    @classmethod
    def update_in_csv(self, book,filter):
        with open('../csv_files/books.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                if row[0] == book.get_title() and row[1] == book.get_author() and row[4] == book.get_genre() and str(row[5]) == str(book.get_year()):
                    match(filter):
                        case 0:
                            row[3] = book.get_copies()
                            row[6] = int(book.get_copies())- int(book.get_lent_count())
                            row[2] = book.get_is_lent()
                            break
                        case 1: #change in copies
                            if book:
                                row[6] = book.get_copies()- book.get_lent_count()
                                row[2] = book.get_is_lent()
                            else:
                                raise RecordNotFoundError(
                                    f"No record found for title='{book.get_title()}', author='{book.get_author()}', genre='{book.get_genre()}', year='{book.get_year()}'."
                                )

            with open('../csv_files/books.csv', 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)

    @classmethod
    def load_books(self):
        """
        Syncs the books.csv file with the program
        :return: None
        """
        with open('../csv_files/books.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows[1:]:
                BookFactory.create_book(row[0], row[1], row[4], row[5], row[3], row[2],int(row[3])-int(row[6]))


    @classmethod
    def load_watch_list(cls):
        """
        Syncs watch list for each book according to waiting_list.csv
        :return: None
        """
        try:
            # check if the file exists
            with open('../csv_files/waiting_list.csv', 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)

                # if the file is empty or has just 1 line.
                if len(rows) <= 1:
                    print("The waiting_list.csv file is empty or contains no entries.")
                    return

                #loop over the lines except the first one
                for row in rows[1:]:
                    try:
                        #check if the row contains all excpected rows
                        if len(row) < 7:
                            print(f"Skipping incomplete row: {row}")
                            continue

                        b = BookManager.extracting_book(row[3], row[4], row[5], row[6])
                        user = [row[0], row[1], row[2]]
                        b.get_watch_list().append(user)

                    except BookNotFound404Error:
                        # אם הספר לא נמצא, פשוט דלג לשורה הבאה
                        print(f"Book not found for row: {row}")
                        continue

        except FileNotFoundError:
            print("Error: The waiting_list.csv file does not exist.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


    @classmethod
    def export_to_file(self, book):
        """
        Appending/Rewrites new book information to the books.csv file
        :param book: The book you want to export
        :return: None
        """
        if os.path.exists("../csv_files/books.csv"):  # Check if the file exists
            with open("../csv_files/books.csv", 'a+', newline="") as file:
                writer = csv.writer(file)
                if os.stat("../csv_files/books.csv").st_size == 0:  # Check if the file is empty
                    writer.writerow(["title", "author", "is_lent", "copies", "genre", "year","Available_copies"])
                writer.writerow([book.get_title(), book.get_author(), book.get_is_lent(), book.get_copies(), book.get_genre(), book.get_year(), book.get_copies()- book.get_lent_count()])
        else:
            # The file does not exist, create it
            with open('../csv_files/books.csv', 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "author", "is_lent", "copies", "genre", "year", "Available_copies"])
                writer.writerow([book.get_title(), book.get_author(), book.get_is_lend(), book.get_copies(), book.get_genre(), book.get_year(), book.get_copies()- book.get_lent_count()])