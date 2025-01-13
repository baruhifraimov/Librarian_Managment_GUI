from Backend.librarian import Librarian
from Backend.librarian_manager import librarians


class LibrarianFactory:

    @classmethod
    def create_librarian(self, username, password, is_connected="False"):
        """
        Create a librarian object and add it to the librarians list in the librarian_manager
        :param username:  librarian username
        :param password:  librarian password
        :param is_connected: indicator if the librarian is connected (live)
        :return:  Librarian object
        """
        new_librarian = Librarian(username, password, str(is_connected))
        librarians.append(new_librarian)
        return new_librarian