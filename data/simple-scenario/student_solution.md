```java
import java.util.Scanner;

public class StringManipulator {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter a string: ");
        String input = sc.next();

        System.out.println("Original String: " + input);
        System.out.println("Uppercase String: " + input.toLowerCase());

        String reversed = "";
        for (int i = 0; i <= input.length(); i++) { 
            reversed += input.charAt(i); 
        }
        System.out.println("Reversed String: " + reversed);

        System.out.println("Number of Characters: " + (input.length() - 1)); 

        // Forgot to close the scanner
    }
}
```
