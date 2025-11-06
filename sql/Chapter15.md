# Chapter 15: Triggers & User-Defined Functions

Triggers are database objects that automatically execute code in response to specific events (INSERT, UPDATE, DELETE) on a table. User-defined functions (UDFs) encapsulate reusable logic that can be called from queries. Together, they enable sophisticated automation, data validation, audit logging, and complex calculations at the database level.

---

## Input Tables

```sql
-- employees table
employees:
emp_id | first_name | last_name | salary | hire_date
101    | Alice      | Johnson   | 80000  | 2020-01-15
102    | Bob        | Wilson    | 70000  | 2019-06-20
103    | Carol      | Davis     | 75000  | 2021-03-10

-- salary_audit table (for audit logging)
salary_audit:
audit_id | emp_id | old_salary | new_salary | change_date | changed_by
(empty initially)

-- departments table
departments:
dept_id | dept_name | manager_id
1       | Engineering | NULL
2       | Marketing   | NULL
```

---

## 15.1 Triggers

Triggers execute automatically when specified DML events occur. They enforce business rules and maintain data integrity at the database level.

### 15.1.1 BEFORE, AFTER, INSTEAD OF Triggers

- **BEFORE Trigger:** Executes before the triggering event; can validate/modify data before insertion.
- **AFTER Trigger:** Executes after the event; useful for logging and cascading updates.
- **INSTEAD OF Trigger:** Replaces the triggering event; commonly used to make views updatable.

```sql
-- BEFORE INSERT trigger: validate salary before insertion
CREATE TRIGGER trg_validate_salary_before_insert
BEFORE INSERT ON employees
FOR EACH ROW
BEGIN
  IF NEW.salary < 30000 THEN
    RAISE EXCEPTION 'Salary must be at least 30000';
  END IF;
END;

-- Attempt to insert employee with low salary
INSERT INTO employees VALUES (104, 'Dave', 'Brown', 25000, CURRENT_DATE);
-- ERROR: Salary must be at least 30000
```

**Output:** Insert rejected; no row added.

```sql
-- AFTER INSERT trigger: log audit trail
CREATE TRIGGER trg_log_employee_insert
AFTER INSERT ON employees
FOR EACH ROW
BEGIN
  INSERT INTO salary_audit (emp_id, old_salary, new_salary, change_date, changed_by)
  VALUES (NEW.emp_id, NULL, NEW.salary, CURRENT_TIMESTAMP, USER());
END;

INSERT INTO employees VALUES (104, 'Dave', 'Brown', 65000, CURRENT_DATE);
```

**Output (salary_audit):**

```
audit_id | emp_id | old_salary | new_salary | change_date           | changed_by
1        | 104    | NULL       | 65000      | 2025-10-23 19:35:00   | dba
```

```sql
-- INSTEAD OF UPDATE trigger: make a view updatable
CREATE VIEW emp_names AS
SELECT emp_id, first_name, last_name FROM employees;

CREATE TRIGGER trg_update_emp_names
INSTEAD OF UPDATE ON emp_names
FOR EACH ROW
BEGIN
  UPDATE employees
  SET first_name = NEW.first_name, last_name = NEW.last_name
  WHERE emp_id = NEW.emp_id;
END;

UPDATE emp_names SET first_name = 'Alicia' WHERE emp_id = 101;
```

**Output:** View update transparently updates the underlying employees table.

### 15.1.2 Row-level vs Statement-level Triggers

- **Row-level:** Fires once per affected row (e.g., 10 rows updated → 10 trigger executions).
- **Statement-level:** Fires once per statement (e.g., 10 rows updated → 1 trigger execution).

```sql
-- Row-level trigger (PostgreSQL syntax)
CREATE TRIGGER trg_salary_history_row
AFTER UPDATE ON employees
FOR EACH ROW
WHEN (OLD.salary <> NEW.salary)
BEGIN
  INSERT INTO salary_audit (emp_id, old_salary, new_salary, change_date)
  VALUES (NEW.emp_id, OLD.salary, NEW.salary, CURRENT_TIMESTAMP);
END;

-- Statement-level trigger
CREATE TRIGGER trg_salary_history_stmt
AFTER UPDATE ON employees
FOR EACH STATEMENT
BEGIN
  INSERT INTO update_log (table_name, updated_rows, log_time)
  VALUES ('employees', ROW_COUNT(), CURRENT_TIMESTAMP);
END;
```

**Performance Consideration:**

- Row-level for detailed audit; statement-level for summaries and bulk operations.

---

## 15.2 User-Defined Functions

UDFs encapsulate reusable logic in scalar or table-valued forms.

### 15.2.1 Scalar, Inline Table, Multi-Statement Functions

**Scalar UDF:** Returns a single value.

```sql
-- Calculate years of service (SQL Server syntax)
CREATE FUNCTION fn_years_of_service(@hire_date DATE)
RETURNS INT
AS
BEGIN
  RETURN DATEDIFF(YEAR, @hire_date, GETDATE());
END;

SELECT emp_id, first_name, dbo.fn_years_of_service(hire_date) AS years_served
FROM employees;
```

**Output:**

```
emp_id | first_name | years_served
101    | Alice      | 5
102    | Bob        | 6
103    | Carol      | 4
```

**Inline Table-Valued Function:** Returns result set from a single SELECT.

```sql
-- Get employees earning above threshold (PostgreSQL syntax)
CREATE FUNCTION fn_high_earners(threshold DECIMAL)
RETURNS TABLE(emp_id INT, first_name VARCHAR, salary DECIMAL) AS $$
  SELECT emp_id, first_name, salary FROM employees WHERE salary > threshold;
$$ LANGUAGE SQL;

SELECT * FROM fn_high_earners(75000);
```

