# 8. Functional API

Three-level outline with H1/H2/H3 headings, numbered like 8.1, 8.1.1, 8.1.2, using layman terms and lots of small code examples highlighting differences. Inline code uses `text`; examples use `java`

## 8.1 Big picture

### 8.1.1 What “Functional API” means

In Java, “Functional API” refers to language and library features that treat behavior (functions) as values: lambdas, method references, and standard functional interfaces like `Predicate`, `Function`, and `Supplier`.  
These pieces enable declarative styles in Streams, concurrency, and everyday code without writing verbose classes.

```java
// Behavior as data: pass a function into a method
void repeat(int n, Runnable task) { for (int i = 0; i < n; i++) task.run(); }

repeat(3, () -> System.out.println("Hi")); // prints 3 times
```

### 8.1.2 Why it helps

Code becomes shorter, clearer, and more reusable by passing “what to do” as parameters.  
The JVM can optimize functional pipelines, and libraries can compose work in powerful ways.

## 8.2 Functional interfaces

### 8.2.1 Core single-arg types

- `Function<T,R>`: takes `T`, returns `R`.
- `Predicate<T>`: takes `T`, returns boolean.
- `Consumer<T>`: takes `T`, returns nothing.
- `Supplier<T>`: takes nothing, returns `T`.

```java
Function<String, Integer> len = String::length;
Predicate<String> longWord = s -> s.length() > 5;
Consumer<String> printer = System.out::println;
Supplier<Double> rnd = Math::random;
```

### 8.2.2 Operators and binaries

- `UnaryOperator<T>`: `T -> T` (like `Function<T,T>`).
- `BinaryOperator<T>`: `(T,T) -> T`.
- `BiFunction<T,U,R>`, `BiPredicate<T,U>`, `BiConsumer<T,U>` for two inputs.

```java
UnaryOperator<Integer> inc = x -> x + 1;
BinaryOperator<Integer> add = Integer::sum;
BiPredicate<String,Integer> longAtLeast = (s, n) -> s.length() >= n;
```

## 8.3 Lambda expressions

### 8.3.1 Syntax in simple words

- Single param: `x -> x + 1`.
- Multiple params: `(x, y) -> x + y`.
- Block with statements: `x -> { System.out.println(x); return x + 1; }`.
- Types often inferred, but can be explicit: `(int x) -> x + 1`.

```java
Comparator<String> byLen = (a, b) -> Integer.compare(a.length(), b.length());
```

### 8.3.2 Effectively final and scope

Lambdas can read local variables only if they are effectively final (not changed after assignment).  
Use fields or holders if mutation is absolutely needed, but prefer pure functions.

```java
int base = 10;
// base++; // would make it not effectively final
Function<Integer,Integer> plusBase = x -> x + base;
```

## 8.4 Method references

### 8.4.1 Four common forms

- Static method: `Type::staticMethod` (e.g., `Math::max`).
- Instance method on any object of type: `Type::instanceMethod` (e.g., `String::isBlank`).
- Instance method on a specific object: `obj::instanceMethod` (e.g., `list::add`).
- Constructor: `ClassName::new` (e.g., `ArrayList::new`).

```java
Function<String, Integer> len = String::length;
Supplier<List<String>> factory = ArrayList::new;
BiFunction<Integer,Integer,Integer> mx = Math::max;
```

### 8.4.2 When to pick reference vs lambda

Use method references when they read naturally and match the target interface.  
Use lambdas when custom logic is small but not a direct method call.

```java
// Both are fine; pick readability
Predicate<String> p1 = String::isEmpty;
Predicate<String> p2 = s -> s.isEmpty();
```

## 8.5 Built-in functional helpers

### 8.5.1 Function composition

Functions can chain: `f.andThen(g)` runs `f` then `g`, `f.compose(g)` runs `g` then `f`.  
Use `Function.identity()` to represent “do nothing” function.

