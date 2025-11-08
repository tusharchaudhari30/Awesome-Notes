# Chapter 14: Views, Materialized Views & Stored Procedures

Views provide logical abstractions over tables, allowing queries to reference predefined result sets. Materialized views cache results physically for fast access. Stored procedures encapsulate business logic in reusable, server-side routines. Together, they improve modularity, security, and performance while reducing client-side complexity.

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
dept_id | dept_name | budget
1       | Engineering | 500000
2       | Marketing   | 300000

-- salaries_history table
salaries_history:
emp_id | salary | effective_date
101    | 75000  | 2020-01-15
101    | 78000  | 2021-06-01
101    | 80000  | 2023-01-01
102    | 65000  | 2019-06-20
```

---

## 14.1 Views

Views are virtual tables created by queries. They don't store data but execute the underlying query each time accessed.

### 14.1.1 Inline vs Indexed Views

- **Inline Views (Standard Views):** Query runs every access; no persistent storage.
- **Indexed Views (Materialized Views in some systems):** Can have indexes for faster access.

```sql
-- Create an inline view
CREATE VIEW high_earners AS
SELECT emp_id, first_name, last_name, salary
FROM employees
WHERE salary > 75000;

-- Query the view
SELECT * FROM high_earners;

-- Drop the view
DROP VIEW high_earners;
```

**Output:**

```
emp_id | first_name | last_name | salary
101    | Alice      | Johnson   | 80000
```

```sql
-- Create a complex view joining multiple tables
CREATE VIEW dept_employee_summary AS
SELECT
  d.dept_id,
  d.dept_name,
  COUNT(e.emp_id) AS employee_count,
  AVG(e.salary) AS avg_salary,
  MAX(e.salary) AS max_salary
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name;

-- Query the view
SELECT * FROM dept_employee_summary;
```

**Output:**

```
dept_id | dept_name    | employee_count | avg_salary | max_salary
1       | Engineering  | 2              | 77500      | 80000
2       | Marketing    | 1              | 70000      | 70000
```

### 14.1.2 Security & Ownership Chaining

Views enforce access control by exposing only necessary columns/rows.

```sql
-- Create a view to expose only non-sensitive employee data
CREATE VIEW public_employee_info AS
SELECT emp_id, first_name, last_name, dept_id
FROM employees
-- Sensitive columns (salary, hire_date) are hidden

-- Grant SELECT on view but deny direct table access
GRANT SELECT ON public_employee_info TO role_public;
REVOKE SELECT ON employees FROM role_public;

-- Users can query the view but not the underlying table
SELECT * FROM public_employee_info;  -- OK
SELECT salary FROM employees;         -- DENIED
```

---

## 14.2 Materialized Views

Materialized views physically store results and must be refreshed to stay current.

### 14.2.1 Refresh Options: On Commit/Interval/Manual

- **On Commit:** Refreshed automatically when base tables change.
- **On Interval:** Refreshed periodically (every N hours).
- **Manual:** Refreshed on demand by administrator.

```sql
-- Oracle syntax: Create materialized view with refresh strategy
CREATE MATERIALIZED VIEW dept_salary_summary
REFRESH COMPLETE ON COMMIT
AS
SELECT
  d.dept_id,
  d.dept_name,
  SUM(e.salary) AS total_salary,
  COUNT(e.emp_id) AS emp_count
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name;

-- Query the materialized view (accesses cached data)
SELECT * FROM dept_salary_summary;
```

**Output (stored physically):**

```
dept_id | dept_name    | total_salary | emp_count
1       | Engineering  | 155000       | 2
2       | Marketing    | 70000        | 1
```

```sql
-- Periodic refresh (PostgreSQL using pg_materialized_views)
CREATE MATERIALIZED VIEW mv_employee_stats AS
SELECT
  dept_id,
  COUNT(*) AS emp_count,
  AVG(salary) AS avg_salary
FROM employees
GROUP BY dept_id;

-- Refresh on schedule (using cron or scheduler)
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_employee_stats;
```

### 14.2.2 Storage and Staleness Trade-Offs

Materialized views trade freshness for speed. Updates incur refresh costs; stale data may be acceptable for reporting.

```sql
-- Example: Real-time sales dashboard (use regular view)
CREATE VIEW live_sales AS
SELECT sale_id, emp_id, amount, sale_date
FROM sales
WHERE sale_date >= CURRENT_DATE - INTERVAL '7 days';

