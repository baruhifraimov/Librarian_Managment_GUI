import unittest
from unittest.mock import patch, MagicMock
from collections import deque
from Backend.book import Book
from Backend.librarian_manager import LibrarianManager
from Backend.subject import Subject
from Exceptions.ExceptionBlankFieldsError import BlankFieldsError
from Exceptions.ExceptionBelowZeroExceeded import BelowZeroError
from Exceptions.ExceptionBorrowingLimitExceeded import BorrowingLimitExceededError
from Exceptions.ExceptionReturnLimitExceeded import ReturnLimitExceededError
from Exceptions.ExceptionUserAlreadyInList import UserAlreadyInListError

class TestBook(unittest.TestCase):
    def setUp(self):
        self.book = Book("Test Title", "Test Author", "Fiction", 2023, copies=5)
        LibrarianManager.load_users()
    def test_update_copies(self):
        self.book.update_copies(3)
        self.assertEqual(self.book.get_copies(), 8)
        self.assertEqual(self.book.get_watch_list_size(), 0)

    @patch("tkinter.messagebox.showinfo", lambda *args, **kwargs: None)  # Ignore the messagebox
    def test_add_to_watch_list_success(self):
        user = ("John Doe", "john@example.com", "1234567890")
        self.book.add_to_watch_list(user)
        self.assertIn(user, self.book.get_watch_list())

    @patch("tkinter.messagebox.showinfo", lambda *args, **kwargs: None)  # Ignore the messagebox
    def test_add_to_watch_list_user_already_in_list(self):
        user = ("John Doe", "john@example.com", "1234567890")
        self.book.add_to_watch_list(user)
        with self.assertRaises(UserAlreadyInListError):
            self.book.add_to_watch_list(user)

    def test_add_to_watch_list_blank_fields(self):
        user = ("", "john@example.com", "1234567890")
        with self.assertRaises(BlankFieldsError):
            self.book.add_to_watch_list(user)

    @patch("tkinter.messagebox.showerror", lambda *args, **kwargs: None)  # Ignore the messagebox
    def test_decrease_watch_list_success(self):
        user = ("John Doe", "john@example.com", "1234567890")
        self.book.add_to_watch_list(user)
        with patch("Backend.book.WaitingListManager.remove_waiting_list_csv") as mock_remove:
            self.book.decrease_watch_list()
            self.assertNotIn(user, self.book.get_watch_list())
            mock_remove.assert_called_once_with(user, self.book)

    def test_decrease_watch_list_below_zero(self):
        with self.assertRaises(BelowZeroError):
            self.book.decrease_watch_list()

    def test_return_action_success(self):
        self.book.borrow_action()
        self.book.return_action()
        self.assertEqual(self.book.get_lent_count(), 0)
        self.assertEqual(self.book.get_is_lent(), "No")

    def test_return_action_exceed_limit(self):
        with self.assertRaises(ReturnLimitExceededError):
            self.book.return_action()

    def test_borrow_action_success(self):
        self.book.borrow_action()
        self.assertEqual(self.book.get_lent_count(), 1)
        self.assertEqual(self.book.get_is_lent(), "No")

    def test_borrow_action_exceed_limit(self):
        self.book.lent_count = 5  # Simulate all copies lent out
        with self.assertRaises(BorrowingLimitExceededError):
            self.book.borrow_action()

    def test_is_available(self):
        self.book.lent_count = 4
        self.assertTrue(self.book.is_available())
        self.book.lent_count = 5
        self.assertFalse(self.book.is_available())

if __name__ == "__main__":
    unittest.main()