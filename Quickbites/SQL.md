# Complete SQL Master Cheatsheet: Beginner to Advanced

## **Beginner Level**

### **1. Database Operations**

Creates, selects, or removes databases so subsequent statements run against the correct schema context.

```sql
-- Create Database
CREATE DATABASE company_db;

-- Use Database
USE company_db;

-- Drop Database
DROP DATABASE company_db;
```

**Example Output:**

```
Query OK, 1 row affected
Database changed
Query OK, 0 rows affected
```

### **2. Table Operations**

Defines, modifies, or drops tables and columns, including data types and constraints like primary keys and uniqueness.

```sql
-- Create Table
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    hire_date DATE,
    salary DECIMAL(10,2),
    department_id INT
);

-- Drop Table
DROP TABLE employees;

-- Alter Table
ALTER TABLE employees ADD COLUMN phone VARCHAR(15);
ALTER TABLE employees DROP COLUMN phone;
ALTER TABLE employees MODIFY COLUMN salary DECIMAL(12,2);
```

**Example Output:**

```
Query OK, 0 rows affected
Query OK, 0 rows affected
Query OK, 3 rows affected
```

### **3. Data Manipulation (CRUD)**

Inserts, selects, updates, and deletes rows to manage the contents of tables.

```sql
-- INSERT
INSERT INTO employees (employee_id, first_name, last_name, email, salary)
VALUES (1, 'John', 'Doe', 'john.doe@email.com', 50000);

-- SELECT
SELECT * FROM employees;
SELECT first_name, last_name, salary FROM employees;

-- UPDATE
UPDATE employees
SET salary = 55000
WHERE employee_id = 1;

-- DELETE
DELETE FROM employees WHERE employee_id = 1;
```

**Example Output:**

```
employee_id | first_name | last_name | email              | salary
----------- | ---------- | --------- | ------------------ | -------
1           | John       | Doe       | john.doe@email.com | 50000.00
```

### **4. Basic Filtering & Sorting**

Filters rows with WHERE, de-duplicates with DISTINCT, and orders results with ORDER BY and optional LIMIT/TOP.

```sql
-- WHERE Clause
SELECT * FROM employees WHERE salary > 50000;
SELECT * FROM employees WHERE department_id = 1 AND salary > 45000;

-- ORDER BY
SELECT * FROM employees ORDER BY salary DESC;
SELECT * FROM employees ORDER BY last_name ASC, first_name ASC;

-- DISTINCT
SELECT DISTINCT department_id FROM employees;

-- LIMIT/TOP
SELECT * FROM employees LIMIT 5;  -- MySQL
SELECT TOP 5 * FROM employees;    -- SQL Server
```

**Example Output:**

```
first_name | last_name | salary
---------- | --------- | -------
James      | Wilson    | 70000.00
David      | Jones     | 65000.00
Emma       | Taylor    | 63000.00
```

### **5. Pattern Matching & Ranges**

Uses LIKE for simple wildcard matching, IN for lists, BETWEEN for ranges, and IS NULL checks for missing values.

```sql
-- LIKE
SELECT * FROM employees WHERE first_name LIKE 'J%';    -- Starts with J
SELECT * FROM employees WHERE email LIKE '%@gmail.com'; -- Ends with @gmail.com

-- IN
SELECT * FROM employees WHERE department_id IN (1, 2, 3);

-- BETWEEN
SELECT * FROM employees WHERE salary BETWEEN 40000 AND 60000;

-- IS NULL / IS NOT NULL
SELECT * FROM employees WHERE phone IS NULL;
```

**Example Output:**

```
first_name | email
---------- | --------------------
John       | john.doe@acme.com
James      | james.w@acme.com
```

## **Intermediate Level**

### **6. Aggregate Functions**

Computes COUNT, SUM, AVG, MIN, MAX across rows and groups with GROUP BY and filters aggregated groups using HAVING.

```sql
-- Basic Aggregates
SELECT COUNT(*) FROM employees;
SELECT COUNT(DISTINCT department_id) FROM employees;
SELECT AVG(salary), MIN(salary), MAX(salary), SUM(salary) FROM employees;

-- GROUP BY
SELECT department_id, COUNT(*) as emp_count, AVG(salary) as avg_salary
FROM employees
GROUP BY department_id;

-- HAVING
SELECT department_id, AVG(salary) as avg_salary
FROM employees
GROUP BY department_id
HAVING AVG(salary) > 50000;
```

**Example Output:**

```
department_id | emp_count | avg_salary
------------- | --------- | ----------
3             | 3         | 61000.00
6             | 2         | 68000.00
```

### **7. String Functions**

Common functions include UPPER, LOWER, CONCAT, SUBSTRING, LENGTH, and TRIM for formatting and parsing text columns.

```sql
-- String Manipulation
SELECT UPPER(first_name), LOWER(last_name) FROM employees;
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM employees;
SELECT SUBSTRING(email, 1, 10) FROM employees;  -- First 10 chars
SELECT LENGTH(first_name) FROM employees;
SELECT TRIM(first_name) FROM employees;         -- Remove spaces
```

**Example Output:**

