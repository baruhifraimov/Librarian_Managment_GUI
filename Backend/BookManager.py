import csv
import os
import tkinter as tk
from tkinter import messagebox
from Backend.Book import Book
from ConfigFiles.LogDecorator import log_activity
from Exceptions.ExceptionBlankFieldsError import BlankFieldsError
from Exceptions.ExceptionBookNotFound404 import BookNotFound404
from Exceptions.ExceptionWatchedBookRemovalError import WatchedBookRemovalError
from Exceptions.RecordNotFoundError import RecordNotFoundError


class BookManager:
    # This class manages the list of books
    books = []  # The list of books is now managed by the BookManager class

    @classmethod
    @log_activity("book added")
    def add_book(self, title, author, genre, year, copies):

        # Check if copies is a valid number, if not set to 1
        if copies == '' or not copies.isdigit():
            copies = 1  # Default value if it's empty or invalid
        else:
            copies = int(copies)  # Convert copies to integer if it's a valid number

        # if the book fields are blank
        if title == "" or author == "" or genre == "" or year == "":
            raise BlankFieldsError

        # Check if the book already exists in the list
        try:
            existing_book = self.extracting_book(title, author, genre, year)
            existing_book.update_copies(int(copies))
            self.update_in_csv(existing_book,0)
        except BookNotFound404:
            book = Book(title, author, genre, year, copies)
            self.books.append(book)
            self.export_to_file(book)


    @classmethod
    @log_activity("book removed")
    def remove_book(self, title, author, genre, year):
        try:
            if title == "" or author == "" or genre == "" or year == "":
                raise BlankFieldsError
            book_to_remove = self.extracting_book(title, author, genre, year)
            # check if the book is still borrowed, raise exception
            if book_to_remove.get_watch_list_size() >0:
                raise WatchedBookRemovalError

            else:
                self.books.remove(book_to_remove)
                self.remove_book_in_csv(book_to_remove)
                return True

        except BookNotFound404:
            return False  # Indicate exception was handled

    @classmethod
    def remove_book_in_csv(cls, book):
        try:
            # Read the CSV file
            with open('../ConfigFiles/books.csv', 'r') as file:
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
            with open('../ConfigFiles/books.csv', 'w', newline="") as file:
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
        for book in self.books:
            if book.get_title() == title and book.get_author() == author and book.get_genre() == genre and str(book.get_year()) == str(year):
                return book
        raise BookNotFound404(title, author, genre, year) # Return None if no book is found

    @classmethod
    def update_in_csv(self, book,filter):
        with open('../ConfigFiles/books.csv', 'r') as file:
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

            with open('../ConfigFiles/books.csv', 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)

    @classmethod
    def load_books(self):
        """
        Syncs the books.csv file with the program
        :return: None
        """
        with open('../ConfigFiles/books.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows[1:]:
                # TODO add the feature that he knows the lent count for each book
                b = Book(row[0], row[1], row[4], row[5], row[3], row[2],int(row[3])-int(row[6]))
                BookManager.books.append(b)

    @classmethod
    def load_watch_list(cls):
        """
        Syncs watch list for each book according to waiting_list.csv
        :return: None
        """
        try:
            # בדיקה אם הקובץ קיים
            with open('../ConfigFiles/waiting_list.csv', 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)

                # אם הקובץ ריק או מכיל רק כותרת
                if len(rows) <= 1:
                    print("The waiting_list.csv file is empty or contains no entries.")
                    return

                # לולאה על השורות (למעט השורה הראשונה - כותרת)
                for row in rows[1:]:
                    try:
                        # בדוק אם השורה מכילה את כל העמודות הצפויות
                        if len(row) < 7:
                            print(f"Skipping incomplete row: {row}")
                            continue

                        b = BookManager.extracting_book(row[3], row[4], row[5], row[6])
                        user = [row[0], row[1], row[2]]
                        b.get_watch_list().append(user)

                    except BookNotFound404:
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
        if os.path.exists("../ConfigFiles/books.csv"):  # Check if the file exists
            with open("../ConfigFiles/books.csv", 'a+', newline="") as file:
                writer = csv.writer(file)
                if os.stat("../ConfigFiles/books.csv").st_size == 0:  # Check if the file is empty
                    writer.writerow(["title", "author", "is_lent", "copies", "genre", "year","Available_copies"])
                writer.writerow([book.get_title(), book.get_author(), book.get_is_lent(), book.get_copies(), book.get_genre(), book.get_year(), book.get_copies()- book.get_lent_count()])
        else:
            # The file does not exist, create it
            with open('../ConfigFiles/books.csv', 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "author", "is_lent", "copies", "genre", "year", "Available_copies"])
                writer.writerow([book.get_title(), book.get_author(), book.get_is_lend(), book.get_copies(), book.get_genre(), book.get_year(), book.get_copies()- book.get_lent_count()])