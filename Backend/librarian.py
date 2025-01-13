from Backend.notification_loger import NotificationLogger
from Backend.observer import Observer
from ConfigFiles.log_decorator import log_activity
import tkinter as tk
from tkinter import messagebox

class User(Observer):

    users = []

    def __init__(self, username, password,is_connected:str='False'):
        self.username = username
        self.password = password
        self.is_connected = str(is_connected)
        User.users.append(self)

    @log_activity("notification sent")
    def update(self, user, book):
        notification_message = (
            f'NOTIFICATION SENT TO LIBRARIAN: {self.username}'
            f' | Notify User:{user[0]} | The book: {book.get_title()} is available now.'
            f' | You can notify him by Email: {user[1]} Or by Phone: {user[2]}'
        )

        print(notification_message)

        # logging the message to the notification log file
        NotificationLogger.log_notification(notification_message)

        # give a popup notification  to the current user that is live
        if self.get_is_connected() == 'True':
            # Displaying a popup notification
            root = tk.Tk()
            messagebox.showinfo("Notification", notification_message)
            root.destroy()




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