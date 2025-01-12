import csv
import os
import tkinter as tk
from Exceptions.ExceptionUserAlreadyInList import UserAlreadyInListError
from tkinter import messagebox


class WaitingListManager:

    @classmethod
    def update_waiting_list_csv(self, book,user : list):
        if os.path.exists("../ConfigFiles/waiting_list.csv"):  # Check if the file exists
            with open("../ConfigFiles/waiting_list.csv", 'a+', newline="") as file:
                writer = csv.writer(file)
                if os.stat("../ConfigFiles/waiting_list.csv").st_size == 0:  # Check if the file is empty
                    writer.writerow(
                        ["Full Name", "Email", "Phone No.", "Book Title", "Book Author", "Book Genre", "Book Year","Queue No."])
                writer.writerow([user[0],user[1],user[2],book.title, book.author, book.genre, book.year,book.get_watch_list_size()])
        else:
            # The file does not exist, create it
            with open('../ConfigFiles/waiting_list.csv', 'w', newline="") as file:
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
            except UserAlreadyInListError:
                tk.messagebox.showinfo(
                    "USER IS ALREADY WATCHING",
                    f" {user[0]} Is already in the watching list for: \n'{book.get_title()}'.")

        else:
            tk.messagebox.showerror("Error", "Please fill in all fields.")

    @classmethod
    def remove_watchlist_csv(cls,user,book):
        try:
            # Read the CSV file
            with open('../ConfigFiles/waiting_list.csv', 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)

                # Search for the book to remove
                row_to_remove = None
                for row in rows:
                    #Full Name,Email,Phone No.,Book Title,Book Author,Book Genre,Book Year,Queue No.
                    if row[0] == user[0] and row[1] == user[1] and row[2] == user[2] and row[3] == book.title and row[4] == book.author and row[5] == book.genre and str(row[6]) == str(book.year):
                        row_to_remove = row




                if row_to_remove is None:
                    tk.messagebox.showinfo(
                        title="404",
                        message=f"The Waiting list Request by {user[0]} for book {book.title} was not found"
                    )
                else:
                    # update all the elements queue that point to the same book (decrease by one)
                    for row in rows:
                        # Book Title,Book Author,Book Genre,Book Year,Queue No.
                        if row[3] == book.title and row[4] == book.author and row[5] == book.genre and str(
                                row[6]) == str(book.year):
                            row[7] = int(row[7]) - 1
                            # row_to_update = row

            # Write the updated rows except the deleted row
            with open('../ConfigFiles/waiting_list.csv', 'w', newline="") as file:
                writer = csv.writer(file)
                for row in rows:
                    if row != row_to_remove:
                        writer.writerow(row)

        except FileNotFoundError as fnf_error:
            tk.messagebox.showinfo(
                title="404",
                message="FILE NOT FOUND"
            )
