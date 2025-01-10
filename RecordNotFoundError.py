class RecordNotFoundError(Exception):
    def __init__(self, message="Record not found in the CSV file"):
        super().__init__(message)