from Backend.observer import Observer
from ConfigFiles.log_decorator import log_activity
from Exceptions.NoObserversError import NoObserversError


class Subject:


    def __init__(self):
        self._observers = []


    def add_observer(self, observer : Observer):
        """
        Add an observer to the list.
        :param observer: The observer to add.
        """
        self._observers.append(observer)

    def remove_observer(self, observer):
        """
        Remove an observer from the list.
        :param observer: The observer to remove.
        """
        self._observers.remove(observer)

    @log_activity("notification sent")
    def notify_observers(self,user,book):
        """
        Notify all observers with book availability information.
        :param book: The book to notify about.
        :param user: The user to notify.
        """
        if not self._observers:
            raise NoObserversError
        else:
            for observer in self._observers:
                observer.update(user,book)
