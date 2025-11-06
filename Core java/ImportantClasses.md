Understood! Here is the **fully structured, interview-focused note sheet** with H1/H2/H3 headers, proper numbering (1.1, 1.1.1, etc.), and clearly separated sections for description, key methods, and examples, as you requested.

# 1. Functional Interfaces

## 1.1 Function<T, R>

### 1.1.1 Description

A converter: takes one value (of type T) and gives back another (of type R). Useful for mapping, transforming data, or chaining steps in processing.

### 1.1.2 Key Methods

- `R apply(T t)`: execute the conversion.
- `andThen(Function after)`: chain another conversion after this one.
- `compose(Function before)`: run a pre-step before this conversion.
- `static identity()`: returns the input as output.

### 1.1.3 Example

```java
Function<String, Integer> length = String::length;
Function<Integer, String> toLabel = n -> "len=" + n;
String out = length.andThen(toLabel).apply("hello"); // "len=5"
```

## 1.2 Predicate<T>

### 1.2.1 Description

A true/false checker. Accepts one value and returns a boolean. Ideal for filtering data or checking rules.

### 1.2.2 Key Methods

- `boolean test(T t)`: run the check.
- `and(Predicate)`, `or(Predicate)`, `negate()`: combine and modify checks.
- `static isEqual(Object)`: shortcut for equality check.

### 1.2.3 Example

```java
Predicate<String> nonBlank = s -> s != null && !s.isBlank();
Predicate<String> longEnough = s -> s.length() >= 3;
boolean ok = nonBlank.and(longEnough).test("abc"); // true
```

## 1.3 Consumer<T>

### 1.3.1 Description

A value consumer: takes one input, performs an action, doesn’t return anything. Use for output, logging, or processing.

### 1.3.2 Key Methods

- `void accept(T t)`: do the action.
- `andThen(Consumer)`: chain another action.

### 1.3.3 Example

```java
Consumer<String> log = System.out::println;
Consumer<String> audit = s -> saveToAudit(s);
log.andThen(audit).accept("USER_LOGIN");
```

## 1.4 Supplier<T>

### 1.4.1 Description

Value generator: provides a value when called, with no arguments. Use for factories, lazy evaluation, or getting random/default values.

### 1.4.2 Key Methods

- `T get()`: fetch or compute the value.

### 1.4.3 Example

```java
Supplier<Double> random = Math::random;
double r = random.get();
```

## 1.5 Optional<T>

### 1.5.1 Description

A safe wrapper: represents a value that might be present or missing (null). Forces you to think about missing values.

### 1.5.2 Key Methods

- `of(value)`, `ofNullable(value)`, `empty()`: creation.
- `isPresent()`, `isEmpty()`, `ifPresent()`: check/use if present.
- `orElse(val)`, `orElseGet(supplier)`, `orElseThrow()`: fallback handling.
- `map(f)`, `flatMap(f)`, `filter(pred)`: safe transformations.

### 1.5.3 Example

```java
String name = Optional.ofNullable(user.getNickname())
    .filter(s -> !s.isBlank())
    .orElseGet(user::getUsername);
```

## 1.6 Comparator<T>

### 1.6.1 Description

A sorting recipe: defines how to compare and order objects by one or more fields. Used in sorting, min/max.

### 1.6.2 Key Methods

- `comparing(keyExtractor)`: build a comparator on a field.
- `thenComparing(...)`: tie-breaker ordering.
- `reversed()`: reverse the order.
- `nullsFirst()/nullsLast()`: handle null values.

### 1.6.3 Example

```java
Comparator<Employee> byDeptThenName =
    Comparator.comparing(Employee::getDepartment, Comparator.nullsLast(String::compareTo))
              .thenComparing(Employee::getName);
```

# 2. Streams

## 2.1 Stream<T>

### 2.1.1 Description

A flow or pipeline of data elements, supporting a chain of processing steps like filtering and mapping. Executes only when a terminal operation is called.

### 2.1.2 Key Methods

- Intermediate: `filter()`, `map()`, `flatMap()`, `distinct()`, `sorted()`, `peek()`, `limit()`, `skip()`
- Terminal: `collect()`, `forEach()`, `reduce()`, `count()`, `toArray()`, `min()`, `max()`, `anyMatch()`, `findFirst()`

### 2.1.3 Example

