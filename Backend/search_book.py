from Backend.search_strategy import *

class SearchBook:

    @classmethod
    def perform_search(self, query, strategy,treeview):
        context = None
        # strategy selection to classes
        if query == 'Title':
            context = StrategySearchByTitle.search(strategy)
        elif query == 'Author':
            context = StrategySearchByAuthor.search(strategy)
        elif query == 'Genre':
            context = StrategySearchByGenre.search(strategy)
        elif query == 'Year':
            context = StrategySearchByYear.search(strategy)

        if context:
            # results = context.search(BookManager.books, query)
            # Display results in the UI
            treeview.delete(*treeview.get_children())  # Clear existing rows
            for book in context:
                treeview.insert("", "end", values=(
                    book.get_title(), book.get_author(), book.get_year(), book.get_genre(), book.get_copies(),
                    book.get_is_lent()))

        else:
            treeview.delete(*treeview.get_children())  # Clear existing rows


