# Chapter 10: Transactions & ACID Properties

Transactions ensure that database operations are reliable, consistent, and recoverable, especially in the presence of concurrent users and unexpected failures. ACID properties—Atomicity, Consistency, Isolation, and Durability—are the foundational principles supporting safe transactions.

---

## 10.1 Transaction Lifecycle

A transaction is a logical unit of work that consists of one or more SQL statements executed as a single operation. Transactions are bracketed by `BEGIN/START TRANSACTION` and `COMMIT` or `ROLLBACK`.

### 10.1.1 BEGIN, COMMIT, ROLLBACK

- **BEGIN/START TRANSACTION:** Marks the start of a transaction.
- **COMMIT:** All operations become permanent; changes are saved to the database.
- **ROLLBACK:** Undoes all changes since the last BEGIN, reverting the database to its earlier state.

```sql
-- Example: Transfer funds between two accounts
BEGIN;

UPDATE accounts
SET balance = balance - 100
WHERE account_id = 101;

UPDATE accounts
SET balance = balance + 100
WHERE account_id = 202;

COMMIT;
```

_Output_: Both updates succeed together, or not at all.

```sql
-- Example with error triggering ROLLBACK
BEGIN;

UPDATE accounts SET balance = balance - 500 WHERE account_id = 101;
-- Oops: forgot to update account 202, or an error occurs
ROLLBACK;
```

_Output_: No balance is changed.

### 10.1.2 Savepoints and Nesting

Savepoints allow partial rollbacks within a transaction. Useful for error recovery during multi-step operations.

```sql
BEGIN;
INSERT INTO orders VALUES (1001, CURRENT_DATE, 250.00);

SAVEPOINT after_order;

-- Faulty insert
INSERT INTO order_items VALUES (1001, 1, 501, 2, 25.99);

ROLLBACK TO SAVEPOINT after_order;

-- Insert correct order item
INSERT INTO order_items VALUES (1001, 1, 502, 3, 15.00);

COMMIT;
```

_Output_: Only the correct order item is added.

---

## 10.2 ACID Guarantees

### 10.2.1 Atomicity & Consistency

**Atomicity:** Each transaction is "all or nothing"—either all steps succeed, or none are applied.

**Consistency:** A transaction brings the database from one valid state to another, enforcing all rules and constraints.

### 10.2.2 Isolation & Durability

**Isolation:** Each transaction executes independently of others. Intermediate results are not visible until commit.

**Durability:** Once committed, changes survive crashes, power losses, and system failures (backed by logging and backup).

```sql
-- Example: Isolation - Alice and Bob acquire concert tickets
BEGIN;  -- Alice's session
UPDATE tickets SET status = 'RESERVED' WHERE seat_no = 1;
-- (No other session can see this UPDATE until commit)

BEGIN;  -- Bob's session
UPDATE tickets SET status = 'RESERVED' WHERE seat_no = 1;
-- Bob is blocked or fails due to Alice's uncommitted change

-- Alice finishes
COMMIT;
-- Now Bob can attempt
```

_Output_: No double reservation due to isolation.

### 10.2.3 Write-Ahead Logging (WAL) and Crash Recovery

- **WAL:** All changes are first written to a transaction log before being applied, ensuring recoverability.
- On crash, the DB restores by replaying the log to redo/undo changes as needed.

---

## 10.3 Two-Phase Commit (2PC)

A protocol used for transactions spanning multiple databases/servers to ensure commitment or rollback across all systems.

### 10.3.1 Prepare and Commit Phases

- **Phase 1 (Prepare):** Each involved system writes changes but does not commit. Systems respond to coordinator: "ready to commit" or "fail."
- **Phase 2 (Commit):** If all are ready, coordinator instructs commit; else, instructs rollback.

```text
System A: PREPARE → READY
System B: PREPARE → FAIL
Coordinator: ROLLBACK to everyone (consistency preserved)
```

### 10.3.2 Coordinator Failures and Recovery

- If the coordinator crashes after prepare, systems "wait" in a locked state until coordinator recovers and sends decision.
- Ensures no partial commits in distributed transactions.

---

## 10.4 Isolation Anomalies

Isolation levels govern which anomalies transactions might experience:

### 10.4.1 Dirty, Non-repeatable, Phantom Reads

- **Dirty Read:** Transaction reads uncommitted changes from another transaction.
- **Non-repeatable Read:** A row retrieved twice yields different results due to updates in another transaction.
- **Phantom Read:** Repeating a query returns new rows inserted by other transactions.

```sql
-- Example: Non-repeatable read at READ COMMITTED isolation
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

SELECT balance FROM accounts WHERE account_id = 101;
-- Another transaction updates the balance and commits
SELECT balance FROM accounts WHERE account_id = 101;
-- Balance may have changed between reads
```

### 10.4.2 Lost Update and Write Skew

- **Lost Update:** Two transactions overwrite each other's changes.
- **Write Skew:** Interleaved writes in concurrent transactions lead to broken invariants.

```sql
-- Lost update scenario
Transaction 1: SELECT stock FROM products WHERE product_id = 10; -- stock=5
Transaction 2: SELECT stock FROM products WHERE product_id = 10; -- stock=5

Transaction 1: UPDATE products SET stock = 4 WHERE product_id = 10;
Transaction 2: UPDATE products SET stock = 4 WHERE product_id = 10;
-- Stock should be 3, but ends up as 4.

-- Prevent with serializable isolation or explicit locking.
```

---

**Summary:**

- Transactions group SQL statements for atomic and consistent operations.
- ACID properties ensure robust data integrity, even in failure and concurrency scenarios.
- Savepoints and two-phase commit provide advanced control over error recovery and distributed operations.
- Select appropriate isolation levels (READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE) based on business needs.

_End of Chapter 10_
