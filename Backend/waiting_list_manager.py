import csv
import os
import tkinter as tk

from Exceptions.ExceptionBlankFieldsError import BlankFieldsError
from Exceptions.ExceptionUserAlreadyInList import UserAlreadyInListError
from tkinter import messagebox


class WaitingListManager:

    @classmethod
    def update_waiting_list_csv(self, book,user : list):
        """
        Update the waiting list csv file with the user details and the book details.
        :param book:  The book to add the user to the waiting list for
        :param user:  The user to add to the waiting list
        :return: None
        """
        if os.path.exists("../csv_files/waiting_list.csv"):  # Check if the file exists
            with open("../csv_files/waiting_list.csv", 'a+', newline="") as file:
                writer = csv.writer(file)
                if os.stat("../csv_files/waiting_list.csv").st_size == 0:  # Check if the file is empty
                    writer.writerow(
                        ["Full Name", "Email", "Phone No.", "Book Title", "Book Author", "Book Genre", "Book Year","Queue No."])
                writer.writerow([user[0],user[1],user[2],book.title, book.author, book.genre, book.year,book.get_watch_list_size()])
        else:
            # The file does not exist, create it
            with open('../csv_files/waiting_list.csv', 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["Full Name", "Email", "Phone No.", "Book Title", "Book Author", "Book Genre", "Book Year",
                     "Queue No."])
                writer.writerow([user[0],user[1],user[2],book.title, book.author, book.genre, book.year,book.get_watch_list_size()])

    @classmethod
    def add_to_waiting_list(self,popup,book,name,phone,email):
        """
        Add a user to the waiting list for a specific book and update the queue accordingly in the csv file.
        If the user is already in the list, an error message is displayed.
        :param popup:  The popup window to close after the user is added to the waiting list
        :param book:  The book to add the user to the waiting list for
        :param name:  The name of the user to add
        :param phone:  The phone number of the user to add
        :param email:  The email of the user to add
        :return:  None
        """
        user = []
        # user[0] - full name
        # user[1] - email
        # user[2] - phone no.
        user.insert(0,name)
        user.insert(1,email)
        user.insert(2,phone)
        try:
            book.add_to_watch_list(user)
            tk.messagebox.showinfo(
                "Waiting List Updated",
                f"Added {user[0]} to the waiting list for the book: \n'{book.get_title()}'.")
            self.update_waiting_list_csv(book, user)
            popup.destroy()
        except BlankFieldsError:
            tk.messagebox.showerror("Error", "Please fill in all fields.")
        except ValueError as e:
            if e.__str__() == "Name must not contain digits":
                tk.messagebox.showerror("Error", "Name must be a string.")
            else:
                tk.messagebox.showerror("Error", "Phone must be a number.")
        except UserAlreadyInListError:
            tk.messagebox.showinfo(
                "USER IS ALREADY WATCHING",
                f" {user[0]} Is already in the watching list for: \n'{book.get_title()}'.")



    @classmethod
    def remove_waiting_list_csv(cls,user,book):
        """
        Remove a user from the waiting list for a specific book and update the queue accordingly in the csv file.
        If the user is not found, an error message is displayed.
        :param user:  The user to be removed
        :param book:  The book to remove the user from
        :return:  None
        """
        try:
            # Read the CSV file
            with open('../csv_files/waiting_list.csv', 'r') as file:
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
            with open('../csv_files/waiting_list.csv', 'w', newline="") as file:
                writer = csv.writer(file)
                for row in rows:
                    if row != row_to_remove:
                        writer.writerow(row)

        except FileNotFoundError as fnf_error:
            tk.messagebox.showinfo(
                title="404",
                message="FILE NOT FOUND"
            )
