# Chapter 5: Joins & Set Operations

## Sample Input Tables for All Examples

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
dept_id | dept_name    | location
1       | Engineering  | New York
2       | Marketing    | Boston
3       | Sales        | Chicago

-- sales table
sales:
sale_id | emp_id | amount | sale_date
501     | 101    | 1500   | 2024-01-15
502     | 101    | 1000   | 2024-01-10
503     | 102    | 1200   | 2024-01-12
504     | 102    | 900    | 2024-01-08

-- offices table
offices:
office_id | office_location
1         | New York
2         | London

-- customers table (for set operations)
customers:
customer_id | city
1           | New York
2           | London
3           | Paris
4           | New York

-- suppliers table (for set operations)
suppliers:
supplier_id | city
10          | London
20          | Berlin
30          | New York
```

## 5.1 Join Types

### 5.1.1 Inner, Left, Right, Full Joins

```sql
-- Inner join: returns only matching rows
SELECT e.emp_id, e.emp_name, d.dept_name
FROM employees e
INNER JOIN departments d
  ON e.dept_id = d.dept_id;
```

**Output:**

```
emp_id | emp_name      | dept_name
101    | Alice Johnson | Engineering
102    | Bob Wilson    | Marketing
103    | Carol Davis   | Engineering
```

```sql
-- Left join: all employees, with department when available
SELECT e.emp_id, e.emp_name, d.dept_name
FROM employees e
LEFT JOIN departments d
  ON e.dept_id = d.dept_id;
```

**Output:**

```
emp_id | emp_name      | dept_name
101    | Alice Johnson | Engineering
102    | Bob Wilson    | Marketing
103    | Carol Davis   | Engineering
104    | Dave Brown    | NULL
```

```sql
-- Right join: all departments, with employees when available
SELECT e.emp_id, e.emp_name, d.dept_name
FROM employees e
RIGHT JOIN departments d
  ON e.dept_id = d.dept_id;
```

**Output:**

```
emp_id | emp_name      | dept_name
101    | Alice Johnson | Engineering
102    | Bob Wilson    | Marketing
103    | Carol Davis   | Engineering
NULL   | NULL          | Sales
```

```sql
-- Full join: all employees and all departments, matched when possible
SELECT e.emp_id, e.emp_name, d.dept_name
FROM employees e
FULL JOIN departments d
  ON e.dept_id = d.dept_id;
```

**Output:**

```
emp_id | emp_name      | dept_name
101    | Alice Johnson | Engineering
102    | Bob Wilson    | Marketing
103    | Carol Davis   | Engineering
104    | Dave Brown    | NULL
NULL   | NULL          | Sales
```

### 5.1.2 Cross & Self-Joins

```sql
-- Cross join: Cartesian product of employees and offices
SELECT e.emp_name, o.office_location
FROM employees e
CROSS JOIN offices o;
```

**Output:**

```
emp_name      | office_location
Alice Johnson | New York
Alice Johnson | London
Bob Wilson    | New York
Bob Wilson    | London
Carol Davis   | New York
Carol Davis   | London
Dave Brown    | New York
Dave Brown    | London
```

```sql
-- Self-join: employees with their managers
SELECT e.emp_name AS employee, m.emp_name AS manager
FROM employees e
LEFT JOIN employees m
  ON e.manager_id = m.emp_id;