```java
Function<String, Integer> len = String::length;
Function<Integer, Boolean> isEven = n -> n % 2 == 0;

Function<String, Boolean> evenLen = len.andThen(isEven);
boolean ok = evenLen.apply("four");
```

### 8.5.2 Predicate helpers

`and`, `or`, `negate`, and `Predicate.isEqual(x)` help build readable tests.  
Combine small tests rather than writing one large complex predicate.

```java
Predicate<String> nonEmpty = s -> !s.isEmpty();
Predicate<String> longish = s -> s.length() >= 5;

Predicate<String> good = nonEmpty.and(longish).or(String::isBlank).negate();
```

## 8.6 Primitive functional variants

### 8.6.1 Avoid boxing overhead

Use `IntPredicate`, `IntFunction<R>`, `IntUnaryOperator`, `IntConsumer`, etc., for primitive `int`, and analogs for `long` and `double`.  
These avoid boxing and can be much faster in loops and hot paths.

```java
IntUnaryOperator inc = x -> x + 1;
IntPredicate even = x -> (x & 1) == 0;
IntSupplier dice = () -> 1 + (int)(Math.random() * 6);
```

### 8.6.2 To/From object types

Bridge with mappers like `IntFunction<String>` or `ToIntFunction<T>`.  
Useful when mixing object streams and primitive processing.

```java
ToIntFunction<String> toLen = String::length;
IntFunction<String> label = n -> "len=" + n;
```

## 8.7 Comparators and orderings

### 8.7.1 Composing comparators

`Comparator.comparing(keyExtractor)` with `thenComparing` builds layered sorts.  
Use `comparingInt/Long/Double` for primitives.

```java
record Person(String name, int age) {}
Comparator<Person> cmp = Comparator
    .comparingInt(Person::age)
    .thenComparing(Person::name);
```

### 8.7.2 Natural order vs custom

Natural order uses `Comparable` of objects (like `String`).  
Custom order uses comparator; `reversed()` flips the result.

```java
Comparator<String> byLenDesc = Comparator.comparingInt(String::length).reversed();
```

## 8.8 Optional as functional value

### 8.8.1 Avoiding null checks

`Optional<T>` wraps a value that may be absent and exposes functional-style helpers.  
Prefer `map`, `flatMap`, `filter`, `ifPresent`, `orElseGet` to reduce `if (x!=null)` code.

```java
Optional<String> maybe = Optional.of("hello");
int n = maybe.map(String::length).orElse(0);
```

### 8.8.2 orElse vs orElseGet

`orElse(v)` always evaluates `v`; `orElseGet(supplier)` calls the supplier only if empty.  
Use `orElseGet` when the fallback is expensive.

```java
Supplier<String> costly = () -> { /* heavy */ return "computed"; };
String v1 = Optional.of("x").orElse(costly.get()); // calls anyway
String v2 = Optional.of("x").orElseGet(costly);    // lazy
```

## 8.9 Streams meet functional interfaces

### 8.9.1 Where they fit

Streams use these interfaces everywhere: `map(Function)`, `filter(Predicate)`, `forEach(Consumer)`, `collect(Supplier, BiConsumer, BiConsumer)`.  
Knowing the signatures helps write cleaner lambdas or references.

```java
List<String> out = Stream.of("a","bbb","cc")
    .filter(s -> s.length() >= 2)       // Predicate
    .map(String::toUpperCase)           // Function
    .peek(System.out::println)          // Consumer
    .toList();
```

### 8.9.2 map vs flatMap vs mapMulti (recap)

`map` = one input → one output; `flatMap` = one → many via nested streams; `mapMulti` = push many directly.  
Pick the simplest that matches the shape of data.

```java
var words = Stream.of("a b", "c", "d e")
    .flatMap(s -> Arrays.stream(s.split(" ")))
    .toList();
```

## 8.10 Higher-order utilities

### 8.10.1 Currying/partial application (DIY)

Java doesn’t have built-in currying, but can return lambdas that capture parameters.  
This builds parameterized functions in steps.

