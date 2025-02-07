class AvBooksItr:

    def __init__(self, books):
        self.books = [book for book in books if book.is_available()]
        self.index = 0

    # initializing the object as an operator, return it as an iterator
    def __iter__(self):
        return self

    # Returns the current book and move the pointer to the next book
    def __next__(self):
        if self.index < len(self.books):
            val = self.index
            self.index += 1
            return self.books[val]
        else:
            raise StopIteration
