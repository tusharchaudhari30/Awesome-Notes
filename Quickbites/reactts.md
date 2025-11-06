# React + TypeScript Interview Notes: Complete Guide (Basics to Expert)

## Table of Contents

1. [TypeScript Fundamentals](#typescript-fundamentals)
2. [React with TypeScript Setup](#react-with-typescript-setup)
3. [Typing Components](#typing-components)
4. [Props and State](#props-and-state)
5. [Event Handling](#event-handling)
6. [Hooks with TypeScript](#hooks-with-typescript)
7. [Advanced Hook Types](#advanced-hook-types)
8. [Context API with TypeScript](#context-api-with-typescript)
9. [TypeScript Generics in React](#typescript-generics-in-react)
10. [Forms and Validation](#forms-and-validation)
11. [TypeScript Utility Types](#typescript-utility-types)
12. [Redux Toolkit with TypeScript](#redux-toolkit-with-typescript)
13. [Performance Optimization](#performance-optimization)
14. [Design Patterns](#design-patterns)
15. [Testing with TypeScript](#testing-with-typescript)
16. [Advanced TypeScript Patterns](#advanced-typescript-patterns)
17. [Best Practices](#best-practices)

---

## TypeScript Fundamentals

### What is TypeScript?

TypeScript is a **statically-typed superset** of JavaScript developed by Microsoft. It adds optional type annotations and compiles to plain JavaScript.

**Key Benefits:**

- **Type Safety**: Catch errors at compile time
- **Better IDE Support**: Autocompletion and IntelliSense
- **Self-Documenting**: Types serve as documentation
- **Refactoring**: Safer code modifications
- **Scalability**: Better for large codebases

### Basic Types

```typescript
// Primitive Types
let name: string = "John";
let age: number = 25;
let isActive: boolean = true;
let nothing: null = null;
let notDefined: undefined = undefined;

// Arrays
let numbers: number[] = [1, 2, 3];
let names: Array<string> = ["John", "Jane"];

// Tuple
let tuple: [string, number] = ["John", 25];

// Enum
enum Color {
  Red,
  Green,
  Blue,
}
let color: Color = Color.Red;

// Any (avoid when possible)
let dynamic: any = "can be anything";

// Unknown (safer than any)
let userInput: unknown;
userInput = 5;
userInput = "hello";

// Void (function returns nothing)
function logMessage(message: string): void {
  console.log(message);
}

// Never (function never returns)
function throwError(message: string): never {
  throw new Error(message);
}
```

### Interface vs Type

**Interface:**

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  age?: number; // Optional property
  readonly createdAt: Date; // Readonly property
}

// Extending interfaces
interface Admin extends User {
  role: string;
  permissions: string[];
}
```

**Type Alias:**

```typescript
type User = {
  id: number;
  name: string;
  email: string;
};

// Union types
type Status = "active" | "inactive" | "pending";

// Intersection types
type Admin = User & {
  role: string;
  permissions: string[];
};
```

**When to Use:**

- **Interface**: For objects, classes, and when you need declaration merging
- **Type**: For unions, intersections, primitives, and tuples

### Union and Intersection Types

```typescript
// Union Type (OR)
type ID = string | number;

function printID(id: ID) {
  if (typeof id === "string") {
    console.log(id.toUpperCase());
  } else {
    console.log(id);
  }
}

// Intersection Type (AND)
type Person = { name: string };
type Employee = { employeeId: number };
type Staff = Person & Employee;

const staff: Staff = {
  name: "John",
  employeeId: 123,
};
```

### Type Assertions

```typescript
// As syntax
let someValue: unknown = "this is a string";
let strLength: number = (someValue as string).length;

// Angle-bracket syntax (not in JSX)
let strLength2: number = (<string>someValue).length;
```

---

## React with TypeScript Setup

### Create React App with TypeScript

```bash
# New project
npx create-react-app my-app --template typescript

# Or with Vite (recommended)
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
npm run dev
```

### Project Structure

```
src/
├── components/
│   ├── Button.tsx
│   └── Button.types.ts
├── hooks/
│   └── useCustomHook.ts
├── types/
│   └── index.ts
├── utils/
│   └── helpers.ts
├── App.tsx
└── main.tsx
```

### tsconfig.json Configuration

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "moduleResolution": "bundler"
  },
  "include": ["src"],
  "exclude": ["node_modules"]
}
```

---

## Typing Components

### Functional Components

**Basic Functional Component:**

```typescript
import React from "react";

// Method 1: Function Declaration
function Greeting(): JSX.Element {
  return <h1>Hello, World!</h1>;
}

// Method 2: Arrow Function
const Greeting = (): JSX.Element => {
  return <h1>Hello, World!</h1>;
};

// Method 3: React.FC (Functional Component)
const Greeting: React.FC = () => {
  return <h1>Hello, World!</h1>;
};
```

**Note:** `React.FC` is less commonly used now as it has some drawbacks:

- Implicitly adds `children` prop
- Doesn't work well with generics
- Modern practice: explicitly type props

### Component with Props

```typescript
// Define props interface
interface GreetingProps {
  name: string;
  age: number;
  isStudent?: boolean; // Optional
}

// Method 1: Inline props type
function Greeting({ name, age, isStudent }: GreetingProps): JSX.Element {
  return (
    <div>
      <h1>Hello, {name}!</h1>
      <p>Age: {age}</p>
      {isStudent && <p>Student</p>}
    </div>
  );
}

// Method 2: Separate props parameter
function Greeting(props: GreetingProps): JSX.Element {
  return (
    <div>
      <h1>Hello, {props.name}!</h1>
      <p>Age: {props.age}</p>
    </div>
  );
}

// Usage
<Greeting name="John" age={25} isStudent={true} />;
```

### Children Props

```typescript
// Method 1: React.ReactNode
interface CardProps {
  title: string;
  children: React.ReactNode;
}

const Card = ({ title, children }: CardProps) => {
  return (
    <div>
      <h2>{title}</h2>
      <div>{children}</div>
    </div>
  );
};

// Method 2: React.PropsWithChildren
interface CardProps {
  title: string;
}

const Card = ({ title, children }: React.PropsWithChildren<CardProps>) => {
  return (
    <div>
      <h2>{title}</h2>
      <div>{children}</div>
    </div>
  );
};

// Usage
<Card title="My Card">
  <p>Card content</p>
</Card>;
```

### Default Props

```typescript
interface ButtonProps {
  label: string;
  variant?: "primary" | "secondary";
  disabled?: boolean;
}

const Button = ({
  label,
  variant = "primary",
  disabled = false,
}: ButtonProps) => {
  return (
    <button className={variant} disabled={disabled}>
      {label}
    </button>
  );
};
```

---

## Props and State

### Props Types

```typescript
// String literal union
interface ButtonProps {
  variant: "primary" | "secondary" | "danger";
  size: "small" | "medium" | "large";
}

// Function props
interface FormProps {
  onSubmit: (data: FormData) => void;
  onChange: (value: string) => void;
}

// Object props
interface User {
  id: number;
  name: string;
  email: string;
}

interface UserCardProps {
  user: User;
  onDelete: (id: number) => void;
}

// Array props
interface ListProps {
  items: string[];
  users: User[];
}

// Extending HTML attributes
interface CustomButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant: "primary" | "secondary";
}

const CustomButton = ({ variant, ...props }: CustomButtonProps) => {
  return <button {...props} className={variant} />;
};

// Usage
<CustomButton
  variant="primary"
  onClick={() => {}}
  disabled={false}
  aria-label="Submit"
/>;
```

### State with TypeScript

```typescript
import { useState } from "react";

// Primitive state
const [count, setCount] = useState<number>(0);
const [name, setName] = useState<string>("");
const [isActive, setIsActive] = useState<boolean>(false);

// Object state
interface User {
  id: number;
  name: string;
  email: string;
}

const [user, setUser] = useState<User>({
  id: 1,
  name: "John",
  email: "john@example.com",
});

// Update object state
setUser({ ...user, name: "Jane" });

// Array state
const [items, setItems] = useState<string[]>([]);
const [users, setUsers] = useState<User[]>([]);

// Nullable state
const [user, setUser] = useState<User | null>(null);

// State with initial function
const [count, setCount] = useState<number>(() => {
  const saved = localStorage.getItem("count");
  return saved ? parseInt(saved) : 0;
});

// Complex state example
interface FormState {
  username: string;
  email: string;
  age: number;
  terms: boolean;
}

const [formData, setFormData] = useState<FormState>({
  username: "",
  email: "",
  age: 0,
  terms: false,
});

const handleChange = (field: keyof FormState, value: any) => {
  setFormData((prev) => ({ ...prev, [field]: value }));
};
```

---

## Event Handling

### Common Event Types

```typescript
import React from "react";

// Click Events
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
  console.log(e.currentTarget.value);
};

<button onClick={handleClick}>Click me</button>;

// Change Events
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  console.log(e.target.value);
};

<input onChange={handleChange} />;

// Form Submit
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
  const formData = new FormData(e.currentTarget);
};

<form onSubmit={handleSubmit}>
  <button type="submit">Submit</button>
</form>;

// Focus Events
const handleFocus = (e: React.FocusEvent<HTMLInputElement>) => {
  console.log("Input focused");
};

<input onFocus={handleFocus} onBlur={handleFocus} />;

// Keyboard Events
const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
  if (e.key === "Enter") {
    console.log("Enter pressed");
  }
};

<input onKeyDown={handleKeyDown} />;

// Mouse Events
const handleMouseEnter = (e: React.MouseEvent<HTMLDivElement>) => {
  console.log("Mouse entered");
};

<div
  onMouseEnter={handleMouseEnter}
  onMouseLeave={handleMouseEnter}
  onMouseMove={handleMouseEnter}
>
  Hover me
</div>;
```

### Complete Form Example

```typescript
import React, { useState } from "react";

interface FormData {
  username: string;
  email: string;
  password: string;
}

const LoginForm = () => {
  const [formData, setFormData] = useState<FormData>({
    username: "",
    email: "",
    password: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log("Form submitted:", formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        name="username"
        value={formData.username}
        onChange={handleChange}
        placeholder="Username"
      />
      <input
        type="email"
        name="email"
        value={formData.email}
        onChange={handleChange}
        placeholder="Email"
      />
      <input
        type="password"
        name="password"
        value={formData.password}
        onChange={handleChange}
        placeholder="Password"
      />
      <button type="submit">Submit</button>
    </form>
  );
};
```

### Type-Safe Event Handlers

```typescript
// Generic event handler
type EventHandler<T = HTMLElement> = (e: React.MouseEvent<T>) => void;

interface ButtonProps {
  onClick: EventHandler<HTMLButtonElement>;
}

// Using the generic type
const Button = ({ onClick }: ButtonProps) => {
  return <button onClick={onClick}>Click me</button>;
};
```

---

## Hooks with TypeScript

### useState

```typescript
import { useState } from "react";

// Type inference (TypeScript infers type)
const [count, setCount] = useState(0); // number
const [name, setName] = useState("John"); // string

// Explicit typing
const [count, setCount] = useState<number>(0);

// With custom type
interface User {
  id: number;
  name: string;
}

const [user, setUser] = useState<User | null>(null);

// With union type
type Status = "idle" | "loading" | "success" | "error";
const [status, setStatus] = useState<Status>("idle");

// Array state
const [items, setItems] = useState<string[]>([]);

// Complex state
interface FormState {
  email: string;
  password: string;
  remember: boolean;
}

const [form, setForm] = useState<FormState>({
  email: "",
  password: "",
  remember: false,
});
```

### useEffect

```typescript
import { useEffect, useState } from "react";

// Basic useEffect
useEffect(() => {
  console.log("Component mounted");
}, []);

// With cleanup
useEffect(() => {
  const timer = setInterval(() => {
    console.log("Tick");
  }, 1000);

  return () => clearInterval(timer);
}, []);

// With dependencies
const [count, setCount] = useState(0);

useEffect(() => {
  document.title = `Count: ${count}`;
}, [count]);

// Async in useEffect
useEffect(() => {
  const fetchData = async () => {
    try {
      const response = await fetch("/api/users");
      const data: User[] = await response.json();
      setUsers(data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  fetchData();
}, []);

// Type-safe dependencies
interface Props {
  userId: number;
}

const UserProfile = ({ userId }: Props) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]); // TypeScript ensures userId is in dependencies
};
```

### useRef

```typescript
import { useRef, useEffect } from "react";

// DOM element ref
const inputRef = useRef<HTMLInputElement>(null);

useEffect(() => {
  inputRef.current?.focus();
}, []);

<input ref={inputRef} />;

// Mutable value ref
const countRef = useRef<number>(0);

const increment = () => {
  countRef.current++;
  console.log(countRef.current);
};

// Previous value ref
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

// Usage
const [count, setCount] = useState(0);
const previousCount = usePrevious(count);
```

### useReducer

```typescript
import { useReducer } from "react";

// Define state type
interface State {
  count: number;
  error: string | null;
}

// Define action types
type Action =
  | { type: "INCREMENT" }
  | { type: "DECREMENT" }
  | { type: "RESET" }
  | { type: "SET_ERROR"; payload: string };

// Reducer function
const reducer = (state: State, action: Action): State => {
  switch (action.type) {
    case "INCREMENT":
      return { ...state, count: state.count + 1 };
    case "DECREMENT":
      return { ...state, count: state.count - 1 };
    case "RESET":
      return { ...state, count: 0 };
    case "SET_ERROR":
      return { ...state, error: action.payload };
    default:
      return state;
  }
};

// Component
const Counter = () => {
  const [state, dispatch] = useReducer(reducer, { count: 0, error: null });

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: "INCREMENT" })}>+</button>
      <button onClick={() => dispatch({ type: "DECREMENT" })}>-</button>
      <button onClick={() => dispatch({ type: "RESET" })}>Reset</button>
    </div>
  );
};
```

### useMemo

```typescript
import { useMemo, useState } from "react";

interface Product {
  id: number;
  name: string;
  price: number;
  category: string;
}

const ProductList = ({ products }: { products: Product[] }) => {
  const [filter, setFilter] = useState("");

  // Memoize filtered products
  const filteredProducts = useMemo(() => {
    console.log("Filtering products...");
    return products.filter((product) =>
      product.name.toLowerCase().includes(filter.toLowerCase())
    );
  }, [products, filter]);

  // Memoize expensive calculation
  const totalPrice = useMemo(() => {
    return filteredProducts.reduce((sum, product) => sum + product.price, 0);
  }, [filteredProducts]);

  return (
    <div>
      <input value={filter} onChange={(e) => setFilter(e.target.value)} />
      <p>Total: ${totalPrice}</p>
      {filteredProducts.map((product) => (
        <div key={product.id}>{product.name}</div>
      ))}
    </div>
  );
};
```

### useCallback

```typescript
import { useCallback, useState, memo } from "react";

interface ChildProps {
  onClick: () => void;
}

// Child component (memoized)
const Child = memo(({ onClick }: ChildProps) => {
  console.log("Child rendered");
  return <button onClick={onClick}>Click me</button>;
});

// Parent component
const Parent = () => {
  const [count, setCount] = useState(0);
  const [text, setText] = useState("");

  // Without useCallback - new function on every render
  // const handleClick = () => {
  //   console.log('Clicked');
  // };

  // With useCallback - stable function reference
  const handleClick = useCallback(() => {
    console.log("Clicked");
  }, []);

  // useCallback with dependencies
  const handleIncrement = useCallback(() => {
    setCount((c) => c + 1);
  }, []);

  return (
    <div>
      <input value={text} onChange={(e) => setText(e.target.value)} />
      <p>Count: {count}</p>
      <Child onClick={handleClick} />
    </div>
  );
};
```

---

## Advanced Hook Types

### Custom Hooks

```typescript
import { useState, useEffect } from "react";

// useFetch Hook
function useFetch<T>(url: string): {
  data: T | null;
  loading: boolean;
  error: Error | null;
} {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch(url);
        const json = await response.json();
        setData(json);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error };
}

// Usage
interface User {
  id: number;
  name: string;
  email: string;
}

const UserProfile = () => {
  const { data, loading, error } = useFetch<User>("/api/user");

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!data) return null;

  return <div>{data.name}</div>;
};
```

**useLocalStorage Hook:**

```typescript
function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  const setValue = (value: T) => {
    try {
      setStoredValue(value);
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue];
}

// Usage
const [name, setName] = useLocalStorage<string>("name", "John");
```

**useToggle Hook:**

```typescript
function useToggle(initialValue: boolean = false): [boolean, () => void] {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => {
    setValue((v) => !v);
  }, []);

  return [value, toggle];
}

// Usage
const [isOpen, toggle] = useToggle(false);
```

**useDebounce Hook:**

```typescript
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
const SearchComponent = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const debouncedSearch = useDebounce(searchTerm, 500);

  useEffect(() => {
    if (debouncedSearch) {
      // Make API call
      fetchResults(debouncedSearch);
    }
  }, [debouncedSearch]);

  return (
    <input value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} />
  );
};
```

### useImperativeHandle

```typescript
import { forwardRef, useImperativeHandle, useRef } from "react";

// Define the exposed methods
interface InputHandle {
  focus: () => void;
  clear: () => void;
  getValue: () => string;
}

// Component with forwardRef
const CustomInput = forwardRef<InputHandle, { placeholder?: string }>(
  (props, ref) => {
    const inputRef = useRef<HTMLInputElement>(null);

    useImperativeHandle(ref, () => ({
      focus: () => {
        inputRef.current?.focus();
      },
      clear: () => {
        if (inputRef.current) {
          inputRef.current.value = "";
        }
      },
      getValue: () => {
        return inputRef.current?.value || "";
      },
    }));

    return <input ref={inputRef} {...props} />;
  }
);

// Parent component
const ParentComponent = () => {
  const inputRef = useRef<InputHandle>(null);

  const handleClick = () => {
    inputRef.current?.focus();
    console.log(inputRef.current?.getValue());
  };

  return (
    <div>
      <CustomInput ref={inputRef} placeholder="Enter text" />
      <button onClick={handleClick}>Focus & Get Value</button>
    </div>
  );
};
```

---

## Context API with TypeScript

### Basic Context Setup

```typescript
import { createContext, useContext, useState, ReactNode } from "react";

// Define context type
interface ThemeContextType {
  theme: "light" | "dark";
  toggleTheme: () => void;
}

// Create context with default value
const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Provider component
interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider = ({ children }: ThemeProviderProps) => {
  const [theme, setTheme] = useState<"light" | "dark">("light");

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

// Custom hook to use context
export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);

  if (context === undefined) {
    throw new Error("useTheme must be used within ThemeProvider");
  }

  return context;
};

// Usage in component
const App = () => {
  return (
    <ThemeProvider>
      <ThemedButton />
    </ThemeProvider>
  );
};

const ThemedButton = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      style={{ background: theme === "light" ? "#fff" : "#333" }}
    >
      Toggle Theme
    </button>
  );
};
```

### Complex Context with Reducer

```typescript
import { createContext, useContext, useReducer, ReactNode } from "react";

// Define types
interface User {
  id: number;
  name: string;
  email: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
}

type AuthAction =
  | { type: "LOGIN"; payload: User }
  | { type: "LOGOUT" }
  | { type: "SET_LOADING"; payload: boolean };

interface AuthContextType {
  state: AuthState;
  login: (user: User) => void;
  logout: () => void;
}

// Reducer
const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case "LOGIN":
      return {
        ...state,
        user: action.payload,
        isAuthenticated: true,
        loading: false,
      };
    case "LOGOUT":
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        loading: false,
      };
    case "SET_LOADING":
      return {
        ...state,
        loading: action.payload,
      };
    default:
      return state;
  }
};

// Create context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Provider
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(authReducer, {
    user: null,
    isAuthenticated: false,
    loading: false,
  });

  const login = (user: User) => {
    dispatch({ type: "LOGIN", payload: user });
  };

  const logout = () => {
    dispatch({ type: "LOGOUT" });
  };

  return (
    <AuthContext.Provider value={{ state, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook
export const useAuth = () => {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error("useAuth must be used within AuthProvider");
  }

  return context;
};
```

---

## TypeScript Generics in React

### Generic Components

```typescript
// Generic List Component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}

// Usage
interface User {
  id: number;
  name: string;
}

const users: User[] = [
  { id: 1, name: "John" },
  { id: 2, name: "Jane" },
];

<List<User> items={users} renderItem={(user) => <div>{user.name}</div>} />;
```

**Generic Table Component:**

```typescript
interface Column<T> {
  key: keyof T;
  header: string;
  render?: (value: T[keyof T], item: T) => React.ReactNode;
}

interface TableProps<T> {
  data: T[];
  columns: Column<T>[];
}

function Table<T extends { id: number | string }>({
  data,
  columns,
}: TableProps<T>) {
  return (
    <table>
      <thead>
        <tr>
          {columns.map((col) => (
            <th key={String(col.key)}>{col.header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((item) => (
          <tr key={item.id}>
            {columns.map((col) => (
              <td key={String(col.key)}>
                {col.render
                  ? col.render(item[col.key], item)
                  : String(item[col.key])}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// Usage
interface Product {
  id: number;
  name: string;
  price: number;
}

const products: Product[] = [
  { id: 1, name: "Laptop", price: 999 },
  { id: 2, name: "Mouse", price: 29 },
];

<Table<Product>
  data={products}
  columns={[
    { key: "name", header: "Product Name" },
    {
      key: "price",
      header: "Price",
      render: (value) => `$${value}`,
    },
  ]}
/>;
```

### Generic Hooks

```typescript
// Generic useArray Hook
function useArray<T>(initialValue: T[]) {
  const [array, setArray] = useState<T[]>(initialValue);

  const push = (element: T) => {
    setArray((prev) => [...prev, element]);
  };

  const filter = (callback: (item: T) => boolean) => {
    setArray((prev) => prev.filter(callback));
  };

  const update = (index: number, newElement: T) => {
    setArray((prev) => [
      ...prev.slice(0, index),
      newElement,
      ...prev.slice(index + 1),
    ]);
  };

  const remove = (index: number) => {
    setArray((prev) => [...prev.slice(0, index), ...prev.slice(index + 1)]);
  };

  const clear = () => setArray([]);

  return { array, set: setArray, push, filter, update, remove, clear };
}

// Usage
const { array, push, remove } = useArray<number>([1, 2, 3]);
```

---

## Forms and Validation

### Controlled Form

```typescript
import { useState, FormEvent, ChangeEvent } from "react";

interface FormData {
  email: string;
  password: string;
  remember: boolean;
}

interface FormErrors {
  email?: string;
  password?: string;
}

const LoginForm = () => {
  const [formData, setFormData] = useState<FormData>({
    email: "",
    password: "",
    remember: false,
  });

  const [errors, setErrors] = useState<FormErrors>({});

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const validate = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.email) {
      newErrors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Email is invalid";
    }

    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 6) {
      newErrors.password = "Password must be at least 6 characters";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (validate()) {
      console.log("Form submitted:", formData);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="Email"
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>

      <div>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          placeholder="Password"
        />
        {errors.password && <span className="error">{errors.password}</span>}
      </div>

      <div>
        <label>
          <input
            type="checkbox"
            name="remember"
            checked={formData.remember}
            onChange={handleChange}
          />
          Remember me
        </label>
      </div>

      <button type="submit">Login</button>
    </form>
  );
};
```

### Type-Safe Form Elements

```typescript
// Extending HTML form element
interface FormElements extends HTMLFormControlsCollection {
  email: HTMLInputElement;
  password: HTMLInputElement;
}

interface LoginFormElement extends HTMLFormElement {
  readonly elements: FormElements;
}

const LoginForm = () => {
  const handleSubmit = (e: FormEvent<LoginFormElement>) => {
    e.preventDefault();

    const email = e.currentTarget.elements.email.value;
    const password = e.currentTarget.elements.password.value;

    console.log({ email, password });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" />
      <input name="password" type="password" />
      <button type="submit">Submit</button>
    </form>
  );
};
```

---

## TypeScript Utility Types

### Partial<Type>

Makes all properties optional.

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  age: number;
}

// All properties optional
type PartialUser = Partial<User>;

// Usage: Updating user (only some fields)
function updateUser(id: number, updates: Partial<User>) {
  // Only update provided fields
  console.log("Updating user", id, updates);
}

updateUser(1, { name: "John" }); // Valid
updateUser(2, { email: "john@example.com", age: 25 }); // Valid
```

### Required<Type>

Makes all properties required.

```typescript
interface Config {
  apiUrl?: string;
  timeout?: number;
  retries?: number;
}

// All properties required
type RequiredConfig = Required<Config>;

const config: RequiredConfig = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
  retries: 3,
}; // All fields must be provided
```

### Pick<Type, Keys>

Picks specific properties from a type.

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  password: string;
  age: number;
}

// Pick only specific properties
type UserPreview = Pick<User, "id" | "name" | "email">;

const preview: UserPreview = {
  id: 1,
  name: "John",
  email: "john@example.com",
  // password and age not needed
};
```

### Omit<Type, Keys>

Omits specific properties from a type.

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  password: string;
}

// Omit sensitive fields
type PublicUser = Omit<User, "password">;

const publicUser: PublicUser = {
  id: 1,
  name: "John",
  email: "john@example.com",
  // password is omitted
};

// Omit multiple fields
type UserWithoutIds = Omit<User, "id" | "password">;
```

### Record<Keys, Type>

Creates an object type with specified keys and value type.

```typescript
// Create a type with string keys and number values
type PageViews = Record<string, number>;

const views: PageViews = {
  home: 1000,
  about: 500,
  contact: 200,
};

// With union type keys
type Page = "home" | "about" | "contact";
type PageInfo = Record<Page, { title: string; views: number }>;

const pages: PageInfo = {
  home: { title: "Home", views: 1000 },
  about: { title: "About", views: 500 },
  contact: { title: "Contact", views: 200 },
};
```

### Readonly<Type>

Makes all properties readonly.

```typescript
interface User {
  id: number;
  name: string;
}

type ReadonlyUser = Readonly<User>;

const user: ReadonlyUser = {
  id: 1,
  name: "John",
};

// user.name = 'Jane'; // Error: Cannot assign to 'name' because it is read-only
```

### ReturnType<Type>

Gets the return type of a function.

```typescript
function getUser() {
  return {
    id: 1,
    name: "John",
    email: "john@example.com",
  };
}

// Get return type of function
type User = ReturnType<typeof getUser>;

// User is now: { id: number; name: string; email: string }
```

### Practical Example: Form Builder

```typescript
interface FormConfig {
  username: {
    type: "text";
    required: true;
    minLength: 3;
  };
  email: {
    type: "email";
    required: true;
  };
  age: {
    type: "number";
    required: false;
    min: 18;
  };
}

// Extract field names
type FormFields = keyof FormConfig;

// Create form data type (all fields optional initially)
type FormData = Partial<Record<FormFields, string | number>>;

// Create validation errors type
type FormErrors = Partial<Record<FormFields, string>>;

// Usage
const formData: FormData = {
  username: "john_doe",
  email: "john@example.com",
};

const errors: FormErrors = {
  username: "Username too short",
};
```

---

## Redux Toolkit with TypeScript

### Store Setup

```typescript
// store.ts
import { configureStore } from "@reduxjs/toolkit";
import counterReducer from "./features/counter/counterSlice";
import userReducer from "./features/user/userSlice";

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    user: userReducer,
  },
});

// Infer types from store
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### Custom Hooks

```typescript
// hooks.ts
import { TypedUseSelectorHook, useDispatch, useSelector } from "react-redux";
import type { RootState, AppDispatch } from "./store";

// Typed versions of useDispatch and useSelector
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

### Slice with TypeScript

```typescript
// counterSlice.ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface CounterState {
  value: number;
  status: "idle" | "loading" | "failed";
}

const initialState: CounterState = {
  value: 0,
  status: "idle",
};

const counterSlice = createSlice({
  name: "counter",
  initialState,
  reducers: {
    increment: (state) => {
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    },
    incrementByAmount: (state, action: PayloadAction<number>) => {
      state.value += action.payload;
    },
    reset: (state) => {
      state.value = 0;
    },
  },
});

export const { increment, decrement, incrementByAmount, reset } =
  counterSlice.actions;
export default counterSlice.reducer;
```

### Async Thunks

```typescript
// userSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";

interface User {
  id: number;
  name: string;
  email: string;
}

interface UserState {
  users: User[];
  loading: boolean;
  error: string | null;
}

const initialState: UserState = {
  users: [],
  loading: false,
  error: null,
};

// Async thunk
export const fetchUsers = createAsyncThunk<User[], void>(
  "user/fetchUsers",
  async () => {
    const response = await fetch("/api/users");
    return response.json();
  }
);

// Async thunk with argument
export const fetchUserById = createAsyncThunk<User, number>(
  "user/fetchUserById",
  async (userId: number) => {
    const response = await fetch(`/api/users/${userId}`);
    return response.json();
  }
);

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    addUser: (state, action: PayloadAction<User>) => {
      state.users.push(action.payload);
    },
    removeUser: (state, action: PayloadAction<number>) => {
      state.users = state.users.filter((user) => user.id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUsers.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchUsers.fulfilled, (state, action) => {
        state.loading = false;
        state.users = action.payload;
      })
      .addCase(fetchUsers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || "Failed to fetch users";
      });
  },
});

export const { addUser, removeUser } = userSlice.actions;
export default userSlice.reducer;
```

### Using Redux in Components

```typescript
import { useAppDispatch, useAppSelector } from "./hooks";
import {
  increment,
  decrement,
  incrementByAmount,
} from "./features/counter/counterSlice";
import { fetchUsers } from "./features/user/userSlice";

const Counter = () => {
  const count = useAppSelector((state) => state.counter.value);
  const dispatch = useAppDispatch();

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => dispatch(increment())}>+</button>
      <button onClick={() => dispatch(decrement())}>-</button>
      <button onClick={() => dispatch(incrementByAmount(5))}>+5</button>
    </div>
  );
};

const UserList = () => {
  const { users, loading, error } = useAppSelector((state) => state.user);
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(fetchUsers());
  }, [dispatch]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
};
```

---

## Performance Optimization

### React.memo with TypeScript

```typescript
import { memo } from "react";

interface Props {
  name: string;
  age: number;
}

// Basic memo
const UserCard = memo<Props>(({ name, age }) => {
  console.log("UserCard rendered");
  return (
    <div>
      <p>{name}</p>
      <p>{age}</p>
    </div>
  );
});

// Memo with custom comparison
const UserCard = memo<Props>(
  ({ name, age }) => {
    return (
      <div>
        <p>{name}</p>
        <p>{age}</p>
      </div>
    );
  },
  (prevProps, nextProps) => {
    // Return true if props are equal (skip re-render)
    return prevProps.name === nextProps.name && prevProps.age === nextProps.age;
  }
);
```

### Lazy Loading

```typescript
import { lazy, Suspense } from "react";

// Lazy load component
const Dashboard = lazy(() => import("./components/Dashboard"));
const Profile = lazy(() => import("./components/Profile"));

const App = () => {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Dashboard />
      <Profile />
    </Suspense>
  );
};
```

### Type-Safe Performance Patterns

```typescript
import { memo, useCallback, useMemo } from "react";

interface Item {
  id: number;
  name: string;
  price: number;
}

interface Props {
  items: Item[];
  onItemClick: (id: number) => void;
}

const ItemList = memo<Props>(({ items, onItemClick }) => {
  // Memoize filtered items
  const expensiveItems = useMemo(() => {
    return items.filter((item) => item.price > 100);
  }, [items]);

  // Memoize handler
  const handleClick = useCallback(
    (id: number) => {
      onItemClick(id);
    },
    [onItemClick]
  );

  return (
    <ul>
      {expensiveItems.map((item) => (
        <li key={item.id} onClick={() => handleClick(item.id)}>
          {item.name} - ${item.price}
        </li>
      ))}
    </ul>
  );
});
```

---

## Design Patterns

### Discriminated Unions

```typescript
// Define discriminated union for different states
type FetchState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: string };

function DisplayData<T>({ state }: { state: FetchState<T> }) {
  // TypeScript narrows type based on status
  switch (state.status) {
    case "idle":
      return <div>Not started</div>;
    case "loading":
      return <div>Loading...</div>;
    case "success":
      return <div>Data: {JSON.stringify(state.data)}</div>;
    case "error":
      return <div>Error: {state.error}</div>;
  }
}

// Usage
interface User {
  id: number;
  name: string;
}

const [userState, setUserState] = useState<FetchState<User>>({
  status: "idle",
});
```

**Button with Discriminated Union:**

```typescript
type ButtonProps =
  | {
      variant: 'primary';
      onClick: () => void;
    }
  | {
      variant: 'link';
      href: string;
    };

const Button = (props: ButtonProps) => {
  if (props.variant === 'primary') {
    return <button onClick={props.onClick}>Click me</button>;
  }

  return <a href={props.href}>Link</a>;
};

// TypeScript enforces correct props
<Button variant="primary" onClick={() => {}} />
<Button variant="link" href="/about" />
```

### HOC with TypeScript

```typescript
import { ComponentType } from "react";

// HOC that adds loading prop
interface WithLoadingProps {
  loading: boolean;
}

function withLoading<P extends object>(
  Component: ComponentType<P>
): ComponentType<P & WithLoadingProps> {
  return ({ loading, ...props }: WithLoadingProps & P) => {
    if (loading) {
      return <div>Loading...</div>;
    }
    return <Component {...(props as P)} />;
  };
}

// Usage
interface UserListProps {
  users: User[];
}

const UserList = ({ users }: UserListProps) => {
  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
};

const UserListWithLoading = withLoading(UserList);

// Use component
<UserListWithLoading loading={false} users={users} />;
```

### Render Props Pattern

```typescript
interface MousePosition {
  x: number;
  y: number;
}

interface MouseTrackerProps {
  render: (position: MousePosition) => React.ReactNode;
}

const MouseTracker = ({ render }: MouseTrackerProps) => {
  const [position, setPosition] = useState<MousePosition>({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return <>{render(position)}</>;
};

// Usage
<MouseTracker
  render={({ x, y }) => (
    <div>
      Mouse position: {x}, {y}
    </div>
  )}
/>;
```

---

## Testing with TypeScript

### Component Testing

```typescript
import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import Counter from "./Counter";

describe("Counter Component", () => {
  test("renders initial count", () => {
    render(<Counter initialCount={0} />);

    const countElement = screen.getByText(/count: 0/i);
    expect(countElement).toBeInTheDocument();
  });

  test("increments count on button click", () => {
    render(<Counter initialCount={0} />);

    const button = screen.getByRole("button", { name: /increment/i });
    fireEvent.click(button);

    expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
  });

  test("calls callback with correct value", () => {
    const mockCallback = jest.fn();
    render(<Counter initialCount={0} onChange={mockCallback} />);

    const button = screen.getByRole("button", { name: /increment/i });
    fireEvent.click(button);

    expect(mockCallback).toHaveBeenCalledWith(1);
  });
});
```

### Hook Testing

```typescript
import { renderHook, act } from "@testing-library/react";
import { useCounter } from "./useCounter";

describe("useCounter", () => {
  test("should increment counter", () => {
    const { result } = renderHook(() => useCounter(0));

    expect(result.current.count).toBe(0);

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  test("should decrement counter", () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(4);
  });
});
```

---

## Advanced TypeScript Patterns

### Conditional Types

```typescript
// Extract array element type
type ArrayElement<T> = T extends (infer U)[] ? U : never;

type NumberArray = number[];
type ElementType = ArrayElement<NumberArray>; // number

// Conditional component props
type ButtonProps<T extends "button" | "link"> = T extends "button"
  ? { type: "button"; onClick: () => void }
  : { type: "link"; href: string };

function Button<T extends "button" | "link">(props: ButtonProps<T>) {
  // Implementation
}
```

### Mapped Types

```typescript
// Make all properties nullable
type Nullable<T> = {
  [K in keyof T]: T[K] | null;
};

interface User {
  id: number;
  name: string;
}

type NullableUser = Nullable<User>;
// { id: number | null; name: string | null }

// Make specific properties optional
type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

type UserWithOptionalEmail = PartialBy<User, "email">;
```

### Template Literal Types

```typescript
// Event names
type EventName<T extends string> = `on${Capitalize<T>}`;

type ClickEvent = EventName<"click">; // 'onClick'
type ChangeEvent = EventName<"change">; // 'onChange'

// CSS properties
type CSSProperty = "color" | "backgroundColor" | "fontSize";
type CSSValue = string | number;

type StyleObject = {
  [K in CSSProperty]: CSSValue;
};
```

---

## Best Practices

### 1. Enable Strict Mode

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true
  }
}
```

### 2. Avoid `any`

```typescript
// Bad
const getData = (data: any) => {
  return data.value;
};

// Good
interface Data {
  value: string;
}

const getData = (data: Data) => {
  return data.value;
};

// Or use unknown for truly unknown types
const processData = (data: unknown) => {
  if (typeof data === "object" && data !== null) {
    // Type guard to safely access properties
  }
};
```

### 3. Use Type Inference

```typescript
// Bad - unnecessary type annotation
const name: string = "John";
const numbers: number[] = [1, 2, 3];

// Good - let TypeScript infer
const name = "John";
const numbers = [1, 2, 3];
```

### 4. Use `readonly` for Immutability

```typescript
interface Props {
  readonly items: readonly string[];
  readonly user: Readonly<User>;
}

// Cannot modify
props.items.push("new"); // Error
props.user.name = "New Name"; // Error
```

### 5. Prefer Interfaces for Objects

```typescript
// Good - use interface for objects
interface User {
  id: number;
  name: string;
}

// Use type for unions, intersections
type Status = "active" | "inactive";
type AdminUser = User & { role: string };
```

### 6. Use Type Guards

```typescript
function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value
  );
}

function processValue(value: unknown) {
  if (isUser(value)) {
    console.log(value.name); // TypeScript knows it's a User
  }
}
```

### 7. Namespace Components

```typescript
// Component with sub-components
const Card = ({ children }: { children: React.ReactNode }) => {
  return <div className="card">{children}</div>;
};

Card.Header = ({ children }: { children: React.ReactNode }) => {
  return <div className="card-header">{children}</div>;
};

Card.Body = ({ children }: { children: React.ReactNode }) => {
  return <div className="card-body">{children}</div>;
};

// Usage
<Card>
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
</Card>;
```

### 8. Use Const Assertions

```typescript
// Without const assertion
const colors = ["red", "blue"]; // string[]

// With const assertion
const colors = ["red", "blue"] as const; // readonly ['red', 'blue']

// Now can use as literal type
type Color = (typeof colors)[number]; // 'red' | 'blue'
```

### 9. Type Your Async Functions

```typescript
async function fetchUser(id: number): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

// Use with error handling
async function fetchUserSafe(id: number): Promise<User | null> {
  try {
    const response = await fetch(`/api/users/${id}`);
    return response.json();
  } catch (error) {
    console.error(error);
    return null;
  }
}
```

### 10. Organize Types

```typescript
// types/user.ts
export interface User {
  id: number;
  name: string;
  email: string;
}

export type UserRole = "admin" | "user" | "guest";

export interface AuthUser extends User {
  role: UserRole;
  token: string;
}

// components/UserCard.tsx
import type { User } from "../types/user";
```

---

## Common Interview Questions

### 1. Why use TypeScript with React?

- **Type Safety**: Catch errors at compile time
- **Better IDE Support**: Autocompletion and IntelliSense
- **Refactoring**: Safer code changes
- **Documentation**: Types serve as documentation
- **Scalability**: Better for large teams

### 2. Interface vs Type?

- **Interface**: Better for objects, supports declaration merging
- **Type**: Can represent unions, intersections, primitives
- **Recommendation**: Use interface for component props

### 3. How to type children props?

```typescript
React.ReactNode; // Most flexible
React.ReactElement; // Single React element
React.ReactChild; // String, number, or element
JSX.Element; // Result of JSX expression
```

### 4. How to type event handlers?

```typescript
React.MouseEvent<HTMLButtonElement>;
React.ChangeEvent<HTMLInputElement>;
React.FormEvent<HTMLFormElement>;
React.KeyboardEvent<HTMLInputElement>;
```

### 5. How to create generic components?

```typescript
interface Props<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>(props: Props<T>) {
  return <ul>{props.items.map(props.renderItem)}</ul>;
}
```

### 6. How to type Redux with TypeScript?

- Define `RootState` and `AppDispatch` types
- Use `createSlice` with typed initial state
- Type async thunks with return type
- Use typed hooks (`useAppSelector`, `useAppDispatch`)

### 7. What are utility types?

- `Partial<T>`: All properties optional
- `Required<T>`: All properties required
- `Pick<T, K>`: Select specific properties
- `Omit<T, K>`: Exclude specific properties
- `Record<K, T>`: Object with specific keys and values

### 8. How to handle optional props?

```typescript
interface Props {
  name: string;
  age?: number; // Optional
}

// With default value
const Component = ({ name, age = 18 }: Props) => {
  // age is now number (not undefined)
};
```

---

## Resources

- **Official TypeScript Docs**: https://www.typescriptlang.org/docs/
- **React TypeScript Cheatsheet**: https://react-typescript-cheatsheet.netlify.app/
- **TypeScript Playground**: https://www.typescriptlang.org/play
- **Total TypeScript**: https://www.totaltypescript.com/
- **Type Challenges**: https://github.com/type-challenges/type-challenges

---

**Good luck with your React + TypeScript interview! 🚀**
