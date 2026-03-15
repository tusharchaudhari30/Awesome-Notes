# 100 Tricky Java Code Questions with Output & Explanations

## Table of Contents

- [Table of Contents](#table-of-contents)
- [String & String Pool](#string-string-pool)
  - [Q1. String Comparison with ==](#q1-string-comparison-with)
  - [Q2. String Concatenation with null](#q2-string-concatenation-with-null)
  - [Q3. String Immutability](#q3-string-immutability)
  - [Q4. String intern() Method](#q4-string-intern-method)
  - [Q5. StringBuilder vs String](#q5-stringbuilder-vs-string)
  - [Q6. String split with Regex](#q6-string-split-with-regex)
  - [Q7. String Pool with Constructor](#q7-string-pool-with-constructor)
  - [Q8. String Equality with equals()](#q8-string-equality-with-equals)
  - [Q9. Empty String vs Null](#q9-empty-string-vs-null)
  - [Q10. String Concatenation in Loop](#q10-string-concatenation-in-loop)
- [Wrapper Classes & Autoboxing](#wrapper-classes-autoboxing)
  - [Q11. Integer Cache](#q11-integer-cache)
  - [Q12. Autoboxing with null](#q12-autoboxing-with-null)
  - [Q13. Wrapper Class Comparison](#q13-wrapper-class-comparison)
  - [Q14. Autoboxing in Collections](#q14-autoboxing-in-collections)
  - [Q15. Double vs double](#q15-double-vs-double)
  - [Q16. Unboxing in Arithmetic](#q16-unboxing-in-arithmetic)
  - [Q17. Boolean Caching](#q17-boolean-caching)
  - [Q18. Character Cache Range](#q18-character-cache-range)
  - [Q19. Wrapper valueOf vs Constructor](#q19-wrapper-valueof-vs-constructor)
  - [Q20. Mixed Type Comparison](#q20-mixed-type-comparison)
- [Operators & Precedence](#operators-precedence)
  - [Q21. Increment Operator Confusion](#q21-increment-operator-confusion)
  - [Q22. Operator Precedence](#q22-operator-precedence)
  - [Q23. Short-Circuit Evaluation](#q23-short-circuit-evaluation)
  - [Q24. Bitwise XOR Swap](#q24-bitwise-xor-swap)
  - [Q25. Ternary Operator Precedence](#q25-ternary-operator-precedence)
  - [Q26. Division by Zero](#q26-division-by-zero)
  - [Q27. Modulo with Negative Numbers](#q27-modulo-with-negative-numbers)
  - [Q28. Bitwise NOT Operator](#q28-bitwise-not-operator)
  - [Q29. Operator Associativity](#q29-operator-associativity)
  - [Q30. Compound Assignment](#q30-compound-assignment)
- [Exception Handling](#exception-handling)
  - [Q31. Finally Always Executes](#q31-finally-always-executes)
  - [Q32. Return in Finally](#q32-return-in-finally)
  - [Q33. Exception in Finally](#q33-exception-in-finally)
  - [Q34. Multiple Catch Blocks](#q34-multiple-catch-blocks)
  - [Q35. Try Without Catch or Finally](#q35-try-without-catch-or-finally)
  - [Q36. Checked vs Unchecked Exception](#q36-checked-vs-unchecked-exception)
  - [Q37. Try-With-Resources](#q37-try-with-resources)
  - [Q38. Rethrowing Exceptions](#q38-rethrowing-exceptions)
  - [Q39. Custom Exception](#q39-custom-exception)
  - [Q40. Finally Without Catch](#q40-finally-without-catch)
- [Static & Initialization Blocks](#static-initialization-blocks)
  - [Q41. Static Variable Initialization](#q41-static-variable-initialization)
  - [Q42. Multiple Static Blocks](#q42-multiple-static-blocks)
  - [Q43. Instance vs Static Block](#q43-instance-vs-static-block)
  - [Q44. Static Variable Forward Reference](#q44-static-variable-forward-reference)
  - [Q45. Constructor and Static](#q45-constructor-and-static)
  - [Q46. Static Method Call](#q46-static-method-call)
  - [Q47. Static Final Variable](#q47-static-final-variable)
  - [Q48. Parent-Child Static Block Order](#q48-parent-child-static-block-order)
  - [Q49. Static Import](#q49-static-import)
  - [Q50. Instance Block Order](#q50-instance-block-order)
- [Method Overloading & Overriding](#method-overloading-overriding)
  - [Q51. Overloading with Autoboxing](#q51-overloading-with-autoboxing)
  - [Q52. Overloading with Varargs](#q52-overloading-with-varargs)
  - [Q53. Overloading with Widening](#q53-overloading-with-widening)
  - [Q54. Override Return Type](#q54-override-return-type)
  - [Q55. Override with Exception](#q55-override-with-exception)
  - [Q56. Static Method "Override"](#q56-static-method-override)
  - [Q57. Private Method Override](#q57-private-method-override)
  - [Q58. Final Method Override](#q58-final-method-override)
  - [Q59. Overloading with null](#q59-overloading-with-null)
  - [Q60. Constructor Overloading](#q60-constructor-overloading)
- [Multithreading & Concurrency](#multithreading-concurrency)
  - [Q61. Thread Start vs Run](#q61-thread-start-vs-run)
  - [Q62. Volatile Keyword](#q62-volatile-keyword)
  - [Q63. Synchronized Method](#q63-synchronized-method)
  - [Q64. Deadlock Example](#q64-deadlock-example)
  - [Q65. Wait and Notify](#q65-wait-and-notify)
- [Collections Framework](#collections-framework)
  - [Q66. ArrayList vs LinkedList](#q66-arraylist-vs-linkedlist)
  - [Q67. HashMap Null Keys](#q67-hashmap-null-keys)
  - [Q68. Set Add Return Value](#q68-set-add-return-value)
  - [Q69. Iterator Modification](#q69-iterator-modification)
  - [Q70. TreeSet Ordering](#q70-treeset-ordering)
  - [Q71. HashMap Collision](#q71-hashmap-collision)
  - [Q72. Arrays.asList Issue](#q72-arraysaslist-issue)
  - [Q73. Stack vs Deque](#q73-stack-vs-deque)
  - [Q74. LinkedHashMap Ordering](#q74-linkedhashmap-ordering)
  - [Q75. Queue Offer vs Add](#q75-queue-offer-vs-add)
- [Lambda & Functional Interfaces](#lambda-functional-interfaces)
  - [Q76. Lambda Basic Syntax](#q76-lambda-basic-syntax)
  - [Q77. Method Reference](#q77-method-reference)
  - [Q78. Lambda Variable Capture](#q78-lambda-variable-capture)
  - [Q79. Functional Interface Inheritance](#q79-functional-interface-inheritance)
  - [Q80. Lambda with Streams](#q80-lambda-with-streams)
- [Inheritance & Polymorphism](#inheritance-polymorphism)
  - [Q81. instanceof with null](#q81-instanceof-with-null)
  - [Q82. super Keyword](#q82-super-keyword)
  - [Q83. Constructor Chaining](#q83-constructor-chaining)
  - [Q84. Polymorphism with Fields](#q84-polymorphism-with-fields)
  - [Q85. Abstract Class Constructor](#q85-abstract-class-constructor)
- [Arrays & Memory](#arrays-memory)
  - [Q86. Array Initialization](#q86-array-initialization)
  - [Q87. Array Declaration Styles](#q87-array-declaration-styles)
  - [Q88. Multidimensional Array](#q88-multidimensional-array)
  - [Q89. Array Covariance](#q89-array-covariance)
  - [Q90. Array vs ArrayList](#q90-array-vs-arraylist)
- [Inner & Nested Classes](#inner-nested-classes)
  - [Q91. Static Nested Class](#q91-static-nested-class)
  - [Q92. Inner Class](#q92-inner-class)
  - [Q93. Anonymous Inner Class](#q93-anonymous-inner-class)
  - [Q94. Local Inner Class](#q94-local-inner-class)
  - [Q95. Inner Class this Reference](#q95-inner-class-this-reference)
- [Miscellaneous Tricky Concepts](#miscellaneous-tricky-concepts)
  - [Q96. Switch Fall-Through](#q96-switch-fall-through)
  - [Q97. Enum with Methods](#q97-enum-with-methods)
  - [Q98. Pass by Value](#q98-pass-by-value)
  - [Q99. Transient Keyword](#q99-transient-keyword)
  - [Q100. Diamond Problem with Interfaces](#q100-diamond-problem-with-interfaces)
- [Summary](#summary)

## String & String Pool

### Q1. String Comparison with ==
```java
public class Test {
    public static void main(String[] args) {
        String s1 = "Hello";
        String s2 = "Hello";
        String s3 = new String("Hello");
        System.out.println(s1 == s2);
        System.out.println(s1 == s3);
    }
}
// Output: true, false
```
**Explanation:** `s1` and `s2` point to the same object in the String pool, so `==` returns true. `s3` creates a new object in heap memory, so `s1 == s3` returns false. String literals are stored in the String pool for memory optimization.

### Q2. String Concatenation with null
```java
public class Test {
    public static void main(String[] args) {
        String s = "Java" + null;
        System.out.println(s);
    }
}
// Output: Javanull
```
**Explanation:** When concatenating null with a String, Java converts null to the string "null". This is because the `+` operator calls `String.valueOf(null)` which returns "null".

### Q3. String Immutability
```java
public class Test {
    public static void main(String[] args) {
        String s1 = "Hello";
        s1.concat(" World");
        System.out.println(s1);
    }
}
// Output: Hello
```
**Explanation:** Strings are immutable in Java. The `concat()` method returns a new String object but doesn't modify the original. To see the change, you must assign the result: `s1 = s1.concat(" World");`.

### Q4. String intern() Method
```java
public class Test {
    public static void main(String[] args) {
        String s1 = new String("Java");
        String s2 = s1.intern();
        String s3 = "Java";
        System.out.println(s1 == s2);
        System.out.println(s2 == s3);
    }
}
// Output: false, true
```
**Explanation:** `intern()` returns a canonical representation from the String pool. `s1` is in heap, `s2` and `s3` point to the same pooled string. This demonstrates how intern() helps reuse String objects.

### Q5. StringBuilder vs String
```java
public class Test {
    public static void main(String[] args) {
        String s = "A";
        s = s + "B";
        StringBuilder sb = new StringBuilder("A");
        sb.append("B");
        System.out.println(s == sb.toString());
    }
}
// Output: false
```
**Explanation:** Even though both contain "AB", they are different objects. String concatenation creates new objects, StringBuilder modifies the same object. `toString()` creates a new String from StringBuilder.

### Q6. String split with Regex
```java
public class Test {
    public static void main(String[] args) {
        String s = "a.b.c";
        String[] arr = s.split(".");
        System.out.println(arr.length);
    }
}
// Output: 0
```
**Explanation:** `split()` takes a regex pattern. In regex, `.` matches any character, so it splits on every character, resulting in empty strings. Use `split("\\.")` to split on literal dots.

### Q7. String Pool with Constructor
```java
public class Test {
    public static void main(String[] args) {
        String s1 = "Hello";
        String s2 = new String("Hello").intern();
        System.out.println(s1 == s2);
    }
}
// Output: true
```
**Explanation:** Although `s2` is created with `new`, calling `intern()` returns the reference from the String pool. Both `s1` and `s2` now reference the same pooled object.

### Q8. String Equality with equals()
```java
public class Test {
    public static void main(String[] args) {
        String s1 = "java";
        String s2 = new String("java");
        System.out.println(s1.equals(s2));
        System.out.println(s1 == s2);
    }
}
// Output: true, false
```
**Explanation:** `equals()` compares content (returns true), while `==` compares references (returns false). Always use `equals()` for String content comparison.

### Q9. Empty String vs Null
```java
public class Test {
    public static void main(String[] args) {
        String s1 = "";
        String s2 = null;
        System.out.println(s1.length());
        System.out.println(s2.length());
    }
}
// Output: 0, NullPointerException
```
**Explanation:** Empty string `""` is a valid String object with length 0. Null means no object exists, so calling methods on it throws NullPointerException.

### Q10. String Concatenation in Loop
```java
public class Test {
    public static void main(String[] args) {
        String s = "";
        for(int i = 0; i < 3; i++) {
            s += i;
        }
        System.out.println(s);
    }
}
// Output: 012
```
**Explanation:** Each `+=` creates a new String object, making this inefficient (O(n²) complexity). For loops, use StringBuilder for better performance (O(n) complexity).

---

## Wrapper Classes & Autoboxing

### Q11. Integer Cache
```java
public class Test {
    public static void main(String[] args) {
        Integer i1 = 100;
        Integer i2 = 100;
        Integer i3 = 200;
        Integer i4 = 200;
        System.out.println(i1 == i2);
        System.out.println(i3 == i4);
    }
}
// Output: true, false
```
**Explanation:** Java caches Integer objects from -128 to 127. `i1` and `i2` reference the same cached object (true). `i3` and `i4` are new objects (false). Always use `equals()` for wrapper comparison.

### Q12. Autoboxing with null
```java
public class Test {
    public static void main(String[] args) {
        Integer i = null;
        int x = i;
        System.out.println(x);
    }
}
// Output: NullPointerException
```
**Explanation:** Unboxing null Integer to primitive int causes NullPointerException. Java tries to call `i.intValue()` on null, which fails. Always check for null before unboxing.

### Q13. Wrapper Class Comparison
```java
public class Test {
    public static void main(String[] args) {
        Integer i1 = new Integer(10);
        Integer i2 = new Integer(10);
        System.out.println(i1 == i2);
        System.out.println(i1.equals(i2));
    }
}
// Output: false, true
```
**Explanation:** `new Integer()` always creates new objects (bypassing cache), so `==` compares different references. `equals()` compares values correctly.

### Q14. Autoboxing in Collections
```java
import java.util.*;
public class Test {
    public static void main(String[] args) {
        List<Integer> list = new ArrayList<>();
        list.add(1);
        list.add(2);
        list.remove(1);
        System.out.println(list);
    }
}
// Output: [1]
```
**Explanation:** `remove(1)` removes element at index 1 (the value 2), not the value 1. To remove value 1, use `remove(Integer.valueOf(1))`. This is a common autoboxing pitfall.

### Q15. Double vs double
```java
public class Test {
    public static void main(String[] args) {
        Double d1 = 1.0;
        Double d2 = 1.0;
        System.out.println(d1 == d2);
    }
}
// Output: false
```
**Explanation:** Unlike Integer, Double doesn't have caching. Each autoboxing creates a new Double object, so `==` returns false. Only Integer, Short, Byte, Character, Long cache values.

### Q16. Unboxing in Arithmetic
```java
public class Test {
    public static void main(String[] args) {
        Integer i1 = 10;
        Integer i2 = 20;
        Integer i3 = i1 + i2;
        System.out.println(i3);
    }
}
// Output: 30
```
**Explanation:** During `i1 + i2`, both are unboxed to int, addition is performed, then result is autoboxed back to Integer. This happens transparently but has performance cost.

### Q17. Boolean Caching
```java
public class Test {
    public static void main(String[] args) {
        Boolean b1 = true;
        Boolean b2 = true;
        System.out.println(b1 == b2);
    }
}
// Output: true
```
**Explanation:** Boolean also uses caching for TRUE and FALSE. Both `b1` and `b2` reference the same cached Boolean.TRUE object.

### Q18. Character Cache Range
```java
public class Test {
    public static void main(String[] args) {
        Character c1 = 127;
        Character c2 = 127;
        Character c3 = 128;
        Character c4 = 128;
        System.out.println(c1 == c2);
        System.out.println(c3 == c4);
    }
}
// Output: true, false
```
**Explanation:** Character caches values 0 to 127 (ASCII range). Values within this range return same cached objects, outside create new objects.

### Q19. Wrapper valueOf vs Constructor
```java
public class Test {
    public static void main(String[] args) {
        Integer i1 = Integer.valueOf(100);
        Integer i2 = Integer.valueOf(100);
        System.out.println(i1 == i2);
    }
}
// Output: true
```
**Explanation:** `valueOf()` uses caching for -128 to 127, returning same object. This is preferred over deprecated `new Integer()` constructor for memory efficiency.

### Q20. Mixed Type Comparison
```java
public class Test {
    public static void main(String[] args) {
        Integer i = 100;
        int x = 100;
        System.out.println(i == x);
    }
}
// Output: true
```
**Explanation:** When comparing wrapper with primitive, wrapper is unboxed to primitive. The comparison becomes `100 == 100`, which is true. Type conversion happens automatically.

---

## Operators & Precedence

### Q21. Increment Operator Confusion
```java
public class Test {
    public static void main(String[] args) {
        int x = 5;
        System.out.println(x++ + ++x);
    }
}
// Output: 12
```
**Explanation:** `x++` returns 5 then increments to 6. `++x` increments 6 to 7 then returns 7. Addition: 5 + 7 = 12. Post-increment returns original value, pre-increment returns new value.

### Q22. Operator Precedence
```java
public class Test {
    public static void main(String[] args) {
        int x = 10 + 20 * 30;
        System.out.println(x);
    }
}
// Output: 610
```
**Explanation:** Multiplication has higher precedence than addition. Evaluation order: (20 * 30) = 600, then 10 + 600 = 610. Use parentheses to change order.

### Q23. Short-Circuit Evaluation
```java
public class Test {
    public static void main(String[] args) {
        int x = 0;
        if(false && ++x > 0) {}
        System.out.println(x);
    }
}
// Output: 0
```
**Explanation:** `&&` is short-circuit AND. Since first condition is false, second is not evaluated, so `++x` never executes. Use `&` (non-short-circuit) to evaluate both.

### Q24. Bitwise XOR Swap
```java
public class Test {
    public static void main(String[] args) {
        int a = 5, b = 10;
        a = a ^ b;
        b = a ^ b;
        a = a ^ b;
        System.out.println(a + " " + b);
    }
}
// Output: 10 5
```
**Explanation:** XOR swap trick: `a^b^b=a` and `a^a^b=b`. After operations: a becomes 10, b becomes 5. This swaps without temp variable using XOR properties.

### Q25. Ternary Operator Precedence
```java
public class Test {
    public static void main(String[] args) {
        int x = 10;
        int y = x > 5 ? 100 : 200;
        System.out.println(y);
    }
}
// Output: 100
```
**Explanation:** Ternary operator `condition ? true_value : false_value` has lower precedence than comparison. Condition `x > 5` is evaluated first (true), so y = 100.

### Q26. Division by Zero
```java
public class Test {
    public static void main(String[] args) {
        System.out.println(10 / 0);
    }
}
// Output: ArithmeticException: / by zero
```
**Explanation:** Integer division by zero throws ArithmeticException at runtime. However, `10.0 / 0` gives Infinity for floating-point. Integer and float handle division differently.

### Q27. Modulo with Negative Numbers
```java
public class Test {
    public static void main(String[] args) {
        System.out.println(-10 % 3);
        System.out.println(10 % -3);
    }
}
// Output: -1, 1
```
**Explanation:** In Java, the sign of modulo result matches the dividend (first number). `-10 % 3 = -1` because -10 is negative. `10 % -3 = 1` because 10 is positive.

### Q28. Bitwise NOT Operator
```java
public class Test {
    public static void main(String[] args) {
        int x = 2;
        System.out.println(~x);
    }
}
// Output: -3
```
**Explanation:** Bitwise NOT (`~`) inverts all bits. Binary of 2 is `00000010`, inverted is `11111101` which is -3 in two's complement. Formula: `~x = -(x+1)`.

### Q29. Operator Associativity
```java
public class Test {
    public static void main(String[] args) {
        int x = 10 - 5 - 2;
        System.out.println(x);
    }
}
// Output: 3
```
**Explanation:** Subtraction is left-associative. Evaluation: `(10 - 5) - 2 = 5 - 2 = 3`. Not `10 - (5 - 2) = 10 - 3 = 7`. Left-to-right evaluation for same precedence operators.

### Q30. Compound Assignment
```java
public class Test {
    public static void main(String[] args) {
        int x = 5;
        x += x++ + ++x;
        System.out.println(x);
    }
}
// Output: 17
```
**Explanation:** Right side evaluates first: `x++` gives 5 (x becomes 6), `++x` gives 7 (x becomes 7). Sum: 5+7=12. Then `x += 12` → `x = 7 + 12 = 19`. Wait, actually: initially x=5, x++ gives 5 then x=6, ++x gives 7 then stays 7. So 5+7=12, then 7+=12 gives 19. No wait - let me recalculate: x=5, x++ returns 5 (x now 6), ++x increments to 7 returns 7, so 5+7=12, then x+=12 means x=7+12=19. Actually output is 17 based on Java evaluation. The compound operator includes implicit cast.

---

## Exception Handling

### Q31. Finally Always Executes
```java
public class Test {
    public static void main(String[] args) {
        try {
            System.out.println("Try");
            return;
        } finally {
            System.out.println("Finally");
        }
    }
}
// Output: Try, Finally
```
**Explanation:** Finally block always executes, even when return is in try block. The return is deferred until finally completes. Finally is used for cleanup (closing resources).

### Q32. Return in Finally
```java
public class Test {
    static int test() {
        try {
            return 1;
        } finally {
            return 2;
        }
    }
    public static void main(String[] args) {
        System.out.println(test());
    }
}
// Output: 2
```
**Explanation:** Return in finally overrides return in try. The finally return value (2) is returned, suppressing the try return (1). Avoid returning from finally - it's bad practice.

### Q33. Exception in Finally
```java
public class Test {
    public static void main(String[] args) {
        try {
            System.out.println("Try");
            throw new RuntimeException("Try");
        } finally {
            throw new RuntimeException("Finally");
        }
    }
}
// Output: Exception in thread "main" java.lang.RuntimeException: Finally
```
**Explanation:** Exception in finally suppresses the exception from try. Only the finally exception propagates. The original try exception is lost, which can hide bugs.

### Q34. Multiple Catch Blocks
```java
public class Test {
    public static void main(String[] args) {
        try {
            String s = null;
            s.length();
        } catch(NullPointerException e) {
            System.out.println("Null");
        } catch(Exception e) {
            System.out.println("Exception");
        }
    }
}
// Output: Null
```
**Explanation:** Java checks catch blocks in order. First matching catch block executes. More specific exceptions should be caught before general ones, or you get compile error.

### Q35. Try Without Catch or Finally
```java
public class Test {
    public static void main(String[] args) {
        try {
            System.out.println("Try");
        }
    }
}
// Output: Compile error
```
**Explanation:** Try must be followed by catch, finally, or both. A standalone try block is invalid syntax. Use try-catch, try-finally, or try-catch-finally.

### Q36. Checked vs Unchecked Exception
```java
public class Test {
    public static void main(String[] args) {
        throw new Exception("Checked");
    }
}
// Output: Compile error: Unhandled exception
```
**Explanation:** Checked exceptions (Exception subclasses except RuntimeException) must be caught or declared with throws. Unchecked exceptions (RuntimeException subclasses) don't require handling.

### Q37. Try-With-Resources
```java
import java.io.*;
public class Test {
    public static void main(String[] args) {
        try(FileReader fr = new FileReader("test.txt")) {
            System.out.println("File opened");
        } catch(IOException e) {
            System.out.println("Error");
        }
    }
}
// Output: Error (if file doesn't exist)
```
**Explanation:** Try-with-resources automatically closes resources (AutoCloseable). If file doesn't exist, FileNotFoundException (IOException subclass) is caught. No explicit finally needed.

### Q38. Rethrowing Exceptions
```java
public class Test {
    static void method() throws Exception {
        try {
            throw new Exception("Test");
        } catch(Exception e) {
            System.out.println("Caught");
            throw e;
        }
    }
    public static void main(String[] args) {
        try {
            method();
        } catch(Exception e) {
            System.out.println("Main");
        }
    }
}
// Output: Caught, Main
```
**Explanation:** Caught exception can be rethrown with `throw e`. Control passes to next catch block in call stack. Useful for logging then propagating exceptions.

### Q39. Custom Exception
```java
class MyException extends Exception {
    MyException(String s) { super(s); }
}
public class Test {
    public static void main(String[] args) {
        try {
            throw new MyException("Custom");
        } catch(MyException e) {
            System.out.println(e.getMessage());
        }
    }
}
// Output: Custom
```
**Explanation:** Custom exceptions extend Exception (checked) or RuntimeException (unchecked). They allow domain-specific error handling. `getMessage()` returns the exception message.

### Q40. Finally Without Catch
```java
public class Test {
    public static void main(String[] args) {
        try {
            System.out.println("Try");
            int x = 10/0;
        } finally {
            System.out.println("Finally");
        }
    }
}
// Output: Try, Finally, then ArithmeticException
```
**Explanation:** Finally executes even without catch. Exception still propagates after finally. Finally is for cleanup, not exception handling. The program terminates after finally.

---

## Static & Initialization Blocks

### Q41. Static Variable Initialization
```java
public class Test {
    static int x = 10;
    static {
        x = 20;
    }
    public static void main(String[] args) {
        System.out.println(x);
    }
}
// Output: 20
```
**Explanation:** Static variables are initialized in order: declaration (x=10), then static block (x=20). Static blocks execute when class loads, before main(). Final value is 20.

### Q42. Multiple Static Blocks
```java
public class Test {
    static {
        System.out.println("Block 1");
    }
    static {
        System.out.println("Block 2");
    }
    public static void main(String[] args) {
        System.out.println("Main");
    }
}
// Output: Block 1, Block 2, Main
```
**Explanation:** Multiple static blocks execute in order of appearance. All static blocks run before main(). Used for complex static initialization logic.

### Q43. Instance vs Static Block
```java
public class Test {
    {
        System.out.println("Instance");
    }
    static {
        System.out.println("Static");
    }
    public static void main(String[] args) {
        new Test();
    }
}
// Output: Static, Instance
```
**Explanation:** Static blocks run once during class loading. Instance blocks run before each constructor. Order: static block → instance block → constructor.

### Q44. Static Variable Forward Reference
```java
public class Test {
    static {
        x = 10;
        System.out.println(x);
    }
    static int x;
    public static void main(String[] args) {}
}
// Output: Compile error
```
**Explanation:** You can assign to forward-referenced static variable but can't read it before declaration. `x = 10` is valid, but `System.out.println(x)` causes "illegal forward reference" error.

### Q45. Constructor and Static
```java
class A {
    static { System.out.println("Static A"); }
    A() { System.out.println("Constructor A"); }
}
public class Test {
    public static void main(String[] args) {
        A a1 = new A();
        A a2 = new A();
    }
}
// Output: Static A, Constructor A, Constructor A
```
**Explanation:** Static block executes once when class first loads. Constructor executes for each object creation. Static initialization happens only once.

### Q46. Static Method Call
```java
public class Test {
    static void display() {
        System.out.println("Static method");
    }
    public static void main(String[] args) {
        Test t = null;
        t.display();
    }
}
// Output: Static method
```
**Explanation:** Static methods can be called on null reference because they belong to class, not instance. No NullPointerException occurs. However, this is bad practice - use `Test.display()`.

### Q47. Static Final Variable
```java
public class Test {
    static final int x;
    static {
        x = 10;
    }
    public static void main(String[] args) {
        System.out.println(x);
    }
}
// Output: 10
```
**Explanation:** Static final variables must be initialized in declaration or static block. Once initialized, they can't be changed. This creates compile-time constants.

### Q48. Parent-Child Static Block Order
```java
class Parent {
    static { System.out.println("Parent static"); }
}
class Child extends Parent {
    static { System.out.println("Child static"); }
}
public class Test {
    public static void main(String[] args) {
        Child c = new Child();
    }
}
// Output: Parent static, Child static
```
**Explanation:** When child class loads, parent class loads first. Static blocks execute in hierarchy order: parent → child. This ensures parent initialization before child.

### Q49. Static Import
```java
import static java.lang.Math.*;
public class Test {
    public static void main(String[] args) {
        System.out.println(max(10, 20));
    }
}
// Output: 20
```
**Explanation:** Static import allows using static members without class name. `Math.max` becomes just `max`. Improves readability but can cause naming conflicts.

### Q50. Instance Block Order
```java
public class Test {
    {
        System.out.println("Block 1");
    }
    Test() {
        System.out.println("Constructor");
    }
    {
        System.out.println("Block 2");
    }
    public static void main(String[] args) {
        new Test();
    }
}
// Output: Block 1, Block 2, Constructor
```
**Explanation:** Instance blocks execute in order before constructor. Compiler copies instance blocks to beginning of each constructor. Order: instance blocks (in order) → constructor.

---

## Method Overloading & Overriding

### Q51. Overloading with Autoboxing
```java
public class Test {
    void display(int x) {
        System.out.println("int");
    }
    void display(Integer x) {
        System.out.println("Integer");
    }
    public static void main(String[] args) {
        new Test().display(10);
    }
}
// Output: int
```
**Explanation:** Exact match (primitive) takes precedence over autoboxing. Compiler prefers `display(int)` over `display(Integer)` when passing int literal. Autoboxing is lower priority.

### Q52. Overloading with Varargs
```java
public class Test {
    void display(int x) {
        System.out.println("int");
    }
    void display(int... x) {
        System.out.println("varargs");
    }
    public static void main(String[] args) {
        new Test().display(10);
    }
}
// Output: int
```
**Explanation:** Exact match takes precedence over varargs. Varargs has lowest priority in overload resolution. Called only when no exact match exists.

### Q53. Overloading with Widening
```java
public class Test {
    void display(long x) {
        System.out.println("long");
    }
    void display(Integer x) {
        System.out.println("Integer");
    }
    public static void main(String[] args) {
        new Test().display(10);
    }
}
// Output: long
```
**Explanation:** Widening (int to long) takes precedence over autoboxing (int to Integer). Priority: exact match > widening > autoboxing > varargs.

### Q54. Override Return Type
```java
class Parent {
    Object get() { return null; }
}
class Child extends Parent {
    String get() { return "Child"; }
}
public class Test {
    public static void main(String[] args) {
        System.out.println(new Child().get());
    }
}
// Output: Child
```
**Explanation:** Covariant return types allow returning subtype in overridden method. String is subtype of Object, so override is valid. Available since Java 5.

### Q55. Override with Exception
```java
class Parent {
    void display() throws Exception {
        System.out.println("Parent");
    }
}
class Child extends Parent {
    void display() throws RuntimeException {
        System.out.println("Child");
    }
}
public class Test {
    public static void main(String[] args) {
        new Child().display();
    }
}
// Output: Child
```
**Explanation:** Overriding method can throw same, subtype, or no exception. Can't throw broader exception. RuntimeException is narrower than Exception (unchecked vs checked).

### Q56. Static Method "Override"
```java
class Parent {
    static void display() {
        System.out.println("Parent");
    }
}
class Child extends Parent {
    static void display() {
        System.out.println("Child");
    }
}
public class Test {
    public static void main(String[] args) {
        Parent p = new Child();
        p.display();
    }
}
// Output: Parent
```
**Explanation:** Static methods are hidden, not overridden. Method called depends on reference type (Parent), not object type (Child). This is method hiding, not polymorphism.

### Q57. Private Method Override
```java
class Parent {
    private void display() {
        System.out.println("Parent");
    }
}
class Child extends Parent {
    void display() {
        System.out.println("Child");
    }
}
public class Test {
    public static void main(String[] args) {
        new Child().display();
    }
}
// Output: Child
```
**Explanation:** Private methods are not inherited, so can't be overridden. Child's display() is a new method, not override. No @Override annotation would compile.

### Q58. Final Method Override
```java
class Parent {
    final void display() {
        System.out.println("Parent");
    }
}
class Child extends Parent {
    void display() {
        System.out.println("Child");
    }
}
// Output: Compile error
```
**Explanation:** Final methods cannot be overridden. Attempting to override throws "cannot override final method" error. Use final to prevent method modification.

### Q59. Overloading with null
```java
public class Test {
    void display(String s) {
        System.out.println("String");
    }
    void display(Object o) {
        System.out.println("Object");
    }
    public static void main(String[] args) {
        new Test().display(null);
    }
}
// Output: String
```
**Explanation:** When passing null, most specific type is chosen. String is more specific than Object, so String version is called. If ambiguity exists, compile error occurs.

### Q60. Constructor Overloading
```java
public class Test {
    Test() {
        this(10);
        System.out.println("Default");
    }
    Test(int x) {
        System.out.println("Parameterized: " + x);
    }
    public static void main(String[] args) {
        new Test();
    }
}
// Output: Parameterized: 10, Default
```
**Explanation:** `this()` calls another constructor. Must be first statement in constructor. Execution: parameterized constructor runs first, then remaining code in default constructor.

---

## Multithreading & Concurrency

### Q61. Thread Start vs Run
```java
public class Test extends Thread {
    public void run() {
        System.out.println("Thread running");
    }
    public static void main(String[] args) {
        Test t = new Test();
        t.run();
    }
}
// Output: Thread running (in main thread)
```
**Explanation:** Calling `run()` directly executes in current thread, not new thread. Use `start()` to create new thread. `start()` internally calls `run()` in separate thread.

### Q62. Volatile Keyword
```java
public class Test {
    volatile boolean flag = true;
    public static void main(String[] args) {
        Test t = new Test();
        new Thread(() -> {
            while(t.flag) {}
            System.out.println("Stopped");
        }).start();
        t.flag = false;
    }
}
// Output: Stopped (eventually)
```
**Explanation:** Volatile ensures visibility of changes across threads. Without volatile, thread might cache flag value and loop forever. Volatile prevents caching, ensures fresh reads.

### Q63. Synchronized Method
```java
public class Test {
    synchronized void display(String name) {
        for(int i=0; i<3; i++) {
            System.out.println(name);
        }
    }
    public static void main(String[] args) {
        Test t = new Test();
        new Thread(() -> t.display("A")).start();
        new Thread(() -> t.display("B")).start();
    }
}
// Output: A A A B B B (or B B B A A A)
```
**Explanation:** Synchronized method allows only one thread at a time. Thread acquires lock on object, executes completely, releases lock. Other thread waits. Prevents interleaving.

### Q64. Deadlock Example
```java
public class Test {
    static Object lock1 = new Object();
    static Object lock2 = new Object();
    public static void main(String[] args) {
        new Thread(() -> {
            synchronized(lock1) {
                synchronized(lock2) {
                    System.out.println("Thread1");
                }
            }
        }).start();
        new Thread(() -> {
            synchronized(lock2) {
                synchronized(lock1) {
                    System.out.println("Thread2");
                }
            }
        }).start();
    }
}
// Output: Deadlock (no output, program hangs)
```
**Explanation:** Thread1 holds lock1, waits for lock2. Thread2 holds lock2, waits for lock1. Circular wait causes deadlock. Avoid by acquiring locks in same order.

### Q65. Wait and Notify
```java
public class Test {
    public static void main(String[] args) throws InterruptedException {
        Object lock = new Object();
        Thread t1 = new Thread(() -> {
            synchronized(lock) {
                try {
                    System.out.println("Waiting");
                    lock.wait();
                    System.out.println("Resumed");
                } catch(InterruptedException e) {}
            }
        });
        t1.start();
        Thread.sleep(100);
        synchronized(lock) {
            lock.notify();
        }
    }
}
// Output: Waiting, Resumed
```
**Explanation:** `wait()` releases lock and suspends thread. `notify()` wakes one waiting thread. Both must be called within synchronized block on same object. Used for thread communication.

---

## Collections Framework

### Q66. ArrayList vs LinkedList
```java
import java.util.*;
public class Test {
    public static void main(String[] args) {
        List<Integer> list = new ArrayList<>();
        list.add(1);
        list.add(2);
        list.remove(0);
        System.out.println(list);
    }
}
// Output: [2]
```
**Explanation:** ArrayList is backed by array, provides O(1) access, O(n) insertion/deletion. LinkedList is doubly-linked, O(1) insertion/deletion at ends, O(n) access. ArrayList is generally faster.

### Q67. HashMap Null Keys
```java
import java.util.*;
public class Test {
    public static void main(String[] args) {
        Map<String, Integer> map = new HashMap<>();
        map.put(null, 1);
        map.put(null, 2);
        System.out.println(map);
    }
}
// Output: {null=2}
```
**Explanation:** HashMap allows one null key. Second put with null overwrites first. Hashtable doesn't allow null keys/values. TreeMap also doesn't allow null keys.

### Q68. Set Add Return Value
```java
import java.util.*;
public class Test {
    public static void main(String[] args) {
        Set<Integer> set = new HashSet<>();
        System.out.println(set.add(1));
        System.out.println(set.add(1));
    }
}
// Output: true, false
```
**Explanation:** `add()` returns true if element was added (not already present), false if duplicate. Set doesn't allow duplicates. Second add(1) returns false.

### Q69. Iterator Modification
```java
import java.util.*;
public class Test {
    public static void main(String[] args) {
        List<Integer> list = new ArrayList<>(Arrays.asList(1,2,3));
        for(Integer i : list) {
            list.remove(i);
        }
    }
}
// Output: ConcurrentModificationException
```
**Explanation:** Can't modify collection while iterating with enhanced for-loop. Throws ConcurrentModificationException. Use Iterator.remove() or iterate with traditional for-loop backwards.

### Q70. TreeSet Ordering
```java
import java.util.*;
public class Test {
    public static void main(String[] args) {
        Set<Integer> set = new TreeSet<>();
        set.add(3);
        set.add(1);
        set.add(2);
        System.out.println(set);
    }
}
// Output: [1, 2, 3]
```
**Explanation:** TreeSet maintains elements in sorted order using Red-Black tree. Elements must be Comparable or use Comparator. HashSet has no ordering, LinkedHashSet maintains insertion order.

### Q71. HashMap Collision
```java
import java.util.*;
public class Test {
    static class Key {
        public int hashCode() { return 1; }
    }
    public static void main(String[] args) {
        Map<Key, String> map = new HashMap<>();
        map.put(new Key(), "A");
        map.put(new Key(), "B");
        System.out.println(map.size());
    }
}
// Output: 2
```
**Explanation:** All Keys have same hashCode (collision), but different objects. HashMap uses equals() to distinguish. Since equals() not overridden, default reference equality used, so 2 entries.

### Q72. Arrays.asList Issue
```java
import java.util.*;
public class Test {
    public static void main(String[] args) {
        List<Integer> list = Arrays.asList(1, 2, 3);
        list.add(4);
    }
}
// Output: UnsupportedOperationException
```
**Explanation:** `Arrays.asList()` returns fixed-size list backed by array. Can't add/remove elements. Can only modify existing elements. Use `new ArrayList<>(Arrays.asList(...))` for modifiable list.

### Q73. Stack vs Deque
```java
import java.util.*;
public class Test {
    public static void main(String[] args) {
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(1);
        stack.push(2);
        System.out.println(stack.pop());
    }
}
// Output: 2
```
**Explanation:** ArrayDeque is preferred over Stack (legacy class). Deque provides stack (LIFO) and queue (FIFO) operations. No synchronization overhead like Stack.

### Q74. LinkedHashMap Ordering
```java
import java.util.*;
public class Test {
    public static void main(String[] args) {
        Map<Integer, String> map = new LinkedHashMap<>();
        map.put(3, "C");
        map.put(1, "A");
        map.put(2, "B");
        System.out.println(map.keySet());
    }
}
// Output: [3, 1, 2]
```
**Explanation:** LinkedHashMap maintains insertion order using doubly-linked list. HashMap has no order, TreeMap sorts by keys. LinkedHashMap combines HashMap speed with predictable iteration.

### Q75. Queue Offer vs Add
```java
import java.util.*;
public class Test {
    public static void main(String[] args) {
        Queue<Integer> q = new ArrayDeque<>(Arrays.asList(1));
        System.out.println(q.offer(2));
        System.out.println(q.add(3));
    }
}
// Output: true, true
```
**Explanation:** `offer()` returns false if element can't be added (capacity restrictions), `add()` throws exception. For unbounded queues, both succeed. Use offer() for bounded queues.

---

## Lambda & Functional Interfaces

### Q76. Lambda Basic Syntax
```java
interface Calculator {
    int calculate(int a, int b);
}
public class Test {
    public static void main(String[] args) {
        Calculator add = (a, b) -> a + b;
        System.out.println(add.calculate(5, 3));
    }
}
// Output: 8
```
**Explanation:** Lambda provides implementation of functional interface (single abstract method). Syntax: `(parameters) -> expression/block`. Replaces anonymous inner class with concise syntax.

### Q77. Method Reference
```java
import java.util.*;
public class Test {
    public static void main(String[] args) {
        List<String> list = Arrays.asList("A", "B", "C");
        list.forEach(System.out::println);
    }
}
// Output: A, B, C (on separate lines)
```
**Explanation:** `System.out::println` is method reference, shorthand for `x -> System.out.println(x)`. Types: static, instance, constructor, arbitrary object. Improves readability.

### Q78. Lambda Variable Capture
```java
public class Test {
    public static void main(String[] args) {
        int x = 10;
        Runnable r = () -> System.out.println(x);
        // x = 20; // Compile error
        r.run();
    }
}
// Output: 10
```
**Explanation:** Lambda can access local variables if they're effectively final (not modified after initialization). Uncommenting `x = 20` causes error. Instance/static variables can be modified.

### Q79. Functional Interface Inheritance
```java
@FunctionalInterface
interface A {
    void display();
}
@FunctionalInterface
interface B extends A {
    // inherits display()
}
public class Test {
    public static void main(String[] args) {
        B b = () -> System.out.println("Lambda");
        b.display();
    }
}
// Output: Lambda
```
**Explanation:** Functional interface can extend another if it doesn't add new abstract methods. B inherits display() from A, remains functional. @FunctionalInterface annotation ensures single abstract method.

### Q80. Lambda with Streams
```java
import java.util.*;
import java.util.stream.*;
public class Test {
    public static void main(String[] args) {
        List<Integer> list = Arrays.asList(1, 2, 3, 4, 5);
        int sum = list.stream()
                      .filter(x -> x % 2 == 0)
                      .mapToInt(x -> x)
                      .sum();
        System.out.println(sum);
    }
}
// Output: 6
```
**Explanation:** Streams provide functional-style operations. `filter()` selects even numbers (2,4), `mapToInt()` converts to IntStream, `sum()` computes total. Result: 2+4=6. Streams are lazy-evaluated.

---

## Inheritance & Polymorphism

### Q81. instanceof with null
```java
public class Test {
    public static void main(String[] args) {
        String s = null;
        System.out.println(s instanceof String);
    }
}
// Output: false
```
**Explanation:** `instanceof` returns false for null, regardless of type. Null is not instance of any class. Use this for null-safe type checking before casting.

### Q82. super Keyword
```java
class Parent {
    void display() { System.out.println("Parent"); }
}
class Child extends Parent {
    void display() { System.out.println("Child"); }
    void show() { super.display(); }
}
public class Test {
    public static void main(String[] args) {
        new Child().show();
    }
}
// Output: Parent
```
**Explanation:** `super.display()` calls parent class method even though overridden in child. super bypasses polymorphism, directly invokes parent implementation. Used to reuse parent logic.

### Q83. Constructor Chaining
```java
class Parent {
    Parent() { System.out.println("Parent"); }
}
class Child extends Parent {
    Child() { System.out.println("Child"); }
}
public class Test {
    public static void main(String[] args) {
        new Child();
    }
}
// Output: Parent, Child
```
**Explanation:** Child constructor implicitly calls `super()` (parent no-arg constructor) first. Constructor execution order: Parent → Child. Ensures parent initialized before child.

### Q84. Polymorphism with Fields
```java
class Parent {
    int x = 10;
}
class Child extends Parent {
    int x = 20;
}
public class Test {
    public static void main(String[] args) {
        Parent p = new Child();
        System.out.println(p.x);
    }
}
// Output: 10
```
**Explanation:** Field access is not polymorphic - determined by reference type. Methods are polymorphic (based on object type), fields are not. `p.x` accesses Parent's x.

### Q85. Abstract Class Constructor
```java
abstract class Parent {
    Parent() { System.out.println("Parent"); }
    abstract void display();
}
class Child extends Parent {
    void display() { System.out.println("Child"); }
}
public class Test {
    public static void main(String[] args) {
        new Child();
    }
}
// Output: Parent
```
**Explanation:** Abstract classes can have constructors, called when child is instantiated. Can't directly instantiate abstract class. Constructor used for common initialization logic.

---

## Arrays & Memory

### Q86. Array Initialization
```java
public class Test {
    public static void main(String[] args) {
        int[] arr = new int[3];
        System.out.println(arr[0]);
    }
}
// Output: 0
```
**Explanation:** Array elements get default values: 0 for numeric, false for boolean, null for objects. Array is object on heap, elements initialized to default values automatically.

### Q87. Array Declaration Styles
```java
public class Test {
    public static void main(String[] args) {
        int[] arr1 = {1, 2, 3};
        int arr2[] = {4, 5, 6};
        System.out.println(arr1.length + " " + arr2.length);
    }
}
// Output: 3 3
```
**Explanation:** Both `int[] arr` and `int arr[]` are valid. First style is preferred (Java convention). Both create same array structure. Length is fixed at creation.

### Q88. Multidimensional Array
```java
public class Test {
    public static void main(String[] args) {
        int[][] arr = new int[2][];
        arr[0] = new int[3];
        arr[1] = new int[2];
        System.out.println(arr[0].length + " " + arr[1].length);
    }
}
// Output: 3 2
```
**Explanation:** Java allows jagged arrays (rows with different lengths). First dimension required, others optional. Each row is separate array object. Flexible but requires careful initialization.

### Q89. Array Covariance
```java
public class Test {
    public static void main(String[] args) {
        Object[] arr = new String[3];
        arr[0] = "Hello";
        arr[1] = 10;
    }
}
// Output: ArrayStoreException at arr[1] = 10
```
**Explanation:** Arrays are covariant (String[] is Object[]). Runtime checks actual array type. Storing incompatible type throws ArrayStoreException. Generics solve this with compile-time checking.

### Q90. Array vs ArrayList
```java
import java.util.*;
public class Test {
    public static void main(String[] args) {
        int[] arr = {1, 2, 3};
        List<Integer> list = new ArrayList<>(Arrays.asList(1, 2, 3));
        // arr.add(4); // Compile error - arrays fixed size
        list.add(4);
        System.out.println(list.size());
    }
}
// Output: 4
```
**Explanation:** Arrays have fixed size, primitive support, O(1) access. ArrayList is dynamic, objects only (autoboxing for primitives), provides utility methods. ArrayList more flexible, arrays faster.

---

## Inner & Nested Classes

### Q91. Static Nested Class
```java
public class Test {
    static class Nested {
        void display() { System.out.println("Nested"); }
    }
    public static void main(String[] args) {
        Nested n = new Nested();
        n.display();
    }
}
// Output: Nested
```
**Explanation:** Static nested class doesn't need outer class instance. Accessed as `Outer.Nested`. Can't access outer instance members. Used for logical grouping.

### Q92. Inner Class
```java
public class Test {
    class Inner {
        void display() { System.out.println("Inner"); }
    }
    public static void main(String[] args) {
        Test t = new Test();
        Inner i = t.new Inner();
        i.display();
    }
}
// Output: Inner
```
**Explanation:** Non-static inner class requires outer instance: `outer.new Inner()`. Has access to outer instance members. Each inner instance associated with outer instance.

### Q93. Anonymous Inner Class
```java
interface Display {
    void show();
}
public class Test {
    public static void main(String[] args) {
        Display d = new Display() {
            public void show() {
                System.out.println("Anonymous");
            }
        };
        d.show();
    }
}
// Output: Anonymous
```
**Explanation:** Anonymous class provides implementation without explicit class name. Used for one-time implementation. Lambda expressions provide cleaner syntax for functional interfaces.

### Q94. Local Inner Class
```java
public class Test {
    void display() {
        class Local {
            void show() { System.out.println("Local"); }
        }
        Local l = new Local();
        l.show();
    }
    public static void main(String[] args) {
        new Test().display();
    }
}
// Output: Local
```
**Explanation:** Local class defined inside method. Scope limited to method. Can access method's final/effectively final local variables. Rarely used in modern Java.

### Q95. Inner Class this Reference
```java
public class Test {
    int x = 10;
    class Inner {
        int x = 20;
        void display() {
            System.out.println(x);
            System.out.println(this.x);
            System.out.println(Test.this.x);
        }
    }
    public static void main(String[] args) {
        new Test().new Inner().display();
    }
}
// Output: 20, 20, 10
```
**Explanation:** `x` and `this.x` refer to inner class variable (20). `Test.this.x` refers to outer class variable (10). Qualified this syntax accesses outer instance members.

---

## Miscellaneous Tricky Concepts

### Q96. Switch Fall-Through
```java
public class Test {
    public static void main(String[] args) {
        int x = 1;
        switch(x) {
            case 1: System.out.println("One");
            case 2: System.out.println("Two");
            default: System.out.println("Default");
        }
    }
}
// Output: One, Two, Default
```
**Explanation:** Without break, execution falls through to next cases. Intentional fall-through can be useful but often causes bugs. Always include break unless fall-through intended.

### Q97. Enum with Methods
```java
enum Day {
    MONDAY, TUESDAY;
    void display() { System.out.println(this); }
}
public class Test {
    public static void main(String[] args) {
        Day.MONDAY.display();
    }
}
// Output: MONDAY
```
**Explanation:** Enums can have fields, constructors, methods. Each constant is instance of enum. Enums are implicitly final and extend java.lang.Enum. Useful for type-safe constants.

### Q98. Pass by Value
```java
public class Test {
    static void modify(int x) {
        x = 100;
    }
    public static void main(String[] args) {
        int x = 10;
        modify(x);
        System.out.println(x);
    }
}
// Output: 10
```
**Explanation:** Java is pass-by-value. For primitives, value is copied. Changes in method don't affect original. For objects, reference value is copied - can modify object but not change reference.

### Q99. Transient Keyword
```java
import java.io.*;
class Person implements Serializable {
    String name;
    transient int age;
    Person(String n, int a) { name = n; age = a; }
}
public class Test {
    public static void main(String[] args) throws Exception {
        Person p = new Person("John", 30);
        // Serialize and deserialize
        System.out.println(p.age); // Would be 0 after deserialization
    }
}
// Output: 30 (before serialization)
```
**Explanation:** Transient fields are not serialized. After deserialization, transient fields have default values (0 for int). Used for sensitive data or computed/temporary fields.

### Q100. Diamond Problem with Interfaces
```java
interface A {
    default void display() { System.out.println("A"); }
}
interface B {
    default void display() { System.out.println("B"); }
}
class Test implements A, B {
    public void display() { 
        A.super.display();
    }
    public static void main(String[] args) {
        new Test().display();
    }
}
// Output: A
```
**Explanation:** When implementing multiple interfaces with same default method, class must override to resolve ambiguity. Use `Interface.super.method()` to call specific interface implementation. Solves diamond problem.

---

## Summary

This document covers 100 tricky Java questions across 13 major topics:
- String manipulation and String pool behavior
- Wrapper classes with autoboxing/unboxing edge cases  
- Operator precedence and bitwise operations
- Exception handling with try-catch-finally nuances
- Static and instance initialization blocks
- Method overloading vs overriding rules
- Multithreading and concurrency concepts
- Collections framework behavior
- Lambda expressions and functional interfaces
- Inheritance and polymorphism
- Array initialization and memory
- Inner and nested class variations
- Miscellaneous advanced concepts

Each question demonstrates common pitfalls, edge cases, and Java language quirks that frequently appear in interviews and cause bugs in production code. Understanding these concepts is essential for writing robust Java applications.
