### Core Java Concepts

### JVM, JRE, JDK

- **JVM (Java Virtual Machine)**: Executes Java bytecode.
- **JRE (Java Runtime Environment)**: Provides libraries and JVM for running Java applications.
- **JDK (Java Development Kit)**: Includes JRE and development tools like compilers and debuggers.

### Data Types

- **Primitive Types**: byte, short, int, long, float, double, char, boolean.
- **Non-Primitive Types**: Classes, Interfaces, Arrays.

### Control Structures

- **if-else**: Conditional statements.
- **switch**: Multi-way branch statement.
- **for, while, do-while**: Looping constructs.

```java
public class ControlStructuresExample {
    public static void main(String[] args) {
        int number = 10;
        // if-else
        if (number > 0) {
            System.out.println("Positive number");
        } else {
            System.out.println("Non-positive number");
        }
        // switch
        int day = 3;
        switch (day) {
            case 1:
                System.out.println("Monday");
                break;
            default:
                System.out.println("Invalid day");
        }
        // for loop
        for (int i = 0; i < 5; i++) {
            System.out.println("for loop iteration: " + i);
        }
        // while loop
        int i = 0;
        while (i < 5) {
            System.out.println("while loop iteration: " + i);
            i++;
        }
        // do-while loop
        i = 0;
        do {
            System.out.println("do-while loop iteration: " + i);
            i++;
        } while (i < 5);
    }
}
```

### Exception Handling

- **try-catch**: Handle exceptions.
- **throw**: Explicitly throw an exception.
- **throws**: Declare an exception.
- **finally**: Block that always executes.

```java
public class ExceptionHandlingExample {

    public static void main(String[] args) {
        try {
            int result = divide(10, 0);
            System.out.println("Result: " + result);
        } catch (ArithmeticException e) {
            System.out.println("Caught an exception: " + e.getMessage());
        } finally {
            System.out.println("This block always executes.");
        }
    }
    // Method that declares an exception using 'throws'
    public static int divide(int a, int b) throws ArithmeticException {
        if (b == 0) {
            // Explicitly throw an exception
            throw new ArithmeticException("Division by zero is not allowed.");
        }
        return a / b;
    }
}

```

### Collections Framework

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/dc02bc8f-be1a-4238-8d11-8a2d66cc4ced/955abade-ef2e-4bea-af54-8ab458ddd881/Untitled.png)

### Multithreading

- **Thread Class**: Create a thread by extending Thread.
- **Runnable Interface**: Create a thread by implementing Runnable.
- **Synchronization**: Control access to shared resources.

### Object-Oriented Programming (OOP)

### Four Pillars

- **Encapsulation**: Wrapping data and methods into a single unit.Pojo
- **Inheritance**: Mechanism where one class acquires properties of another.
- **Polymorphism**: Ability to take many forms (method overloading and overriding).
- **Abstraction**: Hiding implementation details and showing only functionality.

### Classes and Objects

- **Class**: Blueprint for objects.
- **Object**: Instance of a class.
- **Constructors**: Special methods to initialize objects.

### Inheritance

- **extends**: Keyword to inherit a class.
- **super**: Reference to the parent class object.

### Polymorphism

- **Method Overloading**: Same method name with different parameters.
- **Method Overriding**: Subclass provides specific implementation of a method declared in the parent class.

### Interfaces and Abstract Classes

- **Interface**: Abstract type used to specify a behavior that classes must implement.
- **Abstract Class**: Class that cannot be instantiated and may contain abstract methods.

## **1. Functional Programming (java.util.function)**

### **1.1 Core Functional Interfaces**

### **Basic Four Operations**

```java
// Supplier<T> - Provides values (0-arity)
Supplier<String> supplier = () -> "Hello World";
String result = supplier.get();

// Consumer<T> - Accepts values (1-arity)
Consumer<String> consumer = s -> System.out.println(s);
consumer.accept("Hello");

// Predicate<T> - Tests values (1-arity)
Predicate<String> predicate = s -> s.length() > 5;
boolean result = predicate.test("Testing");

// Function<T,R> - Transforms values (1-arity)
Function<String, Integer> function = s -> s.length();
int length = function.apply("Hello");

// BiFunction<T,U,R> - Transforms two values (2-arity)
BiFunction<String, String, Integer> biFunction = (s1, s2) -> s1.length() + s2.length();
int totalLength = biFunction.apply("Hello", "World");// 10
```

