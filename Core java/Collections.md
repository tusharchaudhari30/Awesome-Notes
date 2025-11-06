The Java Collections Framework (JCF) provides standard interfaces and classes for storing, accessing, and manipulating groups of objects, plus algorithms like sorting, searching, and bulk operations. Core abstractions are Collection (List, Set, Queue/Deque) and Map, with generic types for type safety.

### Core interfaces

- Collection<E>: Root of collection hierarchy. Common ops: size, isEmpty, add, remove, contains, iterator, forEach, removeIf, toArray, stream, parallelStream.
- List<E>: Ordered, positional, allows duplicates; random access methods get/set, indexOf/lastIndexOf; listIterator for bidirectional edits.
- Set<E>: Unordered or ordered without duplicates.
- SortedSet<E>/NavigableSet<E>: Sorted order and neighbor navigation (lower, floor, ceiling, higher), views (headSet, tailSet, subSet).
- Queue<E>: Head-tail processing (typically FIFO); methods offer/poll/peek (non-throwing) vs add/remove/element (throwing).
- Deque<E>: Double-ended queue, stack/queue operations on both ends (addFirst/Last, removeFirst/Last, push/pop).
- Map<K,V>: Key→value associations, unique keys; views keySet, values, entrySet; compute/merge/getOrDefault/putIfAbsent.
- SortedMap<K,V>/NavigableMap<K,V>: Sorted by key with neighbor ops and range views.

### When to use what

- ArrayList vs LinkedList
  - ArrayList: Resizable array; O(1) random access; amortized O(1) append; O(n) insert/delete in middle; ideal for most lists.
  - LinkedList: Doubly-linked; O(1) insert/delete given iterator at position; O(n) random access; also implements Deque; useful for frequent head/tail operations with iterators.
- HashSet vs LinkedHashSet vs TreeSet
  - HashSet: Unordered; O(1) average add/contains/remove; requires good hashCode/equals.
  - LinkedHashSet: Insertion-order iteration; similar performance to HashSet with extra memory.
  - TreeSet: Sorted; O(log n) operations; requires natural ordering or Comparator; disallows null by design choice.
- HashMap vs LinkedHashMap vs TreeMap vs Hashtable
  - HashMap: Unordered; O(1) average ops; allows one null key and null values.
  - LinkedHashMap: Predictable iteration (insertion order or access order for LRU-like behavior).
  - TreeMap: Sorted by key; O(log n) operations; no null keys; optional Comparator.
  - Hashtable: Legacy synchronized map; no null keys/values; generally prefer ConcurrentHashMap or synchronized wrappers.
- PriorityQueue vs ArrayDeque
  - PriorityQueue: Heap-based; head is least/greatest by comparator; not FIFO; no random access by priority rank.
  - ArrayDeque: Fast non-blocking stack/queue; no nulls; generally faster than Stack/LinkedList for stack/queue roles.

### Ordering vs sorting

- Ordered means deterministic iteration (e.g., insertion order in LinkedHashMap).
- Sorted means comparator/natural order determines iteration order (e.g., TreeSet/TreeMap).
- Hash-based collections are neither ordered nor sorted.

### Essential APIs with examples

- Iteration
  - Enhanced for
    ```java
    for (String s : list) { System.out.println(s); }
    ```
  - Iterator (supports safe in-loop removal)
    ```java
    Iterator<String> it = list.iterator();
    while (it.hasNext()) {
      if (it.next().isBlank()) it.remove();
    }
    ```
  - forEach
    ```java
    collection.forEach(System.out::println);
    ```
- Bulk operations
  ```java
  list.addAll(List.of("a","b"));
  list.removeIf(s -> s.length() < 3);
  list.retainAll(Set.of("keep1","keep2"));
  ```
- Convert to arrays
  ```java
  String[] a1 = list.toArray(new String[0]);              // commonly used
  String[] a2 = list.toArray(String[]::new);             // generator form
  Object[] a3 = list.toArray();                          // Object[]
  ```
- Streams
  ```java
  long count = list.stream().filter(s -> s.length() > 10).count();
  list.parallelStream().map(String::toUpperCase).forEach(System.out::println);
  ```
