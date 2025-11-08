# Design Patterns & SOLID Principles - Java Cheatsheet

## Table of Contents

1. SOLID Principles
2. Gang of Four (GoF) Design Patterns
3. DRY Principle

---

## 1. SOLID PRINCIPLES

### 1.1 Single Responsibility Principle (SRP)

**Definition**: A class should have only one reason to change. Each class should have a single, well-defined responsibility.

**Benefits**:

- Easier to maintain and test
- Reduces code complexity
- Better code organization

**Example - BAD (Violating SRP)**:

```java
public class Employee {
    public void calculateSalary() { /* ... */ }
    public void saveToDatabase() { /* ... */ }
    public void generateReport() { /* ... */ }
    public void sendEmail() { /* ... */ }
}
```

**Example - GOOD (Following SRP)**:

```java
public class Employee {
    private String name;
    private double salary;

    public void calculateSalary() { /* ... */ }
}

public class EmployeeRepository {
    public void saveToDatabase(Employee employee) { /* ... */ }
}

public class ReportGenerator {
    public void generateReport(Employee employee) { /* ... */ }
}

public class EmailService {
    public void sendEmail(String recipient, String message) { /* ... */ }
}
```

---

### 1.2 Open/Closed Principle (OCP)

**Definition**: Software entities should be open for extension but closed for modification.

**Benefits**:

- Code remains stable when adding new features
- Reduces risk of breaking existing functionality
- Promotes use of abstractions

**Example - BAD (Violating OCP)**:

```java
class VehicleCalculations {
    public double calculateValue(Vehicle vehicle) {
        if (vehicle instanceof Car) {
            return vehicle.getValue() * 0.8;
        } else if (vehicle instanceof Truck) {
            return vehicle.getValue() * 0.7;
        }
        return 0;
    }
}
```

**Example - GOOD (Following OCP)**:

```java
// Using abstraction and polymorphism
abstract class Vehicle {
    public abstract double calculateValue();
}

class Car extends Vehicle {
    @Override
    public double calculateValue() {
        return getValue() * 0.8;
    }
}

class Truck extends Vehicle {
    @Override
    public double calculateValue() {
        return getValue() * 0.7;
    }
}

class VehicleCalculations {
    public double calculateValue(Vehicle vehicle) {
        return vehicle.calculateValue(); // No modification needed for new types
    }
}
```

---

### 1.3 Liskov Substitution Principle (LSP)

**Definition**: Objects of a superclass should be replaceable with objects of its subclasses without breaking the application.

**Benefits**:

- Enhanced code reusability
- Improved maintainability
- Prevents runtime errors

**Example - BAD (Violating LSP)**:

```java
class Bird {
    public void fly() {
        System.out.println("Bird is flying");
    }
}

class Sparrow extends Bird {
    @Override
    public void fly() {
        System.out.println("Sparrow is flying");
    }
}

class Penguin extends Bird {
    @Override
    public void fly() {
        throw new UnsupportedOperationException("Penguins can't fly");
    }
}
```

**Example - GOOD (Following LSP)**:

```java
abstract class Bird {
    public abstract void move();
}

class FlyingBird extends Bird {
    @Override
    public void move() {
        fly();
    }

    public void fly() {
        System.out.println("Flying in the sky");
    }
}

class Sparrow extends FlyingBird {
    @Override
    public void fly() {
        System.out.println("Sparrow is flying");
    }
}

class Penguin extends Bird {
    @Override
    public void move() {
        swim();
    }

    public void swim() {
        System.out.println("Penguin is swimming");
    }
}
```

---

### 1.4 Interface Segregation Principle (ISP)

**Definition**: Clients should not be forced to depend on interfaces they do not use. Create smaller, specific interfaces.

**Benefits**:

- Improved maintainability
- Enhanced flexibility
- Increased reusability

**Example - BAD (Violating ISP)**:

```java
interface Worker {
    void work();
    void eat();
    void sleep();
}

class Developer implements Worker {
    @Override
    public void work() {
        System.out.println("Developer is coding");
    }

    @Override
    public void eat() {
        System.out.println("Developer is eating");
    }

    @Override
    public void sleep() {
        System.out.println("Developer is sleeping");
    }
}

class Robot implements Worker {
    @Override
    public void work() {
        System.out.println("Robot is working");
    }

    @Override
    public void eat() {
        throw new UnsupportedOperationException("Robot does not eat");
    }

    @Override
    public void sleep() {
        throw new UnsupportedOperationException("Robot does not sleep");
    }
}
```

