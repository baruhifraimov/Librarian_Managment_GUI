from Exceptions.ExceptionBorrowingLimitExceeded import BorrowingLimitExceeded
import tkinter as tk
from tkinter import messagebox
from Backend.BookManager import BookManager
from Backend.TreeViewLoader import TreeViewLoader
from Backend.WaitingListManager import WaitingListManager


class LendBook:

    @classmethod
    def book_lending(self, selected_item, treeview, root):
        """
        check if there are available books to borrow
        if True , let me borrow the book.
        if False , The safran has to fill the details of the borrower to add it to the waiting list.
        :param selected_item: item that been selected from the treeView
        :param treeview: tk widget
        :param root: frame root of the application
        :return: None
        """

        if selected_item is not None:
            selected_values = selected_item['values']
            selected_title = selected_values[0]
            selected_author = selected_values[1]
            selected_year = selected_values[2]
            selected_genre = selected_values[3]
            # selected_copies = int(selected_values[4])  # Convert copies to int if necessary

            for book in BookManager.books:
                if (book.get_title() == str(selected_title) and
                        book.get_author() == str(selected_author) and
                        book.get_year() == str(selected_year) and
                        book.get_genre() == str(selected_genre)):

                    if book.get_is_lent() == "No":
                        try:
                            book.borrow_action()  # Borrow the book and add +1 to book lent
                            BookManager.update_in_csv(book, 1)
                            tk.messagebox.showinfo(
                                "Success",
                                f"Book '{selected_title}' is available! Lending now."
                            )
                            TreeViewLoader.refresh_treeview(treeview)
                        except BorrowingLimitExceeded:
                            tk.messagebox.showinfo(
                                "Failed",
                                f"Selected book: '{selected_title}' cannot be borrowed!\n"
                                f"No. of Book Copies Available: {book.get_copies() - book.get_lent_count()}\n"
                            )
                    else:
                        self.show_waiting_list_form(book, root)
                    break
            else:
                tk.messagebox.showinfo(
                    "Failed",
                    f"Selected book: '{selected_title}'  not found in the book list!"
                )
        else:
            tk.messagebox.showinfo(
                "Failed",
                "No book Selected!"
            )

    @classmethod
    def show_waiting_list_form(self, book, root):
        # Create a new popup window
        popup = tk.Toplevel(root)
        popup.title("Add to Waiting List")
        popup.geometry("450x280")

        tk.Label(popup, text=f"Book '{book.get_title()}' is not available. fill details to join waiting list:",
                 font=("Arial", 14)).grid(row=0, column=1, pady=10, padx=10)

        # Form fields
        tk.Label(popup, text="Full Name:", font=("Arial", 14)).grid(row=1, column=0, pady=10, padx=2)
        name_entry = tk.Entry(popup, font=("Arial", 14))
        name_entry.grid(row=1, column=1, pady=10, padx=2)

        tk.Label(popup, text="Email:", font=("Arial", 14)).grid(row=2, column=0, pady=10, padx=2)
        email_entry = tk.Entry(popup, font=("Arial", 14))
        email_entry.grid(row=2, column=1, pady=10, padx=2)

        tk.Label(popup, text="Phone:", font=("Arial", 14)).grid(row=3, column=0, pady=10, padx=2)
        phone_entry = tk.Entry(popup, font=("Arial", 14))
        phone_entry.grid(row=3, column=1, pady=10, padx=2)
        tk.Button(popup, text="Add to Waiting List", font=("Arial", 14),
                  command=lambda: WaitingListManager.add_to_waiting_list(popup, book, name_entry.get(),
                                                                         phone_entry.get(),
                                                                         email_entry.get())).grid(row=4,
                                                                                                       column=0,
                                                                                                       columnspan=2,
                                                                                                       pady=20)