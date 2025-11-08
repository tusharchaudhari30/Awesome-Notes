# Chapter 11: Concurrency Control & Locking

Concurrency control manages simultaneous access to the database by multiple users, ensuring consistency, isolation, and integrity of transactions. Locking mechanisms and multi-version concurrency control (MVCC) prevent conflicts, deadlocks, and data anomalies during concurrent operations.

## Input Tables

```sql
-- accounts table
accounts:
account_id | customer_id | balance
101        | 1           | 5000
102        | 2           | 3000
103        | 3           | 1000

-- tickets table
tickets:
ticket_id | seat_no | status
201       | 1       | AVAILABLE
202       | 2       | AVAILABLE
```

## 11.1 Locking Mechanisms

### 11.1.1 Pessimistic vs Optimistic Locking

- **Pessimistic Locking:** Database acquires locks immediately and holds until transaction end, preventing other transactions from accessing locked data. Best for high contention.
- **Optimistic Locking:** Transactions proceed without locks but check for conflicts before commit. Best for low contention.

```sql
-- Pessimistic: Explicit lock (SQL Server syntax)
BEGIN TRANSACTION;
SELECT balance FROM accounts WHERE account_id = 101 WITH (XLOCK);  -- acquire exclusive lock
UPDATE accounts SET balance = balance - 100 WHERE account_id = 101;
COMMIT;

-- Optimistic: Use a version/timestamp column
UPDATE accounts
SET balance = balance - 100, version = version + 1
WHERE account_id = 101 AND version = :old_version;
-- If no rows updated, someone else changed it; handle conflict
```

### 11.1.2 Row-level, Page-level, Table-level Locks

- **Row-level:** Fine-grained, locks specific rows. Allows high concurrency.
- **Page-level:** Locks memory/storage pages. Balances conflict frequency and overhead.
- **Table-level:** Broad, locks entire table. Simple but low concurrency.

```sql
-- Explicit Table-level lock (PostgreSQL)
LOCK TABLE accounts IN EXCLUSIVE MODE;
-- Only the locking session can update or insert rows until commit
```

## 11.2 Deadlocks

### 11.2.1 Detection Algorithms

Deadlocks occur when two or more transactions block each other, waiting for locks held by another. Databases detect cycles in their lock graphs.

```sql
-- Deadlock scenario:
-- Transaction 1 locks account 101, wants 102
-- Transaction 2 locks account 102, wants 101
-- Neither can proceed, causing a cycle

-- DBMS automatically detects and aborts one transaction to resolve deadlock
```

### 11.2.2 Resolution Strategies

- **Timeouts:** Transactions wait, then are canceled if locks aren't released soon.
- **Killer Selection:** DB picks a victim transaction to roll back, releasing its locks.

## 11.3 MVCC & Snapshot Isolation

MVCC allows readers to view a snapshot of the data as it existed at transaction start, supporting non-blocking reads.

```sql
-- PostgreSQL: Readers see committed versions
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT * FROM accounts WHERE account_id = 101;
-- Writer in another transaction updates and commits
-- This transaction still sees the original balance until commit
```

- **MVCC Process:**
  - Each write creates a new version of a row.
  - Readers select versions based on their transaction start time.

### 11.3.1 Version Chains and Readers-Writers

```sql
-- Example: Multiple versions for account 101
version 1: balance = 5000  (committed)
version 2: balance = 4900  (modified, not yet committed)
-- Reader sees version 1 until version 2 is committed
```

### 11.3.2 Phantom Prevention Approaches

Phantom rows: A query's result set may change due to inserts/deletes in another transaction. Serializable isolation level and predicate locking prevent this.

```sql
-- Serializable isolation: acquires locks on ranges to prevent new rows from matching query predicates
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

## 11.4 Optimistic Concurrency Tokens

### 11.4.1 Rowversion/Timestamp, ETags

- Use columns that increment each update (`row_version`, `timestamp`, `ETag`) to check for stale data before committing changes.

```sql
-- SQL Server example
UPDATE products
SET price = 19.99
WHERE product_id = 501 AND rowversion = @current_version;
-- If no row affected, another update took place; detect and abort
```

### 11.4.2 Compare-and-Swap Patterns

Used in distributed systems and NoSQL databases.

- **Read current value and version**
- **Write new value only if version matches**
- **If not, retry or fail**

```sql
-- Pseudo-SQL
IF version = CURRENT_VERSION THEN
  UPDATE record SET value = NEW_VALUE, version = version + 1
ELSE
  ERROR: Conflict detected
```

---

**Interview Summary:**

- Pessimistic vs optimistic locking control access to shared data
- Deadlocks arise from circular waits; resolved by automatic or manual intervention
- MVCC provides consistent snapshots for reads, improving concurrency
- Optimistic concurrency tokens support safe, scalable updates in web apps and distributed databases