### **1.2 Default Methods & Combinations**

```java
// Predicate combinations
Predicate<String> isLong = s -> s.length() > 5;
Predicate<String> startsWithA = s -> s.startsWith("A");
Predicate<String> combined = isLong.and(startsWithA);
Predicate<String> negated = isLong.negate();
Predicate<String> either = isLong.or(startsWithA);

// Function composition
Function<String, Integer> getLength = String::length;
Function<Integer, Integer> square = x -> x * x;
Function<String, Integer> getLengthSquared = getLength.andThen(square);
Function<String, Integer> composed = square.compose(getLength);

// Consumer chaining
Consumer<String> print = System.out::println;
Consumer<String> log = s -> logger.info(s);
Consumer<String> both = print.andThen(log);

```

---

## **2. Streams API**

### **2.1 Stream Creation**

```java
// From collections
List<String> list = Arrays.asList("a", "b", "c");
Stream<String> stream1 = list.stream();
Stream<String> parallelStream = list.parallelStream();

// From arrays
String[] array = {"a", "b", "c"};
Stream<String> stream2 = Arrays.stream(array);
Stream<String> stream3 = Stream.of("a", "b", "c");

// From generators
Stream<Double> randoms = Stream.generate(Math::random);
Stream<Integer> numbers = Stream.iterate(0, n -> n + 1);
Stream<Integer> limited = Stream.iterate(0, n -> n < 100, n -> n + 1);

// From ranges (primitive streams)IntStream range1 = IntStream.range(1, 10);// 1-9IntStream range2 = IntStream.rangeClosed(1, 10);// 1-10LongStream longStream = LongStream.range(1L, 1000000L);
DoubleStream doubleStream = DoubleStream.of(1.0, 2.0, 3.0);

// From files/strings
Stream<String> lines = Files.lines(Paths.get("file.txt"));
IntStream chars = "hello".chars();

```

### **2.2 Intermediate Operations**

### **Filtering & Mapping**

```java
// filter - keeps elements matching predicate
stream.filter(s -> s.length() > 3)

// map - transforms elements
stream.map(String::toUpperCase)
stream.map(s -> s.length())
stream.mapToInt(String::length)
stream.mapToLong(String::length)
stream.mapToDouble(String::length)

// flatMap - flattens nested structures
List<List<String>> nested = Arrays.asList(
    Arrays.asList("a", "b"), Arrays.asList("c", "d")
);
Stream<String> flattened = nested.stream().flatMap(List::stream);

// flatMapToInt/Long/Double
stream.flatMapToInt(s -> s.chars())

```

### **Sorting & Limiting**

```java
// sorted - natural order or with comparator
stream.sorted()
stream.sorted(Comparator.reverseOrder())
stream.sorted(Comparator.comparing(String::length))

// distinct - removes duplicates
stream.distinct()

// limit - takes first n elements
stream.limit(10)

// skip - skips first n elements
stream.skip(5)

// takeWhile/dropWhile (Java 9+)
stream.takeWhile(s -> s.length() < 5)
stream.dropWhile(s -> s.startsWith("A"))

```

### **Debugging Operations**

```java
// peek - performs action without consuming
stream.peek(System.out::println)
stream.peek(s -> logger.debug("Processing: " + s))

```

### **2.3 Terminal Operations**

### **Collecting Results**

```java
// collect - most flexible terminal operation
List<String> list = stream.collect(Collectors.toList());
Set<String> set = stream.collect(Collectors.toSet());
String joined = stream.collect(Collectors.joining(", "));

// toArray
String[] array = stream.toArray(String[]::new);
Object[] objects = stream.toArray();

// Collection-specific (Java 16+)
List<String> list = stream.toList();// unmodifiable
```

### **Reduction Operations**

```java
// reduce - combines all elements
Optional<String> result = stream.reduce((a, b) -> a + b);
String result = stream.reduce("", (a, b) -> a + b);
int sum = intStream.reduce(0, Integer::sum);

// countlong count = stream.count();

// min/max
Optional<String> min = stream.min(Comparator.naturalOrder());
Optional<String> max = stream.max(String::compareTo);

```

### **Finding Operations**

```java
// findFirst/findAny
Optional<String> first = stream.findFirst();
Optional<String> any = stream.findAny();

// allMatch/anyMatch/noneMatchboolean allLong = stream.allMatch(s -> s.length() > 3);
boolean anyLong = stream.anyMatch(s -> s.length() > 10);
boolean noneEmpty = stream.noneMatch(String::isEmpty);

```

