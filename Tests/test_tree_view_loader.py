import unittest
from unittest.mock import MagicMock, patch
from Backend.tree_view_loader import TreeViewLoader
from Backend.book_manager import BookManager
from Backend.book import Book


class TestTreeViewLoader(unittest.TestCase):
    def setUp(self):
        """
        Set up the test cases.
        """
        # Mock treeview
        self.treeview = MagicMock()
        self.treeview.get_children.return_value = ["item1", "item2"]

        # Mock books
        self.mock_book1 = MagicMock(spec=Book)
        self.mock_book1.get_title.return_value = "Title 1"
        self.mock_book1.get_author.return_value = "Author 1"
        self.mock_book1.get_year.return_value = 2023
        self.mock_book1.get_genre.return_value = "Fiction"
        self.mock_book1.get_copies.return_value = 3
        self.mock_book1.get_is_lent.return_value = "No"
        self.mock_book1.get_Available_books_num.return_value = 2
        self.mock_book1.get_lent_count.return_value = 1

        self.mock_book2 = MagicMock(spec=Book)
        self.mock_book2.get_title.return_value = "Title 2"
        self.mock_book2.get_author.return_value = "Author 2"
        self.mock_book2.get_year.return_value = 2021
        self.mock_book2.get_genre.return_value = "Non-fiction"
        self.mock_book2.get_copies.return_value = 5
        self.mock_book2.get_is_lent.return_value = "Yes"
        self.mock_book2.get_Available_books_num.return_value = 0
        self.mock_book2.get_lent_count.return_value = 5

        # Mock BookManager.books
        BookManager.books = [self.mock_book1, self.mock_book2]

    def test_load_all_books(self):
        """
        Test loading all books into the treeview.
        """
        # Call load_all_books
        TreeViewLoader.load_all_books(self.treeview)


        # Verify books are inserted
        self.treeview.insert.assert_any_call("", "end", values=(
            "Title 1", "Author 1", 2023, "Fiction", 3, "No", 2))
        self.treeview.insert.assert_any_call("", "end", values=(
            "Title 2", "Author 2", 2021, "Non-fiction", 5, "Yes", 0))

    def test_load_all_books_no_books(self):
        """
        Test loading all books into the treeview when no books are available.
        """
        # Set BookManager.books to an empty list
        BookManager.books = []

        # Verify ValueError is raised
        with self.assertRaises(ValueError):
            TreeViewLoader.load_all_books(self.treeview)

    def test_load_available_books(self):
        """
        Test loading available books into the treeview.
        """
        # Mock AvBooksItr to return only available books
        with patch("Backend.tree_view_loader.AvBooksItr", return_value=iter([self.mock_book1])):
            TreeViewLoader.load_available_books(self.treeview)

            # Verify books are inserted
            self.treeview.insert.assert_called_once_with("", "end", values=(
                "Title 1", "Author 1", 2023, "Fiction", 3, "No", 2))

    def test_load_available_books_no_books(self):
        """
        Test loading available books into the treeview when no available books are found.
        """
        # Mock AvBooksItr to return no available books
        with patch("Backend.tree_view_loader.AvBooksItr", return_value=iter([])):
            with self.assertRaises(ValueError):
                TreeViewLoader.load_available_books(self.treeview)

    def test_load_books_into_treeview_all_books(self):
        """
        Test loading all books into the treeview with filter=0.
        """
        # Call load_books_into_treeview with filter=0
        with patch.object(TreeViewLoader, "load_all_books") as mock_load_all_books:
            TreeViewLoader.load_books_into_treeview(self.treeview, filter=0)

            # Verify the correct method was called
            mock_load_all_books.assert_called_once_with(self.treeview)

    def test_load_books_into_treeview_invalid_filter(self):
        """
        Test loading books into the treeview with an invalid filter.
        """
        # Call load_books_into_treeview with an invalid filter
        with patch("tkinter.messagebox.showwarning") as mock_showwarning:
            TreeViewLoader.load_books_into_treeview(self.treeview, filter=99)

            # Verify warning message was shown
            mock_showwarning.assert_called_once_with("Invalid Filter", "No valid filter selected.")

    def test_refresh_treeview(self):
        """
        Test refreshing the treeview with a filter.
        """
        # Mock load_books_into_treeview
        with patch.object(TreeViewLoader, "load_books_into_treeview") as mock_load_books:
            TreeViewLoader.refresh_treeview(self.treeview, filter=1)

            # Verify load_books_into_treeview was called
            mock_load_books.assert_called_once_with(self.treeview, 1)


if __name__ == "__main__":
    unittest.main()