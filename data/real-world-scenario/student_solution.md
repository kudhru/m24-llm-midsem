```java
import java.util.*;

public class LibrarySystem {
    public static void main(String[] args) {
        HashMap library = new HashMap();
        Scanner scanner = new Scanner(System.in);
        int choice = 0;

        do {
            // Display menu
            System.out.println("Welcome to the Library System!");
            System.out.println("1. Add a new book");
            System.out.println("2. Borrow a book");
            System.out.println("3. Return a book");
            System.out.println("4. Display available books");
            System.out.println("5. Exit");
            System.out.print("Enter your choice: ");

            choice = scanner.nextInt();

            // Handle choices
            if (choice == 1) {
                addBook(library, scanner);
            } else if (choice == 2) {
                borrowBook(library, scanner);
            } else if (choice == 3) {
                returnBook(library, scanner);
            } else if (choice == 4) {
                displayAvailableBooks(library);
            } else if (choice == 5) {
                System.out.println("Exiting the system. Goodbye!");
            } else {
                System.out.println("Invalid choice. Please enter a number between 1 and 5.");
            }

        } while (choice != 5);
    }

    public static void addBook(HashMap library, Scanner scanner) {
        // Prompt for book details
        System.out.print("Enter Book ID: ");
        String bookID = scanner.nextLine();
        System.out.print("Enter Book Title: ");
        String title = scanner.nextLine();

        // Check if book ID is unique
        Book book = new Book(bookID, title);
        library.put(bookID, book);
        System.out.println("Book added successfully!");
    }

    public static void borrowBook(HashMap library, Scanner scanner) {
        // Prompt for book ID
        System.out.print("Enter Book ID to borrow: ");
        String bookID = scanner.nextLine();
    }

    public static void returnBook(HashMap library, Scanner scanner) {
        if (book.isBorrowed) {
            book.isBorrowed = false;
            System.out.println("You have returned '" + book.title + "'.");
        } else {
            System.out.println("Book was not borrowed.");
        }
    }

    public static void displayAvailableBooks(HashMap library) {
        System.out.println("Available Books:");
    }
}

class Book {
    public String bookID;
    public String title;
    public boolean isBorrowed;

    // Constructor
    public Book(String bookID, String title) {
        bookID = bookID;
        title = title;
        isBorrowed = false;
    }
}
```