### **forEach Operations**

```java
// forEach - terminal consumption
stream.forEach(System.out::println);
stream.forEachOrdered(System.out::println);// maintains order in parallel
```

### **2.4 Primitive Streams**

### **IntStream**

```java
IntStream intStream = IntStream.of(1, 2, 3, 4, 5);

// Primitive-specific operationsint sum = intStream.sum();
OptionalDouble average = intStream.average();
OptionalInt max = intStream.max();
OptionalInt min = intStream.min();
IntSummaryStatistics stats = intStream.summaryStatistics();

// Boxing
Stream<Integer> boxed = intStream.boxed();

```

### **LongStream & DoubleStream**

```java
LongStream longStream = LongStream.range(1, 1000);
DoubleStream doubleStream = DoubleStream.of(1.1, 2.2, 3.3);

// Similar operations as IntStreamlong sum = longStream.sum();
OptionalDouble avg = doubleStream.average();

```

### **2.5 Collectors Class (Complete List)**

### **Basic Collectors**

```java
// Collection collectors
Collectors.toList()
Collectors.toSet()
Collectors.toCollection(ArrayList::new)

// Array collectors
Collectors.toArray(String[]::new)

// String collectors
Collectors.joining()
Collectors.joining(", ")
Collectors.joining(", ", "[", "]")

// Counting
Collectors.counting()

```

### **Statistical Collectors**

```java
// Summarizing
Collectors.summarizingInt(String::length)
Collectors.summarizingLong(Long::valueOf)
Collectors.summarizingDouble(Double::valueOf)

// Min/Max
Collectors.maxBy(Comparator.naturalOrder())
Collectors.minBy(String::compareTo)

// Averaging/Summing
Collectors.averagingInt(String::length)
Collectors.summingInt(String::length)
Collectors.averagingDouble(Double::valueOf)
Collectors.summingDouble(Double::valueOf)

```

### **Grouping & Partitioning**

```java
// groupingBy - groups by classifier
Map<Integer, List<String>> byLength = stream.collect(
    Collectors.groupingBy(String::length)
);

// With downstream collector
Map<Integer, Long> countByLength = stream.collect(
    Collectors.groupingBy(String::length, Collectors.counting())
);

// partitioningBy - splits by predicate
Map<Boolean, List<String>> partitioned = stream.collect(
    Collectors.partitioningBy(s -> s.length() > 3)
);

// mapping - transforms before collecting
Map<Integer, List<String>> upperCaseByLength = stream.collect(
    Collectors.groupingBy(
        String::length,
        Collectors.mapping(String::toUpperCase, Collectors.toList())
    )
);

// filtering (Java 9+)
Map<Integer, List<String>> filteredByLength = stream.collect(
    Collectors.groupingBy(
        String::length,
        Collectors.filtering(s -> s.startsWith("A"), Collectors.toList())
    )
);

```

### **Advanced Collectors**

```java
// reducing
Collector<String, ?, Optional<String>> longest =
    Collectors.reducing(BinaryOperator.maxBy(Comparator.comparing(String::length)));

// collectingAndThen
List<String> unmodifiableList = stream.collect(
    Collectors.collectingAndThen(Collectors.toList(), Collections::unmodifiableList)
);

// toConcurrentMap
Map<String, Integer> concurrentMap = stream.collect(
    Collectors.toConcurrentMap(Function.identity(), String::length)
);

```

---

## **3. Threading & Concurrency (java.util.concurrent)**

### **3.1 Core Thread Classes**

### **Basic Threading**

```java
// Thread creationThread thread1 = new Thread(() -> System.out.println("Running"));
Thread thread2 = new Thread(new Runnable() {
    public void run() { System.out.println("Running"); }
});

// Thread methods
thread1.start();
thread1.join();
thread1.interrupt();
thread1.isAlive();
thread1.setDaemon(true);
Thread.sleep(1000);
Thread.currentThread();

```

### **3.2 Executor Framework**

### **Executor Interfaces**

