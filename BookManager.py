import csv
import os
from Book import Book
class BookManager:
    # This class manages the list of books
    books = []  # The list of books is now managed by the BookManager class

    @classmethod
    def add_book(self, title, author, genre, year, copies):

        # Check if copies is a valid number, if not set to 1
        if copies == '' or not copies.isdigit():
            copies = 1  # Default value if it's empty or invalid
        else:
            copies = int(copies)  # Convert copies to integer if it's a valid number

        # if the username is blank
        if title == "" or author == "" or genre == "" or year == "":
            return False

        # Check if the book already exists in the list
        existing_book = self.search_book(title, author, genre, year)
        if existing_book:
            existing_book.copies += int(copies)
            self.update_copies_in_csv(existing_book.title, existing_book.author, existing_book.genre,
                                      existing_book.year, existing_book.copies)
        else:
            book = Book(title, author, genre, year, copies)
            self.books.append(book)
            self.export_to_file(book)


    @classmethod
    def remove_book(self, title, author, genre, year):
        book_to_remove = self.search_book(title, author, genre, year)
        if book_to_remove:
            self.books.remove(book_to_remove)
            self.remove_book_in_csv(book_to_remove)
            return True
        return False


    @classmethod
    def remove_book_in_csv(self, book):
        with open('books.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                if row[0] == book.title and row[1] == book.author and row[4] == book.genre and row[5] == str(book.year):
                    row_to_remove = row
                    break
            with open('books.csv', 'w', newline="") as file:
                writer = csv.writer(file)
                for row in rows:
                    if row != row_to_remove:
                        writer.writerow(row)

    @classmethod
    def search_book(self, title, author, genre, year):
        for book in self.books:
            if book.title == title and book.author == author and book.genre == genre and book.year == year:
                return book
        return None # Return None if no book is found

    @classmethod
    def update_copies_in_csv(self, title, author, genre, year, copies):
        with open('books.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                if row[0] == title and row[1] == author and row[4] == genre and row[5] == str(year):
                    row[3] = int(copies)
                    break
            with open('books.csv', 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)

    @classmethod
    def export_to_file(self, book):
        if os.path.exists("books.csv"):  # Check if the file exists
            with open("books.csv", 'a+', newline="") as file:
                writer = csv.writer(file)
                if os.stat("books.csv").st_size == 0:  # Check if the file is empty
                    writer.writerow(["title", "author", "is_lend", "copies", "genre", "year"])
                writer.writerow([book.title, book.author, book.is_lend, book.copies, book.genre, book.year])
        else:
            # The file does not exist, create it
            with open('books.csv', 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "author", "is_lend", "copies", "genre", "year"])
                writer.writerow([book.title, book.author, book.is_lend, book.copies, book.genre, book.year])
