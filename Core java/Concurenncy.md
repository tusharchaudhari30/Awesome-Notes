# Java Concurrency & Threads — Interview Notes

Concurrency lets multiple tasks advance independently, while parallelism executes them at the same time on different cores; Java offers both low-level primitives (<code>Thread</code>, <code>synchronized</code>, <code>wait/notify</code>) and high-level frameworks (<code>ExecutorService</code>, <code>CompletableFuture</code>, concurrent collections) to build correct, scalable systems.

---

## Mental model

- Concurrency vs parallelism: concurrent code interleaves progress; parallel code runs truly simultaneously; correctness must not depend on timing.
- Memory model: use happens-before rules via <code>synchronized</code>, <code>Lock</code>, <code>volatile</code>, or thread-safe classes to ensure visibility and ordering of writes.
- Typical bugs: race conditions (missing atomicity), deadlock (cyclic lock waits), livelock (threads react but make no progress), starvation (unfair scheduling or lock acquisition).

---

## Core building blocks

### Thread & Runnable

- Runnable describes a task with <code>void run()</code>; a <code>Thread</code> executes it; prefer pools over raw threads for scalability.
- Control with <code>interrupt</code> and cooperative checks; never use deprecated <code>stop/suspend/resume</code>.

Methods quick table

| Type     | Key methods                                                                                                                                                                                                                              |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Thread   | <code>start</code>, <code>join</code>, <code>sleep</code>, <code>interrupt</code>, <code>isInterrupted</code>, <code>interrupted</code>, <code>currentThread</code>, <code>getState</code>, <code>setDaemon</code>, <code>setName</code> |
| Runnable | <code>run</code>                                                                                                                                                                                                                         |

Example: extend Thread vs implement Runnable

```java
// Prefer: task logic in Runnable
class Worker implements Runnable {
  public void run() { /* work */ }
}
Thread t = new Thread(new Worker(), "worker-1");
t.start();

// Anti-example uniqueness: extending Thread couples task and thread
class BadWorker extends Thread {
  public void run() { /* work */ }
}
new BadWorker().start();
```

Example: cooperative interrupt (two scenarios)

```java
class InterruptDemo {
  public static void main(String[] args) throws Exception {
    Thread t = new Thread(() -> {
      try {
        while (!Thread.currentThread().isInterrupted()) {
          // do work
          Thread.sleep(100);       // Scenario 2: InterruptedException path
        }
      } catch (InterruptedException ie) {
        // interrupted during blocking call; status cleared here
        Thread.currentThread().interrupt(); // re-set if outer loops need it
      }
    });
    t.start();
    Thread.sleep(300);
    t.interrupt();                 // Scenario 1: sets interrupt flag if running
    t.join();
  }
}
```

---

### Callable, Future, ExecutorService

- <code>Callable<V></code> produces a value or throws; <code>Future</code> models the pending result; <code>ExecutorService</code> schedules and manages tasks.

Methods quick table

| Type            | Key methods                                                                                                                                                               |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ExecutorService | <code>execute</code>, <code>submit</code>, <code>invokeAll</code>, <code>invokeAny</code>, <code>shutdown</code>, <code>shutdownNow</code>, <code>awaitTermination</code> |
| Future          | <code>get</code>, <code>get(timeout, unit)</code>, <code>cancel</code>, <code>isDone</code>, <code>isCancelled</code>                                                     |
| Executors       | <code>newFixedThreadPool</code>, <code>newCachedThreadPool</code>, <code>newSingleThreadExecutor</code>, <code>newScheduledThreadPool</code>                              |

Example: invokeAll with timeout and cancellations

```java
ExecutorService pool = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
List<Callable<Long>> tasks = List.of(
  () -> compute("A"),
  () -> compute("B"),
  () -> compute("C")
);
List<Future<Long>> fs = pool.invokeAll(tasks, 2, TimeUnit.SECONDS); // cancels unfinished
long sum = 0;
for (Future<Long> f : fs) {
  if (!f.isCancelled()) sum += f.get(); // safe: already done or cancelled
}
pool.shutdown();
```

---

### CompletableFuture

- Asynchronous pipeline without blocking; chain with <code>thenApply</code>, compose with <code>thenCompose</code>, combine with <code>thenCombine</code>; handle failures with <code>exceptionally</code>/<code>handle</code>.
- Cancellation marks the future as cancelled but does not interrupt running work by default.

