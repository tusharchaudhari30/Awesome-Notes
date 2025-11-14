# Java DSA & LeetCode Cheatsheet

## Table of Contents

- [String Methods](#string-methods)
- [StringBuilder & StringBuffer](#stringbuilder--stringbuffer)
- [Array Methods](#array-methods)
- [ArrayList Methods](#arraylist-methods)
- [LinkedList Methods](#linkedlist-methods)
- [HashMap & TreeMap Methods](#hashmap--treemap-methods)
- [HashSet & TreeSet Methods](#hashset--treeset-methods)
- [Stack Methods](#stack-methods)
- [Queue & Deque Methods](#queue--deque-methods)
- [PriorityQueue Methods](#priorityqueue-methods)
- [Math Class Methods](#math-class-methods)
- [Integer & Character Methods](#integer--character-methods)
- [Stream API Methods](#stream-api-methods)
- [Comparator & Comparable](#comparator--comparable)
- [Common DSA Patterns](#common-dsa-patterns)
  - [Two Pointers](#two-pointers)
  - [Sliding Window](#sliding-window)
  - [Backtracking](#backtracking)
  - [Bit Manipulation](#bit-manipulation)

---

## String Methods

```java
String str = "Hello World";

// Length and Character Access
str.length()                      // Returns 11
str.charAt(0)                     // Returns 'H'
str.toCharArray()                 // Converts to char[]

// Substring Operations
str.substring(6)                  // "World"
str.substring(0, 5)               // "Hello"

// Search Operations
str.indexOf("World")              // Returns 6
str.indexOf('o')                  // Returns 4
str.lastIndexOf('o')              // Returns 7
str.contains("Hello")             // Returns true
str.startsWith("Hello")           // Returns true
str.endsWith("World")             // Returns true

// Comparison
str.equals("Hello World")         // true
str.equalsIgnoreCase("hello world") // true
str.compareTo("Hello World")      // 0 (equal)
str.compareTo("Hello")            // positive (greater)

// Modification (returns new String)
str.toLowerCase()                 // "hello world"
str.toUpperCase()                 // "HELLO WORLD"
str.trim()                        // Removes leading/trailing spaces
str.strip()                       // Better trim (Java 11+)
str.replace('o', '0')             // "Hell0 W0rld"
str.replaceAll("\\s+", "")        // Removes all whitespace
str.replaceFirst("l", "L")        // "HeLlo World"

// Split and Join
str.split(" ")                    // ["Hello", "World"]
String.join("-", "A", "B", "C")   // "A-B-C"

// Check Properties
str.isEmpty()                     // false
str.isBlank()                     // false (Java 11+)

// Conversion
String.valueOf(123)               // "123"
Integer.parseInt("123")           // 123
```

---

## StringBuilder & StringBuffer

```java
// StringBuilder (Not thread-safe, faster)
StringBuilder sb = new StringBuilder("Hello");

sb.append(" World")               // "Hello World"
sb.insert(5, ",")                 // "Hello, World"
sb.delete(5, 6)                   // "Hello World"
sb.deleteCharAt(5)                // "HelloWorld"
sb.reverse()                      // "dlroWolleH"
sb.replace(0, 5, "Hi")            // "HiWorld"
sb.setCharAt(0, 'h')              // "hiWorld"
sb.charAt(0)                      // 'h'
sb.length()                       // Returns length
sb.capacity()                     // Returns capacity
sb.toString()                     // Convert to String

// StringBuffer (Thread-safe, slower)
StringBuffer sbf = new StringBuffer("Hello");
// Same methods as StringBuilder
```

---

## Array Methods

```java
import java.util.Arrays;

int[] arr = {5, 2, 8, 1, 9};

// Sorting
Arrays.sort(arr);                           // [1, 2, 5, 8, 9]
Arrays.sort(arr, 0, 3);                     // Sort partial array
Arrays.sort(arr, Collections.reverseOrder()); // Descending (for Integer[])

// Searching (array must be sorted)
Arrays.binarySearch(arr, 5);                // Returns index or -(insertion point)-1

// Fill
Arrays.fill(arr, 0);                        // Fill with 0
Arrays.fill(arr, 1, 4, 10);                 // Fill index 1-3 with 10

// Copy
int[] copy = Arrays.copyOf(arr, arr.length);
int[] rangeCopy = Arrays.copyOfRange(arr, 1, 4);

// Comparison
Arrays.equals(arr1, arr2);                  // Returns boolean
Arrays.compare(arr1, arr2);                 // Lexicographic comparison

// Convert to String
Arrays.toString(arr);                       // "[1, 2, 5, 8, 9]"
Arrays.deepToString(arr2D);                 // For 2D arrays

// Convert to List
List<Integer> list = Arrays.asList(1, 2, 3);

// Stream operations (Java 8+)
Arrays.stream(arr).sum();
Arrays.stream(arr).max().getAsInt();
Arrays.stream(arr).min().getAsInt();
```

---

## ArrayList Methods

```java
import java.util.ArrayList;
import java.util.Collections;

ArrayList<Integer> list = new ArrayList<>();

// Add Elements
list.add(10);                               // Add at end
list.add(0, 5);                             // Add at index
list.addAll(Arrays.asList(1, 2, 3));        // Add collection

// Access Elements
list.get(0);                                // Get element at index
list.set(0, 100);                           // Set element at index
list.indexOf(10);                           // First occurrence
list.lastIndexOf(10);                       // Last occurrence

// Remove Elements
list.remove(0);                             // Remove by index
list.remove(Integer.valueOf(10));           // Remove by value
list.removeAll(Arrays.asList(1, 2));        // Remove multiple
list.clear();                               // Remove all

// Size and Check
list.size();                                // Returns size
list.isEmpty();                             // Check if empty
list.contains(10);                          // Check if contains

// Sorting and Operations
Collections.sort(list);                     // Ascending
Collections.sort(list, Collections.reverseOrder()); // Descending
Collections.reverse(list);                  // Reverse
Collections.shuffle(list);                  // Shuffle
Collections.max(list);                      // Max element
Collections.min(list);                      // Min element

// Sublist
list.subList(0, 3);                         // Returns sublist view

// Convert to Array
Integer[] arr = list.toArray(new Integer[0]);

// Iteration
for (int num : list) { }
list.forEach(num -> System.out.println(num));
```

---

## LinkedList Methods

```java
import java.util.LinkedList;

LinkedList<Integer> ll = new LinkedList<>();

// Add Elements
ll.add(10);                                 // Add at end
ll.addFirst(5);                             // Add at beginning
ll.addLast(15);                             // Add at end
ll.add(1, 8);                               // Add at index

// Access Elements
ll.get(0);                                  // Get by index
ll.getFirst();                              // Get first
ll.getLast();                               // Get last
ll.peek();                                  // Get first (returns null if empty)
ll.peekFirst();                             // Get first
ll.peekLast();                              // Get last

// Remove Elements
ll.remove();                                // Remove first
ll.removeFirst();                           // Remove first
ll.removeLast();                            // Remove last
ll.remove(1);                               // Remove by index
ll.poll();                                  // Remove and return first
ll.pollFirst();                             // Remove and return first
ll.pollLast();                              // Remove and return last

// Stack Operations
ll.push(5);                                 // Add to front (stack)
ll.pop();                                   // Remove from front (stack)

// Queue Operations
ll.offer(10);                               // Add to end (queue)
ll.poll();                                  // Remove from front (queue)

// Size
ll.size();
ll.isEmpty();
ll.contains(10);
```

---

## HashMap & TreeMap Methods

```java
import java.util.HashMap;
import java.util.TreeMap;

// HashMap - O(1) operations, no order
HashMap<String, Integer> map = new HashMap<>();

// Put and Get
map.put("A", 1);                            // Add key-value
map.putIfAbsent("B", 2);                    // Add if key doesn't exist
map.get("A");                               // Returns 1
map.getOrDefault("C", 0);                   // Returns 0 if key not found

// Remove
map.remove("A");                            // Remove by key
map.remove("A", 1);                         // Remove if key-value matches

// Check
map.containsKey("A");                       // Check if key exists
map.containsValue(1);                       // Check if value exists
map.isEmpty();
map.size();

// Iteration
for (String key : map.keySet()) { }         // Iterate keys
for (Integer value : map.values()) { }      // Iterate values
for (Map.Entry<String, Integer> entry : map.entrySet()) {
    entry.getKey();
    entry.getValue();
}

// Java 8+ Operations
map.forEach((k, v) -> System.out.println(k + " = " + v));
map.compute("A", (k, v) -> (v == null) ? 1 : v + 1);
map.computeIfAbsent("B", k -> 1);
map.computeIfPresent("A", (k, v) -> v + 1);
map.merge("A", 1, Integer::sum);            // Increment by 1

// TreeMap - O(log n) operations, sorted by keys
TreeMap<String, Integer> treeMap = new TreeMap<>();
// All HashMap methods +
treeMap.firstKey();                         // First key
treeMap.lastKey();                          // Last key
treeMap.floorKey("B");                      // Largest key <= "B"
treeMap.ceilingKey("B");                    // Smallest key >= "B"
treeMap.lowerKey("B");                      // Largest key < "B"
treeMap.higherKey("B");                     // Smallest key > "B"
```

---

## HashSet & TreeSet Methods

```java
import java.util.HashSet;
import java.util.TreeSet;

// HashSet - O(1) operations, no order, no duplicates
HashSet<Integer> set = new HashSet<>();

set.add(1);                                 // Add element
set.addAll(Arrays.asList(2, 3, 4));         // Add multiple
set.remove(1);                              // Remove element
set.contains(2);                            // Check if exists
set.size();
set.isEmpty();
set.clear();

// Iteration
for (int num : set) { }
set.forEach(num -> System.out.println(num));

// TreeSet - O(log n) operations, sorted, no duplicates
TreeSet<Integer> treeSet = new TreeSet<>();
// All HashSet methods +
treeSet.first();                            // First element
treeSet.last();                             // Last element
treeSet.floor(5);                           // Largest element <= 5
treeSet.ceiling(5);                         // Smallest element >= 5
treeSet.lower(5);                           // Largest element < 5
treeSet.higher(5);                          // Smallest element > 5
treeSet.pollFirst();                        // Remove and return first
treeSet.pollLast();                         // Remove and return last
```

---

## Stack Methods

```java
import java.util.Stack;

Stack<Integer> stack = new Stack<>();

// Push and Pop
stack.push(10);                             // Add to top
stack.pop();                                // Remove and return top
stack.peek();                               // Return top without removing

// Check
stack.isEmpty();
stack.size();
stack.search(10);                           // Returns 1-based position from top

// Note: Use Deque instead of Stack for better performance
Deque<Integer> stack2 = new ArrayDeque<>();
stack2.push(10);
stack2.pop();
stack2.peek();
```

---

## Queue & Deque Methods

```java
import java.util.Queue;
import java.util.LinkedList;
import java.util.Deque;
import java.util.ArrayDeque;

// Queue (FIFO)
Queue<Integer> queue = new LinkedList<>();

// Add
queue.offer(10);                            // Add to rear (returns false if fails)
queue.add(20);                              // Add to rear (throws exception if fails)

// Remove
queue.poll();                               // Remove and return front (null if empty)
queue.remove();                             // Remove and return front (exception if empty)

// Peek
queue.peek();                               // Return front (null if empty)
queue.element();                            // Return front (exception if empty)

// Check
queue.isEmpty();
queue.size();

// Deque (Double-ended Queue)
Deque<Integer> deque = new ArrayDeque<>();

// Add to front
deque.addFirst(10);
deque.offerFirst(5);

// Add to rear
deque.addLast(20);
deque.offerLast(25);

// Remove from front
deque.removeFirst();
deque.pollFirst();

// Remove from rear
deque.removeLast();
deque.pollLast();

// Peek
deque.peekFirst();
deque.peekLast();
```

---

## PriorityQueue Methods

```java
import java.util.PriorityQueue;
import java.util.Comparator;

// Min Heap (default)
PriorityQueue<Integer> minHeap = new PriorityQueue<>();

// Max Heap
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
// OR
PriorityQueue<Integer> maxHeap2 = new PriorityQueue<>((a, b) -> b - a);

// Add
minHeap.offer(10);                          // Add element
minHeap.add(5);                             // Add element

// Remove
minHeap.poll();                             // Remove and return smallest
minHeap.remove();                           // Remove and return smallest

// Peek
minHeap.peek();                             // Return smallest without removing

// Check
minHeap.isEmpty();
minHeap.size();
minHeap.contains(10);

// Custom Comparator
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]); // Sort by first element
```

---

## Math Class Methods

```java
// Basic Operations
Math.abs(-10);                              // 10
Math.max(5, 10);                            // 10
Math.min(5, 10);                            // 5

// Power and Root
Math.pow(2, 3);                             // 8.0
Math.sqrt(16);                              // 4.0
Math.cbrt(27);                              // 3.0

// Rounding
Math.ceil(4.3);                             // 5.0
Math.floor(4.7);                            // 4.0
Math.round(4.5);                            // 5

// Exponential and Logarithm
Math.exp(1);                                // e^1
Math.log(Math.E);                           // 1.0 (natural log)
Math.log10(100);                            // 2.0

// Trigonometric
Math.sin(Math.PI / 2);                      // 1.0
Math.cos(0);                                // 1.0
Math.tan(Math.PI / 4);                      // 1.0
Math.toDegrees(Math.PI);                    // 180.0
Math.toRadians(180);                        // Math.PI

// Random
Math.random();                              // [0.0, 1.0)
(int)(Math.random() * 100);                 // [0, 99]

// Constants
Math.PI;                                    // 3.141592653589793
Math.E;                                     // 2.718281828459045
```

---

## Integer & Character Methods

```java
// Integer Wrapper Class
Integer num = 10;

// Conversion
Integer.parseInt("123");                    // String to int
Integer.valueOf("123");                     // String to Integer object
Integer.toString(123);                      // int to String
Integer.toBinaryString(10);                 // "1010"
Integer.toHexString(255);                   // "ff"
Integer.toOctalString(8);                   // "10"

// Comparison
Integer.compare(10, 20);                    // -1 (negative if first < second)
Integer.max(10, 20);                        // 20
Integer.min(10, 20);                        // 10
Integer.sum(10, 20);                        // 30

// Bit Operations
Integer.bitCount(7);                        // 3 (number of 1 bits)
Integer.highestOneBit(10);                  // 8
Integer.lowestOneBit(10);                   // 2
Integer.numberOfLeadingZeros(10);           // 28
Integer.numberOfTrailingZeros(8);           // 3
Integer.reverse(10);                        // Reverse bits
Integer.reverseBytes(10);                   // Reverse byte order
Integer.rotateLeft(8, 1);                   // 16
Integer.rotateRight(8, 1);                  // 4
Integer.signum(-10);                        // -1 (sign of number)

// Constants
Integer.MAX_VALUE;                          // 2147483647
Integer.MIN_VALUE;                          // -2147483648

// Character Class
Character ch = 'A';

// Check Type
Character.isLetter('A');                    // true
Character.isDigit('5');                     // true
Character.isLetterOrDigit('A');             // true
Character.isWhitespace(' ');                // true
Character.isUpperCase('A');                 // true
Character.isLowerCase('a');                 // true

// Conversion
Character.toUpperCase('a');                 // 'A'
Character.toLowerCase('A');                 // 'a'
Character.toString('A');                    // "A"
Character.getNumericValue('5');             // 5
Character.digit('A', 16);                   // 10 (hex)

// Comparison
Character.compare('A', 'B');                // -1
```

---

## Stream API Methods

```java
import java.util.stream.*;
import java.util.Arrays;
import java.util.List;

List<Integer> list = Arrays.asList(1, 2, 3, 4, 5);

// Creating Streams
list.stream();
Arrays.stream(new int[]{1, 2, 3});
Stream.of(1, 2, 3, 4, 5);
Stream.iterate(0, n -> n + 1).limit(10);    // 0 to 9
Stream.generate(Math::random).limit(5);

// Intermediate Operations
list.stream()
    .filter(x -> x > 2)                     // Filter elements
    .map(x -> x * 2)                        // Transform elements
    .distinct()                             // Remove duplicates
    .sorted()                               // Sort (natural order)
    .sorted(Comparator.reverseOrder())      // Sort (reverse)
    .limit(3)                               // Limit to 3 elements
    .skip(2)                                // Skip first 2 elements
    .peek(System.out::println);             // Perform action without consuming

// Terminal Operations
list.stream().forEach(System.out::println); // Print each element
list.stream().count();                      // Count elements
list.stream().collect(Collectors.toList()); // Collect to List
list.stream().collect(Collectors.toSet());  // Collect to Set
list.stream().toArray();                    // Convert to array

// Reduction
list.stream().reduce(0, Integer::sum);      // Sum all elements
list.stream().reduce(Integer::max);         // Find max (returns Optional)
list.stream().sum();                        // Sum (for IntStream)
list.stream().max(Comparator.naturalOrder()); // Max
list.stream().min(Comparator.naturalOrder()); // Min

// Matching
list.stream().anyMatch(x -> x > 3);         // true if any element > 3
list.stream().allMatch(x -> x > 0);         // true if all elements > 0
list.stream().noneMatch(x -> x < 0);        // true if no element < 0

// Finding
list.stream().findFirst();                  // First element (Optional)
list.stream().findAny();                    // Any element (useful in parallel)

// Grouping and Partitioning
Map<Boolean, List<Integer>> partitioned =
    list.stream().collect(Collectors.partitioningBy(x -> x > 3));

Map<Integer, List<Integer>> grouped =
    list.stream().collect(Collectors.groupingBy(x -> x % 2));

// String Operations
String result = list.stream()
    .map(String::valueOf)
    .collect(Collectors.joining(", "));     // "1, 2, 3, 4, 5"

// IntStream, LongStream, DoubleStream
IntStream.range(0, 10);                     // [0, 10)
IntStream.rangeClosed(0, 10);               // [0, 10]
list.stream().mapToInt(Integer::intValue).sum();
list.stream().mapToDouble(Integer::doubleValue).average();
```

---

## Comparator & Comparable

```java
// Comparable Interface (Natural Ordering)
class Student implements Comparable<Student> {
    String name;
    int age;

    @Override
    public int compareTo(Student other) {
        return this.age - other.age;        // Sort by age ascending
    }
}

// Using Comparable
Collections.sort(studentList);              // Uses compareTo()

// Comparator Interface (Custom Ordering)
// Lambda Expression
Comparator<Student> byName = (s1, s2) -> s1.name.compareTo(s2.name);
Comparator<Student> byAge = (s1, s2) -> s1.age - s2.age;

// Method Reference
Comparator<Student> byNameRef = Comparator.comparing(Student::getName);

// Multiple Comparisons
Comparator<Student> multiComparator = Comparator
    .comparing(Student::getAge)
    .thenComparing(Student::getName);

// Reverse Order
Comparator<Student> reverseAge = Comparator.comparing(Student::getAge).reversed();

// Using Comparator
Collections.sort(studentList, byName);
studentList.sort(byAge);
Arrays.sort(studentArray, byName);

// Common Patterns
// Sort array in descending order
Arrays.sort(arr, Collections.reverseOrder());
Arrays.sort(arr, (a, b) -> b - a);

// Sort by custom criteria
Arrays.sort(intervals, (a, b) -> a[0] - b[0]); // Sort by first element
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]); // Sort by second element
```

---

## Common DSA Patterns

### Two Pointers

```java
// Pattern 1: Opposite Ends
public boolean isPalindrome(String s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        if (s.charAt(left) != s.charAt(right)) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}

// Pattern 2: Same Direction (Fast & Slow)
public ListNode findMiddle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    return slow;
}

// Pattern 3: Two Arrays
public int[] mergeSortedArrays(int[] arr1, int[] arr2) {
    int i = 0, j = 0, k = 0;
    int[] result = new int[arr1.length + arr2.length];

    while (i < arr1.length && j < arr2.length) {
        if (arr1[i] <= arr2[j]) {
            result[k++] = arr1[i++];
        } else {
            result[k++] = arr2[j++];
        }
    }

    while (i < arr1.length) result[k++] = arr1[i++];
    while (j < arr2.length) result[k++] = arr2[j++];

    return result;
}
```

### Sliding Window

```java
// Fixed Size Window
public int maxSumSubarray(int[] arr, int k) {
    int maxSum = 0, windowSum = 0;

    // Calculate sum of first window
    for (int i = 0; i < k; i++) {
        windowSum += arr[i];
    }
    maxSum = windowSum;

    // Slide the window
    for (int i = k; i < arr.length; i++) {
        windowSum += arr[i] - arr[i - k];
        maxSum = Math.max(maxSum, windowSum);
    }

    return maxSum;
}

// Variable Size Window Template
public int longestSubarrayWithSumK(int[] arr, int k) {
    int left = 0, right = 0;
    int sum = 0, maxLen = 0;

    while (right < arr.length) {
        // Expand window
        sum += arr[right];

        // Shrink window while condition violated
        while (sum > k && left <= right) {
            sum -= arr[left];
            left++;
        }

        // Update result if valid window
        if (sum == k) {
            maxLen = Math.max(maxLen, right - left + 1);
        }

        right++;
    }

    return maxLen;
}

// Optimized Variable Window (No Shrinking Below Max)
public int longestSubstringWithKDistinct(String s, int k) {
    Map<Character, Integer> map = new HashMap<>();
    int left = 0, right = 0, maxLen = 0;

    while (right < s.length()) {
        char c = s.charAt(right);
        map.put(c, map.getOrDefault(c, 0) + 1);

        // Shrink only if condition violated
        if (map.size() > k) {
            char leftChar = s.charAt(left);
            map.put(leftChar, map.get(leftChar) - 1);
            if (map.get(leftChar) == 0) {
                map.remove(leftChar);
            }
            left++;
        }

        maxLen = Math.max(maxLen, right - left + 1);
        right++;
    }

    return maxLen;
}
```

### Backtracking

```java
// General Backtracking Template
public List<List<Integer>> backtrack(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrackHelper(result, new ArrayList<>(), nums, 0);
    return result;
}

private void backtrackHelper(List<List<Integer>> result, List<Integer> temp,
                             int[] nums, int start) {
    // Base case: process solution
    result.add(new ArrayList<>(temp));

    // Loop through choices
    for (int i = start; i < nums.length; i++) {
        // Make choice
        temp.add(nums[i]);

        // Recurse with updated state
        backtrackHelper(result, temp, nums, i + 1);

        // Undo choice (backtrack)
        temp.remove(temp.size() - 1);
    }
}

// Permutations (Use all elements)
public List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(result, new ArrayList<>(), nums, new boolean[nums.length]);
    return result;
}

private void backtrack(List<List<Integer>> result, List<Integer> temp,
                       int[] nums, boolean[] used) {
    if (temp.size() == nums.length) {
        result.add(new ArrayList<>(temp));
        return;
    }

    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;

        temp.add(nums[i]);
        used[i] = true;

        backtrack(result, temp, nums, used);

        temp.remove(temp.size() - 1);
        used[i] = false;
    }
}

// Combinations (Choose k elements)
public List<List<Integer>> combine(int n, int k) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(result, new ArrayList<>(), 1, n, k);
    return result;
}

private void backtrack(List<List<Integer>> result, List<Integer> temp,
                       int start, int n, int k) {
    if (temp.size() == k) {
        result.add(new ArrayList<>(temp));
        return;
    }

    for (int i = start; i <= n; i++) {
        temp.add(i);
        backtrack(result, temp, i + 1, n, k);
        temp.remove(temp.size() - 1);
    }
}

// Subsets (All possible subsets)
public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(result, new ArrayList<>(), nums, 0);
    return result;
}

private void backtrack(List<List<Integer>> result, List<Integer> temp,
                       int[] nums, int start) {
    result.add(new ArrayList<>(temp));

    for (int i = start; i < nums.length; i++) {
        temp.add(nums[i]);
        backtrack(result, temp, nums, i + 1);
        temp.remove(temp.size() - 1);
    }
}
```

### Bit Manipulation

```java
// Basic Bit Operations
// AND (&): Both bits must be 1
5 & 3;                                      // 1 (0101 & 0011 = 0001)

// OR (|): At least one bit must be 1
5 | 3;                                      // 7 (0101 | 0011 = 0111)

// XOR (^): Bits must be different
5 ^ 3;                                      // 6 (0101 ^ 0011 = 0110)
// XOR Properties: a ^ 0 = a, a ^ a = 0, a ^ b ^ a = b

// NOT (~): Flip all bits
~5;                                         // -6 (inverts bits)

// Left Shift (<<): Multiply by 2^n
5 << 1;                                     // 10 (0101 -> 1010)
5 << 2;                                     // 20 (multiply by 4)

// Right Shift (>>): Divide by 2^n
5 >> 1;                                     // 2 (0101 -> 0010)
20 >> 2;                                    // 5 (divide by 4)

// Unsigned Right Shift (>>>)
-1 >>> 1;                                   // Large positive number

// Common Bit Tricks
// Check if number is power of 2
boolean isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}

// Count number of set bits (1s)
int countSetBits(int n) {
    int count = 0;
    while (n > 0) {
        n &= (n - 1);                       // Clear rightmost set bit
        count++;
    }
    return count;
    // OR use: Integer.bitCount(n);
}

// Get bit at position i
boolean getBit(int n, int i) {
    return ((n >> i) & 1) == 1;
}

// Set bit at position i
int setBit(int n, int i) {
    return n | (1 << i);
}

// Clear bit at position i
int clearBit(int n, int i) {
    return n & ~(1 << i);
}

// Toggle bit at position i
int toggleBit(int n, int i) {
    return n ^ (1 << i);
}

// Check if number is odd
boolean isOdd(int n) {
    return (n & 1) == 1;
}

// Check if number is even
boolean isEven(int n) {
    return (n & 1) == 0;
}

// Swap two numbers without temp variable
void swap(int a, int b) {
    a = a ^ b;
    b = a ^ b;                              // b = a
    a = a ^ b;                              // a = b
}

// Find single number (all others appear twice)
int singleNumber(int[] nums) {
    int result = 0;
    for (int num : nums) {
        result ^= num;
    }
    return result;
}

// Get rightmost set bit
int getRightmostSetBit(int n) {
    return n & -n;
}

// Clear all bits from MSB to i (inclusive)
int clearBitsMSBtoI(int n, int i) {
    return n & ((1 << i) - 1);
}

// Clear all bits from i to 0 (inclusive)
int clearBitsIto0(int n, int i) {
    return n & (~((1 << (i + 1)) - 1));
}

// Update bit at position i with value v (0 or 1)
int updateBit(int n, int i, int v) {
    int mask = ~(1 << i);                   // Clear bit i
    return (n & mask) | (v << i);           // Set bit i to v
}
```

---

## Common LeetCode Patterns Summary

### When to Use Each Pattern

**Two Pointers:**

- Sorted arrays
- Palindromes
- Pair sum problems
- Linked list cycle detection
- In-place array modifications

**Sliding Window:**

- Contiguous subarray/substring problems
- Maximum/minimum subarray with constraints
- "Longest/shortest substring with K distinct characters"
- Problems involving "window" of elements

**Backtracking:**

- Generate all combinations/permutations
- Subsets problems
- Sudoku solver, N-Queens
- Word search, path finding
- Constraint satisfaction problems

**Bit Manipulation:**

- Problems involving powers of 2
- Set operations (union, intersection)
- Single number problems
- Counting set bits
- Optimization when flag storage needed

---

## Time Complexity Cheatsheet

| Data Structure | Access   | Search   | Insert   | Delete   |
| -------------- | -------- | -------- | -------- | -------- |
| Array          | O(1)     | O(n)     | O(n)     | O(n)     |
| ArrayList      | O(1)     | O(n)     | O(1)\*   | O(n)     |
| LinkedList     | O(n)     | O(n)     | O(1)\*\* | O(1)\*\* |
| Stack          | O(n)     | O(n)     | O(1)     | O(1)     |
| Queue          | O(n)     | O(n)     | O(1)     | O(1)     |
| HashSet        | N/A      | O(1)\*   | O(1)\*   | O(1)\*   |
| TreeSet        | N/A      | O(log n) | O(log n) | O(log n) |
| HashMap        | O(1)\*   | O(1)\*   | O(1)\*   | O(1)\*   |
| TreeMap        | O(log n) | O(log n) | O(log n) | O(log n) |
| PriorityQueue  | N/A      | O(n)     | O(log n) | O(log n) |

\* Amortized/Average case
\*\* When you have reference to node

---

## Quick Reference: Common Operations

```java
// Find max in array
int max = Arrays.stream(arr).max().getAsInt();
int max = Collections.max(list);

// Find min in array
int min = Arrays.stream(arr).min().getAsInt();
int min = Collections.min(list);

// Sum of array
int sum = Arrays.stream(arr).sum();

// Reverse array
Collections.reverse(Arrays.asList(arr));

// Reverse string
String reversed = new StringBuilder(str).reverse().toString();

// Check if array is sorted
boolean sorted = IntStream.range(0, arr.length - 1)
                          .allMatch(i -> arr[i] <= arr[i + 1]);

// Remove duplicates from array
int[] unique = Arrays.stream(arr).distinct().toArray();

// Convert char array to string
String str = new String(charArray);
String str = String.valueOf(charArray);

// Convert string to int array
int[] arr = str.chars().map(c -> c - '0').toArray();

// Frequency map
Map<Integer, Long> freq = list.stream()
    .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));

// GCD
int gcd(int a, int b) {
    return b == 0 ? a : gcd(b, a % b);
}

// LCM
int lcm(int a, int b) {
    return (a * b) / gcd(a, b);
}

// Check if prime
boolean isPrime(int n) {
    if (n <= 1) return false;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) return false;
    }
    return true;
}
```

---

**Pro Tips:**

1. Always consider edge cases: empty arrays, single element, duplicates
2. Use appropriate data structures: HashMap for O(1) lookup, TreeMap for sorted order
3. For optimization, think: Can I trade space for time?
4. Master the standard library - don't reinvent the wheel
5. Practice recognizing patterns in problems
6. Time complexity matters more than space in most interviews

---

Created for LeetCode & DSA Interview Preparation
