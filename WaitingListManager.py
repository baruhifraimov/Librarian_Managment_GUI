import csv
import os
import tkinter as tk
from ExceptionUserAlreadyInList import UserAlreadyInList
from tkinter import messagebox, ttk

class WaitingListManager:

    @classmethod
    def update_waiting_list_csv(self, book,user : list):
        if os.path.exists("waiting_list.csv"):  # Check if the file exists
            with open("waiting_list.csv", 'a+', newline="") as file:
                writer = csv.writer(file)
                if os.stat("waiting_list.csv").st_size == 0:  # Check if the file is empty
                    writer.writerow(
                        ["Full Name", "Email", "Phone No.", "Book Title", "Book Author", "Book Genre", "Book Year","Queue No."])
                writer.writerow([user[0],user[1],user[2],book.title, book.author, book.genre, book.year,book.get_watch_list_size()])
        else:
            # The file does not exist, create it
            with open('waiting_list.csv', 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["Full Name", "Email", "Phone No.", "Book Title", "Book Author", "Book Genre", "Book Year",
                     "Queue No."])
                writer.writerow([user[0],user[1],user[2],book.title, book.author, book.genre, book.year,book.get_watch_list_size()])

    @classmethod
    def add_to_waiting_list(self,popup,book,name,phone,email):
        user = []
        # user[0] - full name
        # user[1] - email
        # user[2] - phone no.
        user.insert(0,name)
        user.insert(1,email)
        user.insert(2,phone)

        if user[0] and user[1] and user[2]:
            # Perform logic to add borrower to waiting list
            # TODO implement a save to a queue
            try:
                book.add_to_watch_list(user)
                tk.messagebox.showinfo(
                    "Waiting List Updated",
                    f"Added {user[0]} to the waiting list for the book: \n'{book.get_title()}'.")
                self.update_waiting_list_csv(book, user)
                popup.destroy()
            except UserAlreadyInList:
                tk.messagebox.showinfo(
                    "USER IS ALREADY WATCHING",
                    f" {user[0]} Is already in the watching list for: \n'{book.get_title()}'.")

        else:
            tk.messagebox.showerror("Error", "Please fill in all fields.")