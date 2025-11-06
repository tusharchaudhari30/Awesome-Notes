## 1. Functional Programming (java.util.function)

### 1.1 Core Functional Interfaces

#### Basic Four Operations

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
int totalLength = biFunction.apply("Hello", "World"); // 10

```

### 1.2 Default Methods & Combinations

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

## 2. Streams API

### 2.1 Stream Creation

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

// From ranges (primitive streams)
IntStream range1 = IntStream.range(1, 10);      // 1-9
IntStream range2 = IntStream.rangeClosed(1, 10); // 1-10
LongStream longStream = LongStream.range(1L, 1000000L);
DoubleStream doubleStream = DoubleStream.of(1.0, 2.0, 3.0);

// From files/strings
Stream<String> lines = Files.lines(Paths.get("file.txt"));
IntStream chars = "hello".chars();
```

### 2.2 Intermediate Operations

#### Filtering & Mapping

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

#### Sorting & Limiting

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

#### Debugging Operations

```java
// peek - performs action without consuming
stream.peek(System.out::println)
stream.peek(s -> logger.debug("Processing: " + s))
```

### 2.3 Terminal Operations

#### Collecting Results

```java
// collect - most flexible terminal operation
List<String> list = stream.collect(Collectors.toList());
Set<String> set = stream.collect(Collectors.toSet());
String joined = stream.collect(Collectors.joining(", "));

// toArray
String[] array = stream.toArray(String[]::new);
Object[] objects = stream.toArray();

// Collection-specific (Java 16+)
List<String> list = stream.toList(); // unmodifiable
```

#### Reduction Operations

```java
// reduce - combines all elements
Optional<String> result = stream.reduce((a, b) -> a + b);
String result = stream.reduce("", (a, b) -> a + b);
int sum = intStream.reduce(0, Integer::sum);

// count
long count = stream.count();

// min/max
Optional<String> min = stream.min(Comparator.naturalOrder());
Optional<String> max = stream.max(String::compareTo);
```

#### Finding Operations

```java
// findFirst/findAny
Optional<String> first = stream.findFirst();
Optional<String> any = stream.findAny();

// allMatch/anyMatch/noneMatch
boolean allLong = stream.allMatch(s -> s.length() > 3);
boolean anyLong = stream.anyMatch(s -> s.length() > 10);
boolean noneEmpty = stream.noneMatch(String::isEmpty);
```

#### forEach Operations

```java
// forEach - terminal consumption
stream.forEach(System.out::println);
stream.forEachOrdered(System.out::println); // maintains order in parallel
```

### 2.4 Primitive Streams

#### IntStream

```java
IntStream intStream = IntStream.of(1, 2, 3, 4, 5);

// Primitive-specific operations
int sum = intStream.sum();
OptionalDouble average = intStream.average();
OptionalInt max = intStream.max();
OptionalInt min = intStream.min();
IntSummaryStatistics stats = intStream.summaryStatistics();

// Boxing
Stream<Integer> boxed = intStream.boxed();
```

#### LongStream & DoubleStream

```java
LongStream longStream = LongStream.range(1, 1000);
DoubleStream doubleStream = DoubleStream.of(1.1, 2.2, 3.3);

// Similar operations as IntStream
long sum = longStream.sum();
OptionalDouble avg = doubleStream.average();
```

### 2.5 Collectors Class (Complete List)

#### Basic Collectors

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

#### Statistical Collectors

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

#### Grouping & Partitioning

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

#### Advanced Collectors

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

## 3. Threading & Concurrency (java.util.concurrent)

### 3.1 Core Thread Classes

#### Basic Threading

```java
// Thread creation
Thread thread1 = new Thread(() -> System.out.println("Running"));
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

### 3.2 Executor Framework

#### Executor Interfaces

```java
// Executor - basic execution
Executor executor = command -> new Thread(command).start();

// ExecutorService - lifecycle management
ExecutorService executorService = Executors.newFixedThreadPool(4);
Future<String> future = executorService.submit(() -> "Result");
executorService.shutdown();
executorService.awaitTermination(1, TimeUnit.MINUTES);