```
display_name
------------
JOHN Doe
JAMES Wilson
DAVID Jones
```

### **8. Date Functions**

Extract parts, compute differences, add intervals, and get current time using functions like YEAR, DATEDIFF, DATE_ADD, CURRENT_DATE, and NOW.

```sql
-- Date Operations
SELECT CURRENT_DATE, CURRENT_TIME, NOW();
SELECT YEAR(hire_date), MONTH(hire_date), DAY(hire_date) FROM employees;
SELECT DATEDIFF(CURRENT_DATE, hire_date) AS days_employed FROM employees;
SELECT DATE_ADD(hire_date, INTERVAL 1 YEAR) AS anniversary FROM employees;
```

**Example Output:**

```
hire_date  | days_employed
---------- | --------------
2020-01-15 | 2100
2019-06-20 | 2300
```

### **9. CASE Statements**

Adds conditional logic to map values to categories or labels inline in SQL projections.

```sql
-- Conditional Logic
SELECT first_name, last_name, salary,
    CASE
        WHEN salary > 60000 THEN 'High'
        WHEN salary > 40000 THEN 'Medium'
        ELSE 'Low'
    END AS salary_category
FROM employees;

-- Simple CASE
SELECT first_name,
    CASE department_id
        WHEN 1 THEN 'IT'
        WHEN 2 THEN 'HR'
        WHEN 3 THEN 'Finance'
        ELSE 'Other'
    END AS department_name
FROM employees;
```

**Example Output:**

```
first_name | salary  | salary_category
---------- | ------- | ---------------
John       | 50000.0 | Medium
James      | 70000.0 | High
Emma       | 63000.0 | High
```

### **10. Joins**

Combines rows across tables by matching keys with INNER, LEFT, RIGHT, FULL, CROSS, and SELF joins for relational analysis.

```sql
-- INNER JOIN
SELECT e.first_name, e.last_name, d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id;

-- LEFT JOIN
SELECT e.first_name, d.department_name
FROM employees e
LEFT JOIN departments d ON e.department_id = d.department_id;

-- RIGHT JOIN
SELECT e.first_name, d.department_name
FROM employees e
RIGHT JOIN departments d ON e.department_id = d.department_id;

-- FULL OUTER JOIN
SELECT e.first_name, d.department_name
FROM employees e
FULL OUTER JOIN departments d ON e.department_id = d.department_id;

-- CROSS JOIN
SELECT e.first_name, d.department_name
FROM employees e
CROSS JOIN departments d;

-- SELF JOIN
SELECT e1.first_name as employee, e2.first_name as manager
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.employee_id;
```

**Example Output:**

```
first_name | department_name
---------- | ---------------
John       | Engineering
James      | IT
David      | Engineering
```

### **11. Subqueries**

Embeds queries inside others for filtering, projections, and existence checks using scalar, IN, EXISTS, and correlated subqueries.

```sql
-- Scalar Subquery
SELECT * FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Correlated Subquery
SELECT e1.first_name, e1.salary
FROM employees e1
WHERE salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.department_id = e1.department_id
);

-- EXISTS
SELECT * FROM employees e
WHERE EXISTS (
    SELECT 1 FROM departments d
    WHERE d.department_id = e.department_id
);

-- IN Subquery
SELECT * FROM employees
WHERE department_id IN (
    SELECT department_id FROM departments
    WHERE location = 'New York'
);
```

**Example Output:**

```
first_name | salary
---------- | -------
James      | 70000.00
David      | 65000.00
Emma       | 63000.00
```

### **12. Set Operations**

Combines result sets with UNION, UNION ALL, INTERSECT, and EXCEPT to deduplicate, stack, or compare row sets.

```sql
-- UNION
SELECT first_name FROM employees WHERE department_id = 1
UNION
SELECT first_name FROM employees WHERE department_id = 2;

-- UNION ALL
SELECT first_name FROM employees WHERE department_id = 1
UNION ALL
SELECT first_name FROM employees WHERE department_id = 2;

-- INTERSECT
SELECT employee_id FROM project_assignments
INTERSECT
SELECT employee_id FROM training_records;

-- EXCEPT
SELECT employee_id FROM employees
EXCEPT
SELECT employee_id FROM project_assignments;
```

**Example Output:**

```
first_name
----------
John
Michael
William
James
Matthew
```

## **Advanced Level**

### **13. Basic Window Functions**

Performs calculations like rankings, running totals, and time offsets across a window of rows without collapsing results using OVER with PARTITION BY and ORDER BY.

```sql
-- ROW_NUMBER
SELECT first_name, salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num
FROM employees;

-- RANK and DENSE_RANK
SELECT first_name, salary,
    RANK() OVER (ORDER BY salary DESC) as rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank
FROM employees;

-- PARTITION BY
SELECT first_name, department_id, salary,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) as dept_rank
FROM employees;

-- LAG and LEAD
SELECT first_name, salary,
    LAG(salary) OVER (ORDER BY hire_date) as prev_salary,
    LEAD(salary) OVER (ORDER BY hire_date) as next_salary
FROM employees;

-- FIRST_VALUE and LAST_VALUE
SELECT first_name, salary,
    FIRST_VALUE(salary) OVER (ORDER BY salary DESC) as highest_salary,
    LAST_VALUE(salary) OVER (ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as lowest_salary
FROM employees;

-- Running Total
SELECT first_name, salary,
    SUM(salary) OVER (ORDER BY hire_date ROWS UNBOUNDED PRECEDING) as running_total
FROM employees;

-- Moving Average
SELECT first_name, salary,
    AVG(salary) OVER (ORDER BY hire_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg
FROM employees;
```