```java
// Executor - basic executionExecutor executor = command -> new Thread(command).start();

// ExecutorService - lifecycle managementExecutorService executorService = Executors.newFixedThreadPool(4);
Future<String> future = executorService.submit(() -> "Result");
executorService.shutdown();
executorService.awaitTermination(1, TimeUnit.MINUTES);

// ScheduledExecutorService - delayed/periodic executionScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);
ScheduledFuture<?> scheduled = scheduler.schedule(() -> {}, 5, TimeUnit.SECONDS);
ScheduledFuture<?> periodic = scheduler.scheduleAtFixedRate(() -> {}, 0, 1, TimeUnit.SECONDS);

```

### **Executors Factory Methods**

```java
// Fixed thread poolsExecutorService fixedPool = Executors.newFixedThreadPool(4);
ExecutorService singleThread = Executors.newSingleThreadExecutor();

// Cached thread poolExecutorService cachedPool = Executors.newCachedThreadPool();

// Scheduled executorsScheduledExecutorService scheduledPool = Executors.newScheduledThreadPool(2);
ScheduledExecutorService singleScheduled = Executors.newSingleThreadScheduledExecutor();

// Work-stealing pool (Java 8+)ExecutorService workStealing = Executors.newWorkStealingPool();
ExecutorService workStealingWithParallelism = Executors.newWorkStealingPool(4);

// Virtual threads (Java 19+, preview in 17)ExecutorService virtualThreads = Executors.newVirtualThreadPerTaskExecutor();

```

### **3.3 Concurrent Collections**

### **Thread-Safe Lists**

```java
// CopyOnWriteArrayList - copy-on-write list
List<String> cowList = new CopyOnWriteArrayList<>();
cowList.add("item");

// Vector - synchronized list (legacy)
List<String> vector = new Vector<>();

```

### **Thread-Safe Sets**

```java
// CopyOnWriteArraySet
Set<String> cowSet = new CopyOnWriteArraySet<>();

// ConcurrentSkipListSet - sorted concurrent set
NavigableSet<String> skipListSet = new ConcurrentSkipListSet<>();

```

### **Thread-Safe Maps**

```java
// ConcurrentHashMap - high-performance concurrent map
ConcurrentMap<String, Integer> concurrentMap = new ConcurrentHashMap<>();
concurrentMap.putIfAbsent("key", 1);
concurrentMap.compute("key", (k, v) -> v == null ? 1 : v + 1);
concurrentMap.computeIfAbsent("key", k -> 1);
concurrentMap.computeIfPresent("key", (k, v) -> v + 1);
concurrentMap.merge("key", 1, Integer::sum);

// ConcurrentSkipListMap - sorted concurrent map
ConcurrentNavigableMap<String, Integer> skipListMap = new ConcurrentSkipListMap<>();

// Hashtable - synchronized map (legacy)
Map<String, Integer> hashtable = new Hashtable<>();

```

### **3.4 Blocking Queues**

### **Queue Implementations**

```java
// ArrayBlockingQueue - bounded FIFO queue
BlockingQueue<String> arrayQueue = new ArrayBlockingQueue<>(10);

// LinkedBlockingQueue - optionally bounded FIFO queue
BlockingQueue<String> linkedQueue = new LinkedBlockingQueue<>();
BlockingQueue<String> boundedLinkedQueue = new LinkedBlockingQueue<>(100);

// PriorityBlockingQueue - unbounded priority queue
BlockingQueue<String> priorityQueue = new PriorityBlockingQueue<>();

// DelayQueue - queue of delayed elements
BlockingQueue<Delayed> delayQueue = new DelayQueue<>();

// SynchronousQueue - handoff queue
BlockingQueue<String> synchronousQueue = new SynchronousQueue<>();

// LinkedTransferQueue - transfer queue
TransferQueue<String> transferQueue = new LinkedTransferQueue<>();

```

### **Queue Operations**

```java
// Blocking operations
queue.put("item");// blocks if fullString item = queue.take();// blocks if empty// Non-blocking operationsboolean added = queue.offer("item");
String polled = queue.poll();

// Timed operationsboolean offered = queue.offer("item", 1, TimeUnit.SECONDS);
String polled = queue.poll(1, TimeUnit.SECONDS);

```

### **3.5 Deques**

```java
// ArrayDeque - resizable array deque
Deque<String> arrayDeque = new ArrayDeque<>();

// LinkedBlockingDeque - concurrent deque
BlockingDeque<String> concurrentDeque = new LinkedBlockingDeque<>();

// Deque operations
deque.addFirst("first");
deque.addLast("last");
deque.offerFirst("first");
deque.offerLast("last");
String first = deque.removeFirst();
String last = deque.removeLast();
String polledFirst = deque.pollFirst();
String polledLast = deque.pollLast();

```

