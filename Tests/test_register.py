import unittest
from unittest.mock import patch, MagicMock

from Backend.librarian_manager import LibrarianManager
from GUI.register import Register
from Exceptions.ExceptionBlankFieldsError import BlankFieldsError


class TestRegisterVerifier(unittest.TestCase):

    def setUp(self):
    # Mock the tkinter root instance
            self.root = MagicMock()
            # Create an instance of Register with the mocked root
            self.register_instance = Register(self.root)
            # Mock user loading to avoid dependency on actual files
            LibrarianManager.load_users = MagicMock()

    @patch("tkinter.messagebox.showinfo", lambda *args, **kwargs: None)  # Ignore the messagebox
    @patch('Backend.encryption.Encryption.encrypt_password', return_value="encrypted_password")
    @patch('GUI.register.Register.search_user_in_csv', return_value=False)
    @patch('Backend.user_manager.LibrarianManager.add_user_csv')
    @patch('GUI.register.Register.switch_to_login')  # Mock switch_to_login to avoid the 'login' import issue
    def test_register_verifier_file_not_found(self, mock_add_user_csv, mock_search_user, mock_encrypt_password,
                                       mock_switch_to_login):


        mock_add_user_csv.side_effect = FileNotFoundError("The directory for the file '../csv_files/librarians_users.csv' does not exist.")

    def test_register_verifier_blank_username(self):
        """
        Test if the register_verifier method raises BlankFieldsError when username is blank
        :return:  None
        """
        # Arrange
        username = ""
        password = "password123"

        # Act & Assert
        with self.assertRaises(BlankFieldsError) as context:
            self.register_instance.register_verifier(username, password)
        self.assertEqual(str(context.exception), "Invalid Username: Username is blank.")

    def test_register_verifier_blank_password(self):
        """
        Test if the register_verifier method raises BlankFieldsError when password is blank
        :return:  None
        """
        # Arrange
        username = "testuser"
        password = ""

        # Act & Assert
        with self.assertRaises(BlankFieldsError) as context:
            self.register_instance.register_verifier(username, password)
        self.assertEqual(str(context.exception), "Invalid Password: Password is blank.")

    @patch("tkinter.messagebox.showinfo", lambda *args, **kwargs: None)  # Ignore the messagebox
    @patch("Backend.user_factory.LibrarianFactory.create_user")
    @patch("Backend.encryption.Encryption.encrypt_password", return_value="encrypted_password")
    @patch("GUI.register.Register.search_user_in_csv", return_value=False)
    @patch("Backend.user_manager.LibrarianManager.add_user_csv")
    @patch("GUI.register.Register.switch_to_login")  # Mock switch_to_login to avoid the 'login' import issue
    def test_register_verifier_success(self, mock_switch_to_login, mock_add_user_csv, mock_search_user,
                                       mock_encrypt_password, mock_create_user):
        """
        Test if the register_verifier method works as expected
        :param mock_switch_to_login:  Mock the switch_to_login method
        :param mock_add_user_csv:  Mock the add_user_csv method
        :param mock_search_user:  Mock the search_user_in_csv method
        :param mock_encrypt_password: Mock the encrypt_password method
        :param mock_create_user: Mock the create_user method
        :return:  None
        """
        # Arrange
        username = "admin"
        password = "admin"
        mock_user = MagicMock()  # Mock the user object returned by LibrarianFactory.create_user
        mock_create_user.return_value = mock_user

        # Act
        self.register_instance.register_verifier(username, password)

        # Assert
        mock_encrypt_password.assert_called_once_with(password)
        mock_search_user.assert_called_once_with(username)
        mock_create_user.assert_called_once_with(username, "encrypted_password")
        mock_add_user_csv.assert_called_once_with(mock_user)
        mock_switch_to_login.assert_called_once()  # Ensure switch_to_login was called