**Example Output:**

```
first_name | salary  | row_num | rank | dense_rank
---------- | ------- | ------- | ---- | ----------
James      | 70000.0 | 1       | 1    | 1
David      | 65000.0 | 2       | 2    | 2
Emma       | 63000.0 | 3       | 3    | 3
```

### **14. Distribution Window Functions**

Computes relative rank and cumulative distribution metrics useful for percentiles and statistical analysis.

```sql
-- PERCENT_RANK
SELECT first_name, salary,
       PERCENT_RANK() OVER (ORDER BY salary) AS pct_rank
FROM employees
ORDER BY salary
LIMIT 5;

-- CUME_DIST
SELECT first_name, salary,
       CUME_DIST() OVER (ORDER BY salary) AS cum_dist
FROM employees
ORDER BY salary
LIMIT 5;

-- NTILE
SELECT first_name, salary,
       NTILE(4) OVER (ORDER BY salary) AS quartile
FROM employees
ORDER BY salary;

-- Distribution comparison
SELECT first_name, salary,
  ROW_NUMBER()  OVER (ORDER BY salary DESC) AS rownum,
  RANK()        OVER (ORDER BY salary DESC) AS rnk,
  DENSE_RANK()  OVER (ORDER BY salary DESC) AS drnk,
  PERCENT_RANK() OVER (ORDER BY salary DESC) AS pct,
  CUME_DIST()    OVER (ORDER BY salary DESC) AS cdist
FROM employees
ORDER BY salary DESC;
```

**Example Output:**

```
first_name | salary  | pct_rank | cum_dist | quartile
---------- | ------- | -------- | -------- | --------
John       | 42000.0 | 0.00     | 0.04     | 1
Ava        | 45000.0 | 0.05     | 0.10     | 1
Noah       | 47000.0 | 0.12     | 0.16     | 1
Mia        | 48000.0 | 0.16     | 0.19     | 2
```

### **15. NTH_VALUE and Offset Functions**

Returns the nth value within the frame and provides advanced offset capabilities for accessing specific rows.

```sql
-- NTH_VALUE
SELECT first_name, salary,
       NTH_VALUE(salary, 3) OVER (ORDER BY salary
          ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS third_lowest
FROM employees
ORDER BY salary;

-- NTH_VALUE with PARTITION
SELECT department_id, first_name, salary,
       NTH_VALUE(salary, 2) OVER (
         PARTITION BY department_id
         ORDER BY salary DESC
         ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS second_highest_in_dept
FROM employees
ORDER BY department_id, salary DESC;

-- Advanced LAG/LEAD with defaults
SELECT first_name, hire_date, salary,
  LAG(salary, 2, 0) OVER (ORDER BY hire_date) AS salary_2_periods_ago,
  LEAD(salary, 1, salary) OVER (ORDER BY hire_date) AS next_salary_or_current
FROM employees;
```

**Example Output:**

```
department_id | first_name | salary  | second_highest_in_dept
------------- | ---------- | ------- | ----------------------
3             | James      | 70000.0 | 65000.0
3             | David      | 65000.0 | 65000.0
3             | John       | 50000.0 | 65000.0
```

### **16. Window Frames: ROWS vs RANGE vs GROUPS**

Controls which rows the window function sees relative to the current row, with different behaviors for ties and offsets.

```sql
-- ROWS Frame (physical rows)
SELECT first_name, salary,
  AVG(salary) OVER (ORDER BY salary
                    ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING) AS avg_5_rows
FROM employees;

-- RANGE Frame (value-based)
SELECT first_name, salary,
  AVG(salary) OVER (ORDER BY salary
                    RANGE BETWEEN 5000 PRECEDING AND 5000 FOLLOWING) AS avg_salary_range
FROM employees;

-- Compare ROWS vs RANGE with ties
SELECT first_name, salary,
  AVG(salary) OVER (ORDER BY salary
                    ROWS  BETWEEN 2 PRECEDING AND CURRENT ROW) AS avg_rows,
  AVG(salary) OVER (ORDER BY salary
                    RANGE BETWEEN CURRENT ROW AND CURRENT ROW) AS avg_range
FROM employees
WHERE salary IN (50000, 50000, 50000, 61000, 61000)
ORDER BY salary, first_name;

-- GROUPS Frame (peer groups)
SELECT first_name, salary,
  COUNT(*) OVER (ORDER BY salary
                 GROUPS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS peer_group_count
FROM employees;
```

**Example Output:**

```
first_name | salary  | avg_rows | avg_range
---------- | ------- | -------- | ---------
John       | 50000.0 | 50000.0  | 50000.0
Jane       | 50000.0 | 50000.0  | 50000.0
Jim        | 50000.0 | 50000.0  | 50000.0
Will       | 61000.0 | 57333.3  | 61000.0
```

