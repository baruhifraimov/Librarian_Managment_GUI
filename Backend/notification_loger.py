import datetime
import os

class NotificationLogger:
    @staticmethod
    def log_notification(message):
        """
        Log the notification message to a file with a timestamp
        :param message:  The message to log
        :return:  None
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Use an absolute or relative path to place the file outside the package
        file_path = os.path.join(os.path.dirname(__file__), '..', 'notification_temp.txt')
        with open(file_path, 'a') as file:
            file.write(f'{timestamp} - {message}\n')