// ScheduledExecutorService - delayed/periodic execution
ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);
ScheduledFuture<?> scheduled = scheduler.schedule(() -> {}, 5, TimeUnit.SECONDS);
ScheduledFuture<?> periodic = scheduler.scheduleAtFixedRate(() -> {}, 0, 1, TimeUnit.SECONDS);
```

#### Executors Factory Methods

```java
// Fixed thread pools
ExecutorService fixedPool = Executors.newFixedThreadPool(4);
ExecutorService singleThread = Executors.newSingleThreadExecutor();

// Cached thread pool
ExecutorService cachedPool = Executors.newCachedThreadPool();

// Scheduled executors
ScheduledExecutorService scheduledPool = Executors.newScheduledThreadPool(2);
ScheduledExecutorService singleScheduled = Executors.newSingleThreadScheduledExecutor();

// Work-stealing pool (Java 8+)
ExecutorService workStealing = Executors.newWorkStealingPool();
ExecutorService workStealingWithParallelism = Executors.newWorkStealingPool(4);

// Virtual threads (Java 19+, preview in 17)
ExecutorService virtualThreads = Executors.newVirtualThreadPerTaskExecutor();
```

### 3.3 Concurrent Collections

#### Thread-Safe Lists

```java
// CopyOnWriteArrayList - copy-on-write list
List<String> cowList = new CopyOnWriteArrayList<>();
cowList.add("item");

// Vector - synchronized list (legacy)
List<String> vector = new Vector<>();
```

#### Thread-Safe Sets

```java
// CopyOnWriteArraySet
Set<String> cowSet = new CopyOnWriteArraySet<>();

// ConcurrentSkipListSet - sorted concurrent set
NavigableSet<String> skipListSet = new ConcurrentSkipListSet<>();
```

#### Thread-Safe Maps

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

### 3.4 Blocking Queues

#### Queue Implementations

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

#### Queue Operations

```java
// Blocking operations
queue.put("item");        // blocks if full
String item = queue.take(); // blocks if empty

// Non-blocking operations
boolean added = queue.offer("item");
String polled = queue.poll();

// Timed operations
boolean offered = queue.offer("item", 1, TimeUnit.SECONDS);
String polled = queue.poll(1, TimeUnit.SECONDS);
```

### 3.5 Deques

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

### 3.6 Synchronization Utilities

#### CountDownLatch

```java
CountDownLatch latch = new CountDownLatch(3);
// In worker threads
latch.countDown();
// In main thread
latch.await(); // waits until count reaches 0
```

#### CyclicBarrier

```java
CyclicBarrier barrier = new CyclicBarrier(3, () -> System.out.println("All reached"));
// In each thread
barrier.await(); // waits until all threads reach barrier
```

#### Semaphore

```java
Semaphore semaphore = new Semaphore(2); // 2 permits
semaphore.acquire();
// critical section
semaphore.release();
```

#### Exchanger

```java
Exchanger<String> exchanger = new Exchanger<>();
// In thread 1
String received = exchanger.exchange("data1");
// In thread 2
String received = exchanger.exchange("data2");
```

#### Phaser (Java 7+)

```java
Phaser phaser = new Phaser(3); // 3 parties
// In each thread
phaser.arriveAndAwaitAdvance(); // wait for all to arrive
```

### 3.7 Locks & Atomic Variables

#### ReentrantLock

```java
ReentrantLock lock = new ReentrantLock();
lock.lock();
try {
    // critical section
} finally {
    lock.unlock();
}

// Try lock with timeout
if (lock.tryLock(1, TimeUnit.SECONDS)) {
    try {
        // critical section
    } finally {
        lock.unlock();
    }
}
```

#### ReadWriteLock

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

#### StampedLock (Java 8+)

```java
StampedLock stampedLock = new StampedLock();

// Optimistic read
long stamp = stampedLock.tryOptimisticRead();
// read data
if (!stampedLock.validate(stamp)) {
    // fall back to read lock
    stamp = stampedLock.readLock();
    try {
        // read data
    } finally {
        stampedLock.unlockRead(stamp);
    }
}
```

#### Atomic Classes

```java
// Atomic primitives
AtomicInteger atomicInt = new AtomicInteger(0);
int value = atomicInt.get();
atomicInt.set(10);
int previous = atomicInt.getAndSet(20);
int incremented = atomicInt.incrementAndGet();
boolean updated = atomicInt.compareAndSet(20, 30);

