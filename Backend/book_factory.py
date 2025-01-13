from Backend.book import Book
from Backend.user_manager import UserManager


class BookFactory:
    @staticmethod
    def create_book(title, author, genre, year, copies=1,is_lent="No",lent_count = 0):
        b = Book(title, author, genre, year, copies, is_lent, lent_count)
        from Backend.book_manager import BookManager
        BookManager.books.append(b)
        librarians = UserManager.get_users()
        for librarian in librarians:
            b.add_observer(librarian)
        return b