**Example - GOOD (Following ISP)**:

```java
interface Workable {
    void work();
}

interface Eatable {
    void eat();
}

interface Sleepable {
    void sleep();
}

class Developer implements Workable, Eatable, Sleepable {
    @Override
    public void work() {
        System.out.println("Developer is coding");
    }

    @Override
    public void eat() {
        System.out.println("Developer is eating");
    }

    @Override
    public void sleep() {
        System.out.println("Developer is sleeping");
    }
}

class Robot implements Workable {
    @Override
    public void work() {
        System.out.println("Robot is working");
    }
}
```

---

### 1.5 Dependency Inversion Principle (DIP)

**Definition**: High-level modules should not depend on low-level modules. Both should depend on abstractions.

**Benefits**:

- Loose coupling between components
- Enhanced flexibility
- Improved testability

**Example - BAD (Violating DIP)**:

```java
class MySQLDatabase {
    public void connect() {
        System.out.println("Connecting to MySQL database");
    }
}

class DatabaseService {
    private MySQLDatabase database;

    public DatabaseService() {
        this.database = new MySQLDatabase(); // Tight coupling
    }

    public void fetchData() {
        database.connect();
        System.out.println("Fetching data from MySQL");
    }
}
```

**Example - GOOD (Following DIP)**:

```java
// Abstraction
interface Database {
    void connect();
}

// Low-level modules
class MySQLDatabase implements Database {
    @Override
    public void connect() {
        System.out.println("Connecting to MySQL database");
    }
}

class PostgreSQLDatabase implements Database {
    @Override
    public void connect() {
        System.out.println("Connecting to PostgreSQL database");
    }
}

// High-level module
class DatabaseService {
    private Database database;

    // Dependency injection through constructor
    public DatabaseService(Database database) {
        this.database = database;
    }

    public void fetchData() {
        database.connect();
        System.out.println("Fetching data");
    }
}

// Usage
public class Main {
    public static void main(String[] args) {
        Database mysql = new MySQLDatabase();
        DatabaseService service = new DatabaseService(mysql);
        service.fetchData();

        // Easy to switch databases
        Database postgres = new PostgreSQLDatabase();
        DatabaseService service2 = new DatabaseService(postgres);
        service2.fetchData();
    }
}
```

---

## 2. GANG OF FOUR (GoF) DESIGN PATTERNS

### 2.1 CREATIONAL PATTERNS

#### 2.1.1 Singleton Pattern

**Purpose**: Ensure only one instance of a class exists and provide global access to it.

**Use Cases**: Database connections, logging, configuration managers

**Implementation**:

```java
public class Singleton {
    // Static variable to hold single instance
    private static Singleton instance = null;

    // Private constructor prevents instantiation
    private Singleton() {
        System.out.println("Singleton instance created");
    }

    // Thread-safe getInstance method
    public static synchronized Singleton getInstance() {
        if (instance == null) {
            instance = new Singleton();
        }
        return instance;
    }

    public void showMessage() {
        System.out.println("Hello from Singleton!");
    }
}

// Usage
public class Main {
    public static void main(String[] args) {
        Singleton s1 = Singleton.getInstance();
        Singleton s2 = Singleton.getInstance();

        System.out.println(s1 == s2); // true - same instance
    }
}
```

**Eager Initialization (Thread-safe)**:

```java
public class Singleton {
    private static final Singleton instance = new Singleton();

    private Singleton() {}

    public static Singleton getInstance() {
        return instance;
    }
}
```

---

#### 2.1.2 Factory Pattern

**Purpose**: Create objects without specifying the exact class to create.

**Use Cases**: Object creation logic is complex, need flexibility in object types

**Implementation**:

```java
// Product interface
interface Shape {
    void draw();
}

// Concrete products
class Circle implements Shape {
    @Override
    public void draw() {
        System.out.println("Drawing Circle");
    }
}

class Rectangle implements Shape {
    @Override
    public void draw() {
        System.out.println("Drawing Rectangle");
    }
}

class Square implements Shape {
    @Override
    public void draw() {
        System.out.println("Drawing Square");
    }
}

// Factory class
class ShapeFactory {
    public Shape getShape(String shapeType) {
        if (shapeType == null) {
            return null;
        }

        switch (shapeType.toUpperCase()) {
            case "CIRCLE":
                return new Circle();
            case "RECTANGLE":
                return new Rectangle();
            case "SQUARE":
                return new Square();
            default:
                return null;
        }
    }
}

// Usage
public class Main {
    public static void main(String[] args) {
        ShapeFactory factory = new ShapeFactory();

        Shape circle = factory.getShape("CIRCLE");
        circle.draw();

        Shape rectangle = factory.getShape("RECTANGLE");
        rectangle.draw();
    }
}
```

