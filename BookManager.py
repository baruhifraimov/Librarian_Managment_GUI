import csv
import os
from Book import Book
from ExceptionWatchedBookRemovalError import WatchedBookRemovalError
from RecordNotFoundError import RecordNotFoundError


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

        # if the book fields are blank
        if title == "" or author == "" or genre == "" or year == "":
            return False

        # Check if the book already exists in the list
        existing_book = self.search_book(title, author, genre, year)
        if existing_book:
            existing_book.update_copies(int(copies))
            self.update_in_csv(existing_book,0)
            return True
        else:
            book = Book(title, author, genre, year, copies)
            self.books.append(book)
            self.export_to_file(book)
            return True


    @classmethod
    def remove_book(self, title, author, genre, year):
        book_to_remove = self.search_book(title, author, genre, year)
        if book_to_remove:
            # check if the book is still borrowed, raise exception
            if book_to_remove.get_watch_list_size() >0:
                raise WatchedBookRemovalError
            else:
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
    def update_in_csv(self, book,filter):
        # book = self.search_book(title, author, genre, year)
        with open('books.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                if row[0] == book.get_title() and row[1] == book.get_author() and row[4] == book.get_genre() and row[5] == book.get_year():
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

            with open('books.csv', 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)

    @classmethod
    def load_books(self):
        with open('books.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows[1:]:
                # TODO add the feature that he knows the lent count for each book
                b = Book(row[0], row[1], row[4], row[5], row[3], row[2],int(row[3])-int(row[6]))
                BookManager.books.append(b)

    @classmethod
    def load_watch_list(self):
        with open('waiting_list.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows[1:]:
                b=BookManager.search_book(row[3], row[4], row[5], row[6])
                user = [row[0],row[1],row[2]]
                b.get_watch_list().append(user)


    @classmethod
    def export_to_file(self, book):
        if os.path.exists("books.csv"):  # Check if the file exists
            with open("books.csv", 'a+', newline="") as file:
                writer = csv.writer(file)
                if os.stat("books.csv").st_size == 0:  # Check if the file is empty
                    writer.writerow(["title", "author", "is_lent", "copies", "genre", "year","Available_copies"])
                writer.writerow([book.get_title(), book.get_author(), book.get_is_lent(), book.get_copies(), book.get_genre(), book.get_year(), book.get_copies()- book.get_lent_count()])
        else:
            # The file does not exist, create it
            with open('books.csv', 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "author", "is_lent", "copies", "genre", "year", "Available_copies"])
                writer.writerow([book.get_title(), book.get_author(), book.get_is_lend(), book.get_copies(), book.get_genre(), book.get_year(), book.get_copies()- book.get_lent_count()])