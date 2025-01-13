class BelowZeroError(Exception):
    """Custom exception raised when WatchList limit is exceeded."""
    def __init__(self, max_limit):
        self.max_limit = max_limit
        self.message = f"You cannot go below zero."
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return self.message  # Customize what gets printed