### **3.6 Synchronization Utilities**

### **CountDownLatch**

```java
CountDownLatch latch = new CountDownLatch(3);
// In worker threads
latch.countDown();
// In main thread
latch.await();// waits until count reaches 0
```

### **CyclicBarrier**

```java
CyclicBarrier barrier = new CyclicBarrier(3, () -> System.out.println("All reached"));
// In each thread
barrier.await();// waits until all threads reach barrier
```

### **Semaphore**

```java
Semaphore semaphore = new Semaphore(2);// 2 permits
semaphore.acquire();
// critical section
semaphore.release();

```

### **Exchanger**

```java
Exchanger<String> exchanger = new Exchanger<>();
// In thread 1String received = exchanger.exchange("data1");
// In thread 2String received = exchanger.exchange("data2");

```

### **Phaser (Java 7+)**

```java
Phaser phaser = new Phaser(3);// 3 parties// In each thread
phaser.arriveAndAwaitAdvance();// wait for all to arrive
```

### **3.7 Locks & Atomic Variables**

### **ReentrantLock**

```java
ReentrantLock lock = new ReentrantLock();
lock.lock();
try {
// critical section
} finally {
    lock.unlock();
}

// Try lock with timeoutif (lock.tryLock(1, TimeUnit.SECONDS)) {
    try {
// critical section
    } finally {
        lock.unlock();
    }
}

```

### **ReadWriteLock**

```java
ReadWriteLock rwLock = new ReentrantReadWriteLock();
Lock readLock = rwLock.readLock();
Lock writeLock = rwLock.writeLock();

// Multiple readers
readLock.lock();
try {
// read operation
} finally {
    readLock.unlock();
}

// Single writer
writeLock.lock();
try {
// write operation
} finally {
    writeLock.unlock();
}

```

### **StampedLock (Java 8+)**

```java
StampedLock stampedLock = new StampedLock();

// Optimistic readlong stamp = stampedLock.tryOptimisticRead();
// read dataif (!stampedLock.validate(stamp)) {
// fall back to read lock
    stamp = stampedLock.readLock();
    try {
// read data
    } finally {
        stampedLock.unlockRead(stamp);
    }
}

```

### **Atomic Classes**

```java
// Atomic primitivesAtomicInteger atomicInt = new AtomicInteger(0);
int value = atomicInt.get();
atomicInt.set(10);
int previous = atomicInt.getAndSet(20);
int incremented = atomicInt.incrementAndGet();
boolean updated = atomicInt.compareAndSet(20, 30);

// Other atomic typesAtomicLong atomicLong = new AtomicLong();
AtomicBoolean atomicBoolean = new AtomicBoolean();
AtomicReference<String> atomicRef = new AtomicReference<>();

// Atomic arraysAtomicIntegerArray atomicIntArray = new AtomicIntegerArray(10);
AtomicReferenceArray<String> atomicRefArray = new AtomicReferenceArray<>(10);

// Atomic field updaters
AtomicIntegerFieldUpdater<MyClass> fieldUpdater =
    AtomicIntegerFieldUpdater.newUpdater(MyClass.class, "volatileIntField");

```

### **3.8 CompletableFuture (Java 8+)**

### **Creation & Basic Operations**

```java
// Create completed future
CompletableFuture<String> completed = CompletableFuture.completedFuture("value");

// Async operations
CompletableFuture<String> async = CompletableFuture.supplyAsync(() -> "result");
CompletableFuture<Void> runAsync = CompletableFuture.runAsync(() -> System.out.println("done"));

// With custom executor
CompletableFuture<String> customExec = CompletableFuture.supplyAsync(() -> "result", executor);

```

### **Chaining Operations**

```java
CompletableFuture<String> future = CompletableFuture
    .supplyAsync(() -> "hello")
    .thenApply(s -> s + " world")
    .thenApply(String::toUpperCase)
    .thenCompose(s -> CompletableFuture.supplyAsync(() -> s + "!"))
    .thenAccept(System.out::println)
    .thenRun(() -> System.out.println("Done"));

```

### **Combining Futures**