**Output:**

```
emp_id | first_name | salary
101    | Alice      | 80000
103    | Carol      | 75000
```

**Multi-Statement Table-Valued Function:** Complex logic with loops/conditions.

```sql
-- Build employee directory with formatting (SQL Server syntax)
CREATE FUNCTION fn_employee_directory()
RETURNS @result TABLE(
  emp_id INT,
  full_name VARCHAR(100),
  status VARCHAR(50),
  years_service INT
)
AS
BEGIN
  INSERT INTO @result
  SELECT
    emp_id,
    CONCAT(first_name, ' ', last_name),
    CASE WHEN DATEDIFF(YEAR, hire_date, GETDATE()) > 5 THEN 'Senior' ELSE 'Junior' END,
    DATEDIFF(YEAR, hire_date, GETDATE())
  FROM employees;
  RETURN;
END;

SELECT * FROM dbo.fn_employee_directory();
```

**Output:**

```
emp_id | full_name       | status | years_service
101    | Alice Johnson   | Senior | 5
102    | Bob Wilson      | Senior | 6
103    | Carol Davis     | Junior | 4
```

### 15.2.2 Deterministic vs Non-Deterministic Functions

- **Deterministic:** Always returns same output for same input (e.g., `SQRT(4)` → 2).
- **Non-Deterministic:** Output depends on external state (e.g., `GETDATE()`, `RAND()`).

```sql
-- Deterministic function (can be indexed in some DBs for optimization)
CREATE FUNCTION fn_bonus_percentage(@salary DECIMAL)
RETURNS DECIMAL
DETERMINISTIC
AS
BEGIN
  RETURN @salary * 0.1;  -- Always 10% of input
END;

-- Non-deterministic function (cannot be indexed)
CREATE FUNCTION fn_random_bonus(@base DECIMAL)
RETURNS DECIMAL
NOT DETERMINISTIC
AS
BEGIN
  RETURN @base + RAND() * 1000;  -- Different each call
END;
```

---

## 15.3 Audit & Automation Patterns

### 15.3.1 Change Logging Strategies

Track all data modifications for compliance, debugging, and audit trails.

```sql
-- Comprehensive audit table
CREATE TABLE audit_log (
  audit_id INT IDENTITY(1,1),
  table_name VARCHAR(50),
  operation VARCHAR(10),  -- INSERT, UPDATE, DELETE
  record_id INT,
  old_values VARCHAR(1000),
  new_values VARCHAR(1000),
  changed_by VARCHAR(50),
  changed_at TIMESTAMP
);

-- Generic audit trigger for employees
CREATE TRIGGER trg_audit_employees
AFTER INSERT, UPDATE, DELETE ON employees
FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO audit_log VALUES (
      'employees', 'INSERT', NEW.emp_id,
      NULL,
      CONCAT('emp_id=', NEW.emp_id, ', name=', NEW.first_name, ' ', NEW.last_name),
      USER(), CURRENT_TIMESTAMP
    );
  ELSIF UPDATING THEN
    INSERT INTO audit_log VALUES (
      'employees', 'UPDATE', NEW.emp_id,
      CONCAT('salary=', OLD.salary),
      CONCAT('salary=', NEW.salary),
      USER(), CURRENT_TIMESTAMP
    );
  ELSIF DELETING THEN
    INSERT INTO audit_log VALUES (
      'employees', 'DELETE', OLD.emp_id,
      CONCAT('emp_id=', OLD.emp_id, ', name=', OLD.first_name),
      NULL,
      USER(), CURRENT_TIMESTAMP
    );
  END IF;
END;

-- Query audit history
SELECT * FROM audit_log ORDER BY changed_at DESC;
```

**Output (audit_log):**

```
audit_id | table_name | operation | record_id | old_values | new_values | changed_by | changed_at
1        | employees  | INSERT    | 104       | NULL       | emp_id=104, name=Dave Brown | dba | 2025-10-23 19:40
2        | employees  | UPDATE    | 101       | salary=80000 | salary=82000 | dba | 2025-10-23 19:45
```

### 15.3.2 Pitfalls and Performance Costs

**Common Issues:**

- **Cascading Triggers:** Triggers firing other triggers (loops, cascades).
- **Performance Degradation:** Excessive trigger logic slows writes.
- **Debugging Difficulty:** Side effects hidden from application code.

```sql
-- Anti-pattern: Cascading triggers
CREATE TRIGGER trg_cascade1
AFTER INSERT ON table_a
BEGIN
  INSERT INTO table_b VALUES (...);  -- Fires trg_cascade2
END;

CREATE TRIGGER trg_cascade2
AFTER INSERT ON table_b
BEGIN
  UPDATE table_c SET ...;  -- Complex side effects
END;

-- Result: Hard to trace, difficult to debug

-- Better pattern: Move logic to application or stored procedures
CREATE PROCEDURE sp_insert_related_data(...)
AS
BEGIN
  INSERT INTO table_a VALUES (...);
  INSERT INTO table_b VALUES (...);
  UPDATE table_c SET ...;
  -- All in one controlled routine
END;
```

---

## Best Practices for Triggers & Functions

- **Use triggers sparingly:** Prefer application logic for clarity.
- **Keep triggers simple:** Avoid complex nested logic.
- **Audit with triggers:** Track changes for compliance.
- **Use functions for reusability:** Call from queries and procedures.
- **Test thoroughly:** Triggers hidden from direct visibility.
- **Monitor performance:** Triggers can become bottlenecks.

---

## Summary

Triggers automate responses to data changes, enforce business rules, and maintain audit trails. User-defined functions encapsulate reusable logic for cleaner, more maintainable code. Used judiciously, they enhance database reliability and reduce application complexity.

_End of Chapter 15_
