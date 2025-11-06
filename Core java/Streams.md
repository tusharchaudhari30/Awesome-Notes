# 7. Stream API

Below is a 3-level outline with H1/H2/H3 and numbered sections like 7.1, 7.1.1, 7.1.2, plus clear code examples that highlight differences. Inline code uses `text` and examples use `code`

## 7.1 Paradigm

### 7.1.1 What streams are

Streams are like a conveyor belt where data flows through steps (filter, transform, collect) without manual loops.  
Code describes “what to do” with data, and the library handles looping, laziness, and optimization.

```Java
// Manual loop vs stream
List<String> names = List.of("Ana","Bob","Cal");

// Manual
List<String> upper1 = new ArrayList<>();
for (String n : names) upper1.add(n.toUpperCase());

// Stream
List<String> upper2 = names.stream().map(String::toUpperCase).toList();
```

### 7.1.2 Why streams help

They reduce boilerplate, make pipelines readable, and enable parallelism without thread code.  
They encourage side-effect-free steps, which are easier to reason about and test.

## 7.2 Basics needed

### 7.2.1 Functional interfaces

Common ones: `Predicate` (test), `Function` (transform), `Consumer` (use), `Supplier` (create), `Comparator` (ordering).  
Method references like `Type::method` keep code clean and expressive.

```Java
record Person(String name, int age) {}
var sorted = List.of(new Person("Ana",30), new Person("Bob",20))
    .stream()
    .sorted(Comparator.comparingInt(Person::age))
    .toList();
```

### 7.2.2 Lambdas and references

Use short lambdas for simple logic and method references when they read naturally.  
Combine `Comparator.comparing`, `thenComparing` to layer sort rules.

## 7.3 Pipeline model

### 7.3.1 Three parts

Source → intermediate steps (lazy) → terminal step (executes now).  
Once a terminal runs, the stream is consumed and cannot be reused.

```Java
List<String> out = List.of("a","bb","ccc").stream()
    .filter(s -> s.length() > 1)
    .map(String::toUpperCase)
    .toList(); // terminal executes
```

### 7.3.2 Laziness and single-use

Intermediates don’t run until a terminal is called; then all steps run in one pass.  
A stream is one-shot; create a new stream for another pass.

## 7.4 Characteristics

### 7.4.1 Sequential vs parallel

`sequential()` uses one thread; `parallel()` divides work across cores.  
Parallel can be faster for big data and heavy work, not for small/light tasks.

```Java
long sum = LongStream.rangeClosed(1, 10_000_000).parallel().sum();
```

### 7.4.2 Ordered vs unordered

Ordered streams preserve encounter order; `unordered()` hints order doesn’t matter.  
Dropping order can unlock performance in parallel pipelines.

```Java
List<Integer> anyOrder = List.of(3,1,2).parallelStream()
    .unordered().map(x -> x).toList(); // order not guaranteed
```

## 7.5 Creating streams

### 7.5.1 From collections and arrays

Use `collection.stream()`, `collection.parallelStream()`, `Arrays.stream(array)`.  
Don’t reuse a stream after a terminal operation.

```Java
Stream<Integer> s = Stream.of(1,2,3);
long c1 = s.count();
// s.count(); // IllegalStateException if tried again
```

### 7.5.2 From values and utilities

`Stream.of(...)`, `Stream.empty()`, `Stream.ofNullable(x)` are handy for small/nullable inputs.  
`String.lines()`, `Pattern.splitAsStream`, `Scanner.tokens()` turn text into streams.

```Java
List<String> words = Pattern.compile("\\W+").splitAsStream("a bb ccc").toList();
List<String> lines = "L1\nL2".lines().toList();
```

## 7.6 Infinite and generated

### 7.6.1 generate and iterate

`generate(supplier)` produces endless values; `iterate(seed, step)` walks a sequence.  
Java 9+ `iterate(seed, predicate, step)` stops when the predicate fails.

```Java
Stream<Double> rnd3 = Stream.generate(Math::random).limit(3);
List<Integer> odds = Stream.iterate(1, n -> n < 10, n -> n + 2).toList();
```

### 7.6.2 Truncation helpers

Use `limit`, `takeWhile`, `dropWhile` to control size and avoid infinite loops.  
`takeWhile` stops on first failure; `filter` checks all items.

