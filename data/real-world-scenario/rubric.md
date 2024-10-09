**Rubric for Evaluating Student Submissions**

---

The total marks for this programming assignment are **100**. The rubric below provides detailed, step-by-step evaluation criteria, organized class-wise, to assess student code submissions for the Library Book Management System. Code quality and style are evaluated as part of each class's criteria.

---

### **1. LibrarySystem Class (Total: 106 marks)**

This class is responsible for the main program flow, user interaction, and managing the collection of books.

#### **a. Main Method and Program Flow (35 marks)**

- **Menu Display and Loop (10 marks)**
  - Correctly displays the menu with all required options (Add, Borrow, Return, Display, Exit). *(3 marks)*
  - Implements a loop to repeatedly display the menu until the user chooses to exit. *(4 marks)*
  - Handles the exit option appropriately, including closing the `Scanner`. *(3 marks)*

- **User Input Handling and Validation (20 marks)**
  - Accepts user input for menu choices and validates that it is an integer between 1 and 5. *(5 marks)*
    - Uses `scanner.hasNextInt()` or similar methods to check input. *(2 marks)*
    - Prompts the user again if input is invalid. *(3 marks)*
  - Consumes the newline character after reading integers to prevent input issues. *(2 marks)*
  - Ensures that the program does not crash on invalid input. *(4 marks)*
  - Provides meaningful error messages for invalid menu choices. *(4 marks)*

- **Code Quality and Style (5 marks)**
  - Uses meaningful variable names and follows Java naming conventions. *(2 marks)*
  - Code is properly indented and formatted for readability. *(2 marks)*
  - Includes comments explaining the main program flow and any complex logic. *(1 mark)*

#### **b. addBook Method (20 marks)**

- **Prompting for Book Details (3 marks)**
  - Prompts the user to enter the Book ID and Title. *(3 marks)*

- **Reading and Validating Input (7 marks)**
  - Reads `bookID` and `title` correctly using `scanner.nextLine()` and trims input to remove whitespace. *(3 marks)*
  - Checks if `bookID` is not empty and unique (not already in the library map). *(4 marks)*

- **Creating and Adding Book to Library (5 marks)**
  - Creates a new `Book` object with the provided `bookID` and `title`. *(2 marks)*
  - Adds the new `Book` to the `library` map with `bookID` as the key. *(2 marks)*
  - Confirms addition by displaying "Book added successfully!" *(1 mark)*

- **Handling Duplicate Book IDs (2 marks)**
  - Displays an appropriate message if the `bookID` already exists (e.g., "Book ID already exists. Please try again."). *(2 marks)*

- **Code Quality and Style (3 marks)**
  - Uses clear and consistent code structure within the method. *(1 mark)*
  - Variables and methods are named appropriately. *(1 mark)*
  - Includes comments explaining the purpose of the method and any complex logic. *(1 mark)*

#### **c. borrowBook Method (17 marks)**

- **Prompting for Book ID (2 marks)**
  - Prompts the user to enter the `bookID` of the book to borrow. *(2 marks)*

- **Checking Book Existence (3 marks)**
  - Verifies that the `bookID` exists in the `library` map. *(3 marks)*

- **Checking Borrow Status (5 marks)**
  - Checks if the book is not already borrowed (`isBorrowed` is `false`). *(2 marks)*
  - If the book is borrowed, displays "Book is already borrowed." *(3 marks)*

- **Updating Borrow Status (3 marks)**
  - Sets the book's `isBorrowed` status to `true`. *(2 marks)*
  - Confirms borrowing by displaying "You have borrowed '[Book Title]'." *(1 mark)*

- **Handling Book Not Found (2 marks)**
  - Displays "Book not found." if the `bookID` does not exist. *(2 marks)*

- **Code Quality and Style (2 marks)**
  - Method is well-organized and easy to understand. *(1 mark)*
  - Proper use of variable names and comments. *(1 mark)*

#### **d. returnBook Method (12 marks)**

- **Prompting for Book ID (2 marks)**
  - Prompts the user to enter the `bookID` of the book to return. *(2 marks)*

- **Checking Book Existence (2 marks)**
  - Verifies that the `bookID` exists in the `library` map. *(2 marks)*

- **Checking Borrow Status (3 marks)**
  - Checks if the book is currently borrowed (`isBorrowed` is `true`). *(2 marks)*
  - If the book was not borrowed, displays "Book was not borrowed." *(1 mark)*

- **Updating Borrow Status (2 marks)**
  - Sets the book's `isBorrowed` status to `false`. *(2 marks)*