// Other atomic types
AtomicLong atomicLong = new AtomicLong();
AtomicBoolean atomicBoolean = new AtomicBoolean();
AtomicReference<String> atomicRef = new AtomicReference<>();

// Atomic arrays
AtomicIntegerArray atomicIntArray = new AtomicIntegerArray(10);
AtomicReferenceArray<String> atomicRefArray = new AtomicReferenceArray<>(10);

// Atomic field updaters
AtomicIntegerFieldUpdater<MyClass> fieldUpdater =
    AtomicIntegerFieldUpdater.newUpdater(MyClass.class, "volatileIntField");
```

### 3.8 CompletableFuture (Java 8+)

#### Creation & Basic Operations

```java
// Create completed future
CompletableFuture<String> completed = CompletableFuture.completedFuture("value");

// Async operations
CompletableFuture<String> async = CompletableFuture.supplyAsync(() -> "result");
CompletableFuture<Void> runAsync = CompletableFuture.runAsync(() -> System.out.println("done"));

// With custom executor
CompletableFuture<String> customExec = CompletableFuture.supplyAsync(() -> "result", executor);
```

#### Chaining Operations

```java
CompletableFuture<String> future = CompletableFuture
    .supplyAsync(() -> "hello")
    .thenApply(s -> s + " world")
    .thenApply(String::toUpperCase)
    .thenCompose(s -> CompletableFuture.supplyAsync(() -> s + "!"))
    .thenAccept(System.out::println)
    .thenRun(() -> System.out.println("Done"));
```

#### Combining Futures

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

## 4. Collections Framework (Complete)

### 4.1 Collection Hierarchy

#### Collection Interface Methods

```java
Collection<String> collection = new ArrayList<>();

// Basic operations
boolean add(E e);
boolean remove(Object o);
boolean contains(Object o);
int size();
boolean isEmpty();
void clear();

// Bulk operations
boolean addAll(Collection<? extends E> c);
boolean removeAll(Collection<?> c);
boolean retainAll(Collection<?> c);
boolean containsAll(Collection<?> c);

// Array operations
Object[] toArray();
<T> T[] toArray(T[] a);

// Java 8+ operations
boolean removeIf(Predicate<? super E> filter);
void forEach(Consumer<? super E> action);
Spliterator<E> spliterator();
Stream<E> stream();
Stream<E> parallelStream();
```

### 4.2 List Implementations

#### ArrayList

```java
List<String> arrayList = new ArrayList<>();
List<String> withCapacity = new ArrayList<>(100);
List<String> fromCollection = new ArrayList<>(otherCollection);

// List-specific operations
String get(int index);
String set(int index, String element);
void add(int index, String element);
String remove(int index);
int indexOf(Object o);
int lastIndexOf(Object o);
List<String> subList(int from, int to);
```

#### LinkedList

```java
LinkedList<String> linkedList = new LinkedList<>();

// Deque operations
void addFirst(String e);
void addLast(String e);
String removeFirst();
String removeLast();
String peekFirst();
String peekLast();
```

#### Vector (Legacy)

```java
Vector<String> vector = new Vector<>(); // synchronized
```

#### CopyOnWriteArrayList

```java
List<String> cowList = new CopyOnWriteArrayList<>(); // thread-safe, copy-on-write
```

### 4.3 Set Implementations

#### HashSet

```java
Set<String> hashSet = new HashSet<>();
Set<String> withCapacity = new HashSet<>(100);
Set<String> withLoadFactor = new HashSet<>(100, 0.75f);
```

#### LinkedHashSet

```java
Set<String> linkedHashSet = new LinkedHashSet<>(); // maintains insertion order
```

#### TreeSet

```java
NavigableSet<String> treeSet = new TreeSet<>(); // sorted
NavigableSet<String> withComparator = new TreeSet<>(Comparator.reverseOrder());

// NavigableSet methods
String lower(String e);
String floor(String e);
String ceiling(String e);
String higher(String e);
String pollFirst();
String pollLast();
NavigableSet<String> descendingSet();
Iterator<String> descendingIterator();
NavigableSet<String> subSet(String from, boolean fromInclusive,
                            String to, boolean toInclusive);
