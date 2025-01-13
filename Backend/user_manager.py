import csv
from unittest import case

from Backend.encryption import Encryption
from Backend.librarian import User
from ConfigFiles.log_decorator import log_activity
from Exceptions.ExceptionUserNotFound import UserNotFoundError

users = []

class UserManager:

    @staticmethod
    def get_users():
        return User.users

    @classmethod
    def search_in_user_csv(self, username, password) -> User:
        """
        Method to search in the users csv file
        :param username: user username
        :param password: user password
        :return: User object or Exception (UserNotFoundError)
        """
        password = Encryption.encrypt_password(password)
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
                from Backend.user_factory import UserFactory
                UserFactory.create_user(row[0], row[1],str(row[2]))

    @classmethod
    def log_out_user(self,user):
        user.deactivate_user()
        self.set_user_status_csv(user.username,1)

    @classmethod
    @log_activity("login")
    def extracting_user(self, username):
        for user in User.users:
            if user.get_username().lower() == username.lower():
                return user
        raise UserNotFoundError(f"{username}") # Return None if no User found

    @classmethod
    def extracting_online_user(self):
        for user in User.users:
            if user.get_is_connected() == "True":
                return user