- List specifics
  ```java
  List<String> arr = new ArrayList<>();
  arr.add("x"); arr.add(0, "y");
  arr.set(1, "z");
  int i = arr.indexOf("y");
  List<String> view = arr.subList(0, Math.min(arr.size(), 3)); // view backed
  ListIterator<String> it = arr.listIterator();
  it.add("new"); if (it.hasPrevious()) it.previous();
  ```
- Set specifics
  ```java
  Set<String> s = new HashSet<>(List.of("a","b","c"));
  boolean added = s.add("a"); // false, duplicate
  NavigableSet<Integer> ns = new TreeSet<>(List.of(10,20,30));
  Integer ceil = ns.ceiling(15); // 20
  SortedSet<Integer> range = ns.subSet(10, 30); // [10,30)
  ```
- Queue/Deque specifics
  ```java
  Queue<Integer> q = new ArrayDeque<>();
  q.offer(1); q.offer(2);
  Integer head = q.poll(); // 1 or null if empty
  Deque<String> d = new ArrayDeque<>();
  d.addFirst("a"); d.addLast("b");
  String last = d.removeLast();
  d.push("stack"); String top = d.pop();
  PriorityQueue<Integer> pq = new PriorityQueue<>();
  pq.add(5); pq.add(1); pq.add(3);
  int smallest = pq.poll(); // 1
  ```
- Map basics
  ```java
  Map<String,Integer> m = new HashMap<>();
  m.put("Alice", 1);
  m.putIfAbsent("Bob", 0);
  int val = m.getOrDefault("Carol", 42);
  m.compute("Alice", (k, v) -> v == null ? 1 : v + 1);
  m.merge("Bob", 1, Integer::sum); // counter pattern
  m.forEach((k,v) -> System.out.println(k + "=" + v));
  for (Map.Entry<String,Integer> e : m.entrySet()) {
    e.setValue(e.getValue() + 10);
  }
  ```
- Sorted/Navigable maps
  ```java
  NavigableMap<Integer,String> tm = new TreeMap<>();
  tm.put(10, "a"); tm.put(20, "b");
  Map.Entry<Integer,String> floor = tm.floorEntry(15); // (10,"a")
  SortedMap<Integer,String> sub = tm.subMap(10, 20);   // keys [10,20)
  ```
- Small, fixed, or unmodifiable collections
  ```java
  List<String> fixed = List.of("a","b","c"); // unmodifiable
  Set<Integer> primes = Set.of(2,3,5);
  Map<String,Integer> scores = Map.of("Peter",2, "Paul",3);
  // Make a modifiable copy:
  List<String> mod = new ArrayList<>(fixed);
  // Unmodifiable views:
  List<String> view = Collections.unmodifiableList(mod);
  // Checked views (debug generic type issues at runtime)
  List<String> checked = Collections.checkedList(new ArrayList<>(), String.class);
  ```
- Sorting and searching
  ```java
  List<String> names = new ArrayList<>(List.of("Bob","Ann","Eve"));
  Collections.sort(names); // natural order
  names.sort(Comparator.comparingInt(String::length).thenComparing(Comparator.naturalOrder()));
  int pos = Collections.binarySearch(names, "Eve"); // list must be sorted
  ```
- Comparators and Comparable
  ```java
  class Person implements Comparable<Person> {
    String name; int age;
    public int compareTo(Person other) { return name.compareTo(other.name); }
  }
  Comparator<Person> byAgeDesc = Comparator.comparingInt((Person p) -> p.age).reversed();
  ```
- Equality and hashing correctness
  - For HashSet/HashMap keys, implement equals and hashCode consistently.
  - For TreeSet/TreeMap keys, implement Comparable or supply Comparator consistent with equals where required by logic.

### Concurrency choices

- Synchronized wrappers (legacy/simple)
  ```java
  List<Integer> base = new ArrayList<>();
  List<Integer> syncList = Collections.synchronizedList(base);
  synchronized (syncList) { // manual external sync for iteration
    for (Integer x : syncList) { /* ... */ }
  }
  ```
