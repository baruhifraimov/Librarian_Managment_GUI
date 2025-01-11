from collections import deque

from Backend.Notifier import Notifier
from Backend.WaitingListManager import WaitingListManager
from Exceptions.ExceptionBelowZeroExceeded import ExceptionBelowZero
from Exceptions.ExceptionBorrowingLimitExceeded import BorrowingLimitExceeded
from Exceptions.ExceptionReturnLimitExceeded import ReturnLimitExceeded
from Exceptions.ExceptionUserAlreadyInList import UserAlreadyInList


class Book:

    def __init__(self, title, author, genre, year, copies=1, is_lent="No",lent_count = 0): # need to add availability field
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        if not copies=="":
            self.copies = int(copies)
        else:
            self.copies=1

        # if available change to "No" else change to "Yes"
        self.is_lent = is_lent

        # number of borrowed book, lent_count <= copies
        self.lent_count = lent_count

        #When syncing, make sure to fix kid mistakes
        if int(self.lent_count) == int(self.copies):
            self.is_lent = "Yes"
        else:
            self.is_lent = "No"

        self.watch_list = deque()

    def update_copies(self,num):
        self.copies += num
        self.is_lent = "No"

        # TODO need to notify that the book available
        # Clear watchlist with the size of copies (num)
        while self.get_watch_list_size()>0 and num>0:
            self.decrease_watch_list()
            num -= 1

    def get_Available_books_num(self):
        return self.copies - self.lent_count

    def get_watch_list_size(self):
        return len(self.watch_list)

    def get_watch_list(self):
        return self.watch_list

    def add_to_watch_list(self,user):
        if user in self.watch_list:
            raise UserAlreadyInList
        else:
            self.watch_list.append(user)

    def decrease_watch_list(self):
        if len(self.watch_list) > 0:
            user = self.watch_list.pop()
            WaitingListManager.remove_watchlist_csv(user,self)
            Notifier.notify(user)
            self.borrow_action()
        else:
            raise ExceptionBelowZero(self.get_watch_list_size())

    def return_action(self):
        if self.lent_count > 0:
            self.lent_count -=1
            self.is_lent = "No"
            # if someone returned the book
            # the first guy in the queue gets the book
            # TODO need to notify that the book available
            if self.get_watch_list_size()>0:
                self.decrease_watch_list()
        else:
            raise ReturnLimitExceeded()

    def borrow_action(self):
        if self.copies > self.lent_count:
            self.lent_count += 1
            if self.lent_count == self.copies:
                self.is_lent = "Yes"
            else:
                self.is_lent = "No"
        else:
            raise BorrowingLimitExceeded(self.copies)

    def update_genre(self,new_genre):
        self.genre = new_genre

    def is_available(self):
        return self.copies - self.lent_count > 0

    def get_lent_count(self):
        return self.lent_count

    def get_copies(self):
        return self.copies

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_genre(self):
        return self.genre

    def get_is_lent(self):
        return self.is_lent

    def get_year(self):
        return self.year

    def __eq__(self, other):
        if isinstance(other, Book):
            return (self.title == other.title and
                    self.author == other.author and
                    self.year == other.year and
                    self.genre == other.genre)
        return False