import unittest
from unittest.mock import MagicMock, patch
from Backend.search_book import SearchBook
from Backend.search_strategy import StrategySearchByTitle, StrategySearchByAuthor, StrategySearchByGenre, StrategySearchByYear

class TestSearchBook(unittest.TestCase):
    def setUp(self):
        # Mock treeview
        self.treeview = MagicMock()

        # Mock search strategies
        self.mock_title_strategy = patch("Backend.search_strategy.StrategySearchByTitle.search").start()
        self.mock_author_strategy = patch("Backend.search_strategy.StrategySearchByAuthor.search").start()
        self.mock_genre_strategy = patch("Backend.search_strategy.StrategySearchByGenre.search").start()
        self.mock_year_strategy = patch("Backend.search_strategy.StrategySearchByYear.search").start()

        # Mock book objects
        self.mock_book = MagicMock()
        self.mock_book.get_title.return_value = "Test Title"
        self.mock_book.get_author.return_value = "Test Author"
        self.mock_book.get_year.return_value = 2023
        self.mock_book.get_genre.return_value = "Fiction"
        self.mock_book.get_copies.return_value = 5
        self.mock_book.get_is_lent.return_value = "No"

    def tearDown(self):
        patch.stopall()

    def test_search_by_title(self):
        # Mock search results
        self.mock_title_strategy.return_value = [self.mock_book]

        # Call perform_search with "Title" query
        SearchBook.perform_search("Title", "Test Query", self.treeview)

        # Verify strategy was called
        self.mock_title_strategy.assert_called_once_with("Test Query")

        # Verify treeview was updated with results
        self.treeview.delete.assert_called_once_with(*self.treeview.get_children())
        self.treeview.insert.assert_called_once_with(
            "", "end", values=("Test Title", "Test Author", 2023, "Fiction", 5, "No")
        )

    def test_search_by_author(self):
        # Mock search results
        self.mock_author_strategy.return_value = [self.mock_book]

        # Call perform_search with "Author" query
        SearchBook.perform_search("Author", "Test Query", self.treeview)

        # Verify strategy was called
        self.mock_author_strategy.assert_called_once_with("Test Query")

        # Verify treeview was updated with results
        self.treeview.delete.assert_called_once_with(*self.treeview.get_children())
        self.treeview.insert.assert_called_once_with(
            "", "end", values=("Test Title", "Test Author", 2023, "Fiction", 5, "No")
        )

    def test_no_results(self):
        # Mock no search results
        self.mock_title_strategy.return_value = []

        # Call perform_search with "Title" query
        SearchBook.perform_search("Title", "Test Query", self.treeview)

        # Verify strategy was called
        self.mock_title_strategy.assert_called_once_with("Test Query")

        # Verify treeview was cleared but not updated with any results
        self.treeview.delete.assert_called_once_with(*self.treeview.get_children())
        self.treeview.insert.assert_not_called()

    def test_search_with_invalid_query(self):
        # Call perform_search with an invalid query
        SearchBook.perform_search("Invalid", "Test Query", self.treeview)

        # Verify no strategy was called
        self.mock_title_strategy.assert_not_called()
        self.mock_author_strategy.assert_not_called()
        self.mock_genre_strategy.assert_not_called()
        self.mock_year_strategy.assert_not_called()

        # Verify treeview was cleared
        self.treeview.delete.assert_called_once_with(*self.treeview.get_children())
        self.treeview.insert.assert_not_called()

    def test_search_with_none_strategy(self):
        # Call perform_search with a valid query but None strategy
        SearchBook.perform_search("Title", None, self.treeview)

        # Verify no strategy was called
        self.mock_title_strategy.assert_not_called()
        self.mock_author_strategy.assert_not_called()
        self.mock_genre_strategy.assert_not_called()
        self.mock_year_strategy.assert_not_called()

        # Verify treeview was cleared
        self.treeview.delete.assert_called_once_with(*self.treeview.get_children())
        self.treeview.insert.assert_not_called()
if __name__ == "__main__":
    unittest.main()