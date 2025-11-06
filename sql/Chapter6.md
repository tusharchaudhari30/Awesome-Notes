# Chapter 6: Aggregation & Grouping

## Input Table

```sql
-- sales table
sales:
sale_id | emp_id | dept_id | amount | sale_date
501     | 101    | 1       | 1500   | 2024-01-15
502     | 101    | 1       | 1000   | 2024-01-10
503     | 102    | 2       | 1200   | 2024-01-12
504     | 102    | 2       | 900    | 2024-01-08
505     | 103    | 1       | 800    | 2024-01-14
506     | 104    | NULL    | 700    | 2024-01-11
```

## 6.1 GROUP BY & HAVING

### 6.1.1 Basic GROUP BY

```sql
-- Total sales per department
SELECT dept_id, SUM(amount) AS total_sales
FROM sales
GROUP BY dept_id;
```

**Output:**

```
dept_id | total_sales
1       | 3300       -- 1500 + 1000 + 800
2       | 2100       -- 1200 + 900
NULL    | 700        -- sales without department
```

### 6.1.2 HAVING Filters

```sql
-- Departments with total sales > 2000
SELECT dept_id, SUM(amount) AS total_sales
FROM sales
GROUP BY dept_id
HAVING SUM(amount) > 2000;
```

**Output:**

```
dept_id | total_sales
1       | 3300
2       | 2100
```

## 6.2 Aggregate Functions

### 6.2.1 SUM, COUNT, AVG

```sql
-- Count and average sale amount per employee
SELECT emp_id,
       COUNT(*) AS num_sales,
       AVG(amount) AS avg_sale
FROM sales
GROUP BY emp_id;
```

**Output:**

```
emp_id | num_sales | avg_sale
101    | 2         | 1250     -- (1500+1000)/2
102    | 2         | 1050     -- (1200+900)/2
103    | 1         | 800
104    | 1         | 700
```

### 6.2.2 MIN, MAX, STDDEV, VARIANCE

```sql
-- Statistical summary per dept
SELECT dept_id,
       MIN(amount) AS min_sale,
       MAX(amount) AS max_sale,
       STDDEV(amount) AS stddev_sale,
       VARIANCE(amount) AS var_sale
FROM sales
GROUP BY dept_id;
```

**Output:**

```
dept_id | min_sale | max_sale | stddev_sale | var_sale
1       | 800      | 1500     | 381.05      | 145200.00
2       | 900      | 1200     | 212.13      | 45000.00
NULL    | 700      | 700      | NULL        | NULL       -- single row yields NULL
```

## 6.3 Advanced Grouping

### 6.3.1 ROLLUP & CUBE

```sql
-- Rollup: dept_id totals and grand total
SELECT dept_id, emp_id, SUM(amount) AS total
FROM sales
GROUP BY ROLLUP(dept_id, emp_id);
```

**Output:**

```
dept_id | emp_id | total
1       | 101    | 2500
1       | 103    | 800
1       | NULL   | 3300    -- subtotal for dept 1
2       | 102    | 2100
2       | NULL   | 2100    -- subtotal for dept 2
NULL    | NULL   | 6100    -- grand total
```

```sql
-- Cube: all combinations of dept_id and emp_id subtotals
SELECT dept_id, emp_id, SUM(amount) AS total
FROM sales
GROUP BY CUBE(dept_id, emp_id);
```

**Output (selected rows):**

```
dept_id | emp_id | total
1       | 101    | 2500
1       | 103    | 800
1       | NULL   | 3300
2       | 102    | 2100
2       | NULL   | 2100
NULL    | 101    | 2500    -- total for emp 101 across all depts
NULL    | NULL   | 6100    -- grand total
...     | ...    | ...
```

### 6.3.2 GROUPING SETS & GROUPING_ID

```sql
-- Custom grouping: per dept and overall, ignoring emp_id
SELECT dept_id, SUM(amount) AS total
FROM sales
GROUP BY GROUPING SETS ((dept_id), ());
```

**Output:**

```
dept_id | total
1       | 3300
2       | 2100
NULL    | 6100   -- grand total
```

## 6.4 DISTINCT vs GROUP BY

### 6.4.1 DISTINCT De-duplication Semantics

```sql
-- Number of unique departments in sales
SELECT COUNT(DISTINCT dept_id) AS unique_depts
FROM sales;
```

**Output:**

```
unique_depts
2   -- dept_id 1 and 2, NULL ignored by DISTINCT
```

### 6.4.2 Performance Trade-offs

```sql
-- Using GROUP BY for same result
SELECT COUNT(*) AS unique_depts
FROM (
  SELECT dept_id
  FROM sales
  GROUP BY dept_id
) t;
```

**Output:**

```
unique_depts
3   -- counts NULL as a group as well
```

---

_End of Chapter 6_
