import csv
import os

from LogConfigurator.log_decorator import log_activity
from Exceptions.ExceptionUserNotFound import UserNotFoundError


librarians = []

class LibrarianManager:

    @staticmethod
    def get_librarians():
        """
        Method to get the list of librarians
        :return:  list of librarians
        """
        return librarians

    @classmethod
    def search_in_user_csv(self, username, password):
        """
        Method to search in the librarians csv file
        :param username: user username
        :param password: user password
        :return: Librarian object or Exception (UserNotFoundError)
        """
        with open('../csv_files/librarians_users.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                if row[0] == username and row[1] == password:
                    self.set_user_status_csv(username,0)
                    return self.extracting_user(username)
            raise UserNotFoundError(f"{username}")

    @classmethod
    def set_user_status_csv(self, username,filter):
        """
        Set user online status
        :param filter: 0 for online, 1 for offline
        :param username: user username
        :return: True or Exception (UserNotFoundError)
        """
        with open('../csv_files/librarians_users.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows: #start from row 1
                if row[0].lower() == username.lower():
                    match filter:
                        case 0:
                            row[2] = 'True'
                            self.update_user_csv(rows)
                            return True
                        case 1:
                            row[2] = 'False'
                            self.update_user_csv(rows)
                            return True
            raise UserNotFoundError(f"{username}")

    @staticmethod
    def update_user_csv(rows):
        """
        Update the librarians_users.csv file with the new rows
        :param rows:  list of rows
        :return:  None
        """
        with open('../csv_files/librarians_users.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    @classmethod
    def load_users(cls):
        """
        Syncs the books.csv file with the program
        :return: None
        """
        with open('../csv_files/librarians_users.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows[1:]:
                from Backend.librarian_factory import LibrarianFactory
                LibrarianFactory.create_librarian(row[0], row[1], str(row[2]))

    @classmethod
    def log_out_user(self,user):
        """
        Log out the user
        :param user:  user object
        :return:  None
        """
        user.deactivate_user()
        self.set_user_status_csv(user.username,1)

    @classmethod
    @log_activity("login")
    def extracting_user(self, username):
        """
        Extract the user from the librarians list by username
        :param username:  username
        :return:  Librarian object or Exception (UserNotFoundError)
        """
        for user in librarians:
            if str(user.get_username()).lower() == str(username).lower():
                return user
        raise UserNotFoundError(f"{username}") # Return None if no Librarian found

    @classmethod
    def extracting_online_user(self):
        """
        Extract the online user from the librarians list
        :return: Librarian object
        """
        for librarian in librarians:
            if librarian.get_is_connected() == "True":
                return librarian

    @classmethod
    def add_user_csv(self, user):
        """
        Append the username and password to the librarians_users.csv file.
        Create the file and add headers if it does not exist or is empty.
        :param user: user object that includes username and password.
        """
        try:
            file_path = "../csv_files/librarians_users.csv"

            # Ensure the parent directory exists
            if not os.path.exists(os.path.dirname(file_path)):
                raise FileNotFoundError(f"The directory for the file '{file_path}' does not exist.")

            # Open the file in append mode
            with open(file_path, 'a+', newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                # Write headers if the file is empty
                if os.stat(file_path).st_size == 0:  # Check if the file is empty
                    writer.writerow(["Username", "Password","Is_Connected"])

                # Write the new user's data
                writer.writerow([user.get_username(),user.get_password(),user.get_is_connected()])
                return True
        except Exception as e:
            # Raise a runtime error for unexpected issues
            raise RuntimeError(f"Failed to export user data to file: {e}")