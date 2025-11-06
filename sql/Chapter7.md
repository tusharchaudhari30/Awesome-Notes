# Chapter 7: Subqueries & Common Table Expressions (CTEs)

Subqueries and CTEs are powerful techniques for breaking complex queries into manageable parts, improving readability, and supporting hierarchical and recursive data processing. Subqueries can be used in `SELECT`, `FROM`, `WHERE`, and `HAVING` clauses. CTEs (introduced by the `WITH` keyword) act as named result sets that exist only for the duration of a single query.

## Input Tables

```sql
-- employees table
employees:
emp_id | emp_name      | dept_id | manager_id | salary
101    | Alice Johnson | 1       | NULL       | 80000
102    | Bob Wilson    | 2       | 101        | 70000
103    | Carol Davis   | 1       | 101        | 75000
104    | Dave Brown    | NULL    | 102        | 65000

-- departments table
departments:
dept_id | dept_name
1       | Engineering
2       | Marketing
3       | Sales

-- sales table
sales:
sale_id | emp_id | amount | sale_date
501     | 101    | 1500   | 2024-01-15
502     | 101    | 1000   | 2024-01-10
503     | 102    | 1200   | 2024-01-12
504     | 102    | 900    | 2024-01-08
```

## 7.1 Subquery Types

### 7.1.1 Single-row vs Multi-row Subqueries

- **Single-row subqueries** return exactly one value and can be used wherever a scalar expression is expected.
- **Multi-row subqueries** return a list of values and require operators like `IN`, `ANY`, `ALL`.

```sql
-- Single-row subquery: give 10% raise to lowest-paid employee
UPDATE employees
SET salary = salary * 1.10
WHERE salary = (
  SELECT MIN(salary)
  FROM employees
);
```

**Output:**

```
(emp_id 104 updated from 65000 to 71500)
```

```sql
-- Multi-row subquery: list employees in HR or Sales departments
SELECT emp_id, emp_name
FROM employees
WHERE dept_id IN (
  SELECT dept_id
  FROM departments
  WHERE dept_name IN ('HR','Sales')
);
```

**Output:**

```
emp_id | emp_name
(returns rows for dept_id matching HR or Sales if they exist)
```

### 7.1.2 Correlated vs Uncorrelated Subqueries

- **Uncorrelated**: executes once; independent of outer query.
- **Correlated**: executes for each outer row; references outer columns.

```sql
-- Uncorrelated: apply bonus if company-wide avg salary > 75000
UPDATE employees
SET salary = salary * 1.05
WHERE (
  SELECT AVG(salary)
  FROM employees
) > 75000;
```

**Output:**

```
(all rows updated if condition true)
```

```sql
-- Correlated: find employees earning above their dept average
SELECT e.emp_id, e.emp_name, e.salary
FROM employees e
WHERE e.salary > (
  SELECT AVG(salary)
  FROM employees
  WHERE dept_id = e.dept_id
);
```

**Output:**

```
emp_id | emp_name      | salary
101    | Alice Johnson | 80000
103    | Carol Davis   | 75000
```

## 7.2 Common Table Expressions (CTEs)

CTEs improve query structure by defining temporary named result sets.

### 7.2.1 Non-recursive CTEs

Used for modularizing complex joins or subqueries.

```sql
WITH recent_sales AS (
  SELECT emp_id, amount
  FROM sales
  WHERE sale_date >= CURRENT_DATE - INTERVAL '30 days'
)
SELECT e.emp_name, SUM(r.amount) AS total_recent
FROM recent_sales r
JOIN employees e ON r.emp_id = e.emp_id
GROUP BY e.emp_name;
```

**Output:**

```
emp_name      | total_recent
Alice Johnson | 1500
Bob Wilson    | 1200
```

### 7.2.2 Recursive CTEs

Facilitate hierarchical data traversal (e.g., org charts, bill-of-materials).

```sql
WITH RECURSIVE org_chart AS (
  -- Anchor: top-level managers
  SELECT emp_id, manager_id, emp_name, 1 AS level
  FROM employees
  WHERE manager_id IS NULL

  UNION ALL

  -- Recursive: direct reports
  SELECT e.emp_id, e.manager_id, e.emp_name, oc.level + 1
  FROM employees e
  JOIN org_chart oc ON e.manager_id = oc.emp_id
)
SELECT * FROM org_chart ORDER BY level, emp_id;
```

**Output:**

```
emp_id | manager_id | emp_name      | level
101    | NULL       | Alice Johnson | 1
102    | 101        | Bob Wilson    | 2
103    | 101        | Carol Davis   | 2
104    | 102        | Dave Brown    | 3
```

## 7.3 Derived Tables & Inline Views

### 7.3.1 Derived Tables

Subqueries in the `FROM` clause provide on-the-fly tables.

```sql
SELECT dt.dept_id, dt.avg_salary
FROM (
  SELECT dept_id, AVG(salary) AS avg_salary
  FROM employees
  GROUP BY dept_id
) AS dt
WHERE dt.avg_salary > 75000;
```

**Output:**

```
dept_id | avg_salary
1       | 77500  -- avg of dept 1 salaries
```

### 7.3.2 Inline Views vs CTEs

Inline views are limited to a single query occurrence. CTEs can be referenced multiple times, enhancing readability and reducing duplication.

```sql
-- Inline view repeated
SELECT iv.dept_id, iv.count_emp
FROM (
  SELECT dept_id, COUNT(*) AS count_emp
  FROM employees
  GROUP BY dept_id
) iv
WHERE iv.count_emp > 1

UNION ALL

SELECT iv.dept_id, iv.count_emp
FROM (
  SELECT dept_id, COUNT(*) AS count_emp
  FROM employees
  GROUP BY dept_id
) iv
WHERE iv.count_emp = 1;
```

```sql
-- Better with CTE
WITH dept_counts AS (
  SELECT dept_id, COUNT(*) AS count_emp
  FROM employees
  GROUP BY dept_id
)
SELECT dept_id, count_emp
FROM dept_counts WHERE count_emp > 1
UNION ALL
SELECT dept_id, count_emp
FROM dept_counts WHERE count_emp = 1;
```

**Output (both methods):**

```
dept_id | count_emp
1       | 2
2       | 1
NULL    | 1
```
