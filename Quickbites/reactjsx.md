# React Interview Notes: Complete Guide (Basics to Expert)

## Table of Contents

1. [React Fundamentals](#react-fundamentals)
2. [JSX](#jsx)
3. [Components](#components)
4. [Props vs State](#props-vs-state)
5. [React Hooks](#react-hooks)
6. [Component Lifecycle](#component-lifecycle)
7. [Advanced Hooks](#advanced-hooks)
8. [Performance Optimization](#performance-optimization)
9. [React Design Patterns](#react-design-patterns)
10. [State Management](#state-management)
11. [Error Handling](#error-handling)
12. [Testing](#testing)
13. [Advanced Concepts](#advanced-concepts)

---

## React Fundamentals

### What is React?

React is a JavaScript library developed by Facebook for building user interfaces, particularly for single-page applications. It allows developers to create reusable UI components and efficiently update the view when data changes.

**Key Features:**

- **Component-Based Architecture**: Build encapsulated components that manage their own state
- **Virtual DOM**: Efficiently updates only changed parts of the UI
- **Unidirectional Data Flow**: Data flows from parent to child components
- **JSX**: Syntax extension allowing HTML-like code in JavaScript
- **Declarative**: Describe what the UI should look like, React handles the updates

### How React Works

React uses a Virtual DOM to optimize rendering:

1. When state changes, React creates a new Virtual DOM tree
2. React compares (reconciliation) the new Virtual DOM with the previous one
3. React calculates the minimal set of changes needed
4. React updates only the changed parts in the real DOM

---

## JSX

### What is JSX?

JSX (JavaScript XML) is a syntax extension for JavaScript that allows you to write HTML-like code in JavaScript files.

**Example:**

```javascript
const element = <h1>Hello, World!</h1>;
```

### JSX Transformation

JSX is transpiled by Babel into `React.createElement()` calls:

```javascript
// JSX
const element = <h1 className="greeting">Hello, World!</h1>;

// Transpiled JavaScript
const element = React.createElement(
  "h1",
  { className: "greeting" },
  "Hello, World!"
);
```

### JSX Rules and Best Practices

**1. Expressions in JSX**

```javascript
const name = "John";
const element = <h1>Hello, {name}!</h1>;

// Can use any JavaScript expression
const element = <h1>Result: {2 + 2}</h1>;
```

**2. JSX Attributes**

```javascript
// Use camelCase for attributes
const element = (
  <div className="container" onClick={handleClick}>
    Content
  </div>
);

// Dynamic attributes
const imgUrl = "image.jpg";
const element = <img src={imgUrl} alt="Description" />;
```

**3. Children in JSX**

```javascript
const element = (
  <div>
    <h1>Title</h1>
    <p>Paragraph text</p>
  </div>
);
```

**4. Conditional Rendering**

```javascript
// Using ternary operator
const element = <div>{isLoggedIn ? <UserGreeting /> : <GuestGreeting />}</div>;

// Using && operator
const element = <div>{showWarning && <Warning />}</div>;
```

**5. Lists and Keys**

```javascript
const numbers = [1, 2, 3, 4, 5];
const listItems = numbers.map((number) => (
  <li key={number.toString()}>{number}</li>
));

const element = <ul>{listItems}</ul>;
```

---

## Components

### Functional Components

Modern React uses functional components with hooks:

```javascript
import React from "react";

function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}

// Arrow function syntax
const Welcome = (props) => {
  return <h1>Hello, {props.name}</h1>;
};

// Destructuring props
const Welcome = ({ name }) => {
  return <h1>Hello, {name}</h1>;
};
```

### Class Components

Class components are older but still supported:

```javascript
import React, { Component } from "react";

class Welcome extends Component {
  render() {
    return <h1>Hello, {this.props.name}</h1>;
  }
}
```

### Component Composition

```javascript
function App() {
  return (
    <div>
      <Header />
      <MainContent />
      <Footer />
    </div>
  );
}

function Header() {
  return (
    <header>
      <h1>My Website</h1>
    </header>
  );
}

function MainContent() {
  return (
    <main>
      <p>Welcome to my website</p>
    </main>
  );
}

function Footer() {
  return (
    <footer>
      <p>© 2025</p>
    </footer>
  );
}
```

---

## Props vs State

### Props (Properties)

Props are **read-only** data passed from parent to child components.

**Characteristics:**

- Immutable (cannot be changed by child)
- Passed from parent to child
- Used for component configuration

**Example:**

```javascript
// Parent Component
function ParentComponent() {
  return <ChildComponent name="John" age={25} />;
}

// Child Component
function ChildComponent(props) {
  return (
    <div>
      <p>Name: {props.name}</p>
      <p>Age: {props.age}</p>
    </div>
  );
}

// With destructuring
function ChildComponent({ name, age }) {
  return (
    <div>
      <p>Name: {name}</p>
      <p>Age: {age}</p>
    </div>
  );
}
```

### State

State is **mutable** data managed within a component.

**Characteristics:**

- Mutable (can be changed)
- Local to the component
- Triggers re-render when updated

**Example:**

```javascript
import React, { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={() => setCount(count - 1)}>Decrement</button>
    </div>
  );
}
```

### Props vs State Comparison

| Feature        | Props                           | State                                  |
| -------------- | ------------------------------- | -------------------------------------- |
| **Mutability** | Immutable                       | Mutable                                |
| **Source**     | Passed from parent              | Managed within component               |
| **Updates**    | Cannot be changed by child      | Can be changed using setState/useState |
| **Re-render**  | Triggers re-render when changed | Triggers re-render when changed        |
| **Purpose**    | Pass data to child components   | Manage component's internal data       |

---

## React Hooks

### useState Hook

Manages state in functional components.

**Basic Usage:**

```javascript
import React, { useState } from "react";

function Example() {
  // Declare state variable
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>Click me</button>
    </div>
  );
}
```

**Multiple State Variables:**

```javascript
function UserProfile() {
  const [name, setName] = useState("");
  const [age, setAge] = useState(0);
  const [email, setEmail] = useState("");

  return (
    <form>
      <input value={name} onChange={(e) => setName(e.target.value)} />
      <input value={age} onChange={(e) => setAge(e.target.value)} />
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
    </form>
  );
}
```

**Object State:**

```javascript
function UserProfile() {
  const [user, setUser] = useState({
    name: "",
    age: 0,
    email: "",
  });

  const updateName = (name) => {
    setUser({ ...user, name }); // Spread operator to preserve other properties
  };

  return (
    <input value={user.name} onChange={(e) => updateName(e.target.value)} />
  );
}
```

### useEffect Hook

Performs side effects in functional components (data fetching, subscriptions, DOM manipulation).

**Basic Usage:**

```javascript
import React, { useState, useEffect } from "react";

function Example() {
  const [count, setCount] = useState(0);

  // Runs after every render
  useEffect(() => {
    document.title = `You clicked ${count} times`;
  });

  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>Click me</button>
    </div>
  );
}
```

**With Dependency Array:**

```javascript
// Runs only once (on mount)
useEffect(() => {
  console.log("Component mounted");
}, []);

// Runs when count changes
useEffect(() => {
  console.log("Count changed:", count);
}, [count]);
```

**Cleanup Function:**

```javascript
useEffect(() => {
  // Subscribe to something
  const timer = setInterval(() => {
    console.log("Timer tick");
  }, 1000);

  // Cleanup function (runs on unmount or before next effect)
  return () => {
    clearInterval(timer);
  };
}, []);
```

**Data Fetching Example:**

```javascript
function UserData() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("https://api.example.com/user")
      .then((response) => response.json())
      .then((data) => {
        setUser(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error:", error);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;
  return <div>{user?.name}</div>;
}
```

**Event Listener Cleanup:**

```javascript
function WindowSize() {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);

    window.addEventListener("resize", handleResize);

    // Cleanup
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return <div>Window width: {width}px</div>;
}
```

### useContext Hook

Provides a way to pass data through the component tree without props drilling.

**Creating Context:**

```javascript
import React, { createContext, useContext, useState } from "react";

// Create context
const ThemeContext = createContext();

// Provider component
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState("light");

  const toggleTheme = () => {
    setTheme(theme === "light" ? "dark" : "light");
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// Consumer component
function ThemedButton() {
  const { theme, toggleTheme } = useContext(ThemeContext);

  return (
    <button
      style={{ background: theme === "light" ? "#fff" : "#333" }}
      onClick={toggleTheme}
    >
      Toggle Theme
    </button>
  );
}

// App
function App() {
  return (
    <ThemeProvider>
      <ThemedButton />
    </ThemeProvider>
  );
}
```

### useReducer Hook

Alternative to useState for complex state logic.

**Basic Usage:**

```javascript
import React, { useReducer } from "react";

// Reducer function
function reducer(state, action) {
  switch (action.type) {
    case "increment":
      return { count: state.count + 1 };
    case "decrement":
      return { count: state.count - 1 };
    case "reset":
      return { count: 0 };
    default:
      throw new Error("Unknown action");
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0 });

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: "increment" })}>+</button>
      <button onClick={() => dispatch({ type: "decrement" })}>-</button>
      <button onClick={() => dispatch({ type: "reset" })}>Reset</button>
    </div>
  );
}
```

**Complex Example:**

```javascript
const initialState = {
  users: [],
  loading: false,
  error: null,
};

function reducer(state, action) {
  switch (action.type) {
    case "FETCH_START":
      return { ...state, loading: true, error: null };
    case "FETCH_SUCCESS":
      return { ...state, loading: false, users: action.payload };
    case "FETCH_ERROR":
      return { ...state, loading: false, error: action.payload };
    default:
      return state;
  }
}

function UserList() {
  const [state, dispatch] = useReducer(reducer, initialState);

  useEffect(() => {
    dispatch({ type: "FETCH_START" });
    fetch("https://api.example.com/users")
      .then((res) => res.json())
      .then((data) => dispatch({ type: "FETCH_SUCCESS", payload: data }))
      .catch((err) => dispatch({ type: "FETCH_ERROR", payload: err.message }));
  }, []);

  if (state.loading) return <div>Loading...</div>;
  if (state.error) return <div>Error: {state.error}</div>;
  return (
    <ul>
      {state.users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### useRef Hook

Creates a mutable reference that persists across renders.

**DOM Reference:**

```javascript
import React, { useRef } from "react";

function TextInput() {
  const inputRef = useRef(null);

  const focusInput = () => {
    inputRef.current.focus();
  };

  return (
    <div>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Focus Input</button>
    </div>
  );
}
```

**Storing Mutable Values:**

```javascript
function Timer() {
  const [count, setCount] = useState(0);
  const intervalRef = useRef();

  useEffect(() => {
    intervalRef.current = setInterval(() => {
      setCount((c) => c + 1);
    }, 1000);

    return () => clearInterval(intervalRef.current);
  }, []);

  return <div>Count: {count}</div>;
}
```

**Previous Value:**

```javascript
function usePrevious(value) {
  const ref = useRef();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

function Counter() {
  const [count, setCount] = useState(0);
  const prevCount = usePrevious(count);

  return (
    <div>
      <p>
        Current: {count}, Previous: {prevCount}
      </p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

---

## Component Lifecycle

### Class Component Lifecycle Methods

**Mounting Phase:**

```javascript
class MyComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = { data: null };
    // Initialize state, bind methods
  }

  componentDidMount() {
    // Runs after component is mounted
    // Perfect for API calls, subscriptions
    fetch("/api/data")
      .then((res) => res.json())
      .then((data) => this.setState({ data }));
  }

  render() {
    return <div>{this.state.data}</div>;
  }
}
```

**Updating Phase:**

```javascript
class MyComponent extends React.Component {
  shouldComponentUpdate(nextProps, nextState) {
    // Return false to prevent re-render
    return nextProps.id !== this.props.id;
  }

  componentDidUpdate(prevProps, prevState) {
    // Runs after update
    if (prevProps.userId !== this.props.userId) {
      this.fetchUserData(this.props.userId);
    }
  }

  render() {
    return <div>{this.props.userId}</div>;
  }
}
```

**Unmounting Phase:**

```javascript
class MyComponent extends React.Component {
  componentDidMount() {
    this.timer = setInterval(() => {
      console.log("Tick");
    }, 1000);
  }

  componentWillUnmount() {
    // Cleanup before component is removed
    clearInterval(this.timer);
  }

  render() {
    return <div>Component with timer</div>;
  }
}
```

### Lifecycle in Functional Components

**Equivalent to componentDidMount:**

```javascript
useEffect(() => {
  console.log("Component mounted");
}, []);
```

**Equivalent to componentDidUpdate:**

```javascript
useEffect(() => {
  console.log("Component updated");
}); // No dependency array
```

**Equivalent to componentWillUnmount:**

```javascript
useEffect(() => {
  return () => {
    console.log("Component will unmount");
  };
}, []);
```

**Complete Example:**

```javascript
function LifecycleDemo({ userId }) {
  const [data, setData] = useState(null);

  // componentDidMount + componentDidUpdate (when userId changes)
  useEffect(() => {
    console.log("Fetching data for user:", userId);

    fetch(`/api/user/${userId}`)
      .then((res) => res.json())
      .then((data) => setData(data));

    // componentWillUnmount
    return () => {
      console.log("Cleanup for user:", userId);
    };
  }, [userId]);

  return <div>{data?.name}</div>;
}
```

---

## Advanced Hooks

### useMemo Hook

Memoizes expensive calculations to avoid unnecessary recalculations.

**Basic Usage:**

```javascript
import React, { useMemo, useState } from "react";

function ExpensiveComponent({ items }) {
  const [filter, setFilter] = useState("");

  // Only recalculates when items or filter changes
  const filteredItems = useMemo(() => {
    console.log("Filtering items...");
    return items.filter((item) =>
      item.name.toLowerCase().includes(filter.toLowerCase())
    );
  }, [items, filter]);

  return (
    <div>
      <input value={filter} onChange={(e) => setFilter(e.target.value)} />
      <ul>
        {filteredItems.map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

**Expensive Calculation:**

```javascript
function ProductList({ products }) {
  const [sortOrder, setSortOrder] = useState("asc");

  const sortedProducts = useMemo(() => {
    console.log("Sorting products...");
    return [...products].sort((a, b) => {
      return sortOrder === "asc" ? a.price - b.price : b.price - a.price;
    });
  }, [products, sortOrder]);

  return (
    <div>
      <button onClick={() => setSortOrder("asc")}>Sort Ascending</button>
      <button onClick={() => setSortOrder("desc")}>Sort Descending</button>
      {sortedProducts.map((product) => (
        <div key={product.id}>
          {product.name} - ${product.price}
        </div>
      ))}
    </div>
  );
}
```

### useCallback Hook

Memoizes function definitions to prevent unnecessary re-renders of child components.

**Basic Usage:**

```javascript
import React, { useCallback, useState } from "react";

function ParentComponent() {
  const [count, setCount] = useState(0);
  const [text, setText] = useState("");

  // Function is recreated only when count changes
  const handleClick = useCallback(() => {
    console.log("Count:", count);
  }, [count]);

  return (
    <div>
      <input value={text} onChange={(e) => setText(e.target.value)} />
      <ChildComponent onClick={handleClick} />
    </div>
  );
}

const ChildComponent = React.memo(({ onClick }) => {
  console.log("Child rendered");
  return <button onClick={onClick}>Click me</button>;
});
```

**With Event Handlers:**

```javascript
function SearchComponent() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const handleSearch = useCallback((searchTerm) => {
    fetch(`/api/search?q=${searchTerm}`)
      .then((res) => res.json())
      .then((data) => setResults(data));
  }, []); // No dependencies, stable reference

  return (
    <div>
      <SearchInput onSearch={handleSearch} />
      <ResultsList results={results} />
    </div>
  );
}
```

### useMemo vs useCallback

```javascript
// useMemo - returns memoized VALUE
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);

// useCallback - returns memoized FUNCTION
const memoizedCallback = useCallback(() => {
  doSomething(a, b);
}, [a, b]);

// useCallback is equivalent to:
const memoizedCallback = useMemo(() => {
  return () => doSomething(a, b);
}, [a, b]);
```

### Custom Hooks

Reusable logic extracted into functions.

**useFetch Hook:**

```javascript
function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err);
        setLoading(false);
      });
  }, [url]);

  return { data, loading, error };
}

// Usage
function UserProfile({ userId }) {
  const { data, loading, error } = useFetch(`/api/users/${userId}`);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  return <div>{data.name}</div>;
}
```

**useLocalStorage Hook:**

```javascript
function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  const setValue = (value) => {
    try {
      const valueToStore =
        value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue];
}

// Usage
function App() {
  const [name, setName] = useLocalStorage("name", "");

  return <input value={name} onChange={(e) => setName(e.target.value)} />;
}
```

**useToggle Hook:**

```javascript
function useToggle(initialValue = false) {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => {
    setValue((v) => !v);
  }, []);

  return [value, toggle];
}

// Usage
function Sidebar() {
  const [isOpen, toggleOpen] = useToggle(false);

  return (
    <div>
      <button onClick={toggleOpen}>Toggle Sidebar</button>
      {isOpen && <div>Sidebar Content</div>}
    </div>
  );
}
```

### useImperativeHandle Hook

Customizes the ref value exposed to parent components.

```javascript
import React, { forwardRef, useImperativeHandle, useRef } from "react";

const CustomInput = forwardRef((props, ref) => {
  const inputRef = useRef();

  useImperativeHandle(ref, () => ({
    focus: () => {
      inputRef.current.focus();
    },
    clear: () => {
      inputRef.current.value = "";
    },
    getValue: () => {
      return inputRef.current.value;
    },
  }));

  return <input ref={inputRef} {...props} />;
});

function ParentComponent() {
  const customInputRef = useRef();

  const handleClick = () => {
    customInputRef.current.focus();
    console.log(customInputRef.current.getValue());
  };

  return (
    <div>
      <CustomInput ref={customInputRef} />
      <button onClick={handleClick}>Focus & Get Value</button>
    </div>
  );
}
```

---

## Performance Optimization

### React.memo

Prevents unnecessary re-renders of functional components.

```javascript
const ExpensiveComponent = React.memo(({ data }) => {
  console.log("ExpensiveComponent rendered");
  return <div>{data}</div>;
});

// With custom comparison function
const ExpensiveComponent = React.memo(
  ({ user }) => {
    return <div>{user.name}</div>;
  },
  (prevProps, nextProps) => {
    // Return true if props are equal (skip re-render)
    return prevProps.user.id === nextProps.user.id;
  }
);
```

### Code Splitting with React.lazy

Lazy load components to reduce initial bundle size.

```javascript
import React, { Suspense, lazy } from "react";

// Lazy load component
const LazyComponent = lazy(() => import("./LazyComponent"));

function App() {
  return (
    <div>
      <Suspense fallback={<div>Loading...</div>}>
        <LazyComponent />
      </Suspense>
    </div>
  );
}
```

**Route-based Code Splitting:**

```javascript
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { lazy, Suspense } from "react";

const Home = lazy(() => import("./pages/Home"));
const About = lazy(() => import("./pages/About"));
const Contact = lazy(() => import("./pages/Contact"));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<div>Loading page...</div>}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
```

### List Virtualization

Render only visible items in large lists.

```javascript
import { FixedSizeList } from "react-window";

function VirtualizedList({ items }) {
  const Row = ({ index, style }) => (
    <div style={style}>{items[index].name}</div>
  );

  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
}
```

### Debouncing and Throttling

**Debounce Hook:**

```javascript
function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
function SearchComponent() {
  const [searchTerm, setSearchTerm] = useState("");
  const debouncedSearchTerm = useDebounce(searchTerm, 500);

  useEffect(() => {
    if (debouncedSearchTerm) {
      // API call
      fetch(`/api/search?q=${debouncedSearchTerm}`)
        .then((res) => res.json())
        .then((data) => console.log(data));
    }
  }, [debouncedSearchTerm]);

  return (
    <input value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} />
  );
}
```

### Avoiding Inline Functions

```javascript
// Bad - creates new function on every render
function BadComponent() {
  return <button onClick={() => console.log("clicked")}>Click</button>;
}

// Good - stable function reference
function GoodComponent() {
  const handleClick = useCallback(() => {
    console.log("clicked");
  }, []);

  return <button onClick={handleClick}>Click</button>;
}
```

---

## React Design Patterns

### Container/Presentational Pattern

Separates logic from presentation.

```javascript
// Presentational Component (UI only)
function UserList({ users, onUserClick }) {
  return (
    <ul>
      {users.map((user) => (
        <li key={user.id} onClick={() => onUserClick(user)}>
          {user.name}
        </li>
      ))}
    </ul>
  );
}

// Container Component (logic)
function UserListContainer() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/users")
      .then((res) => res.json())
      .then((data) => {
        setUsers(data);
        setLoading(false);
      });
  }, []);

  const handleUserClick = (user) => {
    console.log("User clicked:", user);
  };

  if (loading) return <div>Loading...</div>;
  return <UserList users={users} onUserClick={handleUserClick} />;
}
```

### Higher-Order Components (HOC)

Functions that take a component and return a new enhanced component.

```javascript
// HOC for authentication
function withAuth(Component) {
  return function AuthenticatedComponent(props) {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
      // Check authentication
      const token = localStorage.getItem("token");
      setIsAuthenticated(!!token);
    }, []);

    if (!isAuthenticated) {
      return <div>Please log in</div>;
    }

    return <Component {...props} />;
  };
}