```java
CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Hello");
CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "World");

// Combine both
CompletableFuture<String> combined = future1.thenCombine(future2, (s1, s2) -> s1 + " " + s2);

// Either one
CompletableFuture<String> either = future1.applyToEither(future2, s -> s.toUpperCase());

// Both complete
CompletableFuture<Void> both = future1.thenAcceptBoth(future2, (s1, s2) ->
    System.out.println(s1 + " " + s2));

// All of
CompletableFuture<Void> allOf = CompletableFuture.allOf(future1, future2);

// Any of
CompletableFuture<Object> anyOf = CompletableFuture.anyOf(future1, future2);

```

---

## **4. Collections Framework (Complete)**

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/dc02bc8f-be1a-4238-8d11-8a2d66cc4ced/955abade-ef2e-4bea-af54-8ab458ddd881/Untitled.png)

# **Core interfaces**

`Collection<E>` — Root type for groups of elements with basic add/remove/iterate operations.

- `List<E>` — Ordered, index-based sequence allowing duplicates.
- `Set<E>` — Unordered collection of unique elements.
- `SortedSet<E>` — Set with elements sorted by natural order or comparator.
- `NavigableSet<E>` — SortedSet with navigation methods like `lower`, `floor`, `ceiling`, `higher`.
- `Queue<E>` — FIFO collection supporting enqueue/dequeue semantics.
- `Deque<E>` — Double-ended queue supporting head and tail operations.
- `Map<K,V>` — Key–value association with unique keys.
- `SortedMap<K,V>` — Map sorted by key’s natural order or comparator.
- `NavigableMap<K,V>` — SortedMap with navigation like `lowerEntry`/`ceilingEntry`.

## **Abstract base classes**

- `AbstractCollection<E>` — Skeletal implementation for collections.
- `AbstractList<E>` — Skeletal implementation for random-access lists.
- `AbstractSequentialList<E>` — Skeletal implementation for sequential-access lists.
- `AbstractSet<E>` — Skeletal implementation for sets.
- `AbstractQueue<E>` — Skeletal implementation for queues.
- `AbstractMap<K,V>` — Skeletal implementation for maps.

## **List implementations**

- `ArrayList<E>` — Resizable array list with fast random access.
- `LinkedList<E>` — Doubly-linked list acting as List, Queue, and Deque.
- `Vector<E>` — Legacy synchronized resizable array list.
- `Stack<E>` — Legacy LIFO stack based on Vector.

## **Set implementations**

- `HashSet<E>` — Hash table set with no ordering guarantees.
- `LinkedHashSet<E>` — HashSet with predictable insertion-order iteration.
- `TreeSet<E>` — Red-black tree set with sorted order and NavigableSet ops.
- `EnumSet<E extends Enum<E>>` — High-performance set for enum constants.
- `CopyOnWriteArraySet<E>` — Thread-safe set optimized for reads.

## **Queue/Deque implementations**

- `ArrayDeque<E>` — Resizable array-based Deque (stack/queue).
- `PriorityQueue<E>` — Heap-based priority queue ordered by comparator/natural order.
- `LinkedBlockingQueue<E>` — Blocking FIFO queue with optional capacity bound.
- `ArrayBlockingQueue<E>` — Bounded blocking FIFO queue backed by array.
- `PriorityBlockingQueue<E>` — Unbounded blocking priority queue.
- `DelayQueue<E extends Delayed>` — Time-based retrieval queue for delayed elements.
- `SynchronousQueue<E>` — Handoff queue with no capacity.
- `LinkedTransferQueue<E>` — Unbounded transfer queue supporting producer handoff.
- `ConcurrentLinkedQueue<E>` — Lock-free, unbounded thread-safe queue.
- `ConcurrentLinkedDeque<E>` — Lock-free, unbounded thread-safe deque.

## **Map implementations**

- `HashMap<K,V>` — Hash table map with amortized O(1) ops, no order.
- `LinkedHashMap<K,V>` — HashMap with predictable insertion-order or access-order iteration.
- `TreeMap<K,V>` — Red-black tree map sorted by key with NavigableMap ops.
- `EnumMap<K extends Enum<K>,V>` — High-performance map for enum keys.
- `WeakHashMap<K,V>` — Map with keys held weakly, entries GC’d when keys unreachable.
- `IdentityHashMap<K,V>` — Map using reference identity (==) instead of equals().
- `Hashtable<K,V>` — Legacy synchronized hash table.
- `Properties` — Hashtable for string key/value pairs with config/file I/O support.

## **Concurrent maps**

