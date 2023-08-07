import org.w3c.dom.css.Rect;
import org.w3c.dom.ls.LSOutput;
import java.util.*;

// The name of the class must match the name of the file:
public class Syntax {

    // In Java, a main method inside a class is the entry point of the program:
    public static void main(String[] args) {

        /* __________Data Types & Structures__________ */
        // int (32 bits):
        int age; 
        age = 35;

        // long  (64 bits), 'L' suffix is needed:
        long myLong = 1000000000000000000L; 

        // flat is 32 bits, 'f' suffix is needed:
        float myFloat = 5.5f; 

        // double is 64 bits:
        double myDouble = 5.5; 

        char myChar = 'M';
        myChar = '\u004D';

        boolean myBool = true;

        // The 'final' keyword is used for constants:
        final String HELLO = "Hello"; 

        // Strings are immutable:
        String myString = "World";

        // When reassigning a string's value, a new string is created in memory.
        myString = HELLO + " " + myString;
        System.out.println(myString); // "Hello World"
        System.out.println(String.format("%s World", HELLO)); // String formatting

        // The 'equals' method is used to compare strings:
        System.out.println(myString.equals("Hello World")); // true

        // Declaring multiple variables in a line:
        String firstName = "John", lastName = "Doe";


        // Declaring an array of strings:
        String[] myArray = new String[5];
        myArray[0] = "Hello";
        myArray[1] = "How";
        myArray[2] = "Are";
        myArray[3] = "You";
        myArray[4] = "Today?";
        
        // Declaring an array of strings with values:
        String[] myArray2 = {"Hello", "How", "Are", "You", "Today?"};


        // Arrays are static in size, so to add a new element, a new array must be created:
        String[] myArray3 = new String[6];
        for (int i=0; i<myArray.length; i++) {
            myArray3[i] = myArray[i];
        }
        myArray3[5] = "Goodbye";


        // Array methods can be utilised for a more concise syntax:
        String[] myArray4 = Arrays.copyOf(myArray, 6);
         myArray3[4] = "Goodbye";

        
        /*  In general, if we need to add or remove elements, it is better to use an ArrayList, which is dynamic.
        Primitive data types cannot be used when creating ArrayLists, so we must use the wrapper classes instead.
        (e.g. Integer, Double, Character, Boolean, instead of int, double, char, boolean)
        */
        ArrayList<String> myArrayList = new ArrayList<String>();
        myArrayList.add("John");
        myArrayList.add("Will");
        myArrayList.add("Alex");
        myArrayList.add("David");
        myArrayList.add("James");

        // This method can be used to sort the array list:
        Collections.sort(myArrayList);
        System.out.println(myArrayList); // [Alex, David, James, John, Will]

        // Add and get methods can be used to access ArrayList Content:
        myArrayList.add("Jack");
        System.out.println(myArrayList.get(5)); // Jack

        // The size method can be used to get the length of an ArrayList:
        System.out.println(myArrayList.size()); // 6

        // The remove method can be used to remove an element from an ArrayList:
        myArrayList.remove(5); // Removing using index
        myArrayList.remove("John"); // Removing using value
        System.out.println(myArrayList.size()); // 4
        
        myArrayList.clear(); // Removes all elements
        System.out.println(myArrayList.isEmpty()); // true


        // Maps are similar to dictionaries in Python:
        // Key and value data types are defined:
        Map<String, String> myMap = new HashMap<>();
        myMap.put("name", "John");
        myMap.put("surname", "Doe");
        System.out.println(myMap.get("name")); // John
        myMap.remove("name");
        System.out.println(myMap.containsKey("name")); // false
        System.out.println(myMap.containsValue("Doe")); // true
        System.out.println(myMap.size()); // 1



        /* __________Conditions__________ 
        || is OR
        && is AND
        */
        if (age >= 18) {
            System.out.println("I am an adult.");
        } else if (age >= 13) {
            System.out.println("I am a teenager.");
        } else {
            System.out.println("I am a child.");
        }

        switch(age % 2) {
            case 0: 
                System.out.println("My age is even."); 
                break;
            case 1:
                System.out.println("My age is odd.");
                break;
            
            // 'default' runs if no case matches:
            default:
                System.out.println("age is not a number");
                // 'break' is not technically needed for the default case since it is checked last, but it is good practice:
                break;
        }

        /* New switch syntax in Java 14 onwards:
        switch (age % 2){
            case 0 -> System.out.println("My age is even.");
            case 1 -> System.out.println("My age is odd.");
            default -> System.out.println("age is not a number");
        }
         */

        // Ternary operator:
        String test = age >= 18 ? "I am an adult." : "I am a minor.";
        System.out.println(test);


        /* __________Loops__________ */
        for (int i=0; i<5; i++) {
            System.out.println(i);
        }

        int i = 0;
        while (i < 5){
            System.out.println(i);
            i++;
        }


        i = 0;
        // Do while loop, condition checked at the end so runs at least once:
        do {
            System.out.println(i);
            i++;
        } while (i < 5);
        

        // ToDo: FOR EACH



        /* __________Functions__________ */

        /* __________Error Handling__________ */

        /* __________Object Oriented Programming__________ 
        In this demonstration, for the sake of simplicity, all classes are defined in the same file.
        However, in practice, each class should be defined in its own file.
        */

        // This happens to be an abstract class. Abstract classes cannot be instantiated, but its children can.
        // They can have both normal and abstract methods (abstract methods need to be implemented by the children).
        abstract class Shape {
            String color;

            public Shape(String color) {
                this.color = color;
            }

            public double area() {
                throw new Error("Cannot calculate area of unknown shape.");
            }
        }

        class Rectangle extends Shape {
            double height;
            double width;

            // Constructor:
            public Rectangle(String color, double height, double width) {
                super(color);
                this.height = height;
                this.width = width;
            }

            // Getters & setters:
            public double getHeight() {
                return height;
            }

            public void setHeight(double height) {
                if (height < 0) {
                    throw new IllegalArgumentException("Height cannot be negative.");
                }
                this.height = height;
            }

            public double getWidth() {
                return width;
            }

            public void setWidth(double width) {
                if (width < 0) {
                    throw new IllegalArgumentException("Width cannot be negative.");
                }
                this.width = width;
            }

            @Override // The override annotation is good practice to include.
            public double area() {
                return this.height * this.width;
            }
        }


        // Inheritance:
        class Square extends Rectangle {
            public Square(String color, double side) {
                super(color, side, side);
            }
            /* If overriding an inherited method, simply define a new method with the same name and parameters.
                Use the 'super.myFunction(argument)' syntax to call the parent method.
                */
        }

        Rectangle myRectangle = new Rectangle("Blue", 5, 10);
        Square mySquare = new Square("Red", 10);


        /* The 'static' keyword makes an attribute/method belong to the class, not the object.
         This means that the attribute/method can be accessed without creating an object of the class.
        */
        class Circle extends Shape {
            // Here, the static keyword is commented out because it cannot be used in an inner class:
            /* static */ final Double pi = 3.14159265359;
            double radius;

            public Circle(String color, double radius) {
                super(color);
                this.radius = radius;
            }

            public double area() {
                return this.pi * this.radius * this.radius;
            }

            // There can also be static method that belong to the class itself:
            /* static */ public Double getPi() {
                return this.pi;
            }
        }

        /* An inner class is a class that is defined inside another class.
        It has access to all the attributes and methods of the outer class, and can define its own.
        Using inner classes can make code easier to understand.
        Technically, all the classes in this file are inner classes of the Syntax class. 
        Usually, each class in Java is defined in its own file. This is just for demonstration purposes
         */


        /*  An interface is a collection of constants and method signatures (method identifier, return type, parameters).
        public interface Animal {
            public void eat();
            public void sleep();
        }

        public class Cat implements Animal {
            @Override
            public void eat() {
                System.out.println("Cat is eating.");
            }

            @Override
            public void sleep() {
                System.out.println("Cat is sleeping.");
            }
        }


        But why not use an abstract class instead of interfaces? 
            1) The class that implements the interface can extend another class.
            2) The interface may be a type for a broad set of objects that don't necessarily have a parent-child relationship.
        */




        /* __________Singleton Pattern__________
        The singleton pattern is used when we want to ensure that there is only one instance of a class.
        This is useful for classes that are used to access a database, utils, or for logging.
        
        class Utils {

            // The single instance of the class is stored in a private static attribute:
            private static Utils instance = null;

            private Utils(){
                // Instantiation code goes here...
            }

            public static Utils getInstance() {
                // Note that the 'this' keyword is not used for static attributes/methods:
                if (instance == null) {
                    instance = new Utils();
                }
                return instance;
            }
        }

        */

        

        /* __________RegEx__________ */

        /* __________Concurrency__________ */






    }
}