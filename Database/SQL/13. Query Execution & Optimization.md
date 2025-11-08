# Chapter 13: Query Execution & Optimization

Query execution and optimization is the process by which a database engine transforms SQL statements into an efficient sequence of physical operations. The query optimizer's goal is to find the fastest execution plan among many possible alternatives by analyzing statistics, constraints, and available indexes. Understanding how queries are parsed, optimized, and executed enables developers to write faster queries and diagnose performance issues.

---

## Input Tables

```sql
-- employees table
employees:
emp_id | first_name | last_name | dept_id | salary | hire_date
101    | Alice      | Johnson   | 1       | 80000  | 2020-01-15
102    | Bob        | Wilson    | 2       | 70000  | 2019-06-20
103    | Carol      | Davis     | 1       | 75000  | 2021-03-10
104    | Dave       | Brown     | NULL    | 65000  | 2022-11-05

-- departments table
departments:
dept_id | dept_name
1       | Engineering
2       | Marketing

-- sales table
sales:
sale_id | emp_id | amount | sale_date
5001    | 101    | 1500   | 2024-01-10
5002    | 101    | 1200   | 2024-01-12
5003    | 102    | 2000   | 2024-01-15
5004    | 103    | 1800   | 2024-01-18
```

---

## 13.1 Execution Phases

Query execution involves three main phases: **parsing**, **optimization**, and **execution**.

### 13.1.1 Parsing & Validation

The SQL statement is parsed to check syntax and validate table/column references. The parser builds a logical parse tree representing the query structure.

```sql
-- Valid parse
SELECT e.first_name, d.dept_name
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
WHERE e.salary > 75000;

-- Invalid parse (syntax error)
SELECT e.first_name, d.dept_name
FROM employees e
JINN departments d ON e.dept_id = d.dept_id;
-- ERROR: Unrecognized keyword 'JINN'
```

### 13.1.2 Optimization & Plan Generation

The optimizer analyzes table statistics, indexes, and constraints to devise multiple candidate plans, then estimates costs for each.

```sql
-- Optimizer considers:
-- 1. Full table scan on employees
-- 2. Index seek on salary column (if available)
-- 3. Order of joins (employees first or departments first)
-- 4. Join algorithms (nested loop, hash join, merge join)

EXPLAIN SELECT e.first_name, d.dept_name
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
WHERE e.salary > 75000;
```

**Output (EXPLAIN plan):**

```
Seq Scan on employees e  (cost=0.00..35.00 rows=2)
  Filter: (salary > 75000)
  ->  Hash Join  (cost=12.00..25.00 rows=2)
        ->  Seq Scan on departments d  (cost=0.00..10.00 rows=2)
        ->  Hash  (cost=5.00..5.00 rows=100)
```

### 13.1.3 Execution & Result Retrieval

The optimizer's chosen plan is executed step-by-step, fetching rows and applying filters/joins, ultimately returning results to the client.

---

## 13.2 Plans & Join Algorithms

### 13.2.1 Logical vs Physical Operators

- **Logical operators** describe abstract operations (filter, join, aggregate).
- **Physical operators** are concrete implementations (index seek, nested loop join, hash aggregate).

```text
Logical Plan:
  Project [first_name, dept_name]
    Join [e.dept_id = d.dept_id]
      Filter [salary > 75000]
        Scan employees e
      Scan departments d

Physical Plan:
  Project [first_name, dept_name]
    Hash Join [e.dept_id = d.dept_id]
      Filter [salary > 75000]
        Index Seek on idx_employees_salary
      Table Scan departments d
```

### 13.2.2 Nested Loop, Hash, Merge Joins

- **Nested Loop Join** iterates outer row, probes inner for matches. Low memory, suitable for small result sets.

```sql
FOR EACH row in outer table
  FOR EACH row in inner table
    IF join condition matches, emit row
```

- **Hash Join** builds hash table of inner table, probes with outer rows. Memory-intensive but fast for large tables.

```sql
HASH_TABLE = Hash(inner_table on join_key)
FOR EACH row in outer_table
  PROBE HASH_TABLE(outer_row.join_key)
  IF match found, emit row
```

- **Merge Join** works on pre-sorted input. Efficient when data is already ordered.

```sql
SORT outer_table on join_key
SORT inner_table on join_key
MERGE both sorted streams, emitting matches
```

**Output comparison:**