```java
List<String> top3 = people.stream()
  .filter(p -> p.getAge() > 18)
  .sorted(Comparator.comparing(Person::getScore).reversed())
  .limit(3)
  .map(Person::getName)
  .toList();
```

## 2.2 IntStream

### 2.2.1 Description

A Stream optimized for processing `int` primitives, offering special numeric methods and avoiding unnecessary boxing.

### 2.2.2 Key Methods

- `range(a,b)`, `rangeClosed(a,b)`: number sequences.
- `sum()`, `average()`, `min()`, `max()`, `sumaryStatistics()`
- Usual stream ops: `map`, `filter`, etc.

### 2.2.3 Example

```java
int sumSquares = IntStream.rangeClosed(1, 100)
    .map(x -> x * x)
    .sum();
```

## 2.3 Collectors

### 2.3.1 Description

Utility class for building up collections, aggregations (counting, grouping, joining), and other downstream results from streams.

### 2.3.2 Key Methods

- `toList()`, `toSet()`, `joining()`, `counting()`
- `groupingBy(classifier[, downstream])`, `partitioningBy(predicate[, downstream])`
- `mapping(mapper, downstream)`, `collectingAndThen(downstream, finisher)`
- `toMap(keyMapper, valueMapper[, mergeFn])`

### 2.3.3 Example

```java
Map<String, Long> countByDept = employees.stream()
  .collect(Collectors.groupingBy(Employee::getDepartment, Collectors.counting()));
```

## 2.4 Collector

### 2.4.1 Description

Low-level contract for writing custom collect() strategies: tell Java how to build, add, combine and finish a reduction result.

### 2.4.2 Key Methods

- Supplier, Accumulator, Combiner, Finisher, Characteristics (as passed to Collector.of())

### 2.4.3 Example

```java
Collector<String, StringBuilder, String> upperJoiner = Collector.of(
  StringBuilder::new,
  (sb, s) -> { if (sb.length()>0) sb.append(';'); sb.append(s.toUpperCase()); },
  (a, b) -> { if (a.length()>0 && b.length()>0) a.append(';'); return a.append(b); },
  StringBuilder::toString
);
String joined = Stream.of("a","b").collect(upperJoiner); // "A;B"
```

## 2.5 Optional (with Streams)

### 2.5.1 Description

Used as the result of finding or reducing. Represents “maybe there’s a value”.

### 2.5.2 Key Methods

- `isPresent()`, `ifPresent()`, `orElse()`, `orElseGet()`

### 2.5.3 Example

```java
Optional<Person> firstAdult = people.stream()
  .filter(p -> p.getAge() >= 18)
  .findFirst();
String name = firstAdult.map(Person::getName).orElse("none");
```

## 2.6 Comparator (with Streams)

### 2.6.1 Description

Defines sorting for Stream.sorted(), min(), max().

### 2.6.2 Key Methods

- `comparing()`, `thenComparing()`, `reversed()`

### 2.6.3 Example

```java
List<Person> sorted = people.stream()
  .sorted(Comparator.comparing(Person::getLastName).thenComparing(Person::getFirstName))
  .toList();
```

# 3. Collections

## 3.1 List<E>

### 3.1.1 Description

Ordered, indexable collection that allows duplicates. Think “array with benefits.”

### 3.1.2 Key Methods

- `add(E)`, `add(int,E)`, `get(int)`, `set(int,E)`
- `remove(int|Object)`, `subList(a,b)`, `indexOf(x)`, `listIterator()`

### 3.1.3 Example

```java
List<String> names = new ArrayList<>();
names.add("A"); names.add("B");
names.set(1, "C"); // [A, C]
```

## 3.2 Set<E>

### 3.2.1 Description

Unordered (or ordered) group of unique elements. No duplicates allowed.

### 3.2.2 Key Methods

- `add(E)`, `contains(E)`, `remove(E)`
- `addAll(Collection)`, `containsAll(Collection)`

### 3.2.3 Example

```java
Set<Integer> uniq = new LinkedHashSet<>(List.of(1,2,2,3)); // [1,2,3]
```

## 3.3 Map<K,V>

### 3.3.1 Description

A collection of key–value pairs, where each key is unique. Used as a dictionary or lookup table.

### 3.3.2 Key Methods

- `put(K,V)`, `get(K)`, `getOrDefault(K,def)`, `remove(K)`
- `putIfAbsent()`, `computeIfAbsent()`, `merge()`, `keySet()`, `values()`, `entrySet()`

