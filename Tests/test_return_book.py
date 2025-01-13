import unittest
from unittest.mock import MagicMock, patch
from Backend.book_manager import BookManager
from Backend.tree_view_loader import TreeViewLoader
from Backend.return_book import ReturnBook
import tkinter as tk
from tkinter import ttk

from Exceptions.ExceptionBookNotFound404 import BookNotFound404Error
from Exceptions.ExceptionReturnLimitExceeded import ReturnLimitExceededError


class TestReturnBook(unittest.TestCase):

    def setUp(self):
        # Mock book object
        self.book = MagicMock()
        self.book.get_title.return_value = "Mock Book"
        self.book.get_author.return_value = "Mock Author"
        self.book.get_year.return_value = "2025"
        self.book.get_genre.return_value = "Fiction"

        # Mock BookManager
        BookManager.extracting_book = MagicMock(return_value=self.book)
        BookManager.update_in_csv = MagicMock()

        # Mock TreeViewLoader
        TreeViewLoader.refresh_treeview = MagicMock()

        # Tkinter setup
        self.root = tk.Tk()
        self.treeview = ttk.Treeview(self.root)

        self.selected_item = {
            'values': ["Mock Book", "Mock Author", "2025", "Fiction"]
        }

    def tearDown(self):
        self.root.destroy()

    @patch("tkinter.messagebox.showinfo")
    def test_successful_book_return(self, mock_messagebox):
        # Test successful book return
        self.book.return_action = MagicMock()

        ReturnBook.book_returner(self.selected_item, self.treeview)

        self.book.return_action.assert_called_once()
        BookManager.update_in_csv.assert_called_once_with(self.book, 1)
        TreeViewLoader.refresh_treeview.assert_called_once_with(self.treeview, 2)
        mock_messagebox.assert_called_with("Success", "Book 'Mock Book' has been returned!")

    @patch("tkinter.messagebox.showinfo")
    def test_return_limit_exceeded(self, mock_messagebox):
        # Test when return limit is exceeded
        self.book.return_action = MagicMock(side_effect=ReturnLimitExceededError)

        ReturnBook.book_returner(self.selected_item, self.treeview)

        self.book.return_action.assert_called_once()
        mock_messagebox.assert_called_with("Failed", "Selected book: 'Mock Book' cannot be returned!\n")

    @patch("tkinter.messagebox.showinfo")
    def test_book_not_found(self, mock_messagebox):
        # Test when the book is not found
        BookManager.extracting_book = MagicMock(side_effect=BookNotFound404Error(self.book.get_title(),self.book.get_author(),self.book.get_genre(),self.book.get_year()))

        ReturnBook.book_returner(self.selected_item, self.treeview)

        BookManager.extracting_book.assert_called_once_with(
            "Mock Book", "Mock Author", "Fiction", "2025"
        )
        mock_messagebox.assert_called_with(
            "Failed", "Selected book: 'Mock Book'  not found in the book list!"
        )

    @patch("tkinter.messagebox.showinfo")
    def test_no_book_selected(self, mock_messagebox):
        # Test when no book is selected
        ReturnBook.book_returner(None, self.treeview)

        mock_messagebox.assert_called_with("Failed", "No book Selected!")


if __name__ == "__main__":
    unittest.main()