```Java
var t = Stream.of(2,4,6,1,8).takeWhile(n -> n % 2 == 0).toList(); // [2,4,6]
var f = Stream.of(2,4,6,1,8).filter(n -> n % 2 == 0).toList();    // [2,4,6,8]
```

## 7.7 Numeric streams

### 7.7.1 Int/Long/Double streams

Primitive streams avoid boxing and add numeric operations like `sum`, `average`.  
`range(a,b)` excludes `b`; `rangeClosed(a,b)` includes `b`.

```Java
double avg = Stream.of("a","bb","ccc").mapToInt(String::length).average().orElse(0);
IntStream r = IntStream.rangeClosed(1, 3); // 1,2,3
```

### 7.7.2 Interop object ↔ primitive

Use `mapToInt/mapToLong/mapToDouble` to go primitive; `boxed()` to go back.  
For strings, `codePoints()` counts full Unicode characters correctly.

```Java
int sum = List.of("1","2","3").stream().mapToInt(Integer::parseInt).sum();
long cps = "𝟘𝟙A".codePoints().count(); // correct Unicode-aware count
```

## 7.8 Core intermediates I

### 7.8.1 filter and map

`filter` keeps items that pass a test; `map` transforms each item.  
Use small, pure functions; avoid mutating external state.

```Java
List<Integer> lens = Stream.of("a","bb","ccc").map(String::length).toList();
```

### 7.8.2 flatMap and mapMulti

`flatMap` flattens nested streams; `mapMulti` pushes results directly (fewer temporary streams).  
Use `mapMulti` for performance when generating multiple outputs per input.

```Java
List<String> phrases = List.of("a b","c","d e");

var words1 = phrases.stream()
    .map(p -> p.split("\\s+"))
    .flatMap(Arrays::stream)
    .toList();

var words2 = phrases.stream()
    .<String>mapMulti((p, down) -> { for (var w : p.split("\\s+")) down.accept(w); })
    .toList();
```

## 7.9 Core intermediates II

### 7.9.1 distinct, sorted, peek

`distinct` removes duplicates; `sorted` orders items; `peek` is for debugging taps.  
Avoid mutating data in `peek`; it’s intended for observation.

```Java
List<Integer> cleaned = List.of(3,1,2,2,1).stream().distinct().sorted().toList(); // [1,2,3]
```

### 7.9.2 Slicing and concat

Use `skip`, `limit`, `takeWhile`, `dropWhile` to slice sequences; use `Stream.concat(a,b)` to join two streams.  
`takeWhile/dropWhile` work best on ordered streams.

```Java
var a = Stream.of(1,2,3,0,4,5).takeWhile(n -> n > 0).toList(); // [1,2,3]
var b = Stream.of(1,2,3,0,4,5).dropWhile(n -> n > 0).toList(); // [0,4,5]
```

## 7.10 Mode and ordering

### 7.10.1 sequential/parallel/unordered

Switch mode mid-pipeline with `sequential()` or `parallel()`.  
Use `unordered()` to tell the system that order doesn’t matter downstream.

```Java
long total = IntStream.range(0, 1_000_000).parallel().unordered().map(x -> x+1).sum();
```

### 7.10.2 forEach vs forEachOrdered

`forEach` may ignore order in parallel; `forEachOrdered` preserves order at some cost.  
Prefer `forEachOrdered` when output order is important.

```Java
IntStream.range(1, 6).parallel().forEach(System.out::print);        // any order
IntStream.range(1, 6).parallel().forEachOrdered(System.out::print); // 12345
```

## 7.11 Terminal ops I

### 7.11.1 Counts and extrema

`count()` returns number of items; `min(cmp)`, `max(cmp)` return `Optional` results.  
Use method references and comparators for clarity.

```Java
long cnt = Stream.of("a","bb","ccc").count();
```

### 7.11.2 Finds and matches

`findFirst()` respects order; `findAny()` may be faster in parallel.  
`anyMatch/allMatch/noneMatch` stop as soon as the answer is known.

```Java
boolean hasLong = Stream.of("aa","b","ccc").anyMatch(s -> s.length() >= 3);
```

## 7.12 Terminal ops II

### 7.12.1 forEach guidance

Avoid using `forEach` to mutate shared structures; prefer `map` + `collect`.  
Side effects cause bugs, especially with parallel streams.

