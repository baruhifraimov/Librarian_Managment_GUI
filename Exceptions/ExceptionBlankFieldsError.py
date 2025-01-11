class BlankFieldsError(Exception):
    """Custom exception raised when at least a single field is blank."""
    def __init__(self):
        self.message = f"The fields you are trying to submit are blank!"
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return self.message  # Customize what gets printed