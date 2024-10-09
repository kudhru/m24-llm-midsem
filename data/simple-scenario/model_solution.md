```java
import java.util.Scanner;

public class StringManipulator {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter a string: ");
        String input = sc.nextLine();
        System.out.println("Original String: " + input);
        System.out.println("Uppercase String: " + input.toUpperCase());
        String reversed = new StringBuilder(input).reverse().toString();
        System.out.println("Reversed String: " + reversed);
        System.out.println("Number of Characters: " + input.length());
        sc.close();
    }
}
```
