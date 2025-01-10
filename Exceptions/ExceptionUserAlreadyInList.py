class UserAlreadyInList(Exception):
    """Custom exception raised when User is already in the watching list of the same book,
     User is not allowed to watch the same item more than once."""
    def __init__(self):
        self.message = f"User already in list."
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return self.message  # Customize what gets printed