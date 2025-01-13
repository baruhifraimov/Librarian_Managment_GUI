class UserAlreadyInListError(Exception):
    """Custom exception raised when Librarian is already in the watching list of the same book,
     Librarian is not allowed to watch the same item more than once."""
    def __init__(self,message = f"User already in list."):
        self.message = message
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return self.message  # Customize what gets printed