### **17. Advanced Window Frames with EXCLUDE**

Excludes specific rows from the frame calculation (PostgreSQL and SQL:2011 compliant engines).

```sql
-- EXCLUDE CURRENT ROW
SELECT first_name, salary,
  AVG(salary) OVER (
    ORDER BY salary
    RANGE BETWEEN 1000 PRECEDING AND 1000 FOLLOWING
    EXCLUDE CURRENT ROW
  ) AS avg_neighbors
FROM employees;

-- EXCLUDE TIES
SELECT first_name, salary,
  COUNT(*) OVER (
    ORDER BY salary
    RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    EXCLUDE TIES
  ) AS count_excluding_ties
FROM employees;

-- EXCLUDE GROUP
SELECT first_name, salary,
  SUM(salary) OVER (
    PARTITION BY department_id
    ORDER BY salary
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    EXCLUDE GROUP
  ) AS sum_excluding_peer_group
FROM employees;
```

**Example Output:**

```
first_name | salary  | avg_neighbors
---------- | ------- | -------------
John       | 50000.0 | 50500.0
Jane       | 50000.0 | 50500.0
Jim        | 50000.0 | 50500.0
Jill       | 51000.0 | 50000.0
```

### **18. Windowed Aggregates per Group**

Aggregates applied per partition without collapsing rows, yielding per-group totals, mins, maxes alongside each row.

```sql
-- Per-partition aggregates
SELECT department_id, first_name, salary,
       SUM(salary) OVER (PARTITION BY department_id) AS dept_total,
       MIN(salary) OVER (PARTITION BY department_id) AS dept_min,
       MAX(salary) OVER (PARTITION BY department_id) AS dept_max,
       COUNT(*) OVER (PARTITION BY department_id) AS dept_count
FROM employees
ORDER BY department_id, salary DESC;

-- Running totals within partitions
SELECT department_id, first_name, hire_date, salary,
  SUM(salary) OVER (
    PARTITION BY department_id
    ORDER BY hire_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_dept_total
FROM employees
ORDER BY department_id, hire_date;
```

**Example Output:**

```
department_id | first_name | salary  | dept_total | dept_min | dept_max | dept_count
------------- | ---------- | ------- | ---------- | -------- | -------- | ----------
3             | James      | 70000.0 | 185000.0   | 50000.0  | 70000.0  | 3
3             | David      | 65000.0 | 185000.0   | 50000.0  | 70000.0  | 3
3             | John       | 50000.0 | 185000.0   | 50000.0  | 70000.0  | 3
```

### **19. Common Table Expressions (CTEs)**

Defines named, reusable subqueries with WITH for clarity, multi-step logic, and easier composition of complex queries.

```sql
-- Basic CTE
WITH high_earners AS (
    SELECT * FROM employees WHERE salary > 60000
)
SELECT department_id, COUNT(*) as high_earner_count
FROM high_earners
GROUP BY department_id;

-- Multiple CTEs
WITH dept_avg AS (
    SELECT department_id, AVG(salary) as avg_salary
    FROM employees
    GROUP BY department_id
),
dept_names AS (
    SELECT department_id, department_name
    FROM departments
)
SELECT dn.department_name, da.avg_salary
FROM dept_avg da
JOIN dept_names dn ON da.department_id = dn.department_id;

-- CTE with window functions
WITH ranked_employees AS (
    SELECT first_name, department_id, salary,
           ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) as dept_rank
    FROM employees
)
SELECT * FROM ranked_employees WHERE dept_rank <= 2;
```

**Example Output:**

```
department_id | high_earner_count
------------- | -----------------
3             | 2
6             | 2
```

### **20. Recursive CTEs**

Uses WITH RECURSIVE to traverse hierarchies or generate sequences by repeatedly referencing the CTE until a termination condition.

```sql
-- Employee Hierarchy
WITH RECURSIVE employee_hierarchy AS (
    -- Anchor member: Top-level managers
    SELECT employee_id, first_name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive member: Direct reports
    SELECT e.employee_id, e.first_name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
)
SELECT employee_id, first_name, level
FROM employee_hierarchy
ORDER BY level, first_name;

-- Number Series
WITH RECURSIVE number_series AS (
    SELECT 1 as num
    UNION ALL
    SELECT num + 1
    FROM number_series
    WHERE num < 10
)
SELECT * FROM number_series;

-- Factorial Calculation
WITH RECURSIVE factorial_cte(n, factorial) AS (
    SELECT 1, 1  -- Base case
    UNION ALL
    SELECT n + 1, (n + 1) * factorial
    FROM factorial_cte
    WHERE n < 5
)
SELECT n, factorial FROM factorial_cte;

-- Date Series
WITH RECURSIVE date_series AS (
    SELECT DATE '2025-01-01' as dt
    UNION ALL
    SELECT dt + INTERVAL '1 day'
    FROM date_series
    WHERE dt < DATE '2025-01-10'
)
SELECT dt FROM date_series;
```

**Example Output:**

