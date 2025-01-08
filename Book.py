import csv
import os


class Book:

    def __init__(self, title, author, genre, year, copies=1, is_lend="No"): # need to add availability field
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        if not copies=="":
            self.copies = int(copies)
        else:
            self.copies=1
        self.is_lend = is_lend

    def remove(self):
        pass

    def update_book(self):
        pass

    def update_title(self,new_title):
        self.title = new_title

    def update_author(self,new_author):
        self.author = new_author

    def update_year(self,new_year):
        self.year = new_year

    def update_genre(self,new_genre):
        self.genre = new_genre


    def is_available(self):
        return self.copies > 0


    def get_copies(self):
        return self.copies

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_genre(self):
        return self.genre

    def get_is_lend(self):
        return self.is_lend

    def get_year(self):
        return self.year

    def __eq__(self, other):
        if isinstance(other, Book):
            return (self.title == other.title and
                    self.author == other.author and
                    self.year == other.year and
                    self.genre == other.genre)
        return False