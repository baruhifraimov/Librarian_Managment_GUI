import csv
import os


class Book:

    #TODO need to initialize all the books.csv
    books = []


    def __init__(self,title,author,genre,year,copies=1,is_loaned='No'): # need to add availability field
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        if not copies=="":
            self.copies = copies
        else:
            self.copies=1
        self.is_loaned = is_loaned

        # checks if the book is already registered
        # uses equal and returns true or false, if true add else, not
        flag = False
        for book in Book.books:
            if self == book:
                flag = True
        if not flag:
            Book.books.append(self)



    def add(self,title,author,genre,year,copies):

        # Check if copies is a valid number, if not set to 1
        if copies == '' or not copies.isdigit():
            copies = 1  # Default value if it's empty or invalid
        else:
            copies = int(copies)  # Convert copies to integer if it's a valid number

        # if the username is blank
        if title == "" or author == "" or genre == "" or year == "":
            return False

        # the book does not exist
        if not self.search_book_in_csv(title, author, genre, year):
            book = Book(title, author, genre, year,copies)
            self.export_to_file(book)
            return True

        # the book object exists, need to extract and update it from the book list
        else:
            existing_book = self.find_book(Book.books,title, author, genre, year)
            if not existing_book is None:
                existing_book.copies += int(copies)
                #x = existing_book.copies
                self.update_copies_in_csv(existing_book.title, existing_book.author, existing_book.genre, existing_book.year,existing_book.copies)


    def find_book(self,books, title, author, genre, year):
        for book in books:
            if book.title == title and book.author == author and book.year == year and book.genre == genre :
                return book
        return None  # Return None if no book is found

    def update_copies_in_csv(self, title, author, genre, year, copies):
        with open('books.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                is_update = False
                if row[0] == title and row[1] == author and row[4] == genre and row[5] == str(year):
                    row[3] = str(copies)
                    is_update = True
                    break
            if is_update:
                with open('books.csv', 'w', newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)


    def export_to_file(self,book):
        if os.path.exists("books.csv"): # check if the file exists
            with open("books.csv", 'a+', newline="") as file:
                writer = csv.writer(file)
                if os.stat("books.csv").st_size == 0:  # check if the file is empty
                    writer.writerow(["title","author","is_loaned","copies","genre","year"])
                writer.writerow([book.title,book.author,book.is_loaned,book.copies,book.genre,book.year])
        else:
            # the file does not exist, so create it
            with open('books.csv','w',newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["title","author","is_loaned","copies","genre","year"])
                    writer.writerow([book.title, book.author, book.is_loaned, book.copies, book.genre, book.year])

    def search_book_in_csv(self,c_title,c_author,c_genre,c_year):
        """
        Return boolean in the CSV file where the copy is found
        :param c_author: Book compare author
        :param c_genre: Book compare genre
        :param c_year: Book compare year
        :param c_title: Book compare title
        :param self: Book
        :return: True if found in the CSV, False if not
        """
        with open('books.csv','r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                if self.compare_with_csv_row(c_title,c_author,c_genre,c_year,row):
                    return True
            else:
                return False

    def compare_with_csv_row(self,c_title,c_author,c_genre,c_year, row):
        """
        Compare the current book object with a row from a CSV file.
        Assumes the CSV row is in the format: title, author, is_loaned, copies, genre, year.
        """
        return (c_title == row[0] and
                c_author == row[1] and
                c_genre == row[4] and
                c_year == row[5])


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

    def get_year(self):
        return self.year

    def __eq__(self, other):
        if isinstance(other, Book):
            return (self.title == other.title and
                    self.author == other.author and
                    self.year == other.year and
                    self.genre == other.genre)
        return False