```java
Function<Integer, Function<Integer, Integer>> add = a -> (b -> a + b);
int five = add.apply(2).apply(3);
```

### 8.10.2 Memoization (DIY)

Wrap a `Function<T,R>` to cache results for the same input.  
Good for expensive, pure functions.

```java
static <T,R> Function<T,R> memo(Function<T,R> f) {
    Map<T,R> cache = new ConcurrentHashMap<>();
    return x -> cache.computeIfAbsent(x, f);
}
```

## 8.11 Exceptions with lambdas

### 8.11.1 Checked exceptions

Functional interfaces don’t declare checked exceptions, so wrapping is needed.  
Write small adapters that catch and rethrow as unchecked or use helper methods.

```java
@FunctionalInterface interface ThrowingIO<T,R> { R apply(T t) throws IOException; }

static <T,R> Function<T,R> uncheck(ThrowingIO<T,R> f) {
    return x -> {
        try { return f.apply(x); } catch (IOException e) { throw new UncheckedIOException(e); }
    };
}
```

### 8.11.2 Practical pattern

Use `uncheck(...)` to adapt file operations in streams.  
Keep exception handling at the pipeline edge rather than in the middle of lambdas.

```java
List<String> lines = Files.list(Path.of(".")).map(Path::toString).toList(); // simple
```

## 8.12 Concurrency-friendly functional use

### 8.12.1 Stateless, non-interfering

Lambdas should not mutate shared state when used in parallel streams or thread pools.  
Prefer pure functions; if state is needed, confine it to thread-local or use concurrent structures.

```java
// Good: pure map
long sum = LongStream.range(1, 1_000_000).parallel().map(x -> x + 1).sum();
```

### 8.12.2 Executors and callables

`ExecutorService` methods use `Runnable` and `Callable<T>` (functional interfaces).  
Submit lambdas instead of implementing classes.

```java
ExecutorService pool = Executors.newFixedThreadPool(4);
Future<Integer> f = pool.submit(() -> 42); // Callable<Integer>
pool.execute(() -> System.out.println("Hi")); // Runnable
pool.shutdown();
```

## 8.13 Collections helpers using functions

### 8.13.1 Map.compute and friends

`compute`, `computeIfAbsent`, `merge` accept functional arguments to update maps declaratively.  
This avoids manual `containsKey` dances.

```java
Map<String, Integer> freq = new HashMap<>();
List.of("a","b","a").forEach(w -> freq.merge(w, 1, Integer::sum));
```

### 8.13.2 Remove, replace, and replaceAll

`removeIf(Predicate)` cleans collections; `replaceAll(UnaryOperator)` transforms in-place.  
Be careful: these mutate the collection directly.

```java
List<String> items = new ArrayList<>(List.of("a","","bb"));
items.removeIf(String::isEmpty);
items.replaceAll(String::toUpperCase); // ["A","BB"]
```

## 8.14 Functional patterns in practice

### 8.14.1 Strategy via lambdas

Pick behavior at runtime by passing different lambdas instead of writing many subclasses.  
Great for validation, filtering, pricing rules, etc.

```java
Function<Double, Double> noTax = x -> x;
Function<Double, Double> gst = x -> x * 1.18;

double finalPrice = gst.apply(100.0);
```

### 8.14.2 Pipelines outside streams

Even without `Stream`, chain `Function.andThen` and `compose` to build mini-pipelines.  
This keeps transformations testable and modular.

```java
Function<String, String> trim = String::trim;
Function<String, String> lower = String::toLowerCase;
Function<String, String> sanitize = trim.andThen(lower);
```

## 8.15 Testing and readability

### 8.15.1 Name small functions

Extract lambdas to well-named variables or methods for clarity, then pass them.  
Shorter lambdas improve readability; long ones belong in methods.

```java
Predicate<String> isEmail = s -> s.contains("@") && s.contains(".");
```

### 8.15.2 Immutability helps

