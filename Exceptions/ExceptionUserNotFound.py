class UserNotFoundError(Exception):
    """Custom exception raised when return limit is exceeded."""
    def __init__(self,user_name):
        self.message = f"User:{user_name} not found."
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return self.message  # Customize what gets printed