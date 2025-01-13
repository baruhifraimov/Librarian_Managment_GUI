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
from ConfigFiles.log_decorator import log_activity
from Exceptions.NoObserversError import NoObserversError


class Book(Subject):

    def __init__(self, title, author, genre, year, copies=1, is_lent="No",lent_count = 0): # need to add availability field
        super().__init__()
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

    @log_activity("user added to watch list")
    def add_to_watch_list(self,user):
        # user[0] - full name
        # user[1] - email
        # user[2] - phone no.
        if user[0] and user[1] and user[2]:
        # Perform logic to add borrower to waiting list
            if any(char.isdigit() for char in user[0]):
                raise ValueError("Name must not contain digits")
            if user in self.watch_list:
                raise UserAlreadyInListError
            else:
                self.watch_list.append(user)
        else:
            raise BlankFieldsError()

    @log_activity("user removed from watch list")
    def decrease_watch_list(self):
        if len(self.watch_list) > 0:

            user = self.watch_list.popleft()
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
        if self.lent_count > 0:
            self.lent_count -=1
            self.is_lent = "No"
            if self.get_watch_list_size()>0:
                self.decrease_watch_list()
        else:
            raise ReturnLimitExceededError()

    @log_activity("book borrowed")
    def borrow_action(self):
        if self.copies > self.lent_count:
            self.lent_count += 1
            if self.lent_count == self.copies:
                self.is_lent = "Yes"
            else:
                self.is_lent = "No"
        else:
            raise BorrowingLimitExceededError(self.copies)

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