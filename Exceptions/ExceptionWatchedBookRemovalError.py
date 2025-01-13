class WatchedBookRemovalError(Exception):
    """Custom exception raised when Librarian is already in the watching list of the same book,
     Librarian is not allowed to watch the same item more than once."""
    def __init__(self):
        self.message = f"Attempted to remove a book that is being actively watched. This operation is not permitted while the book is on the watched list."
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return self.message  # Customize what gets printed