NavigableSet<String> headSet(String to, boolean inclusive);
NavigableSet<String> tailSet(String from, boolean inclusive);
```

#### EnumSet

```java
EnumSet<DayOfWeek> weekdays = EnumSet.range(DayOfWeek.MONDAY, DayOfWeek.FRIDAY);
EnumSet<DayOfWeek> weekend = EnumSet.of(DayOfWeek.SATURDAY, DayOfWeek.SUNDAY);
EnumSet<DayOfWeek> all = EnumSet.allOf(DayOfWeek.class);
EnumSet<DayOfWeek> none = EnumSet.noneOf(DayOfWeek.class);
```

### 4.4 Map Implementations

#### HashMap

```java
Map<String, Integer> hashMap = new HashMap<>();
Map<String, Integer> withCapacity = new HashMap<>(100);

// Map operations
Integer put(String key, Integer value);
Integer get(Object key);
Integer remove(Object key);
boolean containsKey(Object key);
boolean containsValue(Object value);
Set<String> keySet();
Collection<Integer> values();
Set<Map.Entry<String, Integer>> entrySet();

// Java 8+ methods
Integer getOrDefault(Object key, Integer defaultValue);
Integer putIfAbsent(String key, Integer value);
boolean remove(Object key, Object value);
boolean replace(String key, Integer oldValue, Integer newValue);
Integer replace(String key, Integer value);
Integer compute(String key, BiFunction<String, Integer, Integer> remappingFunction);
Integer computeIfAbsent(String key, Function<String, Integer> mappingFunction);
Integer computeIfPresent(String key, BiFunction<String, Integer, Integer> remappingFunction);
Integer merge(String key, Integer value, BiFunction<Integer, Integer, Integer> remappingFunction);
void forEach(BiConsumer<String, Integer> action);
void replaceAll(BiFunction<String, Integer, Integer> function);
```

#### LinkedHashMap

```java
Map<String, Integer> linkedHashMap = new LinkedHashMap<>(); // maintains insertion order
Map<String, Integer> accessOrder = new LinkedHashMap<>(16, 0.75f, true); // access order
```

#### TreeMap

```java
NavigableMap<String, Integer> treeMap = new TreeMap<>(); // sorted by keys
NavigableMap<String, Integer> withComparator = new TreeMap<>(Comparator.reverseOrder());

// NavigableMap methods
Map.Entry<String, Integer> lowerEntry(String key);
String lowerKey(String key);
Map.Entry<String, Integer> floorEntry(String key);
String floorKey(String key);
Map.Entry<String, Integer> ceilingEntry(String key);
String ceilingKey(String key);
Map.Entry<String, Integer> higherEntry(String key);
String higherKey(String key);
Map.Entry<String, Integer> firstEntry();
Map.Entry<String, Integer> lastEntry();
Map.Entry<String, Integer> pollFirstEntry();
Map.Entry<String, Integer> pollLastEntry();
NavigableMap<String, Integer> descendingMap();
NavigableSet<String> navigableKeySet();
NavigableSet<String> descendingKeySet();
NavigableMap<String, Integer> subMap(String from, boolean fromInclusive,
                                     String to, boolean toInclusive);
NavigableMap<String, Integer> headMap(String to, boolean inclusive);
NavigableMap<String, Integer> tailMap(String from, boolean inclusive);
```

#### ConcurrentHashMap

```java
ConcurrentMap<String, Integer> concurrentMap = new ConcurrentHashMap<>();

// Concurrent operations
Integer putIfAbsent(String key, Integer value);
boolean remove(Object key, Object value);
Integer replace(String key, Integer value);
boolean replace(String key, Integer oldValue, Integer newValue);
```

#### EnumMap

```java
Map<DayOfWeek, String> enumMap = new EnumMap<>(DayOfWeek.class);
```

### 4.5 Queue Implementations

#### ArrayDeque

```java
Deque<String> arrayDeque = new ArrayDeque<>();

// Queue operations (FIFO)
boolean offer(String e);
String poll();
String peek();

// Stack operations (LIFO)
void push(String e);
String pop();

