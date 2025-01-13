from Backend.book import Book
from Backend.librarian_manager import LibrarianManager


class BookFactory:
    @staticmethod
    def create_book(title, author, genre, year, copies=1,is_lent="No",lent_count = 0):
        b = Book(title, author, genre, year, copies, is_lent, lent_count)
        from Backend.book_manager import BookManager
        BookManager.books.append(b)
        librarians = LibrarianManager.get_librarians()
        for librarian in librarians:
            b.add_observer(librarian)
        return b
