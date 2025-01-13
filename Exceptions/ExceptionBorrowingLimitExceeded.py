class BorrowingLimitExceededError(Exception):
    """Custom exception raised when borrowing limit is exceeded."""
    def __init__(self, max_limit):
        self.max_limit = max_limit
        self.message = f"No Available Copies for lending this book , already {max_limit} copies has been lent."
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return self.message  # Customize what gets printed