Prefer immutable data flowing through functions; it avoids hidden side effects.  
This style makes code easier to test and reason about.

```java
List<String> out = List.copyOf(List.of("a","b","c"));
```

## 8.16 Differences quick guide

### 8.16.1 Function vs UnaryOperator vs BiFunction

```java
Function<String, Integer> f = String::length;               // T -> R
UnaryOperator<String> u = s -> s.trim();                    // T -> T
BiFunction<String, Integer, String> b = (s, n) -> s.repeat(n); // (T,U) -> R
```

### 8.16.2 Predicate combos vs single complex test

```java
Predicate<String> nonEmpty = s -> !s.isEmpty();
Predicate<String> longish = s -> s.length() >= 5;
Predicate<String> good = nonEmpty.and(longish); // clearer than one big expression
```

### 8.16.3 Method reference vs lambda

```java
Predicate<String> p1 = String::isBlank;     // concise and clear
Predicate<String> p2 = s -> s.isBlank();    // equivalent; use whichever reads better
```

### 8.16.4 Optional map/flatMap vs if-else

```java
Optional<String> env = Optional.ofNullable(System.getenv("HOME"));
int len = env.map(String::length).orElse(0); // avoids explicit if-else
```

### 8.16.5 Primitive vs object function types

```java
IntSupplier dice = () -> 1 + (int)(Math.random() * 6); // no boxing
Supplier<Integer> slowDice = () -> 1 + (int)(Math.random() * 6); // boxing
```

## 8.17 Mini reference (one-liners)

### 8.17.1 Interfaces and factories

- `Function<T,R>`, `UnaryOperator<T>`, `BiFunction<T,U,R>`.
- `Predicate<T>`, `BiPredicate<T,U>`.
- `Consumer<T>`, `BiConsumer<T,U>`.
- `Supplier<T>`.
- Primitive variants: `IntFunction`, `IntPredicate`, `IntUnaryOperator`, `IntSupplier`, etc.
- Creators: `Function.identity()`, `Predicate.isEqual(x)`.

### 8.17.2 Common helpers and combos

- `Function.andThen`, `Function.compose`.
- `Predicate.and`, `Predicate.or`, `Predicate.negate`.
- `Comparator.comparing`, `thenComparing`, `reversed`.
- `Optional.map`, `flatMap`, `filter`, `orElseGet`, `ifPresent`.

---

# 8.18 Practice snippets

## 8.18.1 Validate, transform, and act

```java
Predicate<String> notBlank = s -> s != null && !s.isBlank();
Function<String, String> norm = s -> s.trim().toLowerCase();
Consumer<String> save = s -> System.out.println("Saving: " + s);

Stream.of("  HELLO  ", " ", null, "World")
    .filter(Objects::nonNull)
    .filter(notBlank)
    .map(norm)
    .forEach(save);
```

## 8.18.2 Compose text processors

```java
Function<String, String> stripTags = s -> s.replaceAll("<[^>]+>", "");
Function<String, String> compressWs = s -> s.replaceAll("\\s+", " ").trim();
Function<String, String> pipeline = stripTags.andThen(compressWs);

String cleaned = pipeline.apply("  <b>Hello</b>   world  ");
```

## 8.18.3 Map updates with functions

```java
Map<String, Integer> freq = new HashMap<>();
List.of("a","b","a","c","b","a").forEach(w -> freq.merge(w, 1, Integer::sum));
```

## 8.18.4 Parallel-safe functional style

```java
long count = LongStream.range(0, 5_000_000)
    .parallel()
    .map(x -> x * 2)
    .filter(x -> x % 3 == 0)
    .count();
```

## 8.18.5 Optional glue code

```java
Optional<String> maybeUser = Optional.of("alice");
String greeting = maybeUser
    .filter(u -> !u.isBlank())
    .map(String::toUpperCase)
    .map(u -> "Hello, " + u)
    .orElse("Hello, guest");
```