Methods quick table

| Category  | Methods                                                                                         |
| --------- | ----------------------------------------------------------------------------------------------- |
| Create    | <code>supplyAsync</code>, <code>runAsync</code> (optionally with custom executor)               |
| Transform | <code>thenApply</code>, <code>thenCompose</code>, <code>thenAccept</code>, <code>thenRun</code> |
| Combine   | <code>thenCombine</code>, <code>allOf</code>, <code>anyOf</code>                                |
| Errors    | <code>exceptionally</code>, <code>handle</code>, <code>whenComplete</code>                      |
| Manual    | <code>complete</code>, <code>completeExceptionally</code>, <code>cancel</code>                  |

Example: compose vs apply

```java
CompletableFuture<User> f =
  CompletableFuture.supplyAsync(() -> loadUser(id))
    .thenCompose(u -> CompletableFuture.supplyAsync(() -> enrich(u))) // flatten
    .exceptionally(ex -> fallbackUser());
```

---

### Intrinsic locking & wait/notify

- <code>synchronized</code> gives mutual exclusion and happens-before; <code>wait</code> releases the monitor and suspends; <code>notify</code>/<code>notifyAll</code> wake waiters; always call in a loop to guard against spurious wakeups.

Methods quick table

| Type            | Key methods                                                                                             |
| --------------- | ------------------------------------------------------------------------------------------------------- |
| Object monitor  | <code>wait()</code>, <code>wait(timeout, nanos)</code>, <code>notify()</code>, <code>notifyAll()</code> |
| Thread (timing) | <code>sleep(millis)</code> (does not release locks)                                                     |

Example: bounded buffer using wait/notify

```java
class BoundedQueue<T> {
  private final Queue<T> q = new ArrayDeque<>();
  private final int cap;
  BoundedQueue(int cap) { this.cap = cap; }

  public synchronized void put(T x) throws InterruptedException {
    while (q.size() == cap) wait();
    q.add(x);
    notifyAll();
  }
  public synchronized T take() throws InterruptedException {
    while (q.isEmpty()) wait();
    T x = q.remove();
    notifyAll();
    return x;
  }
}
```

---

### Lock API (programmatic locks)

- <code>ReentrantLock</code> adds <code>tryLock</code> and timed lock, fairness, multiple conditions; <code>ReadWriteLock</code> separates readers/writers.

Methods quick table

| Type          | Key methods                                                                                                                  |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| ReentrantLock | <code>lock</code>, <code>unlock</code>, <code>tryLock</code>, <code>tryLock(timeout, unit)</code>, <code>newCondition</code> |
| ReadWriteLock | <code>readLock</code>, <code>writeLock</code>                                                                                |
| Condition     | <code>await</code>, <code>await(timeout, unit)</code>, <code>signal</code>, <code>signalAll</code>                           |

Example: avoid deadlock with timed tryLock

```java
boolean acquired = false;
if (lock1.tryLock(100, TimeUnit.MILLISECONDS)) {
  try {
    if (lock2.tryLock(100, TimeUnit.MILLISECONDS)) {
      try { /* critical section */ }
      finally { lock2.unlock(); acquired = true; }
    }
  } finally { lock1.unlock(); }
}
if (!acquired) { /* fallback / retry */ }
```

---

### Volatile, atomics, and CAS

- <code>volatile</code> ensures visibility and ordering for that field, not atomicity; use <code>AtomicInteger</code>/<code>AtomicLong</code> for lock-free atomic updates; <code>LongAdder</code> scales better under contention.

Methods quick table

| Type          | Key methods                                                                                                                                     |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| AtomicInteger | <code>get</code>, <code>set</code>, <code>incrementAndGet</code>, <code>addAndGet</code>, <code>compareAndSet</code>, <code>updateAndGet</code> |
| LongAdder     | <code>increment</code>, <code>add</code>, <code>sum</code>                                                                                      |

Example: volatile counter bug vs atomic fix

```java
class Bad {
  volatile int count;                 // visibility only
  void inc() { count++; }             // not atomic: r/m/w interleaving
}

class Good {
  final AtomicInteger count = new AtomicInteger();
  void inc() { count.incrementAndGet(); } // atomic
}
```

CAS loop uniqueness

```java
void casInc(AtomicInteger ai) {
  int prev, next;
  do {
    prev = ai.get();
    next = prev + 1;
  } while (!ai.compareAndSet(prev, next));
}
```

