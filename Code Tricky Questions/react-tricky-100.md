# 100 React Tricky Code Questions with Output & Explanations

## Table of Contents

- [Table of Contents](#table-of-contents)
- [useState Hook Behavior (Questions 1-12)](#usestate-hook-behavior-questions-1-12)
  - [Question 1: Stale State in Event Handler](#question-1-stale-state-in-event-handler)
  - [Question 2: Functional Update Form](#question-2-functional-update-form)
  - [Question 3: setState is Asynchronous](#question-3-setstate-is-asynchronous)
  - [Question 4: Object State Update](#question-4-object-state-update)
  - [Question 5: Initial State Function](#question-5-initial-state-function)
  - [Question 6: State Update with Same Value](#question-6-state-update-with-same-value)
  - [Question 7: Multiple State Variables](#question-7-multiple-state-variables)
  - [Question 8: Array State Mutation](#question-8-array-state-mutation)
  - [Question 9: State in Loop](#question-9-state-in-loop)
  - [Question 10: Boolean State Toggle](#question-10-boolean-state-toggle)
  - [Question 11: State with Function as Value](#question-11-state-with-function-as-value)
  - [Question 12: Derived State](#question-12-derived-state)
- [useEffect Hook & Closures (Questions 13-24)](#useeffect-hook-closures-questions-13-24)
  - [Question 13: Missing Dependency Array](#question-13-missing-dependency-array)
  - [Question 14: Empty Dependency Array](#question-14-empty-dependency-array)
  - [Question 15: Stale Closure in setInterval](#question-15-stale-closure-in-setinterval)
  - [Question 16: Cleanup Function Timing](#question-16-cleanup-function-timing)
  - [Question 17: Multiple Effects Execution Order](#question-17-multiple-effects-execution-order)
  - [Question 18: useEffect with Object Dependency](#question-18-useeffect-with-object-dependency)
  - [Question 19: Async Function in useEffect](#question-19-async-function-in-useeffect)
  - [Question 20: Correct Async Pattern](#question-20-correct-async-pattern)
  - [Question 21: useEffect with Function Dependency](#question-21-useeffect-with-function-dependency)
  - [Question 22: setState Inside useEffect Without Dependency](#question-22-setstate-inside-useeffect-without-dependency)
  - [Question 23: Infinite Loop with useEffect](#question-23-infinite-loop-with-useeffect)
  - [Question 24: useEffect Dependency with Primitive vs Reference](#question-24-useeffect-dependency-with-primitive-vs-reference)
- [React Reconciliation & Keys (Questions 25-32)](#react-reconciliation-keys-questions-25-32)
  - [Question 25: Missing Key in List](#question-25-missing-key-in-list)
  - [Question 26: Index as Key Anti-pattern](#question-26-index-as-key-anti-pattern)
  - [Question 27: Key on Conditional Render](#question-27-key-on-conditional-render)
  - [Question 28: Same Key Forces Reuse](#question-28-same-key-forces-reuse)
  - [Question 29: Key Reset Pattern](#question-29-key-reset-pattern)
  - [Question 30: Fragment with Key](#question-30-fragment-with-key)
  - [Question 31: Dynamic Children Reconciliation](#question-31-dynamic-children-reconciliation)
  - [Question 32: No Key Needed for Static Lists](#question-32-no-key-needed-for-static-lists)
- [Component Re-rendering (Questions 33-40)](#component-re-rendering-questions-33-40)
  - [Question 33: Parent Re-render Causes Child Re-render](#question-33-parent-re-render-causes-child-re-render)
  - [Question 34: React.memo Basic Usage](#question-34-reactmemo-basic-usage)
  - [Question 35: React.memo with Object Prop](#question-35-reactmemo-with-object-prop)
  - [Question 36: React.memo with Function Prop](#question-36-reactmemo-with-function-prop)
  - [Question 37: React.memo Custom Comparison](#question-37-reactmemo-custom-comparison)
  - [Question 38: Inline Object Prop](#question-38-inline-object-prop)
  - [Question 39: Same Element Reference Optimization](#question-39-same-element-reference-optimization)
  - [Question 40: Children Prop Optimization](#question-40-children-prop-optimization)
- [Refs & useRef (Questions 41-48)](#refs-useref-questions-41-48)
  - [Question 41: useRef Doesn't Trigger Re-render](#question-41-useref-doesnt-trigger-re-render)
  - [Question 42: Ref vs State for DOM Element](#question-42-ref-vs-state-for-dom-element)
  - [Question 43: Ref in useEffect](#question-43-ref-in-useeffect)
  - [Question 44: Stale Ref in Closure](#question-44-stale-ref-in-closure)
  - [Question 45: Ref Callback Pattern](#question-45-ref-callback-pattern)
  - [Question 46: createRef vs useRef](#question-46-createref-vs-useref)
  - [Question 47: Ref to Store Previous Value](#question-47-ref-to-store-previous-value)
  - [Question 48: forwardRef Basics](#question-48-forwardref-basics)
- [React Memo & useMemo (Questions 49-56)](#react-memo-usememo-questions-49-56)
  - [Question 49: useMemo Basic Usage](#question-49-usememo-basic-usage)
  - [Question 50: useMemo with Object](#question-50-usememo-with-object)
  - [Question 51: useMemo with Empty Dependencies](#question-51-usememo-with-empty-dependencies)
  - [Question 52: useMemo vs useEffect](#question-52-usememo-vs-useeffect)
  - [Question 53: Premature Optimization with useMemo](#question-53-premature-optimization-with-usememo)
  - [Question 54: useMemo with Array Dependency](#question-54-usememo-with-array-dependency)
  - [Question 55: useMemo for Referential Equality](#question-55-usememo-for-referential-equality)
  - [Question 56: useMemo Doesn't Guarantee Caching](#question-56-usememo-doesnt-guarantee-caching)
- [useCallback Hook (Questions 57-62)](#usecallback-hook-questions-57-62)
  - [Question 57: useCallback Basic Usage](#question-57-usecallback-basic-usage)
  - [Question 58: useCallback with Dependencies](#question-58-usecallback-with-dependencies)
  - [Question 59: useCallback vs useMemo for Functions](#question-59-usecallback-vs-usememo-for-functions)
  - [Question 60: useCallback with Inline Function](#question-60-usecallback-with-inline-function)
  - [Question 61: useCallback in useEffect](#question-61-usecallback-in-useeffect)
  - [Question 62: useCallback Overhead](#question-62-usecallback-overhead)
- [Context API (Questions 63-68)](#context-api-questions-63-68)
  - [Question 63: Context Re-renders All Consumers](#question-63-context-re-renders-all-consumers)
  - [Question 64: Context with useMemo](#question-64-context-with-usememo)
  - [Question 65: Context Split Pattern](#question-65-context-split-pattern)
  - [Question 66: Context Default Value](#question-66-context-default-value)
  - [Question 67: Multiple Context Providers](#question-67-multiple-context-providers)
  - [Question 68: Context Update Performance](#question-68-context-update-performance)
- [Synthetic Events (Questions 69-74)](#synthetic-events-questions-69-74)
  - [Question 69: Event Pooling (React 16)](#question-69-event-pooling-react-16)
  - [Question 70: Accessing Native Event](#question-70-accessing-native-event)
  - [Question 71: Event Handler in setState](#question-71-event-handler-in-setstate)
  - [Question 72: stopPropagation in React](#question-72-stoppropagation-in-react)
  - [Question 73: preventDefault](#question-73-preventdefault)
  - [Question 74: Event Handler Return False](#question-74-event-handler-return-false)
- [React Strict Mode (Questions 75-78)](#react-strict-mode-questions-75-78)
  - [Question 75: Double Render in Strict Mode](#question-75-double-render-in-strict-mode)
  - [Question 76: useEffect Runs Twice in Strict Mode](#question-76-useeffect-runs-twice-in-strict-mode)
  - [Question 77: Detecting Unsafe Lifecycles](#question-77-detecting-unsafe-lifecycles)
  - [Question 78: Strict Mode Doesn't Affect Production](#question-78-strict-mode-doesnt-affect-production)
- [State Batching (Questions 79-82)](#state-batching-questions-79-82)
  - [Question 79: Automatic Batching in Event Handlers](#question-79-automatic-batching-in-event-handlers)
  - [Question 80: No Batching in Async (React 17)](#question-80-no-batching-in-async-react-17)
  - [Question 81: Opt Out of Batching (React 18)](#question-81-opt-out-of-batching-react-18)
  - [Question 82: Reading State After Multiple Updates](#question-82-reading-state-after-multiple-updates)
- [useReducer Hook (Questions 83-86)](#usereducer-hook-questions-83-86)
  - [Question 83: useReducer Basics](#question-83-usereducer-basics)
  - [Question 84: Dispatch Identity is Stable](#question-84-dispatch-identity-is-stable)
  - [Question 85: Lazy Initialization](#question-85-lazy-initialization)
  - [Question 86: Dispatch with Closure](#question-86-dispatch-with-closure)
- [Props & Destructuring (Questions 87-90)](#props-destructuring-questions-87-90)
  - [Question 87: Destructuring Props with Default Values](#question-87-destructuring-props-with-default-values)
  - [Question 88: Props Object Passed as Prop](#question-88-props-object-passed-as-prop)
  - [Question 89: Spread Operator for Props](#question-89-spread-operator-for-props)
  - [Question 90: PropTypes with Destructuring](#question-90-proptypes-with-destructuring)
- [Portals & Event Bubbling (Questions 91-93)](#portals-event-bubbling-questions-91-93)
  - [Question 91: Portal Event Bubbling](#question-91-portal-event-bubbling)
  - [Question 92: Stopping Portal Event Bubbling](#question-92-stopping-portal-event-bubbling)
  - [Question 93: Portal with Context](#question-93-portal-with-context)
- [Advanced Hooks (Questions 94-100)](#advanced-hooks-questions-94-100)
  - [Question 94: useLayoutEffect vs useEffect](#question-94-uselayouteffect-vs-useeffect)
  - [Question 95: useImperativeHandle](#question-95-useimperativehandle)
  - [Question 96: React.lazy and Suspense](#question-96-reactlazy-and-suspense)
  - [Question 97: useDeferredValue](#question-97-usedeferredvalue)
  - [Question 98: useTransition](#question-98-usetransition)
  - [Question 99: Error Boundaries](#question-99-error-boundaries)
  - [Question 100: dangerouslySetInnerHTML](#question-100-dangerouslysetinnerhtml)
- [Summary](#summary)

## useState Hook Behavior (Questions 1-12)

### Question 1: Stale State in Event Handler
```javascript
function Counter() {
  const [count, setCount] = useState(0);
  
  const handleClick = () => {
    setCount(count + 1);
    setCount(count + 1);
    setCount(count + 1);
  };
  
  return <button onClick={handleClick}>{count}</button>;
}
// Output: On click, count becomes 1 (not 3)
```
**Explanation:** All three `setCount` calls use the same `count` value (0) from the current render. React batches the updates, but since they all reference the stale value, the final state is 1. To fix this, use the functional form: `setCount(prev => prev + 1)`.

---

### Question 2: Functional Update Form
```javascript
function Counter() {
  const [count, setCount] = useState(0);
  
  const handleClick = () => {
    setCount(prev => prev + 1);
    setCount(prev => prev + 1);
    setCount(prev => prev + 1);
  };
  
  return <button onClick={handleClick}>{count}</button>;
}
// Output: On click, count becomes 3
```
**Explanation:** Using the functional form `prev => prev + 1` ensures each update receives the latest state value. React processes these sequentially, so: 0 → 1 → 2 → 3.

---

### Question 3: setState is Asynchronous
```javascript
function App() {
  const [count, setCount] = useState(0);
  
  const handleClick = () => {
    setCount(count + 1);
    console.log(count); // What will this log?
  };
  
  return <button onClick={handleClick}>Click</button>;
}
// Output: Console logs 0 (the old value)
```
**Explanation:** `setState` is asynchronous. The `console.log` executes immediately after calling `setCount`, but the state hasn't updated yet. The component will re-render with the new value, but `console.log` captures the old value from the current closure.

---

### Question 4: Object State Update
```javascript
function App() {
  const [user, setUser] = useState({ name: 'John', age: 25 });
  
  const updateAge = () => {
    user.age = 26;
    setUser(user);
  };
  
  return <div>{user.age}</div>;
}
// Output: Component doesn't re-render, age stays 25
```
**Explanation:** React uses shallow comparison (Object.is) to detect state changes. Since we mutated the object directly, the reference remains the same, so React doesn't detect a change. Correct way: `setUser({ ...user, age: 26 })`.

---

### Question 5: Initial State Function
```javascript
function ExpensiveComponent() {
  const [value, setValue] = useState(expensiveCalculation());
  return <div>{value}</div>;
}
// Output: expensiveCalculation() runs on every render
```
**Explanation:** Passing a function call as initial state executes it on every render. Use lazy initialization instead: `useState(() => expensiveCalculation())`. This ensures the expensive function runs only once during initial render.

---

### Question 6: State Update with Same Value
```javascript
function App() {
  const [count, setCount] = useState(0);
  console.log('render');
  
  return <button onClick={() => setCount(0)}>Click</button>;
}
// Output: After first click, "render" doesn't log again
```
**Explanation:** React uses `Object.is` comparison to check if state has changed. If you set the same value, React bails out of the re-render. This optimization prevents unnecessary re-renders.

---

### Question 7: Multiple State Variables
```javascript
function App() {
  const [count1, setCount1] = useState(0);
  const [count2, setCount2] = useState(0);
  
  const handleClick = () => {
    setCount1(count1 + 1);
    setCount2(count2 + 1);
  };
  
  console.log('render');
  return <button onClick={handleClick}>Click</button>;
}
// Output: "render" logs once per click (not twice)
```
**Explanation:** React batches multiple state updates in event handlers into a single re-render for performance. Both states update, but only one render cycle occurs.

---

### Question 8: Array State Mutation
```javascript
function TodoList() {
  const [todos, setTodos] = useState(['Task 1']);
  
  const addTodo = () => {
    todos.push('Task 2');
    setTodos(todos);
  };
  
  return <div>{todos.length}</div>;
}
// Output: Component doesn't re-render
```
**Explanation:** Array mutation doesn't create a new reference. React doesn't detect the change. Use immutable updates: `setTodos([...todos, 'Task 2'])` or `setTodos(prev => [...prev, 'Task 2'])`.

---

### Question 9: State in Loop
```javascript
function App() {
  const [count, setCount] = useState(0);
  
  const handleClick = () => {
    for (let i = 0; i < 3; i++) {
      setCount(count + 1);
    }
  };
  
  return <button onClick={handleClick}>{count}</button>;
}
// Output: count becomes 1 (not 3)
```
**Explanation:** Each iteration captures the same `count` value due to closure. All three `setCount` calls use `count + 1` with the same initial value. Solution: use functional form `setCount(prev => prev + 1)`.

---

### Question 10: Boolean State Toggle
```javascript
function App() {
  const [isOpen, setIsOpen] = useState(false);
  
  const toggle = () => {
    setIsOpen(!isOpen);
    setIsOpen(!isOpen);
  };
  
  return <div>{isOpen.toString()}</div>;
}
// Output: isOpen remains false
```
**Explanation:** Both `setIsOpen` calls read the same `isOpen` value (false), so `!isOpen` is `true` for both. React batches them and the final value is `true`, but then the second call sets it back to `true` (since both evaluated to `!false`). Actually, since batching happens, the final value becomes `true`. Better: use `setIsOpen(prev => !prev)`.

---

### Question 11: State with Function as Value
```javascript
function App() {
  const [fn, setFn] = useState(() => () => console.log('hello'));
  
  return <button onClick={fn}>Click</button>;
}
// Output: Works correctly, logs "hello" on click
```
**Explanation:** When storing a function in state, you must use lazy initialization `() => yourFunction`. If you do `useState(yourFunction)`, React thinks it's lazy initialization and calls it immediately. The outer arrow function prevents this.

---

### Question 12: Derived State
```javascript
function App({ items }) {
  const [list, setList] = useState(items);
  
  return <div>{list.length}</div>;
}
// Output: list doesn't update when items prop changes
```
**Explanation:** `useState` only uses the initial value on the first render. Changes to `items` prop don't affect `list` state. This is a common anti-pattern. Either use `items` directly, or sync with `useEffect`, or use `key` to reset component.

---

## useEffect Hook & Closures (Questions 13-24)

### Question 13: Missing Dependency Array
```javascript
function App() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    console.log(count);
  });
  
  return <button onClick={() => setCount(count + 1)}>Click</button>;
}
// Output: Logs count on every render
```
**Explanation:** Without a dependency array, `useEffect` runs after every render. This can cause performance issues. Use `[]` for mount only, or specify dependencies to control when it runs.

---

### Question 14: Empty Dependency Array
```javascript
function App() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    console.log(count);
  }, []);
  
  return <button onClick={() => setCount(count + 1)}>Click</button>;
}
// Output: Always logs 0
```
**Explanation:** Empty dependency array means the effect runs only once on mount. It captures `count` from the first render (0) and never updates. This creates a stale closure.

---

### Question 15: Stale Closure in setInterval
```javascript
function Timer() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    const id = setInterval(() => {
      setCount(count + 1);
    }, 1000);
    return () => clearInterval(id);
  }, []);
  
  return <div>{count}</div>;
}
// Output: count stays at 1
```
**Explanation:** The interval captures `count` as 0 from initial render. Every tick sets count to `0 + 1 = 1`. Solution: use functional form `setCount(prev => prev + 1)` or include `count` in dependencies (but then you need to clear and recreate interval).

---

### Question 16: Cleanup Function Timing
```javascript
function App() {
  useEffect(() => {
    console.log('Effect');
    return () => console.log('Cleanup');
  });
  
  return <div>Component</div>;
}
// Output: "Effect" on mount, then "Cleanup" → "Effect" on each update
```
**Explanation:** Cleanup runs before the next effect execution and on unmount. The order is: mount → effect, update → cleanup → effect, unmount → cleanup.

---

### Question 17: Multiple Effects Execution Order
```javascript
function App() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    console.log('Effect 1');
  });
  
  useEffect(() => {
    console.log('Effect 2');
  });
  
  return <div>{count}</div>;
}
// Output: "Effect 1" then "Effect 2" on each render
```
**Explanation:** Effects run in the order they're defined in the component, after the render is committed to the screen.

---

### Question 18: useEffect with Object Dependency
```javascript
function App() {
  const [count, setCount] = useState(0);
  const obj = { value: count };
  
  useEffect(() => {
    console.log('Effect');
  }, [obj]);
  
  return <button onClick={() => setCount(count + 1)}>Click</button>;
}
// Output: "Effect" logs on every click
```
**Explanation:** A new object `{ value: count }` is created on every render. React compares dependencies using `Object.is`, and since the object reference changes each time, the effect runs on every render. Solution: use `useMemo` or destructure: `[obj.value]`.

---

### Question 19: Async Function in useEffect
```javascript
function App() {
  useEffect(async () => {
    const data = await fetchData();
    console.log(data);
  }, []);
  
  return <div>App</div>;
}
// Output: Warning! useEffect must return a cleanup function or nothing
```
**Explanation:** `useEffect` expects a cleanup function (or nothing) to be returned, not a Promise. Async functions return Promises. Solution: define an async function inside and call it, or use `.then()`.

---

### Question 20: Correct Async Pattern
```javascript
function App() {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    let cancelled = false;
    
    async function fetchData() {
      const result = await fetch('/api');
      if (!cancelled) {
        setData(result);
      }
    }
    
    fetchData();
    return () => { cancelled = true; };
  }, []);
  
  return <div>{data}</div>;
}
// Output: Properly handles async data fetching with cleanup
```
**Explanation:** This pattern prevents setting state on unmounted components. The cleanup function sets a flag that prevents state updates if the component unmounts before the fetch completes.

---

### Question 21: useEffect with Function Dependency
```javascript
function App() {
  const [count, setCount] = useState(0);
  
  const logCount = () => {
    console.log(count);
  };
  
  useEffect(() => {
    logCount();
  }, [logCount]);
  
  return <button onClick={() => setCount(count + 1)}>Click</button>;
}
// Output: Effect runs on every render
```
**Explanation:** `logCount` is recreated on every render, so the dependency changes each time. Solution: wrap `logCount` with `useCallback` or move it inside the effect.

---

### Question 22: setState Inside useEffect Without Dependency
```javascript
function App() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    setCount(count + 1);
  }, []);
  
  return <div>{count}</div>;
}
// Output: count is 1
```
**Explanation:** Effect runs once on mount, setting count to 1. Without `count` in dependencies, it doesn't create an infinite loop. However, this pattern is usually an anti-pattern unless you specifically want a side effect on mount only.

---

### Question 23: Infinite Loop with useEffect
```javascript
function App() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    setCount(count + 1);
  }, [count]);
  
  return <div>{count}</div>;
}
// Output: Infinite loop! Component keeps re-rendering
```
**Explanation:** Effect runs when `count` changes → effect updates `count` → triggers re-render → effect runs again → infinite loop. Never update a state variable in an effect that depends on that variable without proper conditions.

---

### Question 24: useEffect Dependency with Primitive vs Reference
```javascript
function App() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    console.log('Primitive');
  }, [count]);
  
  useEffect(() => {
    console.log('Array');
  }, [[1, 2, 3]]);
  
  return <div>{count}</div>;
}
// Output: "Array" logs on every render, "Primitive" only when count changes
```
**Explanation:** Primitive values (numbers, strings) are compared by value. Arrays/objects are compared by reference. `[1,2,3]` creates a new array each render, so the effect runs every time.

---

## React Reconciliation & Keys (Questions 25-32)

### Question 25: Missing Key in List
```javascript
function App() {
  const items = ['A', 'B', 'C'];
  return (
    <div>
      {items.map(item => <div>{item}</div>)}
    </div>
  );
}
// Output: Warning in console about missing key prop
```
**Explanation:** React needs keys to identify which items changed, were added, or removed. Without keys, React may reuse DOM nodes incorrectly, leading to bugs with component state or performance issues.

---

### Question 26: Index as Key Anti-pattern
```javascript
function TodoList() {
  const [todos, setTodos] = useState(['Task 1', 'Task 2']);
  
  const addTodo = () => {
    setTodos(['New Task', ...todos]);
  };
  
  return (
    <div>
      {todos.map((todo, index) => (
        <input key={index} defaultValue={todo} />
      ))}
      <button onClick={addTodo}>Add</button>
    </div>
  );
}
// Output: Input values don't match tasks after adding new task
```
**Explanation:** Using index as key causes problems when items are reordered or inserted. When "New Task" is added at index 0, React thinks index 0 and 1 are the same elements, just with different content, causing input state to be mismatched. Use stable unique IDs instead.

---

### Question 27: Key on Conditional Render
```javascript
function App() {
  const [showA, setShowA] = useState(true);
  
  return (
    <div>
      {showA ? <Input key="a" /> : <Input key="b" />}
      <button onClick={() => setShowA(!showA)}>Toggle</button>
    </div>
  );
}
// Output: Input resets when toggling (different keys = different components)
```
**Explanation:** Different keys tell React these are different components. When the key changes, React unmounts the old component and mounts a new one, resetting its state. If you want to preserve state, use the same key or conditional props instead.

---

### Question 28: Same Key Forces Reuse
```javascript
function App() {
  const [showA, setShowA] = useState(true);
  
  return (
    <div>
      {showA ? <Input key="same" /> : <Input key="same" />}
      <button onClick={() => setShowA(!showA)}>Toggle</button>
    </div>
  );
}
// Output: Input state persists when toggling
```
**Explanation:** Same key tells React to reuse the component. Even though the conditional changes, React sees the same key and type, so it reuses the existing component instance, preserving its state.

---

### Question 29: Key Reset Pattern
```javascript
function UserProfile({ userId }) {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    fetchUser(userId).then(setData);
  }, [userId]);
  
  return <div>{data?.name}</div>;
}

function App() {
  const [userId, setUserId] = useState(1);
  return <UserProfile key={userId} userId={userId} />;
}
// Output: Component fully remounts when userId changes
```
**Explanation:** Changing the `key` prop forces React to unmount and remount the component, resetting all its state. This is useful for resetting complex component state without manual cleanup.

---

### Question 30: Fragment with Key
```javascript
function App() {
  const items = [{id: 1, name: 'A'}, {id: 2, name: 'B'}];
  
  return (
    <div>
      {items.map(item => (
        <React.Fragment key={item.id}>
          <div>{item.name}</div>
          <hr />
        </React.Fragment>
      ))}
    </div>
  );
}
// Output: Works correctly with keys on fragments
```
**Explanation:** You can (and should) add keys to `<React.Fragment>` when mapping arrays. The shorthand `<>...</>` syntax doesn't support keys, so you must use the full `<React.Fragment>` form.

---

### Question 31: Dynamic Children Reconciliation
```javascript
function App() {
  const [reverse, setReverse] = useState(false);
  const items = reverse ? ['C', 'B', 'A'] : ['A', 'B', 'C'];
  
  return (
    <div>
      {items.map(item => <Input key={item} defaultValue={item} />)}
      <button onClick={() => setReverse(!reverse)}>Reverse</button>
    </div>
  );
}
// Output: Input values follow the keys correctly
```
**Explanation:** With proper keys, React tracks each element across re-renders even when their positions change. Input with key "A" maintains its state regardless of its position in the array.

---

### Question 32: No Key Needed for Static Lists
```javascript
function App() {
  return (
    <div>
      <p>First</p>
      <p>Second</p>
      <p>Third</p>
    </div>
  );
}
// Output: No warning, works fine
```
**Explanation:** Keys are only needed for dynamic lists (arrays). Static JSX children don't need keys because React can track them by their position, which never changes.

---

## Component Re-rendering (Questions 33-40)

### Question 33: Parent Re-render Causes Child Re-render
```javascript
function Child() {
  console.log('Child render');
  return <div>Child</div>;
}

function Parent() {
  const [count, setCount] = useState(0);
  console.log('Parent render');
  
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      <Child />
    </div>
  );
}
// Output: Both "Parent render" and "Child render" log on each click
```
**Explanation:** By default, when a parent re-renders, all its children re-render too, even if their props haven't changed. This is React's default behavior. Use `React.memo` to prevent unnecessary child re-renders.

---

### Question 34: React.memo Basic Usage
```javascript
const Child = React.memo(() => {
  console.log('Child render');
  return <div>Child</div>;
});

function Parent() {
  const [count, setCount] = useState(0);
  console.log('Parent render');
  
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      <Child />
    </div>
  );
}
// Output: "Child render" logs only once
```
**Explanation:** `React.memo` prevents re-rendering if props haven't changed (shallow comparison). Since `Child` receives no props, it only renders once on mount.

---

### Question 35: React.memo with Object Prop
```javascript
const Child = React.memo(({ user }) => {
  console.log('Child render');
  return <div>{user.name}</div>;
});

function Parent() {
  const [count, setCount] = useState(0);
  const user = { name: 'John' };
  
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      <Child user={user} />
    </div>
  );
}
// Output: "Child render" logs on every click
```
**Explanation:** Even with `React.memo`, a new `user` object is created on each render. Shallow comparison sees different references and triggers re-render. Solution: use `useMemo` or move object outside component.

---

### Question 36: React.memo with Function Prop
```javascript
const Child = React.memo(({ onClick }) => {
  console.log('Child render');
  return <button onClick={onClick}>Click</button>;
});

function Parent() {
  const [count, setCount] = useState(0);
  
  const handleClick = () => {
    console.log('Clicked');
  };
  
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      <Child onClick={handleClick} />
    </div>
  );
}
// Output: "Child render" logs on every click
```
**Explanation:** `handleClick` is recreated on every render. Use `useCallback` to memoize the function: `const handleClick = useCallback(() => { ... }, [])`.

---

### Question 37: React.memo Custom Comparison
```javascript
const Child = React.memo(
  ({ user }) => {
    console.log('Child render');
    return <div>{user.name}</div>;
  },
  (prevProps, nextProps) => {
    return prevProps.user.id === nextProps.user.id;
  }
);

function Parent() {
  const [count, setCount] = useState(0);
  const user = { id: 1, name: 'John', timestamp: Date.now() };
  
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      <Child user={user} />
    </div>
  );
}
// Output: "Child render" logs only once
```
**Explanation:** The second argument to `React.memo` is a custom comparison function. Return `true` to skip re-render, `false` to allow it. Here, we only compare `user.id`, ignoring other properties.

---

### Question 38: Inline Object Prop
```javascript
function Child({ style }) {
  console.log('Child render');
  return <div style={style}>Child</div>;
}

function Parent() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      <Child style={{ color: 'red' }} />
    </div>
  );
}
// Output: "Child render" logs on every click
```
**Explanation:** Inline objects `{ color: 'red' }` create a new reference on each render. Move the object outside the component or use `useMemo`: `const style = useMemo(() => ({ color: 'red' }), [])`.

---

### Question 39: Same Element Reference Optimization
```javascript
function Parent() {
  const [count, setCount] = useState(0);
  const child = <ExpensiveChild />;
  
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      {child}
    </div>
  );
}
// Output: ExpensiveChild doesn't re-render on count change
```
**Explanation:** `child` is created once and its reference doesn't change across renders. React sees the same element reference and doesn't re-render it. This is a clever optimization pattern.

---

### Question 40: Children Prop Optimization
```javascript
function Wrapper({ children }) {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      {children}
    </div>
  );
}

function App() {
  return (
    <Wrapper>
      <ExpensiveComponent />
    </Wrapper>
  );
}
// Output: ExpensiveComponent doesn't re-render on count change
```
**Explanation:** `children` prop is created in the parent (`App`), so when `Wrapper` re-renders due to its own state, `children` reference remains the same. React skips re-rendering `ExpensiveComponent`.

---

## Refs & useRef (Questions 41-48)

### Question 41: useRef Doesn't Trigger Re-render
```javascript
function App() {
  const countRef = useRef(0);
  
  const handleClick = () => {
    countRef.current++;
    console.log(countRef.current);
  };
  
  return (
    <div>
      <button onClick={handleClick}>Click</button>
      <div>Count: {countRef.current}</div>
    </div>
  );
}
// Output: Console logs increment, but UI shows 0
```
**Explanation:** Updating `ref.current` doesn't trigger a re-render. Refs are for storing mutable values that don't affect rendering. Use state if you need to trigger re-renders.

---

### Question 42: Ref vs State for DOM Element
```javascript
function App() {
  const inputRef = useRef(null);
  
  const focusInput = () => {
    inputRef.current.focus();
  };
  
  return (
    <div>
      <input ref={inputRef} />
      <button onClick={focusInput}>Focus</button>
    </div>
  );
}
// Output: Clicking button focuses the input
```
**Explanation:** Refs are perfect for accessing DOM elements imperatively. `useRef` provides a stable reference that persists across renders.

---

### Question 43: Ref in useEffect
```javascript
function App() {
  const renderCount = useRef(0);
  
  useEffect(() => {
    renderCount.current++;
    console.log('Render count:', renderCount.current);
  });
  
  const [count, setCount] = useState(0);
  
  return <button onClick={() => setCount(count + 1)}>Click</button>;
}
// Output: Logs incrementing render count on each click
```
**Explanation:** Refs are useful for tracking values across renders without causing re-renders. This pattern tracks how many times the component has rendered.

---

### Question 44: Stale Ref in Closure
```javascript
function App() {
  const [count, setCount] = useState(0);
  const countRef = useRef(count);
  
  useEffect(() => {
    const id = setInterval(() => {
      console.log('Count:', countRef.current);
    }, 1000);
    return () => clearInterval(id);
  }, []);
  
  return <button onClick={() => setCount(count + 1)}>Click</button>;
}
// Output: Always logs 0
```
**Explanation:** `countRef` is initialized with 0 and never updated. To keep ref in sync, add: `useEffect(() => { countRef.current = count; }, [count])`.

---

### Question 45: Ref Callback Pattern
```javascript
function App() {
  const inputRef = useCallback((node) => {
    if (node) {
      console.log('Input width:', node.offsetWidth);
      node.focus();
    }
  }, []);
  
  return <input ref={inputRef} />;
}
// Output: Logs width and focuses input on mount
```
**Explanation:** Callback refs are called with the DOM node when mounted and `null` when unmounted. They're useful for performing actions immediately when the element is available, before `componentDidMount` or `useEffect`.

---

### Question 46: createRef vs useRef
```javascript
function App() {
  const refA = useRef(0);
  const refB = React.createRef();
  
  refA.current++;
  refB.current = (refB.current || 0) + 1;
  
  console.log('useRef:', refA.current, 'createRef:', refB.current);
  
  const [, forceRender] = useState({});
  return <button onClick={() => forceRender({})}>Render</button>;
}
// Output: useRef increments across renders, createRef resets to 1
```
**Explanation:** `useRef` returns the same ref object on every render. `createRef` creates a new ref object on each render. In function components, always use `useRef`.

---

### Question 47: Ref to Store Previous Value
```javascript
function App() {
  const [count, setCount] = useState(0);
  const prevCountRef = useRef();
  
  useEffect(() => {
    prevCountRef.current = count;
  }, [count]);
  
  const prevCount = prevCountRef.current;
  
  return (
    <div>
      <div>Current: {count}, Previous: {prevCount}</div>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
// Output: Shows previous and current count values
```
**Explanation:** This pattern uses refs to access the previous value of a state variable. The effect updates the ref after render, so during render we have the previous value.

---

### Question 48: forwardRef Basics
```javascript
const Input = React.forwardRef((props, ref) => {
  return <input ref={ref} {...props} />;
});

function App() {
  const inputRef = useRef();
  
  return (
    <div>
      <Input ref={inputRef} />
      <button onClick={() => inputRef.current.focus()}>Focus</button>
    </div>
  );
}
// Output: Button focuses the input
```
**Explanation:** Function components can't receive refs directly. `forwardRef` allows passing a ref through a component to a child DOM element or component. The ref is passed as the second parameter.

---

## React Memo & useMemo (Questions 49-56)

### Question 49: useMemo Basic Usage
```javascript
function App() {
  const [count, setCount] = useState(0);
  const [value, setValue] = useState('');
  
  const expensiveResult = useMemo(() => {
    console.log('Computing...');
    return count * 2;
  }, [count]);
  
  return (
    <div>
      <input value={value} onChange={(e) => setValue(e.target.value)} />
      <div>{expensiveResult}</div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
    </div>
  );
}
// Output: "Computing..." only logs when count changes, not on typing
```
**Explanation:** `useMemo` memoizes the result of an expensive calculation. It only recomputes when dependencies (`count`) change, not on unrelated state updates (`value`).

---

### Question 50: useMemo with Object
```javascript
const Child = React.memo(({ data }) => {
  console.log('Child render');
  return <div>{data.value}</div>;
});

function Parent() {
  const [count, setCount] = useState(0);
  
  const data = useMemo(() => ({ value: count }), [count]);
  
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <Child data={data} />
    </div>
  );
}
// Output: "Child render" only when count changes
```
**Explanation:** `useMemo` creates a stable object reference as long as dependencies don't change. This works well with `React.memo` to prevent unnecessary child re-renders.

---

### Question 51: useMemo with Empty Dependencies
```javascript
function App() {
  const value = useMemo(() => {
    console.log('Creating value');
    return { data: Math.random() };
  }, []);
  
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <div>{value.data}</div>
      <button onClick={() => setCount(count + 1)}>Re-render</button>
    </div>
  );
}
// Output: "Creating value" logs once, value.data never changes
```
**Explanation:** Empty dependency array `[]` means the memoized value is computed only once on mount and never recomputed. Useful for expensive initializations.

---

### Question 52: useMemo vs useEffect
```javascript
function App() {
  const [count, setCount] = useState(0);
  
  // This is wrong!
  useMemo(() => {
    document.title = `Count: ${count}`;
  }, [count]);
  
  return <button onClick={() => setCount(count + 1)}>Click</button>;
}
// Output: Works but is incorrect usage
```
**Explanation:** `useMemo` is for computing values, not side effects. Use `useEffect` for side effects. `useMemo` runs during render (may not run or run multiple times), `useEffect` runs after render is committed.

---

### Question 53: Premature Optimization with useMemo
```javascript
function App() {
  const [count, setCount] = useState(0);
  
  const doubledCount = useMemo(() => count * 2, [count]);
  
  return <div>{doubledCount}</div>;
}
// Output: Works but unnecessary overhead
```
**Explanation:** Don't use `useMemo` for cheap calculations. `count * 2` is extremely fast. `useMemo` adds overhead (function call, dependency checking). Profile before optimizing.

---

### Question 54: useMemo with Array Dependency
```javascript
function App({ items }) {
  const sortedItems = useMemo(() => {
    console.log('Sorting');
    return [...items].sort();
  }, [items]);
  
  return <div>{sortedItems.length}</div>;
}
// Output: "Sorting" logs whenever items array reference changes
```
**Explanation:** `useMemo` uses shallow comparison for dependencies. If `items` is a new array on each render (even with same contents), it will recompute. Ensure parent memoizes or stabilizes the array reference.

---

### Question 55: useMemo for Referential Equality
```javascript
function Parent() {
  const [count, setCount] = useState(0);
  const [text, setText] = useState('');
  
  const config = useMemo(() => ({
    id: 1,
    name: 'Config'
  }), []);
  
  return (
    <div>
      <input value={text} onChange={(e) => setText(e.target.value)} />
      <Child config={config} />
    </div>
  );
}
// Output: Child receives same config object across Parent re-renders
```
**Explanation:** Without `useMemo`, a new `config` object would be created on every render. `useMemo` with empty deps ensures referential equality across re-renders.

---

### Question 56: useMemo Doesn't Guarantee Caching
```javascript
function App() {
  const value = useMemo(() => {
    console.log('Computing');
    return expensiveCalculation();
  }, []);
  
  return <div>{value}</div>;
}
// Output: "Computing" may log more than once in development (Strict Mode)
```
**Explanation:** React may discard memoized values and recompute on next render (memory optimization). In Strict Mode, it intentionally invokes functions twice. Don't rely on `useMemo` for semantic correctness, only performance.

---

## useCallback Hook (Questions 57-62)

### Question 57: useCallback Basic Usage
```javascript
const Child = React.memo(({ onClick }) => {
  console.log('Child render');
  return <button onClick={onClick}>Click</button>;
});

function Parent() {
  const [count, setCount] = useState(0);
  
  const handleClick = useCallback(() => {
    console.log('Clicked');
  }, []);
  
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      <Child onClick={handleClick} />
    </div>
  );
}
// Output: "Child render" logs only once
```
**Explanation:** `useCallback` memoizes the function reference. Without it, `handleClick` would be a new function on each render, causing `Child` to re-render despite `React.memo`.

---

### Question 58: useCallback with Dependencies
```javascript
function App() {
  const [count, setCount] = useState(0);
  
  const handleClick = useCallback(() => {
    console.log(count);
  }, []);
  
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={handleClick}>Log</button>
    </div>
  );
}
// Output: Always logs 0
```
**Explanation:** Empty dependencies means the function is created once with `count` as 0. It captures that value in a closure. To log current count, add `count` to dependencies: `[count]`, or use a ref.

---

### Question 59: useCallback vs useMemo for Functions
```javascript
// These are equivalent:

const memoizedCallback = useCallback(() => {
  doSomething(a, b);
}, [a, b]);

const memoizedCallback = useMemo(() => {
  return () => doSomething(a, b);
}, [a, b]);

// Output: Both create memoized function references
```
**Explanation:** `useCallback(fn, deps)` is shorthand for `useMemo(() => fn, deps)`. Use `useCallback` for functions, `useMemo` for values.

---

### Question 60: useCallback with Inline Function
```javascript
function App() {
  const [count, setCount] = useState(0);
  
  const handleClick = useCallback(() => {
    setCount(count + 1);
  }, [count]);
  
  return <button onClick={handleClick}>Count: {count}</button>;
}
// Output: Works but creates new function on each count change
```
**Explanation:** Including `count` in dependencies means `handleClick` is recreated whenever `count` changes, defeating the purpose of memoization. Use functional form: `setCount(prev => prev + 1)` with empty deps.

---

### Question 61: useCallback in useEffect
```javascript
function App({ id }) {
  const fetchData = useCallback(() => {
    fetch(`/api/${id}`).then(console.log);
  }, [id]);
  
  useEffect(() => {
    fetchData();
  }, [fetchData]);
  
  return <div>App</div>;
}
// Output: Fetches data when id changes
```
**Explanation:** Memoizing `fetchData` with `useCallback` allows using it as a `useEffect` dependency without causing unnecessary effect runs. When `id` changes, `fetchData` is recreated, triggering the effect.

---

### Question 62: useCallback Overhead
```javascript
function App() {
  const handleClick = useCallback(() => {
    console.log('Clicked');
  }, []);
  
  return <button onClick={handleClick}>Click</button>;
}
// Output: Works but useCallback is unnecessary here
```
**Explanation:** If the memoized function isn't passed to a memoized child or used in a dependency array, `useCallback` adds overhead without benefit. Regular functions are fine for event handlers.

---

## Context API (Questions 63-68)

### Question 63: Context Re-renders All Consumers
```javascript
const MyContext = createContext();

function Child() {
  const value = useContext(MyContext);
  console.log('Child render');
  return <div>{value.count}</div>;
}

function App() {
  const [count, setCount] = useState(0);
  
  return (
    <MyContext.Provider value={{ count }}>
      <Child />
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </MyContext.Provider>
  );
}
// Output: "Child render" on every click
```
**Explanation:** When context value changes, all consumers re-render. A new object `{ count }` is created each render, triggering all consumers even if `count` hasn't changed.

---

### Question 64: Context with useMemo
```javascript
const MyContext = createContext();

function Child() {
  const value = useContext(MyContext);
  console.log('Child render');
  return <div>{value.count}</div>;
}

function App() {
  const [count, setCount] = useState(0);
  const [text, setText] = useState('');
  
  const value = useMemo(() => ({ count }), [count]);
  
  return (
    <MyContext.Provider value={value}>
      <input value={text} onChange={(e) => setText(e.target.value)} />
      <Child />
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </MyContext.Provider>
  );
}
// Output: "Child render" only when count changes, not on typing
```
**Explanation:** Memoizing context value prevents unnecessary consumer re-renders when unrelated state changes (`text`). Consumers only re-render when the actual context value changes.

---

### Question 65: Context Split Pattern
```javascript
const CountContext = createContext();
const DispatchContext = createContext();

function Child() {
  const dispatch = useContext(DispatchContext);
  console.log('Child render');
  return <button onClick={() => dispatch()}>Increment</button>;
}

function App() {
  const [count, setCount] = useState(0);
  
  return (
    <CountContext.Provider value={count}>
      <DispatchContext.Provider value={() => setCount(c => c + 1)}>
        <Child />
      </DispatchContext.Provider>
    </CountContext.Provider>
  );
}
// Output: "Child render" only once (doesn't consume CountContext)
```
**Explanation:** Splitting context into data and updaters allows components to subscribe only to what they need. `Child` doesn't re-render when `count` changes because it only consumes dispatch.

---

### Question 66: Context Default Value
```javascript
const MyContext = createContext('default');

function Child() {
  const value = useContext(MyContext);
  return <div>{value}</div>;
}

function App() {
  return <Child />;
}
// Output: Displays "default"
```
**Explanation:** When there's no matching Provider above in the tree, `useContext` returns the default value passed to `createContext`. This is useful for testing or providing fallback values.

---

### Question 67: Multiple Context Providers
```javascript
const ThemeContext = createContext('light');
const UserContext = createContext(null);

function Child() {
  const theme = useContext(ThemeContext);
  const user = useContext(UserContext);
  return <div>{theme} - {user?.name}</div>;
}

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <UserContext.Provider value={{ name: 'John' }}>
        <Child />
      </UserContext.Provider>
    </ThemeContext.Provider>
  );
}
// Output: "dark - John"
```
**Explanation:** Components can consume multiple contexts. Each `useContext` call subscribes to its respective context independently.

---

### Question 68: Context Update Performance
```javascript
const MyContext = createContext();

const MemoChild = React.memo(() => {
  console.log('MemoChild render');
  return <div>Memo Child</div>;
});

function ContextChild() {
  const value = useContext(MyContext);
  console.log('ContextChild render');
  return <div>{value}</div>;
}

function App() {
  const [count, setCount] = useState(0);
  
  return (
    <MyContext.Provider value={count}>
      <MemoChild />
      <ContextChild />
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </MyContext.Provider>
  );
}
// Output: Only "ContextChild render" logs on click
```
**Explanation:** `React.memo` works even with context. `MemoChild` doesn't consume context, so it doesn't re-render. Only components that consume context via `useContext` re-render when context changes.

---

## Synthetic Events (Questions 69-74)

### Question 69: Event Pooling (React 16)
```javascript
function App() {
  const handleClick = (e) => {
    console.log(e.type); // "click"
    
    setTimeout(() => {
      console.log(e.type); // null in React 16
    }, 100);
  };
  
  return <button onClick={handleClick}>Click</button>;
}
// Output: In React 16, second log is null. In React 17+, both log "click"
```
**Explanation:** React 16 pooled synthetic events for performance, nullifying properties after the handler. React 17+ removed event pooling. To persist events in React 16, call `e.persist()`.

---

### Question 70: Accessing Native Event
```javascript
function App() {
  const handleClick = (e) => {
    console.log(e.nativeEvent); // Native browser event
    console.log(e.target); // Target element
  };
  
  return <button onClick={handleClick}>Click</button>;
}
// Output: Logs native event and button element
```
**Explanation:** React's synthetic event wraps the native event for cross-browser compatibility. Access the native event via `e.nativeEvent`.

---

### Question 71: Event Handler in setState
```javascript
function App() {
  const [value, setValue] = useState('');
  
  const handleChange = (e) => {
    setValue(e.target.value); // Error in React 16 without persist
  };
  
  return <input value={value} onChange={handleChange} />;
}
// Output: Works in React 17+, needs e.persist() in React 16
```
**Explanation:** In React 16, accessing `e.target.value` inside setState required `e.persist()` or caching the value. React 17+ removed this requirement by eliminating event pooling.

---

### Question 72: stopPropagation in React
```javascript
function App() {
  return (
    <div onClick={() => console.log('Div clicked')}>
      <button onClick={(e) => {
        e.stopPropagation();
        console.log('Button clicked');
      }}>
        Click
      </button>
    </div>
  );
}
// Output: Only "Button clicked" logs
```
**Explanation:** `e.stopPropagation()` prevents event from bubbling up the React component tree (and DOM tree). The div's onClick handler doesn't fire.

---

### Question 73: preventDefault
```javascript
function App() {
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form submitted');
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <button type="submit">Submit</button>
    </form>
  );
}
// Output: "Form submitted" logs, page doesn't reload
```
**Explanation:** `e.preventDefault()` prevents the browser's default behavior. For forms, it prevents page reload. This is the same as native DOM events.

---

### Question 74: Event Handler Return False
```javascript
function App() {
  const handleClick = (e) => {
    return false; // Doesn't prevent default!
  };
  
  return <a href="https://example.com" onClick={handleClick}>Link</a>;
}
// Output: Link navigates despite returning false
```
**Explanation:** Unlike plain HTML `onclick="return false"`, React doesn't support returning `false` to prevent default. You must explicitly call `e.preventDefault()`.

---

## React Strict Mode (Questions 75-78)

### Question 75: Double Render in Strict Mode
```javascript
function App() {
  console.log('Render');
  const [count, setCount] = useState(0);
  
  return <button onClick={() => setCount(count + 1)}>Click</button>;
}

// In index.js:
<React.StrictMode>
  <App />
</React.StrictMode>
// Output: "Render" logs twice per update in development
```
**Explanation:** Strict Mode intentionally double-invokes component functions, constructors, and certain hooks in development to help detect side effects. This doesn't happen in production.

---

### Question 76: useEffect Runs Twice in Strict Mode
```javascript
function App() {
  useEffect(() => {
    console.log('Effect');
    return () => console.log('Cleanup');
  }, []);
  
  return <div>App</div>;
}

<React.StrictMode>
  <App />
</React.StrictMode>
// Output: "Effect" → "Cleanup" → "Effect" on mount in development
```
**Explanation:** Strict Mode mounts components, unmounts them, then mounts again to help detect missing cleanup functions. This simulates what happens when users navigate away and back.

---

### Question 77: Detecting Unsafe Lifecycles
```javascript
class App extends React.Component {
  componentWillMount() {
    console.log('Will mount');
  }
  
  render() {
    return <div>App</div>;
  }
}

<React.StrictMode>
  <App />
</React.StrictMode>
// Output: Warning about deprecated lifecycle method
```
**Explanation:** Strict Mode warns about deprecated lifecycle methods like `componentWillMount`, `componentWillReceiveProps`, and `componentWillUpdate`. These are unsafe in async rendering.

---

### Question 78: Strict Mode Doesn't Affect Production
```javascript
function App() {
  console.count('Render');
  return <div>App</div>;
}

// Development: logs "Render: 2"
// Production: logs "Render: 1"
```
**Explanation:** All Strict Mode checks (double rendering, extra effect runs, warnings) only happen in development. Production builds behave normally for optimal performance.

---

## State Batching (Questions 79-82)

### Question 79: Automatic Batching in Event Handlers
```javascript
function App() {
  const [count1, setCount1] = useState(0);
  const [count2, setCount2] = useState(0);
  console.log('Render');
  
  const handleClick = () => {
    setCount1(count1 + 1);
    setCount2(count2 + 1);
  };
  
  return <button onClick={handleClick}>Click</button>;
}
// Output: "Render" logs once per click
```
**Explanation:** React automatically batches state updates in event handlers into a single re-render for performance. Multiple `setState` calls trigger only one render.

---

### Question 80: No Batching in Async (React 17)
```javascript
function App() {
  const [count1, setCount1] = useState(0);
  const [count2, setCount2] = useState(0);
  console.log('Render');
  
  const handleClick = () => {
    setTimeout(() => {
      setCount1(count1 + 1);
      setCount2(count2 + 1);
    }, 0);
  };
  
  return <button onClick={handleClick}>Click</button>;
}
// React 17: "Render" logs twice per click
// React 18+: "Render" logs once per click
```
**Explanation:** React 17 didn't batch updates outside event handlers (setTimeout, promises, native events). React 18+ introduced automatic batching everywhere with `createRoot`.

---

### Question 81: Opt Out of Batching (React 18)
```javascript
import { flushSync } from 'react-dom';

function App() {
  const [count1, setCount1] = useState(0);
  const [count2, setCount2] = useState(0);
  console.log('Render');
  
  const handleClick = () => {
    flushSync(() => {
      setCount1(count1 + 1);
    });
    // DOM updated here
    flushSync(() => {
      setCount2(count2 + 1);
    });
  };
  
  return <button onClick={handleClick}>Click</button>;
}
// Output: "Render" logs twice per click
```
**Explanation:** `flushSync` forces React to synchronously update the DOM immediately. Use sparingly as it opts out of batching and can hurt performance.

---

### Question 82: Reading State After Multiple Updates
```javascript
function App() {
  const [count, setCount] = useState(0);
  
  const handleClick = () => {
    setCount(count + 1);
    setCount(count + 1);
    console.log(count); // Still logs old value
  };
  
  return <button onClick={handleClick}>{count}</button>;
}
// Output: Console logs old count, UI shows +1
```
**Explanation:** Even with batching, `console.log` runs immediately with the current closure's `count` value. State updates are queued, not applied synchronously. Can't read updated state immediately after setState.

---

## useReducer Hook (Questions 83-86)

### Question 83: useReducer Basics
```javascript
function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    default:
      return state;
  }
}

function App() {
  const [state, dispatch] = useReducer(reducer, { count: 0 });
  
  return (
    <div>
      <div>{state.count}</div>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
    </div>
  );
}
// Output: Count increments on click
```
**Explanation:** `useReducer` is an alternative to `useState` for complex state logic. It takes a reducer function and initial state, returns current state and dispatch function.

---

### Question 84: Dispatch Identity is Stable
```javascript
function App() {
  const [state, dispatch] = useReducer(reducer, { count: 0 });
  
  useEffect(() => {
    console.log('Effect runs');
    dispatch({ type: 'increment' });
  }, [dispatch]); // dispatch doesn't need to be in deps, but it's safe
  
  return <div>{state.count}</div>;
}
// Output: Effect runs once on mount (infinite loop doesn't occur)
```
**Explanation:** React guarantees `dispatch` identity is stable and won't change across re-renders. It's safe to omit from dependency arrays, though including it is harmless.

---

### Question 85: Lazy Initialization
```javascript
function init(initialCount) {
  console.log('Lazy init');
  return { count: initialCount };
}

function App() {
  const [state, dispatch] = useReducer(reducer, 10, init);
  
  return <div>{state.count}</div>;
}
// Output: "Lazy init" logs once, initial count is 10
```
**Explanation:** The third argument to `useReducer` is a lazy initialization function. It receives the second argument and returns initial state. Useful for expensive initializations or resetting state.

---

### Question 86: Dispatch with Closure
```javascript
function App() {
  const [state, dispatch] = useReducer(reducer, { count: 0 });
  
  useEffect(() => {
    const id = setInterval(() => {
      dispatch({ type: 'increment' }); // No stale closure!
    }, 1000);
    return () => clearInterval(id);
  }, []);
  
  return <div>{state.count}</div>;
}
// Output: Count increments every second correctly
```
**Explanation:** Since `dispatch` is stable, you can safely use it in closures without stale values. Unlike `setState`, you don't need to use functional form or add dependencies.

---

## Props & Destructuring (Questions 87-90)

### Question 87: Destructuring Props with Default Values
```javascript
function Greeting({ name = 'Guest', age = 0 }) {
  return <div>{name} is {age} years old</div>;
}

function App() {
  return <Greeting name="John" />;
}
// Output: "John is 0 years old"
```
**Explanation:** Destructuring with default values provides fallbacks for missing props. `age` uses default value 0 since it's not passed. Default values only apply to `undefined`, not `null`.

---

### Question 88: Props Object Passed as Prop
```javascript
function Child(props) {
  const { inputRows, inputCols } = props.props;
  return <div>{inputRows.length}</div>;
}

function Parent() {
  const data = { inputRows: [], inputCols: [] };
  return <Child props={data} />;
}
// Output: Works but confusing naming
```
**Explanation:** Passing props as `<Child props={data} />` creates nested structure `props.props`. Better: `<Child {...data} />` to spread, or `<Child data={data} />` with clear naming.

---

### Question 89: Spread Operator for Props
```javascript
function Button({ onClick, ...rest }) {
  return <button onClick={onClick} {...rest} />;
}

function App() {
  return (
    <Button 
      onClick={() => console.log('Clicked')}
      className="btn"
      disabled
    >
      Click me
    </Button>
  );
}
// Output: Button receives all props except onClick is handled separately
```
**Explanation:** `...rest` collects remaining props after destructuring specific ones. Useful for wrapper components that pass most props through to children.

---

### Question 90: PropTypes with Destructuring
```javascript
function User({ name, age }) {
  return <div>{name} - {age}</div>;
}

User.propTypes = {
  name: PropTypes.string.isRequired,
  age: PropTypes.number
};

function App() {
  return <User name={123} />; // Warning in console
}
// Output: Logs PropTypes warning, renders "123 - undefined"
```
**Explanation:** PropTypes validates props at runtime in development. Destructuring works with PropTypes. Here, `name` should be string but receives number, triggering a warning.

---

## Portals & Event Bubbling (Questions 91-93)

### Question 91: Portal Event Bubbling
```javascript
function Modal({ children }) {
  return ReactDOM.createPortal(
    children,
    document.getElementById('modal-root')
  );
}

function App() {
  const handleClick = () => {
    console.log('Parent clicked');
  };
  
  return (
    <div onClick={handleClick}>
      <Modal>
        <button>Click me</button>
      </Modal>
    </div>
  );
}
// Output: "Parent clicked" logs when button is clicked
```
**Explanation:** Events bubble through React component tree, not DOM tree. Even though modal is rendered in a different DOM node, events still bubble to React parent components.

---

### Question 92: Stopping Portal Event Bubbling
```javascript
function Modal({ children, onClose }) {
  return ReactDOM.createPortal(
    <div onClick={onClose}>
      <div onClick={(e) => e.stopPropagation()}>
        {children}
      </div>
    </div>,
    document.getElementById('modal-root')
  );
}
// Output: Clicking inside modal content doesn't trigger onClose
```
**Explanation:** Use `e.stopPropagation()` in portal content to prevent events from bubbling to parent handlers. This is useful for preventing modals from closing when clicking their content.

---

### Question 93: Portal with Context
```javascript
const ThemeContext = createContext('light');

function Modal() {
  const theme = useContext(ThemeContext);
  
  return ReactDOM.createPortal(
    <div className={theme}>Modal content</div>,
    document.getElementById('modal-root')
  );
}

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Modal />
    </ThemeContext.Provider>
  );
}
// Output: Modal receives "dark" theme from context
```
**Explanation:** Portals render in different DOM location but remain in the same React tree. They have access to context, props, and state from their position in the React tree.

---

## Advanced Hooks (Questions 94-100)

### Question 94: useLayoutEffect vs useEffect
```javascript
function App() {
  const [width, setWidth] = useState(0);
  const divRef = useRef();
  
  useLayoutEffect(() => {
    setWidth(divRef.current.offsetWidth);
  }, []);
  
  return <div ref={divRef}>Width: {width}</div>;
}
// Output: Width displays immediately without flicker
```
**Explanation:** `useLayoutEffect` runs synchronously after DOM mutations but before browser paint. It's perfect for DOM measurements or mutations that need to happen before the user sees the update. `useEffect` would cause a flicker.

---

### Question 95: useImperativeHandle
```javascript
const FancyInput = forwardRef((props, ref) => {
  const inputRef = useRef();
  
  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current.focus(),
    clear: () => inputRef.current.value = ''
  }));
  
  return <input ref={inputRef} />;
});

function App() {
  const ref = useRef();
  
  return (
    <div>
      <FancyInput ref={ref} />
      <button onClick={() => ref.current.focus()}>Focus</button>
      <button onClick={() => ref.current.clear()}>Clear</button>
    </div>
  );
}
// Output: Buttons control input through custom ref API
```
**Explanation:** `useImperativeHandle` customizes the instance value exposed to parent when using `forwardRef`. Instead of exposing DOM element, you can expose custom methods.

---

### Question 96: React.lazy and Suspense
```javascript
const LazyComponent = React.lazy(() => import('./Heavy'));

function App() {
  const [show, setShow] = useState(false);
  
  return (
    <div>
      <button onClick={() => setShow(true)}>Load</button>
      {show && (
        <Suspense fallback={<div>Loading...</div>}>
          <LazyComponent />
        </Suspense>
      )}
    </div>
  );
}
// Output: Shows "Loading..." while component loads, then renders it
```
**Explanation:** `React.lazy` enables code splitting. It returns a component that loads dynamically. Must be wrapped in `Suspense` which shows fallback UI while loading.

---

### Question 97: useDeferredValue
```javascript
function App() {
  const [text, setText] = useState('');
  const deferredText = useDeferredValue(text);
  
  return (
    <div>
      <input value={text} onChange={(e) => setText(e.target.value)} />
      <SlowList text={deferredText} />
    </div>
  );
}
// Output: Input updates immediately, SlowList updates after with lower priority
```
**Explanation:** `useDeferredValue` defers updating a value until more urgent updates finish. The input stays responsive while the expensive list render is deferred. Part of concurrent features in React 18+.

---

### Question 98: useTransition
```javascript
function App() {
  const [isPending, startTransition] = useTransition();
  const [input, setInput] = useState('');
  const [list, setList] = useState([]);
  
  const handleChange = (e) => {
    setInput(e.target.value);
    startTransition(() => {
      setList(generateHugeList(e.target.value));
    });
  };
  
  return (
    <div>
      <input value={input} onChange={handleChange} />
      {isPending && <Spinner />}
      <HugeList items={list} />
    </div>
  );
}
// Output: Input updates immediately, list updates are marked as non-urgent
```
**Explanation:** `useTransition` lets you mark state updates as non-urgent (transitions). Urgent updates (input) happen immediately, transitions can be interrupted. `isPending` indicates if transition is in progress.

---

### Question 99: Error Boundaries
```javascript
class ErrorBoundary extends React.Component {
  state = { hasError: false };
  
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  
  componentDidCatch(error, errorInfo) {
    console.log(error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>;
    }
    return this.props.children;
  }
}

function BuggyComponent() {
  throw new Error('Oops!');
}

function App() {
  return (
    <ErrorBoundary>
      <BuggyComponent />
    </ErrorBoundary>
  );
}
// Output: Shows "Something went wrong" instead of crashing
```
**Explanation:** Error boundaries catch JavaScript errors in component tree, log them, and display fallback UI. Currently only available as class components. They catch errors during rendering, lifecycles, and constructors of child components.

---

### Question 100: dangerouslySetInnerHTML
```javascript
function App() {
  const html = '<script>alert("XSS")</script><p>Content</p>';
  
  return (
    <div dangerouslySetInnerHTML={{ __html: html }} />
  );
}
// Output: Script doesn't execute (sanitized by browser), shows <p>Content</p>
```
**Explanation:** `dangerouslySetInnerHTML` injects raw HTML, bypassing React's XSS protection. Named "dangerous" as a warning. The `__html` key is intentionally verbose to make you think twice. Always sanitize user-generated content before using this. Modern browsers have some XSS protection, but don't rely on it.

---

## Summary

These 100 tricky questions cover:
- **State Management**: useState, useReducer, closures, stale state
- **Side Effects**: useEffect, useLayoutEffect, cleanup, dependencies
- **Performance**: React.memo, useMemo, useCallback, reconciliation
- **Refs**: useRef, forwardRef, useImperativeHandle
- **Advanced Patterns**: Context, portals, error boundaries, Suspense
- **Concurrency**: useTransition, useDeferredValue
- **Events**: Synthetic events, batching, event pooling
- **Developer Tools**: Strict Mode, debugging re-renders

**Key Takeaways:**
1. Always use functional form for state updates when referencing previous state
2. Memoize objects and functions passed as props to memoized components
3. Be careful with closures in effects and callbacks
4. Use proper keys for lists - never use index for dynamic lists
5. Understand when React re-renders and how to optimize
6. `dispatch` from useReducer is stable, `setState` from useState is stable (but often wrapped)
7. Context triggers re-renders for all consumers - split contexts and memoize values
8. Refs don't trigger re-renders - use them for values that don't affect rendering
9. Profile before optimizing - premature optimization adds overhead
10. React 18+ automatic batching and concurrent features change some behaviors

**Practice Tips:**
- Set up a local environment and test each example
- Modify examples to experiment with variations
- Use React DevTools Profiler to understand re-renders
- Enable ESLint rules for hooks to catch common mistakes
- Read error messages carefully - React provides helpful warnings

Happy coding! 🚀