```
employee_id | first_name | level
----------- | ---------- | -----
1           | Alice      | 1
2           | John       | 2
3           | Emma       | 2
4           | James      | 2
5           | Sarah      | 3
```

### **21. Advanced Joins & Complex Queries**

Chains multiple joins and applies conditional join predicates to filter related tables efficiently during the join step.

```sql
-- Multiple Joins
SELECT e.first_name, d.department_name, p.project_name, s.skill_name
FROM employees e
JOIN departments d ON e.department_id = d.department_id
JOIN employee_projects ep ON e.employee_id = ep.employee_id
JOIN projects p ON ep.project_id = p.project_id
JOIN employee_skills es ON e.employee_id = es.employee_id
JOIN skills s ON es.skill_id = s.skill_id;

-- Conditional Joins
SELECT e.first_name, e.salary, b.bonus_amount
FROM employees e
LEFT JOIN bonuses b ON e.employee_id = b.employee_id
    AND b.year = YEAR(CURRENT_DATE);

-- Anti-Join (find employees without projects)
SELECT e.first_name
FROM employees e
LEFT JOIN employee_projects ep ON e.employee_id = ep.employee_id
WHERE ep.employee_id IS NULL;

-- Complex join with aggregation
SELECT d.department_name,
       COUNT(e.employee_id) as emp_count,
       AVG(e.salary) as avg_salary,
       COUNT(DISTINCT p.project_id) as active_projects
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
LEFT JOIN employee_projects ep ON e.employee_id = ep.employee_id
LEFT JOIN projects p ON ep.project_id = p.project_id
    AND p.status = 'Active'
GROUP BY d.department_id, d.department_name;
```

**Example Output:**

```
first_name | project_name | skill_name
---------- | ------------ | ----------
John       | Apollo       | Python
Michael    | Apollo       | Java
William    | Hermes       | JavaScript
```

### **22. Views**

Creates logical, reusable named queries that simplify complex joins or enforce column-level security as virtual tables.

```sql
-- Create View
CREATE VIEW employee_summary AS
SELECT
    e.employee_id,
    CONCAT(e.first_name, ' ', e.last_name) as full_name,
    d.department_name,
    e.salary,
    CASE
        WHEN e.salary > 60000 THEN 'Senior'
        ELSE 'Junior'
    END as level
FROM employees e
JOIN departments d ON e.department_id = d.department_id;

-- Use View
SELECT * FROM employee_summary WHERE level = 'Senior';

-- Materialized View (PostgreSQL)
CREATE MATERIALIZED VIEW dept_stats AS
SELECT department_id,
       COUNT(*) as emp_count,
       AVG(salary) as avg_salary,
       MAX(salary) as max_salary
FROM employees
GROUP BY department_id;

-- Update View
CREATE OR REPLACE VIEW employee_summary AS
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    d.department_name,
    e.salary
FROM employees e
JOIN departments d ON e.department_id = d.department_id;

-- Drop View
DROP VIEW employee_summary;
```

**Example Output:**

```
employee_id | full_name   | department_name | salary   | level
----------- | ----------- | --------------- | -------- | ------
7           | James Wilson| IT              | 70000.00 | Senior
5           | David Jones | Engineering     | 65000.00 | Senior
```

### **23. Indexes**

Speeds lookups and joins by creating ordered structures on columns, while UNIQUE indexes enforce uniqueness and EXPLAIN reveals index usage plans.

```sql
-- Create Index
CREATE INDEX idx_employee_salary ON employees(salary);
CREATE INDEX idx_employee_dept_salary ON employees(department_id, salary);

-- Unique Index
CREATE UNIQUE INDEX idx_employee_email ON employees(email);

-- Composite Index
CREATE INDEX idx_employee_name_dept ON employees(last_name, first_name, department_id);

-- Covering Index (SQL Server/PostgreSQL)
CREATE INDEX idx_employee_covering ON employees(department_id) INCLUDE (first_name, last_name, salary);

-- Partial Index (PostgreSQL)
CREATE INDEX idx_active_employees ON employees(salary) WHERE active = true;

-- Functional Index (PostgreSQL)
CREATE INDEX idx_employee_upper_name ON employees(UPPER(last_name));

-- Drop Index
DROP INDEX idx_employee_salary;

-- Check Index Usage
EXPLAIN SELECT * FROM employees WHERE salary > 50000;
ANALYZE TABLE employees;  -- MySQL
```

**Example Output:**

```
id | select_type | table     | key                 | rows | Extra
-- | ----------- | --------- | ------------------- | ---- | --------------------
1  | SIMPLE      | employees | idx_emp_dept_salary |   10 | Using where; Using index
```

### **24. Stored Procedures**

Encapsulates parameterized logic on the server for reuse, security, and performance, invoked with CALL or EXEC depending on dialect.

