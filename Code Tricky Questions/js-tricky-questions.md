# 100 JavaScript Tricky Code Questions with Outputs

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Type Coercion & Equality](#type-coercion-equality)
  - [Question 1](#question-1)
  - [Question 2](#question-2)
  - [Question 3](#question-3)
  - [Question 4](#question-4)
  - [Question 5](#question-5)
  - [Question 6](#question-6)
  - [Question 7](#question-7)
  - [Question 8](#question-8)
  - [Question 9](#question-9)
  - [Question 10](#question-10)
  - [Question 11](#question-11)
  - [Question 12](#question-12)
  - [Question 13](#question-13)
  - [Question 14](#question-14)
  - [Question 15](#question-15)
- [Hoisting](#hoisting)
  - [Question 16](#question-16)
  - [Question 17](#question-17)
  - [Question 18](#question-18)
  - [Question 19](#question-19)
  - [Question 20](#question-20)
  - [Question 21](#question-21)
  - [Question 22](#question-22)
  - [Question 23](#question-23)
  - [Question 24](#question-24)
  - [Question 25](#question-25)
- [Scope & Closures](#scope-closures)
  - [Question 26](#question-26)
  - [Question 27](#question-27)
  - [Question 28](#question-28)
  - [Question 29](#question-29)
  - [Question 30](#question-30)
  - [Question 31](#question-31)
  - [Question 32](#question-32)
  - [Question 33](#question-33)
  - [Question 34](#question-34)
  - [Question 35](#question-35)
- [this Keyword](#this-keyword)
  - [Question 36](#question-36)
  - [Question 37](#question-37)
  - [Question 38](#question-38)
  - [Question 39](#question-39)
  - [Question 40](#question-40)
  - [Question 41](#question-41)
  - [Question 42](#question-42)
  - [Question 43](#question-43)
  - [Question 44](#question-44)
  - [Question 45](#question-45)
- [Objects & Prototypes](#objects-prototypes)
  - [Question 46](#question-46)
  - [Question 47](#question-47)
  - [Question 48](#question-48)
  - [Question 49](#question-49)
  - [Question 50](#question-50)
  - [Question 51](#question-51)
  - [Question 52](#question-52)
  - [Question 53](#question-53)
  - [Question 54](#question-54)
  - [Question 55](#question-55)
- [Arrays](#arrays)
  - [Question 56](#question-56)
  - [Question 57](#question-57)
  - [Question 58](#question-58)
  - [Question 59](#question-59)
  - [Question 60](#question-60)
  - [Question 61](#question-61)
  - [Question 62](#question-62)
  - [Question 63](#question-63)
  - [Question 64](#question-64)
  - [Question 65](#question-65)
- [Functions](#functions)
  - [Question 66](#question-66)
  - [Question 67](#question-67)
  - [Question 68](#question-68)
  - [Question 69](#question-69)
  - [Question 70](#question-70)
  - [Question 71](#question-71)
  - [Question 72](#question-72)
  - [Question 73](#question-73)
  - [Question 74](#question-74)
  - [Question 75](#question-75)
- [Asynchronous JavaScript](#asynchronous-javascript)
  - [Question 76](#question-76)
  - [Question 77](#question-77)
  - [Question 78](#question-78)
  - [Question 79](#question-79)
  - [Question 80](#question-80)
  - [Question 81](#question-81)
  - [Question 82](#question-82)
  - [Question 83](#question-83)
  - [Question 84](#question-84)
  - [Question 85](#question-85)
- [Operators & Expressions](#operators-expressions)
  - [Question 86](#question-86)
  - [Question 87](#question-87)
  - [Question 88](#question-88)
  - [Question 89](#question-89)
  - [Question 90](#question-90)
  - [Question 91](#question-91)
  - [Question 92](#question-92)
  - [Question 93](#question-93)
  - [Question 94](#question-94)
  - [Question 95](#question-95)
- [Miscellaneous](#miscellaneous)
  - [Question 96](#question-96)
  - [Question 97](#question-97)
  - [Question 98](#question-98)
  - [Question 99](#question-99)
  - [Question 100](#question-100)
- [Summary](#summary)

## Type Coercion & Equality

### Question 1
```javascript
console.log([] + []);
// Output: ""
```
**Explanation:** When the `+` operator is used with arrays, JavaScript converts them to strings. Empty array converts to empty string, so `"" + ""` results in `""`.

### Question 2
```javascript
console.log([] + {});
// Output: "[object Object]"
```
**Explanation:** Empty array converts to `""`, and empty object converts to `"[object Object]"`. String concatenation results in `"[object Object]"`.

### Question 3
```javascript
console.log({} + []);
// Output: 0 (in most browsers when run as statement)
// Output: "[object Object]" (when run as expression)
```
**Explanation:** When `{}` appears at the beginning of a statement, it's interpreted as an empty code block (not an object). Then `+[]` converts empty array to number 0. In expression context, it concatenates as strings.

### Question 4
```javascript
console.log(true + false);
// Output: 1
```
**Explanation:** Boolean values are converted to numbers in arithmetic operations. `true` becomes 1, `false` becomes 0. So `1 + 0 = 1`.

### Question 5
```javascript
console.log("5" + 3);
// Output: "53"
```
**Explanation:** When `+` operator has a string operand, JavaScript performs string concatenation. Number 3 is converted to string "3".

### Question 6
```javascript
console.log("5" - 3);
// Output: 2
```
**Explanation:** The `-` operator only works with numbers, so JavaScript converts "5" to number 5, then performs `5 - 3 = 2`.

### Question 7
```javascript
console.log(null == undefined);
// Output: true
```
**Explanation:** In loose equality (`==`), `null` and `undefined` are considered equal to each other and nothing else.

### Question 8
```javascript
console.log(null === undefined);
// Output: false
```
**Explanation:** Strict equality (`===`) checks both value and type. `null` and `undefined` are different types, so they're not strictly equal.

### Question 9
```javascript
console.log("" == 0);
// Output: true
```
**Explanation:** Empty string is converted to number 0 in loose equality comparison, so `0 == 0` is true.

### Question 10
```javascript
console.log("" === 0);
// Output: false
```
**Explanation:** Strict equality checks type. String and number are different types, so this is false.

### Question 11
```javascript
console.log(false == "0");
// Output: true
```
**Explanation:** Both sides are converted to numbers: `false` becomes 0, `"0"` becomes 0. So `0 == 0` is true.

### Question 12
```javascript
console.log(false === "0");
// Output: false
```
**Explanation:** Boolean and string are different types, so strict equality returns false.

### Question 13
```javascript
console.log(NaN == NaN);
// Output: false
```
**Explanation:** `NaN` is the only value in JavaScript that is not equal to itself. This is defined by IEEE 754 floating-point standard.

### Question 14
```javascript
console.log(typeof NaN);
// Output: "number"
```
**Explanation:** Despite its name "Not a Number", `NaN` is of type "number". It represents an invalid number value.

### Question 15
```javascript
console.log(1 < 2 < 3);
// Output: true
console.log(3 > 2 > 1);
// Output: false
```
**Explanation:** Operations are evaluated left to right. First: `1 < 2` is `true`, then `true < 3` converts `true` to 1, so `1 < 3` is true. Second: `3 > 2` is `true`, then `true > 1` converts to `1 > 1` which is false.

---

## Hoisting

### Question 16
```javascript
console.log(x);
var x = 5;
// Output: undefined
```
**Explanation:** Variable declarations are hoisted to the top, but not their assignments. So `var x` is hoisted, making x defined but `undefined` before the assignment.

### Question 17
```javascript
console.log(y);
let y = 5;
// Output: ReferenceError: Cannot access 'y' before initialization
```
**Explanation:** `let` and `const` are hoisted but not initialized. They remain in the "temporal dead zone" until the declaration is reached.

### Question 18
```javascript
foo();
function foo() {
  console.log("Hello");
}
// Output: "Hello"
```
**Explanation:** Function declarations are fully hoisted (both declaration and definition), so they can be called before they appear in code.

### Question 19
```javascript
bar();
var bar = function() {
  console.log("Hello");
};
// Output: TypeError: bar is not a function
```
**Explanation:** This is a function expression assigned to a variable. Only the variable declaration is hoisted (as `undefined`), not the function assignment.

### Question 20
```javascript
var a = 1;
function test() {
  console.log(a);
  var a = 2;
}
test();
// Output: undefined
```
**Explanation:** The `var a` inside the function is hoisted to the top of the function scope, shadowing the outer `a`. It's declared but not yet assigned when logged.

### Question 21
```javascript
console.log(foo);
var foo = function() {};
// Output: undefined
```
**Explanation:** Variable `foo` is hoisted but the function expression assignment happens later, so `foo` is `undefined` at the point of logging.

### Question 22
```javascript
function test() {
  console.log(a);
  console.log(foo());
  var a = 1;
  function foo() {
    return 2;
  }
}
test();
// Output: undefined
// Output: 2
```
**Explanation:** `var a` is hoisted as `undefined`. Function `foo` is fully hoisted, so it can be called and returns 2.

### Question 23
```javascript
var x = 10;
function test() {
  console.log(x);
  if (false) {
    var x = 20;
  }
}
test();
// Output: undefined
```
**Explanation:** `var x` inside the function is hoisted regardless of the `if` condition being false. It shadows the outer `x` and is `undefined` at log time.

### Question 24
```javascript
console.log(typeof foo);
var foo = function() {};
// Output: "undefined"
```
**Explanation:** Variable `foo` is hoisted but not initialized with the function yet, so `typeof foo` is `"undefined"`.

### Question 25
```javascript
function outer() {
  console.log(inner);
  function inner() {}
}
outer();
// Output: [Function: inner]
```
**Explanation:** Function declaration `inner` is fully hoisted within `outer`, so it's accessible before its declaration line.

---

## Scope & Closures

### Question 26
```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0);
}
// Output: 3 3 3
```
**Explanation:** `var` has function scope. All three timeouts share the same `i`, which becomes 3 after the loop completes. The callbacks execute after the loop finishes.

### Question 27
```javascript
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0);
}
// Output: 0 1 2
```
**Explanation:** `let` has block scope. Each iteration creates a new binding of `i`, so each callback captures its own value.

### Question 28
```javascript
function makeCounter() {
  let count = 0;
  return function() {
    return ++count;
  };
}
const counter = makeCounter();
console.log(counter());
console.log(counter());
// Output: 1
// Output: 2
```
**Explanation:** The inner function forms a closure over `count`, maintaining access to it even after `makeCounter` returns. Each call increments the same `count`.

### Question 29
```javascript
let x = 10;
function foo() {
  console.log(x);
}
function bar() {
  let x = 20;
  foo();
}
bar();
// Output: 10
```
**Explanation:** Functions use lexical scoping. `foo` was defined in the scope where `x` is 10, not where it's called, so it accesses the outer `x`.

### Question 30
```javascript
function test() {
  console.log(a);
  console.log(b);
  var a = 10;
  let b = 20;
}
test();
// Output: undefined
// Output: ReferenceError: Cannot access 'b' before initialization
```
**Explanation:** `var a` is hoisted and initialized as `undefined`. `let b` is hoisted but remains in temporal dead zone until its declaration.

### Question 31
```javascript
const funcs = [];
for (var i = 0; i < 3; i++) {
  funcs[i] = function() {
    return i;
  };
}
console.log(funcs[0]());
// Output: 3
```
**Explanation:** All functions share the same `i` due to `var`'s function scope. After loop completion, `i` is 3, so all functions return 3.

### Question 32
```javascript
function outer() {
  let x = 10;
  return function inner() {
    console.log(x);
    let x = 20;
  };
}
outer()();
// Output: ReferenceError: Cannot access 'x' before initialization
```
**Explanation:** The inner `let x` creates a new binding that shadows the outer `x`. Due to temporal dead zone, accessing `x` before its declaration throws an error.

### Question 33
```javascript
var a = 1;
function test() {
  a = 10;
  return;
  function a() {}
}
test();
console.log(a);
// Output: 1
```
**Explanation:** Function declaration `function a()` is hoisted, creating a local variable `a` in function scope. Assignment `a = 10` modifies the local `a`, not the global one.

### Question 34
```javascript
function createFunctions() {
  var result = [];
  for (var i = 0; i < 3; i++) {
    result.push((function(x) {
      return function() {
        return x;
      };
    })(i));
  }
  return result;
}
const funcs = createFunctions();
console.log(funcs[0]());
// Output: 0
```
**Explanation:** IIFE creates a new scope for each iteration, passing `i` as `x`. Each returned function closes over its own `x` value.

### Question 35
```javascript
let x = 1;
{
  let x = 2;
  {
    let x = 3;
    console.log(x);
  }
  console.log(x);
}
console.log(x);
// Output: 3
// Output: 2
// Output: 1
```
**Explanation:** Each block creates a new scope with its own `x` binding. Inner blocks shadow outer ones, but each scope maintains its own value.

---

## this Keyword

### Question 36
```javascript
const obj = {
  name: "Alice",
  getName: function() {
    return this.name;
  }
};
const getName = obj.getName;
console.log(getName());
// Output: undefined (in non-strict mode) or TypeError (in strict mode)
```
**Explanation:** When method is extracted and called without context, `this` becomes the global object (or `undefined` in strict mode), which doesn't have a `name` property.

### Question 37
```javascript
const obj = {
  name: "Alice",
  getName: () => {
    return this.name;
  }
};
console.log(obj.getName());
// Output: undefined
```
**Explanation:** Arrow functions don't have their own `this`. They inherit `this` from the enclosing scope (global scope here), where `this.name` is undefined.

### Question 38
```javascript
function Person(name) {
  this.name = name;
  setTimeout(function() {
    console.log(this.name);
  }, 100);
}
new Person("Alice");
// Output: undefined (after 100ms)
```
**Explanation:** Regular function in `setTimeout` has its own `this` which refers to global object (or `undefined` in strict mode), not the Person instance.

### Question 39
```javascript
function Person(name) {
  this.name = name;
  setTimeout(() => {
    console.log(this.name);
  }, 100);
}
new Person("Alice");
// Output: "Alice" (after 100ms)
```
**Explanation:** Arrow function doesn't have its own `this`, so it uses `this` from the constructor, which refers to the new Person instance.

### Question 40
```javascript
const obj = {
  value: 42,
  getValue: function() {
    return this.value;
  }
};
console.log((obj.getValue)());
console.log((obj.getValue, obj.getValue)());
// Output: 42
// Output: undefined
```
**Explanation:** First call: parentheses don't change context, method is called on `obj`. Second call: comma operator returns the function without context, so `this` is global.

### Question 41
```javascript
const obj1 = {
  name: "obj1",
  getName() {
    return this.name;
  }
};
const obj2 = { name: "obj2" };
obj2.getName = obj1.getName;
console.log(obj2.getName());
// Output: "obj2"
```
**Explanation:** `this` is determined by how a function is called, not where it's defined. When called as `obj2.getName()`, `this` refers to `obj2`.

### Question 42
```javascript
function foo() {
  console.log(this.a);
}
const obj = { a: 2, foo };
const bar = obj.foo;
bar();
// Output: undefined (or error in strict mode)
```
**Explanation:** `bar` is called without any object context, so `this` defaults to global object (or `undefined` in strict mode).

### Question 43
```javascript
const obj = {
  a: 1,
  b: function() {
    console.log(this.a);
    function inner() {
      console.log(this.a);
    }
    inner();
  }
};
obj.b();
// Output: 1
// Output: undefined
```
**Explanation:** First call: `this` in method `b` refers to `obj`. Second call: `inner` is called without context, so `this` is global object.

### Question 44
```javascript
const obj = {
  value: 10,
  increment: function() {
    this.value++;
  }
};
const inc = obj.increment;
inc();
console.log(obj.value);
// Output: 10
```
**Explanation:** `inc()` is called without context, so `this` is global object. It tries to increment `global.value`, not `obj.value`, leaving `obj.value` unchanged.

### Question 45
```javascript
class MyClass {
  constructor() {
    this.value = 42;
  }
  getValue = () => {
    return this.value;
  }
}
const obj = new MyClass();
const getValue = obj.getValue;
console.log(getValue());
// Output: 42
```
**Explanation:** Arrow function as class field binds `this` to the instance permanently. Even when extracted, it maintains reference to the instance.

---

## Objects & Prototypes

### Question 46
```javascript
const obj = { a: 1 };
const obj2 = obj;
obj2.a = 2;
console.log(obj.a);
// Output: 2
```
**Explanation:** Objects are assigned by reference. `obj2` points to the same object as `obj`, so modifying `obj2.a` also changes `obj.a`.

### Question 47
```javascript
const obj = { a: 1 };
Object.freeze(obj);
obj.a = 2;
console.log(obj.a);
// Output: 1
```
**Explanation:** `Object.freeze()` makes an object immutable. Attempts to modify it fail silently (or throw error in strict mode).

### Question 48
```javascript
const obj = { a: { b: 1 } };
Object.freeze(obj);
obj.a.b = 2;
console.log(obj.a.b);
// Output: 2
```
**Explanation:** `Object.freeze()` is shallow. It freezes the object itself but not nested objects. `obj.a` is still mutable.

### Question 49
```javascript
console.log("a" in { a: undefined });
// Output: true
console.log({ a: undefined }.hasOwnProperty("a"));
// Output: true
```
**Explanation:** Both `in` operator and `hasOwnProperty` check for property existence, not value. The property exists even though its value is `undefined`.

### Question 50
```javascript
const obj = Object.create(null);
console.log(obj.toString);
// Output: undefined
```
**Explanation:** `Object.create(null)` creates an object without a prototype chain, so it doesn't inherit methods like `toString` from Object.prototype.

### Question 51
```javascript
function Person(name) {
  this.name = name;
}
Person.prototype.getName = function() {
  return this.name;
};
const p = new Person("Alice");
console.log(p.getName());
console.log(p.hasOwnProperty("getName"));
// Output: "Alice"
// Output: false
```
**Explanation:** `getName` exists on the prototype, not on the instance itself. `hasOwnProperty` returns false for inherited properties.

### Question 52
```javascript
const obj = { a: 1 };
console.log(obj.b);
// Output: undefined
```
**Explanation:** Accessing non-existent property returns `undefined`, not an error.

### Question 53
```javascript
const obj = { a: 1, b: 2, a: 3 };
console.log(obj.a);
// Output: 3
```
**Explanation:** Duplicate keys in object literals are allowed. The last value overwrites previous ones.

### Question 54
```javascript
const key = "name";
const obj = { [key]: "Alice" };
console.log(obj.name);
// Output: "Alice"
```
**Explanation:** Computed property names (using brackets) evaluate the expression and use the result as the property key.

### Question 55
```javascript
const obj = { a: 1 };
delete obj.a;
console.log(obj.a);
// Output: undefined
```
**Explanation:** `delete` operator removes the property from the object. Accessing it afterwards returns `undefined`.

---

## Arrays

### Question 56
```javascript
const arr = [1, 2, 3];
arr[10] = 99;
console.log(arr.length);
console.log(arr[5]);
// Output: 11
// Output: undefined
```
**Explanation:** Setting an element beyond current length extends the array, creating "holes" (empty slots). Holes return `undefined` when accessed.

### Question 57
```javascript
const arr = [1, 2, 3];
arr.length = 0;
console.log(arr);
// Output: []
```
**Explanation:** Setting `length` to 0 truncates the array, removing all elements.

### Question 58
```javascript
console.log([1, 2, 3] + [4, 5, 6]);
// Output: "1,2,34,5,6"
```
**Explanation:** Arrays are converted to strings when using `+`. `[1,2,3]` becomes `"1,2,3"`, and string concatenation produces `"1,2,34,5,6"`.

### Question 59
```javascript
const arr = [1, 2, 3];
console.log(arr.map(parseInt));
// Output: [1, NaN, NaN]
```
**Explanation:** `map` passes three arguments: element, index, array. `parseInt` accepts value and radix. So it becomes `parseInt(1, 0)`, `parseInt(2, 1)`, `parseInt(3, 2)`. Only first works correctly.

### Question 60
```javascript
console.log([1, 2, 3].map(x => x * 2).length);
// Output: 3
```
**Explanation:** `map` creates a new array with the same length as the original, applying the function to each element.

### Question 61
```javascript
const arr = [1, 2, 3];
arr.push(4);
console.log(arr);
// Output: [1, 2, 3, 4]
```
**Explanation:** `push` adds element(s) to the end of the array and modifies it in place.

### Question 62
```javascript
console.log(Array(3));
console.log(Array(1, 2, 3));
// Output: [<3 empty items>] or [ , , ]
// Output: [1, 2, 3]
```
**Explanation:** `Array(n)` with one numeric argument creates an array with n empty slots. `Array(a, b, c)` creates an array with those elements.

### Question 63
```javascript
const arr = [1, 2, 3];
delete arr[1];
console.log(arr);
console.log(arr.length);
// Output: [1, <1 empty item>, 3] or [1, , 3]
// Output: 3
```
**Explanation:** `delete` removes the element but creates a hole. It doesn't change the array length.

### Question 64
```javascript
console.log([1, 2, 3].reverse());
console.log([1, 2, 3]);
// Output: [3, 2, 1]
// Output: [1, 2, 3]
```
**Explanation:** First call: `reverse()` modifies the array in place and returns it. Second call: this is a new array, unaffected by the first.

### Question 65
```javascript
const arr = [1, 2, 3, 4, 5];
console.log(arr.slice(1, 3));
console.log(arr);
// Output: [2, 3]
// Output: [1, 2, 3, 4, 5]
```
**Explanation:** `slice` returns a shallow copy of a portion without modifying the original array. It extracts from index 1 up to (but not including) index 3.

---

## Functions

### Question 66
```javascript
function sum(a, b) {
  return a + b;
}
console.log(sum(1, 2, 3, 4));
// Output: 3
```
**Explanation:** JavaScript doesn't enforce parameter count. Extra arguments are ignored. Only `a` and `b` are used, resulting in `1 + 2 = 3`.

### Question 67
```javascript
function test() {
  return
  {
    value: 42
  };
}
console.log(test());
// Output: undefined
```
**Explanation:** Automatic Semicolon Insertion (ASI) adds a semicolon after `return`, making it return `undefined`. The object literal is unreachable.

### Question 68
```javascript
console.log(typeof function() {});
// Output: "function"
```
**Explanation:** Functions have their own type. `typeof` returns `"function"` for function objects.

### Question 69
```javascript
function foo(a, b = a) {
  console.log(b);
}
foo(10);
// Output: 10
```
**Explanation:** Default parameters can reference earlier parameters. Since `a` is 10, `b` defaults to 10.

### Question 70
```javascript
function foo(a = b, b = 1) {
  console.log(a, b);
}
foo(undefined, 2);
// Output: ReferenceError: Cannot access 'b' before initialization
```
**Explanation:** Default parameter `a = b` tries to access `b` before it's initialized in the parameter list, causing a temporal dead zone error.

### Question 71
```javascript
const add = (a, b) => (a, b);
console.log(add(1, 2));
// Output: 2
```
**Explanation:** Parentheses without curly braces denote an expression. The comma operator evaluates both expressions but returns only the last one (b).

### Question 72
```javascript
function outer() {
  return function inner() {
    console.log("inner");
  };
}
outer();
// Output: (no output)
```
**Explanation:** `outer()` returns a function but doesn't execute it. To see output, you need `outer()()`.

### Question 73
```javascript
(function() {
  var a = b = 5;
})();
console.log(typeof a);
console.log(typeof b);
// Output: "undefined"
// Output: "number"
```
**Explanation:** `b = 5` creates a global variable (no `var`), then `a` is declared locally. After IIFE, `a` is out of scope but `b` remains global.

### Question 74
```javascript
function test(a, a) {
  console.log(a);
}
test(1, 2);
// Output: 2 (in non-strict mode)
```
**Explanation:** In non-strict mode, duplicate parameters are allowed. The last value wins. In strict mode, this would throw a SyntaxError.

### Question 75
```javascript
const fn = new Function("a", "b", "return a + b");
console.log(fn(1, 2));
// Output: 3
```
**Explanation:** `Function` constructor creates a function from strings. Last argument is the function body, previous ones are parameters.

---

## Asynchronous JavaScript

### Question 76
```javascript
console.log("A");
setTimeout(() => console.log("B"), 0);
console.log("C");
// Output: A C B
```
**Explanation:** `setTimeout` queues the callback in the task queue, even with 0ms delay. Synchronous code executes first, then queued tasks.

### Question 77
```javascript
console.log("A");
Promise.resolve().then(() => console.log("B"));
console.log("C");
// Output: A C B
```
**Explanation:** Promise callbacks are microtasks, executed after current script but before task queue. So synchronous code runs first, then promise callback.

### Question 78
```javascript
console.log("A");
setTimeout(() => console.log("B"), 0);
Promise.resolve().then(() => console.log("C"));
console.log("D");
// Output: A D C B
```
**Explanation:** Synchronous code runs first (A, D). Microtasks (promises) execute before macrotasks (setTimeout), so C runs before B.

### Question 79
```javascript
async function test() {
  console.log("A");
  await Promise.resolve();
  console.log("B");
}
test();
console.log("C");
// Output: A C B
```
**Explanation:** Code before `await` runs synchronously. `await` pauses the async function, allowing synchronous code to complete. Then async function resumes.

### Question 80
```javascript
const promise = new Promise((resolve, reject) => {
  console.log("A");
  resolve();
  console.log("B");
});
promise.then(() => console.log("C"));
console.log("D");
// Output: A B D C
```
**Explanation:** Promise executor runs synchronously (A, B). Synchronous code completes (D). Then promise `.then` callback runs as microtask (C).

### Question 81
```javascript
setTimeout(() => console.log("A"), 0);
Promise.resolve().then(() => console.log("B"));
Promise.resolve().then(() => console.log("C"));
setTimeout(() => console.log("D"), 0);
// Output: B C A D
```
**Explanation:** All microtasks (B, C) execute before any macrotasks (A, D). Within each category, order is preserved.

### Question 82
```javascript
async function foo() {
  return 1;
}
console.log(foo());
// Output: Promise { 1 }
```
**Explanation:** Async functions always return a promise. Return value is automatically wrapped in `Promise.resolve()`.

### Question 83
```javascript
Promise.resolve(1)
  .then(x => x + 1)
  .then(x => { throw new Error("error"); })
  .catch(() => 1)
  .then(x => console.log(x))
  .catch(console.log);
// Output: 1
```
**Explanation:** First `.then` returns 2. Second throws error, caught by `.catch` which returns 1. Final `.then` logs that 1.

### Question 84
```javascript
async function test() {
  console.log("A");
  await console.log("B");
  console.log("C");
}
test();
console.log("D");
// Output: A B D C
```
**Explanation:** `console.log("B")` executes synchronously (returning undefined). `await` pauses function. "D" runs, then function resumes with "C".

### Question 85
```javascript
Promise.resolve()
  .then(() => {
    return new Error("error");
  })
  .then(console.log)
  .catch(console.log);
// Output: Error: error
```
**Explanation:** Returning an error is not the same as throwing it. The error object is passed to the next `.then`, not `.catch`.

---

## Operators & Expressions

### Question 86
```javascript
console.log(1 + "2" + 3);
console.log(1 + 2 + "3");
// Output: "123"
// Output: "33"
```
**Explanation:** First: `1 + "2"` is `"12"` (string), then `"12" + 3` is `"123"`. Second: `1 + 2` is `3` (number), then `3 + "3"` is `"33"`.

### Question 87
```javascript
console.log(typeof typeof 1);
// Output: "string"
```
**Explanation:** `typeof 1` returns `"number"` (a string). Then `typeof "number"` returns `"string"`.

### Question 88
```javascript
console.log(3 > 2 > 1);
// Output: false
```
**Explanation:** `3 > 2` is `true`. Then `true > 1` converts `true` to 1, so `1 > 1` is false.

### Question 89
```javascript
console.log([] == ![]);
// Output: true
```
**Explanation:** `![]` is `false` (empty array is truthy). Then `[] == false` converts both to numbers: `0 == 0` is true.

### Question 90
```javascript
console.log(null >= 0);
console.log(null == 0);
console.log(null > 0);
// Output: true
// Output: false
// Output: false
```
**Explanation:** Comparison operators convert `null` to 0, so `0 >= 0` is true and `0 > 0` is false. Equality operator has special rule: `null` equals only `undefined`.

### Question 91
```javascript
console.log(10 / 0);
console.log(-10 / 0);
console.log(0 / 0);
// Output: Infinity
// Output: -Infinity
// Output: NaN
```
**Explanation:** Division by zero produces Infinity (with appropriate sign). `0 / 0` is indeterminate, resulting in NaN.

### Question 92
```javascript
console.log(+"");
console.log(+"0");
console.log(+"1");
// Output: 0
// Output: 0
// Output: 1
```
**Explanation:** Unary `+` converts operand to number. Empty string becomes 0, numeric strings become their numeric values.

### Question 93
```javascript
console.log(!!"");
console.log(!!"false");
console.log(!!null);
// Output: false
// Output: true
// Output: false
```
**Explanation:** Double negation converts to boolean. Empty string and null are falsy. Non-empty string "false" is truthy.

### Question 94
```javascript
console.log(0.1 + 0.2);
console.log(0.1 + 0.2 === 0.3);
// Output: 0.30000000000000004
// Output: false
```
**Explanation:** Floating-point arithmetic has precision limitations due to binary representation. Result is close to but not exactly 0.3.

### Question 95
```javascript
console.log(1 && 2 && 3);
console.log(1 || 2 || 3);
// Output: 3
// Output: 1
```
**Explanation:** `&&` returns the first falsy value or the last value. `||` returns the first truthy value or the last value.

---

## Miscellaneous

### Question 96
```javascript
const obj = {
  a: "foo",
  b: function() {},
  c: () => {},
  d: undefined,
  e: null
};
console.log(JSON.stringify(obj));
// Output: {"a":"foo","e":null}
```
**Explanation:** `JSON.stringify` omits functions and undefined values. Only serializable values (strings, numbers, booleans, null, objects, arrays) are included.

### Question 97
```javascript
console.log(1 == [1]);
console.log(1 == [[1]]);
// Output: true
// Output: true
```
**Explanation:** Arrays are converted to primitives for comparison. `[1]` becomes `"1"`, then 1. `[[1]]` also converts to 1 through string conversion.

### Question 98
```javascript
const a = {};
const b = { key: "b" };
const c = { key: "c" };
a[b] = 123;
a[c] = 456;
console.log(a[b]);
// Output: 456
```
**Explanation:** Object keys are strings. Objects used as keys are converted to `"[object Object]"`. Both `b` and `c` convert to same string, so `c` overwrites `b`.

### Question 99
```javascript
console.log(String("Hello") === "Hello");
console.log(new String("Hello") === "Hello");
// Output: true
// Output: false
```
**Explanation:** `String()` without `new` converts to primitive string. `new String()` creates a String object. Object is never strictly equal to primitive.

### Question 100
```javascript
const obj = { a: 1, b: 2, c: 3 };
for (const key in obj) {
  console.log(obj[key]);
}
// Output: 1
// Output: 2
// Output: 3
```
**Explanation:** `for...in` iterates over enumerable properties of an object. Each iteration assigns the property name to the loop variable.

---

## Summary

This collection covers essential JavaScript concepts that often trip up developers:

- **Type Coercion**: Understanding implicit conversions between types
- **Hoisting**: How declarations are moved to the top of their scope
- **Scope & Closures**: Variable visibility and function memory
- **this Binding**: Context determination in different scenarios
- **Objects & Prototypes**: Reference behavior and inheritance
- **Arrays**: Quirks with methods, length, and holes
- **Functions**: Parameters, returns, and various declaration styles
- **Async Patterns**: Event loop, promises, and execution order
- **Operators**: Unexpected behavior with type conversion
- **Miscellaneous**: Edge cases and common pitfalls

Mastering these tricky scenarios will significantly improve your JavaScript debugging skills and help you write more robust code!
