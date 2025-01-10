from Backend.AvBooksItr import AvBooksItr
from Backend.BookManager import BookManager
from Backend.LendBookItr import LendBookItr
import tkinter as tk


class TreeViewLoader:

    @classmethod
    def load_books_into_treeview(self, treeview, filter=0):
        # delete all exist books
        for row in treeview.get_children():
            treeview.delete(row)

        match filter:
            case 0:
                # base case , show all books
                for book in BookManager.books:
                    treeview.insert("", tk.END, values=(
                        book.get_title(), book.get_author(), book.get_year(), book.get_genre(), book.get_copies(),
                        book.get_is_lent(), book.get_Available_books_num()))
            case 1:
                # case 1 , sort by only available books.
                iterator = iter(AvBooksItr(BookManager.books))
                for book in iterator:
                    treeview.insert("", tk.END, values=(
                        book.get_title(), book.get_author(), book.get_year(), book.get_genre(), book.get_copies(),
                        book.get_is_lent(), book.get_Available_books_num()))

            case 2:
                # case 2 , sort by the books that are being lent.
                # sorted takes the current list and duplicates (and sorts) it to a new list
                iterator = iter(LendBookItr(BookManager.books))
                for book in iterator:
                    treeview.insert("", tk.END, values=(
                        book.get_title(), book.get_author(), book.get_year(), book.get_genre(), book.get_copies(),
                        book.get_is_lent(), book.get_Available_books_num()))

            case 3:
                # case 3 , sort by only lent books.
                srt_cat_books = sorted(BookManager.books, key=lambda book: book.get_genre())
                for book in srt_cat_books:
                    treeview.insert("", tk.END, values=(
                        book.get_title(), book.get_author(), book.get_year(), book.get_genre(), book.get_copies(),
                        book.get_is_lent(), book.get_Available_books_num()))

            case 4:
                popular_books = []
                # case 3 , sort by only popularity books.
                for book in BookManager.books:
                    if int(book.get_lent_count()) > 0:
                        popular_books.append(book)
                popular_books.sort(key=lambda book: (int(book.get_lent_count()) + int(book.get_watch_list_size())),
                                   reverse=True)
                for book in popular_books[:10]:
                    treeview.insert("", tk.END, values=(
                        book.get_title(), book.get_author(), book.get_year(), book.get_genre(),
                        int(book.get_lent_count()) + int(book.get_watch_list_size())))

            case default:
                return "no filter"

    def on_treeview_select(event, treeview, parent):
        selected = treeview.focus()  # Get the focused item
        parent.selected_item = treeview.item(selected)  # Update selected_item directly in the parent class

    @classmethod
    def refresh_treeview(self, treeview,filter = 0):
        # Clear existing rows
        for row in treeview.get_children():
            treeview.delete(row)

        TreeViewLoader.load_books_into_treeview(treeview, filter)