- Concurrent collections (preferred)
  - ConcurrentHashMap: High concurrency, lock-striping, non-blocking reads, methods compute/merge/putIfAbsent optimized.
    ```java
    ConcurrentHashMap<String, Long> counts = new ConcurrentHashMap<>();
    counts.merge("key", 1L, Long::sum);
    ```
  - ConcurrentLinkedQueue/Deque: Lock-free queues for producer/consumer without blocking.
  - BlockingQueue implementations: LinkedBlockingQueue, ArrayBlockingQueue, PriorityBlockingQueue for producer/consumer with backpressure (put/take block).
  - CopyOnWriteArrayList/CopyOnWriteArraySet: Iteration without locking; costly writes; great for read-heavy event listener lists.
- Immutable/unmodifiable collections are inherently thread-safe for reading; ensure no thread mutates the backing collection.

### Fail-fast vs safe iteration

- Most java.util iterators are fail-fast (ConcurrentModificationException when structurally modified outside iterator).
- Concurrent collections provide weakly consistent iterators (no CME, may miss or see concurrent updates).

### Special-purpose collections

- EnumSet/EnumMap: High-performance sets/maps for enum keys.
  ```java
  enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }
  EnumSet<Day> workdays = EnumSet.range(Day.MON, Day.FRI);
  EnumMap<Day, String> duty = new EnumMap<>(Day.class);
  ```
- WeakHashMap: Keys held with weak references; entries removed when keys no longer strongly reachable (good for caches keyed by external object identity).
- IdentityHashMap: Keys compared by reference (==) not equals.
- LinkedHashMap with access-order for LRU
  ```java
  Map<K,V> lru = new LinkedHashMap<>(16, 0.75f, true);
  ```
  Override removeEldestEntry for size-based eviction.

### Views and ranges

- SubList/subSet/subMap are views backed by the original; modifying either reflects in the other; changing structure of backing may invalidate views.
- Navigable ranges with inclusive/exclusive bounds:
  ```java
  NavigableSet<Integer> s = new TreeSet<>(List.of(1,2,3,4,5));
  NavigableSet<Integer> mid = s.subSet(2, true, 4, true); // [2,4]
  ```

### Null handling

- Most modern collections disallow nulls in concurrent and sorted variants; HashMap/HashSet allow nulls; using null in maps complicates semantics (e.g., get may return null for absent or null value), prefer getOrDefault/containsKey.

### Performance tips

- Prefer ArrayList over LinkedList unless linked semantics are explicitly needed.
- Pre-size HashMap/ArrayList when size known to reduce rehash/resizes.
- Use RandomAccess marker to branch algorithms:
  ```java
  if (list instanceof RandomAccess) { /* index loop */ } else { /* iterator */ }
  ```

### Common patterns and idioms

- Counting words with merge
  ```java
  Map<String,Integer> freq = new HashMap<>();
  for (String w : words) freq.merge(w, 1, Integer::sum);
  ```
- Grouping and collecting with streams
  ```java
  Map<Integer, List<String>> byLen = list.stream().collect(Collectors.groupingBy(String::length));
  ```
- Top-K with PriorityQueue
  ```java
  record Item(String id, int score) {}
  PriorityQueue<Item> top = new PriorityQueue<>(Comparator.comparingInt(Item::score)); // min-heap
  for (Item it : items) { top.offer(it); if (top.size() > k) top.poll(); }
  List<Item> result = new ArrayList<>(top); result.sort(Comparator.comparingInt(Item::score).reversed());
  ```
- LRU cache skeleton
  ```java
  class Lru<K,V> extends LinkedHashMap<K,V> {
    private final int cap;
    Lru(int cap) { super(16, 0.75f, true); this.cap = cap; }
    protected boolean removeEldestEntry(Map.Entry<K,V> e) { return size() > cap; }
  }
  ```

### Equality, hashCode, comparator correctness

- equals contract: reflexive, symmetric, transitive, consistent; if equals returns true, hashCode must match.
- Comparator must be consistent with equals for sorted sets/maps when needed; avoid compare returning 0 for unequal objects unless intended to treat as duplicates.

### Unmodifiable, immutable, defensive design

- Return unmodifiable views from APIs to prevent external mutation.
  ```java
  private final List<String> friends = new ArrayList<>();
  public List<String> getFriends() { return Collections.unmodifiableList(friends); }
  ```
