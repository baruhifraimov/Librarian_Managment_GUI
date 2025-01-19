import tkinter as tk
from curses.ascii import isdigit
from tkinter import messagebox
from collections import deque

from Backend.waiting_list_manager import WaitingListManager
from Backend.subject import Subject
from Exceptions.ExceptionBelowZeroExceeded import BelowZeroError
from Exceptions.ExceptionBlankFieldsError import BlankFieldsError
from Exceptions.ExceptionBorrowingLimitExceeded import BorrowingLimitExceededError
from Exceptions.ExceptionReturnLimitExceeded import ReturnLimitExceededError
from Exceptions.ExceptionUserAlreadyInList import UserAlreadyInListError
from LogConfigurator.log_decorator import log_activity
from Exceptions.ExceptionNoObserversError import NoObserversError


class Book(Subject):

    def __init__(self, title, author, genre, year, copies=1, is_lent="No",lent_count = 0): # need to add availability field
        super().__init__()
        self.__title = title
        self.__author = author
        self.__year = year
        self.__genre = genre
        self.__watch_list = deque()
        # if available change to "No" else change to "Yes"
        self.__is_lent = is_lent

        # number of borrowed book, lent_count <= copies
        self.__lent_count = lent_count

        # if copies is not given, default is 1
        if not copies=="":
            self.__copies = int(copies)
        else:
            self.__copies=1
        #When syncing, make sure to fix kid mistakes
        if int(self.__lent_count) == int(self.__copies):
            self.__is_lent = "Yes"
        else:
            self.__is_lent = "No"


    def update_copies(self,num):
        self.__copies += num
        self.__is_lent = "No"

        # Clear watchlist with the size of copies (num)
        while self.get_watch_list_size()>0 and num>0:
            self.decrease_watch_list()
            num -= 1

    def get_available_books_num(self):
        return self.__copies - self.__lent_count

    def get_watch_list_size(self):
        return len(self.__watch_list)

    def get_watch_list(self):
        return self.__watch_list

    @log_activity("user added to watch list")
    def add_to_watch_list(self,user):
        # user[0] - full name
        # user[1] - email
        # user[2] - phone no.
        if user[0] and user[1] and user[2]:
        # Perform logic to add borrower to waiting list
            if any(char.isdigit() for char in user[0]):
                raise ValueError("Name must not contain digits")
            if user in self.__watch_list:
                raise UserAlreadyInListError
            if not any(char.isdigit() for char in user[2]):
                raise ValueError("Phone only contain digits")
            else:
                self.__watch_list.append(user)
        else:
            raise BlankFieldsError()

    @log_activity("user removed from watch list")
    def decrease_watch_list(self):
        if len(self.__watch_list) > 0:

            user = self.__watch_list.popleft()
            #Notifier.notify(user)
            try:
                self.notify_observers(user,self)
            except NoObserversError:
                tk.messagebox.showerror("INTERNAL ERROR","There are no Librarians in the library")
            WaitingListManager.remove_waiting_list_csv(user, self)
            self.borrow_action()
        else:
            raise BelowZeroError(self.get_watch_list_size())


    @log_activity("book returned")
    def return_action(self):
        """
        Return the book and decrease the lent count by 1 and remove the user from the watch list if the book is returned successfully
        :return:
        """
        if self.__lent_count > 0:
            self.__lent_count -=1
            self.__is_lent = "No"
            if self.get_watch_list_size()>0:
                self.decrease_watch_list()
        else:
            raise ReturnLimitExceededError()

    @log_activity("book borrowed")
    def borrow_action(self):
        """
        Borrow the book and add +1 to book lent count
        :return:  None
        """
        if self.__copies > self.__lent_count:
            self.__lent_count += 1
            if self.__lent_count == self.__copies:
                self.is_lent = "Yes"
            else:
                self.__is_lent = "No"
        else:
            raise BorrowingLimitExceededError(self.__copies)

    def update_genre(self,new_genre):
        self.__genre = new_genre

    def is_available(self):
        return self.__copies - self.__lent_count > 0

    def get_lent_count(self):
        return self.__lent_count

    def get_copies(self):
        return self.__copies

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_genre(self):
        return self.__genre

    def get_is_lent(self):
        return self.__is_lent

    def get_year(self):
        return self.__year

    def __eq__(self, other):
        if isinstance(other, Book):
            return (self.__title == other.__title and
                    self.__author == other.__author and
                    self.__year == other.__year and
                    self.__genre == other.__genre)
        return False