---

### Concurrent collections & blocking queues

- Prefer <code>ConcurrentHashMap</code> with atomic operations (<code>compute</code>, <code>merge</code>, <code>putIfAbsent</code>), and <code>BlockingQueue</code> (<code>put/take</code>, timed <code>offer/poll</code>) for producer–consumer.

Methods quick table

| Type              | Key methods                                                                                                                                                      |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ConcurrentHashMap | <code>compute</code>, <code>computeIfAbsent</code>, <code>merge</code>, <code>putIfAbsent</code>, <code>forEach</code>, <code>search</code>, <code>reduce</code> |
| BlockingQueue     | <code>put</code>, <code>take</code>, <code>offer</code>, <code>poll</code>, <code>offer/poll(timeout, unit)</code>                                               |
| Others            | <code>ConcurrentLinkedQueue</code> (non-blocking), <code>CopyOnWriteArrayList</code> (read-mostly), <code>ConcurrentSkipListMap</code> (sorted)                  |

Example: frequency count with compute/merge

```java
ConcurrentHashMap<String, LongAdder> freq = new ConcurrentHashMap<>();
Stream.of(words).forEach(w -> freq.computeIfAbsent(w, k -> new LongAdder()).increment());
// Or merging longs
Map<String, Long> counts = new ConcurrentHashMap<>();
counts.merge(w, 1L, Long::sum);
```

Producer–consumer with poison pill

```java
BlockingQueue<Path> q = new LinkedBlockingQueue<>(100);
Path POISON = Path.of("__POISON__");

// Producer
new Thread(() -> {
  try (Stream<Path> s = Files.walk(root)) {
    s.filter(Files::isRegularFile).forEach(p -> { try { q.put(p); } catch (InterruptedException ignored) { Thread.currentThread().interrupt(); }});
  } catch (IOException e) { /* log */ }
  try { q.put(POISON); } catch (InterruptedException ignored) { Thread.currentThread().interrupt(); }
}).start();

// Consumer
new Thread(() -> {
  try {
    for (;;) {
      Path p = q.take();
      if (p.equals(POISON)) { q.put(POISON); break; } // fan-out friendly
      process(p);
    }
  } catch (InterruptedException ie) { Thread.currentThread().interrupt(); }
}).start();
```

---

### Synchronizers

- Coordinate phases and gates without manual wait/notify.

Methods quick table

| Type           | Usage                  | Key methods                                                                                 |
| -------------- | ---------------------- | ------------------------------------------------------------------------------------------- |
| CountDownLatch | start/done gates       | <code>await</code>, <code>countDown</code>                                                  |
| CyclicBarrier  | rendezvous             | <code>await</code> (+ optional barrier action), <code>reset</code>                          |
| Phaser         | dynamic phases/parties | <code>register</code>, <code>arriveAndAwaitAdvance</code>, <code>arriveAndDeregister</code> |
| Semaphore      | permits/limits         | <code>acquire</code>, <code>release</code>, <code>tryAcquire</code>                         |

Example: start gate and completion gate

```java
int n = 8;
CountDownLatch start = new CountDownLatch(1);
CountDownLatch done  = new CountDownLatch(n);
for (int i = 0; i < n; i++) {
  new Thread(() -> {
    try {
      start.await();
      work();
    } catch (InterruptedException ie) {
      Thread.currentThread().interrupt();
    } finally { done.countDown(); }
  }).start();
}
start.countDown();     // go
done.await();          // all finished
```

---

### Fork/Join & parallel streams

- Prefer high-level data-parallel APIs: <code>parallelStream()</code>, <code>Arrays.parallelSort</code>, etc.; avoid shared mutable state in lambdas.

Example: safe parallel reduction

```java
long count = words.parallelStream()
    .filter(w -> w.length() > 12)
    .count(); // stateless, associative/commutative terminal op
```

---

### ThreadLocal

- Per-thread state without passing through call chains; beware reuse by thread pools (always <code>remove</code>).

Methods quick table

| Type           | Key methods                                                                       |
| -------------- | --------------------------------------------------------------------------------- |
| ThreadLocal<T> | <code>withInitial</code>, <code>get</code>, <code>set</code>, <code>remove</code> |

Example: per-thread connection