- Prefer List.of/Set.of/Map.of for small immutable collections; wrap with new ArrayList<>(List.of(...)) for a mutable copy.

### Error handling and pitfalls

- Don’t modify a collection while iterating except via Iterator.remove or collection methods documented as safe; otherwise expect ConcurrentModificationException.
- Sublist pitfalls: structural changes to backing list outside the view can cause IllegalArgumentException/CME in view operations.
- TreeSet/TreeMap with inconsistent comparator can lose elements or misbehave.

### Generics essentials with collections

- Prefer interface types in variable and parameter declarations (e.g., List<E> not ArrayList<E>).
- Use bounded wildcards to maximize API flexibility:
  - Producer extends, Consumer super (PECS):
    ```java
    // reads from src, writes into dst
    static <T> void copy(List<? extends T> src, List<? super T> dst) {
      for (T t : src) dst.add(t);
    }
    ```
- Arrays are covariant and reifiable; generics are invariant and erased; prefer collections for generic flexibility.

### Quick comparison table

| Topic      | ArrayList | LinkedList         | HashSet  | LinkedHashSet | TreeSet | HashMap      | LinkedHashMap    | TreeMap       | PriorityQueue | ArrayDeque  |
| ---------- | --------- | ------------------ | -------- | ------------- | ------- | ------------ | ---------------- | ------------- | ------------- | ----------- |
| Order      | Insertion | Insertion via list | None     | Insertion     | Sorted  | None         | Insertion/access | Sorted by key | Priority      | Deque order |
| Dupes      | Yes       | Yes                | No       | No            | No      | Keys no      | Keys no          | Keys no       | Yes           | Yes         |
| Nulls      | Yes       | Yes                | Yes      | Yes           | No      | 1 null key   | 1 null key       | No key null   | No            | No          |
| Access     | O(1) get  | O(n) get           | n/a      | n/a           | log n   | get O(1)     | get O(1)         | get log n     | head O(1)     | ends O(1)   |
| Insert mid | O(n)      | with iterator O(1) | O(1) avg | O(1) avg      | log n   | put O(1) avg | O(1) avg         | log n         | log n         | O(1)        |

### Practice exercises

- Implement frequency map with merge and then extract top-10 by value using a min-heap.
- Re-implement a stack using ArrayDeque and compare latency vs Stack.
- Create a synchronized view and demonstrate safe iteration with external synchronization.
- Use NavigableSet to find nearest neighbors in a sorted set of integers.

### Sample end-to-end snippet

```java
import java.util.*;
import java.util.stream.*;

public class CollectionsCheatsheet {
  public static void main(String[] args) {
    // Build mutable list from immutable seed
    List<String> words = new ArrayList<>(List.of("apple","banana","apricot","banana","cherry"));

    // De-duplicate while preserving order
    List<String> dedup = new ArrayList<>(new LinkedHashSet<>(words));

    // Group by first letter and sort each group by length then alpha
    Map<Character, List<String>> grouped =
        dedup.stream()
             .collect(Collectors.groupingBy(
                 s -> s.charAt(0),
                 Collectors.collectingAndThen(
                     Collectors.toCollection(ArrayList::new),
                     lst -> { lst.sort(Comparator.comparingInt(String::length).thenComparing(Comparator.naturalOrder())); return lst; }
                 )));

    // Frequency with merge
    Map<String, Integer> freq = new HashMap<>();
    for (String w : words) freq.merge(w, 1, Integer::sum);

    // Top-2 by frequency
    Comparator<Map.Entry<String,Integer>> byVal = Map.Entry.comparingByValue();
    PriorityQueue<Map.Entry<String,Integer>> top = new PriorityQueue<>(byVal);
    for (var e : freq.entrySet()) { top.offer(e); if (top.size() > 2) top.poll(); }
    List<Map.Entry<String,Integer>> top2 = new ArrayList<>(top);
    top2.sort(byVal.reversed());

    System.out.println(grouped);
    System.out.println(freq);
    System.out.println(top2);
  }
}
```

This set of notes covers interfaces, concrete classes, differences and trade-offs, iteration and bulk APIs, sorting/searching, concurrency choices, special-purpose collections, views and ranges, and practical examples to apply the Java Collections API effectively.
