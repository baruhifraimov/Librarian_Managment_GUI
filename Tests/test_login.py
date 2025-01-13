import os
import unittest

from unittest.mock import MagicMock, patch
from Backend.librarian_manager import LibrarianManager
from Exceptions.ExceptionBlankFieldsError import BlankFieldsError
from Exceptions.ExceptionUserNotFound import UserNotFoundError
from GUI.login import Login

class TestLogin(unittest.TestCase):
    def setUp(self):
        # Create a mocking instance object to pass to the Login class
        # to mock the root tkinter instance
        self.root = MagicMock()
        # Create an instance of Login with the root
        self.login_instance = Login(self.root)
        LibrarianManager.load_users()

    @patch("tkinter.messagebox.showinfo", lambda *args, **kwargs: None)  # Ignore the messagebox
    def test_login_success(self):
        """
        Test if the login is successful with the correct credentials
        """
        self.assertTrue(Login.login_verifier(self.login_instance,"1","1"))

    def test_login_verifier_blank(self):
        """
        Test if the login raising BlankFieldsError with blank credentials
        """
        login_instance = Login(self.root)
        self.assertRaises(BlankFieldsError, Login.login_verifier,self,"","")

    def tst_login_verifier_blank_password(self):
        """
        Test if the login raising BlankFieldsError with blank password credentials
        """
        login_instance = Login(self.root)
        self.assertRaises(BlankFieldsError, Login.login_verifier,self,"username","")

    def tst_login_verifier_blank_username(self):
        """
        Test if the login raising BlankFieldsError with blank username credentials
        """
        login_instance = Login(self.root)
        self.assertRaises(BlankFieldsError, Login.login_verifier,self,"","password")

    # we send an exist user to see that only error will be cant reach the file)
    def test_login_verifier_path_not_found(self):
        """
        Test if the login raising FileNotFoundError with non existing file
        """
        # Mock the behavior of os.path.exists
        original_exists = os.path.exists
        os.path.exists = lambda x: False  # Simulate file not existing

        self.assertRaises(FileNotFoundError, Login.login_verifier, self, "1", "1")

        # Restore original os.path.exists
        os.path.exists = original_exists

    def test_login_verifier_user_not_found(self):
        """
        Test if the login raising UserNotFoundError with non existing user in the file
        """
        # Mock the behavior of os.path.exists
        self.assertRaises(UserNotFoundError, Login.login_verifier, self, "amosi", "amosi")
        # Restore original os.path.exists



if __name__ == "__main__":
    unittest.main()