---

#### 2.1.3 Builder Pattern

**Purpose**: Construct complex objects step by step.

**Use Cases**: Objects with many optional parameters, complex object construction

**Implementation**:

```java
public class User {
    // Required parameters
    private final String firstName;
    private final String lastName;

    // Optional parameters
    private final int age;
    private final String email;
    private final String phone;

    private User(UserBuilder builder) {
        this.firstName = builder.firstName;
        this.lastName = builder.lastName;
        this.age = builder.age;
        this.email = builder.email;
        this.phone = builder.phone;
    }

    // Static nested Builder class
    public static class UserBuilder {
        private final String firstName;
        private final String lastName;
        private int age;
        private String email;
        private String phone;

        public UserBuilder(String firstName, String lastName) {
            this.firstName = firstName;
            this.lastName = lastName;
        }

        public UserBuilder age(int age) {
            this.age = age;
            return this;
        }

        public UserBuilder email(String email) {
            this.email = email;
            return this;
        }

        public UserBuilder phone(String phone) {
            this.phone = phone;
            return this;
        }

        public User build() {
            return new User(this);
        }
    }

    // Getters
    public String getFirstName() { return firstName; }
    public String getLastName() { return lastName; }
    public int getAge() { return age; }
    public String getEmail() { return email; }
    public String getPhone() { return phone; }
}

// Usage
public class Main {
    public static void main(String[] args) {
        User user = new User.UserBuilder("John", "Doe")
                .age(30)
                .email("[email protected]")
                .phone("123-456-7890")
                .build();

        System.out.println(user.getFirstName() + " " + user.getEmail());
    }
}
```

---

### 2.2 STRUCTURAL PATTERNS

#### 2.2.1 Adapter Pattern

**Purpose**: Allow incompatible interfaces to work together.

**Use Cases**: Integrate legacy code, work with third-party libraries

**Implementation**:

```java
// Target interface
interface Printer {
    void print();
}

// Adaptee (existing incompatible class)
class LegacyPrinter {
    public void printDocument() {
        System.out.println("Legacy Printer is printing document");
    }
}

// Adapter
class PrinterAdapter implements Printer {
    private LegacyPrinter legacyPrinter;

    public PrinterAdapter() {
        this.legacyPrinter = new LegacyPrinter();
    }

    @Override
    public void print() {
        legacyPrinter.printDocument();
    }
}

// Usage
public class Main {
    public static void main(String[] args) {
        Printer printer = new PrinterAdapter();
        printer.print(); // Uses legacy printer through adapter
    }
}
```

---

#### 2.2.2 Decorator Pattern

**Purpose**: Add new functionality to objects dynamically without altering their structure.

**Use Cases**: Add responsibilities to individual objects, flexible alternative to subclassing

**Implementation**:

```java
// Component interface
interface Coffee {
    String getDescription();
    double getCost();
}

// Concrete component
class SimpleCoffee implements Coffee {
    @Override
    public String getDescription() {
        return "Simple Coffee";
    }

    @Override
    public double getCost() {
        return 2.0;
    }
}

// Decorator abstract class
abstract class CoffeeDecorator implements Coffee {
    protected Coffee decoratedCoffee;

    public CoffeeDecorator(Coffee coffee) {
        this.decoratedCoffee = coffee;
    }

    @Override
    public String getDescription() {
        return decoratedCoffee.getDescription();
    }

    @Override
    public double getCost() {
        return decoratedCoffee.getCost();
    }
}

// Concrete decorators
class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) {
        super(coffee);
    }

    @Override
    public String getDescription() {
        return decoratedCoffee.getDescription() + ", Milk";
    }

    @Override
    public double getCost() {
        return decoratedCoffee.getCost() + 0.5;
    }
}

class SugarDecorator extends CoffeeDecorator {
    public SugarDecorator(Coffee coffee) {
        super(coffee);
    }

    @Override
    public String getDescription() {
        return decoratedCoffee.getDescription() + ", Sugar";
    }

    @Override
    public double getCost() {
        return decoratedCoffee.getCost() + 0.2;
    }
}

// Usage
public class Main {
    public static void main(String[] args) {
        Coffee coffee = new SimpleCoffee();
        System.out.println(coffee.getDescription() + " $" + coffee.getCost());

        // Add milk
        coffee = new MilkDecorator(coffee);
        System.out.println(coffee.getDescription() + " $" + coffee.getCost());

        // Add sugar
        coffee = new SugarDecorator(coffee);
        System.out.println(coffee.getDescription() + " $" + coffee.getCost());
    }
}
```

