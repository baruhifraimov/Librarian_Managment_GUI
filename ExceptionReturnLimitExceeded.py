class ReturnLimitExceeded(Exception):
    """Custom exception raised when return limit is exceeded."""
    def __init__(self):
        self.message = f"No books to return."
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return self.message  # Customize what gets printed