```sql
-- Create Stored Procedure
DELIMITER //
CREATE PROCEDURE GetEmployeesByDepartment(IN dept_id INT)
BEGIN
    SELECT employee_id, first_name, last_name, salary
    FROM employees
    WHERE department_id = dept_id
    ORDER BY salary DESC;
END //
DELIMITER ;

-- Call Stored Procedure
CALL GetEmployeesByDepartment(1);

-- Procedure with Output Parameter
DELIMITER //
CREATE PROCEDURE GetEmployeeCount(IN dept_id INT, OUT emp_count INT)
BEGIN
    SELECT COUNT(*) INTO emp_count
    FROM employees
    WHERE department_id = dept_id;
END //
DELIMITER ;

-- Call with Output
CALL GetEmployeeCount(1, @count);
SELECT @count;

-- Procedure with Exception Handling
DELIMITER //
CREATE PROCEDURE UpdateEmployeeSalary(
    IN emp_id INT,
    IN new_salary DECIMAL(10,2)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;
    UPDATE employees SET salary = new_salary WHERE employee_id = emp_id;
    COMMIT;
END //
DELIMITER ;

-- Drop Procedure
DROP PROCEDURE GetEmployeesByDepartment;
```

**Example Output:**

```
employee_id | first_name | last_name | salary
----------- | ---------- | --------- | -------
3           | Michael    | Brown     | 62000.00
13          | William    | Davis     | 61000.00
1           | John       | Doe       | 50000.00
```

### **25. Functions**

Returns a single value per row for use in SELECTs or predicates, often to standardize calculations like bonuses or scores.

```sql
-- Create Function
DELIMITER //
CREATE FUNCTION CalculateBonus(salary DECIMAL(10,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE bonus DECIMAL(10,2);
    IF salary > 60000 THEN
        SET bonus = salary * 0.15;
    ELSE
        SET bonus = salary * 0.10;
    END IF;
    RETURN bonus;
END //
DELIMITER ;

-- Use Function
SELECT first_name, salary, CalculateBonus(salary) as bonus
FROM employees;

-- Table-Valued Function (SQL Server)
CREATE FUNCTION GetDepartmentEmployees(@dept_id INT)
RETURNS TABLE
AS
RETURN (
    SELECT employee_id, first_name, last_name, salary
    FROM employees
    WHERE department_id = @dept_id
);

-- Use Table Function
SELECT * FROM GetDepartmentEmployees(3);

-- Drop Function
DROP FUNCTION CalculateBonus;
```

**Example Output:**

```
first_name | salary  | bonus
---------- | ------- | -------
David      | 65000.0 | 9750.00
James      | 70000.0 | 10500.00
John       | 50000.0 | 5000.00
```

### **26. Triggers**

Executes automatic logic on row events like INSERT, UPDATE, or DELETE for auditing, validation, or denormalized updates.

```sql
-- BEFORE INSERT Trigger
DELIMITER //
CREATE TRIGGER before_employee_insert
BEFORE INSERT ON employees
FOR EACH ROW
BEGIN
    SET NEW.email = LOWER(NEW.email);
    SET NEW.hire_date = IFNULL(NEW.hire_date, CURRENT_DATE);

    -- Validation
    IF NEW.salary < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Salary cannot be negative';
    END IF;
END //
DELIMITER ;

-- AFTER UPDATE Trigger
DELIMITER //
CREATE TRIGGER after_salary_update
AFTER UPDATE ON employees
FOR EACH ROW
BEGIN
    IF OLD.salary != NEW.salary THEN
        INSERT INTO salary_audit (employee_id, old_salary, new_salary, change_date)
        VALUES (NEW.employee_id, OLD.salary, NEW.salary, NOW());
    END IF;
END //
DELIMITER ;

-- AFTER DELETE Trigger
DELIMITER //
CREATE TRIGGER after_employee_delete
AFTER DELETE ON employees
FOR EACH ROW
BEGIN
    INSERT INTO deleted_employees_log
    VALUES (OLD.employee_id, OLD.first_name, OLD.last_name, NOW());
END //
DELIMITER ;

-- Instead Of Trigger (SQL Server - for views)
CREATE TRIGGER tr_employee_view_insert
ON employee_view
INSTEAD OF INSERT
AS
BEGIN
    INSERT INTO employees (first_name, last_name, department_id)
    SELECT first_name, last_name, department_id FROM inserted;
END;

-- Drop Trigger
DROP TRIGGER before_employee_insert;
```

**Example Output (after salary update):**

```
employee_id | old_salary | new_salary | change_date
----------- | ---------- | ---------- | -------------------
7           | 70000.00   | 72000.00   | 2025-10-11 11:59:00
```

### **27. Transactions**

Groups statements into atomic units with BEGIN/COMMIT/ROLLBACK and optional SAVEPOINTs to ensure consistency and recoverability.