```java
class Db {
  static final ThreadLocal<Connection> CONN =
      ThreadLocal.withInitial(() -> open());
  static Result query(String sql) throws SQLException {
    return CONN.get().createStatement().executeQuery(sql);
  }
  static void close() throws SQLException { CONN.get().close(); CONN.remove(); }
}
```

---

## Lifecycle & coordination

### States, joining, sleeping, interruption

- States: NEW → RUNNABLE (READY/RUNNING) → BLOCKED/WAITING/TIMED_WAITING → TERMINATED; use <code>join</code> or <code>join(timeout)</code> to await completion; <code>sleep</code> pauses without releasing locks.

Methods quick table

| Purpose   | Methods                                                                                    |
| --------- | ------------------------------------------------------------------------------------------ |
| Join      | <code>join</code>, <code>join(timeout)</code>                                              |
| Sleep     | <code>sleep(millis)</code>, <code>sleep(millis, nanos)</code>                              |
| Interrupt | <code>interrupt</code>, <code>isInterrupted</code>, <code>interrupted</code> (clears flag) |

Example: join both workers

```java
Thread a = new Thread(() -> runA(), "A");
Thread b = new Thread(() -> runB(), "B");
a.start(); b.start();
a.join(); b.join();
// Both done here
```

---

## Deadlock, livelock, starvation

- Deadlock: cyclic lock dependency; fix via global lock ordering, timed <code>tryLock</code>, or breaking cycles.
- Livelock: threads keep responding to each other without progress; introduce backoff/randomization.
- Starvation: unfair scheduling or lock policy; use fair locks or <code>notifyAll</code> appropriately.

Example: deadlock and fix

```java
final Object o1 = new Object(), o2 = new Object();

// Broken: opposite orders
Thread t1 = new Thread(() -> { synchronized (o1) { synchronized (o2) { /*...*/ } }});
Thread t2 = new Thread(() -> { synchronized (o2) { synchronized (o1) { /*...*/ } }});

// Fix: consistent ordering
void inOrder(Object a, Object b) {
  Object first = System.identityHashCode(a) < System.identityHashCode(b) ? a : b;
  Object second = first == a ? b : a;
  synchronized (first) { synchronized (second) { /*...*/ } }
}
```

---

## Differentiating cheat sheet

### Key comparisons

| Topic                                | A                                                    | B                                                                         | When to choose                                                         |
| ------------------------------------ | ---------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Runnable vs Callable                 | <code>void run()</code>, no result/checked exception | <code>V call()</code>, returns result/can throw                           | Use <code>Callable</code> when a result or checked exception is needed |
| Thread vs ExecutorService            | Manual thread lifecycle                              | Pools manage threads, queuing, lifecycle                                  | Prefer executors for scalability and control                           |
| synchronized vs ReentrantLock        | Simpler, implicit monitors, no timed/acquire         | <code>tryLock</code>, timeout, fairness, multiple <code>Condition</code>s | Use locks for timed, polled, or multiple-condition waits               |
| wait/notify vs BlockingQueue         | Manual coordination and loops                        | Built-in backpressure and blocking ops                                    | Prefer <code>BlockingQueue</code> for producer–consumer                |
| Future vs CompletableFuture          | Blocking <code>get</code>, manual composition        | Non-blocking chains, composition, callbacks                               | Use <code>CompletableFuture</code> for async pipelines                 |
| AtomicLong vs LongAdder              | CAS per update; contention hurts                     | Striped cells; fast under high contention                                 | Use <code>LongAdder</code> for hot counters                            |
| ConcurrentHashMap vs synchronizedMap | Lock-striping, atomic <code>compute/merge</code>     | Single lock, coarse-grained                                               | Prefer <code>ConcurrentHashMap</code> for concurrent updates           |
| parallelStream vs custom pool        | Data-parallel, easy but uses common pool             | Fine-grained control (pool size, scheduling)                              | Use parallel streams for CPU-bound, side-effect-free pipelines         |

---

## “Gotchas” and interview tips

- <code>volatile</code> does not make compound actions atomic; use atomics or locks for <code>x++</code>-style updates.
- Always guard <code>wait</code> with a loop; <code>sleep</code> does not release locks; <code>wait</code> does.
- Don’t swallow <code>InterruptedException</code>; decide to propagate, cancel, or re-set the flag.
- Avoid blocking or stateful lambdas in parallel streams; prefer stateless, associative reductions.
- Prefer library synchronizers (<code>CountDownLatch</code>, <code>Phaser</code>, <code>BlockingQueue</code>) over custom <code>wait/notify</code>.
- Use consistent lock ordering or <code>tryLock</code> with timeouts to prevent deadlocks.

