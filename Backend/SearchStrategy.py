from abc import ABC, abstractmethod
from Backend.BookManager import BookManager


class SearchStrategy:
    class SearchStrategy(ABC):
        @abstractmethod
        def search(self, books, query) -> BookManager:
            pass


class StrategySearchByTitle(SearchStrategy):
    @classmethod
    def search(self, query):
        return [book for book in BookManager.books if query.lower() in book.get_title().lower()]

class StrategySearchByAuthor(SearchStrategy):
    @classmethod
    def search(self, query):
        return [book for book in BookManager.books if query.lower() in book.get_author().lower()]

class StrategySearchByGenre(SearchStrategy):
    @classmethod
    def search(self, query):
        return [book for book in BookManager.books if query.lower() in book.get_genre().lower()]

class StrategySearchByYear(SearchStrategy):
    @classmethod
    def search(self, query):
        return [book for book in BookManager.books if query.lower() in book.get_year().lower()]