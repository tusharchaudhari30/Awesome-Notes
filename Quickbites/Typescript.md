# TypeScript Complete Interview Notes

## From Basics to Expert Level

---

## Table of Contents

1. [Introduction to TypeScript](#introduction)
2. [Basic Types](#basic-types)
3. [Variables and Type Annotations](#variables)
4. [Functions](#functions)
5. [Interfaces](#interfaces)
6. [Type Aliases](#type-aliases)
7. [Classes and OOP](#classes)
8. [Generics](#generics)
9. [Advanced Types](#advanced-types)
10. [Utility Types](#utility-types)
11. [Decorators](#decorators)
12. [Modules and Namespaces](#modules)
13. [Async Programming](#async)
14. [Error Handling](#error-handling)
15. [Best Practices](#best-practices)

---

## 1. Introduction to TypeScript {#introduction}

TypeScript is a statically typed superset of JavaScript developed by Microsoft. It adds optional static typing, classes, and interfaces to JavaScript, enabling developers to catch errors during development rather than at runtime.

**Key Benefits:**

- Static type checking
- Enhanced IDE support
- Better code maintainability
- Modern ECMAScript features
- Compiles to JavaScript

**Installation:**

```bash
npm install -g typescript
```

**Compilation:**

```bash
tsc filename.ts
```

---

## 2. Basic Types {#basic-types}

### Primitive Types

**Number:**

```typescript
let age: number = 25;
let price: number = 99.99;
let hex: number = 0xf00d;
```

**String:**

```typescript
let firstName: string = "John";
let lastName: string = "Doe";
let fullName: string = `${firstName} ${lastName}`;
```

**Boolean:**

```typescript
let isActive: boolean = true;
let hasPermission: boolean = false;
```

**Null and Undefined:**

```typescript
let n: null = null;
let u: undefined = undefined;
```

### Special Types

**Any:**

```typescript
let data: any = "Hello";
data = 42; // No error
data = true; // No error
// Avoid using 'any' - defeats the purpose of TypeScript
```

**Unknown:**

```typescript
let value: unknown = "Hello";
// value.toUpperCase(); // Error: Object is of type 'unknown'

// Type narrowing required
if (typeof value === "string") {
  console.log(value.toUpperCase()); // OK
}
```

**Never:**

```typescript
// Function that never returns
function throwError(message: string): never {
  throw new Error(message);
}

function infiniteLoop(): never {
  while (true) {}
}
```

**Void:**

```typescript
function logMessage(message: string): void {
  console.log(message);
  // No return value
}
```

### Arrays

```typescript
// Array of numbers
let numbers: number[] = [1, 2, 3, 4, 5];
let scores: Array<number> = [90, 85, 88];

// Array of strings
let names: string[] = ["Alice", "Bob", "Charlie"];

// Mixed array (not recommended)
let mixed: any[] = [1, "two", true];
```

### Tuples

```typescript
// Fixed-length array with specific types
let person: [string, number] = ["John", 30];

// Accessing tuple elements
console.log(person[0]); // "John"
console.log(person[1]); // 30

// Tuple with optional elements
let optionalTuple: [string, number?] = ["Alice"];

// Tuple with rest elements
let restTuple: [string, ...number[]] = ["Scores", 90, 85, 88];
```

### Enums

```typescript
// Numeric enum
enum Direction {
  Up = 1,
  Down,
  Left,
  Right,
}

let dir: Direction = Direction.Up;
console.log(dir); // 1

// String enum
enum Status {
  Active = "ACTIVE",
  Inactive = "INACTIVE",
  Pending = "PENDING",
}

let currentStatus: Status = Status.Active;
console.log(currentStatus); // "ACTIVE"

// Const enum (for better performance)
const enum Color {
  Red,
  Green,
  Blue,
}

let c: Color = Color.Red;
```

---

## 3. Variables and Type Annotations {#variables}

### Type Annotations

```typescript
// Explicit type annotation
let userName: string = "Alice";
let userAge: number = 25;

// Type inference (TypeScript infers the type)
let inferredName = "Bob"; // inferred as string
let inferredAge = 30; // inferred as number
```

### Variable Declarations

```typescript
// let - block-scoped
let x = 10;

// const - block-scoped and immutable reference
const PI = 3.14159;

// var - function-scoped (avoid using)
var oldStyle = "not recommended";
```

### Union Types

```typescript
let id: number | string;
id = 101; // OK
id = "ABC101"; // OK
// id = true;    // Error

function printId(id: number | string) {
  if (typeof id === "string") {
    console.log(id.toUpperCase());
  } else {
    console.log(id);
  }
}
```

### Intersection Types

```typescript
interface Person {
  name: string;
  age: number;
}

interface Employee {
  employeeId: number;
  department: string;
}

type Staff = Person & Employee;

let employee: Staff = {
  name: "John",
  age: 30,
  employeeId: 1001,
  department: "IT",
};
```

### Literal Types

```typescript
// String literal types
let direction: "left" | "right" | "up" | "down";
direction = "left"; // OK
// direction = "forward"; // Error

// Numeric literal types
let diceRoll: 1 | 2 | 3 | 4 | 5 | 6;
diceRoll = 3; // OK

// Boolean literal types
let isTrue: true = true;
```

---

## 4. Functions {#functions}

### Function Types

```typescript
// Named function
function add(a: number, b: number): number {
  return a + b;
}

// Anonymous function
let multiply = function (a: number, b: number): number {
  return a * b;
};

// Arrow function
let divide = (a: number, b: number): number => a / b;
```

### Optional and Default Parameters

```typescript
// Optional parameter
function greet(name: string, greeting?: string): string {
  if (greeting) {
    return `${greeting}, ${name}!`;
  }
  return `Hello, ${name}!`;
}

console.log(greet("Alice")); // "Hello, Alice!"
console.log(greet("Bob", "Good morning")); // "Good morning, Bob!"

// Default parameter
function createUser(name: string, role: string = "user"): void {
  console.log(`${name} - ${role}`);
}

createUser("Alice"); // "Alice - user"
createUser("Bob", "admin"); // "Bob - admin"
```

### Rest Parameters

```typescript
function sum(...numbers: number[]): number {
  return numbers.reduce((total, num) => total + num, 0);
}

console.log(sum(1, 2, 3)); // 6
console.log(sum(10, 20, 30, 40)); // 100
```

### Function Overloading

```typescript
// Overload signatures
function format(value: string): string;
function format(value: number): string;
function format(value: boolean): string;

// Implementation signature
function format(value: string | number | boolean): string {
  if (typeof value === "string") {
    return value.toUpperCase();
  } else if (typeof value === "number") {
    return value.toFixed(2);
  } else {
    return value.toString();
  }
}

console.log(format("hello")); // "HELLO"
console.log(format(123.456)); // "123.46"
console.log(format(true)); // "true"
```

### Call Signatures

```typescript
type MathOperation = {
  (a: number, b: number): number;
  description: string;
};

const addition: MathOperation = (a, b) => a + b;
addition.description = "Adds two numbers";

console.log(addition(5, 3)); // 8
console.log(addition.description); // "Adds two numbers"
```

---

## 5. Interfaces {#interfaces}

### Basic Interface

```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

let user: User = {
  id: 1,
  name: "Alice",
  email: "alice@example.com",
};
```

### Optional Properties

```typescript
interface Product {
  id: number;
  name: string;
  description?: string; // Optional
  price: number;
}

let product1: Product = {
  id: 1,
  name: "Laptop",
  price: 999.99,
};

let product2: Product = {
  id: 2,
  name: "Mouse",
  description: "Wireless mouse",
  price: 25.99,
};
```

### Readonly Properties

```typescript
interface Point {
  readonly x: number;
  readonly y: number;
}

let point: Point = { x: 10, y: 20 };
// point.x = 15; // Error: Cannot assign to 'x' because it is a read-only property
```

### Function Types in Interfaces

```typescript
interface SearchFunc {
  (source: string, subString: string): boolean;
}

let mySearch: SearchFunc = function (src: string, sub: string): boolean {
  return src.indexOf(sub) > -1;
};

console.log(mySearch("Hello World", "World")); // true
```

### Extending Interfaces

```typescript
interface Animal {
  name: string;
  age: number;
}

interface Dog extends Animal {
  breed: string;
  bark(): void;
}

let myDog: Dog = {
  name: "Buddy",
  age: 3,
  breed: "Golden Retriever",
  bark() {
    console.log("Woof!");
  },
};
```

### Multiple Interface Inheritance

```typescript
interface Colorful {
  color: string;
}

interface Shape {
  area(): number;
}

interface ColoredShape extends Colorful, Shape {
  name: string;
}

let circle: ColoredShape = {
  color: "red",
  name: "Circle",
  area() {
    return Math.PI * 10 * 10;
  },
};
```

---

## 6. Type Aliases {#type-aliases}

### Basic Type Alias

```typescript
type ID = number | string;

let userId: ID = 101;
let productId: ID = "P-1001";
```

### Object Type Alias

```typescript
type User = {
  id: number;
  name: string;
  email: string;
};

let user: User = {
  id: 1,
  name: "Alice",
  email: "alice@example.com",
};
```

### Union Type Alias

```typescript
type Status = "success" | "error" | "pending";

function handleStatus(status: Status): void {
  switch (status) {
    case "success":
      console.log("Operation successful!");
      break;
    case "error":
      console.log("An error occurred!");
      break;
    case "pending":
      console.log("Operation pending...");
      break;
  }
}
```

### Type Alias vs Interface

```typescript
// Both can be used similarly
type PersonType = {
  name: string;
  age: number;
};

interface PersonInterface {
  name: string;
  age: number;
}

// Key Differences:
// 1. Interfaces can be extended and merged
interface Window {
  title: string;
}

interface Window {
  ts: string;
}

// 2. Types can use union/intersection
type StringOrNumber = string | number;

// 3. Types can use mapped types
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};
```

---

## 7. Classes and OOP {#classes}

### Basic Class

```typescript
class Person {
  name: string;
  age: number;

  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }

  introduce(): void {
    console.log(`Hi, I'm ${this.name} and I'm ${this.age} years old.`);
  }
}

let person = new Person("Alice", 25);
person.introduce(); // "Hi, I'm Alice and I'm 25 years old."
```

### Access Modifiers

```typescript
class BankAccount {
  public accountNumber: string;
  private balance: number;
  protected owner: string;

  constructor(accountNumber: string, owner: string, initialBalance: number) {
    this.accountNumber = accountNumber;
    this.owner = owner;
    this.balance = initialBalance;
  }

  public deposit(amount: number): void {
    this.balance += amount;
  }

  public getBalance(): number {
    return this.balance;
  }

  private calculateInterest(): number {
    return this.balance * 0.05;
  }
}

let account = new BankAccount("123456", "John", 1000);
account.deposit(500);
console.log(account.getBalance()); // 1500
// console.log(account.balance); // Error: Property 'balance' is private
```

### Inheritance

```typescript
class Animal {
  protected name: string;

  constructor(name: string) {
    this.name = name;
  }

  move(distance: number = 0): void {
    console.log(`${this.name} moved ${distance} meters.`);
  }
}

class Dog extends Animal {
  constructor(name: string) {
    super(name); // Call parent constructor
  }

  bark(): void {
    console.log("Woof! Woof!");
  }

  // Override parent method
  move(distance: number = 5): void {
    console.log("Running...");
    super.move(distance);
  }
}

let dog = new Dog("Buddy");
dog.bark(); // "Woof! Woof!"
dog.move(10); // "Running..." "Buddy moved 10 meters."
```

### Abstract Classes

```typescript
abstract class Shape {
  abstract getArea(): number;
  abstract getPerimeter(): number;

  displayInfo(): void {
    console.log(`Area: ${this.getArea()}`);
    console.log(`Perimeter: ${this.getPerimeter()}`);
  }
}

class Circle extends Shape {
  constructor(private radius: number) {
    super();
  }

  getArea(): number {
    return Math.PI * this.radius * this.radius;
  }

  getPerimeter(): number {
    return 2 * Math.PI * this.radius;
  }
}

let circle = new Circle(5);
circle.displayInfo();
```

### Static Members

```typescript
class MathOperations {
  static PI: number = 3.14159;

  static calculateCircleArea(radius: number): number {
    return this.PI * radius * radius;
  }
}

console.log(MathOperations.PI); // 3.14159
console.log(MathOperations.calculateCircleArea(5)); // 78.53975
```

### Getters and Setters

```typescript
class Employee {
  private _salary: number = 0;

  get salary(): number {
    return this._salary;
  }

  set salary(value: number) {
    if (value < 0) {
      throw new Error("Salary cannot be negative");
    }
    this._salary = value;
  }
}

let emp = new Employee();
emp.salary = 50000;
console.log(emp.salary); // 50000
```

---

## 8. Generics {#generics}

### Basic Generics

```typescript
// Generic function
function identity<T>(arg: T): T {
  return arg;
}

let output1 = identity<string>("Hello");
let output2 = identity<number>(42);
let output3 = identity(true); // Type inference
```

### Generic Interfaces

```typescript
interface Box<T> {
  value: T;
}

let stringBox: Box<string> = { value: "Hello" };
let numberBox: Box<number> = { value: 42 };
```

### Generic Classes

```typescript
class DataManager<T> {
  private data: T[] = [];

  add(item: T): void {
    this.data.push(item);
  }

  getAll(): T[] {
    return this.data;
  }

  getById(index: number): T | undefined {
    return this.data[index];
  }
}

let stringManager = new DataManager<string>();
stringManager.add("Alice");
stringManager.add("Bob");
console.log(stringManager.getAll()); // ["Alice", "Bob"]

let numberManager = new DataManager<number>();
numberManager.add(10);
numberManager.add(20);
console.log(numberManager.getAll()); // [10, 20]
```

### Generic Constraints

```typescript
// Constraint using interface
interface HasLength {
  length: number;
}

function logLength<T extends HasLength>(arg: T): void {
  console.log(arg.length);
}

logLength("Hello"); // 5
logLength([1, 2, 3]); // 3
// logLength(123);       // Error: number doesn't have 'length'

// Constraint using keyof
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

let person = { name: "Alice", age: 25, city: "NYC" };
let name = getProperty(person, "name"); // OK
// let invalid = getProperty(person, "salary"); // Error
```

### Multiple Type Parameters

```typescript
function merge<T, U>(obj1: T, obj2: U): T & U {
  return { ...obj1, ...obj2 };
}

let merged = merge({ name: "Alice" }, { age: 25 });
console.log(merged); // { name: "Alice", age: 25 }
```

---

## 9. Advanced Types {#advanced-types}

### Conditional Types

```typescript
type IsString<T> = T extends string ? "yes" : "no";

type Test1 = IsString<string>; // "yes"
type Test2 = IsString<number>; // "no"

// Practical example
type NonNullable<T> = T extends null | undefined ? never : T;

type A = NonNullable<string | null>; // string
type B = NonNullable<number | undefined>; // number
```

### Mapped Types

```typescript
// Make all properties optional
type Partial<T> = {
  [P in keyof T]?: T[P];
};

// Make all properties required
type Required<T> = {
  [P in keyof T]-?: T[P];
};

// Make all properties readonly
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};

// Example usage
interface User {
  id: number;
  name: string;
  email: string;
}

type PartialUser = Partial<User>;
// { id?: number; name?: string; email?: string; }

type ReadonlyUser = Readonly<User>;
// { readonly id: number; readonly name: string; readonly email: string; }
```

### Template Literal Types

```typescript
type World = "world";
type Greeting = `hello ${World}`; // "hello world"

type EmailLocale = "welcome_email" | "password_reset";
type EmailType = `${EmailLocale}_subject` | `${EmailLocale}_body`;
// "welcome_email_subject" | "welcome_email_body" |
// "password_reset_subject" | "password_reset_body"
```

### Infer Keyword

```typescript
// Extract return type of a function
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

function getUser() {
  return { name: "Alice", age: 25 };
}

type User = ReturnType<typeof getUser>;
// { name: string; age: number; }

// Extract parameter types
type Parameters<T> = T extends (...args: infer P) => any ? P : never;

function greet(name: string, age: number) {
  console.log(`Hello ${name}, you are ${age} years old`);
}

type GreetParams = Parameters<typeof greet>;
// [string, number]
```

### Type Guards

```typescript
// typeof type guard
function printValue(value: string | number) {
  if (typeof value === "string") {
    console.log(value.toUpperCase());
  } else {
    console.log(value.toFixed(2));
  }
}

// instanceof type guard
class Dog {
  bark() {
    console.log("Woof!");
  }
}

class Cat {
  meow() {
    console.log("Meow!");
  }
}

function makeSound(animal: Dog | Cat) {
  if (animal instanceof Dog) {
    animal.bark();
  } else {
    animal.meow();
  }
}

// User-defined type guard
interface Fish {
  swim(): void;
}

interface Bird {
  fly(): void;
}

function isFish(pet: Fish | Bird): pet is Fish {
  return (pet as Fish).swim !== undefined;
}

function move(pet: Fish | Bird) {
  if (isFish(pet)) {
    pet.swim();
  } else {
    pet.fly();
  }
}
```

### Discriminated Unions

```typescript
interface Square {
  kind: "square";
  size: number;
}

interface Rectangle {
  kind: "rectangle";
  width: number;
  height: number;
}

interface Circle {
  kind: "circle";
  radius: number;
}

type Shape = Square | Rectangle | Circle;

function getArea(shape: Shape): number {
  switch (shape.kind) {
    case "square":
      return shape.size * shape.size;
    case "rectangle":
      return shape.width * shape.height;
    case "circle":
      return Math.PI * shape.radius * shape.radius;
  }
}
```

---

## 10. Utility Types {#utility-types}

### Partial&lt;T&gt;

```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

// Makes all properties optional
function updateUser(user: User, updates: Partial<User>): User {
  return { ...user, ...updates };
}

let user = { id: 1, name: "Alice", email: "alice@example.com" };
let updated = updateUser(user, { name: "Bob" });
```

### Required&lt;T&gt;

```typescript
interface Props {
  name?: string;
  age?: number;
}

type RequiredProps = Required<Props>;
// { name: string; age: number; }
```

### Readonly&lt;T&gt;

```typescript
interface Todo {
  title: string;
  completed: boolean;
}

const todo: Readonly<Todo> = {
  title: "Learn TypeScript",
  completed: false,
};

// todo.completed = true; // Error: Cannot assign to 'completed'
```

### Pick&lt;T, K&gt;

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  age: number;
}

type UserPreview = Pick<User, "id" | "name">;
// { id: number; name: string; }

let preview: UserPreview = {
  id: 1,
  name: "Alice",
};
```

### Omit&lt;T, K&gt;

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  password: string;
}

type UserWithoutPassword = Omit<User, "password">;
// { id: number; name: string; email: string; }
```

### Record&lt;K, T&gt;

```typescript
type Status = "pending" | "approved" | "rejected";

const statusMessages: Record<Status, string> = {
  pending: "Your request is being processed",
  approved: "Your request has been approved",
  rejected: "Your request has been rejected",
};

console.log(statusMessages.pending);
```

### Exclude&lt;T, U&gt;

```typescript
type T = "a" | "b" | "c";
type U = "a" | "c";

type Result = Exclude<T, U>; // "b"
```

### Extract&lt;T, U&gt;

```typescript
type T = "a" | "b" | "c";
type U = "a" | "c" | "d";

type Result = Extract<T, U>; // "a" | "c"
```

### NonNullable&lt;T&gt;

```typescript
type T = string | number | null | undefined;

type NonNull = NonNullable<T>; // string | number
```

### ReturnType&lt;T&gt;

```typescript
function getUser() {
  return { id: 1, name: "Alice" };
}

type User = ReturnType<typeof getUser>;
// { id: number; name: string; }
```

---

## 11. Decorators {#decorators}

**Note:** Enable decorators in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "experimentalDecorators": true
  }
}
```

### Class Decorator

```typescript
function sealed(constructor: Function) {
  Object.seal(constructor);
  Object.seal(constructor.prototype);
}

@sealed
class Greeter {
  greeting: string;

  constructor(message: string) {
    this.greeting = message;
  }

  greet() {
    return `Hello, ${this.greeting}`;
  }
}
```

### Method Decorator

```typescript
function log(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    console.log(`Calling ${propertyKey} with args:`, args);
    const result = originalMethod.apply(this, args);
    console.log(`Result:`, result);
    return result;
  };

  return descriptor;
}

class Calculator {
  @log
  add(a: number, b: number): number {
    return a + b;
  }
}

let calc = new Calculator();
calc.add(5, 3);
// Calling add with args: [5, 3]
// Result: 8
```

### Property Decorator

```typescript
function readonly(target: any, propertyKey: string) {
  Object.defineProperty(target, propertyKey, {
    writable: false,
  });
}

class Person {
  @readonly
  name: string = "Alice";
}

let person = new Person();
// person.name = "Bob"; // Error at runtime
```

### Parameter Decorator

```typescript
function required(target: Object, propertyKey: string, parameterIndex: number) {
  console.log(`Parameter ${parameterIndex} of ${propertyKey} is required`);
}

class UserService {
  createUser(@required name: string, age: number) {
    console.log(`Creating user: ${name}, ${age}`);
  }
}
```

---

## 12. Modules and Namespaces {#modules}

### ES6 Modules

**math.ts:**

```typescript
export function add(a: number, b: number): number {
  return a + b;
}

export function subtract(a: number, b: number): number {
  return a - b;
}

export const PI = 3.14159;

export default class Calculator {
  multiply(a: number, b: number): number {
    return a * b;
  }
}
```

**app.ts:**

```typescript
import Calculator, { add, subtract, PI } from "./math";

console.log(add(5, 3)); // 8
console.log(subtract(10, 4)); // 6
console.log(PI); // 3.14159

let calc = new Calculator();
console.log(calc.multiply(2, 3)); // 6
```

### Namespaces

```typescript
namespace Geometry {
  export interface Point {
    x: number;
    y: number;
  }

  export class Circle {
    constructor(public center: Point, public radius: number) {}

    getArea(): number {
      return Math.PI * this.radius * this.radius;
    }
  }

  export namespace Utils {
    export function distance(p1: Point, p2: Point): number {
      const dx = p2.x - p1.x;
      const dy = p2.y - p1.y;
      return Math.sqrt(dx * dx + dy * dy);
    }
  }
}

let circle = new Geometry.Circle({ x: 0, y: 0 }, 5);
console.log(circle.getArea());

let dist = Geometry.Utils.distance({ x: 0, y: 0 }, { x: 3, y: 4 });
console.log(dist); // 5
```

### Module vs Namespace

**Use Modules when:**

- Working with modern JavaScript/TypeScript
- Need external dependencies
- Building applications with bundlers

**Use Namespaces when:**

- Organizing internal code
- Working without a module loader
- Maintaining legacy code

---

## 13. Async Programming {#async}

### Promises

```typescript
function fetchData(url: string): Promise<string> {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (url) {
        resolve(`Data from ${url}`);
      } else {
        reject(new Error("Invalid URL"));
      }
    }, 1000);
  });
}

fetchData("https://api.example.com")
  .then((data) => console.log(data))
  .catch((error) => console.error(error));
```

### Async/Await

```typescript
async function getUserData(userId: number): Promise<User> {
  try {
    const response = await fetch(`/api/users/${userId}`);

    if (!response.ok) {
      throw new Error("Failed to fetch user");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

// Usage
async function main() {
  try {
    const user = await getUserData(1);
    console.log(user);
  } catch (error) {
    console.error("Failed to get user");
  }
}

main();
```

### Promise.all with TypeScript

```typescript
async function fetchMultipleUsers(ids: number[]): Promise<User[]> {
  const promises = ids.map((id) => getUserData(id));
  return await Promise.all(promises);
}

// Usage
const users = await fetchMultipleUsers([1, 2, 3]);
```

### Typing Promises

```typescript
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

async function fetchApi<T>(url: string): Promise<ApiResponse<T>> {
  const response = await fetch(url);
  const data = await response.json();

  return {
    data: data,
    status: response.status,
    message: response.statusText,
  };
}

// Usage
interface User {
  id: number;
  name: string;
}

const result = await fetchApi<User>("/api/user/1");
console.log(result.data.name);
```

---

## 14. Error Handling {#error-handling}

### Try-Catch-Finally

```typescript
function divide(a: number, b: number): number {
  try {
    if (b === 0) {
      throw new Error("Division by zero");
    }
    return a / b;
  } catch (error) {
    if (error instanceof Error) {
      console.error("Error:", error.message);
    }
    throw error;
  } finally {
    console.log("Operation completed");
  }
}

try {
  const result = divide(10, 0);
} catch (error) {
  console.log("Caught error");
}
```

### Custom Error Classes

```typescript
class ValidationError extends Error {
  constructor(public field: string, message: string) {
    super(message);
    this.name = "ValidationError";
    Object.setPrototypeOf(this, ValidationError.prototype);
  }
}

class User {
  constructor(public email: string) {
    if (!email.includes("@")) {
      throw new ValidationError("email", "Invalid email format");
    }
  }
}

try {
  const user = new User("invalid-email");
} catch (error) {
  if (error instanceof ValidationError) {
    console.log(`${error.field}: ${error.message}`);
  }
}
```

### Error Handling in Async Functions

```typescript
async function fetchUserWithErrorHandling(
  userId: number
): Promise<User | null> {
  try {
    const response = await fetch(`/api/users/${userId}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    if (error instanceof Error) {
      console.error("Failed to fetch user:", error.message);
    }
    return null;
  }
}
```

### Type-safe Error Handling

```typescript
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

function divide(a: number, b: number): Result<number> {
  if (b === 0) {
    return {
      success: false,
      error: new Error("Division by zero"),
    };
  }
  return {
    success: true,
    data: a / b,
  };
}

const result = divide(10, 2);
if (result.success) {
  console.log(result.data); // 5
} else {
  console.error(result.error.message);
}
```

---

## 15. Best Practices {#best-practices}

### 1. Enable Strict Mode

**tsconfig.json:**

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictPropertyInitialization": true
  }
}
```

### 2. Use Type Inference

```typescript
// Bad
let name: string = "Alice";

// Good
let name = "Alice"; // Type inferred as string
```

### 3. Avoid 'any' Type

```typescript
// Bad
function processData(data: any) {
  return data.value;
}

// Good
interface Data {
  value: string;
}

function processData(data: Data) {
  return data.value;
}

// Or use unknown for truly unknown types
function processUnknown(data: unknown) {
  if (typeof data === "object" && data !== null && "value" in data) {
    return (data as Data).value;
  }
}
```

### 4. Use Const Assertions

```typescript
// Without const assertion
const colors = ["red", "green", "blue"];
// Type: string[]

// With const assertion
const colors = ["red", "green", "blue"] as const;
// Type: readonly ["red", "green", "blue"]
```

### 5. Prefer Interfaces for Objects

```typescript
// Good for objects
interface User {
  id: number;
  name: string;
}

// Good for unions, primitives
type ID = number | string;
type Status = "active" | "inactive";
```

### 6. Use Discriminated Unions

```typescript
interface SuccessResponse {
  status: "success";
  data: any;
}

interface ErrorResponse {
  status: "error";
  message: string;
}

type ApiResponse = SuccessResponse | ErrorResponse;

function handleResponse(response: ApiResponse) {
  if (response.status === "success") {
    console.log(response.data);
  } else {
    console.error(response.message);
  }
}
```

### 7. Use Optional Chaining

```typescript
interface User {
  name: string;
  address?: {
    street?: string;
    city?: string;
  };
}

let user: User = { name: "Alice" };

// Without optional chaining
const city = user.address && user.address.city;

// With optional chaining
const cityOptional = user.address?.city;
```

### 8. Use Nullish Coalescing

```typescript
let value: string | null = null;

// Old way
const result1 = value !== null && value !== undefined ? value : "default";

// New way
const result2 = value ?? "default";
```

### 9. Organize Imports

```typescript
// Group imports: external, internal, relative
import React from "react";
import { Observable } from "rxjs";

import { UserService } from "@/services/UserService";
import { formatDate } from "@/utils/dateUtils";

import { Header } from "./Header";
import { Footer } from "./Footer";
```

### 10. Document Complex Types

```typescript
/**
 * Represents a user in the system
 * @property id - Unique identifier
 * @property name - User's full name
 * @property email - User's email address
 */
interface User {
  id: number;
  name: string;
  email: string;
}

/**
 * Fetches user data from the API
 * @param userId - The ID of the user to fetch
 * @returns Promise resolving to User object
 * @throws {Error} If user not found or network error
 */
async function fetchUser(userId: number): Promise<User> {
  // implementation
}
```

---

## Common Interview Questions

### 1. What is TypeScript and why use it?

TypeScript is a statically typed superset of JavaScript that compiles to plain JavaScript. Benefits include:

- Early error detection through static typing
- Better IDE support and autocompletion
- Enhanced code maintainability
- Support for modern JavaScript features
- Better documentation through types

### 2. Difference between Interface and Type?

**Interfaces:**

- Can be extended and merged
- Better for object shapes
- Better error messages
- Can be implemented by classes

**Types:**

- More flexible (unions, intersections, primitives)
- Cannot be reopened for declaration merging
- Can use mapped and conditional types

### 3. What are Generics?

Generics allow creating reusable components that work with multiple types while maintaining type safety.

```typescript
function identity<T>(arg: T): T {
  return arg;
}
```

### 4. Explain 'never' type

The `never` type represents values that never occur. Used for:

- Functions that never return
- Exhaustive type checking

```typescript
function throwError(message: string): never {
  throw new Error(message);
}
```

### 5. What is Type Assertion?

Type assertion tells TypeScript to treat a value as a specific type when you know more than the compiler.

```typescript
let value: any = "Hello";
let length: number = (value as string).length;
```

---

## Advanced Interview Topics

1. **Mapped Types** - Transform properties of existing types
2. **Conditional Types** - Types that depend on conditions
3. **Template Literal Types** - String manipulation at type level
4. **Decorators** - Meta-programming for classes and members
5. **Module Resolution** - How TypeScript finds modules
6. **Declaration Files (.d.ts)** - Type definitions for JavaScript libraries
7. **Type Guards** - Runtime checks that narrow types
8. **Discriminated Unions** - Pattern matching with type narrowing

---

## Tips for Interviews

1. **Understand the basics thoroughly** - primitives, interfaces, types
2. **Practice generics** - commonly asked in interviews
3. **Know utility types** - Partial, Pick, Omit, etc.
4. **Understand type inference** - when and how TypeScript infers types
5. **Be familiar with best practices** - strict mode, avoiding 'any'
6. **Practice coding problems** - implement common patterns
7. **Understand OOP concepts** - classes, inheritance, access modifiers
8. **Know async patterns** - Promises, async/await
9. **Understand module systems** - ES6 modules, namespaces
10. **Be ready to explain trade-offs** - when to use types vs interfaces

---

## Resources for Further Learning

- Official TypeScript Handbook: typescriptlang.org/docs
- TypeScript Deep Dive: basarat.gitbook.io/typescript
- TypeScript Playground: typescriptlang.org/play
- Definitely Typed: github.com/DefinitelyTyped
- TypeScript GitHub: github.com/microsoft/TypeScript

---

**End of TypeScript Complete Interview Notes**

Good luck with your interview preparation!