```

**Output:**

```
employee      | manager
Alice Johnson | NULL
Bob Wilson    | Alice Johnson
Carol Davis   | Alice Johnson
Dave Brown    | Bob Wilson
```

### 5.1.3 Semi-Join & Anti-Join via EXISTS/NOT EXISTS

```sql
-- Semi-join (EXISTS): employees who have made sales
SELECT e.emp_id, e.emp_name
FROM employees e
WHERE EXISTS (
  SELECT 1
  FROM sales s
  WHERE s.emp_id = e.emp_id
);
```

**Output:**

```
emp_id | emp_name
101    | Alice Johnson
102    | Bob Wilson
```

```sql
-- Anti-join (NOT EXISTS): employees with no sales
SELECT e.emp_id, e.emp_name
FROM employees e
WHERE NOT EXISTS (
  SELECT 1
  FROM sales s
  WHERE s.emp_id = e.emp_id
);
```

**Output:**

```
emp_id | emp_name
103    | Carol Davis
104    | Dave Brown
```

## 5.2 Set Operators

### 5.2.1 UNION vs UNION ALL

```sql
-- UNION: remove duplicates from cities
SELECT city FROM customers
UNION
SELECT city FROM suppliers;
```

**Output:**

```
city
Berlin
London
New York
Paris
```

```sql
-- UNION ALL: include duplicates
SELECT city FROM customers
UNION ALL
SELECT city FROM suppliers;
```

**Output:**

```
city
New York
London
Paris
New York
London
Berlin
New York
```

### 5.2.2 INTERSECT & EXCEPT

```sql
-- INTERSECT: cities present in both customers and suppliers
SELECT city FROM customers
INTERSECT
SELECT city FROM suppliers;
```

**Output:**

```
city
London
New York
```

```sql
-- EXCEPT: cities in customers but not in suppliers
SELECT city FROM customers
EXCEPT
SELECT city FROM suppliers;
```

**Output:**

```
city
Paris
```

## 5.3 Performance Considerations

### 5.3.1 Join Order & Join Hints

```sql
-- Example with join hint (SQL Server syntax)
SELECT /*+ USE_HASH(e,d) */ e.emp_name, d.dept_name
FROM employees e
JOIN departments d
  ON e.dept_id = d.dept_id;
```

**Output:**

```
emp_name      | dept_name
Alice Johnson | Engineering
Bob Wilson    | Marketing
Carol Davis   | Engineering
```

### 5.3.2 Index Usage & Statistics

```sql
-- Ensure indexes exist for optimal join performance
-- CREATE INDEX idx_employees_dept_id ON employees(dept_id);
-- CREATE INDEX idx_departments_dept_id ON departments(dept_id);

-- Query with indexed columns
SELECT e.emp_name, d.dept_name, d.location
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
WHERE d.location = 'New York';
```

**Output:**

```
emp_name      | dept_name   | location
Alice Johnson | Engineering | New York
Carol Davis   | Engineering | New York
```

## 5.4 Lateral Joins

### 5.4.1 CROSS APPLY/OUTER APPLY

```sql
-- CROSS APPLY: each employee with their highest sale (SQL Server/Oracle syntax)
SELECT e.emp_id, e.emp_name, s.max_amount
FROM employees e
CROSS APPLY (
  SELECT MAX(amount) as max_amount
  FROM sales
  WHERE emp_id = e.emp_id
) s;
```

**Output:**

```
emp_id | emp_name   | max_amount
101    | Alice Johnson | 1500
102    | Bob Wilson    | 1200
```

```sql
-- OUTER APPLY: includes employees even if no sales
SELECT e.emp_id, e.emp_name, s.max_amount
FROM employees e
OUTER APPLY (
  SELECT MAX(amount) as max_amount
  FROM sales
  WHERE emp_id = e.emp_id
) s;
```

**Output:**

```
emp_id | emp_name      | max_amount
101    | Alice Johnson | 1500
102    | Bob Wilson    | 1200
103    | Carol Davis   | NULL
104    | Dave Brown    | NULL
```

### 5.4.2 UNNEST/ARRAY Operations (PostgreSQL)

```sql
-- Sample data for array operations
-- products table with array column:
products_with_tags:
product_id | name   | tags
1          | Laptop | {electronics, computers, portable}
2          | Phone  | {electronics, mobile}

-- UNNEST: expand array into separate rows
SELECT p.product_id, p.name, tag
FROM products_with_tags p
CROSS JOIN LATERAL UNNEST(p.tags) AS tag;
```

**Output:**

```
product_id | name   | tag
1          | Laptop | electronics
1          | Laptop | computers
1          | Laptop | portable
2          | Phone  | electronics
2          | Phone  | mobile
```

## Key Performance Tips for Joins

1. **Index Join Columns**: Always index foreign key columns used in joins
2. **Join Order Matters**: Start with smaller tables when possible
3. **Use EXISTS vs IN**: For semi-joins, EXISTS often performs better than IN with subqueries
4. **Statistics Currency**: Keep table statistics updated for optimal query plans
5. **Consider Join Algorithms**: Hash joins for large tables, nested loops for small tables