```sql
-- Basic Transaction
BEGIN TRANSACTION;

UPDATE employees SET salary = salary * 1.1 WHERE department_id = 1;
INSERT INTO salary_changes (employee_id, old_salary, new_salary, change_date)
SELECT employee_id, salary / 1.1, salary, CURRENT_DATE
FROM employees WHERE department_id = 1;

COMMIT;

-- Transaction with Rollback
BEGIN TRANSACTION;

UPDATE employees SET salary = salary * 1.1 WHERE department_id = 1;

-- Check if update was successful
IF @@ROWCOUNT = 0
BEGIN
    ROLLBACK;
    PRINT 'No employees updated';
END
ELSE
BEGIN
    COMMIT;
    PRINT 'Salaries updated successfully';
END

-- Savepoints
BEGIN TRANSACTION;

INSERT INTO employees (employee_id, first_name, last_name) VALUES (100, 'Test', 'User');
SAVEPOINT sp1;

UPDATE employees SET salary = 50000 WHERE employee_id = 100;
SAVEPOINT sp2;

DELETE FROM employees WHERE employee_id = 100;

-- Rollback to savepoint
ROLLBACK TO sp1;

COMMIT;

-- Transaction Isolation Levels
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

**Example Output:**

```
Query OK, 3 rows affected
Query OK, 3 rows affected
Query OK, committed
Salaries updated successfully
```

### **28. Advanced Data Types & JSON**

Stores semi-structured data and supports JSON_EXTRACT/JSON_SET for querying and updating JSON documents in supported SQL dialects.

```sql
-- JSON Operations (MySQL 5.7+)
CREATE TABLE user_preferences (
    user_id INT,
    preferences JSON
);

INSERT INTO user_preferences VALUES
(1, '{"theme": "dark", "language": "en", "notifications": {"email": true, "sms": false}}');

-- Query JSON
SELECT user_id,
       JSON_EXTRACT(preferences, '$.theme') as theme,
       JSON_EXTRACT(preferences, '$.notifications.email') as email_notifications
FROM user_preferences;

-- Update JSON
UPDATE user_preferences
SET preferences = JSON_SET(preferences, '$.theme', 'light')
WHERE user_id = 1;

-- JSON Array operations
SELECT user_id,
       JSON_EXTRACT(preferences, '$.tags[0]') as first_tag,
       JSON_LENGTH(preferences, '$.tags') as tag_count
FROM user_preferences;

-- JSON Table Functions (MySQL 8.0+)
SELECT * FROM JSON_TABLE(
    '{"employees": [{"name": "John", "salary": 50000}, {"name": "Jane", "salary": 60000}]}',
    '$.employees[*]' COLUMNS (
        name VARCHAR(50) PATH '$.name',
        salary INT PATH '$.salary'
    )
) AS jt;

-- PostgreSQL JSONB operations
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    data JSONB
);

-- JSONB queries with operators
SELECT * FROM documents WHERE data ? 'name';                    -- Key exists
SELECT * FROM documents WHERE data->'age' > '25';               -- Value comparison
SELECT * FROM documents WHERE data @> '{"active": true}';       -- Contains
SELECT * FROM documents WHERE data->'tags' ? | ARRAY['urgent', 'important']; -- Array overlap
```

**Example Output:**

```
user_id | theme  | email_notifications
------- | ------ | ------------------
1       | "dark" | true
```

### **29. Performance Optimization**

Uses EXPLAIN plans, proper indexes, and denormalization or partitioning when appropriate to reduce scans and improve cardinality and I/O patterns.

```sql
-- Query Optimization
-- Use EXPLAIN to analyze query execution
EXPLAIN SELECT e.first_name, d.department_name
FROM employees e
JOIN departments d ON e.department_id = d.department_id
WHERE e.salary > 50000;

-- Index Hints (MySQL)
SELECT * FROM employees USE INDEX (idx_salary) WHERE salary > 50000;
SELECT * FROM employees FORCE INDEX (idx_dept_salary) WHERE department_id = 3;

-- Query Rewriting for Performance
-- Instead of:
SELECT * FROM employees WHERE YEAR(hire_date) = 2020;
-- Use:
SELECT * FROM employees WHERE hire_date >= '2020-01-01' AND hire_date < '2021-01-01';

-- Covering Index for specific query
CREATE INDEX idx_salary_covering ON employees(salary) INCLUDE (first_name, department_id);

-- Partitioning (for large tables)
CREATE TABLE sales_data (
    id INT,
    sale_date DATE,
    amount DECIMAL(10,2)
)
PARTITION BY RANGE (YEAR(sale_date)) (
    PARTITION p2020 VALUES LESS THAN (2021),
    PARTITION p2021 VALUES LESS THAN (2022),
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024)
);

-- Hash Partitioning
CREATE TABLE user_data (
    user_id INT,
    username VARCHAR(50),
    email VARCHAR(100)
)
PARTITION BY HASH(user_id) PARTITIONS 4;

-- Statistics Update
ANALYZE TABLE employees;
UPDATE STATISTICS employees;  -- SQL Server
VACUUM ANALYZE employees;     -- PostgreSQL
```

**Example Output:**

```
id | select_type | table | key           | rows | Extra
-- | ----------- | ----- | ------------- | ---- | -----------------
1  | SIMPLE      | e     | idx_emp_sal   |   12 | Using where
1  | SIMPLE      | d     | PRIMARY       |    1 | Using index
```

### **30. Advanced Query Techniques**

Implements pivot-like aggregates, gaps and islands, and percentiles with window functions for analytics-heavy use cases.

```sql
-- Pivot Table Simulation
SELECT
    department_id,
    SUM(CASE WHEN YEAR(hire_date) = 2020 THEN 1 ELSE 0 END) as hired_2020,
    SUM(CASE WHEN YEAR(hire_date) = 2021 THEN 1 ELSE 0 END) as hired_2021,
    SUM(CASE WHEN YEAR(hire_date) = 2022 THEN 1 ELSE 0 END) as hired_2022
