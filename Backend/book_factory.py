from Backend.book import Book
from Backend.librarian_manager import LibrarianManager


class BookFactory:
    @staticmethod
    def create_book(title : str, author : str, genre : str, year, copies=1,is_lent : str ="No" ,lent_count = 0):
        """
        Create a new book object and add it to the book manager. Add all librarians as observers to the book.
        :param title:  The title of the book to create (str)
        :param author:  The author of the book to create (str)
        :param genre:  The genre of the book to create (str)
        :param year:  The year of the book to create (int)
        :param copies:  The number of copies of the book to create (int)
        :param is_lent:  The lent status of the book to create (str)
        :param lent_count:  The number of times the book has been lent (int)
        :return:  The created book object
        """
        b = Book(title, author, genre, year, copies, is_lent, lent_count)
        from Backend.book_manager import BookManager
        BookManager.books.append(b)
        librarians = LibrarianManager.get_librarians()
        for librarian in librarians:
            b.add_observer(librarian)
        return b
