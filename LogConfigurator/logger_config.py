import logging
import os

# Define the log file path
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app.log')

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set the log level

# File handler (for logging to a file)
file_handler = logging.FileHandler(LOG_FILE_PATH, mode='a')  # Use 'a' for append, 'w' for overwrite
file_handler.setLevel(logging.INFO)  # Set the log level for the file handler

# Stream handler (for logging to the console)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)  # Set the log level for the console

# Formatter (for both handlers)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)