---

### 2.3 BEHAVIORAL PATTERNS

#### 2.3.1 Strategy Pattern

**Purpose**: Define a family of algorithms, encapsulate each one, and make them interchangeable.

**Use Cases**: Multiple algorithms for a task, runtime algorithm selection

**Implementation**:

```java
// Strategy interface
interface PaymentStrategy {
    void pay(int amount);
}

// Concrete strategies
class CreditCardStrategy implements PaymentStrategy {
    private String name;
    private String cardNumber;

    public CreditCardStrategy(String name, String cardNumber) {
        this.name = name;
        this.cardNumber = cardNumber;
    }

    @Override
    public void pay(int amount) {
        System.out.println(amount + " paid with credit card");
    }
}

class PayPalStrategy implements PaymentStrategy {
    private String email;

    public PayPalStrategy(String email) {
        this.email = email;
    }

    @Override
    public void pay(int amount) {
        System.out.println(amount + " paid using PayPal");
    }
}

// Context class
class ShoppingCart {
    private PaymentStrategy paymentStrategy;

    public void setPaymentStrategy(PaymentStrategy strategy) {
        this.paymentStrategy = strategy;
    }

    public void checkout(int amount) {
        paymentStrategy.pay(amount);
    }
}

// Usage
public class Main {
    public static void main(String[] args) {
        ShoppingCart cart = new ShoppingCart();

        // Pay with credit card
        cart.setPaymentStrategy(new CreditCardStrategy("John Doe", "1234-5678-9012-3456"));
        cart.checkout(100);

        // Pay with PayPal
        cart.setPaymentStrategy(new PayPalStrategy("[email protected]"));
        cart.checkout(200);
    }
}
```

---

#### 2.3.2 Observer Pattern

**Purpose**: Define one-to-many dependency so when one object changes state, all dependents are notified.

**Use Cases**: Event handling, publish-subscribe systems

**Implementation**:

```java
import java.util.ArrayList;
import java.util.List;

// Subject interface
interface Subject {
    void attach(Observer observer);
    void detach(Observer observer);
    void notifyObservers();
}

// Observer interface
interface Observer {
    void update(String message);
}

// Concrete Subject
class NewsAgency implements Subject {
    private List<Observer> observers = new ArrayList<>();
    private String news;

    @Override
    public void attach(Observer observer) {
        observers.add(observer);
    }

    @Override
    public void detach(Observer observer) {
        observers.remove(observer);
    }

    @Override
    public void notifyObservers() {
        for (Observer observer : observers) {
            observer.update(news);
        }
    }

    public void setNews(String news) {
        this.news = news;
        notifyObservers();
    }
}

// Concrete Observers
class NewsChannel implements Observer {
    private String name;

    public NewsChannel(String name) {
        this.name = name;
    }

    @Override
    public void update(String news) {
        System.out.println(name + " received news: " + news);
    }
}

// Usage
public class Main {
    public static void main(String[] args) {
        NewsAgency agency = new NewsAgency();

        NewsChannel channel1 = new NewsChannel("Channel 1");
        NewsChannel channel2 = new NewsChannel("Channel 2");

        agency.attach(channel1);
        agency.attach(channel2);

        agency.setNews("Breaking: New design pattern discovered!");
    }
}
```

---

#### 2.3.3 Template Method Pattern

**Purpose**: Define the skeleton of an algorithm, deferring some steps to subclasses.

**Use Cases**: Common algorithm structure with varying implementations

**Implementation**:

```java
// Abstract class with template method
abstract class BeveragePreparation {
    // Template method - final to prevent override
    public final void prepareBeverage() {
        boilWater();
        brew();
        pourInCup();
        addCondiments();
    }

    private void boilWater() {
        System.out.println("Boiling water");
    }

    private void pourInCup() {
        System.out.println("Pouring into cup");
    }

    // Abstract methods to be implemented by subclasses
    protected abstract void brew();
    protected abstract void addCondiments();
}

// Concrete implementations
class Tea extends BeveragePreparation {
    @Override
    protected void brew() {
        System.out.println("Steeping the tea");
    }

    @Override
    protected void addCondiments() {
        System.out.println("Adding lemon");
    }
}

class Coffee extends BeveragePreparation {
    @Override
    protected void brew() {
        System.out.println("Dripping coffee through filter");
    }

    @Override
    protected void addCondiments() {
        System.out.println("Adding sugar and milk");
    }
}

// Usage
public class Main {
    public static void main(String[] args) {
        BeveragePreparation tea = new Tea();
        tea.prepareBeverage();

        System.out.println();

        BeveragePreparation coffee = new Coffee();
        coffee.prepareBeverage();
    }
}
```