---

## Mini method cheat sheets

### Executors and scheduling

| Method                                                       | Purpose                      |
| ------------------------------------------------------------ | ---------------------------- |
| <code>Executors.newFixedThreadPool(n)</code>                 | CPU-bound tasks (n ≈ cores)  |
| <code>Executors.newCachedThreadPool()</code>                 | Many short/IO-bound tasks    |
| <code>Executors.newSingleThreadExecutor()</code>             | Serialize task execution     |
| <code>ScheduledExecutorService.scheduleAtFixedRate</code>    | Periodic tasks (fixed rate)  |
| <code>ScheduledExecutorService.scheduleWithFixedDelay</code> | Periodic tasks (fixed delay) |

### BlockingQueue ops

| Full/empty | Throws               | Special value      | Blocks            | Times out                |
| ---------- | -------------------- | ------------------ | ----------------- | ------------------------ |
| Insert     | <code>add</code>     | <code>offer</code> | <code>put</code>  | <code>offer(t, u)</code> |
| Remove     | <code>remove</code>  | <code>poll</code>  | <code>take</code> | <code>poll(t, u)</code>  |
| Peek       | <code>element</code> | <code>peek</code>  | —                 | —                        |

---

## Difference-highlighting code gallery

Thread vs pool

```java
// Raw Thread (manual)
new Thread(() -> handle(req)).start();

// Pool (preferred)
ExecutorService pool = Executors.newFixedThreadPool(8);
pool.execute(() -> handle(req));
```

wait/notify vs BlockingQueue

```java
// Low-level (fragile)
synchronized (buf) {
  while (bufFull()) buf.wait();
  put(item);
  buf.notifyAll();
}

// High-level (robust)
queue.put(item);
```

thenApply vs thenCompose

```java
// Returns CompletableFuture<CompletableFuture<User>>
cf.thenApply(id -> loadAsync(id));
// Returns CompletableFuture<User>
cf.thenCompose(id -> loadAsync(id));
```

synchronized vs ReentrantLock

```java
// Intrinsic
synchronized (lock) { /* critical */ }

// Programmatic
lock.lock();
try { /* critical */ }
finally { lock.unlock(); }
```

AtomicLong vs LongAdder

```java
AtomicLong hits = new AtomicLong();
hits.incrementAndGet();

LongAdder adder = new LongAdder();
adder.increment(); long total = adder.sum();
```

parallelStream vs custom executor

```java
// Quick data-parallel
list.parallelStream().map(this::expensive).toList();

// Fine control (custom pool)
var pool = Executors.newWorkStealingPool();
CompletableFuture<List<R>> f = CompletableFuture
  .supplyAsync(() -> list.stream().map(this::expensive).toList(), pool);
```

---

## Quick practice prompts

- Implement a thread-safe counter five ways and benchmark: unsafe, <code>volatile</code>, <code>synchronized</code>, <code>AtomicInteger</code>, <code>ReentrantLock</code>.
- Build a pipeline with <code>CompletableFuture</code> that fetches, parses, and aggregates with error fallback.
- Convert a <code>wait/notify</code> queue to <code>BlockingQueue</code> with a poison pill and graceful shutdown.
- Demonstrate deadlock and fix with a total lock ordering or <code>tryLock</code>.

---

### Final reminders

- Prefer high-level concurrency utilities; reach for low-level primitives only when necessary.
- Design for cancellation, timeouts, and backpressure from the start.
- Test with stress and concurrency tools; non-determinism hides bugs.

[1](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_a6559622-e442-497c-b6c4-55a437ed9544/f771d900-48d0-42e7-a8f1-a711a230a316/Oracle-Press-for-Java-Khalid-Mughal-Vasily-Strelnikov-OCP-Oracle-Certified-Professional-Java-SE-17-Developer-Exam-1Z0-829-Programmer-s-Guide-Oracle-Press-2023.pdf)
[2](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_a6559622-e442-497c-b6c4-55a437ed9544/4e75dc53-0148-467a-9ec6-000c3a89b019/Cay-S.-Horstmann-Core-Java-for-the-Impatient-3rd-Edition-2022-Addison-Wesley-Professional-libgen.li.pdf)
