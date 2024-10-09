**Programming Assignment:**

---

**Title:** Simple Library Book Management System

**Objective:**

Develop a Java program that simulates a simple library system to manage books. The program should allow users to add books to the library, borrow books, return books, and display the list of available books. Utilize Java Collections Framework classes such as `Map`, `Set`, and `List`. The entire solution should be contained in a single Java file.

---

**Assignment Details:**

**Functional Requirements:**

1. **Book Management:**

   - **Add Books:**
     - Allow the addition of new books to the library with a unique book ID and title.
   - **Borrow Books:**
     - Allow users to borrow books if they are available.
     - Update the status of the book to indicate it is borrowed.
   - **Return Books:**
     - Allow users to return books they have borrowed.
     - Update the status of the book to indicate it is available.
   - **Display Available Books:**
     - Show a list of all books that are currently available in the library.

2. **Collections Framework Usage:**

   - Use a `Map` to store books with the book ID as the key and the book object as the value.
   - Use a `Set` or `List` as needed for managing collections of data.

3. **Constraints:**

   - The entire solution should be contained in **one Java file**.
   - The `Book` class should be defined **outside** of the `LibrarySystem` class (not nested).
   - Handle exceptions appropriately (e.g., attempting to borrow a book that doesn't exist or is already borrowed).

---

**Instructions:**

1. **Class Definitions:**

   - **Main Class (`LibrarySystem`):**
     - Contains the `main` method.
     - Manages user interaction and menu display.
     - Manages the collection of books using appropriate data structures.
     - **Functions to implement in `LibrarySystem` class:**
       - **`addBook(Map<String, Book> library, Scanner scanner)`:**
         - Prompts the user to enter the `bookID` and `title`.
         - Checks if the `bookID` is unique (i.e., not already in the `library` map).
         - If unique, creates a new `Book` object and adds it to the `library` map.
         - Displays a message indicating the book was added successfully.
       - **`borrowBook(Map<String, Book> library, Scanner scanner)`:**
         - Prompts the user to enter the `bookID` of the book to borrow.
         - Checks if the book exists in the `library`.
         - If the book exists and is not borrowed, updates its `isBorrowed` status to `true`.
         - Displays a message indicating the book was borrowed.
         - If the book is already borrowed, displays an appropriate message.
       - **`returnBook(Map<String, Book> library, Scanner scanner)`:**
         - Prompts the user to enter the `bookID` of the book to return.
         - Checks if the book exists in the `library`.
         - If the book exists and is currently borrowed, updates its `isBorrowed` status to `false`.
         - Displays a message indicating the book was returned.
         - If the book is not borrowed, displays an appropriate message.
       - **`displayAvailableBooks(Map<String, Book> library)`:**
         - Iterates over the `library` map and displays books where `isBorrowed` is `false`.
         - If no books are available, displays a message indicating so.

   - **`Book` Class:**
     - Define the `Book` class outside of the `LibrarySystem` class.
     - Represents a book with at least the following attributes:
       - `bookID` (String)
       - `title` (String)
       - `isBorrowed` (boolean)
     - **Functions to implement in `Book` class:**
       - **Constructor:**
         - Initializes the `bookID`, `title`, and sets `isBorrowed` to `false` initially.
       - **Getters:**
         - `getBookID()`: Returns the `bookID`.
         - `getTitle()`: Returns the `title`.
         - `isBorrowed()`: Returns the `isBorrowed` status.
       - **Setters:**
         - `setBorrowed(boolean status)`: Updates the `isBorrowed` status.
       - **`toString()` Method:**
         - Overrides the `toString()` method to provide a string representation of the book (e.g., `"Book ID: B001, Title: The Great Gatsby"`).

2. **Program Flow:**

   - Display a menu with options:
     1. Add a new book
     2. Borrow a book
     3. Return a book
     4. Display available books
     5. Exit
   - Perform actions based on the user's choice.
   - Continue displaying the menu until the user chooses to exit.

3. **Data Management:**

   - Use a `HashMap<String, Book>` in the `LibrarySystem` class to store the books.
   - Ensure that when adding a new book, the `bookID` is unique.
   - Update the `isBorrowed` status of the book when borrowing or returning.

4. **Exception Handling:**

   - Provide meaningful messages to the user for invalid operations (e.g., "Book not found," "Book already borrowed").
   - Handle user inputs gracefully to prevent the program from crashing.

---

**Example Scenario:**

```
Welcome to the Library System!
1. Add a new book
2. Borrow a book
3. Return a book
4. Display available books
5. Exit
Enter your choice: 1

Enter Book ID: B001
Enter Book Title: The Great Gatsby
Book added successfully!

Enter your choice: 1

Enter Book ID: B002
Enter Book Title: 1984
Book added successfully!

Enter your choice: 2

Enter Book ID to borrow: B001
You have borrowed 'The Great Gatsby'.

Enter your choice: 4

Available Books:
Book ID: B002, Title: 1984

Enter your choice: 3

Enter Book ID to return: B001
You have returned 'The Great Gatsby'.

Enter your choice: 4

Available Books:
Book ID: B001, Title: The Great Gatsby
Book ID: B002, Title: 1984

Enter your choice: 5

Exiting the system. Goodbye!
```

---

**Submission Guidelines:**

- Submit the Java source code file (`LibrarySystem.java`).
- Ensure your code is well-commented and follows standard coding conventions.
- Include any assumptions or notes in comments at the top of your `LibrarySystem.java` file.
