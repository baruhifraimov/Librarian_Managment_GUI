from Backend.librarian import User
from Backend.user_manager import users


class UserFactory:

    @classmethod
    def create_user(self, username, password, is_connected):
        new_user = User(username, password,str(is_connected))
        users.append(new_user)
        return new_user