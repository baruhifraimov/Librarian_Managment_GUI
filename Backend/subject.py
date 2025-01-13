from Backend.observer import Observer
from ConfigFiles.log_decorator import log_activity
from Exceptions.NoObserversError import NoObserversError

# Subject class that will be observed by the observers (Librarians)
# The subject will notify the observers about the book availability to the user
# The subject will contain a list of observers
# The subject will notify all observers in the list
# The subject will add and remove observers from the list
# The subject will notify the observers with the book availability information
# The subject will raise an exception if there are no observers to notify
class Subject:
    def __init__(self):
        self._observers = []


    def add_observer(self, observer : Observer):
        """
        Add an observer to the list.
        :param observer: The observer to add.
        """
        if observer not in self._observers:
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