---

## 3. DRY PRINCIPLE (Don't Repeat Yourself)

**Definition**: Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

**Benefits**:

- Reduces code redundancy
- Easier maintenance
- Better code reusability
- Single source of truth

**Example - BAD (Violating DRY)**:

```java
public class Departments {
    public void displayCSE() {
        System.out.println("This is Computer Science");
        System.out.println("IIT - Madras");
    }

    public void displayECE() {
        System.out.println("This is Electronics");
        System.out.println("IIT - Madras");
    }

    public void displayIT() {
        System.out.println("This is Information Technology");
        System.out.println("IIT - Madras");
    }
}
```

**Example - GOOD (Following DRY)**:

```java
public class Departments {
    // Common method - single source of truth
    private void displayCollege() {
        System.out.println("IIT - Madras");
    }

    public void displayCSE() {
        System.out.println("This is Computer Science");
        displayCollege(); // Reuse
    }

    public void displayECE() {
        System.out.println("This is Electronics");
        displayCollege(); // Reuse
    }

    public void displayIT() {
        System.out.println("This is Information Technology");
        displayCollege(); // Reuse
    }
}
```

**Advanced DRY Example**:

```java
public class DataValidator {
    // Reusable validation methods
    public boolean isValidEmail(String email) {
        return email != null && email.matches("^[A-Za-z0-9+_.-]+@(.+)$");
    }

    public boolean isValidPhone(String phone) {
        return phone != null && phone.matches("\\d{10}");
    }
}

public class UserService {
    private DataValidator validator = new DataValidator();

    public void registerUser(String email, String phone) {
        if (!validator.isValidEmail(email)) {
            throw new IllegalArgumentException("Invalid email");
        }
        if (!validator.isValidPhone(phone)) {
            throw new IllegalArgumentException("Invalid phone");
        }
        // Registration logic
    }
}

public class EmployeeService {
    private DataValidator validator = new DataValidator();

    public void addEmployee(String email, String phone) {
        if (!validator.isValidEmail(email)) {
            throw new IllegalArgumentException("Invalid email");
        }
        if (!validator.isValidPhone(phone)) {
            throw new IllegalArgumentException("Invalid phone");
        }
        // Employee addition logic
    }
}
```

---

## QUICK REFERENCE TABLE

### GoF Patterns Summary

| Pattern         | Type       | Purpose                           | Use When                                 |
| --------------- | ---------- | --------------------------------- | ---------------------------------------- |
| Singleton       | Creational | One instance only                 | Need global access point                 |
| Factory         | Creational | Object creation                   | Don't know exact type at compile time    |
| Builder         | Creational | Complex object construction       | Many optional parameters                 |
| Adapter         | Structural | Make incompatible interfaces work | Integrate legacy/third-party code        |
| Decorator       | Structural | Add functionality dynamically     | Need flexible alternative to subclassing |
| Strategy        | Behavioral | Interchangeable algorithms        | Multiple algorithms for same task        |
| Observer        | Behavioral | Notify dependents of changes      | Event-driven systems                     |
| Template Method | Behavioral | Algorithm skeleton                | Common structure, varying steps          |

### SOLID Principles Summary

| Principle | Key Concept                                 | Solution                          |
| --------- | ------------------------------------------- | --------------------------------- |
| SRP       | One responsibility per class                | Split classes by responsibility   |
| OCP       | Open for extension, closed for modification | Use abstractions and polymorphism |
| LSP       | Subclasses should be substitutable          | Maintain behavioral consistency   |
| ISP       | No forced dependencies                      | Create small, focused interfaces  |
| DIP       | Depend on abstractions                      | Use dependency injection          |

---

## BEST PRACTICES

1. **Always favor composition over inheritance**
2. **Program to an interface, not an implementation**
3. **Encapsulate what varies**
4. **Strive for loosely coupled designs**
5. **Classes should be open for extension but closed for modification**
6. **Depend on abstractions, not concrete classes**

---

_This cheatsheet covers the core Design Patterns and SOLID Principles with practical Java examples for interview preparation._