-- Example: Monthly revenue report (materialized view acceptable)
CREATE MATERIALIZED VIEW mv_monthly_revenue AS
SELECT
  DATE_TRUNC('month', sale_date)::DATE AS month,
  SUM(amount) AS total_revenue
FROM sales
GROUP BY DATE_TRUNC('month', sale_date);
-- Refresh nightly; reports update daily
```

---

## 14.3 Stored Procedures & Functions

Stored procedures are precompiled routines executing business logic on the server, reducing network overhead and improving security.

### 14.3.1 Parameters, Overloading, Error Handling

```sql
-- Basic stored procedure (SQL Server syntax)
CREATE PROCEDURE sp_give_raise
  @emp_id INT,
  @raise_percent DECIMAL(5,2),
  @new_salary DECIMAL(10,2) OUTPUT
AS
BEGIN
  BEGIN TRY
    UPDATE employees
    SET salary = salary * (1 + @raise_percent / 100)
    WHERE emp_id = @emp_id;

    SELECT @new_salary = salary FROM employees WHERE emp_id = @emp_id;
  END TRY
  BEGIN CATCH
    PRINT ERROR_MESSAGE();
    RETURN -1;
  END CATCH
END;

-- Call the procedure
DECLARE @new_sal DECIMAL(10,2);
EXEC sp_give_raise @emp_id = 101, @raise_percent = 5.0, @new_salary = @new_sal OUTPUT;
SELECT @new_sal;
```

**Output:**

```
new_salary
84000.00
```

```sql
-- Stored function (PostgreSQL syntax)
CREATE OR REPLACE FUNCTION get_employee_bonus(emp_id INT)
RETURNS DECIMAL(10,2) AS $$
DECLARE
  base_salary DECIMAL(10,2);
  bonus DECIMAL(10,2);
BEGIN
  SELECT salary INTO base_salary FROM employees WHERE emp_id = get_employee_bonus.emp_id;

  IF base_salary IS NULL THEN
    RAISE EXCEPTION 'Employee not found';
  END IF;

  bonus := base_salary * 0.1;  -- 10% bonus
  RETURN bonus;
END;
$$ LANGUAGE plpgsql;

-- Call the function
SELECT get_employee_bonus(101);
```

**Output:**

```
get_employee_bonus
8000.00
```

### 14.3.2 Transaction Scope and Side-Effects

Stored procedures execute in their own transaction context; changes persist unless explicitly rolled back.

```sql
-- Procedure with multi-step transaction
CREATE PROCEDURE sp_transfer_funds
  @from_account INT,
  @to_account INT,
  @amount DECIMAL(10,2)
AS
BEGIN
  BEGIN TRANSACTION;

  BEGIN TRY
    UPDATE accounts SET balance = balance - @amount WHERE account_id = @from_account;
    UPDATE accounts SET balance = balance + @amount WHERE account_id = @to_account;
    COMMIT;
  END TRY
  BEGIN CATCH
    ROLLBACK;
    THROW;
  END CATCH
END;

EXEC sp_transfer_funds @from_account = 101, @to_account = 202, @amount = 500;
```

**Output:** Both account updates succeed together, or both rollback on error.

---

## 14.4 MERGE/Upsert Patterns

MERGE combines INSERT, UPDATE, and DELETE into a single atomic operation, useful for synchronizing data.

```sql
-- SQL Server MERGE syntax
MERGE INTO employees AS target
USING (
  VALUES
    (105, 'Eve', 'Miller', 3, 72000),
    (101, 'Alice', 'Johnson', 1, 85000)  -- Update Alice's salary
) AS source(emp_id, first_name, last_name, dept_id, salary)
ON target.emp_id = source.emp_id

WHEN MATCHED THEN
  UPDATE SET first_name = source.first_name,
             last_name = source.last_name,
             dept_id = source.dept_id,
             salary = source.salary

WHEN NOT MATCHED THEN
  INSERT (emp_id, first_name, last_name, dept_id, salary)
  VALUES (source.emp_id, source.first_name, source.last_name, source.dept_id, source.salary);
```

**Output:**

```
-- emp_id 101 updated (Alice's salary increased)
-- emp_id 105 inserted (Eve is new)
```

---

## Summary

- **Views** provide logical abstractions, security boundaries, and reusable queries without storage overhead.
- **Materialized Views** cache results for fast access, ideal for reporting and analytics.
- **Stored Procedures** encapsulate business logic, reduce network traffic, and enforce consistency.
- **MERGE** statements atomically synchronize data across systems.

These database objects are foundational for building maintainable, secure, and performant applications.

_End of Chapter 14_
