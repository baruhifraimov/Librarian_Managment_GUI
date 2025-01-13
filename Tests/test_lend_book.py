import unittest
from unittest.mock import MagicMock, patch
from Backend.book_manager import BookManager
from Backend.waiting_list_manager import WaitingListManager
from Backend.lend_book import LendBook
import tkinter as tk


class TestBookManagerAndWaitingList(unittest.TestCase):

    def setUp(self):
        # Mock book object
        self.book = MagicMock()
        self.book.get_title.return_value = "Mock Book"
        self.book.get_author.return_value = "Mock Author"
        self.book.get_year.return_value = "2025"
        self.book.get_genre.return_value = "Fiction"
        self.book.get_is_lent.return_value = "No"
        self.book.get_copies.return_value = 5
        self.book.get_lent_count.return_value = 2

        # Mock file interactions
        self.mock_csv_data = [
            ["Mock Book", "Mock Author", "No", "5", "Fiction", "2025", "3"]
        ]

        self.popup = MagicMock()  # Mock popup window

    @patch("builtins.open")
    @patch("csv.reader")
    @patch("csv.writer")
    def test_update_in_csv(self, mock_writer, mock_reader, mock_open):
        # Setup mocks
        mock_reader.return_value = self.mock_csv_data
        mock_writer.return_value = MagicMock()

        # Call method with filter 0
        BookManager.update_in_csv(self.book, 0)
        mock_writer.assert_called_once()

        # Check modifications to the data
        updated_row = self.mock_csv_data[0]
        self.assertEqual(updated_row[3], self.book.get_copies())  # Copies updated
        self.assertEqual(updated_row[6],
                         int(self.book.get_copies() - self.book.get_lent_count()))  # Available copies updated
        self.assertEqual(updated_row[2], self.book.get_is_lent())  # Lending status updated

    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.messagebox.showerror")
    @patch("Backend.waiting_list_manager.WaitingListManager.update_waiting_list_csv")  # Mock the method here
    def test_add_to_waiting_list(self, mock_update_csv, mock_error, mock_info):
        # Call method with valid input
        WaitingListManager.add_to_waiting_list(self.popup, self.book, "John Doe", "1234567890", "john.doe@example.com")

        # Assert the waiting list is updated
        self.book.add_to_watch_list.assert_called_once()
        mock_update_csv.assert_called_once_with(self.book, ["John Doe", "john.doe@example.com", "1234567890"])
        self.popup.destroy.assert_called_once()

    def tearDown(self):
        pass  # Cleanup resources if necessary


if __name__ == "__main__":
    unittest.main()