```Java
List<Integer> squares = IntStream.rangeClosed(1,5).map(n -> n*n).boxed().toList();
```

### 7.12.2 reduce overview

`reduce` folds a stream into one value: with identity, with optional result, or with a parallel combiner.  
Use the 3-arg form for correct parallel reductions.

```Java
int sum1 = IntStream.rangeClosed(1,5).reduce(0, Integer::sum);
int prodPar = Stream.of(1,2,3,4).parallel()
    .reduce(1, (a,b)->a*b, (x,y)->x*y);
```

## 7.13 Optional with streams

### 7.13.1 Optional basics

`Optional` represents “maybe a value” without `null`.  
Use `orElse`, `orElseGet`, `orElseThrow`, `ifPresent`, and `optional.stream()`.

```Java
Optional<String> maybe = Stream.of("a","bb","ccc")
    .filter(s -> s.length() > 5)
    .findFirst();

String v = maybe.orElse("fallback");
List<String> oneOrZero = maybe.stream().toList();
```

### 7.13.2 orElse vs orElseGet

`orElse` evaluates its value immediately; `orElseGet` calls supplier only if empty.  
Prefer `orElseGet` when the fallback is expensive to compute.

```Java
Supplier<String> costly = () -> { /* expensive */ return "computed"; };
String eager = Optional.of("value").orElse(costly.get()); // calls supplier anyway
String lazy  = Optional.of("value").orElseGet(costly);    // calls only if empty
```

## 7.14 Collecting basics

### 7.14.1 Common collectors

`toList`, `toSet`, `toCollection`, `toArray`, `joining` cover most needs.  
`joining(delim)` is great for CSV-like strings.

```Java
String csv = Stream.of("a","b","c").collect(Collectors.joining(","));
```

### 7.14.2 Summaries

`summarizingInt/Long/Double` returns count, sum, min, max, average at once.  
Avoid multiple passes by using a single summary collector.

```Java
IntSummaryStatistics stats = Stream.of("a","bb","ccc")
    .collect(Collectors.summarizingInt(String::length));
```

## 7.15 Maps via collectors

### 7.15.1 toMap variants

`toMap(key, value)` needs unique keys; provide a merge function to resolve duplicates.  
Choose a map type with the map supplier overload if needed.

```Java
record User(int id, String name) {}
var users = List.of(new User(1,"A"), new User(2,"B"), new User(2,"B2"));

Map<Integer,String> byId = users.stream().collect(
    Collectors.toMap(User::id, User::name, (oldV, newV) -> oldV) // keep first
);
```

### 7.15.2 toConcurrentMap

`toConcurrentMap` builds a concurrent map, useful in parallel pipelines.  
Provide a merge function when keys can collide.

```Java
ConcurrentMap<Integer, Long> freq = Stream.of(1,2,2,3).collect(
    Collectors.toConcurrentMap(x -> x, x -> 1L, Long::sum)
);
```

## 7.16 Grouping and partitioning

### 7.16.1 groupingBy

`groupingBy(classifier)` builds `Map<K, List<T>>`, and can take a downstream collector.  
Use downstreams to count, map, or reduce inside each group.

```Java
Map<Integer, List<String>> byLen = Stream.of("a","bb","c","dd","eee")
    .collect(Collectors.groupingBy(String::length));
```

### 7.16.2 partitioningBy

`partitioningBy(predicate)` splits into `true` and `false` lists.  
It’s a specialized two-bucket grouping.

```Java
Map<Boolean, List<Integer>> parts = IntStream.rangeClosed(1,6).boxed()
    .collect(Collectors.partitioningBy(n -> n % 2 == 0));
```

## 7.17 Downstream collectors

### 7.17.1 mapping, filtering, counting

Downstreams apply extra work per group: `mapping`, `flatMapping`, `filtering`, `counting`.  
Combine them for clean, one-pass group processing.

```Java
Map<Integer, Long> countByLen = Stream.of("a","bb","c","dd","eee")
    .collect(Collectors.groupingBy(String::length, Collectors.counting()));
```

### 7.17.2 min/max, teeing

`maxBy/minBy` find extremes per group; `teeing` merges two collectors’ results.  
`teeing` is great to compute two stats and merge into one object.

