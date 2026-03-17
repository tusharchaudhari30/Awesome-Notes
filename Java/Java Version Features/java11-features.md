# Java 11 Features — Complete Interview-Ready Notes

> **Release Date:** September 25, 2018
> **License:** Oracle changed to a subscription-based model. OpenJDK 11 is free under GPL+CE.
> **LTS Version:** Java 11 is a **Long-Term Support (LTS)** release (after Java 8). LTS releases receive extended updates and patches.
> **Key Fact:** Java 11 removed several modules and APIs that were deprecated in Java 9/10 (e.g., Java EE, CORBA modules). It is the first LTS release under the new 6-month release cadence.

---

## Table of Contents

1. [New String Methods](#1-new-string-methods)
2. [New File Methods — Files.readString() and Files.writeString()](#2-new-file-methods--filesreadstring-and-fileswritestring)
3. [Collection to Array — toArray(IntFunction)](#3-collection-to-array--toarrayintfunction)
4. [The `not()` Predicate Method](#4-the-not-predicate-method)
5. [Local-Variable Syntax for Lambda Parameters (var in Lambdas)](#5-local-variable-syntax-for-lambda-parameters-var-in-lambdas)
6. [HTTP Client API (Standardized)](#6-http-client-api-standardized)
7. [Optional New Methods — isEmpty()](#7-optional-new-methods--isempty)
8. [Nest-Based Access Control](#8-nest-based-access-control)
9. [Running Java Files Directly (Single-File Source-Code Programs)](#9-running-java-files-directly-single-file-source-code-programs)
10. [Epsilon Garbage Collector (No-Op GC)](#10-epsilon-garbage-collector-no-op-gc)
11. [Z Garbage Collector (ZGC) — Experimental](#11-z-garbage-collector-zgc--experimental)
12. [Flight Recorder (JFR)](#12-flight-recorder-jfr)
13. [Dynamic Class-File Constants](#13-dynamic-class-file-constants)
14. [Removed and Deprecated APIs/Features](#14-removed-and-deprecated-apisfeatures)
15. [Unicode 10 Support](#15-unicode-10-support)
16. [TLS 1.3 Support](#16-tls-13-support)
17. [Key Nashorn Deprecation](#17-key-nashorn-deprecation)
18. [Pattern Matching Preparation and Other Minor Changes](#18-pattern-matching-preparation-and-other-minor-changes)
19. [Complete JEP List for Java 11](#19-complete-jep-list-for-java-11)
20. [Top Interview Questions Summary](#20-top-interview-questions-summary)

---

## 1. New String Methods

Java 11 introduced **six** new methods to the `String` class. These are among the most frequently asked features in interviews.

### 1.1 `isBlank()`

Returns `true` if the string is empty or contains only **white space codepoints** (spaces, tabs, newlines, etc.). Uses `Character.isWhitespace()` internally.

```java
// isBlank() — checks for empty or whitespace-only strings
String str1 = "";
String str2 = "   ";
String str3 = " \t\n ";
String str4 = "Java";

System.out.println(str1.isBlank()); // true  (empty string)
System.out.println(str2.isBlank()); // true  (spaces only)
System.out.println(str3.isBlank()); // true  (tab + newline + space)
System.out.println(str4.isBlank()); // false (contains non-whitespace)
```

**Interview Tip:** `isBlank()` vs `isEmpty()`:
- `isEmpty()` returns `true` only if `length() == 0`. It does **not** consider whitespace.
- `isBlank()` returns `true` if the string is empty **OR** contains only whitespace.
- `"   ".isEmpty()` → `false`; `"   ".isBlank()` → `true`.

### 1.2 `strip()`, `stripLeading()`, `stripTrailing()`

Removes **leading and/or trailing whitespace** from a string. Uses Unicode-aware `Character.isWhitespace()`.

```java
String str = "  \t Hello Java 11 \n  ";

System.out.println(str.strip());          // "Hello Java 11"
System.out.println(str.stripLeading());   // "Hello Java 11 \n  "
System.out.println(str.stripTrailing());  // "  \t Hello Java 11"
```

**Interview Tip:** `strip()` vs `trim()`:
| Feature | `trim()` | `strip()` |
|---|---|---|
| Introduced in | Java 1.0 | Java 11 |
| Whitespace detection | Removes characters with codepoint ≤ `U+0020` (ASCII space) | Uses `Character.isWhitespace()` (Unicode-aware) |
| Unicode support | Does **NOT** handle Unicode whitespace like `\u2005` (Four-Per-Em Space) | **Handles** all Unicode whitespace characters |
| Example | `"\u2005Hello\u2005".trim()` → `"\u2005Hello\u2005"` (unchanged) | `"\u2005Hello\u2005".strip()` → `"Hello"` |

```java
// Demonstrating the difference
char unicodeSpace = '\u2005'; // Four-Per-Em Space
String str = unicodeSpace + "Java" + unicodeSpace;

System.out.println(str.trim().length());  // 6 (trim does NOT remove \u2005)
System.out.println(str.strip().length()); // 4 (strip DOES remove \u2005)
```

### 1.3 `lines()`

Returns a `Stream<String>` of lines extracted from the string, split by line terminators: `\n`, `\r`, or `\r\n`.

```java
String multiline = "Line1\nLine2\nLine3\r\nLine4";

multiline.lines()
         .forEach(System.out::println);
// Output:
// Line1
// Line2
// Line3
// Line4

// Count lines
long count = "A\nB\nC".lines().count();
System.out.println(count); // 3

// Collect to a list
List<String> lineList = "Hello\nWorld".lines().collect(Collectors.toList());
System.out.println(lineList); // [Hello, World]
```

**Key Detail:** A trailing line terminator does **not** cause an additional empty string at the end. `"A\nB\n".lines().count()` → `2`, not `3`.

### 1.4 `repeat(int count)`

Returns a string whose value is the concatenation of this string repeated `count` times. If count is `0`, the empty string is returned.

```java
String str = "Java ";

System.out.println(str.repeat(3));  // "Java Java Java "
System.out.println(str.repeat(0));  // ""
System.out.println("AB".repeat(5)); // "ABABABABAB"

// Useful for formatting
System.out.println("-".repeat(40)); // "----------------------------------------"
```

**Edge Cases:**
- `repeat(0)` → `""` (empty string)
- `"".repeat(100)` → `""` (empty string)
- `repeat(-1)` → throws `IllegalArgumentException`
- If `count == 1` → returns the string itself
- If `string.length() * count` overflows `int`, throws `OutOfMemoryError`

---

## 2. New File Methods — `Files.readString()` and `Files.writeString()`

Java 11 added convenience methods to `java.nio.file.Files` for reading/writing strings directly.

### 2.1 `Files.readString(Path path)`

Reads all content from a file into a `String`. Uses **UTF-8** encoding by default.

```java
import java.nio.file.Files;
import java.nio.file.Path;

// Read entire file as a single String
String content = Files.readString(Path.of("example.txt"));
System.out.println(content);

// With explicit charset
String contentLatin = Files.readString(Path.of("data.txt"), StandardCharsets.ISO_8859_1);
```

### 2.2 `Files.writeString(Path path, CharSequence csq, OpenOption... options)`

Writes a `CharSequence` (e.g., `String`) to a file. Creates or overwrites the file by default.

```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

// Write string to a file (creates or overwrites)
Path path = Files.writeString(Path.of("output.txt"), "Hello Java 11!");

// Append to an existing file
Files.writeString(Path.of("output.txt"), "\nAppended line",
    StandardOpenOption.APPEND);

// With explicit charset
Files.writeString(Path.of("output.txt"), "日本語テキスト",
    StandardCharsets.UTF_8);
```

**Interview Tip:** Before Java 11, you had to use `Files.readAllBytes()` and then construct a `new String(bytes, charset)`, or use `BufferedReader`. Now it's a single method call.

---

## 3. Collection to Array — `toArray(IntFunction)`

Java 11 added a new default method `toArray(IntFunction<T[]> generator)` to the `java.util.Collection` interface.

```java
import java.util.List;

List<String> names = List.of("Alice", "Bob", "Charlie");

// Before Java 11 — clunky
String[] oldWay = names.toArray(new String[0]);

// Java 11 — using method reference with IntFunction
String[] newWay = names.toArray(String[]::new);

System.out.println(Arrays.toString(newWay)); // [Alice, Bob, Charlie]
```

**Interview Tip:** `String[]::new` is equivalent to `size -> new String[size]`. This is cleaner than `toArray(new String[0])` and is equally (or more) performant.

---

## 4. The `not()` Predicate Method

A new static method `Predicate.not(Predicate)` was added. It returns the **negation** of the supplied predicate. Extremely useful for method references where you previously couldn't negate them.

```java
import java.util.function.Predicate;
import java.util.List;
import java.util.stream.Collectors;

List<String> words = List.of("Java", "", "  ", "11", "Features", "");

// Before Java 11 — cannot negate a method reference directly
List<String> nonBlank1 = words.stream()
    .filter(s -> !s.isBlank())
    .collect(Collectors.toList());

// Java 11 — using Predicate.not() with method reference
List<String> nonBlank2 = words.stream()
    .filter(Predicate.not(String::isBlank))
    .collect(Collectors.toList());

System.out.println(nonBlank2); // [Java, 11, Features]
```

**Why is this important?**
- Before Java 11, you could NOT negate method references. `filter(!String::isBlank)` is a compile error.
- `Predicate.not()` enables clean negation with method references.
- You can also statically import it: `import static java.util.function.Predicate.not;` → `filter(not(String::isBlank))`

---

## 5. Local-Variable Syntax for Lambda Parameters (var in Lambdas)

**JEP 323** — Allows `var` to be used when declaring the formal parameters of implicitly typed lambda expressions.

### Why was this added?

In Java 10, `var` was introduced for local variable type inference. But you could **not** use `var` in lambda parameters. Java 11 fixes this.

```java
// Java 10 lambdas (already valid — implicit types)
(x, y) -> x + y

// Java 11 — you can now use 'var'
(var x, var y) -> x + y
```

### The real benefit — annotations on lambda parameters:

```java
import javax.annotation.Nonnull;

// Without var — cannot add annotations to implicitly typed parameters
// (@Nonnull x, @Nonnull y) -> x + y   // COMPILE ERROR in Java 10

// With var in Java 11 — annotations are possible
(@Nonnull var x, @Nonnull var y) -> x + y  // VALID
```

### Rules and Restrictions:

```java
// VALID usages:
(var x, var y) -> x + y               // All params use var
(var x) -> x.toUpperCase()            // Single param with var

// INVALID usages:
(var x, y) -> x + y                   // Cannot mix var and implicit — COMPILE ERROR
(var x, int y) -> x + y               // Cannot mix var and explicit types — COMPILE ERROR
var x -> x.toUpperCase()              // Parentheses required when using var — COMPILE ERROR
```

**Interview Rule Summary:**
1. If you use `var` for one lambda parameter, you must use `var` for **all** parameters.
2. You **cannot mix** `var` with explicit types (e.g., `(var x, int y)` is illegal).
3. You **cannot mix** `var` with implicit (no-type) parameters (e.g., `(var x, y)` is illegal).
4. Parentheses are **required** when using `var` (e.g., `var x -> ...` is illegal, must be `(var x) -> ...`).
5. The primary use case is adding **annotations** to lambda parameters.

---

## 6. HTTP Client API (Standardized)

**JEP 321** — The HTTP Client that was introduced as an **incubator module** in Java 9 (`jdk.incubator.httpclient`) is now **standardized** in Java 11 under `java.net.http`.

### Key Classes:

| Class | Description |
|---|---|
| `HttpClient` | The main entry point. Sends requests and receives responses. |
| `HttpRequest` | Represents an HTTP request (immutable). |
| `HttpResponse` | Represents an HTTP response. |
| `HttpResponse.BodyHandlers` | Predefined handlers for common body types. |
| `HttpRequest.BodyPublishers` | Predefined publishers for sending request bodies. |
| `WebSocket` | Support for the WebSocket protocol. |

### Key Features:

- Supports **HTTP/1.1** and **HTTP/2** (with automatic fallback)
- Supports **synchronous** and **asynchronous** request processing
- Supports **WebSocket** communication
- Uses **Builder pattern** for creating requests and clients
- Supports **reactive streams** (`Flow` API) for body processing
- Immutable and **thread-safe**

### 6.1 Synchronous GET Request

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

HttpClient client = HttpClient.newHttpClient(); // default settings

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://jsonplaceholder.typicode.com/posts/1"))
    .header("Accept", "application/json")
    .GET()  // default method — can be omitted
    .build();

// Synchronous call — blocks until response is received
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

System.out.println("Status Code: " + response.statusCode());   // 200
System.out.println("Headers: " + response.headers());
System.out.println("Body: " + response.body());
```

### 6.2 Asynchronous GET Request

```java
import java.util.concurrent.CompletableFuture;

HttpClient client = HttpClient.newHttpClient();

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://jsonplaceholder.typicode.com/posts/1"))
    .build();

// Asynchronous call — returns CompletableFuture
CompletableFuture<HttpResponse<String>> futureResponse =
    client.sendAsync(request, HttpResponse.BodyHandlers.ofString());

futureResponse
    .thenApply(HttpResponse::body)
    .thenAccept(System.out::println)
    .join(); // wait for completion
```

### 6.3 POST Request with Body

```java
HttpClient client = HttpClient.newHttpClient();

String json = """
    {"title": "foo", "body": "bar", "userId": 1}
    """; // Note: text blocks are Java 13+; use regular string for Java 11

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://jsonplaceholder.typicode.com/posts"))
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(
        "{\"title\": \"foo\", \"body\": \"bar\", \"userId\": 1}"))
    .build();

HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
System.out.println(response.statusCode()); // 201
System.out.println(response.body());
```

### 6.4 Configuring HttpClient

```java
import java.net.ProxySelector;
import java.time.Duration;

HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)             // prefer HTTP/2
    .followRedirects(HttpClient.Redirect.NORMAL)    // follow redirects
    .connectTimeout(Duration.ofSeconds(10))          // connection timeout
    .proxy(ProxySelector.getDefault())               // proxy settings
    .authenticator(Authenticator.getDefault())       // authentication
    .build();
```

### 6.5 Common BodyHandlers

```java
// String body
HttpResponse.BodyHandlers.ofString()

// Byte array
HttpResponse.BodyHandlers.ofByteArray()

// File (save response body to a file)
HttpResponse.BodyHandlers.ofFile(Path.of("response.json"))

// InputStream
HttpResponse.BodyHandlers.ofInputStream()

// Discard body
HttpResponse.BodyHandlers.discarding()

// Line-by-line streaming
HttpResponse.BodyHandlers.ofLines()
```

### 6.6 Common BodyPublishers

```java
// String body
HttpRequest.BodyPublishers.ofString("Hello")

// File body
HttpRequest.BodyPublishers.ofFile(Path.of("data.json"))

// Byte array
HttpRequest.BodyPublishers.ofByteArray(bytes)

// No body
HttpRequest.BodyPublishers.noBody()

// InputStream
HttpRequest.BodyPublishers.ofInputStream(() -> inputStream)
```

### 6.7 WebSocket Example

```java
HttpClient client = HttpClient.newHttpClient();

WebSocket webSocket = client.newWebSocketBuilder()
    .buildAsync(URI.create("ws://echo.websocket.org"), new WebSocket.Listener() {
        @Override
        public void onOpen(WebSocket webSocket) {
            System.out.println("Connected");
            webSocket.sendText("Hello WebSocket!", true);
            WebSocket.Listener.super.onOpen(webSocket);
        }

        @Override
        public CompletionStage<?> onText(WebSocket webSocket, CharSequence data, boolean last) {
            System.out.println("Received: " + data);
            return WebSocket.Listener.super.onText(webSocket, data, last);
        }
    }).join();
```

---

## 7. Optional New Methods — `isEmpty()`

Java 11 added the `isEmpty()` method to `java.util.Optional`, `OptionalInt`, `OptionalLong`, and `OptionalDouble`.

```java
import java.util.Optional;

Optional<String> optFull = Optional.of("Java 11");
Optional<String> optEmpty = Optional.empty();

// Java 11 — isEmpty()
System.out.println(optFull.isEmpty());  // false
System.out.println(optEmpty.isEmpty()); // true

// Compared to isPresent() — they are logical inverses
System.out.println(optFull.isPresent());  // true
System.out.println(optEmpty.isPresent()); // true → wait, that's wrong. Let me fix:
// optFull.isPresent()  → true
// optEmpty.isPresent() → false
```

**Interview Tip:**
- `isEmpty()` is the **logical negation** of `isPresent()`.
- `opt.isEmpty()` ≡ `!opt.isPresent()`
- Before Java 11, you had to write `!optional.isPresent()` which was awkward, especially in `if` conditions.
- `OptionalInt`, `OptionalLong`, `OptionalDouble` also received `isEmpty()`.

---

## 8. Nest-Based Access Control

**JEP 181** — Introduces **nests** as an access-control context in the JVM. This fixes a long-standing mismatch between how the Java language and the JVM handle private access for nested classes.

### The Problem (Before Java 11):

In Java, an outer class and its nested (inner) classes can access each other's private members at the **language level**. But at the **bytecode level**, the compiler generates **synthetic bridge methods** (package-private accessor methods) to allow this access, since the JVM treated them as separate, unrelated classes.

### The Java 11 Solution:

The JVM now understands the concept of **nests** (groups of classes that share private access). No more synthetic bridge methods are needed.

### New Reflection API Methods:

```java
// Class A with nested class B
public class Outer {
    private int x = 10;

    class Inner {
        private int y = 20;
    }

    public static void main(String[] args) {
        // getNestHost() — returns the nest host of this class
        System.out.println(Outer.class.getNestHost());        // class Outer
        System.out.println(Outer.Inner.class.getNestHost());  // class Outer

        // getNestMembers() — returns all members of the nest
        Class<?>[] nestMembers = Outer.class.getNestMembers();
        for (Class<?> member : nestMembers) {
            System.out.println(member.getName());
        }
        // Output: Outer, Outer$Inner

        // isNestmateOf() — checks if two classes are in the same nest
        System.out.println(Outer.class.isNestmateOf(Outer.Inner.class)); // true
    }
}
```

### New Reflection Methods Summary:

| Method | Description |
|---|---|
| `Class.getNestHost()` | Returns the nest host of this class. Returns itself if it has no nest host. |
| `Class.getNestMembers()` | Returns an array of all classes belonging to the same nest. |
| `Class.isNestmateOf(Class)` | Returns `true` if this class and the given class are in the same nest. |

**Interview Keywords:** Nest-based access control, nest host, nest members, nestmates, synthetic bridge methods eliminated, JEP 181.

---

## 9. Running Java Files Directly (Single-File Source-Code Programs)

**JEP 330** — You can now run a Java source file directly with `java` without explicitly compiling it first with `javac`.

```bash
# Before Java 11 — two-step process
javac HelloWorld.java
java HelloWorld

# Java 11 — single command
java HelloWorld.java
```

### Example:

```java
// File: HelloWorld.java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello from Java 11!");
    }
}
```

```bash
$ java HelloWorld.java
Hello from Java 11!
```

### Rules and Constraints:

1. The file **must** contain a class with a `public static void main(String[] args)` method.
2. All classes must be in a **single source file**.
3. The first class in the file is the one that is executed (it must have `main()`).
4. The file is compiled **in-memory** and executed — no `.class` file is produced.
5. The file extension **does not** have to be `.java` when passed to the `java` launcher.
6. Cannot reference classes in other source files (only classes in the same file or on the classpath).
7. The source file must be the **first argument** after options.

### Shebang Support (Unix/Linux):

```java
#!/usr/bin/java --source 11
public class Script {
    public static void main(String[] args) {
        System.out.println("I'm a Java script!");
    }
}
```

```bash
$ chmod +x Script
$ ./Script
I'm a Java script!
```

**Interview Tip:** This is sometimes called the **"launch single-file source-code programs"** feature. The `--source` flag can be used to specify the Java version. This makes Java viable for scripting tasks and quick prototyping.

---

## 10. Epsilon Garbage Collector (No-Op GC)

**JEP 318** — A garbage collector that handles memory allocation but does **not** reclaim any memory. Once the heap is exhausted, the JVM shuts down with an `OutOfMemoryError`.

### How to Enable:

```bash
java -XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC MyApp
```

### Use Cases:

| Use Case | Explanation |
|---|---|
| **Performance testing** | Measure application performance without GC overhead or pauses |
| **Memory pressure testing** | Test how much memory an application actually needs |
| **Short-lived applications** | Apps that allocate less memory than available heap and exit quickly |
| **Latency-sensitive testing** | Benchmark worst-case latency without GC interference |
| **GC algorithm benchmarking** | Compare other GCs against "no GC" as a baseline |
| **Last-drop optimization** | Extremely latency-sensitive apps that can manage within the heap |

**Interview Keywords:** No-Op GC, Epsilon GC, JEP 318, no memory reclamation, OutOfMemoryError on heap exhaustion, experimental, performance benchmarking.

---

## 11. Z Garbage Collector (ZGC) — Experimental

**JEP 333** — A scalable, low-latency garbage collector designed for large heaps.

### Key Characteristics:

| Property | Value |
|---|---|
| **Max pause time** | < 10ms (regardless of heap size) |
| **Heap size support** | From 8MB to **16TB** |
| **Concurrent** | Almost all GC work is done concurrently with the application |
| **Region-based** | Uses dynamically sized regions |
| **NUMA-aware** | Optimized for Non-Uniform Memory Access |
| **Colored pointers** | Uses metadata bits in 64-bit pointers (reference coloring) |
| **Load barriers** | Uses load barriers instead of store barriers |
| **Platform** | Linux/x64 only in Java 11 (expanded later) |

### How to Enable:

```bash
java -XX:+UnlockExperimentalVMOptions -XX:+UseZGC MyApp
```

**Interview Keywords:** ZGC, JEP 333, sub-10ms pauses, terabyte heaps, concurrent, colored pointers, load barriers, region-based, NUMA-aware, experimental.

### Comparison with Other GCs in Java 11:

| GC | Focus | Pause Times | Heap Limit |
|---|---|---|---|
| **Serial** | Simplicity, small footprint | High | Small heaps |
| **Parallel (throughput)** | Maximum throughput | Medium-High | Medium |
| **G1 (default)** | Balanced throughput/latency | Medium (< 200ms target) | Large |
| **ZGC (experimental)** | Ultra-low latency | < 10ms | Up to 16TB |
| **Epsilon (experimental)** | No GC at all | N/A | Any |

---

## 12. Flight Recorder (JFR)

**JEP 328** — Java Flight Recorder, previously a commercial feature of Oracle JDK, is now **open-sourced** and available in OpenJDK 11.

### What is JFR?

- A **low-overhead** profiling and diagnostics framework built into the JVM.
- Collects diagnostic and profiling data about the JVM and Java application.
- Designed for **always-on** production use (< 1% overhead by default).
- Records **events** like GC pauses, thread states, I/O, method profiling, allocations, etc.
- Data is written to a binary `.jfr` file that can be analyzed with **JDK Mission Control (JMC)**.

### How to Use:

```bash
# Start recording from command line
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr MyApp

# Start recording with jcmd (runtime)
jcmd <PID> JFR.start duration=60s filename=recording.jfr

# Dump recording
jcmd <PID> JFR.dump filename=dump.jfr

# Stop recording
jcmd <PID> JFR.stop
```

### Programmatic API:

```java
import jdk.jfr.*;

// Define a custom event
@Label("My Custom Event")
@Description("Example of a custom JFR event")
class MyEvent extends Event {
    @Label("Message")
    String message;

    @Label("Value")
    int value;
}

// Use it in your code
public class JFRExample {
    public static void main(String[] args) {
        MyEvent event = new MyEvent();
        event.message = "Processing started";
        event.value = 42;
        event.begin();
        // ... perform work ...
        event.end();
        event.commit(); // record the event
    }
}
```

### JFR Event Categories:

| Category | Examples |
|---|---|
| **JVM** | GC events, class loading, JIT compilation |
| **OS** | CPU load, memory usage, thread scheduling |
| **Java Library** | I/O, socket, file operations |
| **Application** | Custom events defined by developers |

**Interview Keywords:** JFR, JEP 328, low-overhead profiling, production-ready, always-on diagnostics, `.jfr` file, JDK Mission Control, custom events, open-sourced from Oracle JDK.

---

## 13. Dynamic Class-File Constants

**JEP 309** — Extends the Java class-file format to support a new constant-pool form: `CONSTANT_Dynamic`. This is the lazy, on-demand cousin of `CONSTANT_InvokeDynamic`.

### Key Points:

- Adds a new constant pool entry type: `CONSTANT_Dynamic`
- The constant's value is computed at first use by invoking a **bootstrap method** (similar to `invokedynamic` for method calls).
- Reduces the cost and complexity of creating new forms of materializable class-file constants.
- Primarily benefits **language designers and compiler authors**, not typical application developers.
- Enables more efficient implementation of language features like pattern matching and records (in future versions).

**Interview Keywords:** CONSTANT_Dynamic, JEP 309, bootstrap methods, constant pool, lazy initialization, compiler optimization.

---

## 14. Removed and Deprecated APIs/Features

### 14.1 Removed Java EE and CORBA Modules (JEP 320)

The following modules, which were **deprecated for removal in Java 9**, are now **removed**:

| Removed Module | Description | Replacement |
|---|---|---|
| `java.xml.ws` | JAX-WS (SOAP web services) | Use standalone `jakarta.xml.ws` |
| `java.xml.bind` | JAXB (XML binding) | Use standalone `jakarta.xml.bind` |
| `java.activation` | JAF (JavaBeans Activation Framework) | Use standalone `jakarta.activation` |
| `java.xml.ws.annotation` | Common annotations | Use standalone `jakarta.annotation-api` |
| `java.corba` | CORBA | Use third-party CORBA implementation |
| `java.transaction` | JTA (Java Transaction API) | Use standalone `jakarta.transaction-api` |
| `jdk.xml.ws` | Tools for JAX-WS | N/A |
| `jdk.xml.bind` | Tools for JAXB | N/A |

**Maven Dependency for JAXB (most commonly needed):**

```xml
<dependency>
    <groupId>jakarta.xml.bind</groupId>
    <artifactId>jakarta.xml.bind-api</artifactId>
    <version>2.3.3</version>
</dependency>
<dependency>
    <groupId>org.glassfish.jaxb</groupId>
    <artifactId>jaxb-runtime</artifactId>
    <version>2.3.3</version>
</dependency>
```

### 14.2 Removed `JavaFX` (JEP 320 related)

JavaFX was removed from the JDK and is now available as a separate download at [openjfx.io](https://openjfx.io).

### 14.3 Removed `Applet API` (Deprecated)

The Applet API (`java.applet.Applet`) was **deprecated for removal**. Browser vendors had already dropped support.

### 14.4 Removed `java.se.ee` Aggregator Module

This aggregator module, which included the Java EE modules above, is removed.

### 14.5 Other Removals:

| Removed Item | Details |
|---|---|
| **Thread.destroy()** and **Thread.stop(Throwable)** | Removed (were already no-ops/deprecated) |
| **`com.sun.awt.AWTUtilities`** | Removed |
| **`sun.misc.Unsafe.defineClass()`** | Removed — use `java.lang.invoke.MethodHandles.Lookup.defineClass()` instead |
| **`-XX:+AggressiveOpts`** | JVM flag removed |
| **`pack200` / `unpack200`** | Deprecated for removal (still present, removed in Java 14) |

---

## 15. Unicode 10 Support

Java 11 supports **Unicode 10.0** (upgraded from Unicode 8.0 in Java 10).

### Key Additions in Unicode 10:

- **8,518 new characters** (total: 136,690 characters)
- 4 new scripts: Zanabazar Square, Soyombo, Masaram Gondi, Nüshu
- 56 new emoji characters
- Bitcoin sign ₿ (U+20BF)

```java
// Bitcoin sign
System.out.println('\u20BF'); // ₿

// Check character properties
System.out.println(Character.isLetter('₿'));      // false
System.out.println(Character.getType('\u20BF'));   // 26 (CURRENCY_SYMBOL)
```

---

## 16. TLS 1.3 Support

**JEP 332** — Implements TLS 1.3 (Transport Layer Security), the latest version of the TLS protocol.

### Key Improvements in TLS 1.3:

| Feature | Details |
|---|---|
| **Security** | Removed obsolete crypto algorithms (RC4, DES, 3DES, etc.) |
| **Performance** | 1-RTT (one round-trip) handshake; 0-RTT resumption |
| **Simplicity** | Fewer cipher suites, simpler handshake |
| **Forward Secrecy** | Mandatory (all key exchanges use ephemeral keys) |

```java
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;

SSLContext sslContext = SSLContext.getInstance("TLSv1.3");
sslContext.init(null, null, null);

SSLSocketFactory factory = sslContext.getSocketFactory();
SSLSocket socket = (SSLSocket) factory.createSocket("example.com", 443);

// Restrict to TLS 1.3 only
socket.setEnabledProtocols(new String[] { "TLSv1.3" });

// New TLS 1.3 cipher suites
// TLS_AES_128_GCM_SHA256
// TLS_AES_256_GCM_SHA384
```

**Interview Keywords:** TLS 1.3, JEP 332, 1-RTT handshake, 0-RTT resumption, mandatory forward secrecy, removed obsolete algorithms.

---

## 17. Key Nashorn Deprecation

**JEP 335** — The **Nashorn JavaScript Engine** (`javax.script` integration and `jjs` tool) is **deprecated for removal**.

```java
// This still works in Java 11 but generates deprecation warnings
ScriptEngineManager manager = new ScriptEngineManager();
ScriptEngine engine = manager.getEngineByName("nashorn");
Object result = engine.eval("1 + 2");
System.out.println(result); // 3
// Warning: Nashorn is deprecated
```

**Replacement:** GraalVM's JavaScript engine or other third-party engines.
**Removed in:** Java 15.

---

## 18. Pattern Matching Preparation and Other Minor Changes

### 18.1 `CharSequence.compare()` (static method)

```java
int result = CharSequence.compare("abc", "def");
System.out.println(result); // negative (abc < def)

int result2 = CharSequence.compare("xyz", "xyz");
System.out.println(result2); // 0
```

### 18.2 `Character.toString(int codePoint)`

```java
// New overload — accepts int codePoint instead of just char
String emoji = Character.toString(128512); // 😀
System.out.println(emoji);
```

### 18.3 `Predicate` methods chaining (recap from Java 8 + Java 11)

```java
Predicate<String> nonNull = Objects::nonNull;
Predicate<String> nonEmpty = Predicate.not(String::isEmpty);    // Java 11
Predicate<String> nonBlank = Predicate.not(String::isBlank);    // Java 11

Predicate<String> validString = nonNull.and(nonEmpty).and(nonBlank);

System.out.println(validString.test("Hello")); // true
System.out.println(validString.test(""));      // false
System.out.println(validString.test("   "));   // false
System.out.println(validString.test(null));     // false
```

### 18.4 `TimeUnit.convert(Duration)` — New method

```java
import java.time.Duration;
import java.util.concurrent.TimeUnit;

Duration duration = Duration.ofHours(2);
long minutes = TimeUnit.MINUTES.convert(duration);
System.out.println(minutes); // 120
```

### 18.5 `Path.of()` — Factory Method

```java
import java.nio.file.Path;

// Before Java 11
Path path1 = Paths.get("/home", "user", "file.txt");

// Java 11 — Path.of() (preferred)
Path path2 = Path.of("/home", "user", "file.txt");
Path path3 = Path.of(URI.create("file:///home/user/file.txt"));
```

**Note:** `Paths.get()` now internally delegates to `Path.of()`. `Path.of()` is the preferred API going forward.

### 18.6 `Reader.nullReader()`, `Writer.nullWriter()`, `InputStream.nullInputStream()`, `OutputStream.nullOutputStream()`

Null object pattern for I/O streams — reads return EOF, writes are discarded.

```java
import java.io.*;

// Null Reader — always returns -1 (EOF)
Reader nullReader = Reader.nullReader();
System.out.println(nullReader.read()); // -1

// Null Writer — discards all output
Writer nullWriter = Writer.nullWriter();
nullWriter.write("This is discarded");

// Null InputStream — always returns -1 (EOF)
InputStream nullIn = InputStream.nullInputStream();
System.out.println(nullIn.read()); // -1

// Null OutputStream — discards all bytes
OutputStream nullOut = OutputStream.nullOutputStream();
nullOut.write(42); // silently discarded
```

**Use Cases:** Testing, placeholder streams, discarding output, default parameters.

---

## 19. Complete JEP List for Java 11

| JEP | Title | Category |
|---|---|---|
| **181** | Nest-Based Access Control | Language/JVM |
| **309** | Dynamic Class-File Constants | JVM |
| **315** | Improve Aarch64 Intrinsics | Performance |
| **318** | Epsilon: A No-Op Garbage Collector | GC |
| **320** | Remove the Java EE and CORBA Modules | Removals |
| **321** | HTTP Client (Standard) | Library |
| **323** | Local-Variable Syntax for Lambda Parameters | Language |
| **324** | Key Agreement with Curve25519 and Curve448 | Security |
| **327** | Unicode 10 | Library |
| **328** | Flight Recorder | Diagnostics |
| **329** | ChaCha20 and Poly1305 Cryptographic Algorithms | Security |
| **330** | Launch Single-File Source-Code Programs | Tools |
| **331** | Low-Overhead Heap Profiling | Diagnostics |
| **332** | Transport Layer Security (TLS) 1.3 | Security |
| **333** | ZGC: A Scalable Low-Latency Garbage Collector (Experimental) | GC |
| **335** | Deprecate the Nashorn JavaScript Engine | Deprecation |
| **336** | Deprecate the Pack200 Tools and API | Deprecation |

---

## 20. Top Interview Questions Summary

### Quick-Fire Q&A

**Q1: Is Java 11 an LTS release?**
Yes. It is the first LTS release after Java 8 under the new 6-month release cadence.

**Q2: What is the difference between `strip()` and `trim()`?**
`trim()` removes characters ≤ U+0020 (ASCII). `strip()` uses `Character.isWhitespace()` and handles Unicode whitespace characters. Always prefer `strip()` in Java 11+.

**Q3: Can you use `var` in lambda parameters in Java 11?**
Yes (JEP 323). The main benefit is the ability to add annotations to lambda parameters. All parameters must use `var` if any do — mixing is not allowed.

**Q4: What happened to JAXB in Java 11?**
It was removed (JEP 320). You must add it as an external dependency (e.g., `jakarta.xml.bind`).

**Q5: What is the Epsilon GC?**
A no-op garbage collector (JEP 318) that allocates memory but never reclaims it. Used for performance benchmarking and short-lived applications.

**Q6: What is ZGC?**
An experimental, scalable, low-latency GC (JEP 333) with sub-10ms pause times, supporting heaps up to 16TB.

**Q7: What is the difference between `isBlank()` and `isEmpty()`?**
`isEmpty()` checks if `length() == 0`. `isBlank()` checks if the string is empty OR contains only whitespace.

**Q8: What is Nest-Based Access Control?**
JEP 181. It allows nested classes to access each other's private members directly at the JVM level without synthetic bridge methods. New reflection methods: `getNestHost()`, `getNestMembers()`, `isNestmateOf()`.

**Q9: How do you run a Java file without compiling it first in Java 11?**
Use `java FileName.java` directly. The file is compiled in-memory. This is JEP 330.

**Q10: What is Java Flight Recorder?**
A low-overhead profiling/diagnostics tool (JEP 328) now open-sourced. Designed for always-on production monitoring with < 1% overhead.

**Q11: What is `Predicate.not()`?**
A static method in `java.util.function.Predicate` that returns the negation of a given predicate. It enables clean negation of method references: `Predicate.not(String::isBlank)`.

**Q12: Name all new String methods in Java 11.**
`isBlank()`, `lines()`, `strip()`, `stripLeading()`, `stripTrailing()`, `repeat(int)`.

**Q13: What is the HTTP Client API module name?**
`java.net.http` (standardized in Java 11 from the `jdk.incubator.httpclient` incubator module in Java 9).

**Q14: What was removed vs deprecated in Java 11?**
Removed: Java EE modules (JAXB, JAX-WS, CORBA, JTA, JAF), JavaFX.
Deprecated: Nashorn JavaScript Engine, Pack200 tools.

**Q15: What new security features were added in Java 11?**
TLS 1.3 (JEP 332), ChaCha20/Poly1305 cipher algorithms (JEP 329), Curve25519/Curve448 key agreement (JEP 324).

---

> **Pro Tip for Interviews:** When discussing Java 11 features, always mention the associated **JEP number**. It shows depth of knowledge. The most commonly asked features are: String methods (`isBlank`, `strip`, `lines`, `repeat`), HTTP Client API, `var` in lambdas, running `.java` files directly, and the removals (JAXB/Java EE).
