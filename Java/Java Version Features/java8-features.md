# Java 8 Features — Complete Interview Guide

> **Java 8 (JDK 1.8)** was released on **March 18, 2014**. It is one of the most significant releases in Java's history, introducing **functional programming** paradigms, a new **Date/Time API**, **Streams**, **Lambdas**, and much more.

---

## Table of Contents

1. [Lambda Expressions](#1-lambda-expressions)
2. [Functional Interfaces](#2-functional-interfaces)
3. [Method References](#3-method-references)
4. [Stream API](#4-stream-api)
5. [Default and Static Methods in Interfaces](#5-default-and-static-methods-in-interfaces)
6. [Optional Class](#6-optional-class)
7. [New Date and Time API (java.time)](#7-new-date-and-time-api-javatime)
8. [Nashorn JavaScript Engine](#8-nashorn-javascript-engine)
9. [forEach() Method](#9-foreach-method)
10. [StringJoiner Class](#10-stringjoiner-class)
11. [Collectors Class](#11-collectors-class)
12. [Parallel Streams](#12-parallel-streams)
13. [Type Annotations and Repeating Annotations](#13-type-annotations-and-repeating-annotations)
14. [CompletableFuture](#14-completablefuture)
15. [Base64 Encoding and Decoding](#15-base64-encoding-and-decoding)
16. [Map API Enhancements](#16-map-api-enhancements)
17. [Concurrency API Enhancements](#17-concurrency-api-enhancements)
18. [IO/NIO Enhancements](#18-ionio-enhancements)
19. [Miscellaneous Enhancements](#19-miscellaneous-enhancements)
20. [Interview Questions & Answers](#20-top-interview-questions--answers)

---

## 1. Lambda Expressions

### What is a Lambda Expression?

A **lambda expression** is an anonymous function (a function with no name, no return type, and no access modifier). It provides a clear and concise way to implement **Single Abstract Method (SAM)** interfaces using an expression. It enables **functional programming** in Java.

### Syntax

```
(parameters) -> expression
(parameters) -> { statements; }
```

### Key Points (Interview)

- Lambda expressions are used to implement **functional interfaces**.
- The type of a lambda is inferred by the compiler (**target typing**).
- Lambda expressions can access **effectively final** local variables from the enclosing scope.
- `this` keyword inside a lambda refers to the **enclosing class** instance, NOT the lambda itself.
- Lambdas do **NOT** create a new scope; they share the scope of the enclosing block.
- Lambdas can throw **checked exceptions** only if the functional interface's abstract method declares them.

### Examples

```java
// 1. No parameter
Runnable r = () -> System.out.println("Hello Lambda!");
r.run();

// 2. Single parameter (parentheses optional)
Consumer<String> greet = name -> System.out.println("Hello " + name);
greet.accept("Java");

// 3. Multiple parameters
Comparator<Integer> comp = (a, b) -> a.compareTo(b);

// 4. With block body and return
BiFunction<Integer, Integer, Integer> add = (a, b) -> {
    int sum = a + b;
    return sum;
};

// 5. Using in Collections
List<String> names = Arrays.asList("Charlie", "Alice", "Bob");
names.sort((s1, s2) -> s1.compareTo(s2));

// 6. Lambda with Thread
new Thread(() -> System.out.println("Running in thread")).start();

// 7. Effectively final variable access
int factor = 2; // effectively final
Function<Integer, Integer> multiplier = n -> n * factor;
// factor = 3; // ERROR: local variables referenced from lambda must be final or effectively final
```

### Lambda vs Anonymous Inner Class

| Feature | Lambda Expression | Anonymous Inner Class |
|---|---|---|
| Applicable to | Functional interfaces only | Any interface or abstract class |
| `this` keyword | Refers to enclosing class | Refers to anonymous class itself |
| Compilation | Generates `invokedynamic` bytecode | Generates a separate `.class` file |
| State | Stateless (no instance variables) | Can have instance variables |
| Verbosity | Concise | Verbose |
| Shadowing | Cannot shadow enclosing scope variables | Can shadow enclosing scope variables |

---

## 2. Functional Interfaces

### What is a Functional Interface?

A functional interface is an interface that contains **exactly one abstract method**. It may contain any number of **default** and **static** methods. The `@FunctionalInterface` annotation is optional but recommended for compile-time validation.

### Key Points (Interview)

- `@FunctionalInterface` annotation triggers a **compile-time error** if the interface has more than one abstract method.
- Methods inherited from `java.lang.Object` (like `equals()`, `hashCode()`, `toString()`) do **NOT count** as abstract methods.
- Functional interfaces are the **target types** for lambda expressions and method references.
- A functional interface can **extend** another interface only if the parent doesn't add any new abstract methods (or adds the same abstract method).

### Built-in Functional Interfaces (java.util.function)

#### 1. Predicate\<T>

- Abstract method: `boolean test(T t)`
- Used for: **conditional checks / filtering**

```java
Predicate<Integer> isEven = n -> n % 2 == 0;
System.out.println(isEven.test(4));     // true
System.out.println(isEven.test(5));     // false

// Composed predicates
Predicate<Integer> isPositive = n -> n > 0;
Predicate<Integer> isPositiveAndEven = isPositive.and(isEven);
Predicate<Integer> isNotEven = isEven.negate();
Predicate<Integer> isEvenOrPositive = isEven.or(isPositive);

// Static method
Predicate<String> isEqual = Predicate.isEqual("Java");
System.out.println(isEqual.test("Java"));   // true
```

#### 2. Function\<T, R>

- Abstract method: `R apply(T t)`
- Used for: **transformations**

```java
Function<String, Integer> length = String::length;
System.out.println(length.apply("Lambda")); // 6

// Compose & andThen
Function<Integer, Integer> doubleIt = n -> n * 2;
Function<Integer, Integer> square = n -> n * n;

Function<Integer, Integer> doubleThenSquare = doubleIt.andThen(square); // first double, then square
System.out.println(doubleThenSquare.apply(3)); // (3*2)^2 = 36

Function<Integer, Integer> squareThenDouble = doubleIt.compose(square); // first square, then double
System.out.println(squareThenDouble.apply(3)); // (3^2)*2 = 18

// Identity function
Function<String, String> identity = Function.identity();
```

#### 3. Consumer\<T>

- Abstract method: `void accept(T t)`
- Used for: **performing actions** on input (no return)

```java
Consumer<String> print = System.out::println;
print.accept("Hello Consumer!");

// andThen
Consumer<String> upper = s -> System.out.println(s.toUpperCase());
Consumer<String> lower = s -> System.out.println(s.toLowerCase());
upper.andThen(lower).accept("Java"); // JAVA then java
```

#### 4. Supplier\<T>

- Abstract method: `T get()`
- Used for: **lazy generation / factory** (no input, returns value)

```java
Supplier<Double> randomValue = Math::random;
System.out.println(randomValue.get());

Supplier<List<String>> listFactory = ArrayList::new;
List<String> newList = listFactory.get();

Supplier<LocalDate> today = LocalDate::now;
```

#### 5. BiPredicate\<T, U>

```java
BiPredicate<String, Integer> checkLength = (str, len) -> str.length() == len;
System.out.println(checkLength.test("Java", 4)); // true
```

#### 6. BiFunction\<T, U, R>

```java
BiFunction<Integer, Integer, String> addToStr = (a, b) -> "Sum: " + (a + b);
System.out.println(addToStr.apply(10, 20)); // Sum: 30
```

#### 7. BiConsumer\<T, U>

```java
BiConsumer<String, Integer> printEntry = (k, v) -> System.out.println(k + "=" + v);
Map<String, Integer> map = Map.of("a", 1, "b", 2);
map.forEach(printEntry);
```

#### 8. UnaryOperator\<T> (extends Function\<T, T>)

```java
UnaryOperator<String> toUpper = String::toUpperCase;
System.out.println(toUpper.apply("hello")); // HELLO
```

#### 9. BinaryOperator\<T> (extends BiFunction\<T, T, T>)

```java
BinaryOperator<Integer> max = BinaryOperator.maxBy(Comparator.naturalOrder());
System.out.println(max.apply(10, 20)); // 20

BinaryOperator<Integer> sum = Integer::sum;
System.out.println(sum.apply(5, 3)); // 8
```

#### Primitive Specialized Functional Interfaces

Avoid autoboxing overhead:

| Interface | Abstract Method |
|---|---|
| `IntPredicate` | `boolean test(int value)` |
| `LongPredicate` | `boolean test(long value)` |
| `DoublePredicate` | `boolean test(double value)` |
| `IntFunction<R>` | `R apply(int value)` |
| `IntConsumer` | `void accept(int value)` |
| `IntSupplier` | `int getAsInt()` |
| `IntUnaryOperator` | `int applyAsInt(int operand)` |
| `IntBinaryOperator` | `int applyAsInt(int left, int right)` |
| `IntToDoubleFunction` | `double applyAsDouble(int value)` |
| `IntToLongFunction` | `long applyAsLong(int value)` |
| `ToIntFunction<T>` | `int applyAsInt(T value)` |
| `ObjIntConsumer<T>` | `void accept(T t, int value)` |

### Custom Functional Interface

```java
@FunctionalInterface
interface MathOperation {
    double operate(double a, double b);

    // Allowed: default method
    default MathOperation andThen(Function<Double, Double> after) {
        return (a, b) -> after.apply(this.operate(a, b));
    }

    // Allowed: static method
    static MathOperation add() {
        return (a, b) -> a + b;
    }
}

// Usage
MathOperation addition = (a, b) -> a + b;
MathOperation multiplication = (a, b) -> a * b;
System.out.println(addition.operate(10, 5));        // 15.0
System.out.println(multiplication.operate(10, 5));  // 50.0
```

---

## 3. Method References

### What is a Method Reference?

A **method reference** is a shorthand notation of a lambda expression that calls an **existing method**. It uses the `::` operator. Method references make the code more readable when the lambda body merely delegates to an existing method.

### Types of Method References

#### 1. Reference to a Static Method — `ClassName::staticMethodName`

```java
// Lambda
Function<String, Integer> parser1 = s -> Integer.parseInt(s);

// Method Reference
Function<String, Integer> parser2 = Integer::parseInt;

System.out.println(parser2.apply("100")); // 100

// Sorting with static method reference
List<Integer> numbers = Arrays.asList(3, 1, 4, 1, 5);
numbers.sort(Integer::compare);
```

#### 2. Reference to an Instance Method of a Particular Object — `object::instanceMethodName`

```java
String greeting = "Hello, World!";
Supplier<Integer> lengthSupplier = greeting::length;
System.out.println(lengthSupplier.get()); // 13

Consumer<String> printer = System.out::println;
printer.accept("Method Reference!");

List<String> names = Arrays.asList("Alice", "Bob");
names.forEach(System.out::println);
```

#### 3. Reference to an Instance Method of an Arbitrary Object of a Particular Type — `ClassName::instanceMethodName`

```java
// Lambda
Function<String, String> upper1 = s -> s.toUpperCase();

// Method Reference
Function<String, String> upper2 = String::toUpperCase;

// Used as Comparator
List<String> names = Arrays.asList("Charlie", "Alice", "Bob");
names.sort(String::compareToIgnoreCase);

// BiPredicate example
BiPredicate<String, String> checker = String::startsWith;
System.out.println(checker.test("Java", "Ja")); // true
```

#### 4. Reference to a Constructor — `ClassName::new`

```java
// No-arg constructor
Supplier<ArrayList<String>> listCreator = ArrayList::new;
List<String> list = listCreator.get();

// Parameterized constructor
Function<String, StringBuilder> sbCreator = StringBuilder::new;
StringBuilder sb = sbCreator.apply("Hello");

// Array constructor reference
Function<Integer, String[]> arrayCreator = String[]::new;
String[] arr = arrayCreator.apply(5); // creates String[5]

// Useful with streams
List<String> names = Arrays.asList("Alice", "Bob");
List<StringBuilder> builders = names.stream()
    .map(StringBuilder::new)
    .collect(Collectors.toList());
```

---

## 4. Stream API

### What is a Stream?

A **Stream** (`java.util.stream.Stream`) is a sequence of elements supporting **sequential** and **parallel** aggregate operations. It is **NOT** a data structure — it doesn't store data. It takes input from Collections, Arrays, or I/O channels and processes data through a **pipeline** of operations.

### Key Characteristics (Interview)

- Streams are **lazy** — intermediate operations are not executed until a terminal operation is invoked.
- Streams are **not reusable** — once a terminal operation is performed, the stream is **consumed** and cannot be used again.
- Streams do **NOT modify the source** data structure.
- Streams support both **sequential** and **parallel** execution.
- Stream operations are divided into **intermediate** (return Stream) and **terminal** (produce a result/side-effect).
- Streams use **internal iteration** (the library handles iteration), unlike external iteration with iterators.
- Short-circuit operations: `findFirst()`, `findAny()`, `anyMatch()`, `allMatch()`, `noneMatch()`, `limit()`.

### Creating Streams

```java
// 1. From Collection
List<String> list = Arrays.asList("a", "b", "c");
Stream<String> stream1 = list.stream();
Stream<String> parallelStream = list.parallelStream();

// 2. From Array
String[] arr = {"x", "y", "z"};
Stream<String> stream2 = Arrays.stream(arr);
Stream<String> stream2b = Stream.of(arr);

// 3. Using Stream.of()
Stream<Integer> stream3 = Stream.of(1, 2, 3, 4, 5);

// 4. Using Stream.empty()
Stream<String> emptyStream = Stream.empty();

// 5. Using Stream.builder()
Stream<String> stream4 = Stream.<String>builder()
    .add("a").add("b").add("c")
    .build();

// 6. Using Stream.generate() — infinite stream
Stream<Double> randoms = Stream.generate(Math::random).limit(5);

// 7. Using Stream.iterate() — infinite stream
Stream<Integer> evens = Stream.iterate(0, n -> n + 2).limit(10);

// 8. From String (chars)
IntStream chars = "Hello".chars();

// 9. From Files
Stream<String> lines = Files.lines(Paths.get("file.txt"));

// 10. Primitive Streams
IntStream intStream = IntStream.range(1, 5);           // 1, 2, 3, 4
IntStream intStreamClosed = IntStream.rangeClosed(1, 5); // 1, 2, 3, 4, 5
LongStream longStream = LongStream.of(1L, 2L, 3L);
DoubleStream doubleStream = DoubleStream.of(1.1, 2.2);

// 11. Stream.concat()
Stream<String> combined = Stream.concat(stream1, stream2);
```

### Intermediate Operations (Lazy — return Stream)

#### filter(Predicate\<T>)

```java
List<Integer> evens = numbers.stream()
    .filter(n -> n % 2 == 0)
    .collect(Collectors.toList());
```

#### map(Function\<T, R>)

```java
List<String> upperNames = names.stream()
    .map(String::toUpperCase)
    .collect(Collectors.toList());
```

#### flatMap(Function\<T, Stream\<R>>)

Flattens nested structures into a single stream.

```java
List<List<Integer>> nestedList = Arrays.asList(
    Arrays.asList(1, 2, 3),
    Arrays.asList(4, 5, 6),
    Arrays.asList(7, 8, 9)
);
List<Integer> flatList = nestedList.stream()
    .flatMap(Collection::stream)
    .collect(Collectors.toList()); // [1, 2, 3, 4, 5, 6, 7, 8, 9]

// Splitting words
List<String> sentences = Arrays.asList("Hello World", "Java 8");
List<String> words = sentences.stream()
    .flatMap(s -> Arrays.stream(s.split(" ")))
    .collect(Collectors.toList()); // [Hello, World, Java, 8]
```

#### distinct()

```java
List<Integer> unique = Arrays.asList(1, 2, 2, 3, 3, 4).stream()
    .distinct()
    .collect(Collectors.toList()); // [1, 2, 3, 4]
// Uses equals() and hashCode() for object comparison
```

#### sorted() / sorted(Comparator\<T>)

```java
List<String> sorted = names.stream()
    .sorted()                                      // natural order
    .collect(Collectors.toList());

List<String> reverseSorted = names.stream()
    .sorted(Comparator.reverseOrder())
    .collect(Collectors.toList());

List<Employee> byAge = employees.stream()
    .sorted(Comparator.comparing(Employee::getAge))
    .collect(Collectors.toList());

// Multiple sort criteria
List<Employee> bySalaryThenName = employees.stream()
    .sorted(Comparator.comparing(Employee::getSalary)
                       .thenComparing(Employee::getName))
    .collect(Collectors.toList());
```

#### peek(Consumer\<T>)

Used for **debugging** — performs an action on each element without modifying the stream.

```java
List<String> result = names.stream()
    .filter(s -> s.length() > 3)
    .peek(s -> System.out.println("Filtered: " + s))
    .map(String::toUpperCase)
    .peek(s -> System.out.println("Mapped: " + s))
    .collect(Collectors.toList());
```

#### limit(long n) and skip(long n)

```java
// First 3 elements
List<Integer> firstThree = Stream.of(1,2,3,4,5)
    .limit(3)
    .collect(Collectors.toList()); // [1, 2, 3]

// Skip first 2
List<Integer> skipped = Stream.of(1,2,3,4,5)
    .skip(2)
    .collect(Collectors.toList()); // [3, 4, 5]

// Pagination (page 2, size 10)
list.stream().skip(10).limit(10).collect(Collectors.toList());
```

#### mapToInt / mapToLong / mapToDouble

```java
IntStream lengths = names.stream().mapToInt(String::length);
int totalLength = names.stream().mapToInt(String::length).sum();
```

### Terminal Operations (Eager — produce result)

#### collect(Collector)

See [Collectors section](#11-collectors-class).

#### forEach(Consumer\<T>)

```java
names.stream().forEach(System.out::println);
// forEachOrdered() guarantees encounter order in parallel streams
names.parallelStream().forEachOrdered(System.out::println);
```

#### reduce(BinaryOperator\<T>)

```java
// Sum
Optional<Integer> sum = numbers.stream().reduce(Integer::sum);

// Sum with identity
int sum2 = numbers.stream().reduce(0, Integer::sum);

// Max
Optional<Integer> max = numbers.stream().reduce(Integer::max);

// Concatenation
String joined = words.stream().reduce("", (a, b) -> a + " " + b).trim();

// Three-argument reduce (for parallel streams)
int total = numbers.parallelStream()
    .reduce(0,                       // identity
            Integer::sum,            // accumulator
            Integer::sum);           // combiner (for parallel)
```

#### count()

```java
long count = names.stream().filter(s -> s.startsWith("A")).count();
```

#### min(Comparator) / max(Comparator)

```java
Optional<Integer> min = numbers.stream().min(Comparator.naturalOrder());
Optional<String> longest = names.stream().max(Comparator.comparing(String::length));
```

#### findFirst() / findAny()

```java
Optional<String> first = names.stream()
    .filter(s -> s.startsWith("A"))
    .findFirst();

// findAny() is non-deterministic — useful in parallel streams
Optional<String> any = names.parallelStream()
    .filter(s -> s.startsWith("A"))
    .findAny();
```

#### anyMatch / allMatch / noneMatch

```java
boolean hasEven = numbers.stream().anyMatch(n -> n % 2 == 0);
boolean allPositive = numbers.stream().allMatch(n -> n > 0);
boolean noneNegative = numbers.stream().noneMatch(n -> n < 0);
```

#### toArray()

```java
Object[] arr1 = names.stream().toArray();
String[] arr2 = names.stream().toArray(String[]::new);
```

### Primitive Streams — IntStream, LongStream, DoubleStream

```java
// Statistical operations
IntStream intStream = IntStream.of(1, 2, 3, 4, 5);
int sum = intStream.sum();                          // 15
OptionalInt max = IntStream.of(1,2,3).max();        // 3
OptionalDouble avg = IntStream.of(1,2,3).average(); // 2.0

// Summary statistics
IntSummaryStatistics stats = IntStream.of(1, 2, 3, 4, 5).summaryStatistics();
stats.getCount();   // 5
stats.getSum();     // 15
stats.getMin();     // 1
stats.getMax();     // 5
stats.getAverage(); // 3.0

// Boxing / Unboxing
Stream<Integer> boxed = IntStream.of(1,2,3).boxed();
IntStream unboxed = Stream.of(1,2,3).mapToInt(Integer::intValue);

// asLongStream() / asDoubleStream()
LongStream longs = IntStream.of(1,2,3).asLongStream();
DoubleStream doubles = IntStream.of(1,2,3).asDoubleStream();
```

### Stream Pipeline Complete Example

```java
List<Employee> employees = getEmployees();

Map<String, Double> avgSalaryByDept = employees.stream()
    .filter(e -> e.getAge() > 25)
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.averagingDouble(Employee::getSalary)
    ));

// Find second highest salary
Optional<Double> secondHighest = employees.stream()
    .map(Employee::getSalary)
    .distinct()
    .sorted(Comparator.reverseOrder())
    .skip(1)
    .findFirst();
```

---

## 5. Default and Static Methods in Interfaces

### Default Methods

Allow adding **new methods** to interfaces without breaking existing implementations. Enables **backward compatibility** and **interface evolution**.

```java
public interface Vehicle {
    void start();

    // Default method with body
    default void honk() {
        System.out.println("Beep beep!");
    }

    default void stop() {
        System.out.println("Vehicle stopped.");
    }
}

public class Car implements Vehicle {
    @Override
    public void start() {
        System.out.println("Car started");
    }

    // Can optionally override default method
    @Override
    public void honk() {
        System.out.println("Car horn: HOOOONK!");
    }
}
```

### Diamond Problem / Multiple Inheritance Conflict

```java
interface A {
    default void greet() { System.out.println("Hello from A"); }
}

interface B {
    default void greet() { System.out.println("Hello from B"); }
}

// MUST override to resolve ambiguity — otherwise COMPILE ERROR
class C implements A, B {
    @Override
    public void greet() {
        A.super.greet(); // Explicitly call A's version
        // B.super.greet(); // Or call B's version
    }
}
```

### Resolution Rules (Interview)

1. **Class wins** over interface default methods.
2. **Sub-interface wins** over super-interface (most specific interface).
3. If still ambiguous, the class **must explicitly override** and choose which to call using `InterfaceName.super.methodName()`.

### Static Methods in Interfaces

```java
public interface Validator {
    boolean validate(String input);

    // Static method — called via InterfaceName.staticMethod()
    static boolean isNullOrEmpty(String input) {
        return input == null || input.trim().isEmpty();
    }

    // Cannot be overridden by implementing classes
    // Cannot be called via implementation class name
}

// Usage
boolean empty = Validator.isNullOrEmpty(""); // true
```

### Key Interview Points

- Default methods are **inherited**; static methods are **NOT inherited**.
- Default methods can be **overridden**; static methods **cannot**.
- Static methods are called using the **interface name**, not the implementing class name.
- A class can implement multiple interfaces with conflicting default methods but **must override** to resolve the conflict.
- A **concrete class method** always takes priority over a default method.

---

## 6. Optional Class

### What is Optional?

`java.util.Optional<T>` is a **container object** that may or may not contain a non-null value. It was introduced to **avoid NullPointerException** and to express the intent that a value might be absent.

### Key Interview Points

- Optional is meant for **return types**, NOT for method parameters, fields, or collection elements.
- Optional is **not serializable** — do not use as entity fields.
- Encourages **functional-style programming** to handle null gracefully.
- `Optional.of(null)` throws **NullPointerException**; use `Optional.ofNullable(null)` instead.

### Creating Optional

```java
// 1. Empty Optional
Optional<String> empty = Optional.empty();

// 2. Of non-null value — throws NPE if null!
Optional<String> name = Optional.of("Java");

// 3. Of nullable value — handles null safely
Optional<String> nullable = Optional.ofNullable(getSomeValue()); // null-safe
```

### Checking and Retrieving Values

```java
Optional<String> opt = Optional.of("Hello");

// isPresent() — check if value exists
if (opt.isPresent()) {
    System.out.println(opt.get());
}

// ifPresent(Consumer) — execute action if present
opt.ifPresent(System.out::println);

// get() — returns value or throws NoSuchElementException
String val = opt.get(); // AVOID without isPresent() check

// orElse(defaultValue) — return default if empty
String result = opt.orElse("Default");

// orElseGet(Supplier) — lazy default (evaluated only if empty)
String result2 = opt.orElseGet(() -> computeDefault());

// orElseThrow(Supplier) — throw custom exception
String result3 = opt.orElseThrow(() -> new RuntimeException("Not found!"));
// Java 10+: orElseThrow() without argument throws NoSuchElementException
```

### orElse vs orElseGet (Important Interview Question)

```java
// orElse ALWAYS evaluates the argument, even if Optional has a value
Optional<String> opt = Optional.of("Value");
String r1 = opt.orElse(expensiveMethod());        // expensiveMethod() IS called!

// orElseGet evaluates the Supplier ONLY when Optional is empty
String r2 = opt.orElseGet(() -> expensiveMethod()); // expensiveMethod() NOT called
```

### Transforming Optionals

```java
Optional<String> name = Optional.of("java");

// map() — transforms the value if present
Optional<String> upper = name.map(String::toUpperCase); // Optional[JAVA]

// flatMap() — when the mapping function returns an Optional
Optional<Optional<String>> nested = name.map(s -> Optional.of(s.toUpperCase())); // Bad!
Optional<String> flat = name.flatMap(s -> Optional.of(s.toUpperCase()));         // Good!

// filter() — returns Optional if value matches predicate
Optional<String> filtered = name.filter(s -> s.length() > 3);
```

### Chaining Optionals — Avoiding Null Checks

```java
// Before Java 8 (nested null checks)
if (user != null) {
    Address addr = user.getAddress();
    if (addr != null) {
        String city = addr.getCity();
        if (city != null) {
            System.out.println(city.toUpperCase());
        }
    }
}

// Java 8 with Optional
Optional.ofNullable(user)
    .map(User::getAddress)
    .map(Address::getCity)
    .map(String::toUpperCase)
    .ifPresent(System.out::println);
```

### Optional with Streams

```java
// Stream of Optionals -> filter empty ones
List<Optional<String>> optionals = Arrays.asList(
    Optional.of("A"), Optional.empty(), Optional.of("C")
);

List<String> values = optionals.stream()
    .filter(Optional::isPresent)
    .map(Optional::get)
    .collect(Collectors.toList()); // [A, C]

// Java 9+: Optional.stream()
// List<String> values = optionals.stream()
//     .flatMap(Optional::stream)
//     .collect(Collectors.toList());
```

---

## 7. New Date and Time API (java.time)

### Why New API? (Interview)

Problems with the old `java.util.Date` and `java.util.Calendar`:

- **Not thread-safe** — `Date` and `SimpleDateFormat` are mutable.
- **Poor API design** — months are 0-indexed, years start from 1900.
- **Lack of timezone handling** — confusing and error-prone.
- **Mutable** — can be modified after creation.

The new `java.time` package (JSR 310, inspired by **Joda-Time**):

- **Immutable and thread-safe** — all classes are immutable.
- **Clear and intuitive** API.
- **ISO 8601** standard by default.
- Separation of concerns: date-only, time-only, date-time, zoned, etc.

### Core Classes

#### LocalDate — Date without time or timezone

```java
LocalDate today = LocalDate.now();                         // 2024-03-15
LocalDate specific = LocalDate.of(2024, Month.MARCH, 15); // 2024-03-15
LocalDate parsed = LocalDate.parse("2024-03-15");          // ISO format

// Getters
int year = today.getYear();
Month month = today.getMonth();
int dayOfMonth = today.getDayOfMonth();
DayOfWeek dayOfWeek = today.getDayOfWeek();
int dayOfYear = today.getDayOfYear();
int lengthOfMonth = today.lengthOfMonth();
boolean isLeap = today.isLeapYear();

// Manipulation (returns new instance — immutable!)
LocalDate tomorrow = today.plusDays(1);
LocalDate lastMonth = today.minusMonths(1);
LocalDate nextYear = today.plusYears(1);
LocalDate adjusted = today.withMonth(6).withDayOfMonth(1);

// Comparison
boolean isBefore = today.isBefore(tomorrow); // true
boolean isAfter = today.isAfter(tomorrow);   // false
boolean isEqual = today.isEqual(today);       // true
```

#### LocalTime — Time without date or timezone

```java
LocalTime now = LocalTime.now();                    // 14:30:15.123
LocalTime specific = LocalTime.of(14, 30, 15);     // 14:30:15
LocalTime parsed = LocalTime.parse("14:30:15");
LocalTime midnight = LocalTime.MIDNIGHT;            // 00:00
LocalTime noon = LocalTime.NOON;                    // 12:00
LocalTime max = LocalTime.MAX;                      // 23:59:59.999999999
LocalTime min = LocalTime.MIN;                      // 00:00

int hour = now.getHour();
int minute = now.getMinute();
int second = now.getSecond();
int nano = now.getNano();

LocalTime later = now.plusHours(2).plusMinutes(30);
```

#### LocalDateTime — Date and time without timezone

```java
LocalDateTime now = LocalDateTime.now();
LocalDateTime specific = LocalDateTime.of(2024, 3, 15, 14, 30, 0);
LocalDateTime combined = LocalDateTime.of(LocalDate.now(), LocalTime.now());
LocalDateTime parsed = LocalDateTime.parse("2024-03-15T14:30:00");

// Convert
LocalDate date = now.toLocalDate();
LocalTime time = now.toLocalTime();
```

#### ZonedDateTime — Date-time with timezone

```java
ZonedDateTime now = ZonedDateTime.now();
ZonedDateTime inTokyo = ZonedDateTime.now(ZoneId.of("Asia/Tokyo"));
ZonedDateTime specific = ZonedDateTime.of(
    LocalDateTime.of(2024, 3, 15, 14, 30),
    ZoneId.of("America/New_York")
);

// Convert between timezones
ZonedDateTime tokyoTime = now.withZoneSameInstant(ZoneId.of("Asia/Tokyo"));

// All available zone IDs
Set<String> allZones = ZoneId.getAvailableZoneIds();

ZoneId zone = ZoneId.of("US/Eastern");
ZoneOffset offset = ZoneOffset.of("+05:30");
```

#### Instant — Machine timestamp (epoch-based)

```java
Instant now = Instant.now();                          // UTC timestamp
Instant epoch = Instant.EPOCH;                        // 1970-01-01T00:00:00Z
Instant fromEpochSecond = Instant.ofEpochSecond(1000000);
Instant fromEpochMilli = Instant.ofEpochMilli(System.currentTimeMillis());

long epochSecond = now.getEpochSecond();
int nano = now.getNano();
long epochMilli = now.toEpochMilli();

// Convert to ZonedDateTime
ZonedDateTime zdt = now.atZone(ZoneId.of("UTC"));
```

#### Duration — Time-based amount (hours, minutes, seconds)

```java
Duration d1 = Duration.between(time1, time2);
Duration d2 = Duration.ofHours(2);
Duration d3 = Duration.ofMinutes(30);
Duration d4 = Duration.ofSeconds(120);
Duration d5 = Duration.parse("PT2H30M"); // ISO-8601

long hours = d1.toHours();
long minutes = d1.toMinutes();
long seconds = d1.getSeconds();
```

#### Period — Date-based amount (years, months, days)

```java
Period p1 = Period.between(date1, date2);
Period p2 = Period.of(1, 6, 15);    // 1 year, 6 months, 15 days
Period p3 = Period.ofMonths(3);
Period p4 = Period.parse("P1Y6M15D");

int years = p1.getYears();
int months = p1.getMonths();
int days = p1.getDays();

LocalDate futureDate = LocalDate.now().plus(p2);
```

#### DateTimeFormatter — Formatting and Parsing

```java
// Predefined formatters
LocalDateTime now = LocalDateTime.now();
String iso = now.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);

// Custom patterns
DateTimeFormatter custom = DateTimeFormatter.ofPattern("dd-MM-yyyy HH:mm:ss");
String formatted = now.format(custom);         // 15-03-2024 14:30:00
LocalDateTime parsed = LocalDateTime.parse("15-03-2024 14:30:00", custom);

// With Locale
DateTimeFormatter french = DateTimeFormatter.ofPattern("d MMMM yyyy", Locale.FRENCH);
String frenchDate = LocalDate.now().format(french); // 15 mars 2024

// Predefined patterns
DateTimeFormatter.ISO_DATE;          // 2024-03-15
DateTimeFormatter.ISO_TIME;          // 14:30:00
DateTimeFormatter.ISO_DATE_TIME;     // 2024-03-15T14:30:00
DateTimeFormatter.BASIC_ISO_DATE;    // 20240315
```

#### TemporalAdjusters — Complex Date Manipulation

```java
import java.time.temporal.TemporalAdjusters;

LocalDate today = LocalDate.now();

LocalDate firstDayOfMonth = today.with(TemporalAdjusters.firstDayOfMonth());
LocalDate lastDayOfMonth = today.with(TemporalAdjusters.lastDayOfMonth());
LocalDate firstDayOfYear = today.with(TemporalAdjusters.firstDayOfYear());
LocalDate nextMonday = today.with(TemporalAdjusters.next(DayOfWeek.MONDAY));
LocalDate previousFriday = today.with(TemporalAdjusters.previous(DayOfWeek.FRIDAY));
LocalDate firstMondayOfMonth = today.with(TemporalAdjusters.firstInMonth(DayOfWeek.MONDAY));

// Custom TemporalAdjuster
TemporalAdjuster nextWorkDay = temporal -> {
    LocalDate date = LocalDate.from(temporal);
    DayOfWeek day = date.getDayOfWeek();
    if (day == DayOfWeek.FRIDAY) return date.plusDays(3);
    if (day == DayOfWeek.SATURDAY) return date.plusDays(2);
    return date.plusDays(1);
};
LocalDate nextWork = today.with(nextWorkDay);
```

#### Converting Between Old and New API

```java
// Date -> Instant -> LocalDateTime
Date oldDate = new Date();
Instant instant = oldDate.toInstant();
LocalDateTime ldt = LocalDateTime.ofInstant(instant, ZoneId.systemDefault());

// LocalDateTime -> Instant -> Date
LocalDateTime now = LocalDateTime.now();
Instant inst = now.atZone(ZoneId.systemDefault()).toInstant();
Date date = Date.from(inst);

// Calendar -> ZonedDateTime
Calendar cal = Calendar.getInstance();
ZonedDateTime zdt = cal.toInstant().atZone(cal.getTimeZone().toZoneId());

// java.sql.Date
java.sql.Date sqlDate = java.sql.Date.valueOf(LocalDate.now());
LocalDate localDate = sqlDate.toLocalDate();

// java.sql.Timestamp
java.sql.Timestamp ts = java.sql.Timestamp.valueOf(LocalDateTime.now());
LocalDateTime fromTs = ts.toLocalDateTime();
```

---

## 8. Nashorn JavaScript Engine

### What is Nashorn?

Nashorn is a **JavaScript engine** developed in Java, introduced in Java 8 to replace the older **Rhino** engine. It compiles JavaScript to Java bytecode using `invokedynamic`, offering better performance.

> **Note**: Nashorn was **deprecated in Java 11** and **removed in Java 15**.

```java
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;

ScriptEngineManager manager = new ScriptEngineManager();
ScriptEngine engine = manager.getEngineByName("nashorn");

// Execute JavaScript
engine.eval("print('Hello from JavaScript!')");

// Evaluate expressions
Object result = engine.eval("10 + 20");
System.out.println(result); // 30

// Pass variables between Java and JavaScript
engine.put("name", "Java");
engine.eval("print('Hello ' + name)"); // Hello Java

// Call JavaScript function from Java
engine.eval("function add(a, b) { return a + b; }");
Invocable invocable = (Invocable) engine;
Object sum = invocable.invokeFunction("add", 10, 20);
System.out.println(sum); // 30.0

// Run JavaScript files
engine.eval(new FileReader("script.js"));
```

### Command-line tool: `jjs`

```bash
$ jjs
jjs> print("Hello Nashorn")
Hello Nashorn
jjs> var x = 10 + 20
jjs> print(x)
30
```

---

## 9. forEach() Method

### Iterable.forEach()

A new **default method** added to `java.lang.Iterable` interface.

```java
// Signature
default void forEach(Consumer<? super T> action)

// List
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
names.forEach(name -> System.out.println(name));
names.forEach(System.out::println); // method reference

// Set
Set<Integer> numbers = new HashSet<>(Arrays.asList(1, 2, 3));
numbers.forEach(System.out::println);

// Map (using BiConsumer)
Map<String, Integer> map = new HashMap<>();
map.put("a", 1);
map.put("b", 2);
map.forEach((key, value) -> System.out.println(key + " = " + value));
```

### forEach() vs for-each loop (Interview)

| Feature | forEach() | for-each loop |
|---|---|---|
| **Type** | Method on Iterable | Language construct |
| **Break/Continue** | NOT supported | Supported |
| **Checked Exceptions** | Cannot throw directly | Can throw |
| **Local Variables** | Must be effectively final | Can modify |
| **Performance** | Slight overhead (lambda) | Slightly faster |

### Handling Exceptions in forEach

```java
// Wrapper approach
names.forEach(name -> {
    try {
        processName(name); // may throw checked exception
    } catch (Exception e) {
        throw new RuntimeException(e);
    }
});

// Custom functional interface approach
@FunctionalInterface
interface ThrowingConsumer<T, E extends Exception> {
    void accept(T t) throws E;
}

static <T> Consumer<T> wrap(ThrowingConsumer<T, Exception> consumer) {
    return t -> {
        try { consumer.accept(t); }
        catch (Exception e) { throw new RuntimeException(e); }
    };
}

names.forEach(wrap(name -> riskyOperation(name)));
```

---

## 10. StringJoiner Class

### What is StringJoiner?

`java.util.StringJoiner` is used to construct a sequence of characters separated by a delimiter, with optional prefix and suffix.

```java
// Simple delimiter
StringJoiner sj1 = new StringJoiner(", ");
sj1.add("Alice").add("Bob").add("Charlie");
System.out.println(sj1.toString()); // Alice, Bob, Charlie

// With prefix and suffix
StringJoiner sj2 = new StringJoiner(", ", "[", "]");
sj2.add("1").add("2").add("3");
System.out.println(sj2.toString()); // [1, 2, 3]

// Empty value handling
StringJoiner sj3 = new StringJoiner(", ", "[", "]");
sj3.setEmptyValue("EMPTY");
System.out.println(sj3.toString()); // EMPTY

// Merge two StringJoiners
StringJoiner sj4 = new StringJoiner("-");
sj4.add("A").add("B");
StringJoiner sj5 = new StringJoiner("-");
sj5.add("C").add("D");
sj4.merge(sj5);
System.out.println(sj4); // A-B-C-D

// String.join() static method (uses StringJoiner internally)
String joined = String.join(", ", "Alice", "Bob", "Charlie"); // Alice, Bob, Charlie
String joinedList = String.join(" | ", names);                 // Alice | Bob | Charlie

// Collectors.joining()
String result = names.stream().collect(Collectors.joining(", ", "[", "]")); // [Alice, Bob, Charlie]
```

---

## 11. Collectors Class

`java.util.stream.Collectors` provides reduction operations for use with `Stream.collect()`.

### All Major Collectors

```java
List<Employee> employees = getEmployees();

// 1. toList()
List<String> nameList = employees.stream()
    .map(Employee::getName)
    .collect(Collectors.toList()); // Returns ArrayList

// 2. toSet()
Set<String> nameSet = employees.stream()
    .map(Employee::getDepartment)
    .collect(Collectors.toSet()); // Returns HashSet

// 3. toCollection() — specific collection type
TreeSet<String> sortedSet = employees.stream()
    .map(Employee::getName)
    .collect(Collectors.toCollection(TreeSet::new));

LinkedList<String> linkedList = employees.stream()
    .map(Employee::getName)
    .collect(Collectors.toCollection(LinkedList::new));

// 4. toMap()
Map<String, Double> nameSalaryMap = employees.stream()
    .collect(Collectors.toMap(
        Employee::getName,       // key mapper
        Employee::getSalary      // value mapper
    ));

// Handle duplicate keys
Map<String, Double> withMerge = employees.stream()
    .collect(Collectors.toMap(
        Employee::getDepartment,
        Employee::getSalary,
        (existing, replacement) -> existing + replacement // merge function
    ));

// Specify map type
TreeMap<String, Double> treeMap = employees.stream()
    .collect(Collectors.toMap(
        Employee::getName,
        Employee::getSalary,
        (a, b) -> a,
        TreeMap::new
    ));

// 5. toUnmodifiableList() / toUnmodifiableSet() / toUnmodifiableMap() (Java 10+)

// 6. joining()
String names = employees.stream()
    .map(Employee::getName)
    .collect(Collectors.joining());                     // AliceBobCharlie
String csv = employees.stream()
    .map(Employee::getName)
    .collect(Collectors.joining(", "));                 // Alice, Bob, Charlie
String formatted = employees.stream()
    .map(Employee::getName)
    .collect(Collectors.joining(", ", "[", "]"));       // [Alice, Bob, Charlie]

// 7. counting()
long count = employees.stream()
    .collect(Collectors.counting()); // same as .count()

// 8. summingInt / summingLong / summingDouble
double totalSalary = employees.stream()
    .collect(Collectors.summingDouble(Employee::getSalary));

// 9. averagingInt / averagingLong / averagingDouble
double avgSalary = employees.stream()
    .collect(Collectors.averagingDouble(Employee::getSalary));

// 10. summarizingInt / summarizingLong / summarizingDouble
DoubleSummaryStatistics stats = employees.stream()
    .collect(Collectors.summarizingDouble(Employee::getSalary));
// stats.getCount(), getSum(), getMin(), getMax(), getAverage()

// 11. groupingBy()
Map<String, List<Employee>> byDept = employees.stream()
    .collect(Collectors.groupingBy(Employee::getDepartment));

// groupingBy with downstream collector
Map<String, Long> countByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.counting()
    ));

Map<String, Double> avgSalaryByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.averagingDouble(Employee::getSalary)
    ));

Map<String, Optional<Employee>> highestPaidByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.maxBy(Comparator.comparing(Employee::getSalary))
    ));

// Multi-level grouping
Map<String, Map<String, List<Employee>>> byDeptThenCity = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.groupingBy(Employee::getCity)
    ));

// groupingBy with specific map type
TreeMap<String, List<Employee>> sortedByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        TreeMap::new,
        Collectors.toList()
    ));

// 12. partitioningBy() — special case groupingBy with boolean key
Map<Boolean, List<Employee>> partitioned = employees.stream()
    .collect(Collectors.partitioningBy(e -> e.getSalary() > 50000));
List<Employee> highEarners = partitioned.get(true);
List<Employee> lowEarners = partitioned.get(false);

// With downstream
Map<Boolean, Long> partitionCount = employees.stream()
    .collect(Collectors.partitioningBy(
        e -> e.getSalary() > 50000,
        Collectors.counting()
    ));

// 13. maxBy() / minBy()
Optional<Employee> highestPaid = employees.stream()
    .collect(Collectors.maxBy(Comparator.comparing(Employee::getSalary)));

// 14. reducing()
Optional<Double> totalSal = employees.stream()
    .map(Employee::getSalary)
    .collect(Collectors.reducing(Double::sum));

double totalSal2 = employees.stream()
    .collect(Collectors.reducing(0.0, Employee::getSalary, Double::sum));

// 15. mapping() — downstream collector with transformation
Map<String, List<String>> namesByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.mapping(Employee::getName, Collectors.toList())
    ));

// 16. collectingAndThen()
List<Employee> unmodifiable = employees.stream()
    .collect(Collectors.collectingAndThen(
        Collectors.toList(),
        Collections::unmodifiableList
    ));

int size = employees.stream()
    .collect(Collectors.collectingAndThen(
        Collectors.toList(),
        List::size
    ));
```

---

## 12. Parallel Streams

### What are Parallel Streams?

Parallel Streams split the source data into **multiple chunks**, process them **concurrently** using the **ForkJoinPool**, and combine the results.

```java
// Creating Parallel Streams
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

// Method 1: parallelStream() from collection
Stream<Integer> parallel1 = numbers.parallelStream();

// Method 2: parallel() on existing stream
Stream<Integer> parallel2 = numbers.stream().parallel();

// Check if parallel
boolean isPar = parallel1.isParallel(); // true

// Convert back to sequential
Stream<Integer> seq = parallel1.sequential();
```

### ForkJoinPool

```java
// Default uses ForkJoinPool.commonPool()
// Size = Runtime.getRuntime().availableProcessors() - 1

// Custom ForkJoinPool
ForkJoinPool customPool = new ForkJoinPool(4); // 4 threads
long count = customPool.submit(() ->
    numbers.parallelStream()
        .filter(n -> n % 2 == 0)
        .count()
).get();
customPool.shutdown();

// System property to change common pool size
// -Djava.util.concurrent.ForkJoinPool.common.parallelism=8
```

### When to Use Parallel Streams (Interview)

**Use when**:

- Large dataset (>10,000 elements).
- Stateless, independent operations.
- CPU-intensive operations (not I/O-bound).
- Operations are **associative** and **non-interfering**.
- Source is efficiently splittable (`ArrayList`, arrays — good; `LinkedList`, `Stream.iterate` — bad).

**Avoid when**:

- Small datasets (overhead > benefit).
- Operations have **side effects** or modify **shared mutable state**.
- Order matters and cannot use `forEachOrdered()`.
- Operations are I/O-bound (use async instead).
- Using `LinkedList` (poor splitting).
- Using `limit()` or `findFirst()` (ordering constraints reduce parallelism).

### Thread Safety Issues

```java
// WRONG — shared mutable state
List<Integer> result = new ArrayList<>(); // NOT thread-safe
numbers.parallelStream()
    .filter(n -> n % 2 == 0)
    .forEach(result::add); // RACE CONDITION!

// CORRECT — use collect()
List<Integer> result = numbers.parallelStream()
    .filter(n -> n % 2 == 0)
    .collect(Collectors.toList());

// CORRECT — use thread-safe collection
List<Integer> result = Collections.synchronizedList(new ArrayList<>());
numbers.parallelStream()
    .filter(n -> n % 2 == 0)
    .forEach(result::add);
```

### Ordering in Parallel Streams

```java
// forEachOrdered() maintains encounter order
numbers.parallelStream()
    .forEachOrdered(System.out::println); // Ordered but slower

// unordered() allows optimization
numbers.parallelStream()
    .unordered()
    .limit(5)
    .forEach(System.out::println); // Better performance
```

### Performance Comparison

```java
long start, end;
List<Integer> largeList = IntStream.rangeClosed(1, 10_000_000)
    .boxed().collect(Collectors.toList());

// Sequential
start = System.nanoTime();
long seqSum = largeList.stream()
    .reduce(0, Integer::sum);
end = System.nanoTime();
System.out.println("Sequential: " + (end - start) / 1_000_000 + " ms");

// Parallel
start = System.nanoTime();
long parSum = largeList.parallelStream()
    .reduce(0, Integer::sum);
end = System.nanoTime();
System.out.println("Parallel: " + (end - start) / 1_000_000 + " ms");
```

### Spliterator (Splittable Iterator)

```java
// Spliterator is the internal mechanism for parallel stream splitting
Spliterator<Integer> spliterator = numbers.spliterator();

// Key methods
spliterator.tryAdvance(System.out::println);  // process one element
spliterator.forEachRemaining(System.out::println); // process remaining

// trySplit() splits into two parts for parallel processing
Spliterator<Integer> second = spliterator.trySplit();

// Characteristics
long size = spliterator.estimateSize();
int characteristics = spliterator.characteristics();
// ORDERED, DISTINCT, SORTED, SIZED, SUBSIZED, NONNULL, IMMUTABLE, CONCURRENT
```

---

## 13. Type Annotations and Repeating Annotations

### Type Annotations (JSR 308)

Java 8 allows annotations on **any use of a type**, not just declarations.

```java
// On type use
@NonNull String name = "Java";

// On generic type argument
List<@NonNull String> names = new ArrayList<>();

// On extends/implements
class MyList implements @ReadOnly List<String> { }

// On object creation
new @Interned MyObject();

// On type cast
String s = (@NonNull String) obj;

// On throws clause
void process() throws @Critical Exception { }

// On array types
String @NonNull [] arr;

// New ElementType values
@Target(ElementType.TYPE_USE)         // Any type use
@Target(ElementType.TYPE_PARAMETER)   // Type parameters like <T>
```

### Repeating Annotations (JSR 337)

Java 8 allows the same annotation to be applied **multiple times** to the same declaration.

```java
// Step 1: Define the repeatable annotation
@Repeatable(Schedules.class)
@interface Schedule {
    String day();
    String time();
}

// Step 2: Define the container annotation
@interface Schedules {
    Schedule[] value();
}

// Step 3: Use it
@Schedule(day = "Monday", time = "9:00")
@Schedule(day = "Wednesday", time = "14:00")
@Schedule(day = "Friday", time = "9:00")
public class Meeting {
    // ...
}

// Retrieve via reflection
Schedule[] schedules = Meeting.class.getAnnotationsByType(Schedule.class);
for (Schedule s : schedules) {
    System.out.println(s.day() + " at " + s.time());
}

// Or get container annotation
Schedules container = Meeting.class.getAnnotation(Schedules.class);
```

---

## 14. CompletableFuture

### What is CompletableFuture?

`java.util.concurrent.CompletableFuture<T>` is an enhancement over `Future<T>`. It represents a future result of an asynchronous computation and supports a fluent API for composing, combining, and handling async operations.

### Key Advantages over Future (Interview)

| Feature | Future | CompletableFuture |
|---|---|---|
| Manual completion | No | Yes (`complete()`) |
| Chaining/Composition | No | Yes (`thenApply`, `thenCompose`) |
| Combining results | No | Yes (`thenCombine`, `allOf`, `anyOf`) |
| Exception handling | Only `get()` throws | `exceptionally()`, `handle()` |
| Callback | No | `thenAccept()`, `thenRun()` |
| Non-blocking | No (`get()` blocks) | Yes (callbacks) |

### Creating CompletableFuture

```java
// 1. supplyAsync — with return value
CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> {
    // runs in ForkJoinPool.commonPool()
    return "Hello from async!";
});

// 2. runAsync — no return value
CompletableFuture<Void> future2 = CompletableFuture.runAsync(() -> {
    System.out.println("Running async task");
});

// 3. With custom Executor
ExecutorService executor = Executors.newFixedThreadPool(4);
CompletableFuture<String> future3 = CompletableFuture.supplyAsync(
    () -> "Custom executor", executor
);

// 4. Already completed
CompletableFuture<String> completed = CompletableFuture.completedFuture("Done");

// 5. Manual completion
CompletableFuture<String> manual = new CompletableFuture<>();
manual.complete("Manually completed!");
```

### Chaining Operations

```java
// thenApply — transform result (like map)
CompletableFuture<Integer> lengthFuture = CompletableFuture
    .supplyAsync(() -> "Hello World")
    .thenApply(String::length);    // 11

// thenAccept — consume result (no return)
CompletableFuture.supplyAsync(() -> "Hello")
    .thenAccept(System.out::println);

// thenRun — run after completion (no access to result)
CompletableFuture.supplyAsync(() -> "Hello")
    .thenRun(() -> System.out.println("Completed!"));

// thenCompose — chain dependent futures (like flatMap)
CompletableFuture<Double> priceFuture = getUserFuture(userId)
    .thenCompose(user -> getOrderFuture(user))
    .thenCompose(order -> getPriceFuture(order));

// thenCombine — combine two independent futures
CompletableFuture<String> hello = CompletableFuture.supplyAsync(() -> "Hello");
CompletableFuture<String> world = CompletableFuture.supplyAsync(() -> "World");
CompletableFuture<String> combined = hello.thenCombine(world, (h, w) -> h + " " + w);
System.out.println(combined.get()); // Hello World
```

### Async Variants

```java
// *Async methods execute the callback in a different thread
future.thenApply(s -> s.toUpperCase());         // same thread
future.thenApplyAsync(s -> s.toUpperCase());    // ForkJoinPool
future.thenApplyAsync(s -> s.toUpperCase(), executor); // custom executor
```

### Exception Handling

```java
// exceptionally — recover from exceptions
CompletableFuture<String> future = CompletableFuture
    .supplyAsync(() -> {
        if (true) throw new RuntimeException("Error!");
        return "Success";
    })
    .exceptionally(ex -> "Fallback: " + ex.getMessage());

// handle — handle both success and failure
CompletableFuture<String> handled = CompletableFuture
    .supplyAsync(() -> {
        if (true) throw new RuntimeException("Oops");
        return "OK";
    })
    .handle((result, ex) -> {
        if (ex != null) return "Error: " + ex.getMessage();
        return result;
    });

// whenComplete — like handle but doesn't transform the result
CompletableFuture<String> whenDone = CompletableFuture
    .supplyAsync(() -> "Result")
    .whenComplete((result, ex) -> {
        if (ex != null) System.err.println("Failed: " + ex);
        else System.out.println("Success: " + result);
    });
```

### Combining Multiple Futures

```java
// allOf — wait for ALL to complete (returns CompletableFuture<Void>)
CompletableFuture<String> f1 = CompletableFuture.supplyAsync(() -> "A");
CompletableFuture<String> f2 = CompletableFuture.supplyAsync(() -> "B");
CompletableFuture<String> f3 = CompletableFuture.supplyAsync(() -> "C");

CompletableFuture<Void> allDone = CompletableFuture.allOf(f1, f2, f3);
allDone.thenRun(() -> {
    System.out.println(f1.join() + f2.join() + f3.join()); // ABC
});

// Collect all results
CompletableFuture<List<String>> allResults = CompletableFuture.allOf(f1, f2, f3)
    .thenApply(v -> Stream.of(f1, f2, f3)
        .map(CompletableFuture::join)
        .collect(Collectors.toList()));

// anyOf — completes when ANY one completes
CompletableFuture<Object> fastest = CompletableFuture.anyOf(f1, f2, f3);
System.out.println(fastest.get()); // first to complete
```

### get() vs join() (Interview)

| Method | Checked Exception | Use Case |
|---|---|---|
| `get()` | Throws `ExecutionException`, `InterruptedException` | When you need to handle checked exceptions |
| `get(timeout, unit)` | Also throws `TimeoutException` | When you need timeout |
| `join()` | Throws `CompletionException` (unchecked) | Cleaner in lambda/stream pipelines |

---

## 15. Base64 Encoding and Decoding

Java 8 provides `java.util.Base64` with three encoders/decoders:

```java
import java.util.Base64;

// 1. Basic Encoder/Decoder
String original = "Hello, Java 8!";
String encoded = Base64.getEncoder().encodeToString(original.getBytes());
byte[] decoded = Base64.getDecoder().decode(encoded);
String decodedStr = new String(decoded);
System.out.println(encoded);    // SGVsbG8sIEphdmEgOCE=
System.out.println(decodedStr); // Hello, Java 8!

// Without padding
String noPadding = Base64.getEncoder().withoutPadding()
    .encodeToString(original.getBytes());

// 2. URL and Filename Safe Encoder/Decoder
// Uses '-' and '_' instead of '+' and '/'
String urlEncoded = Base64.getUrlEncoder().encodeToString("https://example.com?a=1&b=2".getBytes());
byte[] urlDecoded = Base64.getUrlDecoder().decode(urlEncoded);

// 3. MIME Encoder/Decoder
// Inserts line separators (\r\n) every 76 characters — for MIME content
byte[] mimeEncoded = Base64.getMimeEncoder().encode(largeData);
byte[] mimeDecoded = Base64.getMimeDecoder().decode(mimeEncoded);

// Custom line length and separator
Base64.Encoder customMime = Base64.getMimeEncoder(64, "\n".getBytes());

// Wrapping streams
OutputStream encodingStream = Base64.getEncoder().wrap(outputStream);
InputStream decodingStream = Base64.getDecoder().wrap(inputStream);
```

---

## 16. Map API Enhancements

```java
Map<String, Integer> map = new HashMap<>();
map.put("a", 1);
map.put("b", 2);
map.put("c", 3);

// 1. getOrDefault()
int val = map.getOrDefault("d", 0); // 0

// 2. putIfAbsent() — puts value ONLY if key is absent or mapped to null
map.putIfAbsent("d", 4); // adds d=4
map.putIfAbsent("a", 99); // a remains 1

// 3. forEach()
map.forEach((k, v) -> System.out.println(k + "=" + v));

// 4. replaceAll()
map.replaceAll((k, v) -> v * 10); // all values multiplied by 10

// 5. replace()
map.replace("a", 100);       // replaces if key exists
map.replace("a", 100, 200);  // replaces only if key=a AND value=100

// 6. remove() with value
map.remove("a", 1); // removes only if key=a AND value=1

// 7. compute()
map.compute("a", (k, v) -> (v == null) ? 1 : v + 1);

// 8. computeIfAbsent() — compute value if key is absent
map.computeIfAbsent("e", k -> k.length()); // e -> 1

// Common pattern: building multi-value maps
Map<String, List<String>> multiMap = new HashMap<>();
multiMap.computeIfAbsent("fruits", k -> new ArrayList<>()).add("apple");
multiMap.computeIfAbsent("fruits", k -> new ArrayList<>()).add("banana");
// {fruits=[apple, banana]}

// 9. computeIfPresent()
map.computeIfPresent("a", (k, v) -> v + 1); // increments if present

// 10. merge()
map.merge("a", 1, Integer::sum);      // if present: sum; else: put 1
map.merge("newKey", 42, Integer::sum); // puts 42

// Word counting with merge
String[] words = {"hello", "world", "hello", "java"};
Map<String, Integer> wordCount = new HashMap<>();
for (String word : words) {
    wordCount.merge(word, 1, Integer::sum);
}
// {hello=2, world=1, java=1}
```

---

## 17. Concurrency API Enhancements

### StampedLock

An alternative to `ReadWriteLock` with **optimistic read** capability.

```java
StampedLock lock = new StampedLock();

// Write lock
long stamp = lock.writeLock();
try {
    // modify shared state
} finally {
    lock.unlockWrite(stamp);
}

// Read lock
long stamp = lock.readLock();
try {
    // read shared state
} finally {
    lock.unlockRead(stamp);
}

// Optimistic read (no locking — best performance)
long stamp = lock.tryOptimisticRead();
// read shared state into local variables
int currentX = x;
int currentY = y;
if (!lock.validate(stamp)) {
    // someone wrote — fall back to read lock
    stamp = lock.readLock();
    try {
        currentX = x;
        currentY = y;
    } finally {
        lock.unlockRead(stamp);
    }
}
// use currentX, currentY
```

### LongAdder and LongAccumulator

Better performance than `AtomicLong` under high contention.

```java
// LongAdder — optimized for summation
LongAdder adder = new LongAdder();
adder.increment();
adder.add(10);
long sum = adder.sum();
adder.reset();

// LongAccumulator — generalized version
LongAccumulator acc = new LongAccumulator(Long::max, Long.MIN_VALUE);
acc.accumulate(10);
acc.accumulate(20);
acc.accumulate(5);
long max = acc.get(); // 20

// DoubleAdder / DoubleAccumulator also available
```

### ConcurrentHashMap Enhancements

```java
ConcurrentHashMap<String, Integer> cmap = new ConcurrentHashMap<>();
cmap.put("a", 1);
cmap.put("b", 2);
cmap.put("c", 3);

// forEach with parallelism threshold
// threshold = 1 means always parallel
cmap.forEach(1, (k, v) -> System.out.println(k + "=" + v));

// search — find first matching entry
String found = cmap.search(1, (k, v) -> v > 1 ? k : null);

// reduce
int sum = cmap.reduce(1, (k, v) -> v, Integer::sum);

// forEachKey / forEachValue / forEachEntry
cmap.forEachValue(1, System.out::println);

// reduceKeys / reduceValues
int maxVal = cmap.reduceValues(1, Integer::max);

// mappingCount() returns long (instead of size() which returns int)
long count = cmap.mappingCount();

// newKeySet() — creates concurrent set backed by ConcurrentHashMap
Set<String> concurrentSet = ConcurrentHashMap.newKeySet();
concurrentSet.add("item1");
```

---

## 18. IO/NIO Enhancements

```java
// 1. Files.lines() — lazy stream of lines
try (Stream<String> lines = Files.lines(Paths.get("file.txt"))) {
    lines.filter(line -> line.contains("error"))
         .forEach(System.out::println);
}

// With charset
Stream<String> lines = Files.lines(Paths.get("file.txt"), StandardCharsets.UTF_8);

// 2. Files.list() — list directory contents (non-recursive)
try (Stream<Path> paths = Files.list(Paths.get("/home"))) {
    paths.filter(Files::isDirectory)
         .forEach(System.out::println);
}

// 3. Files.walk() — recursive directory traversal
try (Stream<Path> walk = Files.walk(Paths.get("/home"), 3)) { // maxDepth=3
    walk.filter(p -> p.toString().endsWith(".java"))
        .forEach(System.out::println);
}

// 4. Files.find() — find files with BiPredicate
try (Stream<Path> found = Files.find(Paths.get("/home"), Integer.MAX_VALUE,
    (path, attrs) -> attrs.isRegularFile() && path.toString().endsWith(".log"))) {
    found.forEach(System.out::println);
}

// 5. BufferedReader.lines()
try (BufferedReader br = new BufferedReader(new FileReader("file.txt"))) {
    br.lines()
      .map(String::trim)
      .filter(line -> !line.isEmpty())
      .forEach(System.out::println);
}

// 6. Files.readAllLines() (pre-Java 8, but often used with streams)
List<String> allLines = Files.readAllLines(Paths.get("file.txt"));
```

---

## 19. Miscellaneous Enhancements

### Collection Enhancements

```java
// List.sort() default method (replaces Collections.sort())
List<String> names = new ArrayList<>(Arrays.asList("C", "A", "B"));
names.sort(Comparator.naturalOrder());

// Collection.removeIf()
names.removeIf(s -> s.startsWith("A")); // removes "A"

// Collection.spliterator() — for parallel iteration

// Arrays.parallelSort()
int[] arr = {5, 3, 1, 4, 2};
Arrays.parallelSort(arr); // uses ForkJoin — faster for large arrays

// Arrays.parallelPrefix() — cumulative operation
int[] nums = {1, 2, 3, 4, 5};
Arrays.parallelPrefix(nums, Integer::sum);
// Result: [1, 3, 6, 10, 15]

// Arrays.parallelSetAll()
int[] squares = new int[10];
Arrays.parallelSetAll(squares, i -> i * i);
// [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### Comparator Enhancements

```java
// comparing()
Comparator<Employee> byName = Comparator.comparing(Employee::getName);
Comparator<Employee> bySalary = Comparator.comparing(Employee::getSalary);

// Chaining with thenComparing()
Comparator<Employee> byDeptThenName = Comparator
    .comparing(Employee::getDepartment)
    .thenComparing(Employee::getName);

// reversed()
Comparator<Employee> bySalaryDesc = Comparator
    .comparing(Employee::getSalary)
    .reversed();

// naturalOrder() / reverseOrder()
Comparator<String> natural = Comparator.naturalOrder();
Comparator<String> reverse = Comparator.reverseOrder();

// nullsFirst() / nullsLast()
Comparator<String> nullSafe = Comparator.nullsFirst(Comparator.naturalOrder());
Comparator<Employee> nullSalaryLast = Comparator.comparing(
    Employee::getSalary,
    Comparator.nullsLast(Comparator.naturalOrder())
);

// comparingInt / comparingLong / comparingDouble (avoid autoboxing)
Comparator<Employee> byAge = Comparator.comparingInt(Employee::getAge);
```

### PermGen Removal — Metaspace

- **PermGen** (Permanent Generation) has been **removed** in Java 8.
- Replaced by **Metaspace**, which uses **native memory** (not JVM heap).
- Metaspace grows **automatically** by default (no fixed size like PermGen).
- `-XX:MetaspaceSize` and `-XX:MaxMetaspaceSize` JVM flags control it.
- `java.lang.OutOfMemoryError: PermGen space` is **no longer possible**.
- Now you may see `java.lang.OutOfMemoryError: Metaspace` instead.
- Class metadata is stored in Metaspace; interned Strings moved to **heap** (since Java 7).

### Other Notable Changes

- **Method parameter names** are retained at runtime with `-parameters` compiler flag, accessible via `java.lang.reflect.Parameter.getName()`.
- **`@FunctionalInterface`** annotation added.
- **HashMap** improvements — balanced tree (red-black tree) for buckets when collision count exceeds threshold (TREEIFY_THRESHOLD = 8), improving worst-case from O(n) to O(log n).
- **Atomic\* classes** enhanced with `getAndUpdate()`, `updateAndGet()`, `getAndAccumulate()`, `accumulateAndGet()`.
- **Process API** — `ProcessBuilder` improvements.
- **JDBC 4.2** support.

---

## 20. Top Interview Questions & Answers

### Q1: What is the difference between `map()` and `flatMap()` in Streams?

`map()` applies a function to each element and produces a one-to-one mapping (Stream of objects). `flatMap()` applies a function that returns a stream for each element and then flattens all the resulting streams into one (one-to-many mapping). Use `flatMap()` when each element maps to multiple values (like splitting sentences into words, or unwrapping nested collections).

### Q2: What is the difference between `Collection.stream()` and `Collection.parallelStream()`?

`stream()` processes elements sequentially in the calling thread. `parallelStream()` splits data into sub-streams, processes them in parallel using the `ForkJoinPool.commonPool()`, and merges results. Parallel streams are faster for large datasets with CPU-intensive, stateless, independent operations, but add overhead for small datasets.

### Q3: What is an effectively final variable?

A variable that is not declared `final` but whose value is **never changed** after initialization. Lambda expressions and anonymous inner classes can only access local variables that are `final` or effectively final.

### Q4: Can a functional interface extend another functional interface?

Yes, but the child interface must NOT declare any additional abstract methods. It can add default or static methods. If both have the same abstract method signature, it still counts as one.

### Q5: What is the difference between `Predicate` and `Function`?

`Predicate<T>` takes an input and returns `boolean` (used for filtering/testing conditions). `Function<T, R>` takes an input of type T and returns a result of type R (used for transformations).

### Q6: What is a Spliterator?

`Spliterator` (Splittable Iterator) is an internal iterator introduced for parallel processing. It can split elements for parallel traversal (`trySplit()`), estimate size (`estimateSize()`), and has characteristics flags (ORDERED, SIZED, SORTED, etc.). It's the backbone of parallel streams.

### Q7: Explain `reduce()` with three arguments.

The three-argument `reduce(identity, accumulator, combiner)`:
- **identity**: initial value and identity for the combiner.
- **accumulator**: combines a partial result with the next element.
- **combiner**: merges two partial results (used only in parallel streams).

### Q8: What is the difference between `findFirst()` and `findAny()`?

`findFirst()` returns the **first element** in encounter order (deterministic). `findAny()` returns **any element** and is non-deterministic — optimized for parallel streams where returning the first element would require synchronization.

### Q9: What is the purpose of `peek()`?

`peek()` is an intermediate operation that performs a side-effect action on each element as it passes through the pipeline. It's primarily used for **debugging** — logging elements at each stage. It should NOT be used for modifying elements or as a replacement for `forEach()`.

### Q10: Why was the Date/Time API redesigned?

Old `java.util.Date` was mutable (thread-unsafe), had zero-indexed months, years offset by 1900, poor timezone support, and `SimpleDateFormat` was not thread-safe. The new `java.time` API is **immutable, thread-safe**, uses ISO 8601, has clear separation (LocalDate, LocalTime, etc.), and provides Duration, Period, and TemporalAdjusters.

### Q11: What is `thenCompose()` vs `thenCombine()` in CompletableFuture?

`thenCompose()` chains dependent futures sequentially — the second future depends on the result of the first (like `flatMap`). `thenCombine()` runs two independent futures in parallel and combines their results when both complete.

### Q12: Can we use `break` or `return` inside `forEach()` on a stream?

No. `break` and `continue` are not allowed. `return` inside a lambda only exits the lambda (like `continue` in a loop), not the enclosing method. To short-circuit, use `findFirst()`, `findAny()`, `anyMatch()`, `limit()`, or `takeWhile()` (Java 9+).

### Q13: Difference between `Collectors.groupingBy()` and `Collectors.partitioningBy()`?

`groupingBy()` groups elements by a classifier function, producing `Map<K, List<T>>` where K can be any type. `partitioningBy()` takes a predicate and produces `Map<Boolean, List<T>>` — always exactly two groups (true/false). `partitioningBy()` always has both keys present (even if the list is empty); `groupingBy()` only has keys for which elements exist.

### Q14: How does HashMap handle collisions differently in Java 8?

Before Java 8: Collisions were resolved using a **linked list** (O(n) worst case). In Java 8: When a bucket exceeds **TREEIFY_THRESHOLD (8)** entries, the linked list is converted to a **balanced red-black tree** (O(log n)). When it drops below **UNTREEIFY_THRESHOLD (6)**, it converts back. The key class should implement `Comparable` for optimal tree performance.

### Q15: What is the diamond problem in Java 8 interfaces and how is it resolved?

When a class implements two interfaces that both have a default method with the same signature, the compiler raises an error. The implementing class **must override** the method and can call a specific interface's version using `InterfaceName.super.methodName()`. Resolution rules: class wins > sub-interface wins > must override.

---

## Quick Reference Cheat Sheet

| Feature | Package/Class | Key Points |
|---|---|---|
| Lambda | — | `(params) -> body`, target type = functional interface |
| Functional Interface | `java.util.function` | Predicate, Function, Consumer, Supplier |
| Method Reference | — | `Class::method`, 4 types |
| Stream API | `java.util.stream` | Lazy, non-reusable, internal iteration |
| Default Methods | — | Interface method with body, `default` keyword |
| Optional | `java.util.Optional` | Container for nullable values |
| Date/Time | `java.time` | Immutable, thread-safe, ISO 8601 |
| Nashorn | `javax.script` | JS engine (deprecated Java 11) |
| Base64 | `java.util.Base64` | Basic, URL, MIME encoders/decoders |
| CompletableFuture | `java.util.concurrent` | Async programming, chaining, combining |
| StringJoiner | `java.util` | Delimiter-based string joining |
| StampedLock | `java.util.concurrent.locks` | Optimistic read lock |
| Metaspace | JVM | Replaces PermGen, native memory |

---

> **Tip**: Practice writing code with Streams, Lambdas, and Optional in an IDE. Most Java 8 interview rounds include live coding or whiteboard questions using the Stream API and Collectors.
