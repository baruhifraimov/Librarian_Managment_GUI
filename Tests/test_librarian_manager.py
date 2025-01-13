import os
import unittest
from unittest.mock import mock_open, patch, MagicMock
from Exceptions.ExceptionUserNotFound import UserNotFoundError
from Backend.librarian_manager import LibrarianManager
from Backend.librarian import Librarian


class TestLibrarianManager(unittest.TestCase):

    @patch("Backend.librarian_manager.open", new_callable=mock_open, read_data="id,name\n1,Test Librarian")
    @patch("Backend.librarian_manager.csv.reader")
    def test_search_in_user_csv(self, mock_csv_reader, mock_file):
        mock_csv_reader.return_value = [["1", "Test Librarian"]]
        result = LibrarianManager.search_in_user_csv("1", "Test Librarian")
        self.assertIsInstance(result, Librarian)
        self.assertEqual(result.get_user_messages(), "1")
        self.assertEqual(result.get_password(), "Test Librarian")

    @patch("Backend.librarian_manager.open", new_callable=mock_open)
    @patch("Backend.librarian_manager.csv.writer")
    def test_add_user_csv(self, mock_csv_writer, mock_file):
        LibrarianManager.add_user_csv("1,Test Librarian")
        mock_file.assert_called_once_with("librarians.csv", mode="a", newline="")
        mock_csv_writer.return_value.writerow.assert_called_once_with(["1", "Test Librarian"])

    @patch("Backend.librarian_manager.open", new_callable=mock_open, read_data="id,name\n1,Test Librarian")
    @patch("Backend.librarian_manager.csv.reader")
    def test_extracting_user(self, mock_csv_reader, mock_file):
        mock_csv_reader.return_value = [["1", "Test Librarian"]]
        result = LibrarianManager.extracting_user("1")
        self.assertIsInstance(result, Librarian)
        self.assertEqual(result.id, "1")
        self.assertEqual(result.name, "Test Librarian")

    @patch("Backend.librarian_manager.open", new_callable=mock_open, read_data="id,name\n1,Test Librarian\n2,Another Librarian")
    @patch("Backend.librarian_manager.csv.reader")
    def test_load_users(self, mock_csv_reader, mock_file):
        mock_csv_reader.return_value = [["1", "Test Librarian"], ["2", "Another Librarian"]]
        LibrarianManager.load_users()
        librarians = LibrarianManager.get_librarians()
        self.assertGreater(len(librarians), 0)
        self.assertEqual(len(librarians), 2)
        self.assertEqual(librarians[0].id, "1")
        self.assertEqual(librarians[0].name, "Test Librarian")