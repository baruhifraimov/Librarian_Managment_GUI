from collections import deque

from Backend.notification_loger import NotificationLogger
from Backend.observer import Observer
from ConfigFiles.log_decorator import log_activity
import tkinter as tk
from tkinter import messagebox
from Backend import librarian_manager

class Librarian(Observer):

    def __init__(self, username, password,is_connected:str='False'):
        self.username = username
        self.password = password
        self.is_connected = str(is_connected)
        # contain only 5 messages max
        self.message_list = deque(maxlen=5)
        librarian_manager.librarians.append(self)

    @log_activity("notification sent")
    def update(self, user, book):
        notification_message = (
            f'NOTIFICATION SENT TO LIBRARIAN: {self.username}'
            f' | Notify Librarian:{user[0]} | The book: {book.get_title()} is available now.'
            f' | You can notify him by Email: {user[1]} Or by Phone: {user[2]}'
        )
        self.message_list.append(notification_message)

        print(notification_message)

        # logging the message to the notification log file
        NotificationLogger.log_notification(notification_message)

        # give a popup notification  to the current user that is live
        if self.get_is_connected() == 'True':
            # Displaying a popup notification
            root = tk.Tk()
            messagebox.showinfo("Notification", notification_message)
            self.pop_user_message()
            root.destroy()

    def get_user_messages(self):
        return self.message_list

    def pop_user_message(self):
        return self.message_list.popleft()

    def get_user_messages_size(self):
        return len(self.message_list)

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_is_connected(self):
        return self.is_connected

    def activate_user(self):
        self.is_connected = 'True'

    def deactivate_user(self):
        self.is_connected = 'False'