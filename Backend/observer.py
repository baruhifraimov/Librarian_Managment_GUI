from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self,user,book):
        """
        Handle an update from the observable.
        :param book: The book to update.
        :param user: The user to update.
        """
        pass