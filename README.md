# README

## Instructions to Run the Project

To run the project, you need to navigate to the `main.py` file and execute the main function.  
From there, a GUI will be displayed to the user. The first page will present three options:
1. **Login with an existing user.**
2. **Register a user.**
3. **Exit the application.**

After logging in, the user (librarian) will be notified of their existing notifications. The system manages a notification system unique to each librarian.

At the backend, the librarian who logs in will have an online flag activated, indicating that they are currently logged in.

### Main Screen
The main screen displays a welcome message that includes the librarian's username. The menu screen is populated with buttons arranged in a "chocolate cube" pattern. These buttons include:

#### Exposed Buttons:
- **Add Book:** Allows the librarian to add a new book to the system.
- **Remove Book:** Enables the librarian to remove a book from the collection.
- **Search Books:** Facilitates searching for books by title, author, or genre.
- **View Books:** Displays the list of all books available in the library.
- **Lend Book:** Allows the librarian to lend a book to a user.
- **Return Book:** Enables the librarian to process the return of a book.
- **Popular Books:** Displays a list of the most popular books based on lending data. (Popular book is determined by the number of times it has been lent out plus the size of his user waiting list.)
- **Logout:** Logs the librarian out of the system.
- **Exit:** Closes the application.

Each button is linked to its specific functionality, enabling seamless navigation and task execution.

---

## Data Management

The project uses CSV files to store essential data:

- **`books.csv`:** Stores book information, including the number of available copies, which updates dynamically.
- **`librarians_users.csv`:** Stores usernames and hashed passwords for users. Passwords are encrypted using `hashlib` with SHA-256.
- **`waiting_list.csv`:** Manages the waiting list for unavailable books. Each entry includes:
  - Full Name
  - Email
  - Phone Number
  - Book Title
  - Queue Number (updates automatically)

---

## Exception Handling

The application has a custom exception system. Each exception clearly specifies potential issues that may arise during runtime.

### Custom Exceptions:

#### **1. `ExceptionBelowZeroExceeded`**
**Purpose:**  
This exception is raised when an operation results in a value below zero, which violates business logic constraints (e.g., reducing the count of available books below zero).


#### **2. `ExceptionBlankFieldsError`**
**Purpose:**  
This exception is raised when a required field is left blank, ensuring mandatory information is provided before proceeding.


#### **3. `ExceptionBookNotFound404`**
**Purpose:**  
Raised when a book requested by the user cannot be found in the library's catalog or database.

#### **4. `ExceptionBorrowingLimitExceeded`**
**Purpose:**  
Raised when a user attempts to borrow more books than their account allows.

#### **5. `ExceptionNoObserversError`**
**Purpose:**  
This exception is triggered when an operation requires at least one observer, but none are registered.

#### **6. `ExceptionRecordNotFoundError`**
**Purpose:**  
Raised when a requested record (e.g., user profile, transaction history) is not found in the database.

#### **7. `ExceptionReturnLimitExceeded`**
**Purpose:**  
Raised when a user attempts to return more books than they have borrowed.

#### **8. `ExceptionUserAlreadyInList`**
**Purpose:**  
This exception is raised when a user is added to a list (e.g., waitlist) but is already present in the list.

#### **9. `ExceptionUserNotFound`**
**Purpose:**  
Raised when a user-related operation is attempted, but the user cannot be found in the system.

#### **10. `ExceptionWatchedBookRemovalError`**
**Purpose:**  
Raised when an attempt is made to remove a book that is being watched by users (e.g., reserved or requested).
---

## Logging System

The system logs all major actions and events performed by librarians. This includes actions such as adding books, lending books, updating the waiting list, and logging in or out. The logging system is implemented using Python's `logging` module and follows these principles:

- **Log Levels:** The system uses different log levels (`INFO`, `ERROR`) to categorize log messages based on their importance.
- **Log Storage:**
  - General application logs are stored in `logs/app.log`.
  - Notifications are logged in `notification_temp.txt` and later merged into the main log system.
- **Log Format:** Each log entry includes a timestamp, the log level, the module or function name, and a descriptive message.
- **Decorator Pattern:** Key functions use decorators from `log_decorator.py` to ensure consistent and efficient logging.

This centralized logging approach simplifies debugging and provides an audit trail of all actions performed within the system.

---
## Notification System

- When a user is added to the waiting list and a book becomes available, all observers (librarians) are notified.
- The system automatically assigns the book to the first user in the queue and updates all related files accordingly.
- Notifications are logged one file:
  - **`notification_temp.txt`:** Stores all the notifications.

If a librarian logs out and another logs in, the new librarian is presented with the last five notifications sent to them.

---

## System Features

### Core Features:
- **Book Management:**
  - Add, remove, search, lend, and return books.
  - Maintain a list of popular books.
- **User Management:**
  - Register and authenticate librarians securely.
  - Manage librarian-specific notifications.
- **Waiting List Management:**
  - Track users in the waiting list and notify them when books become available.
- **Encryption:**
  - Securely store sensitive data using SHA-256 encryption.
- **Logging:**
  - Detailed logs for all operations and errors.

---

## Design Patterns Implemented

### 1. **Factory Pattern:**
- Used in `book_factory.py` and `librarian_factory.py` to create book and librarian instances dynamically.

### 2. **Observer Pattern:**
- Implemented in `observer.py` for real-time notifications of waiting list updates.

### 3. **Strategy Pattern:**
- Used in `search_strategy.py` to provide flexible search mechanisms for books (e.g., by title, author, or genre).

### 4. **Singleton Pattern:**
- Ensures a single instance of the `Logger` class for consistent logging across the system (`logger_config.py`).

### 5. **Iterator Pattern:**
- Facilitates traversing available books and lent books efficiently in `avl_books_iter.py` and `lend_book_iter.py`.

### 6. **Decorator Pattern:**
- Used in `log_decorator.py` to add logging capabilities to key functions.

---

## SOLID OOP Principles

### 1. **Single Responsibility Principle:**
- Each class in the system has a single, well-defined responsibility. For instance, `book_manager.py` handles book-related logic, while `librarian_manager.py` focuses on managing librarians.

### 2. **Open/Closed Principle:**
- The system is designed to be easily extendable. For example, adding new search strategies only requires extending the `search_strategy.py` without modifying existing code.

### 3. **Liskov Substitution Principle:**
- Subtypes can replace their parent types without altering the functionality. This is evident in the observer system, where different observer types (e.g., librarians) can subscribe to updates seamlessly.

### 4. **Interface Segregation Principle:**
- Interfaces are designed to be client-specific. Each component, such as the `book_factory.py` and `search_strategy.py`, has minimal and focused methods.

### 5. **Dependency Inversion Principle:**
- High-level modules do not depend on low-level modules but rather on abstractions. For instance, the `Logger` and `Observer` functionalities rely on abstract interfaces, allowing flexibility in implementation.

