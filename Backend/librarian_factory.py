from Backend.librarian import Librarian
from Backend.librarian_manager import librarians


class LibrarianFactory:

    @classmethod
    def create_user(self, username, password, is_connected="False"):
        new_librarian = Librarian(username, password, str(is_connected))
        librarians.append(new_librarian)
        return new_librarian