FROM employees
GROUP BY department_id;

-- Running Difference
SELECT
    first_name,
    salary,
    salary - LAG(salary) OVER (ORDER BY hire_date) as salary_diff
FROM employees
ORDER BY hire_date;

-- Percentile Calculations
SELECT
    first_name,
    salary,
    PERCENT_RANK() OVER (ORDER BY salary) as salary_percentile,
    NTILE(4) OVER (ORDER BY salary) as salary_quartile,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) OVER () as median_salary
FROM employees;

-- Gap Analysis (find missing sequences)
WITH salary_gaps AS (
    SELECT
        salary,
        LEAD(salary) OVER (ORDER BY salary) as next_salary,
        LEAD(salary) OVER (ORDER BY salary) - salary as gap
    FROM employees
)
SELECT salary, next_salary, gap
FROM salary_gaps
WHERE gap > 5000
ORDER BY gap DESC;

-- Islands and Gaps (consecutive ranges)
WITH numbered AS (
    SELECT employee_id, hire_date,
           ROW_NUMBER() OVER (ORDER BY hire_date) as rn,
           DATE_SUB(hire_date, INTERVAL ROW_NUMBER() OVER (ORDER BY hire_date) DAY) as grp
    FROM employees
)
SELECT MIN(hire_date) as range_start,
       MAX(hire_date) as range_end,
       COUNT(*) as consecutive_hires
FROM numbered
GROUP BY grp
ORDER BY range_start;

-- Moving Window Analytics
SELECT first_name, hire_date, salary,
  AVG(salary) OVER (ORDER BY hire_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as trailing_7_avg,
  MAX(salary) OVER (ORDER BY hire_date ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING) as surrounding_max,
  COUNT(*) OVER (ORDER BY hire_date RANGE BETWEEN INTERVAL '1' YEAR PRECEDING AND CURRENT ROW) as hires_last_year
FROM employees
ORDER BY hire_date;

-- Conditional Aggregation
SELECT department_id,
  COUNT(*) as total_employees,
  COUNT(CASE WHEN salary > 60000 THEN 1 END) as high_earners,
  AVG(CASE WHEN YEAR(hire_date) >= 2020 THEN salary END) as avg_salary_recent_hires,
  STRING_AGG(CASE WHEN salary = MAX(salary) OVER (PARTITION BY department_id)
                  THEN first_name END, ', ') as top_earners
FROM employees
GROUP BY department_id;
```

**Example Output:**

```
department_id | hired_2020 | hired_2021 | hired_2022
------------- | ---------- | ---------- | ----------
3             | 1          | 1          | 0
4             | 1          | 1          | 1
5             | 0          | 1          | 0

first_name | salary  | salary_diff
---------- | ------- | -----------
James      | 70000.0 | NULL
John       | 50000.0 | -20000.0
Sophia     | 59000.0 | 9000.0
Robert     | 58000.0 | -1000.0
```

### **31. Database Administration**

Essential commands for managing users, permissions, backups, and database maintenance.

```sql
-- User Management
CREATE USER 'analyst'@'localhost' IDENTIFIED BY 'password123';
CREATE USER 'readonly_user'@'%' IDENTIFIED BY 'readonly_pass';

-- Grant Permissions
GRANT SELECT, INSERT, UPDATE ON company_db.employees TO 'analyst'@'localhost';
GRANT SELECT ON company_db.* TO 'readonly_user'@'%';
GRANT ALL PRIVILEGES ON company_db.* TO 'admin'@'localhost';

-- Revoke Permissions
REVOKE INSERT, UPDATE ON company_db.employees FROM 'analyst'@'localhost';

-- Show Grants
SHOW GRANTS FOR 'analyst'@'localhost';

-- Drop User
DROP USER 'readonly_user'@'%';

-- Backup and Restore
-- MySQL
mysqldump -u root -p company_db > backup.sql
mysql -u root -p company_db < backup.sql

-- PostgreSQL
pg_dump company_db > backup.sql
psql company_db < backup.sql

-- Database Maintenance
OPTIMIZE TABLE employees;     -- MySQL
VACUUM employees;            -- PostgreSQL
REINDEX TABLE employees;     -- PostgreSQL
DBCC REINDEX('employees');   -- SQL Server

-- Show Database Information
SHOW DATABASES;
SHOW TABLES;
DESCRIBE employees;
SHOW CREATE TABLE employees;
SHOW INDEX FROM employees;
```

**Example Output:**

```
Query OK, 0 rows affected
Query OK, 0 rows affected

Grants for analyst@localhost
-----------------------------
GRANT SELECT, INSERT, UPDATE ON `company_db`.`employees` TO `analyst`@`localhost`
```

This comprehensive cheatsheet covers SQL from basic operations to advanced analytics, performance tuning, and database administration. Each section includes practical examples with expected outputs to help understand the concepts and verify implementations across different SQL dialects.