### 3.3.3 Example

```java
Map<String,Integer> freq = new HashMap<>();
for (String w : words) freq.merge(w, 1, Integer::sum);
```

## 3.4 Queue<E>

### 3.4.1 Description

First-in, first-out (FIFO) structure. Useful for lining up tasks or data for processing.

### 3.4.2 Key Methods

- `offer(E)`, `poll()`, `peek()`
- `add(E)`, `remove()`, `element()` // these throw if broken

### 3.4.3 Example

```java
Queue<String> q = new ArrayDeque<>();
q.offer("a"); q.offer("b");
String head = q.poll(); // "a"
```

## 3.5 Deque<E>

### 3.5.1 Description

A double-ended queue: supports adding/removing from both ends. Useful as both a stack and a queue.

### 3.5.2 Key Methods

- `addFirst/Last()`, `offerFirst/Last()`, `pollFirst/Last()`, `peekFirst/Last()`, `push()`, `pop()`

### 3.5.3 Example

```java
Deque<Integer> d = new ArrayDeque<>();
d.push(1); d.push(2);
int top = d.pop(); // 2
```

## 3.6 ArrayList

### 3.6.1 Description

Array-backed, growable list. Fast random access and appends, but slower inserts/removals in the middle.

### 3.6.2 Key Methods

- `ensureCapacity()`, `trimToSize()`
- All List methods.

### 3.6.3 Example

```java
ArrayList<Integer> list = new ArrayList<>();
list.add(1); list.add(2);
list.add(1, 9); // insert in middle
```

## 3.7 HashSet

### 3.7.1 Description

A fast, unordered set built atop a HashMap. No duplicates, O(1) expected add/contains/remove.

### 3.7.2 Key Methods

- `add(E)`, `contains(E)`, `remove(E)`, `addAll()`

### 3.7.3 Example

```java
Set<String> tags = new HashSet<>();
tags.add("java"); tags.add("java"); // duplicate ignored
```

## 3.8 HashMap

### 3.8.1 Description

A fast, unordered map backed by hash tables. Good for fast key-based lookup and updates.

### 3.8.2 Key Methods

- All Map core methods.
- Java 8+ methods: `computeIfAbsent()`, `merge()`, bucket treeification.

### 3.8.3 Example

```java
Map<String, Integer> scores = new HashMap<>();
scores.put("Ann", 90);
scores.merge("Ann", 5, Integer::sum); // 95
```

## 3.9 Collections (utility class)

### 3.9.1 Description

Helper class with static methods for manipulating, sorting, and wrapping collections.

### 3.9.2 Key Methods

- `sort()`, `reverse()`, `shuffle()`, `min()/max()`, `unmodifiableList()`, `synchronizedList()`

### 3.9.3 Example

```java
List<Integer> list = new ArrayList<>(List.of(3,1,2));
Collections.sort(list); // [1,2,3]
```

## 3.10 Arrays (utility class)

### 3.10.1 Description

Helper class for all array needs: sorting, copying, filling, searching, and converting arrays.

### 3.10.2 Key Methods

- `sort()`, `parallelSort()`, `binarySearch()`, `asList()`, `copyOf()`, `fill()`

### 3.10.3 Example

```java
int[] a = {3,1,2};
Arrays.parallelSort(a);
List<Integer> view = Arrays.asList(1,2,3); // fixed-size view
```

## 3.11 Concurrent Collections

### 3.11.1 Description

Thread-safe collections designed for high performance in concurrent applications.

### 3.11.2 Key Types and Methods

- `ConcurrentHashMap`: `putIfAbsent()`, `computeIfAbsent()`, `merge()`
- `CopyOnWriteArrayList`: super-fast reads, slow writes.
- `BlockingQueue` variants: thread-safe queues for producer-consumer
- `ConcurrentSkipListMap/Set`: lock-free, sorted concurrent collections

### 3.11.3 Example

```java
ConcurrentMap<String,Integer> cm = new ConcurrentHashMap<>();
cm.merge("k", 1, Integer::sum);
BlockingQueue<Task> bq = new LinkedBlockingQueue<>();
```

# 4. Concurrency

## 4.1 Thread

### 4.1.1 Description

A worker that runs code in parallel to the main program. Usually managed by thread pools instead of direct use.

### 4.1.2 Key Methods

- `start()`, `run()`, `join()`, `sleep()`, `interrupt()`, `isInterrupted()`

