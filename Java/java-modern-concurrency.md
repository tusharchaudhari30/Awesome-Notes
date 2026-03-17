# Java Modern Concurrency — Complete Interview-Ready Technical Notes

---

## Table of Contents

1. [Fundamentals of Concurrency](#1-fundamentals-of-concurrency)
2. [Thread Lifecycle & Creation](#2-thread-lifecycle--creation)
3. [Synchronization & Locks](#3-synchronization--locks)
4. [The `java.util.concurrent` Package](#4-the-javautilconcurrent-package)
5. [Executor Framework](#5-executor-framework)
6. [Fork/Join Framework](#6-forkjoin-framework)
7. [Concurrent Collections](#7-concurrent-collections)
8. [Atomic Variables & CAS](#8-atomic-variables--cas)
9. [CompletableFuture & Asynchronous Programming](#9-completablefuture--asynchronous-programming)
10. [Locks, Conditions & Synchronizers](#10-locks-conditions--synchronizers)
11. [The Java Memory Model (JMM)](#11-the-java-memory-model-jmm)
12. [`volatile`, `happens-before`, and Ordering](#12-volatile-happens-before-and-ordering)
13. [ThreadLocal & InheritableThreadLocal](#13-threadlocal--inheritablethreadlocal)
14. [Virtual Threads (Project Loom — Java 21+)](#14-virtual-threads-project-loom--java-21)
15. [Structured Concurrency (JEP 453 — Java 21+)](#15-structured-concurrency-jep-453--java-21)
16. [Scoped Values (JEP 446 — Java 21+)](#16-scoped-values-jep-446--java-21)
17. [Reactive Streams & Flow API (Java 9+)](#17-reactive-streams--flow-api-java-9)
18. [StampedLock (Java 8+)](#18-stampedlock-java-8)
19. [Common Concurrency Patterns](#19-common-concurrency-patterns)
20. [Common Concurrency Problems & Pitfalls](#20-common-concurrency-problems--pitfalls)
21. [Best Practices & Interview Tips](#21-best-practices--interview-tips)
22. [Quick-Reference Cheat Sheet](#22-quick-reference-cheat-sheet)

---

## 1. Fundamentals of Concurrency

### 1.1 Concurrency vs. Parallelism

| Aspect | Concurrency | Parallelism |
|--------|------------|-------------|
| Definition | Managing multiple tasks by interleaving execution on one or more cores | Executing multiple tasks **simultaneously** on multiple CPU cores |
| Goal | Improved **responsiveness** and task management | Improved **throughput** via hardware utilization |
| Requires | At least one CPU core | Multiple CPU cores |
| Example | A web server handling 1000 connections on 4 threads | Matrix multiplication split across 8 cores |

### 1.2 Process vs. Thread

| Aspect | Process | Thread |
|--------|---------|--------|
| Memory | Separate address space | Shared heap, separate stack |
| Communication | IPC (sockets, pipes, shared memory) | Direct via shared variables |
| Overhead | Heavy (context switch involves page tables) | Lighter (shares address space) |
| Isolation | Crash in one process doesn't affect others | Unhandled exception can crash the JVM |

### 1.3 Why Concurrency Is Hard

- **Visibility problem**: One thread's writes may not be visible to another thread without proper synchronization.
- **Atomicity problem**: Compound operations (check-then-act, read-modify-write) can be interleaved.
- **Ordering problem**: Compilers/CPUs reorder instructions for performance; without memory barriers, observed order may differ from program order.

---

## 2. Thread Lifecycle & Creation

### 2.1 Thread States (`Thread.State` enum)

```
NEW → RUNNABLE → (BLOCKED | WAITING | TIMED_WAITING) → TERMINATED
```

| State | Description |
|-------|-------------|
| `NEW` | Created but `start()` not yet called |
| `RUNNABLE` | Eligible to run (may or may not be actually executing on a CPU) |
| `BLOCKED` | Waiting to acquire an intrinsic monitor lock |
| `WAITING` | Waiting indefinitely — `Object.wait()`, `Thread.join()`, `LockSupport.park()` |
| `TIMED_WAITING` | Waiting with a timeout — `Thread.sleep()`, `wait(timeout)`, `join(timeout)` |
| `TERMINATED` | Execution completed (normally or via exception) |

### 2.2 Ways to Create Threads

**Method 1: Extending `Thread`**

```java
class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Running in: " + Thread.currentThread().getName());
    }
}

MyThread t = new MyThread();
t.start(); // NEVER call run() directly — it won't create a new thread
```

**Method 2: Implementing `Runnable` (preferred — allows extending another class)**

```java
class MyTask implements Runnable {
    @Override
    public void run() {
        System.out.println("Task executing");
    }
}

Thread t = new Thread(new MyTask(), "worker-1");
t.start();

// Lambda shorthand (Java 8+)
Thread t2 = new Thread(() -> System.out.println("Lambda task"));
t2.start();
```

**Method 3: Implementing `Callable<V>` (returns a result, can throw checked exceptions)**

```java
Callable<Integer> task = () -> {
    TimeUnit.SECONDS.sleep(1);
    return 42;
};

ExecutorService executor = Executors.newSingleThreadExecutor();
Future<Integer> future = executor.submit(task);
Integer result = future.get(); // Blocks until result is available
executor.shutdown();
```

### 2.3 Daemon vs. User Threads

```java
Thread daemon = new Thread(() -> { /* background work */ });
daemon.setDaemon(true); // Must be set BEFORE start()
daemon.start();
```

- **User threads**: JVM waits for all user threads to finish before exiting.
- **Daemon threads**: JVM exits when only daemon threads remain. `finally` blocks may NOT execute.
- GC, Signal Dispatcher, and Finalizer are daemon threads.

### 2.4 Thread Priority

```java
thread.setPriority(Thread.MAX_PRIORITY);  // 10
thread.setPriority(Thread.NORM_PRIORITY); // 5 (default)
thread.setPriority(Thread.MIN_PRIORITY);  // 1
```

- Priorities are **hints** to the OS scheduler — no guarantees.
- Avoid relying on priorities for correctness.

### 2.5 Key Thread Methods

| Method | Description |
|--------|-------------|
| `start()` | Schedules thread for execution; calls `run()` in new thread |
| `run()` | Entry point; calling directly does NOT create a new thread |
| `join()` | Caller blocks until this thread terminates |
| `join(long millis)` | Caller blocks for at most `millis` ms |
| `sleep(long millis)` | Static; pauses current thread (does NOT release locks) |
| `yield()` | Hint to scheduler to give up current time slice |
| `interrupt()` | Sets interrupt flag; may throw `InterruptedException` if thread is blocked |
| `isInterrupted()` | Checks interrupt flag without clearing it |
| `Thread.interrupted()` | Static; checks AND clears the interrupt flag of current thread |
| `setUncaughtExceptionHandler()` | Registers a handler for uncaught exceptions |

### 2.6 Interruption Model

```java
class InterruptibleTask implements Runnable {
    @Override
    public void run() {
        while (!Thread.currentThread().isInterrupted()) {
            try {
                // Blocking call — throws InterruptedException, CLEARS interrupt flag
                TimeUnit.MILLISECONDS.sleep(100);
                doWork();
            } catch (InterruptedException e) {
                // Option 1: Restore interrupt flag and exit
                Thread.currentThread().interrupt();
                break;
                // Option 2: Propagate (if Callable)
                // throw new RuntimeException(e);
            }
        }
        System.out.println("Thread cleanly interrupted");
    }
}
```

**Critical rule**: Never swallow `InterruptedException` silently. Either re-interrupt the thread or propagate.

---

## 3. Synchronization & Locks

### 3.1 The `synchronized` Keyword

Every Java object has an **intrinsic lock (monitor)**.

```java
// Method-level synchronization
public synchronized void increment() {    // Lock on 'this'
    count++;
}

public static synchronized void staticMethod() { // Lock on Class object
    // ...
}

// Block-level synchronization (preferred — finer granularity)
public void transfer(Account from, Account to, int amount) {
    synchronized (from) {      // Lock on 'from' object
        synchronized (to) {    // Lock on 'to' object (BEWARE: deadlock risk)
            from.debit(amount);
            to.credit(amount);
        }
    }
}
```

### 3.2 Reentrancy

Intrinsic locks in Java are **reentrant** — the same thread can acquire a lock it already holds without deadlocking.

```java
public synchronized void outer() {
    inner(); // Same thread re-acquires the lock — OK (reentrant)
}

public synchronized void inner() {
    // ...
}
```

### 3.3 `wait()`, `notify()`, `notifyAll()`

These methods belong to `java.lang.Object` and must be called from within a `synchronized` block on the **same object**.

```java
class BoundedBuffer<T> {
    private final Queue<T> queue = new LinkedList<>();
    private final int capacity;

    public BoundedBuffer(int capacity) { this.capacity = capacity; }

    public synchronized void put(T item) throws InterruptedException {
        while (queue.size() == capacity) { // ALWAYS use 'while', NOT 'if' (spurious wakeups)
            wait();  // Releases lock, suspends thread
        }
        queue.add(item);
        notifyAll(); // Wake up ALL waiting threads
    }

    public synchronized T take() throws InterruptedException {
        while (queue.isEmpty()) {
            wait();
        }
        T item = queue.poll();
        notifyAll();
        return item;
    }
}
```

**Interview key points:**
- `wait()` releases the intrinsic lock; `Thread.sleep()` does NOT.
- Always call `wait()` in a `while` loop — **spurious wakeups** can occur.
- Prefer `notifyAll()` over `notify()` — `notify()` wakes only one arbitrary thread and can cause **liveness failures**.

---

## 4. The `java.util.concurrent` Package

Introduced in Java 5 (JSR 166), designed by Doug Lea. Major sub-packages:

| Package | Contents |
|---------|----------|
| `java.util.concurrent` | Executors, Future, concurrent collections, synchronizers |
| `java.util.concurrent.atomic` | Lock-free atomic variables (CAS-based) |
| `java.util.concurrent.locks` | Explicit lock implementations |

---

## 5. Executor Framework

### 5.1 Architecture

```
                  Executor (interface)
                     │
                ExecutorService (interface)
                     │
          ┌──────────┼──────────────┐
  AbstractExecutorService    ScheduledExecutorService (interface)
          │                          │
  ThreadPoolExecutor     ScheduledThreadPoolExecutor
          │
  ForkJoinPool
```

### 5.2 `Executor` and `ExecutorService`

```java
// Executor — simple task submission
public interface Executor {
    void execute(Runnable command);
}

// ExecutorService — full lifecycle management
public interface ExecutorService extends Executor {
    <T> Future<T> submit(Callable<T> task);
    Future<?> submit(Runnable task);
    <T> List<Future<T>> invokeAll(Collection<? extends Callable<T>> tasks);
    <T> T invokeAny(Collection<? extends Callable<T>> tasks);
    void shutdown();          // Graceful — no new tasks, finishes existing
    List<Runnable> shutdownNow(); // Attempts to stop all tasks
    boolean awaitTermination(long timeout, TimeUnit unit);
    boolean isShutdown();
    boolean isTerminated();
}
```

### 5.3 Factory Methods via `Executors`

```java
// Fixed thread pool — bounded, best for CPU-bound tasks
ExecutorService fixed = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());

// Cached thread pool — unbounded, reuses idle threads, good for short-lived I/O tasks
ExecutorService cached = Executors.newCachedThreadPool();

// Single thread executor — guarantees sequential execution, task ordering
ExecutorService single = Executors.newSingleThreadExecutor();

// Scheduled thread pool — delayed and periodic tasks
ScheduledExecutorService scheduled = Executors.newScheduledThreadPool(4);

// Work-stealing pool (Java 8+) — uses ForkJoinPool
ExecutorService workStealing = Executors.newWorkStealingPool();

// Virtual thread per-task executor (Java 21+)
ExecutorService virtual = Executors.newVirtualThreadPerTaskExecutor();
```

### 5.4 `ThreadPoolExecutor` — The Core Implementation

```java
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    4,                  // corePoolSize — minimum threads kept alive
    8,                  // maximumPoolSize — max threads allowed
    60L,                // keepAliveTime — idle time before excess threads are terminated
    TimeUnit.SECONDS,   // time unit for keepAliveTime
    new LinkedBlockingQueue<>(100),  // workQueue — holds tasks before execution
    new ThreadFactoryBuilder().setNameFormat("worker-%d").build(), // threadFactory
    new ThreadPoolExecutor.CallerRunsPolicy()  // rejectedExecutionHandler
);
```

**Task submission flow:**

```
Task submitted
    │
    ├─ threads < corePoolSize? → Create new core thread
    │
    ├─ Queue not full? → Enqueue task
    │
    ├─ threads < maximumPoolSize? → Create new non-core thread
    │
    └─ Queue full AND at max threads → RejectedExecutionHandler
```

### 5.5 Rejection Policies

| Policy | Behavior |
|--------|----------|
| `AbortPolicy` (default) | Throws `RejectedExecutionException` |
| `CallerRunsPolicy` | Runs the task in the caller's thread (back-pressure) |
| `DiscardPolicy` | Silently discards the task |
| `DiscardOldestPolicy` | Discards oldest unprocessed task, retries submission |

### 5.6 Choosing the Right Queue

| Queue Type | Behavior | Use Case |
|------------|----------|----------|
| `LinkedBlockingQueue` (unbounded) | Never triggers thread creation beyond core | Default for `newFixedThreadPool` |
| `ArrayBlockingQueue` (bounded) | Triggers new thread creation when full | Rate limiting, back-pressure |
| `SynchronousQueue` | Direct handoff; no buffering | Default for `newCachedThreadPool` |
| `PriorityBlockingQueue` | Priority ordering | Priority-based task execution |
| `DelayQueue` | Tasks available only after delay | Scheduled task execution |

### 5.7 `ScheduledExecutorService`

```java
ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);

// One-time delayed execution
scheduler.schedule(() -> System.out.println("Delayed"), 5, TimeUnit.SECONDS);

// Fixed-rate: every 2s starting after 1s (timer ticks are independent of task duration)
scheduler.scheduleAtFixedRate(() -> doWork(), 1, 2, TimeUnit.SECONDS);

// Fixed-delay: 2s AFTER previous task completes
scheduler.scheduleWithFixedDelay(() -> doWork(), 1, 2, TimeUnit.SECONDS);
```

**`scheduleAtFixedRate` vs `scheduleWithFixedDelay`:**
- **Fixed rate**: If task takes longer than period, next execution starts immediately after previous finishes (no parallel runs).
- **Fixed delay**: Guarantees a gap between end of one execution and start of next.

### 5.8 `Future<V>` Interface

```java
Future<String> future = executor.submit(() -> {
    TimeUnit.SECONDS.sleep(2);
    return "Result";
});

future.isDone();          // Non-blocking check
future.isCancelled();     // Was it cancelled?
future.cancel(true);      // Attempt cancellation; true = interrupt if running
String result = future.get();                      // Blocks indefinitely
String result2 = future.get(5, TimeUnit.SECONDS);  // Blocks with timeout
```

**Limitations of `Future`** (motivates `CompletableFuture`):
- Cannot chain or compose futures
- No callback mechanism
- `get()` is blocking
- No exception handling pipeline
- Cannot combine multiple futures

### 5.9 Proper Shutdown Pattern

```java
executor.shutdown(); // Prevent new task submission
try {
    if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
        executor.shutdownNow(); // Force shutdown
        if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
            System.err.println("Executor did not terminate");
        }
    }
} catch (InterruptedException e) {
    executor.shutdownNow();
    Thread.currentThread().interrupt();
}
```

---

## 6. Fork/Join Framework

Introduced in Java 7. Based on **work-stealing** algorithm. Optimized for recursive divide-and-conquer tasks.

### 6.1 Core Classes

| Class | Description |
|-------|-------------|
| `ForkJoinPool` | Executor that manages worker threads with work-stealing |
| `ForkJoinTask<V>` | Abstract base; lighter than `Thread` |
| `RecursiveTask<V>` | Returns a result |
| `RecursiveAction` | No result (void) |

### 6.2 Example: Parallel Sum

```java
class ParallelSum extends RecursiveTask<Long> {
    private static final int THRESHOLD = 10_000;
    private final long[] array;
    private final int start, end;

    ParallelSum(long[] array, int start, int end) {
        this.array = array;
        this.start = start;
        this.end = end;
    }

    @Override
    protected Long compute() {
        int length = end - start;
        if (length <= THRESHOLD) {
            // Base case — compute directly
            long sum = 0;
            for (int i = start; i < end; i++) sum += array[i];
            return sum;
        }

        // Recursive case — split
        int mid = start + length / 2;
        ParallelSum left = new ParallelSum(array, start, mid);
        ParallelSum right = new ParallelSum(array, mid, end);

        left.fork();            // Asynchronously execute left half
        long rightResult = right.compute();  // Compute right half in current thread
        long leftResult = left.join();       // Wait for left half

        return leftResult + rightResult;
    }
}

// Usage
ForkJoinPool pool = new ForkJoinPool(); // Uses Runtime.availableProcessors() threads
// OR use the common pool:
// ForkJoinPool pool = ForkJoinPool.commonPool();

long[] data = LongStream.rangeClosed(1, 1_000_000).toArray();
long result = pool.invoke(new ParallelSum(data, 0, data.length));
```

### 6.3 Work-Stealing Algorithm

- Each worker thread has a **deque (double-ended queue)**.
- A thread pushes/pops from the **tail** of its own deque (LIFO — better locality).
- Idle threads **steal** from the **head** of another thread's deque (FIFO — takes largest chunks).

### 6.4 `ForkJoinPool.commonPool()`

- Shared instance used by parallel streams and `CompletableFuture.supplyAsync()`.
- Default parallelism = `Runtime.getRuntime().availableProcessors() - 1`.
- Configurable via `-Djava.util.concurrent.ForkJoinPool.common.parallelism=N`.
- **Caution**: Long-running/blocking tasks in the common pool can starve other operations (including parallel streams).

### 6.5 `ManagedBlocker`

For blocking operations inside `ForkJoinPool`, use `ManagedBlocker` to allow the pool to compensate by creating additional threads:

```java
ForkJoinPool.managedBlock(new ForkJoinPool.ManagedBlocker() {
    @Override public boolean block() throws InterruptedException {
        result = blockingOperation();
        return true;
    }
    @Override public boolean isReleasable() {
        return result != null;
    }
});
```

---

## 7. Concurrent Collections

### 7.1 Overview

| Collection | Description | Key Characteristics |
|-----------|-------------|---------------------|
| `ConcurrentHashMap` | Thread-safe `HashMap` | Segment-based locking (pre-Java 8), CAS + `synchronized` on bins (Java 8+) |
| `ConcurrentSkipListMap` | Thread-safe sorted map | `O(log n)` operations, no locking |
| `ConcurrentSkipListSet` | Thread-safe sorted set | Based on `ConcurrentSkipListMap` |
| `ConcurrentLinkedQueue` | Lock-free FIFO queue | Michael-Scott non-blocking algorithm |
| `ConcurrentLinkedDeque` | Lock-free double-ended queue | CAS-based |
| `CopyOnWriteArrayList` | Thread-safe `ArrayList` | Copies entire array on every mutation; great for read-heavy scenarios |
| `CopyOnWriteArraySet` | Thread-safe `Set` | Based on `CopyOnWriteArrayList` |

### 7.2 `ConcurrentHashMap` Deep Dive

```java
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();

// Basic atomic operations
map.put("key", 1);
map.putIfAbsent("key", 2);       // Only if key is absent
map.replace("key", 1, 10);       // CAS-like: only if current value is 1
map.remove("key", 10);           // Only if value is 10

// Atomic compute operations (Java 8+)
map.compute("key", (k, v) -> v == null ? 1 : v + 1);
map.computeIfAbsent("key", k -> expensiveComputation(k));
map.computeIfPresent("key", (k, v) -> v + 1);
map.merge("key", 1, Integer::sum); // If absent → put 1; if present → sum

// Bulk operations (Java 8+) — parallelismThreshold
// Operations parallelize if estimated map size exceeds threshold
map.forEach(1, (k, v) -> System.out.println(k + "=" + v));  // threshold=1 → always parallel
long count = map.reduceValuesToLong(1, Long::valueOf, 0L, Long::sum);
String result = map.search(1, (k, v) -> v > 100 ? k : null);
```

**Interview critical points:**
- Java 8 replaced segment-based locking with **CAS + per-bin `synchronized`** + **tree bins** (red-black trees when collision chains exceed **8 entries** and table has ≥ **64 buckets**; otherwise the bin is expanded).
- **`size()`** returns an approximate count. Use **`mappingCount()`** (returns `long`) for potentially large maps.
- **NOT a replacement for synchronized blocks** when you need atomicity across multiple operations.
- `compute` / `merge` lambdas execute atomically per key but should be **short and non-blocking**.

### 7.3 `CopyOnWriteArrayList`

```java
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
list.add("A");  // Creates a new copy of the internal array

// Iterator sees a SNAPSHOT — no ConcurrentModificationException
for (String s : list) {
    list.add("B"); // OK! Iterator sees the old snapshot
}
```

- **Use when**: Reads vastly outnumber writes (e.g., listener lists, configuration).
- **Avoid when**: Frequent writes — each mutation copies the entire array → O(n) per write.

### 7.4 Blocking Queues

| Queue | Bounded? | Ordering | Special Features |
|-------|----------|----------|------------------|
| `ArrayBlockingQueue` | Yes (fixed) | FIFO | Optional fairness policy |
| `LinkedBlockingQueue` | Optional | FIFO | Separate put/take locks |
| `PriorityBlockingQueue` | No | Priority | Natural ordering or `Comparator` |
| `DelayQueue` | No | Delay-based | Elements available only after their delay expires |
| `SynchronousQueue` | Zero capacity | Direct handoff | No internal storage; put blocks until take |
| `LinkedTransferQueue` | No | FIFO | `transfer()` blocks until consumer receives |

```java
BlockingQueue<Task> queue = new ArrayBlockingQueue<>(100);

// Producer
queue.put(task);        // Blocks if full
queue.offer(task, 1, TimeUnit.SECONDS); // Waits up to 1s

// Consumer
Task t = queue.take();  // Blocks if empty
Task t2 = queue.poll(1, TimeUnit.SECONDS); // Waits up to 1s
```

**Producer-Consumer Pattern:**

```java
class Producer implements Runnable {
    private final BlockingQueue<String> queue;
    Producer(BlockingQueue<String> q) { this.queue = q; }

    @Override
    public void run() {
        try {
            for (int i = 0; i < 100; i++) {
                queue.put("Item-" + i);
            }
            queue.put("POISON_PILL"); // Sentinel to signal termination
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}

class Consumer implements Runnable {
    private final BlockingQueue<String> queue;
    Consumer(BlockingQueue<String> q) { this.queue = q; }

    @Override
    public void run() {
        try {
            while (true) {
                String item = queue.take();
                if ("POISON_PILL".equals(item)) break;
                process(item);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

---

## 8. Atomic Variables & CAS

### 8.1 Compare-And-Swap (CAS) Principle

CAS is a CPU-level atomic instruction:

```
CAS(memoryLocation, expectedValue, newValue)
  → if memoryLocation == expectedValue:
       memoryLocation = newValue; return true
    else:
       return false (and retry)
```

- **Non-blocking**: Threads never hold locks.
- **Lock-free**: At least one thread always makes progress.
- Used in `java.util.concurrent.atomic` and internal JDK data structures.

### 8.2 Atomic Classes

| Class | Description |
|-------|-------------|
| `AtomicInteger` | Atomic `int` operations |
| `AtomicLong` | Atomic `long` operations |
| `AtomicBoolean` | Atomic `boolean` operations |
| `AtomicReference<V>` | Atomic reference operations |
| `AtomicIntegerArray` | Atomic operations on `int[]` |
| `AtomicLongArray` | Atomic operations on `long[]` |
| `AtomicReferenceArray<E>` | Atomic operations on `Object[]` |
| `AtomicMarkableReference<V>` | Reference + boolean mark (solve ABA partially) |
| `AtomicStampedReference<V>` | Reference + int stamp (fully solves ABA problem) |
| `AtomicIntegerFieldUpdater<T>` | Reflection-based atomic update of `volatile int` fields |
| `AtomicLongFieldUpdater<T>` | Reflection-based atomic update of `volatile long` fields |
| `AtomicReferenceFieldUpdater<T,V>` | Reflection-based atomic update of `volatile` reference fields |

### 8.3 Key Operations

```java
AtomicInteger counter = new AtomicInteger(0);

counter.get();                    // Read
counter.set(10);                  // Write
counter.getAndIncrement();        // i++ atomically
counter.incrementAndGet();        // ++i atomically
counter.getAndAdd(5);             // Add and return old value
counter.addAndGet(5);             // Add and return new value
counter.compareAndSet(10, 20);    // CAS
counter.getAndUpdate(x -> x * 2);      // Atomic update with function
counter.updateAndGet(x -> x * 2);      // Atomic update, return new value
counter.getAndAccumulate(5, Integer::sum); // Combine with accumulator
counter.accumulateAndGet(5, Integer::sum);

// AtomicReference
AtomicReference<Node> head = new AtomicReference<>(null);
head.compareAndSet(expectedNode, newNode);
```

### 8.4 ABA Problem

```
Thread 1: Reads A, gets preempted
Thread 2: Changes A → B → A
Thread 1: CAS succeeds (sees A) — but the state has changed underneath
```

**Solution: `AtomicStampedReference`**

```java
AtomicStampedReference<String> ref = new AtomicStampedReference<>("A", 0);

int[] stampHolder = new int[1];
String current = ref.get(stampHolder); // Gets value AND stamp
int stamp = stampHolder[0];

// CAS checks BOTH value AND stamp
ref.compareAndSet("A", "B", stamp, stamp + 1);
```

### 8.5 `LongAdder` and `LongAccumulator` (Java 8+)

For high-contention counters, `LongAdder` outperforms `AtomicLong` by distributing updates across **cells** (striping).

```java
LongAdder adder = new LongAdder();
adder.increment();   // Distributed across cells
adder.add(10);
long sum = adder.sum();       // Aggregates all cells — NOT atomic snapshot
adder.sumThenReset();         // Read and reset

// LongAccumulator — generalized version
LongAccumulator max = new LongAccumulator(Long::max, Long.MIN_VALUE);
max.accumulate(42);
max.get();

// DoubleAdder, DoubleAccumulator also available
```

**When to use what:**
- **Single variable, low contention** → `AtomicLong`
- **Single variable, high contention (many writers)** → `LongAdder`
- **CAS semantics needed** → `AtomicLong` or `AtomicReference`

### 8.6 `VarHandle` (Java 9+)

Low-level alternative to `sun.misc.Unsafe` for atomic and ordered access.

```java
import java.lang.invoke.MethodHandles;
import java.lang.invoke.VarHandle;

class Counter {
    private volatile int count;

    private static final VarHandle COUNT;
    static {
        try {
            COUNT = MethodHandles.lookup()
                .findVarHandle(Counter.class, "count", int.class);
        } catch (ReflectiveOperationException e) {
            throw new ExceptionInInitializerError(e);
        }
    }

    public void increment() {
        COUNT.getAndAdd(this, 1);   // Atomic increment
    }

    public boolean cas(int expected, int update) {
        return COUNT.compareAndSet(this, expected, update);
    }

    // Access modes:
    // COUNT.get(this)                  — plain read
    // COUNT.getVolatile(this)          — volatile read
    // COUNT.getOpaque(this)            — opaque read (no reordering guarantee, but sees latest write)
    // COUNT.getAcquire(this)           — acquire read (loads after this won't be reordered before it)
    // COUNT.set(this, val)             — plain write
    // COUNT.setVolatile(this, val)     — volatile write
    // COUNT.setOpaque(this, val)       — opaque write
    // COUNT.setRelease(this, val)      — release write (stores before this won't be reordered after it)
}
```

---

## 9. CompletableFuture & Asynchronous Programming

### 9.1 Overview

`CompletableFuture<T>` (Java 8) implements both `Future<T>` and `CompletionStage<T>`. Supports:
- Non-blocking callbacks
- Chaining / composition
- Combining multiple futures
- Exception handling pipelines
- Explicit completion

### 9.2 Creating CompletableFutures

```java
// Run async (no return value)
CompletableFuture<Void> cf1 = CompletableFuture.runAsync(() -> doWork());

// Supply async (returns value)
CompletableFuture<String> cf2 = CompletableFuture.supplyAsync(() -> fetchData());

// With custom executor
ExecutorService myPool = Executors.newFixedThreadPool(4);
CompletableFuture<String> cf3 = CompletableFuture.supplyAsync(() -> fetchData(), myPool);

// Pre-completed futures
CompletableFuture<String> completed = CompletableFuture.completedFuture("value");
CompletableFuture<String> failed = CompletableFuture.failedFuture(new RuntimeException("error"));

// Manual completion
CompletableFuture<String> manual = new CompletableFuture<>();
manual.complete("done");          // First call wins
manual.completeExceptionally(ex); // Complete with exception
manual.completeOnTimeout("default", 5, TimeUnit.SECONDS); // Java 9+
manual.orTimeout(5, TimeUnit.SECONDS); // Java 9+ — completes exceptionally on timeout
```

### 9.3 Transformation & Chaining

```java
CompletableFuture<String> future = CompletableFuture
    .supplyAsync(() -> "Hello")

    // thenApply: T → U (synchronous transformation)
    .thenApply(s -> s + " World")

    // thenApplyAsync: T → U (async transformation, uses ForkJoinPool.commonPool())
    .thenApplyAsync(String::toUpperCase)

    // thenApplyAsync with custom executor
    .thenApplyAsync(s -> s + "!", myPool);
```

### 9.4 Method Variants: Sync vs. Async

| Sync (runs in completing thread or caller) | Async (default pool) | Async (custom executor) |
|---|---|---|
| `thenApply(Function)` | `thenApplyAsync(Function)` | `thenApplyAsync(Function, Executor)` |
| `thenAccept(Consumer)` | `thenAcceptAsync(Consumer)` | `thenAcceptAsync(Consumer, Executor)` |
| `thenRun(Runnable)` | `thenRunAsync(Runnable)` | `thenRunAsync(Runnable, Executor)` |
| `thenCompose(Function)` | `thenComposeAsync(Function)` | `thenComposeAsync(Function, Executor)` |
| `thenCombine(CF, BiFunction)` | `thenCombineAsync(...)` | `thenCombineAsync(..., Executor)` |
| `handle(BiFunction)` | `handleAsync(BiFunction)` | `handleAsync(BiFunction, Executor)` |

### 9.5 Full API Categories

```java
// --- TRANSFORMATION ---
// thenApply: Transform result (T → U)
cf.thenApply(result -> result.toUpperCase());

// --- CONSUMPTION ---
// thenAccept: Consume result (T → void)
cf.thenAccept(result -> System.out.println(result));

// --- ACTION ---
// thenRun: Run action after completion (ignores result)
cf.thenRun(() -> System.out.println("Done"));

// --- FLAT MAP (monadic composition) ---
// thenCompose: T → CompletableFuture<U> (avoids CompletableFuture<CompletableFuture<U>>)
cf.thenCompose(userId -> fetchUserAsync(userId));  // Like flatMap

// --- COMBINING TWO FUTURES ---
// thenCombine: Combine results of two independent futures
cf1.thenCombine(cf2, (result1, result2) -> result1 + result2);

// thenAcceptBoth: Consume results of both (no return)
cf1.thenAcceptBoth(cf2, (r1, r2) -> System.out.println(r1 + " " + r2));

// runAfterBoth: Run action after both complete
cf1.runAfterBoth(cf2, () -> System.out.println("Both done"));

// --- EITHER/ANY ---
// applyToEither: Use result of whichever completes first
cf1.applyToEither(cf2, result -> result.toUpperCase());

// acceptEither: Consume whichever completes first
cf1.acceptEither(cf2, System.out::println);

// runAfterEither: Run after either completes
cf1.runAfterEither(cf2, () -> System.out.println("One done"));
```

### 9.6 Combining Multiple Futures

```java
List<CompletableFuture<String>> futures = urls.stream()
    .map(url -> CompletableFuture.supplyAsync(() -> fetch(url)))
    .collect(Collectors.toList());

// allOf: Completes when ALL futures complete (returns CompletableFuture<Void>)
CompletableFuture<Void> allDone = CompletableFuture.allOf(
    futures.toArray(new CompletableFuture[0])
);

// Collect results after all complete
CompletableFuture<List<String>> allResults = allDone.thenApply(v ->
    futures.stream()
        .map(CompletableFuture::join) // Safe — all already completed
        .collect(Collectors.toList())
);

// anyOf: Completes when ANY future completes (returns CompletableFuture<Object>)
CompletableFuture<Object> firstDone = CompletableFuture.anyOf(
    futures.toArray(new CompletableFuture[0])
);
```

### 9.7 Exception Handling

```java
CompletableFuture<String> result = CompletableFuture
    .supplyAsync(() -> {
        if (error) throw new RuntimeException("Oops");
        return "OK";
    })

    // exceptionally: Handle exception, provide fallback (only called on failure)
    .exceptionally(ex -> {
        log.error("Failed", ex);
        return "Fallback";
    })

    // handle: Called on BOTH success and failure
    .handle((value, ex) -> {
        if (ex != null) return "Error: " + ex.getMessage();
        return "Success: " + value;
    })

    // whenComplete: Peek at result/exception without transforming
    .whenComplete((value, ex) -> {
        if (ex != null) log.error("Failed", ex);
        else log.info("Completed: " + value);
    });

// Java 12+
cf.exceptionallyCompose(ex -> fetchFromBackup());   // Async recovery
cf.exceptionallyAsync(ex -> "fallback");             // Async exception handler
```

### 9.8 `thenApply` vs `thenCompose`

```java
// thenApply: synchronous transformation → CompletableFuture<T>
CompletableFuture<String> cf = getUserId()
    .thenApply(id -> id.toUpperCase()); // String → String

// thenCompose: async transformation → avoids nesting
// WRONG: thenApply returns CompletableFuture<CompletableFuture<User>>
CompletableFuture<CompletableFuture<User>> nested = getUserId()
    .thenApply(id -> fetchUserAsync(id)); // String → CompletableFuture<User>

// CORRECT: thenCompose flattens the nesting
CompletableFuture<User> flat = getUserId()
    .thenCompose(id -> fetchUserAsync(id)); // String → CompletableFuture<User> → flattened
```

**Analogy**: `thenApply` is `map`, `thenCompose` is `flatMap`.

---

## 10. Locks, Conditions & Synchronizers

### 10.1 `ReentrantLock`

```java
import java.util.concurrent.locks.ReentrantLock;

ReentrantLock lock = new ReentrantLock();       // Non-fair (default)
ReentrantLock fairLock = new ReentrantLock(true); // Fair — FIFO ordering (lower throughput)

lock.lock();
try {
    // Critical section
} finally {
    lock.unlock(); // ALWAYS in finally
}

// Timed and interruptible locking
if (lock.tryLock()) {                       // Non-blocking attempt
    try { /* ... */ } finally { lock.unlock(); }
}

if (lock.tryLock(1, TimeUnit.SECONDS)) {    // Timed attempt
    try { /* ... */ } finally { lock.unlock(); }
}

lock.lockInterruptibly(); // Throws InterruptedException if interrupted while waiting
```

**`ReentrantLock` vs `synchronized`:**

| Feature | `synchronized` | `ReentrantLock` |
|---------|---------------|-----------------|
| Syntax | Implicit (keyword) | Explicit (API) |
| Release | Automatic (block exit) | Manual (`unlock()` in `finally`) |
| Fairness | Non-fair only | Configurable |
| `tryLock()` | No | Yes |
| Interruptible | No | Yes (`lockInterruptibly()`) |
| Multiple conditions | No (one wait-set per monitor) | Yes (`newCondition()`) |
| Performance | Optimized in modern JVMs | Comparable |

### 10.2 `ReadWriteLock` / `ReentrantReadWriteLock`

Allows concurrent reads, exclusive writes.

```java
ReadWriteLock rwLock = new ReentrantReadWriteLock();
Lock readLock = rwLock.readLock();
Lock writeLock = rwLock.writeLock();

// Multiple threads can hold the read lock simultaneously
readLock.lock();
try {
    return data.get(key);
} finally {
    readLock.unlock();
}

// Only one thread can hold the write lock (exclusive)
writeLock.lock();
try {
    data.put(key, value);
} finally {
    writeLock.unlock();
}
```

- **Read lock**: Shared — multiple readers allowed.
- **Write lock**: Exclusive — no readers or other writers.
- **Downgrade**: A thread holding the write lock CAN acquire the read lock, then release the write lock.
- **Upgrade**: A thread holding the read lock CANNOT acquire the write lock (deadlocks). Use `StampedLock` instead.

### 10.3 `Condition` (replacement for `wait/notify`)

```java
ReentrantLock lock = new ReentrantLock();
Condition notEmpty = lock.newCondition();
Condition notFull = lock.newCondition();

// Producer
lock.lock();
try {
    while (queue.size() == capacity) {
        notFull.await(); // Like Object.wait() — releases the lock
    }
    queue.add(item);
    notEmpty.signal(); // Like Object.notify()
} finally {
    lock.unlock();
}

// Consumer
lock.lock();
try {
    while (queue.isEmpty()) {
        notEmpty.await();
    }
    queue.remove();
    notFull.signal();
} finally {
    lock.unlock();
}
```

**Key `Condition` methods:**
- `await()` — releases lock, waits until signaled
- `await(long time, TimeUnit unit)` — timed await
- `awaitNanos(long nanosTimeout)` — precise nanosecond timing
- `awaitUntil(Date deadline)` — absolute time deadline
- `awaitUninterruptibly()` — cannot be interrupted
- `signal()` — wake one waiting thread
- `signalAll()` — wake all waiting threads

### 10.4 `CountDownLatch`

One-shot barrier — threads wait until count reaches zero.

```java
int workerCount = 5;
CountDownLatch startSignal = new CountDownLatch(1);
CountDownLatch doneSignal = new CountDownLatch(workerCount);

for (int i = 0; i < workerCount; i++) {
    new Thread(() -> {
        try {
            startSignal.await(); // All workers wait for start signal
            doWork();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            doneSignal.countDown(); // Signal completion
        }
    }).start();
}

startSignal.countDown();      // Release all workers
doneSignal.await();           // Wait for all workers to finish
System.out.println("All done");
```

- **Cannot be reset** — use `CyclicBarrier` or `Phaser` for reusable barriers.

### 10.5 `CyclicBarrier`

Reusable barrier — parties wait for each other, then all proceed.

```java
int parties = 3;
CyclicBarrier barrier = new CyclicBarrier(parties, () -> {
    System.out.println("All parties arrived — barrier action executed");
});

for (int i = 0; i < parties; i++) {
    new Thread(() -> {
        try {
            System.out.println(Thread.currentThread().getName() + " working...");
            doPhaseWork();

            barrier.await(); // Wait for all parties
            // After barrier breaks, all threads continue here

            doNextPhaseWork();
            barrier.await(); // Barrier is reusable!
        } catch (InterruptedException | BrokenBarrierException e) {
            Thread.currentThread().interrupt();
        }
    }).start();
}
```

**`CountDownLatch` vs `CyclicBarrier`:**

| Aspect | `CountDownLatch` | `CyclicBarrier` |
|--------|-----------------|-----------------|
| Reusable | No | Yes |
| Action | One thread waits for N events | N threads wait for each other |
| Barrier action | None | Optional `Runnable` on trip |
| Reset | Cannot reset | `reset()` method |

### 10.6 `Semaphore`

Controls access to a shared resource with a fixed number of permits.

```java
Semaphore semaphore = new Semaphore(3);       // 3 permits
Semaphore fairSem = new Semaphore(3, true);   // Fair ordering

semaphore.acquire();     // Blocks if no permits available
try {
    accessResource();
} finally {
    semaphore.release(); // Returns permit
}

// Non-blocking
if (semaphore.tryAcquire(1, TimeUnit.SECONDS)) {
    try { accessResource(); }
    finally { semaphore.release(); }
}

// Acquire multiple permits at once
semaphore.acquire(2);
```

- **Binary semaphore** (permits=1): Similar to a mutex, but **non-reentrant** and **any thread can release** (unlike locks).
- Use for connection pooling, rate limiting, resource throttling.

### 10.7 `Phaser` (Java 7)

Flexible synchronization barrier supporting dynamic registration/deregistration and multiple phases.

```java
Phaser phaser = new Phaser(1); // Register self (the main thread)

for (int i = 0; i < 3; i++) {
    phaser.register(); // Register each worker
    new Thread(() -> {
        for (int phase = 0; phase < 3; phase++) {
            doPhaseWork(phase);
            phaser.arriveAndAwaitAdvance(); // Wait for all parties
        }
        phaser.arriveAndDeregister(); // Done — leave the phaser
    }).start();
}

phaser.arriveAndDeregister(); // Main thread deregisters
```

- Replaces both `CountDownLatch` and `CyclicBarrier` with more flexibility.
- Supports **tiered phasers** (tree structure) for large numbers of parties.

### 10.8 `Exchanger<V>`

Two-thread synchronization point where threads swap values.

```java
Exchanger<String> exchanger = new Exchanger<>();

// Thread 1
String fromThread2 = exchanger.exchange("Data from Thread 1");

// Thread 2
String fromThread1 = exchanger.exchange("Data from Thread 2");
```

---

## 11. The Java Memory Model (JMM)

### 11.1 What the JMM Defines

The **Java Memory Model** (JSR-133, Java 5+) specifies:
- When writes by one thread are **guaranteed to be visible** to reads by another thread.
- What reorderings are permitted by the compiler and CPU.
- How `synchronized`, `volatile`, and `final` establish ordering guarantees.

### 11.2 Key Concepts

**Main memory vs. Working memory**: Each thread may cache variables in CPU caches/registers. The JMM defines when cache flushes must occur.

**Program order**: The order of statements within a single thread.

**Happens-before relationship** (`→hb`): If action A happens-before action B, then B is **guaranteed** to see the effects of A.

### 11.3 Happens-Before Rules

1. **Program order rule**: Each action in a thread happens-before every subsequent action in that thread.
2. **Monitor lock rule**: An unlock on a monitor happens-before every subsequent lock on that same monitor.
3. **Volatile variable rule**: A write to a `volatile` field happens-before every subsequent read of that same field.
4. **Thread start rule**: `Thread.start()` happens-before any action in the started thread.
5. **Thread join rule**: All actions in a thread happen-before another thread returns from `join()` on that thread.
6. **Thread interruption rule**: `thread.interrupt()` happens-before the interrupted thread detects the interruption.
7. **Finalizer rule**: End of a constructor happens-before the start of the finalizer for that object.
8. **Transitivity**: If A →hb B and B →hb C, then A →hb C.

### 11.4 Data Races

A **data race** occurs when:
- Two threads access the same variable
- At least one access is a write
- The accesses are not ordered by a happens-before relationship

Programs with data races have **undefined behavior** in the JMM.

### 11.5 Safe Publication

An object is safely published when both the reference to the object and the object's state are visible to other threads at the same time.

**Safe publication idioms:**
1. Initialize from a `static` initializer.
2. Store in a `volatile` field or `AtomicReference`.
3. Store in a `final` field of a properly constructed object.
4. Store in a field guarded by a lock.

```java
// UNSAFE publication
public class Holder {
    private int n;
    public Holder(int n) { this.n = n; }
    public void assertSanity() {
        if (n != n) throw new AssertionError("This CAN happen without safe publication");
    }
}

// Another thread may see a partially constructed Holder (n=0 then n=42)
public Holder holder;
// ... in some thread:
holder = new Holder(42); // UNSAFE — no volatile/synchronized

// SAFE: Use volatile
public volatile Holder holder;
```

---

## 12. `volatile`, `happens-before`, and Ordering

### 12.1 `volatile` Keyword

```java
private volatile boolean flag = false;
private volatile int counter = 0;
```

**Guarantees:**
- **Visibility**: A write to a `volatile` variable is immediately visible to all threads.
- **Ordering**: A write to a `volatile` variable happens-before all subsequent reads of that variable (establishes a happens-before edge).
- **No word tearing**: 64-bit `volatile long` and `volatile double` are atomic (without `volatile`, they are NOT guaranteed atomic on 32-bit JVMs).

**Does NOT guarantee:**
- **Atomicity of compound operations**: `volatile int counter; counter++` is NOT atomic (it's read-modify-write).

### 12.2 When to Use `volatile`

```java
// Pattern 1: Status flags
private volatile boolean shutdown = false;

public void shutdown() { shutdown = true; }
public void doWork() {
    while (!shutdown) { /* work */ }
}

// Pattern 2: Double-checked locking (only works with volatile!)
class Singleton {
    private static volatile Singleton instance;

    public static Singleton getInstance() {
        if (instance == null) {                // First check (no lock)
            synchronized (Singleton.class) {
                if (instance == null) {         // Second check (with lock)
                    instance = new Singleton(); // volatile prevents reordering
                }
            }
        }
        return instance;
    }
}
```

**Why `volatile` is needed for double-checked locking**: Without `volatile`, the JVM can reorder the object allocation and constructor call, allowing another thread to see a non-null reference to a partially constructed object.

### 12.3 Memory Barriers / Fences

`volatile` operations insert **memory barriers**:
- **StoreStore** before a volatile write: All prior stores are flushed.
- **StoreLoad** after a volatile write: The write is visible before subsequent loads.
- **LoadLoad** after a volatile read: Subsequent loads see up-to-date values.
- **LoadStore** after a volatile read: Subsequent stores happen after the volatile read.

### 12.4 `final` Field Semantics

```java
class SafePublication {
    private final int x;
    private final List<String> items;

    SafePublication(int x) {
        this.x = x;
        this.items = new ArrayList<>();
        this.items.add("A");
        // After constructor completes, any thread that sees a reference
        // to this object is GUARANTEED to see x=42 and items containing "A"
    }
}
```

- `final` fields are **safely published** without `volatile` or synchronization.
- The object must be **properly constructed** (no `this` escape during construction).

---

## 13. ThreadLocal & InheritableThreadLocal

### 13.1 `ThreadLocal<T>`

Each thread gets its own independent copy of the variable.

```java
// Common: SimpleDateFormat is not thread-safe
private static final ThreadLocal<SimpleDateFormat> formatter =
    ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd"));

// Usage
String date = formatter.get().format(new Date());

// CRITICAL: Always remove in thread pools to prevent memory leaks
try {
    formatter.get().format(someDate);
} finally {
    formatter.remove(); // Prevents memory leaks in thread pools
}
```

### 13.2 Memory Leak in Thread Pools

```
Thread → ThreadLocalMap → Entry(WeakReference<ThreadLocal>, Value)
```

- The `ThreadLocal` key is a **weak reference** → can be GC'd.
- But the **value** is a **strong reference** → stays in memory.
- In thread pools, threads are reused → values accumulate → **memory leak**.
- **Always call `remove()`** when done.

### 13.3 `InheritableThreadLocal`

Child threads inherit the parent's value at creation time.

```java
InheritableThreadLocal<String> context = new InheritableThreadLocal<>();
context.set("parent-value");

new Thread(() -> {
    System.out.println(context.get()); // "parent-value"
}).start();
```

- **Does NOT work with thread pools** — threads are reused, not newly created.
- For thread pools, use **Scoped Values** (Java 21+) or manual propagation.

---

## 14. Virtual Threads (Project Loom — Java 21+)

### 14.1 Platform Threads vs. Virtual Threads

| Aspect | Platform Threads | Virtual Threads |
|--------|-----------------|-----------------|
| Mapping | 1:1 with OS threads | M:N (many virtual threads on few carrier threads) |
| Memory | ~1MB stack per thread | ~few KB initially, grows on demand |
| Creation cost | Expensive | Cheap (microseconds) |
| Max count | Typically thousands | Millions |
| Scheduling | OS scheduler | JVM scheduler (work-stealing `ForkJoinPool`) |
| Blocking | Blocks OS thread | Unmounts from carrier thread |
| Use case | CPU-bound, long-running tasks | I/O-bound, high-concurrency tasks |

### 14.2 Creating Virtual Threads

```java
// Method 1: Thread.startVirtualThread()
Thread vt = Thread.startVirtualThread(() -> {
    System.out.println("Running on: " + Thread.currentThread());
});

// Method 2: Thread.ofVirtual()
Thread vt2 = Thread.ofVirtual()
    .name("my-virtual-thread")
    .start(() -> doWork());

// Method 3: Unstarted
Thread vt3 = Thread.ofVirtual()
    .name("vt-", 0)   // "vt-0", "vt-1", etc.
    .unstarted(() -> doWork());
vt3.start();

// Method 4: ExecutorService (PREFERRED for production)
try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
    // Each submitted task gets its own virtual thread
    List<Future<String>> futures = IntStream.range(0, 100_000)
        .mapToObj(i -> executor.submit(() -> fetchUrl(urls.get(i))))
        .toList();

    for (Future<String> f : futures) {
        System.out.println(f.get());
    }
} // AutoCloseable — awaits termination
```

### 14.3 How Virtual Threads Work Internally

```
Virtual Thread (mounted)  →  Carrier Thread (platform thread)  →  OS Thread
        │
    blocking I/O
        │
Virtual Thread (unmounted / parked)
        │
    Carrier thread is FREE to run other virtual threads
        │
    I/O completes → Virtual thread remounted on (possibly different) carrier
```

- **Carrier threads**: Platform threads in a `ForkJoinPool` (default size = available processors).
- **Mounting**: Virtual thread runs on a carrier.
- **Unmounting**: On blocking I/O, the virtual thread **yields** the carrier — carrier runs another virtual thread.
- **Pinning**: Virtual thread is stuck on carrier when:
  - Inside a `synchronized` block (use `ReentrantLock` instead)
  - Inside a native method / foreign function

### 14.4 Pinning Problem

```java
// BAD: synchronized causes pinning — carrier thread blocked
synchronized (lock) {
    socket.read(); // Virtual thread CANNOT unmount — carrier is pinned
}

// GOOD: ReentrantLock allows unmounting
lock.lock();
try {
    socket.read(); // Virtual thread CAN unmount — carrier is free
} finally {
    lock.unlock();
}
```

Detect pinning: `-Djdk.tracePinnedThreads=full` or `-Djdk.tracePinnedThreads=short`.

### 14.5 Best Practices for Virtual Threads

- **Don't pool virtual threads** — create a new one per task.
- **Replace `synchronized` with `ReentrantLock`** to avoid pinning.
- **Use them for I/O-bound tasks** — not CPU-bound.
- **Avoid `ThreadLocal` for expensive objects** — millions of virtual threads = millions of copies.
- **Use `Executors.newVirtualThreadPerTaskExecutor()`** — integrates with existing `ExecutorService` code.
- Virtual threads are **always daemon threads**.
- Virtual threads **cannot** have their priority changed.

### 14.6 Practical Example: High-Concurrency HTTP Server

```java
try (var serverSocket = new ServerSocket(8080)) {
    try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
        while (true) {
            Socket socket = serverSocket.accept();
            executor.submit(() -> handleRequest(socket)); // Millions of concurrent connections
        }
    }
}

void handleRequest(Socket socket) {
    try (socket;
         var in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
         var out = new PrintWriter(socket.getOutputStream(), true)) {

        String request = in.readLine();
        // Blocking I/O is fine — virtual thread unmounts
        String response = queryDatabase(request);
        out.println(response);
    } catch (IOException e) {
        // handle
    }
}
```

---

## 15. Structured Concurrency (JEP 453 — Java 21+)

### 15.1 The Problem with Unstructured Concurrency

```java
// Unstructured: What if fetchUser fails but fetchOrder is still running?
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
Future<User> userFuture = executor.submit(() -> fetchUser(id));
Future<Order> orderFuture = executor.submit(() -> fetchOrder(id));
// If fetchUser throws, fetchOrder keeps running — leaked work
```

### 15.2 `StructuredTaskScope` (Preview API)

Treats concurrent tasks as a **unit of work** — if one fails, all are cancelled.

```java
import java.util.concurrent.StructuredTaskScope;

// ShutdownOnFailure: Cancel all tasks if any fails
Response handle() throws ExecutionException, InterruptedException {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        Subtask<User> user = scope.fork(() -> fetchUser());
        Subtask<Order> order = scope.fork(() -> fetchOrder());

        scope.join();            // Wait for all tasks
        scope.throwIfFailed();   // Propagate first failure

        // Both succeeded
        return new Response(user.get(), order.get());
    }
}

// ShutdownOnSuccess: Return first successful result, cancel the rest
String fetchFastest() throws ExecutionException, InterruptedException {
    try (var scope = new StructuredTaskScope.ShutdownOnSuccess<String>()) {
        scope.fork(() -> fetchFromPrimary());
        scope.fork(() -> fetchFromMirror());

        scope.join();
        return scope.result();  // First successful result
    }
}
```

### 15.3 Benefits

- **Lifetime management**: Child tasks cannot outlive the parent scope.
- **Cancellation propagation**: Failure in one task cancels siblings.
- **Observability**: Thread dumps show structured parent-child relationships.
- **Error handling**: Exceptions are aggregated in a controlled way.

---

## 16. Scoped Values (JEP 446 — Java 21+)

### 16.1 Replacement for ThreadLocal in Virtual Threads

```java
import java.lang.ScopedValue;

// Declare a scoped value
private static final ScopedValue<String> USER = ScopedValue.newInstance();

// Bind and run
ScopedValue.where(USER, "alice").run(() -> {
    System.out.println(USER.get()); // "alice"
    processRequest();               // All code in this scope sees "alice"
});

// Callable version
String result = ScopedValue.where(USER, "bob").call(() -> {
    return fetchDataFor(USER.get());
});
```

### 16.2 `ScopedValue` vs `ThreadLocal`

| Aspect | `ThreadLocal` | `ScopedValue` |
|--------|--------------|---------------|
| Mutability | Mutable (`set()`, `get()`) | Immutable within scope |
| Lifetime | Until `remove()` | Automatic — bounded by scope |
| Inheritance | `InheritableThreadLocal` (copies value) | Automatic with `StructuredTaskScope` (shared, no copy) |
| Virtual threads | Problematic (memory, pooling) | Designed for virtual threads |
| Memory leaks | Common if `remove()` forgotten | Impossible — scoped |

---

## 17. Reactive Streams & Flow API (Java 9+)

### 17.1 The `java.util.concurrent.Flow` Interfaces

```java
@FunctionalInterface
public static interface Flow.Publisher<T> {
    void subscribe(Flow.Subscriber<? super T> subscriber);
}

public static interface Flow.Subscriber<T> {
    void onSubscribe(Flow.Subscription subscription);
    void onNext(T item);
    void onError(Throwable throwable);
    void onComplete();
}

public static interface Flow.Subscription {
    void request(long n);    // Request n items (backpressure)
    void cancel();
}

public static interface Flow.Processor<T, R> extends Flow.Subscriber<T>, Flow.Publisher<R> {
    // Both subscriber and publisher — transformation stage
}
```

### 17.2 `SubmissionPublisher<T>` (Built-in Implementation)

```java
SubmissionPublisher<String> publisher = new SubmissionPublisher<>();

// Custom subscriber
Flow.Subscriber<String> subscriber = new Flow.Subscriber<>() {
    private Flow.Subscription subscription;

    @Override
    public void onSubscribe(Flow.Subscription subscription) {
        this.subscription = subscription;
        subscription.request(1); // Request first item (backpressure)
    }

    @Override
    public void onNext(String item) {
        System.out.println("Received: " + item);
        subscription.request(1); // Request next item
    }

    @Override
    public void onError(Throwable throwable) {
        throwable.printStackTrace();
    }

    @Override
    public void onComplete() {
        System.out.println("Done");
    }
};

publisher.subscribe(subscriber);
publisher.submit("Hello");
publisher.submit("World");
publisher.close(); // Triggers onComplete
```

### 17.3 Backpressure

- **Pull-based**: Subscriber controls the rate via `request(n)`.
- **`request(Long.MAX_VALUE)`**: Effectively unbounded (no backpressure).
- `SubmissionPublisher` buffers items and blocks/drops if subscriber can't keep up (configurable).

---

## 18. StampedLock (Java 8+)

### 18.1 Three Lock Modes

```java
StampedLock lock = new StampedLock();

// 1. Write lock (exclusive)
long stamp = lock.writeLock();
try {
    x = newX;
    y = newY;
} finally {
    lock.unlockWrite(stamp);
}

// 2. Read lock (shared, pessimistic)
long stamp = lock.readLock();
try {
    return Math.sqrt(x * x + y * y);
} finally {
    lock.unlockRead(stamp);
}

// 3. Optimistic read (no actual lock — just a validation)
long stamp = lock.tryOptimisticRead();
double currentX = x, currentY = y;  // Read fields
if (!lock.validate(stamp)) {         // Check if a write occurred since stamp
    // Fallback to pessimistic read
    stamp = lock.readLock();
    try {
        currentX = x;
        currentY = y;
    } finally {
        lock.unlockRead(stamp);
    }
}
return Math.sqrt(currentX * currentX + currentY * currentY);
```

### 18.2 Lock Conversion

```java
// Read → Write upgrade (unlike ReentrantReadWriteLock, this works!)
long stamp = lock.readLock();
try {
    while (x == 0.0) {
        long writeStamp = lock.tryConvertToWriteLock(stamp);
        if (writeStamp != 0L) {
            stamp = writeStamp;
            x = newX;
            break;
        } else {
            lock.unlockRead(stamp);
            stamp = lock.writeLock();
        }
    }
} finally {
    lock.unlock(stamp); // Works for any lock mode
}
```

**Key characteristics:**
- **NOT reentrant** — do not attempt to re-acquire from the same thread.
- **Does NOT implement `Lock`** interface — cannot be used with `Condition`.
- **Optimistic reads** have zero overhead when there's no write contention.
- Best for read-heavy scenarios where reads vastly outnumber writes.

---

## 19. Common Concurrency Patterns

### 19.1 Singleton Patterns

```java
// 1. Enum Singleton (recommended by Joshua Bloch)
public enum Singleton {
    INSTANCE;
    public void doSomething() { /* ... */ }
}

// 2. Static holder idiom (lazy, thread-safe, no synchronization)
public class Singleton {
    private Singleton() {}
    private static class Holder {
        static final Singleton INSTANCE = new Singleton();
    }
    public static Singleton getInstance() { return Holder.INSTANCE; }
}

// 3. Double-checked locking with volatile
public class Singleton {
    private static volatile Singleton instance;
    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

### 19.2 Thread-Safe Lazy Initialization

```java
// Using AtomicReference with CAS
private final AtomicReference<ExpensiveObject> ref = new AtomicReference<>();

public ExpensiveObject getOrCreate() {
    ExpensiveObject existing = ref.get();
    if (existing != null) return existing;

    ExpensiveObject newObj = new ExpensiveObject();
    if (ref.compareAndSet(null, newObj)) {
        return newObj; // We won the race
    }
    return ref.get(); // Someone else initialized first
}
```

### 19.3 Thread-Confinement

- **Stack confinement**: Variables declared inside a method (local variables) are thread-confined.
- **ThreadLocal confinement**: Per-thread storage.
- **Ad-hoc confinement**: Convention-based (fragile, not enforced).

### 19.4 Immutability Pattern

```java
// Immutable objects are inherently thread-safe
public final class ImmutablePoint {
    private final int x;
    private final int y;

    public ImmutablePoint(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() { return x; }
    public int getY() { return y; }

    public ImmutablePoint translate(int dx, int dy) {
        return new ImmutablePoint(x + dx, y + dy); // Return new instance
    }
}
```

### 19.5 Producer-Consumer with Virtual Threads

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    BlockingQueue<String> queue = new LinkedBlockingQueue<>(1000);
    int numProducers = 10;
    int numConsumers = 5;

    // Producers
    for (int i = 0; i < numProducers; i++) {
        executor.submit(() -> {
            while (!Thread.currentThread().isInterrupted()) {
                queue.put(produceItem());
            }
        });
    }

    // Consumers
    for (int i = 0; i < numConsumers; i++) {
        executor.submit(() -> {
            while (!Thread.currentThread().isInterrupted()) {
                String item = queue.take();
                processItem(item);
            }
        });
    }
}
```

---

## 20. Common Concurrency Problems & Pitfalls

### 20.1 Deadlock

All four Coffman conditions must hold simultaneously:

1. **Mutual exclusion**: Resources cannot be shared.
2. **Hold and wait**: Thread holds one resource while waiting for another.
3. **No preemption**: Resources cannot be forcibly taken away.
4. **Circular wait**: Circular chain of threads waiting for each other.

```java
// DEADLOCK EXAMPLE
Object lockA = new Object(), lockB = new Object();

// Thread 1: lockA → lockB
new Thread(() -> { synchronized(lockA) { synchronized(lockB) { /* ... */ } } }).start();

// Thread 2: lockB → lockA
new Thread(() -> { synchronized(lockB) { synchronized(lockA) { /* ... */ } } }).start();

// SOLUTION: Consistent lock ordering
// Always acquire lockA before lockB (or use lock ordering by System.identityHashCode)
```

**Detection**: `jstack <pid>` shows deadlock info. `ThreadMXBean.findDeadlockedThreads()`.

### 20.2 Livelock

Threads are active (not blocked) but keep reacting to each other without making progress.

```java
// Two threads keep yielding to each other
while (otherThread.isWaiting()) {
    yield(); // Both threads keep yielding — no progress
}
```

**Solution**: Introduce random backoff or asymmetric behavior.

### 20.3 Starvation

A thread is perpetually denied access to resources (e.g., low-priority thread never gets the lock due to high-priority threads).

**Solutions**: Fair locks (`new ReentrantLock(true)`), fair semaphores.

### 20.4 Race Condition

**Check-then-act** and **read-modify-write** patterns without proper synchronization.

```java
// RACE CONDITION: check-then-act
if (!map.containsKey(key)) {     // Check
    map.put(key, computeValue()); // Act — another thread may have put between check and act
}

// SOLUTION: atomic operations
map.computeIfAbsent(key, k -> computeValue());
```

### 20.5 Thread Leaks

Threads that are started but never properly shut down, accumulating over time.

```java
// Always use try-with-resources for ExecutorService (Java 19+)
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    // tasks...
} // Auto-shutdown

// Or use proper shutdown pattern (pre-Java 19)
```

### 20.6 False Sharing

When two threads modify different variables that reside on the **same CPU cache line** (typically 64 bytes), causing unnecessary cache invalidation.

```java
// BAD: likely false sharing
class Counters {
    volatile long counter1;
    volatile long counter2; // Same cache line as counter1
}

// SOLUTION: Padding (or @Contended annotation)
class Counters {
    @jdk.internal.vm.annotation.Contended
    volatile long counter1;

    @jdk.internal.vm.annotation.Contended
    volatile long counter2;
}
// Enable with: -XX:-RestrictContended
```

`LongAdder` internally uses `@Contended` to avoid false sharing among its cells.

---

## 21. Best Practices & Interview Tips

### 21.1 General Best Practices

1. **Prefer higher-level concurrency utilities** over `synchronized`, `wait/notify`.
2. **Use immutable objects** — they are inherently thread-safe.
3. **Minimize lock scope** — hold locks for the shortest time possible.
4. **Prefer `ReentrantLock` over `synchronized`** when you need tryLock, fairness, or multiple conditions.
5. **Use `concurrent` collections** instead of synchronizing standard collections.
6. **Avoid `Executors.newFixedThreadPool()`** in production — use `ThreadPoolExecutor` directly for control over queue size and rejection policy.
7. **Always name your threads** — invaluable for debugging.
8. **Use virtual threads for I/O-bound work** — platform threads for CPU-bound.
9. **Never call `Thread.stop()`, `Thread.suspend()`, `Thread.resume()`** — all deprecated, can leave objects in inconsistent state.
10. **Prefer `ExecutorService.submit()` over `Thread.start()`** — better lifecycle management and error handling.

### 21.2 Sizing Thread Pools

```
CPU-bound tasks:
    threads = N_cpu + 1    (where N_cpu = Runtime.getRuntime().availableProcessors())

I/O-bound tasks:
    threads = N_cpu × U_cpu × (1 + W/C)
    where:
        U_cpu = target CPU utilization (0 < U_cpu ≤ 1)
        W/C   = ratio of wait time to compute time

Example: 8 cores, 80% utilization, tasks wait 5x more than they compute:
    threads = 8 × 0.8 × (1 + 5) = 38.4 ≈ 38
```

### 21.3 Critical Interview Questions to Remember

| Question | Key Answer Points |
|----------|-------------------|
| `volatile` vs `synchronized` | `volatile` = visibility + ordering, no atomicity; `synchronized` = visibility + ordering + atomicity + mutual exclusion |
| Why is `String` immutable? | Thread safety, string pool, hashcode caching, security |
| `ConcurrentHashMap` vs `Hashtable` | Segment/CAS-based vs. single lock; null keys/values disallowed in both `CHM` and `Hashtable` |
| `CountDownLatch` vs `CyclicBarrier` | One-shot vs. reusable; event-waiting vs. peer-waiting |
| `Runnable` vs `Callable` | void vs return value; no checked exceptions vs. throws Exception |
| Thread pool lifecycle | RUNNING → SHUTDOWN → STOP → TIDYING → TERMINATED |
| What is the common `ForkJoinPool`? | Shared pool for parallel streams and `CompletableFuture`; starving it blocks all parallel operations |
| `thenApply` vs `thenCompose` | map vs flatMap; synchronous transform vs async chaining |
| `sleep()` vs `wait()` | `sleep` doesn't release lock; `wait` releases monitor; `sleep` is static |
| Virtual threads vs platform threads | M:N scheduling, cheap, don't pool them, avoid `synchronized` (pinning) |

---

## 22. Quick-Reference Cheat Sheet

### Thread-Safe Singleton

```java
public enum Singleton { INSTANCE; }
```

### Atomic Counter (High Contention)

```java
LongAdder counter = new LongAdder();
counter.increment();
long total = counter.sum();
```

### Async Pipeline

```java
CompletableFuture.supplyAsync(() -> fetchUser(id))
    .thenCompose(user -> fetchOrders(user.getId()))
    .thenApply(orders -> buildReport(orders))
    .exceptionally(ex -> fallbackReport())
    .thenAccept(this::sendEmail);
```

### Virtual Thread HTTP Handler

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> handleRequest(socket));
}
```

### Structured Concurrency

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var user = scope.fork(() -> fetchUser());
    var order = scope.fork(() -> fetchOrder());
    scope.join().throwIfFailed();
    return new Response(user.get(), order.get());
}
```

### Proper Lock Usage

```java
ReentrantLock lock = new ReentrantLock();
lock.lock();
try { /* critical section */ } finally { lock.unlock(); }
```

### `ConcurrentHashMap` Atomic Update

```java
map.compute(key, (k, v) -> v == null ? 1 : v + 1);
map.merge(key, 1, Integer::sum);
```

### Timeout Pattern

```java
CompletableFuture.supplyAsync(() -> slowOperation())
    .orTimeout(5, TimeUnit.SECONDS)
    .exceptionally(ex -> defaultValue());
```

---

> **Note**: These notes cover Java 8 through Java 21+ features. Interview depth typically focuses on the Executor Framework, `CompletableFuture`, `ConcurrentHashMap` internals, the Java Memory Model, `volatile` semantics, and increasingly, Virtual Threads (Project Loom). Be prepared to write code for any pattern shown above, and be ready to explain the "why" behind each mechanism — not just the "how."
