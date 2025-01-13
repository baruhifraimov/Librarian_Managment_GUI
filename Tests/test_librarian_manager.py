import unittest
from unittest.mock import mock_open, patch

from Backend.encryption import Encryption
from Backend.librarian import Librarian
from Backend.librarian_factory import LibrarianFactory
from Backend.librarian_manager import LibrarianManager


class TestLibrarianManager(unittest.TestCase):
    def setUp(self):
        """Set up a LibrarianManager instance for testing."""
        self.manager = LibrarianManager()
        self.factory = LibrarianFactory()
        self.librarian = Librarian(1, 1)

    def test_add_librarian(self):
        """Test that a librarian is added successfully and also added as part of the librarians list."""
        test_lib = self.factory.create_librarian('one','two')
        self.assertIn(test_lib, self.manager.get_librarians(), "Librarian should be added to the manager.")

    def test_add_user_csv(self):
        """
        Test if the user is added to the csv file successfully and returns True
        """
        test = LibrarianFactory.create_librarian("test", "test")
        self.assertTrue(LibrarianManager.add_user_csv(test), True)

    def test_extracting_user(self):
        """
        Test if the user is extracted from the csv file successfully and is an instance of Librarian
        """
        self.assertIsInstance(LibrarianManager.extracting_user(self.librarian.get_username()),Librarian)

    def test_load_users(self):
        """
        Test if the users are loaded from the csv file
        """
        LibrarianManager.load_users()
        self.assertGreater(len(LibrarianManager.get_librarians()), 0)