### 4.1.3 Example

```java
Thread t = new Thread(() -> {
  while (!Thread.currentThread().isInterrupted()) doWorkStep();
});
t.start();
t.join();
```

## 4.2 Runnable

### 4.2.1 Description

A basic unit of work with no result. Used for simple background jobs.

### 4.2.2 Key Methods

- `run()`

### 4.2.3 Example

```java
Runnable job = () -> System.out.println("Hello");
```

## 4.3 Callable<V>

### 4.3.1 Description

A task that produces a value or throws an exception. Used when background work returns data.

### 4.3.2 Key Methods

- `call()`: returns the computed value.

### 4.3.3 Example

```java
Callable<Integer> task = () -> 40 + 2;
```

## 4.4 ExecutorService

### 4.4.1 Description

A thread pool manager: schedules and runs submitted tasks efficiently on multiple threads.

### 4.4.2 Key Methods

- `submit(Runnable/Callable)`, `invokeAll()`, `invokeAny()`
- `shutdown()`, `shutdownNow()`, `awaitTermination()`

### 4.4.3 Example

```java
ExecutorService pool = Executors.newFixedThreadPool(4);
Future<Integer> f = pool.submit(() -> compute());
try { Integer v = f.get(); } finally { pool.shutdown(); }
```

## 4.5 Future<V>

### 4.5.1 Description

A handle representing a result that may not be ready yet; supports blocking waits, cancellation, and status checks.

### 4.5.2 Key Methods

- `get()`, `get(timeout, unit)`
- `isDone()`, `isCancelled()`, `cancel()`

### 4.5.3 Example

```java
Future<String> f = pool.submit(() -> fetch());
String data = f.get(1, TimeUnit.SECONDS);
```

## 4.6 CompletableFuture<T>

### 4.6.1 Description

A Future with extended features: allows non-blocking chaining, combining, and exception handling for asynchronous tasks.

### 4.6.2 Key Methods

- `supplyAsync()`, `runAsync()`
- `thenApply()`, `thenAccept()`, `thenRun()`, `thenCompose()`, `thenCombine()`
- `allOf()`, `anyOf()`
- `exceptionally()`, `handle()`, `whenComplete()`
- `orTimeout()`, `completeOnTimeout()`

### 4.6.3 Example

```java
CompletableFuture<Integer> price = CompletableFuture.supplyAsync(() -> fetchPrice());
CompletableFuture<Integer> tax = CompletableFuture.supplyAsync(() -> fetchTax());
int total = price.thenCombine(tax, Integer::sum)
                 .exceptionally(ex -> 0)
                 .join();
```

## 4.7 Locks

### 4.7.1 Description

Explicit tools for more advanced thread safety and concurrency control than `synchronized`.

### 4.7.2 Key Types/Methods

- `ReentrantLock`: `lock()`, `unlock()`, `tryLock()`, `lockInterruptibly()`
- `ReadWriteLock`: `readLock()`, `writeLock()`
- `StampedLock`: `optimisticRead()`, `readLock()`, `writeLock()`

### 4.7.3 Example

```java
Lock lock = new ReentrantLock();
if (lock.tryLock()) {
  try { /* critical section */ } finally { lock.unlock(); }
}
```

## 4.8 Latches, Barriers, Semaphores

### 4.8.1 Description

Tools for coordinating thread progress and limiting parallelism.

### 4.8.2 Key Types/Methods

- CountDownLatch: `await()`, `countDown()`
- CyclicBarrier: `await()`
- Semaphore: `acquire()`, `release()`

### 4.8.3 Example

```java
CountDownLatch latch = new CountDownLatch(3);
for (int i=0;i<3;i++) new Thread(() -> { stage(); latch.countDown(); }).start();
latch.await();
```

## 4.9 Atomics

### 4.9.1 Description

Primitives for safe, lock-free updates to counters and references, ideal for high-concurrency counts and updates.

### 4.9.2 Key Types/Methods

- AtomicInteger/Long/Boolean/Reference: `get()`, `set()`, `compareAndSet()`, `getAndIncrement()`
- LongAdder/LongAccumulator: advanced counters for heavy concurrency

### 4.9.3 Example

```java
AtomicInteger ai = new AtomicInteger();
ai.incrementAndGet();
```

---

Let me know if you want any section expanded, more classes added, or deeper explanations for specific interview hooks and edge cases!