```Java
record Stats(long sum, long count) {}
Stats stats = IntStream.rangeClosed(1, 5).boxed()
    .collect(Collectors.teeing(
        Collectors.summingInt(Integer::intValue),
        Collectors.counting(),
        (sum, count) -> new Stats(sum, count)
    ));
double avg = (stats.count == 0) ? 0 : (double) stats.sum / stats.count;
```

## 7.18 Custom collectors

### 7.18.1 When to write one

Write a `Collector<T,A,R>` when built-ins don’t fit or performance needs a custom accumulation.  
Define supplier, accumulator, combiner, finisher, and characteristics.

### 7.18.2 Example sketch

Join strings with a delimiter without creating many temporary strings.  
The combiner merges partial results in parallel.

```Java
class Joiner implements Collector<String, StringBuilder, String> {
    private final String delim;
    Joiner(String d) { this.delim = d; }
    public Supplier<StringBuilder> supplier() { return StringBuilder::new; }
    public BiConsumer<StringBuilder, String> accumulator() {
        return (sb, s) -> { if (!sb.isEmpty()) sb.append(delim); sb.append(s); };
    }
    public BinaryOperator<StringBuilder> combiner() {
        return (a, b) -> { if (!a.isEmpty() && !b.isEmpty()) a.append(delim); return a.append(b); };
    }
    public Function<StringBuilder, String> finisher() { return StringBuilder::toString; }
    public Set<Characteristics> characteristics() { return Set.of(); }
}
String joined = Stream.of("a","b","c").collect(new Joiner("|"));
```

## 7.19 Parallel streams

### 7.19.1 Correctness rules

Operations must be stateless, non-interfering, and associative for reductions.  
Avoid shared mutable state; prefer pure functions.

```Java
int right = Stream.of(1,2,3,4).parallel().reduce(0, Integer::sum); // associative
```

### 7.19.2 When parallel helps

Helps with large data, heavy per-item work, and splittable sources (arrays, ranges, files).  
`unordered()` and avoiding order-sensitive steps improve scaling.

```Java
long fast = IntStream.range(0, 1_000_000).parallel().unordered().map(x -> x+1).sum();
```

## 7.20 Best practices

### 7.20.1 Avoid side effects

Don’t change the source or shared variables from pipeline steps.  
Use `map` + `collect` instead of adding to a list in `forEach`.

```Java
List<Integer> safe = IntStream.rangeClosed(1, 5).map(n -> n*n).boxed().toList();
```

### 7.20.2 Handle infinite and I/O streams

Always truncate infinite streams.  
Close resource-backed streams with try-with-resources.

```Java
try (Stream<String> lines = Files.lines(Path.of("big.txt"))) {
    long count = lines.filter(l -> !l.isBlank()).count();
}
```

## 7.21 Interop and real-world sources

### 7.21.1 Files, readers, and maps

`Files.lines(path)` and `BufferedReader.lines()` stream lines; remember to close.  
Stream map entries via `map.entrySet().stream()`.

```Java
Map<String, Integer> freq = Map.of("a",1,"b",2);
List<String> keysOver1 = freq.entrySet().stream()
    .filter(e -> e.getValue() > 1)
    .map(Map.Entry::getKey)
    .toList();
```

### 7.21.2 Strings and Unicode

`String.lines()` splits into lines; `Pattern.splitAsStream()` tokenizes by regex.  
Use `codePoints()` to process full Unicode characters.

```Java
long cps = "𝟘𝟙A".codePoints().count();
```

## 7.22 Exercises and applications

### 7.22.1 Word frequency

Split, normalize, count, and get top-N words using grouping and sorting.  
This combines tokenization, filtering, grouping, and ordering.

```Java
String text = "To be, or not to be, that is the question.";
Map<String, Long> freq = Pattern.compile("\\W+").splitAsStream(text.toLowerCase())
    .filter(w -> !w.isBlank())
    .collect(Collectors.groupingBy(w -> w, Collectors.counting()));

List<Map.Entry<String, Long>> top = freq.entrySet().stream()
    .sorted(Map.Entry.<String, Long>comparingByValue().reversed())
    .limit(5)
    .toList();
```

### 7.22.2 Numeric map-reduce

Map numbers to derived values and reduce them to totals or products.  
Use primitive streams to avoid boxing and speed up calculations.

```Java
int sumSquares = IntStream.rangeClosed(1, 10).map(n -> n*n).sum();
```

---

