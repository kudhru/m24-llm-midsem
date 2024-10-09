```java
import java.util.*;

class Book {
    private String bookID;
    private String title;
    private boolean isBorrowed;

    // Constructor
    public Book(String bookID, String title) {
        this.bookID = bookID;
        this.title = title;
        this.isBorrowed = false;
    }

    // Getters
    public String getBookID() {
        return bookID;
    }

    public String getTitle() {
        return title;
    }

    public boolean isBorrowed() {
        return isBorrowed;
    }

    // Setter
    public void setBorrowed(boolean status) {
        this.isBorrowed = status;
    }

    // toString method
    @Override
    public String toString() {
        return "Book ID: " + bookID + ", Title: " + title;
    }
}
public class LibrarySystem {
    public static void main(String[] args) {
        Map<String, Book> library = new HashMap<>();
        Scanner scanner = new Scanner(System.in);
        int choice;

        do {
            // Display menu
            System.out.println("Welcome to the Library System!");
            System.out.println("1. Add a new book");
            System.out.println("2. Borrow a book");
            System.out.println("3. Return a book");
            System.out.println("4. Display available books");
            System.out.println("5. Exit");
            System.out.print("Enter your choice: ");

            while (!scanner.hasNextInt()) {
                System.out.print("Invalid input. Please enter a number between 1 and 5: ");
                scanner.next();
            }
            choice = scanner.nextInt();
            scanner.nextLine(); // Consume newline

            // Handle choices
            switch (choice) {
                case 1:
                    addBook(library, scanner);
                    break;
                case 2:
                    borrowBook(library, scanner);
                    break;
                case 3:
                    returnBook(library, scanner);
                    break;
                case 4:
                    displayAvailableBooks(library);
                    break;
                case 5:
                    System.out.println("Exiting the system. Goodbye!");
                    break;
                default:
                    System.out.println("Invalid choice. Please enter a number between 1 and 5.");
            }

            System.out.println();

        } while (choice != 5);

        scanner.close();
    }

    public static void addBook(Map<String, Book> library, Scanner scanner) {
        // Prompt for book details
        System.out.print("Enter Book ID: ");
        String bookID = scanner.nextLine().trim();
        System.out.print("Enter Book Title: ");
        String title = scanner.nextLine().trim();

        // Check if book ID is unique
        if (!library.containsKey(bookID)) {
            Book newBook = new Book(bookID, title);
            library.put(bookID, newBook);
            System.out.println("Book added successfully!");
        } else {
            System.out.println("Book ID already exists. Please try again.");
        }
    }

    public static void borrowBook(Map<String, Book> library, Scanner scanner) {
        // Prompt for book ID
        System.out.print("Enter Book ID to borrow: ");
        String bookID = scanner.nextLine().trim();

        // Check if book exists and is available
        if (library.containsKey(bookID)) {
            Book book = library.get(bookID);
            if (!book.isBorrowed()) {
                book.setBorrowed(true);
                System.out.println("You have borrowed '" + book.getTitle() + "'.");
            } else {
                System.out.println("Book is already borrowed.");
            }
        } else {
            System.out.println("Book not found.");
        }
    }

    public static void returnBook(Map<String, Book> library, Scanner scanner) {
        // Prompt for book ID
        System.out.print("Enter Book ID to return: ");
        String bookID = scanner.nextLine().trim();

        // Check if book exists and is borrowed
        if (library.containsKey(bookID)) {
            Book book = library.get(bookID);
            if (book.isBorrowed()) {
                book.setBorrowed(false);
                System.out.println("You have returned '" + book.getTitle() + "'.");
            } else {
                System.out.println("Book was not borrowed.");
            }
        } else {
            System.out.println("Book not found.");
        }
    }

    public static void displayAvailableBooks(Map<String, Book> library) {
        boolean anyAvailable = false;
        System.out.println("Available Books:");
        for (Book book : library.values()) {
            if (!book.isBorrowed()) {
                System.out.println(book);
                anyAvailable = true;
            }
        }
        if (!anyAvailable) {
            System.out.println("No books are currently available.");
        }
    }
}
```
