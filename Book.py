class Book:

    books = {}

    def __init__(self,title,author,is_loaned,copies,genre,year): # need to add availability field
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.copies = copies
        self.is_loaned = is_loaned
        Book.books[title] = self

    def remove(self):
        pass

    def add(self):
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

    def get_year(self):
        return self.year