# Differences cheat-sheet

## 7.23.1 map vs flatMap vs mapMulti

```Java
Stream<String> s = Stream.of("a b", "c", "d e");

// map: one input → one output (arrays here)
var m1 = s.map(t -> t.split(" ")); // Stream<String[]>

// flatMap: one input → many outputs, flattened
var m2 = Stream.of("a b","c","d e")
    .flatMap(t -> Arrays.stream(t.split(" ")));

// mapMulti: like flatMap but pushes directly (no temp streams)
var m3 = Stream.of("a b","c","d e")
    .<String>mapMulti((t, down) -> { for (var w : t.split(" ")) down.accept(w); });
```

## 7.23.2 takeWhile/dropWhile vs filter

```Java
var t = Stream.of(2,4,6,1,8).takeWhile(n -> n % 2 == 0).toList(); // [2,4,6] stops at first odd
var d = Stream.of(2,4,6,1,8).dropWhile(n -> n % 2 == 0).toList(); // [1,8] starts from first odd
var f = Stream.of(2,4,6,1,8).filter(n -> n % 2 == 0).toList();    // [2,4,6,8] checks all
```

## 7.23.3 findFirst vs findAny (parallel)

```Java
var ff = Stream.of(1,2,3,4).parallel().findFirst(); // first by stream order
var fa = Stream.of(1,2,3,4).parallel().findAny();   // any element (often faster)
```

## 7.23.4 forEach vs forEachOrdered (parallel)

```Java
IntStream.range(1, 6).parallel().forEach(System.out::print);        // any order
IntStream.range(1, 6).parallel().forEachOrdered(System.out::print); // 12345
```

## 7.23.5 reduce variants

```Java
var r1 = Stream.of(1,2,3).reduce(0, Integer::sum);                      // identity + accumulator
var r2 = Stream.of(1,2,3).reduce(Integer::sum).orElse(0);               // Optional result
var r3 = Stream.of(1,2,3).parallel().reduce(1, (a,b)->a*b, (x,y)->x*y); // combiner for parallel
```

## 7.23.6 toMap vs groupingBy vs toConcurrentMap

```Java
List<String> animals = List.of("ant","ape","bat","bear");

// toMap with merge (same first letter)
Map<Character, Integer> firstCount = animals.stream().collect(
    Collectors.toMap(s -> s.charAt(0), s -> 1, Integer::sum)
);

// groupingBy to lists per key
Map<Character, List<String>> grouped = animals.stream().collect(
    Collectors.groupingBy(s -> s.charAt(0))
);

// concurrent map (parallel-friendly counting)
ConcurrentMap<Character, Long> freq = animals.parallelStream().collect(
    Collectors.toConcurrentMap(s -> s.charAt(0), s -> 1L, Long::sum)
);
```

## 7.23.7 Optional: orElse vs orElseGet

```Java
Supplier<String> costly = () -> { /* expensive work */ return "computed"; };
String eager = Optional.of("value").orElse(costly.get()); // calls supplier regardless
String lazy  = Optional.of("value").orElseGet(costly);    // calls only if empty
```

## 7.23.8 chars vs codePoints

```Java
String txt = "𝟘𝟙A";
long ok    = txt.codePoints().count(); // correct Unicode-aware count
long risky = txt.chars().count();      // may split surrogate pairs
```

## 7.23.9 Object vs primitive streams

```Java
double avg = Stream.of("a","bb","ccc").mapToInt(String::length).average().orElse(0);
List<Integer> boxed = IntStream.of(1,2,3).boxed().toList();
```

## 7.23.10 unordered hint helps parallel speed

```Java
long total = IntStream.range(0, 1_000_000).parallel().unordered().map(x -> x+1).sum();
```

## 7.23.11 Side effects: bad vs good

```Java
List<Integer> data = IntStream.rangeClosed(1, 5).boxed().toList();

// Bad: shared mutable state (race condition)
List<Integer> out = new ArrayList<>();
data.parallelStream().forEach(n -> out.add(n*n));

// Good: pure mapping + collect
List<Integer> safe = data.parallelStream().map(n -> n*n).toList();
```

## 7.23.12 Resource-backed streams

```Java
try (Stream<String> lines = Files.lines(Path.of("big.txt"))) {
    long count = lines.filter(l -> !l.isBlank()).count();
}
```