- `ConcurrentHashMap<K,V>` — High-concurrency hash map with non-blocking reads and segmented updates.
- `ConcurrentSkipListMap<K,V>` — Concurrent, sorted, skip-list based NavigableMap.

## **Concurrent lists/sets**

- `CopyOnWriteArrayList<E>` — Thread-safe list that copies on write, ideal for frequent reads.
- `ConcurrentSkipListSet<E>` — Concurrent, sorted NavigableSet built on skip list.

## **Special-purpose collections**

- `BitSet` — Compact bit vector for boolean flags and set-like ops on bits.
- `Vector`/`Stack` — Legacy synchronized list/stack (prefer modern alternatives).
- `Collections` (utility) — Static factory/algorithms: `sort`, `binarySearch`, `unmodifiable*`, `synchronized*`, `singleton*`, `empty*`.
- `Arrays` (utility) — Array helpers including `asList`, `sort`, `binarySearch`, and array-to-collection bridges.

---

# **Quick contrasts in code**

```java
// List vs Set vs Map
List<String> list = new ArrayList<>();// ordered, allows duplicates
list.add("a"); list.add("a");// duplicates OK

Set<String> set = new HashSet<>();// unique, no order guarantee
set.add("a"); set.add("a");// second add ignored

Map<String,Integer> map = new HashMap<>();// key->value, unique keys
map.put("a", 1); map.put("a", 2);// overwrites value for key "a"
```

```java
// HashSet vs LinkedHashSet vs TreeSet
Set<Integer> hs  = new HashSet<>();// fastest adds, iteration order unspecified
Set<Integer> lhs = new LinkedHashSet<>();// preserves insertion order
Set<Integer> ts  = new TreeSet<>();// sorted ascending (or comparator)
```

```java
// ArrayList vs LinkedList
List<Integer> arr = new ArrayList<>();// O(1) random access, amortized O(1) append
List<Integer> lnk = new LinkedList<>();// O(1) add/remove ends, O(n) random access
```

```java
// Queue vs Deque
Queue<Integer> q = new ArrayDeque<>();// FIFO: offer/poll
q.offer(1); q.offer(2); q.poll();// 1

Deque<Integer> d = new ArrayDeque<>();// double-ended: addFirst/addLast/removeFirst/removeLast
d.addFirst(1); d.addLast(2); d.removeLast();// 2
```

```java
// PriorityQueue: smallest first by default
PriorityQueue<Integer> pq = new PriorityQueue<>();
pq.add(3); pq.add(1); pq.add(2);
pq.poll();// 1
```

```java
// TreeMap/NavigableMap navigation
NavigableMap<Integer,String> tm = new TreeMap<>();
tm.put(10,"a"); tm.put(20,"b");
tm.floorEntry(15).getValue();// "a"
tm.ceilingKey(15);// 20
```

```java
// ConcurrentHashMap vs synchronized Map
Map<String,Integer> m1 = new ConcurrentHashMap<>();// high concurrency, non-blocking reads
Map<String,Integer> m2 = Collections.synchronizedMap(new HashMap<>());// coarse-grained locking
```

```java
// CopyOnWriteArrayList: safe iteration under concurrent writes, expensive writes
CopyOnWriteArrayList<String> cow = new CopyOnWriteArrayList<>();
cow.add("x");
for (String s : cow) {
  cow.add("y");// no ConcurrentModificationException
}

```

```java
// WeakHashMap: entries auto-removed when keys only weakly reachable
WeakHashMap<Object, String> whm = new WeakHashMap<>();
Object key = new Object();
whm.put(key, "value");
key = null; System.gc();// entry may disappear later
```

```java
// Unmodifiable and immutable views
List<String> base = new ArrayList<>(List.of("a","b"));
List<String> ro = Collections.unmodifiableList(base);// throws on write via view
List<String> imm = List.of("x","y");// truly immutable list
```

```java
// EnumSet/EnumMap: compact and fast for enumsenum Day { MON, TUE, WED }
EnumSet<Day> work = EnumSet.of(Day.MON, Day.TUE);
EnumMap<Day, Integer> hours = new EnumMap<>(Day.class);
hours.put(Day.MON, 8);

```

```java
// Blocking queues for producer-consumer
BlockingQueue<Integer> bq = new ArrayBlockingQueue<>(10);
new Thread(() -> { try { bq.put(42); } catch (InterruptedException ignored) {} }).start();
try { int x = bq.take(); } catch (InterruptedException ignored) {}
```