// Deque operations
void addFirst(String e);
void addLast(String e);
String removeFirst();
String removeLast();
String peekFirst();
String peekLast();
```

#### PriorityQueue

```java
PriorityQueue<String> priorityQueue = new PriorityQueue<>();
PriorityQueue<String> withComparator = new PriorityQueue<>(Comparator.reverseOrder());

// Queue operations
boolean offer(String e);
String poll();
String peek();
```

### 4.6 Collections Utility Class

#### Factory Methods

```java
// Empty collections
List<String> emptyList = Collections.emptyList();
Set<String> emptySet = Collections.emptySet();
Map<String, Integer> emptyMap = Collections.emptyMap();

// Singleton collections
List<String> singletonList = Collections.singletonList("item");
Set<String> singletonSet = Collections.singleton("item");
Map<String, Integer> singletonMap = Collections.singletonMap("key", 1);

// nCopies
List<String> copies = Collections.nCopies(5, "item");
```

#### Algorithms

```java
List<String> list = new ArrayList<>();

// Sorting
Collections.sort(list);
Collections.sort(list, Comparator.reverseOrder());

// Searching
int index = Collections.binarySearch(list, "item");

// Shuffling
Collections.shuffle(list);
Collections.shuffle(list, new Random());

// Reversing
Collections.reverse(list);

// Rotating
Collections.rotate(list, 2);

// Min/Max
String min = Collections.min(list);
String max = Collections.max(list, comparator);

// Frequency
int count = Collections.frequency(list, "item");

// Replacing
boolean replaced = Collections.replaceAll(list, "old", "new");

// Copying
Collections.copy(destination, source);

// Filling
Collections.fill(list, "value");
```

#### Synchronized Wrappers

```java
List<String> syncList = Collections.synchronizedList(new ArrayList<>());
Set<String> syncSet = Collections.synchronizedSet(new HashSet<>());
Map<String, Integer> syncMap = Collections.synchronizedMap(new HashMap<>());
```

#### Unmodifiable Wrappers

```java
List<String> unmodList = Collections.unmodifiableList(list);
Set<String> unmodSet = Collections.unmodifiableSet(set);
Map<String, Integer> unmodMap = Collections.unmodifiableMap(map);
```

### 4.7 Factory Methods (Java 9+)

```java
// List factory methods
List<String> list = List.of("a", "b", "c");
List<String> empty = List.of();

// Set factory methods
Set<String> set = Set.of("a", "b", "c");
Set<String> empty = Set.of();

// Map factory methods
Map<String, Integer> map = Map.of("a", 1, "b", 2, "c", 3);
Map<String, Integer> mapFromEntries = Map.ofEntries(
    Map.entry("a", 1),
    Map.entry("b", 2),
    Map.entry("c", 3)
);
```

---

## Summary: Complete API Reference

This brainmap covers **all major classes and methods** in:

### **Functional Programming**

- **43 functional interfaces** with all their methods
- **Default method combinations** for composition
- **Method references** and **lambda expressions**

### **Streams API**

- **Stream creation** from all sources
- **25+ intermediate operations**
- **15+ terminal operations**
- **Primitive streams** (IntStream, LongStream, DoubleStream)
- **30+ Collectors** for complex reductions

### **Threading & Concurrency**

- **Executor framework** with all implementations
- **12+ concurrent collections**
- **8+ synchronization utilities**
- **Atomic classes** and **locks**
- **CompletableFuture** with all operations

### **Collections Framework**

- **15+ collection implementations**
- **All interface methods** for List, Set, Map, Queue, Deque
- **Collections utility class** with 20+ algorithms
- **Factory methods** and **views**

Each section includes **complete method signatures** and **practical code examples** showing real usage patterns.

[1](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_a6559622-e442-497c-b6c4-55a437ed9544/f771d900-48d0-42e7-a8f1-a711a230a316/Oracle-Press-for-Java-Khalid-Mughal-Vasily-Strelnikov-OCP-Oracle-Certified-Professional-Java-SE-17-Developer-Exam-1Z0-829-Programmer-s-Guide-Oracle-Press-2023.pdf)
[2](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_a6559622-e442-497c-b6c4-55a437ed9544/4e75dc53-0148-467a-9ec6-000c3a89b019/Cay-S.-Horstmann-Core-Java-for-the-Impatient-3rd-Edition-2022-Addison-Wesley-Professional-libgen.li.pdf)
