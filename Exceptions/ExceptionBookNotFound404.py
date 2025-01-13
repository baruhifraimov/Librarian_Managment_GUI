class BookNotFound404Error(Exception):
    """Custom exception raised when at least a single field is blank."""
    def __init__(self,title, author, genre, year):
        self.message = (f"No Book with the details: (Title:{title}"
                        f"Author:{author}"
                        f"Genre:{genre}"
                        f"Year:{year})"
                        f"Exists")
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return self.message  # Customize what gets printed