- **Confirming Return (1 mark)**
  - Confirms return by displaying "You have returned '[Book Title]'." *(1 mark)*

- **Code Quality and Style (2 marks)**
  - Method is clear and logically structured. *(1 mark)*
  - Uses appropriate variable names and includes comments where necessary. *(1 mark)*

#### **e. displayAvailableBooks Method (12 marks)**

- **Iterating Over Library Map (4 marks)**
  - Iterates over the `library.values()` to access all `Book` objects. *(2 marks)*
  - Checks each book's `isBorrowed` status. *(2 marks)*

- **Displaying Available Books (4 marks)**
  - Displays each available book using the `toString()` method of the `Book` class. *(3 marks)*
  - Formats the output as specified (e.g., "Book ID: B001, Title: The Great Gatsby"). *(1 mark)*

- **Handling No Available Books (2 marks)**
  - If no books are available, displays "No books are currently available." *(2 marks)*

- **Code Quality and Style (2 marks)**
  - Efficient and readable code structure. *(1 mark)*
  - Includes comments if necessary for clarity. *(1 mark)*

#### **f. Use of Collections Framework (5 marks)**

- **Using HashMap for Library (5 marks)**
  - Correctly uses `HashMap<String, Book>` to store books with `bookID` as the key. *(3 marks)*
  - Ensures efficient retrieval and management of books. *(2 marks)*

#### **g. Exception Handling and Input Validation (5 marks)**

- **Preventing Crashes (2 marks)**
  - Handles exceptions that could cause the program to crash (e.g., `InputMismatchException`). *(2 marks)*

- **User-Friendly Messages (3 marks)**
  - Provides clear and helpful messages when errors occur or invalid input is detected. *(3 marks)*

---

### **2. Book Class (Total: 34 marks)**

This class represents the book entity with its attributes and behaviors.

#### **a. Class Declaration and Fields (9 marks)**

- **Correct Class Declaration (2 marks)**
  - Class is declared correctly outside the `LibrarySystem` class. *(2 marks)*

- **Private Fields (5 marks)**
  - Declares private fields `bookID`, `title`, and `isBorrowed`. *(3 marks)*
  - Uses appropriate data types for fields (`String` for `bookID` and `title`, `boolean` for `isBorrowed`). *(2 marks)*

- **Code Quality and Style (2 marks)**
  - Proper use of access modifiers (`private`, `public`) to encapsulate data. *(1 mark)*
  - Fields are named clearly and appropriately. *(1 mark)*

#### **b. Constructor (5 marks)**

- **Constructor Initialization (5 marks)**
  - Constructor accepts `bookID` and `title` as parameters. *(2 marks)*
  - Initializes `isBorrowed` to `false` by default. *(2 marks)*
  - Correctly assigns parameters to the class fields. *(1 mark)*

#### **c. Getters and Setter (10 marks)**

- **Getters (6 marks)**
  - `getBookID()` returns the `bookID`. *(2 marks)*
  - `getTitle()` returns the `title`. *(2 marks)*
  - `isBorrowed()` returns the `isBorrowed` status. *(2 marks)*

- **Setter (4 marks)**
  - `setBorrowed(boolean status)` updates the `isBorrowed` status. *(4 marks)*

#### **d. Overriding toString Method (3 marks)**

- **toString Implementation (3 marks)**
  - Overrides the `toString()` method. *(1 mark)*
  - Returns a string in the format "Book ID: [bookID], Title: [title]". *(2 marks)*

#### **e. Code Quality and Style (5 marks)**

- **Code Readability (2 marks)**
  - Code is properly formatted and indented. *(1 mark)*
  - Uses meaningful method and variable names following Java conventions. *(1 mark)*

- **Comments and Documentation (2 marks)**
  - Includes comments explaining the purpose of the class and methods. *(2 marks)*

- **Encapsulation and Access Modifiers (1 mark)**
  - Proper use of `private` for fields and `public` for methods to maintain encapsulation. *(1 mark)*

---

**Total Marks: 140**

---

**Notes for Evaluators:**

- **Partial Credit:** If a student partially completes a requirement, award partial marks accordingly.

- **Exception Handling:** Ensure that the program does not crash on invalid inputs, such as non-integer menu choices or null inputs.

- **Program Constraints:** Verify that the entire solution is contained in a single Java file and that only two classes are defined (`LibrarySystem` and `Book`), with the `Book` class defined outside of the `LibrarySystem` class.

- **Functionality Over Style:** While code quality is important and integrated into each class's criteria, the primary focus should be on the correct implementation of the required functionalities.

- **Originality:** Ensure that the student's work is original and not copied from external sources.

---
