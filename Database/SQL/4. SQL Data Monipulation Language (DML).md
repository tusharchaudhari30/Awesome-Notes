# Chapter 4: SQL Data Manipulation Language (DML)

## Input Tables

```sql
-- employees table
employees:
emp_id | first_name | last_name | department  | salary
201    | Emma       | Brown     | Sales       | 60000
202    | Liam       | Smith     | Engineering | 80000
203    | Olivia     | Jones     | Marketing   | 70000
204    | Noah       | Davis     | HR          | 65000

-- orders table
orders:
order_id | customer_id | order_date  | total_amount | status
5001     | 2           | 2025-10-01  | 250.00       | PENDING

-- order_items table
order_items:
order_id | item_number | product_id | quantity | unit_price
1001     | 1           | 501        | 2        | 25.99
1001     | 2           | 502        | 1        | 45.50
1002     | 1           | 501        | 3        | 25.99
1002     | 2           | 503        | 1        | 15.75

-- products table
products:
product_id | product_name | price  | discount_percent | category
501        | Widget A     | 50.00  | 10.0             | Electronics
502        | Widget B     | 75.00  | 0                | Home
503        | Widget C     | 20.00  | 5.0              | Sports
```

## 4.1 INSERT Operations

### 4.1.1 Single-row vs Multi-row Inserts

```sql
-- Single-row insert
INSERT INTO employees (emp_id, first_name, last_name, department, salary)
VALUES (205, 'Sophia', 'Lee', 'Engineering', 82000);
```

**Output (employees after insert):**

```
emp_id | first_name | last_name | department  | salary
201    | Emma       | Brown     | Sales       | 60000
202    | Liam       | Smith     | Engineering | 80000
203    | Olivia     | Jones     | Marketing   | 70000
204    | Noah       | Davis     | HR          | 65000
205    | Sophia     | Lee       | Engineering | 82000
```

```sql
-- Multi-row insert
INSERT INTO employees (emp_id, first_name, last_name, department, salary)
VALUES
  (206, 'Mason', 'Clark', 'Marketing', 72000),
  (207, 'Isabella', 'Garcia', 'Sales', 63000);
```

**Output (employees after multi-row insert):**

```
... plus rows:
206 | Mason     | Clark    | Marketing   | 72000
207 | Isabella  | Garcia   | Sales       | 63000
```

### 4.1.2 Bulk Loads and Performance

```sql
-- PostgreSQL bulk load from CSV
COPY employees(emp_id, first_name, last_name, department, salary)
FROM '/data/new_employees.csv'
WITH (FORMAT csv, HEADER true);
```

**Output:** New rows from CSV loaded into `employees`.

## 4.2 UPDATE Techniques

### 4.2.1 UPDATE with JOINs

```sql
-- Give a 5% raise to all employees in Engineering
UPDATE employees AS e
SET salary = salary * 1.05
FROM departments AS d
WHERE e.department = d.dept_name
  AND d.dept_name = 'Engineering';
```

**Output (employees after update):**

```
emp_id | first_name | last_name | department  | salary
202    | Liam       | Smith     | Engineering | 84000  -- 80000 * 1.05
205    | Sophia     | Lee       | Engineering | 86100  -- 82000 * 1.05
```

### 4.2.2 UPDATE with Subqueries

```sql
-- Set price to category average for underpriced products
UPDATE products
SET price = (
  SELECT AVG(price)
  FROM products AS p2
  WHERE p2.category = products.category
)
WHERE price < (
  SELECT AVG(price)
  FROM products AS p2
  WHERE p2.category = products.category
);
```

**Output (products after update):**

```
product_id | product_name | price | discount_percent | category
501        | Widget A     | 50.00 | 10.0             | Electronics
502        | Widget B     | 75.00 | 0                | Home
503        | Widget C     | 20.00 | 5.0              | Sports
```

(No change if none below their category average)

## 4.3 DELETE & MERGE

### 4.3.1 DELETE vs TRUNCATE

```sql
-- Delete employees in HR
DELETE FROM employees
WHERE department = 'HR';
```

**Output (employees after delete):**

```
Rows with department 'HR' removed (emp_id 204)
```

```sql
-- Truncate entire employees table
TRUNCATE TABLE employees;
```

**Output:** Table emptied of all rows.

### 4.3.2 MERGE (Upsert) Patterns

```sql
-- Merge new order into orders table
MERGE INTO orders AS tgt
USING (VALUES (5001, 3, 300.00)) AS src(order_id, customer_id, total_amount)
ON tgt.order_id = src.order_id
WHEN MATCHED THEN
  UPDATE SET total_amount = src.total_amount
WHEN NOT MATCHED THEN
  INSERT (order_id, customer_id, total_amount)
  VALUES (src.order_id, src.customer_id, src.total_amount);
```

**Output (orders after merge):**

```
order_id | customer_id | total_amount | status
5001     | 3           | 300.00       | PENDING  -- updated
```

## 4.4 Transactional DML

### 4.4.1 Savepoints & Nested Transactions

```sql
BEGIN;
INSERT INTO orders (order_id, customer_id, total_amount)
VALUES (5002, 4, 150.00);

SAVEPOINT sp1;

-- Faulty insert
INSERT INTO order_items (order_id, item_number, product_id, quantity, unit_price)
VALUES (5002, 1, 999, 1, 10.00);  -- product_id 999 does not exist

ROLLBACK TO SAVEPOINT sp1;

-- Correct insert
INSERT INTO order_items (order_id, item_number, product_id, quantity, unit_price)
VALUES (5002, 1, 501, 2, 25.99);

COMMIT;
```

**Output:**

- Order 5002 committed with valid item; faulty insert discarded.

### 4.4.2 Error Handling and Rollbacks

```sql
BEGIN;
SAVEPOINT sp2;

INSERT INTO employees (emp_id, first_name, last_name, department, salary)
VALUES (202, 'Duplicate', 'User', 'IT', 70000); -- duplicate emp_id

ROLLBACK TO SAVEPOINT sp2;

-- Correct the emp_id
INSERT INTO employees (emp_id, first_name, last_name, department, salary)
VALUES (208, 'Ethan', 'Martinez', 'IT', 70000);

COMMIT;
```

**Output:**

- Duplicate insert rolled back; corrected insert committed.

## 4.5 Temporary Objects

### 4.5.1 Temporary Tables and Table Variables

```sql
-- Create temp table for high-value orders
CREATE TEMPORARY TABLE temp_high_orders AS
SELECT order_id, total_amount
FROM orders
WHERE total_amount > 200.00;
```

**Output (`temp_high_orders` contents):**

```
order_id | total_amount
5001     | 300.00
```

### 4.5.2 CTEs vs Temp Tables Trade-offs

```sql
-- Using CTE
WITH high_orders AS (
  SELECT order_id, total_amount
  FROM orders
  WHERE total_amount > 200.00
)
SELECT * FROM high_orders;

-- Using temp table
CREATE TEMP TABLE high_orders AS
SELECT order_id, total_amount
FROM orders
WHERE total_amount > 200.00;

SELECT * FROM high_orders;
```

**Output (both methods):**

```
order_id | total_amount
5001     | 300.00
```