// Usage
function Dashboard() {
  return <div>Dashboard Content</div>;
}

const AuthenticatedDashboard = withAuth(Dashboard);
```

**HOC for Loading State:**

```javascript
function withLoading(Component) {
  return function LoadingComponent({ isLoading, ...props }) {
    if (isLoading) {
      return <div>Loading...</div>;
    }
    return <Component {...props} />;
  };
}

// Usage
const UserListWithLoading = withLoading(UserList);

function App() {
  const [loading, setLoading] = useState(true);
  const [users, setUsers] = useState([]);

  return <UserListWithLoading isLoading={loading} users={users} />;
}
```

### Compound Components Pattern

Components that work together to form a complete UI.

```javascript
import React, { createContext, useContext, useState } from "react";

const TabsContext = createContext();

function Tabs({ children }) {
  const [activeTab, setActiveTab] = useState(0);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

function TabList({ children }) {
  return <div className="tab-list">{children}</div>;
}

function Tab({ index, children }) {
  const { activeTab, setActiveTab } = useContext(TabsContext);
  const isActive = activeTab === index;

  return (
    <button
      className={isActive ? "active" : ""}
      onClick={() => setActiveTab(index)}
    >
      {children}
    </button>
  );
}

function TabPanels({ children }) {
  const { activeTab } = useContext(TabsContext);
  return <div>{children[activeTab]}</div>;
}

function TabPanel({ children }) {
  return <div className="tab-panel">{children}</div>;
}

// Attach sub-components
Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panels = TabPanels;
Tabs.Panel = TabPanel;

// Usage
function App() {
  return (
    <Tabs>
      <Tabs.List>
        <Tabs.Tab index={0}>Tab 1</Tabs.Tab>
        <Tabs.Tab index={1}>Tab 2</Tabs.Tab>
        <Tabs.Tab index={2}>Tab 3</Tabs.Tab>
      </Tabs.List>
      <Tabs.Panels>
        <Tabs.Panel>Content 1</Tabs.Panel>
        <Tabs.Panel>Content 2</Tabs.Panel>
        <Tabs.Panel>Content 3</Tabs.Panel>
      </Tabs.Panels>
    </Tabs>
  );
}
```

### Render Props Pattern

Component shares code using a prop whose value is a function.

```javascript
function Mouse({ render }) {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return render(position);
}

// Usage
function App() {
  return (
    <Mouse
      render={({ x, y }) => (
        <div>
          Mouse position: {x}, {y}
        </div>
      )}
    />
  );
}
```

---

## State Management

### Local State Management

Using useState and useReducer for component-level state.

```javascript
function TodoList() {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState("");

  const addTodo = () => {
    setTodos([...todos, { id: Date.now(), text: input, completed: false }]);
    setInput("");
  };

  const toggleTodo = (id) => {
    setTodos(
      todos.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    );
  };

  return (
    <div>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={addTodo}>Add</button>
      <ul>
        {todos.map((todo) => (
          <li
            key={todo.id}
            onClick={() => toggleTodo(todo.id)}
            style={{ textDecoration: todo.completed ? "line-through" : "none" }}
          >
            {todo.text}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Context API for Global State

Share state across multiple components without prop drilling.

```javascript
import React, { createContext, useContext, useReducer } from "react";

// Create context
const AppContext = createContext();

// Reducer
function appReducer(state, action) {
  switch (action.type) {
    case "SET_USER":
      return { ...state, user: action.payload };
    case "SET_THEME":
      return { ...state, theme: action.payload };
    case "LOGOUT":
      return { ...state, user: null };
    default:
      return state;
  }
}

// Provider
function AppProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, {
    user: null,
    theme: "light",
  });

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}

// Custom hook
function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useApp must be used within AppProvider");
  }
  return context;
}

// Usage in components
function UserProfile() {
  const { state, dispatch } = useApp();

  const handleLogout = () => {
    dispatch({ type: "LOGOUT" });
  };

  return (
    <div>
      {state.user ? (
        <>
          <p>Welcome, {state.user.name}</p>
          <button onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <p>Please log in</p>
      )}
    </div>
  );
}
```

### Redux Toolkit

Modern Redux with less boilerplate.

**Setup:**

```javascript
// store.js
import { configureStore } from "@reduxjs/toolkit";
import counterReducer from "./features/counter/counterSlice";

export const store = configureStore({
  reducer: {
    counter: counterReducer,
  },
});
```

**Create Slice:**

```javascript
// counterSlice.js
import { createSlice } from "@reduxjs/toolkit";

const counterSlice = createSlice({
  name: "counter",
  initialState: {
    value: 0,
  },
  reducers: {
    increment: (state) => {
      state.value += 1; // Immer allows "mutation"
    },
    decrement: (state) => {
      state.value -= 1;
    },
    incrementByAmount: (state, action) => {
      state.value += action.payload;
    },
  },
});

export const { increment, decrement, incrementByAmount } = counterSlice.actions;
export default counterSlice.reducer;
```

**Use in Component:**

```javascript
import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { increment, decrement, incrementByAmount } from "./counterSlice";

function Counter() {
  const count = useSelector((state) => state.counter.value);
  const dispatch = useDispatch();

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => dispatch(increment())}>+</button>
      <button onClick={() => dispatch(decrement())}>-</button>
      <button onClick={() => dispatch(incrementByAmount(5))}>+5</button>
    </div>
  );
}
```

**Async Actions with createAsyncThunk:**

```javascript
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

// Async thunk
export const fetchUsers = createAsyncThunk("users/fetchUsers", async () => {
  const response = await fetch("/api/users");
  return response.json();
});

const usersSlice = createSlice({
  name: "users",
  initialState: {
    entities: [],
    loading: "idle",
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUsers.pending, (state) => {
        state.loading = "pending";
      })
      .addCase(fetchUsers.fulfilled, (state, action) => {
        state.loading = "idle";
        state.entities = action.payload;
      })
      .addCase(fetchUsers.rejected, (state, action) => {
        state.loading = "idle";
        state.error = action.error.message;
      });
  },
});

export default usersSlice.reducer;

// Usage
function UserList() {
  const dispatch = useDispatch();
  const { entities, loading, error } = useSelector((state) => state.users);

  useEffect(() => {
    dispatch(fetchUsers());
  }, [dispatch]);

  if (loading === "pending") return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  return (
    <ul>
      {entities.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

---

## Error Handling

### Error Boundaries

Catch JavaScript errors in component tree and display fallback UI.

**Class-based Error Boundary:**

```javascript
import React from "react";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Error caught:", error, errorInfo);
    this.setState({ error, errorInfo });
    // Log to error reporting service
  }

  render() {
    if (this.state.hasError) {
      return (
        <div>
          <h1>Something went wrong</h1>
          <details>
            <summary>Error details</summary>
            <pre>{this.state.error?.toString()}</pre>
            <pre>{this.state.errorInfo?.componentStack}</pre>
          </details>
          <button onClick={() => this.setState({ hasError: false })}>
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Usage
function App() {
  return (
    <ErrorBoundary>
      <MyComponent />
    </ErrorBoundary>
  );
}
```

**Using react-error-boundary Library:**

```javascript
import { ErrorBoundary } from "react-error-boundary";

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert">
      <p>Something went wrong:</p>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      onReset={() => {
        // Reset application state
      }}
      onError={(error, errorInfo) => {
        // Log to error service
        console.error("Error:", error, errorInfo);
      }}
    >
      <MyComponent />
    </ErrorBoundary>
  );
}
```

**Multiple Error Boundaries:**

```javascript
function App() {
  return (
    <div>
      <ErrorBoundary>
        <Header />
      </ErrorBoundary>

      <ErrorBoundary>
        <MainContent />
      </ErrorBoundary>

      <ErrorBoundary>
        <Footer />
      </ErrorBoundary>
    </div>
  );
}
```

---

## Testing

### Testing with Jest and React Testing Library

**Setup:**

```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

**Basic Component Test:**

```javascript
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import "@testing-library/jest-dom";
import Counter from "./Counter";

describe("Counter Component", () => {
  test("renders initial count", () => {
    render(<Counter />);
    const countElement = screen.getByText(/count: 0/i);
    expect(countElement).toBeInTheDocument();
  });

  test("increments count when button clicked", async () => {
    render(<Counter />);
    const button = screen.getByRole("button", { name: /increment/i });

    await userEvent.click(button);

    expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
  });

  test("decrements count when button clicked", async () => {
    render(<Counter />);
    const button = screen.getByRole("button", { name: /decrement/i });

    await userEvent.click(button);

    expect(screen.getByText(/count: -1/i)).toBeInTheDocument();
  });
});
```

**Testing Async Components:**

```javascript
import { render, screen, waitFor } from "@testing-library/react";
import UserProfile from "./UserProfile";

test("loads and displays user data", async () => {
  // Mock fetch
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () =>
        Promise.resolve({ name: "John Doe", email: "john@example.com" }),
    })
  );

  render(<UserProfile userId="123" />);

  // Initially shows loading
  expect(screen.getByText(/loading/i)).toBeInTheDocument();

  // Wait for data to load
  await waitFor(() => {
    expect(screen.getByText(/john doe/i)).toBeInTheDocument();
  });

  expect(global.fetch).toHaveBeenCalledWith("/api/users/123");
});
```

**Testing User Interactions:**

```javascript
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import Form from "./Form";

test("submits form with user input", async () => {
  const handleSubmit = jest.fn();
  render(<Form onSubmit={handleSubmit} />);

  const nameInput = screen.getByLabelText(/name/i);
  const emailInput = screen.getByLabelText(/email/i);
  const submitButton = screen.getByRole("button", { name: /submit/i });

  await userEvent.type(nameInput, "John Doe");
  await userEvent.type(emailInput, "john@example.com");
  await userEvent.click(submitButton);

  expect(handleSubmit).toHaveBeenCalledWith({
    name: "John Doe",
    email: "john@example.com",
  });
});
```

**Testing Hooks:**

```javascript
import { renderHook, act } from "@testing-library/react";
import useCounter from "./useCounter";

test("increments counter", () => {
  const { result } = renderHook(() => useCounter());

  expect(result.current.count).toBe(0);

  act(() => {
    result.current.increment();
  });

  expect(result.current.count).toBe(1);
});
```

---

## Advanced Concepts

### React Server Components (RSC)

Components that run on the server.

**Server Component:**

```javascript
// ServerComponent.js (runs on server)
async function ServerComponent() {
  // Direct database access
  const data = await db.query("SELECT * FROM users");

  return (
    <div>
      <h1>Users</h1>
      <ul>
        {data.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default ServerComponent;
```

**Client Component:**

```javascript
"use client"; // Marks as client component

import { useState } from "react";

function ClientComponent() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}

export default ClientComponent;
```

### React Suspense

Handle async operations declaratively.

**Data Fetching with Suspense:**

```javascript
import { Suspense } from "react";

const resource = fetchData(); // Returns a Suspense-compatible resource

function DataComponent() {
  const data = resource.read(); // Suspends if not ready
  return <div>{data.name}</div>;
}

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <DataComponent />
    </Suspense>
  );
}
```

**Nested Suspense:**

```javascript
function App() {
  return (
    <Suspense fallback={<div>Loading app...</div>}>
      <Header />
      <Suspense fallback={<div>Loading content...</div>}>
        <Content />
      </Suspense>
      <Suspense fallback={<div>Loading sidebar...</div>}>
        <Sidebar />
      </Suspense>
    </Suspense>
  );
}
```

### React Portals

Render children into a DOM node outside parent hierarchy.

```javascript
import { createPortal } from "react-dom";

function Modal({ isOpen, children }) {
  if (!isOpen) return null;

  return createPortal(
    <div className="modal-overlay">
      <div className="modal-content">{children}</div>
    </div>,
    document.getElementById("modal-root") // Render outside root
  );
}

// Usage
function App() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div>
      <button onClick={() => setIsOpen(true)}>Open Modal</button>
      <Modal isOpen={isOpen}>
        <h2>Modal Title</h2>
        <button onClick={() => setIsOpen(false)}>Close</button>
      </Modal>
    </div>
  );
}
```

### React.forwardRef

Forward refs to child components.

```javascript
import React, { forwardRef, useRef } from "react";

const FancyInput = forwardRef((props, ref) => {
  return (
    <div>
      <label>{props.label}</label>
      <input ref={ref} {...props} />
    </div>
  );
});

function App() {
  const inputRef = useRef();

  const handleClick = () => {
    inputRef.current.focus();
  };

  return (
    <div>
      <FancyInput ref={inputRef} label="Name:" />
      <button onClick={handleClick}>Focus Input</button>
    </div>
  );
}
```

### Reconciliation

React's algorithm for differing trees.

**Keys in Lists:**

```javascript
// Bad - using index as key
{
  items.map((item, index) => <li key={index}>{item.name}</li>);
}

// Good - using stable unique identifier
{
  items.map((item) => <li key={item.id}>{item.name}</li>);
}
```

**React.StrictMode:**

```javascript
import React from "react";

function App() {
  return (
    <React.StrictMode>
      <MyApp />
    </React.StrictMode>
  );
}

// StrictMode helps identify:
// - Components with unsafe lifecycles
// - Legacy string ref API usage
// - Deprecated findDOMNode usage
// - Unexpected side effects
// - Legacy context API
```

---

## Common Interview Questions

### 1. What is the Virtual DOM?

The Virtual DOM is a lightweight copy of the actual DOM. React uses it to:

- Calculate the minimal changes needed
- Batch updates for better performance
- Update only changed parts of the real DOM

### 2. Explain React's reconciliation algorithm

React compares the new Virtual DOM with the previous one and:

- Elements of different types produce different trees
- Uses keys to identify which items changed
- Updates only the differences in the real DOM

### 3. What is prop drilling and how to avoid it?

Prop drilling is passing props through multiple levels of components. Avoid with:

- Context API for global state
- State management libraries (Redux, Zustand)
- Component composition

### 4. Controlled vs Uncontrolled Components

**Controlled:**

```javascript
function ControlledInput() {
  const [value, setValue] = useState("");
  return <input value={value} onChange={(e) => setValue(e.target.value)} />;
}
```

**Uncontrolled:**

```javascript
function UncontrolledInput() {
  const inputRef = useRef();
  const handleSubmit = () => console.log(inputRef.current.value);
  return <input ref={inputRef} />;
}
```

### 5. What are Pure Components?

Components that render the same output for same props and state.

```javascript
const PureComponent = React.memo(({ name }) => {
  console.log("Rendered");
  return <div>{name}</div>;
});
```

### 6. Differences between useEffect and useLayoutEffect

- `useEffect`: Runs after paint (asynchronous)
- `useLayoutEffect`: Runs before paint (synchronous)

Use `useLayoutEffect` for DOM measurements that affect rendering.

### 7. How to optimize React app performance?

- Use React.memo for expensive components
- useMemo and useCallback for expensive calculations
- Code splitting with React.lazy
- List virtualization for long lists
- Avoid inline functions and objects
- Use production build

### 8. What is lifting state up?

Moving state to the closest common ancestor of components that need it.

```javascript
function Parent() {
  const [count, setCount] = useState(0);
  return (
    <>
      <Child1 count={count} />
      <Child2 setCount={setCount} />
    </>
  );
}
```

---

## Best Practices

1. **Keep Components Small and Focused**

   - Single responsibility principle
   - Easy to test and maintain

2. **Use Functional Components with Hooks**

   - Modern React standard
   - More concise and readable

3. **Proper Key Usage**

   - Use stable unique identifiers
   - Avoid using array index

4. **Avoid Direct State Mutation**

   ```javascript
   // Bad
   state.items.push(newItem);

   // Good
   setState([...state.items, newItem]);
   ```

5. **Use PropTypes or TypeScript**

   - Type safety
   - Better IDE support
   - Self-documenting code

6. **Handle Loading and Error States**

   - Provide feedback to users
   - Graceful error handling

7. **Code Organization**

   - Separate concerns (logic vs presentation)
   - Consistent file structure
   - Reusable custom hooks

8. **Performance Optimization**

   - Profile before optimizing
   - Use React DevTools
   - Implement code splitting

9. **Testing**

   - Write tests for critical functionality
   - Test user interactions
   - Mock external dependencies

10. **Accessibility**
    - Use semantic HTML
    - Add ARIA attributes
    - Keyboard navigation support

---

## Resources for Further Learning

- **Official Documentation**: https://react.dev
- **React Hooks**: https://react.dev/reference/react
- **Redux Toolkit**: https://redux-toolkit.js.org
- **React Testing Library**: https://testing-library.com/react
- **React Patterns**: https://reactpatterns.com

---

**Good luck with your React interview! 🚀**
