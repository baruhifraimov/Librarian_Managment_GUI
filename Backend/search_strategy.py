from abc import ABC, abstractmethod
from Backend.book_manager import BookManager
from LogConfigurator.log_decorator import search_log_activity


class SearchStrategy:
    class SearchStrategy(ABC):
        """
        Abstract class for search strategies to implement.
        """
        @abstractmethod
        def search(self, books, query) -> BookManager:
            pass


class StrategySearchByTitle(SearchStrategy):
    @classmethod
    @search_log_activity("name")
    def search(cls, query):
        """
        Search for books by title. Returns a list of books that match the query.
         If no books are found, raises a ValueError.
        :param query:  The query to search for.
        :return:  A list of books that match the query.
        """
        try:
            result = [book for book in BookManager.books if query.lower() in book.get_title().lower()]
            if not result:  # No books found
                raise ValueError(f"No books found with title containing '{query}'.")
            return result
        except Exception as e:
            raise e  # Re-raise the exception to be caught by the decorator

class StrategySearchByAuthor(SearchStrategy):
    @classmethod
    @search_log_activity("author")
    def search(cls, query):
        """
        Search for books by author. Returns a list of books that match the query.
        If no books are found, raises a ValueError.
        :param query:  The query to search for.
        :return:  A list of books that match the query.
        """
        try:
            result = [book for book in BookManager.books if query.lower() in book.get_author().lower()]
            if not result:  # No books found
                raise ValueError(f"No books found with author containing '{query}'.")
            return result
        except Exception as e:
            raise e  # Re-raise the exception to be caught by the decorator

class StrategySearchByGenre(SearchStrategy):
    @classmethod
    @search_log_activity("genre")
    def search(cls, query):
        """
        Search for books by genre. Returns a list of books that match the query.
        :param query:  The query to search for.
        :return:  A list of books that match the query.
        """
        try:
            result = [book for book in BookManager.books if query.lower() in book.get_genre().lower()]
            if not result:  # No books found
                raise ValueError(f"No books found with genre containing '{query}'.")
            return result
        except Exception as e:
            raise e  # Re-raise the exception to be caught by the decorator

class StrategySearchByYear(SearchStrategy):
    @classmethod
    @search_log_activity("year")
    def search(cls, query):
        """
        Search for books by year. Returns a list of books that match the query.
        :param query:  The query to search for.
        :return:  A list of books that match the query.
        """
        try:
            result = [book for book in BookManager.books if query.lower() in book.get_year().lower()]
            if not result:  # No books found
                raise ValueError(f"No books found with year '{query}'.")
            return result
        except Exception as e:
            raise e  # Re-raise the exception to be caught by the decorator