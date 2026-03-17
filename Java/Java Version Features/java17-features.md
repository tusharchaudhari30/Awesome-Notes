# Java 17 Features — Complete Interview Guide

> **Java 17** is a **Long-Term Support (LTS)** release, published on **September 14, 2021**. It follows Java 11 (previous LTS) and precedes Java 21 (next LTS). It includes features finalized from Java 12 through Java 17.

---

## Table of Contents

1. [Sealed Classes (JEP 409)](#1-sealed-classes-jep-409)
2. [Pattern Matching for instanceof (JEP 394)](#2-pattern-matching-for-instanceof-jep-394)
3. [Records (JEP 395)](#3-records-jep-395)
4. [Text Blocks (JEP 378)](#4-text-blocks-jep-378)
5. [Switch Expressions (JEP 361)](#5-switch-expressions-jep-361)
6. [Pattern Matching for switch (Preview — JEP 406)](#6-pattern-matching-for-switch-preview--jep-406)
7. [Enhanced Pseudo-Random Number Generators (JEP 356)](#7-enhanced-pseudo-random-number-generators-jep-356)
8. [New macOS Rendering Pipeline (JEP 382)](#8-new-macos-rendering-pipeline-jep-382)
9. [macOS/AArch64 Port (JEP 391)](#9-macosaarch64-port-jep-391)
10. [Deprecate the Applet API for Removal (JEP 398)](#10-deprecate-the-applet-api-for-removal-jep-398)
11. [Strongly Encapsulate JDK Internals (JEP 403)](#11-strongly-encapsulate-jdk-internals-jep-403)
12. [Remove RMI Activation (JEP 407)](#12-remove-rmi-activation-jep-407)
13. [Remove the Experimental AOT and JIT Compiler (JEP 410)](#13-remove-the-experimental-aot-and-jit-compiler-jep-410)
14. [Deprecate the Security Manager for Removal (JEP 411)](#14-deprecate-the-security-manager-for-removal-jep-411)
15. [Foreign Function & Memory API (Incubator — JEP 412)](#15-foreign-function--memory-api-incubator--jep-412)
16. [Vector API (Second Incubator — JEP 414)](#16-vector-api-second-incubator--jep-414)
17. [Context-Specific Deserialization Filters (JEP 415)](#17-context-specific-deserialization-filters-jep-415)
18. [Helpful NullPointerExceptions (JEP 358)](#18-helpful-nullpointerexceptions-jep-358)
19. [Compact Number Formatting](#19-compact-number-formatting)
20. [Day Period Support in DateTimeFormatter](#20-day-period-support-in-datetimeformatter)
21. [Stream.toList() Method](#21-streamtolist-method)
22. [Other Notable API Additions](#22-other-notable-api-additions)
23. [Garbage Collectors in Java 17](#23-garbage-collectors-in-java-17)
24. [Migration from Java 11 to Java 17](#24-migration-from-java-11-to-java-17)
25. [Quick Interview Cheat Sheet](#25-quick-interview-cheat-sheet)

---

## 1. Sealed Classes (JEP 409)

### What Are Sealed Classes?

Sealed classes and interfaces **restrict which other classes or interfaces may extend or implement them**. They provide fine-grained control over the inheritance hierarchy.

**Status:** Finalized in Java 17 (Preview in Java 15 & 16).

### Keywords

| Keyword | Purpose |
|---------|---------|
| `sealed` | Declares a class/interface as sealed |
| `permits` | Lists the allowed subclasses/sub-interfaces |
| `non-sealed` | A permitted subclass that reopens the hierarchy |
| `final` | A permitted subclass that closes the hierarchy |

### Key Rules

- Every permitted subclass **must** be declared `final`, `sealed`, or `non-sealed`.
- Permitted subclasses must be in the **same module** (if in a module) or the **same package** (if not in a module).
- Permitted subclasses must **directly** extend the sealed class.
- If all permitted subclasses are in the same compilation unit (same `.java` file), the `permits` clause can be **omitted** — the compiler infers it.

### Example

```java
// Sealed interface — only Circle, Rectangle, and Triangle can implement it
public sealed interface Shape permits Circle, Rectangle, Triangle {
    double area();
}

// final — cannot be extended further
public final class Circle implements Shape {
    private final double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    @Override
    public double area() {
        return Math.PI * radius * radius;
    }
}

// sealed — further restricts who can extend
public sealed class Rectangle implements Shape permits Square {
    protected final double length, width;

    public Rectangle(double length, double width) {
        this.length = length;
        this.width = width;
    }

    @Override
    public double area() {
        return length * width;
    }
}

// final subclass of a sealed class
public final class Square extends Rectangle {
    public Square(double side) {
        super(side, side);
    }
}

// non-sealed — reopens the hierarchy, anyone can extend Triangle
public non-sealed class Triangle implements Shape {
    private final double base, height;

    public Triangle(double base, double height) {
        this.base = base;
        this.height = height;
    }

    @Override
    public double area() {
        return 0.5 * base * height;
    }
}

// Since Triangle is non-sealed, this is legal:
public class EquilateralTriangle extends Triangle {
    public EquilateralTriangle(double side) {
        super(side, side * Math.sqrt(3) / 2);
    }
}
```

### Sealed Classes with Records

Records are implicitly `final`, so they satisfy the sealed class requirement:

```java
public sealed interface Expr permits Constant, Add, Multiply, Negate {
    int evaluate();
}

public record Constant(int value) implements Expr {
    public int evaluate() { return value; }
}

public record Add(Expr left, Expr right) implements Expr {
    public int evaluate() { return left.evaluate() + right.evaluate(); }
}

public record Multiply(Expr left, Expr right) implements Expr {
    public int evaluate() { return left.evaluate() * right.evaluate(); }
}

public record Negate(Expr expr) implements Expr {
    public int evaluate() { return -expr.evaluate(); }
}
```

### Reflection API

```java
// Check if a class is sealed
boolean isSealed = Shape.class.isSealed();  // true

// Get permitted subclasses
Class<?>[] permitted = Shape.class.getPermittedSubclasses();
// [class Circle, class Rectangle, class Triangle]
```

### Sealed Classes vs. Enum

| Feature | Sealed Class | Enum |
|---------|-------------|------|
| Instances | Multiple per subclass | Singleton per constant |
| State | Each subclass can have different fields | Shared field set |
| Inheritance | Subclasses can be full classes, records, etc. | No subclassing |
| Use case | Modeling complex domain hierarchies | Fixed set of simple constants |

### Interview Tip

> Sealed classes enable **exhaustive pattern matching** in switch expressions. The compiler can verify all permitted subclasses are handled, eliminating the need for a `default` branch.

---

## 2. Pattern Matching for instanceof (JEP 394)

### What Is It?

Eliminates the need for explicit casting after an `instanceof` check. The variable declared in the pattern is a **pattern variable** and is in scope where the match is guaranteed.

**Status:** Finalized in Java 16 (Preview in Java 14 & 15).

### Before vs. After

```java
// ❌ Old way — manual cast
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}

// ✅ New way — pattern variable
if (obj instanceof String s) {
    System.out.println(s.length());  // s is already a String
}
```

### Scoping Rules (Flow Scoping)

The pattern variable is only in scope where the compiler can guarantee the match succeeded:

```java
// Variable 's' is in scope inside the if-block
if (obj instanceof String s) {
    System.out.println(s.toUpperCase());
}
// 's' is NOT in scope here

// Scope extends via short-circuit operators
if (obj instanceof String s && s.length() > 5) {
    // 's' is in scope because && guarantees the left side was true
    System.out.println(s);
}

// ❌ Compile error — || does NOT guarantee the left side was true
if (obj instanceof String s || s.length() > 5) {  // ERROR
}

// Scope extends to the else-block of negated checks
if (!(obj instanceof String s)) {
    // 's' is NOT in scope here
    return;
}
// 's' IS in scope here — because if we reach here, the match succeeded
System.out.println(s.toLowerCase());
```

### Using with Sealed Classes

```java
public static double calculateArea(Shape shape) {
    if (shape instanceof Circle c) {
        return Math.PI * c.radius() * c.radius();
    } else if (shape instanceof Rectangle r) {
        return r.length() * r.width();
    } else if (shape instanceof Triangle t) {
        return 0.5 * t.base() * t.height();
    }
    throw new IllegalArgumentException("Unknown shape");
}
```

### Guards and Compound Conditions

```java
if (obj instanceof String s && !s.isEmpty()) {
    System.out.println("Non-empty string: " + s);
}

if (obj instanceof Integer i && i > 0 && i < 100) {
    System.out.println("Small positive: " + i);
}
```

### Interview Keywords

- **Pattern variable**: The variable declared in the `instanceof` expression.
- **Flow scoping**: The compiler determines scope based on control flow, not lexical blocks.
- **Dominance**: A pattern that matches a supertype dominates patterns for subtypes.

---

## 3. Records (JEP 395)

### What Are Records?

Records are **transparent carriers for immutable data**. They automatically generate `equals()`, `hashCode()`, `toString()`, a canonical constructor, and accessor methods.

**Status:** Finalized in Java 16 (Preview in Java 14 & 15).

### Declaration and Generated Members

```java
public record Point(int x, int y) { }
```

This single line generates:

| Generated Member | Description |
|------------------|-------------|
| `private final int x` | Final field for each component |
| `private final int y` | Final field for each component |
| `public int x()` | Accessor (NOT `getX()`) |
| `public int y()` | Accessor (NOT `getY()`) |
| `public Point(int x, int y)` | Canonical constructor |
| `equals(Object)` | Component-wise equality |
| `hashCode()` | Hash based on all components |
| `toString()` | Returns `Point[x=1, y=2]` |

### Canonical Constructor (Compact Form)

```java
public record Range(int start, int end) {
    // Compact constructor — no parameter list, no explicit assignment
    public Range {
        if (start > end) {
            throw new IllegalArgumentException(
                "start (%d) must be <= end (%d)".formatted(start, end)
            );
        }
        // Implicit: this.start = start; this.end = end;
    }
}
```

### Custom Canonical Constructor

```java
public record Email(String value) {
    // Full canonical constructor — must assign all fields
    public Email(String value) {
        if (value == null || !value.contains("@")) {
            throw new IllegalArgumentException("Invalid email: " + value);
        }
        this.value = value.toLowerCase().trim();
    }
}
```

### Additional Methods and Static Members

```java
public record Employee(String name, String department, double salary) {

    // Static fields and methods are allowed
    public static final Employee DEFAULT = new Employee("Unknown", "N/A", 0.0);

    // Custom instance methods
    public String formattedSalary() {
        return "$%.2f".formatted(salary);
    }

    // Custom accessor override (still must match return type)
    public String name() {
        return name.toUpperCase();
    }

    // Additional constructors — must delegate to the canonical constructor
    public Employee(String name) {
        this(name, "General", 50000.0);
    }
}
```

### Records Implement Interfaces

```java
public sealed interface Expr permits Literal, BinOp {}

public record Literal(double value) implements Expr, Comparable<Literal> {
    @Override
    public int compareTo(Literal other) {
        return Double.compare(this.value, other.value);
    }
}

public record BinOp(Expr left, String op, Expr right) implements Expr {}
```

### What Records Cannot Do

| Restriction | Reason |
|-------------|--------|
| Cannot extend another class | Implicitly extends `java.lang.Record` |
| Cannot declare instance fields beyond components | Ensures transparency |
| Cannot be `abstract` | Must be implicitly `final` |
| Cannot use `native` methods | Design constraint |
| Components are implicitly `final` | Immutability guarantee |
| No setters | Immutability guarantee |

### Local Records

Records can be declared inside methods:

```java
public List<String> processOrders(List<Order> orders) {
    record OrderSummary(String id, double total) {}  // local record

    return orders.stream()
        .map(o -> new OrderSummary(o.getId(), o.calculateTotal()))
        .filter(s -> s.total() > 100)
        .map(OrderSummary::id)
        .toList();
}
```

### Records and Serialization

Records support `Serializable` with improved security — deserialization always uses the canonical constructor:

```java
public record User(String name, int age) implements Serializable {
    private static final long serialVersionUID = 1L;
    // No custom readObject/writeObject needed
    // Deserialization goes through the canonical constructor
}
```

### Reflection API

```java
RecordComponent[] components = Point.class.getRecordComponents();
for (RecordComponent rc : components) {
    System.out.println(rc.getName() + " : " + rc.getType());
    // x : int
    // y : int
}
boolean isRecord = Point.class.isRecord();  // true
```

---

## 4. Text Blocks (JEP 378)

### What Are Text Blocks?

Multi-line string literals delimited by triple double-quotes (`"""`). They preserve formatting while stripping **incidental indentation**.

**Status:** Finalized in Java 15 (Preview in Java 13 & 14).

### Syntax Rules

```java
// Opening """ must be followed by a line terminator
// Content starts on the NEXT line
String textBlock = """
        Hello,
        World!
        """;
// Result: "Hello,\nWorld!\n"
```

### Indentation Handling

The compiler removes **common leading whitespace** (incidental indentation). The position of the closing `"""` determines the baseline:

```java
// Closing """ on its own line — controls indentation
String s1 = """
        Hello
        World
        """;
// "Hello\nWorld\n" — all leading spaces are incidental

String s2 = """
        Hello
        World
    """;
// "    Hello\n    World\n" — 4 spaces retained (relative to closing """)

// Closing """ on the last line — no trailing newline
String s3 = """
        Hello
        World""";
// "Hello\nWorld" — no trailing newline
```

### Escape Sequences

| Escape | Purpose | Example |
|--------|---------|---------|
| `\n` | Newline | Standard |
| `\t` | Tab | Standard |
| `\"` | Double quote | Standard |
| `\\` | Backslash | Standard |
| `\s` | Literal space (NEW) | Prevents trailing whitespace stripping |
| `\<newline>` | Line continuation (NEW) | Joins lines without inserting `\n` |

```java
// \s — preserve trailing spaces
String aligned = """
        Name:   John\s\s
        Age:    30\s\s\s
        """;

// \ — line continuation (no newline inserted)
String longLine = """
        This is a very long \
        sentence that spans \
        multiple lines but renders as one.""";
// "This is a very long sentence that spans multiple lines but renders as one."
```

### Methods on Text Blocks

Text blocks produce ordinary `String` objects, so all `String` methods work:

```java
String json = """
        {
            "name": "%s",
            "age": %d
        }
        """.formatted("Alice", 30);

// stripIndent() — manually apply indentation stripping
// translateEscapes() — process escape sequences

String html = """
        <html>
            <body>%s</body>
        </html>
        """.formatted("<p>Hello</p>");
```

### Practical Use Cases

```java
// SQL
String sql = """
        SELECT e.name, e.salary, d.department_name
        FROM employees e
        JOIN departments d ON e.dept_id = d.id
        WHERE e.salary > ?
        ORDER BY e.salary DESC
        """;

// JSON
String json = """
        {
            "id": 1,
            "name": "Java 17",
            "features": ["sealed classes", "records", "text blocks"]
        }
        """;

// HTML
String html = """
        <html>
        <head><title>%s</title></head>
        <body>
            <h1>%s</h1>
            <p>%s</p>
        </body>
        </html>
        """.formatted(title, heading, content);

// Regex
String pattern = """
        \\d{3}    # area code
        -         # separator
        \\d{3}    # exchange
        -         # separator
        \\d{4}    # subscriber
        """;
```

---

## 5. Switch Expressions (JEP 361)

### What Changed?

Switch can now be used as an **expression** (returns a value), supports **arrow labels** (`->`), and requires **exhaustiveness** when used as an expression.

**Status:** Finalized in Java 14 (Preview in Java 12 & 13).

### Old vs. New Syntax

```java
// ❌ Old — statement, fall-through risk
switch (day) {
    case MONDAY:
    case FRIDAY:
    case SUNDAY:
        numLetters = 6;
        break;
    case TUESDAY:
        numLetters = 7;
        break;
    default:
        numLetters = -1;
}

// ✅ New — expression, no fall-through, returns a value
int numLetters = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> 6;
    case TUESDAY                -> 7;
    case WEDNESDAY, THURSDAY    -> 8;
    case SATURDAY               -> 8;
};
```

### Arrow Labels (`->`)

- No fall-through — each arm is independent.
- Right side can be an expression, a block (with `yield`), or a throw statement.
- Multiple constants per case separated by commas.

### The `yield` Keyword

Used to return a value from a block inside a switch expression:

```java
String description = switch (statusCode) {
    case 200 -> "OK";
    case 301 -> "Moved Permanently";
    case 404 -> "Not Found";
    case 500 -> {
        logger.severe("Internal server error occurred");
        yield "Internal Server Error";  // yield returns the value
    }
    default -> {
        logger.warning("Unrecognized status: " + statusCode);
        yield "Unknown";
    }
};
```

### Exhaustiveness

When used as an expression, the switch must cover all possible input values:

```java
// Enum — must cover all constants or have a default
enum Season { SPRING, SUMMER, AUTUMN, WINTER }

String weather = switch (season) {
    case SPRING -> "Mild";
    case SUMMER -> "Hot";
    case AUTUMN -> "Cool";
    case WINTER -> "Cold";
    // No default needed — all enum constants are covered
};

// Non-enum types — MUST have a default
int result = switch (str) {
    case "hello" -> 1;
    case "world" -> 2;
    default -> 0;  // Required
};
```

### Colon Labels Still Work

You can still use `:` labels with `yield` in expression form:

```java
int result = switch (s) {
    case "Foo":
    case "Bar":
        yield 1;  // fall-through from "Foo" to "Bar", then yield
    default:
        yield 0;
};
```

### Null Handling in Switch (Preview in Java 17)

```java
// Before Java 17 — NullPointerException if selector is null
// Java 17 Preview — explicit null case
String result = switch (s) {
    case null  -> "Null value";
    case "foo" -> "Foo";
    default    -> "Other";
};
```

---

## 6. Pattern Matching for switch (Preview — JEP 406)

### What Is It?

Extends switch expressions and statements to use patterns in case labels, enabling type-based branching with pattern variables.

**Status:** Preview in Java 17. Finalized in Java 21.

### Type Pattern in Switch

```java
// Enable preview: javac --enable-preview --source 17
static String describe(Object obj) {
    return switch (obj) {
        case Integer i    -> "Integer: " + i;
        case Long l       -> "Long: " + l;
        case Double d     -> "Double: " + d;
        case String s     -> "String: " + s;
        case int[] arr    -> "Array of length " + arr.length;
        case null         -> "Null!";
        default           -> "Unknown: " + obj.getClass().getName();
    };
}
```

### Guarded Patterns

```java
static String categorize(Object obj) {
    return switch (obj) {
        case Integer i && i > 0  -> "Positive integer: " + i;
        case Integer i && i == 0 -> "Zero";
        case Integer i           -> "Negative integer: " + i;
        case String s && s.isEmpty() -> "Empty string";
        case String s            -> "Non-empty string: " + s;
        default                  -> "Something else";
    };
}
// Note: In Java 21, the syntax changed from && to `when` keyword:
// case Integer i when i > 0 -> ...
```

### Dominance and Ordering

More specific patterns must appear **before** more general ones:

```java
// ✅ Correct order
switch (obj) {
    case String s && s.length() > 10 -> "Long string";
    case String s                     -> "Short string";
    case CharSequence cs              -> "CharSequence";
    default                           -> "Other";
}

// ❌ Compile error — CharSequence dominates String
switch (obj) {
    case CharSequence cs -> "CharSequence";
    case String s        -> "String";  // ERROR: unreachable
    default              -> "Other";
}
```

### Sealed Classes + Pattern Matching Switch (Exhaustiveness)

```java
sealed interface Shape permits Circle, Rectangle, Triangle {}
record Circle(double radius) implements Shape {}
record Rectangle(double l, double w) implements Shape {}
record Triangle(double b, double h) implements Shape {}

double area = switch (shape) {
    case Circle c    -> Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.l() * r.w();
    case Triangle t  -> 0.5 * t.b() * t.h();
    // No default needed — sealed hierarchy is exhaustive
};
```

---

## 7. Enhanced Pseudo-Random Number Generators (JEP 356)

### What Changed?

Introduces a new interface hierarchy (`RandomGenerator`) and new PRNG algorithms. Provides a unified API for all random number generators.

### New Interface Hierarchy

```
RandomGenerator (top-level interface)
├── SplittableRandomGenerator     — supports split()
├── JumpableRandomGenerator       — supports jump()
│   └── LeapableRandomGenerator   — supports leap()
├── StreamableRandomGenerator     — supports rngs(), rngs(long)
└── ArbitrarilyJumpableRandomGenerator — supports jumpTo(double)
```

### New Algorithms

| Algorithm | Type | Notes |
|-----------|------|-------|
| `L32X64MixRandom` | LXM | Good for general use |
| `L64X128MixRandom` | LXM | Higher period |
| `L64X256MixRandom` | LXM | Even higher period |
| `L128X128MixRandom` | LXM | Very high period |
| `L128X256MixRandom` | LXM | Highest period |
| `Xoshiro256PlusPlus` | Xoshiro | Fast, good statistical quality |
| `Xoroshiro128PlusPlus` | Xoroshiro | Fast, smaller state |

### Usage Examples

```java
import java.util.random.RandomGenerator;
import java.util.random.RandomGeneratorFactory;

// Use the new factory approach
RandomGenerator rng = RandomGeneratorFactory.of("L64X128MixRandom").create();

// Or use the convenience method
RandomGenerator rng2 = RandomGenerator.of("Xoshiro256PlusPlus");

// Generate values (same methods as Random)
int randomInt = rng.nextInt(100);
double randomDouble = rng.nextDouble();
long randomLong = rng.nextLong();

// Stream of random numbers
rng.ints(10, 0, 100).forEach(System.out::println);

// List all available algorithms
RandomGeneratorFactory.all()
    .map(RandomGeneratorFactory::name)
    .sorted()
    .forEach(System.out::println);

// Check algorithm properties
RandomGeneratorFactory.all()
    .filter(factory -> factory.group().equals("LXM"))
    .forEach(factory -> System.out.printf(
        "%-25s period=2^%d splittable=%b%n",
        factory.name(),
        factory.stateBits(),
        factory.isSplittable()
    ));
```

### Legacy Classes Now Implement RandomGenerator

`java.util.Random`, `ThreadLocalRandom`, and `SplittableRandom` now implement the `RandomGenerator` interface, so legacy code works seamlessly:

```java
RandomGenerator rng = new Random();          // works
RandomGenerator rng = ThreadLocalRandom.current();  // works
```

---

## 8. New macOS Rendering Pipeline (JEP 382)

### What Changed?

- Replaces the deprecated **Apple OpenGL** rendering pipeline with a new **Apple Metal** rendering pipeline for Java2D on macOS.
- Apple deprecated OpenGL in macOS 10.14 (Mojave).
- The Metal pipeline is the default on macOS in Java 17.
- Enabled via: `-Dsun.java2d.metal=true` (or it is default).
- Fallback: `-Dsun.java2d.metal=false` to force OpenGL.

### Interview Tip

> This is a **platform-specific change** and affects only **macOS users** running Swing/AWT/Java2D applications. Not asked in detail but good to mention awareness.

---

## 9. macOS/AArch64 Port (JEP 391)

### What Changed?

- Provides a native JDK port for **macOS on Apple Silicon (M1, M2, etc.)** — the AArch64 (ARM64) architecture.
- Previously Java ran on Apple Silicon only via Rosetta 2 (x86 emulation).
- This gives **native performance** on Apple Silicon Macs.

### Key Points

- The `os.arch` property returns `aarch64` on Apple Silicon.
- Conditional code checking architecture:

```java
String arch = System.getProperty("os.arch");
if ("aarch64".equals(arch)) {
    System.out.println("Running natively on Apple Silicon");
}
```

---

## 10. Deprecate the Applet API for Removal (JEP 398)

### What Changed?

The **Applet API** is deprecated for removal. Key classes:

- `java.applet.Applet`
- `java.applet.AppletStub`
- `java.applet.AppletContext`
- `java.applet.AudioClip`
- `javax.swing.JApplet`

### Why?

- All major browsers dropped support for Java plugins years ago.
- Applets are a dead technology.
- The classes remain in the JDK but are annotated with `@Deprecated(since="9", forRemoval=true)`.

---

## 11. Strongly Encapsulate JDK Internals (JEP 403)

### What Changed?

- It is no longer possible to use `--illegal-access` to relax strong encapsulation of JDK internals.
- Internal APIs (e.g., `sun.misc.Unsafe`, `sun.reflect.*`) are **inaccessible by default**.
- The `--illegal-access=permit|warn|debug|deny` flag (introduced in Java 9) is removed.
- The only way to access internal APIs now is `--add-opens` on the command line.

### Impact

```bash
# ❌ No longer works in Java 17
java --illegal-access=permit MyApp

# ✅ Use specific --add-opens flags instead
java --add-opens java.base/java.lang=ALL-UNNAMED MyApp
java --add-opens java.base/sun.nio.ch=ALL-UNNAMED MyApp
```

### Critical APIs Affected

| Internal API | Replacement |
|-------------|-------------|
| `sun.misc.Unsafe` | `java.lang.invoke.VarHandle`, `MemorySegment` (incubating) |
| `sun.reflect.Reflection` | `StackWalker` API |
| `com.sun.crypto.provider` | Standard `javax.crypto` |

### Interview Tip

> This affects many legacy libraries (Hibernate, Spring, Jackson older versions). Know the `--add-opens` flag and module system.

---

## 12. Remove RMI Activation (JEP 407)

### What Changed?

- **Removed** the RMI Activation mechanism (`java.rmi.activation` package).
- RMI itself (remote method invocation) still exists, only the activation part is removed.
- The `rmid` tool (RMI activation daemon) is also removed.

### Why?

- RMI Activation was obsolete, rarely used, and had a maintenance burden.
- Modern distributed systems use REST, gRPC, message queues, etc.

---

## 13. Remove the Experimental AOT and JIT Compiler (JEP 410)

### What Changed?

- Removed the **experimental Java-based Ahead-of-Time (AOT) compiler** (`jaotc` tool).
- Removed the **experimental Graal JIT compiler** from the JDK.
- The `jaotc` tool and related modules (`jdk.aot`) are gone.

### Why?

- Low adoption, high maintenance cost.
- GraalVM is available as a separate distribution for those needing AOT/Graal JIT.
- The standard C2 JIT compiler remains the default HotSpot JIT.

---

## 14. Deprecate the Security Manager for Removal (JEP 411)

### What Changed?

- The `SecurityManager` and related APIs are **deprecated for removal**.
- Running with a Security Manager emits a warning at startup.
- `System.setSecurityManager()` still works but is deprecated.

### Why?

- Complex, poorly understood, rarely used correctly.
- Not an effective security mechanism for modern applications.
- Container-level and OS-level security is preferred.

### Affected Classes

- `java.lang.SecurityManager`
- `java.security.Policy`
- `java.security.AccessController`
- `java.security.AccessControlContext`
- All `java.security.Permission` subclasses

---

## 15. Foreign Function & Memory API (Incubator — JEP 412)

### What Is It?

An API for **interacting with native code (C libraries) and native memory** without JNI. It combines the Foreign-Memory Access API and the Foreign Linker API.

**Status:** Incubator in Java 17. Finalized in Java 22.

### Key Abstractions

| Abstraction | Purpose |
|-------------|---------|
| `MemorySegment` | A contiguous region of memory (on- or off-heap) |
| `MemoryAddress` | A raw memory address |
| `SegmentAllocator` | Allocates memory segments |
| `ResourceScope` | Manages lifecycle of memory segments |
| `CLinker` | Link Java code to native (C) functions |
| `FunctionDescriptor` | Describes a native function's signature |
| `SymbolLookup` | Looks up native function addresses |

### Example — Allocating and Reading Native Memory

```java
// Requires: --add-modules jdk.incubator.foreign
import jdk.incubator.foreign.*;

try (ResourceScope scope = ResourceScope.newConfinedScope()) {
    // Allocate 100 bytes of native memory
    MemorySegment segment = MemorySegment.allocateNative(100, scope);

    // Write an int at offset 0
    segment.set(ValueLayout.JAVA_INT, 0, 42);

    // Read it back
    int value = segment.get(ValueLayout.JAVA_INT, 0);
    System.out.println(value);  // 42
}
// Memory is automatically freed when scope closes
```

### Example — Calling a Native C Function

```java
import jdk.incubator.foreign.*;
import java.lang.invoke.MethodHandle;

// Look up strlen from the C standard library
CLinker linker = CLinker.systemCLinker();
SymbolLookup lookup = CLinker.systemLookup();

MethodHandle strlen = linker.downcallHandle(
    lookup.lookup("strlen").get(),
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
);

try (ResourceScope scope = ResourceScope.newConfinedScope()) {
    MemorySegment cString = CLinker.toCString("Hello, Foreign!", scope);
    long length = (long) strlen.invoke(cString.address());
    System.out.println("Length: " + length);  // 15
}
```

### Foreign Function API vs. JNI

| Feature | JNI | Foreign Function API |
|---------|-----|---------------------|
| Boilerplate | High (native headers, C code, compile) | Minimal (pure Java) |
| Safety | Manual memory management | Scoped, auto-freed |
| Performance | Good but overhead at boundary | Optimized, less overhead |
| Ease of use | Complex | Straightforward |

---

## 16. Vector API (Second Incubator — JEP 414)

### What Is It?

An API for expressing **SIMD (Single Instruction, Multiple Data)** vector computations that compile to optimal hardware vector instructions (SSE, AVX, NEON, etc.) at runtime.

**Status:** Second Incubator in Java 17. Still incubating as of Java 22.

### Key Concepts

| Concept | Description |
|---------|-------------|
| `VectorSpecies` | Describes element type + vector length (e.g., 256-bit float) |
| `Vector<E>` | An immutable sequence of lane values |
| `VectorMask` | Boolean mask for conditional operations |
| `VectorShuffle` | Index map for rearranging lanes |

### Example

```java
// Requires: --add-modules jdk.incubator.vector
import jdk.incubator.vector.*;

static final VectorSpecies<Float> SPECIES = FloatVector.SPECIES_256;

static float[] vectorAdd(float[] a, float[] b) {
    float[] result = new float[a.length];
    int i = 0;
    int upperBound = SPECIES.loopBound(a.length);

    // Process in SIMD chunks
    for (; i < upperBound; i += SPECIES.length()) {
        FloatVector va = FloatVector.fromArray(SPECIES, a, i);
        FloatVector vb = FloatVector.fromArray(SPECIES, b, i);
        FloatVector vr = va.add(vb);
        vr.intoArray(result, i);
    }

    // Scalar tail
    for (; i < a.length; i++) {
        result[i] = a[i] + b[i];
    }

    return result;
}
```

---

## 17. Context-Specific Deserialization Filters (JEP 415)

### What Is It?

Allows applications to configure **context-specific and dynamically-selected deserialization filters** via a JVM-wide filter factory. This is a defense against deserialization attacks.

### Why?

Java deserialization is a well-known attack vector (arbitrary code execution). This JEP builds on the per-stream filters from JEP 290 (Java 9) to allow application-wide policies.

### Key Concepts

| Concept | Description |
|---------|-------------|
| `ObjectInputFilter` | Functional interface that accepts or rejects classes during deserialization |
| `ObjectInputFilter.Config.setSerialFilterFactory()` | Sets a JVM-wide filter factory |
| Filter factory | A `BinaryOperator<ObjectInputFilter>` that merges per-stream and global filters |

### Example

```java
import java.io.ObjectInputFilter;

// Set a JVM-wide filter factory (called once at startup)
ObjectInputFilter.Config.setSerialFilterFactory((currentFilter, newFilter) -> {
    // Combine current (stream-specific) filter with a global policy
    ObjectInputFilter globalFilter = ObjectInputFilter.Config.createFilter(
        "maxdepth=5;maxrefs=1000;!com.dangerous.**"
    );

    // Return a composite filter
    return ObjectInputFilter.merge(newFilter, globalFilter);
});

// Per-stream filter
ObjectInputFilter.Config.setSerialFilter(
    ObjectInputFilter.Config.createFilter("com.myapp.**;java.base/*;!*")
);
```

### Filter Pattern Syntax

| Pattern | Meaning |
|---------|---------|
| `com.myapp.**` | Allow all classes under `com.myapp` |
| `!com.dangerous.**` | Reject all classes under `com.dangerous` |
| `maxdepth=10` | Max nesting depth |
| `maxrefs=500` | Max object references |
| `maxbytes=1000000` | Max bytes read |
| `maxarray=10000` | Max array length |

---

## 18. Helpful NullPointerExceptions (JEP 358)

### What Changed?

The JVM now precisely describes **which variable was null** in a `NullPointerException`. Enabled by default since Java 15 (introduced in Java 14).

### Before vs. After

```java
Employee emp = getEmployee();
String city = emp.getAddress().getCity().toUpperCase();
```

```
// ❌ Before (Java 14-)
Exception in thread "main" java.lang.NullPointerException

// ✅ After (Java 14+)
Exception in thread "main" java.lang.NullPointerException:
    Cannot invoke "Address.getCity()" because the return value of
    "Employee.getAddress()" is null
```

### How It Works

- The JVM performs **data-flow analysis** on the bytecode at the point of the NPE.
- It identifies the exact expression that evaluated to `null`.
- Covers: field access, method invocation, array access, array store, unboxing.

### Enable/Disable

```bash
# Enabled by default since Java 15
# To disable:
java -XX:-ShowCodeDetailsInExceptionMessages MyApp
```

---

## 19. Compact Number Formatting

### What Is It?

Format numbers in a human-readable compact form (e.g., `1K`, `1M`, `1B`).

```java
import java.text.NumberFormat;
import java.util.Locale;

NumberFormat shortFormat = NumberFormat.getCompactNumberInstance(
    Locale.US, NumberFormat.Style.SHORT
);
shortFormat.setMaximumFractionDigits(1);

System.out.println(shortFormat.format(1_000));       // "1K"
System.out.println(shortFormat.format(1_500));       // "1.5K"
System.out.println(shortFormat.format(1_000_000));   // "1M"
System.out.println(shortFormat.format(1_000_000_000)); // "1B"

NumberFormat longFormat = NumberFormat.getCompactNumberInstance(
    Locale.US, NumberFormat.Style.LONG
);
System.out.println(longFormat.format(1_000));     // "1 thousand"
System.out.println(longFormat.format(1_000_000)); // "1 million"

// Locale-aware
NumberFormat indiaFormat = NumberFormat.getCompactNumberInstance(
    new Locale("hi", "IN"), NumberFormat.Style.SHORT
);
System.out.println(indiaFormat.format(10_00_000)); // "10 लाख"
```

---

## 20. Day Period Support in DateTimeFormatter

### What Is It?

The `B` pattern letter gives locale-aware day period names instead of AM/PM.

```java
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.Locale;

DateTimeFormatter formatter = DateTimeFormatter.ofPattern("h:mm B", Locale.US);

System.out.println(LocalTime.of(6, 0).format(formatter));   // "6:00 in the morning"
System.out.println(LocalTime.of(12, 0).format(formatter));  // "12:00 noon"
System.out.println(LocalTime.of(15, 0).format(formatter));  // "3:00 in the afternoon"
System.out.println(LocalTime.of(21, 0).format(formatter));  // "9:00 at night"
```

---

## 21. Stream.toList() Method

### What Is It?

A convenience method that returns an **unmodifiable list** from a stream. Simpler than `Collectors.toList()`.

### Comparison

```java
import java.util.List;
import java.util.stream.Collectors;

List<String> names = List.of("Alice", "Bob", "Charlie", "Diana");

// Old way — returns a MUTABLE list
List<String> filtered1 = names.stream()
    .filter(n -> n.length() > 3)
    .collect(Collectors.toList());
filtered1.add("Eve");  // ✅ Works

// New way — returns an UNMODIFIABLE list
List<String> filtered2 = names.stream()
    .filter(n -> n.length() > 3)
    .toList();
filtered2.add("Eve");  // ❌ UnsupportedOperationException

// For unmodifiable list (old way, equivalent to toList())
List<String> filtered3 = names.stream()
    .filter(n -> n.length() > 3)
    .collect(Collectors.toUnmodifiableList());
```

### Key Differences: `toList()` vs `Collectors.toList()` vs `Collectors.toUnmodifiableList()`

| Feature | `toList()` | `Collectors.toList()` | `Collectors.toUnmodifiableList()` |
|---------|-----------|----------------------|----------------------------------|
| Modifiable? | No | Yes | No |
| Allows null? | Yes | Yes | No |
| Type | Unmodifiable | ArrayList | Unmodifiable |
| Introduced | Java 16 | Java 8 | Java 10 |

---

## 22. Other Notable API Additions

### String New Methods (Java 11–17)

```java
// Java 11
"  hello  ".strip();          // "hello" (Unicode-aware)
"  hello  ".stripLeading();   // "hello  "
"  hello  ".stripTrailing();  // "  hello"
"  ".isBlank();               // true
"line1\nline2".lines();       // Stream<String>: ["line1", "line2"]
"abc".repeat(3);              // "abcabcabc"

// Java 12
"hello".indent(4);            // "    hello\n"
"hello".transform(s -> s.toUpperCase());  // "HELLO"

// Java 15
" hello ".stripIndent();      // Strips common leading whitespace
" hello ".translateEscapes(); // Processes escape sequences
```

### Files New Methods

```java
import java.nio.file.Files;
import java.nio.file.Path;

// Java 11 — Read/Write strings directly
String content = Files.readString(Path.of("file.txt"));
Files.writeString(Path.of("output.txt"), "Hello, World!");

// Java 12 — Mismatch (returns position of first differing byte, -1 if identical)
long mismatch = Files.mismatch(Path.of("file1.txt"), Path.of("file2.txt"));
```

### NIO Improvements

```java
import java.nio.channels.SocketChannel;
import java.net.UnixDomainSocketAddress;
import java.net.StandardProtocolFamily;

// Java 16 — Unix-Domain Socket Channels
var address = UnixDomainSocketAddress.of("/tmp/my.socket");
var channel = SocketChannel.open(StandardProtocolFamily.UNIX);
channel.connect(address);
```

### Process and InstantSource

```java
// Process — get the process PID
ProcessHandle.current().pid();

// Java 17 — InstantSource (interface for testable time)
import java.time.InstantSource;

InstantSource source = InstantSource.system();
Instant now = source.instant();

// In tests, provide a fixed source
InstantSource fixedSource = InstantSource.fixed(Instant.parse("2025-01-01T00:00:00Z"));
```

### HexFormat (Java 17)

```java
import java.util.HexFormat;

HexFormat hex = HexFormat.of();

// Byte array to hex string
byte[] bytes = {0x00, 0x1A, (byte) 0xFF};
String hexStr = hex.formatHex(bytes);        // "001aff"

// Hex string to byte array
byte[] parsed = hex.parseHex("001aff");

// With delimiters and uppercase
HexFormat prettyHex = HexFormat.ofDelimiter(":").withUpperCase();
String formatted = prettyHex.formatHex(bytes); // "00:1A:FF"

// Single value conversions
String singleHex = hex.toHexDigits((byte) 0x2F);  // "2f"
int value = hex.fromHexDigits("2f");               // 47
```

### Map.Entry Creation

```java
// Java 9+
var entry = Map.entry("key", "value");  // Immutable entry
```

---

## 23. Garbage Collectors in Java 17

### Available GCs

| GC | Flag | Default? | Best For |
|----|------|----------|----------|
| **G1 GC** | `-XX:+UseG1GC` | Yes (default) | General-purpose, balanced throughput/latency |
| **ZGC** | `-XX:+UseZGC` | No | Ultra-low latency (<1ms pause), large heaps |
| **Shenandoah** | `-XX:+UseShenandoahGC` | No | Low latency, concurrent compaction |
| **Parallel GC** | `-XX:+UseParallelGC` | No | Maximum throughput |
| **Serial GC** | `-XX:+UseSerialGC` | No | Single-threaded, small heaps, embedded |
| **Epsilon GC** | `-XX:+UseEpsilonGC` | No | No-op GC (testing, benchmarks) |

### ZGC (Production-Ready since Java 15)

- Sub-millisecond pause times regardless of heap size.
- Supports heap sizes from 8MB to 16TB.
- Concurrent marking, relocation, and reference processing.
- `+UseZGC` in Java 17 is production-ready and fully supported.

### Shenandoah (Production-Ready since Java 15)

- Low pause times through concurrent compaction.
- Available in OpenJDK builds (not Oracle JDK in some builds).

---

## 24. Migration from Java 11 to Java 17

### Compilation Changes

| Area | Action Required |
|------|----------------|
| Internal API usage | Replace with public APIs or add `--add-opens` |
| `javax.annotation`, `javax.xml.bind` | Add external dependencies (Jakarta EE) |
| `SecurityManager` usage | Plan for removal, use OS-level security |
| Reflection on JDK internals | Use `--add-opens` or public APIs |

### Common Migration Issues

```xml
<!-- Add these dependencies if migrating from Java 11 -->
<!-- JAXB (removed from JDK) -->
<dependency>
    <groupId>jakarta.xml.bind</groupId>
    <artifactId>jakarta.xml.bind-api</artifactId>
    <version>4.0.0</version>
</dependency>

<!-- JAX-WS (removed from JDK) -->
<dependency>
    <groupId>jakarta.xml.ws</groupId>
    <artifactId>jakarta.xml.ws-api</artifactId>
    <version>4.0.0</version>
</dependency>

<!-- Java Activation (removed from JDK) -->
<dependency>
    <groupId>jakarta.activation</groupId>
    <artifactId>jakarta.activation-api</artifactId>
    <version>2.1.0</version>
</dependency>
```

### JVM Flags Changes

```bash
# Removed flags (will cause JVM startup failure)
-XX:+UseConcMarkSweepGC         # CMS removed in Java 14
--illegal-access=permit          # Removed in Java 17
-XX:+UseAdaptiveGCBoundary       # Removed

# New/Changed flags
-XX:+UseZGC                      # Production-ready
--add-opens java.base/java.lang=ALL-UNNAMED  # Required for some libraries
```

---

## 25. Quick Interview Cheat Sheet

### Feature Matrix — Java 12 through 17

| Feature | Introduced | Finalized | JEP |
|---------|-----------|-----------|-----|
| Switch Expressions | Java 12 (Preview) | Java 14 | 361 |
| Text Blocks | Java 13 (Preview) | Java 15 | 378 |
| Records | Java 14 (Preview) | Java 16 | 395 |
| Pattern Matching for `instanceof` | Java 14 (Preview) | Java 16 | 394 |
| Sealed Classes | Java 15 (Preview) | Java 17 | 409 |
| Helpful NullPointerExceptions | Java 14 | Java 15 (default) | 358 |
| ZGC (Production) | Java 11 (Experimental) | Java 15 | 377 |
| Shenandoah (Production) | Java 12 (Experimental) | Java 15 | 379 |
| `Stream.toList()` | Java 16 | Java 16 | — |
| `HexFormat` | Java 17 | Java 17 | — |
| Foreign Function & Memory API | Java 14 (Incubator) | Java 22 | 412 |
| Vector API | Java 16 (Incubator) | Incubating | 414 |
| Pattern Matching for `switch` | Java 17 (Preview) | Java 21 | 406 |
| Enhanced PRNGs | Java 17 | Java 17 | 356 |
| Context-Specific Deserialization | Java 17 | Java 17 | 415 |

### Top 10 Interview Questions — Quick Answers

**Q1: Why is Java 17 important?**
It is an **LTS release**, production-supported for years. It finalizes sealed classes, records, pattern matching for instanceof, text blocks, and switch expressions.

**Q2: What are sealed classes?**
Classes/interfaces that restrict which types can extend/implement them using `sealed` + `permits`. Subclasses must be `final`, `sealed`, or `non-sealed`.

**Q3: How do records differ from regular classes?**
Records are transparent data carriers — the compiler generates `equals()`, `hashCode()`, `toString()`, accessors, and a canonical constructor. They are implicitly `final`, extend `java.lang.Record`, and cannot have mutable instance fields.

**Q4: What does `Stream.toList()` return?**
An **unmodifiable** list. Unlike `Collectors.toList()` which returns a mutable `ArrayList`.

**Q5: What is the difference between text blocks and regular strings?**
Text blocks use `"""..."""`, preserve multi-line formatting, strip incidental indentation, support `\s` and `\<newline>` escapes, and produce ordinary `String` objects.

**Q6: What is pattern matching for `instanceof`?**
It combines type checking and casting into one step: `if (obj instanceof String s)` — `s` is a pattern variable available via flow scoping where the match is guaranteed.

**Q7: What is the `yield` keyword?**
Used inside switch expression blocks to return a value. It is NOT a general `return` — it is specific to switch expressions.

**Q8: Why was `--illegal-access` removed?**
To enforce strong encapsulation of JDK internals. Access to internal APIs requires explicit `--add-opens` flags, improving security and module boundaries.

**Q9: What is `HexFormat`?**
A Java 17 utility class for converting between bytes and hexadecimal strings, with options for delimiters, upper/lower case, and prefix/suffix.

**Q10: What are the GC options in Java 17?**
G1 (default), ZGC (ultra-low latency, production-ready), Shenandoah (low latency), Parallel (throughput), Serial (small heaps), Epsilon (no-op).

---

> **Tip:** When asked "What's new in Java 17?" in an interview, focus on the **five finalized language features**: Sealed Classes, Records, Pattern Matching for instanceof, Text Blocks, and Switch Expressions. Then mention HexFormat, Stream.toList(), strong encapsulation, and GC improvements as supporting points.