```
Query: SELECT * FROM employees e
       JOIN sales s ON e.emp_id = s.emp_id

Nested Loop (1,000 employees × 10,000 sales = 10M comparisons)
Hash Join (build hash of 10,000 sales, probe with 1,000 employees = ~11K operations)
Merge Join (sort both tables once, then stream = ~11K operations)
```

---

## 13.3 Hints & Rewriting

### 13.3.1 Index and Join Hints

Hints force the optimizer to use specific strategies when you know better than the optimizer.

```sql
-- SQL Server: Force index usage
SELECT /*+ FORCESEEK(employees idx_emp_salary) */
  first_name, salary
FROM employees
WHERE salary > 75000;

-- PostgreSQL: Force join type
SELECT /*+ HASHJOIN(e s) */
  e.first_name, s.amount
FROM employees e
JOIN sales s ON e.emp_id = s.emp_id;
```

### 13.3.2 Query Refactoring Patterns

Rewrite queries for better optimizer decisions.

```sql
-- Inefficient: function on indexed column prevents index use
SELECT * FROM employees WHERE YEAR(hire_date) = 2020;

-- Optimized: SARGable range predicate
SELECT * FROM employees
WHERE hire_date >= '2020-01-01' AND hire_date < '2021-01-01';

-- Inefficient: OR condition prevents index usage
SELECT * FROM employees WHERE dept_id = 1 OR dept_id = 2;

-- Optimized: IN clause or JOIN
SELECT * FROM employees WHERE dept_id IN (1, 2);
```

---

## 13.4 Engine-Specific Top-N & Pagination

### 13.4.1 LIMIT/OFFSET, TOP, FETCH FIRST

Different SQL engines provide different syntax for pagination.

```sql
-- PostgreSQL/MySQL: LIMIT/OFFSET
SELECT first_name, salary FROM employees
ORDER BY salary DESC
LIMIT 10 OFFSET 20;  -- Skip 20, get next 10

-- SQL Server: TOP
SELECT TOP 10 first_name, salary FROM employees
ORDER BY salary DESC;

-- Oracle/PostgreSQL: FETCH FIRST
SELECT first_name, salary FROM employees
ORDER BY salary DESC
FETCH FIRST 10 ROWS ONLY;
OFFSET 20 ROWS;
```

**Output (all return the 21st to 30th highest-paid employees):**

```
first_name | salary
...        | ...
```

### 13.4.2 Keyset Pagination for Performance

OFFSET is slow on large result sets. Keyset pagination uses the last row's key to fetch the next batch.

```sql
-- Inefficient pagination for large offsets
SELECT * FROM sales ORDER BY sale_id LIMIT 10 OFFSET 1000000;

-- Efficient keyset pagination
-- First page:
SELECT * FROM sales ORDER BY sale_id LIMIT 10;

-- Next page (pass last_sale_id from previous page):
SELECT * FROM sales
WHERE sale_id > :last_sale_id
ORDER BY sale_id LIMIT 10;
```

**Output:**

- Keyset approach skips the expensive OFFSET calculation.

---

## 13.5 Statistics Management

### 13.5.1 Auto-Stats and Stale Statistics Issues

Statistics track row counts, value distributions, and index selectivity. Stale stats cause poor plan choices.

```sql
-- Update statistics manually when they're stale
ANALYZE TABLE employees;  -- MySQL
ANALYZE employees;        -- Oracle
ANALYZE TABLE employees;  -- SQL Server

-- Check statistics age
SELECT * FROM sys.dm_db_stats_info
WHERE object_id = OBJECT_ID('employees');
```

### 13.5.2 Cardinality Estimation Pitfalls

Inaccurate row count predictions lead to suboptimal join orders and plan choices.

```sql
-- Complex predicate (stats uncertain)
SELECT * FROM sales
WHERE amount > 1000 AND emp_id IN (SELECT emp_id FROM employees WHERE dept_id = 1);
-- Optimizer may misestimate result size, choosing wrong join order

-- Simplify and restructure for clearer cardinality
WITH dept_emps AS (
  SELECT emp_id FROM employees WHERE dept_id = 1
)
SELECT s.* FROM sales s
JOIN dept_emps de ON s.emp_id = de.emp_id
WHERE s.amount > 1000;
```

---

## Summary

Understanding query execution and optimization enables:

- Writing SARGable, index-friendly queries
- Choosing appropriate join algorithms for your data
- Using pagination effectively at scale
- Diagnosing performance bottlenecks via EXPLAIN plans
- Maintaining accurate statistics for consistent performance

A well-optimized query can execute 10-100x faster than an unoptimized one—making this knowledge invaluable for building responsive systems.
