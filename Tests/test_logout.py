import unittest
from unittest.mock import MagicMock, patch
from Backend.librarian_manager import LibrarianManager

class TestLogOut(unittest.TestCase):
    def setUp(self):
        # Create a mock user object
        self.user = MagicMock()
        self.user.username = "test_user"

    @patch.object(LibrarianManager, "set_user_status_csv")  # Mock set_user_status_csv
    def test_log_out_user(self, mock_set_user_status_csv):
        """
        Test that the log_out_user method calls the deactivate_user method on the user object and calls set_user_status_csv
        :param mock_set_user_status_csv:  Mocked set_user_status_csv method from LibrarianManager
        """
        # Call the logout method
        LibrarianManager.log_out_user(self.user)

        # Assert deactivate_user was called on the user
        self.user.deactivate_user.assert_called_once()

        # Assert set_user_status_csv was called with the correct arguments
        #the current username and 1 to change is_available to false.
        mock_set_user_status_csv.assert_called_once_with(self.user.username, 1)


if __name__ == "__main__":
    unittest.main()