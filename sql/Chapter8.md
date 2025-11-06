# Chapter 8: Window Functions & Analytics

## Input Tables

```sql
-- employees table
employees:
emp_id | emp_name      | dept_id | salary
101    | Alice Johnson | 1       | 80000
102    | Bob Wilson    | 2       | 70000
103    | Carol Davis   | 1       | 75000
104    | Dave Brown    | NULL    | 65000

-- sales table
sales:
sale_id | emp_id | amount | sale_date
501     | 101    | 1500   | 2024-01-15
502     | 101    | 1000   | 2024-01-10
503     | 102    | 1200   | 2024-01-12
504     | 102    | 900    | 2024-01-08
505     | 103    | 800    | 2024-01-14
506     | 103    | 700    | 2024-01-11
```

## 8.1 Ranking Functions

### 8.1.1 ROW_NUMBER(), RANK(), DENSE_RANK()

```sql
-- Assign row numbers, rank, and dense rank per department by salary
SELECT
  emp_id,
  emp_name,
  dept_id,
  salary,
  ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rn,
  RANK()       OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk,
  DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS drnk
FROM employees
WHERE dept_id IS NOT NULL;
```

**Output:**

```
emp_id | emp_name      | dept_id | salary | rn | rnk | drnk
101    | Alice Johnson | 1       | 80000  | 1  | 1   | 1
103    | Carol Davis   | 1       | 75000  | 2  | 2   | 2
102    | Bob Wilson    | 2       | 70000  | 1  | 1   | 1
```

### 8.1.2 NTILE() Distributions

```sql
-- Divide sales into 2 buckets per employee by amount
SELECT
  sale_id,
  emp_id,
  amount,
  NTILE(2) OVER (PARTITION BY emp_id ORDER BY amount DESC) AS bucket
FROM sales;
```

**Output:**

```
sale_id | emp_id | amount | bucket
501     | 101    | 1500   | 1
502     | 101    | 1000   | 2
503     | 102    | 1200   | 1
504     | 102    | 900    | 2
505     | 103    | 800    | 1
506     | 103    | 700    | 2
```

## 8.2 Aggregate OVER()

### 8.2.1 SUM() OVER Partitions

```sql
-- Total and running sum per employee
SELECT
  sale_id,
  emp_id,
  amount,
  SUM(amount) OVER (PARTITION BY emp_id) AS total_by_emp,
  SUM(amount) OVER (PARTITION BY emp_id ORDER BY sale_date
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_sum
FROM sales;
```

**Output:**

```
sale_id | emp_id | amount | total_by_emp | running_sum
501     | 101    | 1500   | 2500         | 1500
502     | 101    | 1000   | 2500         | 2500
503     | 102    | 1200   | 2100         | 1200
504     | 102    | 900    | 2100         | 2100
505     | 103    | 800    | 1500         | 800
506     | 103    | 700    | 1500         | 1500
```

### 8.2.2 AVG() OVER Orderings

```sql
-- Moving average of 2 latest sales per employee
SELECT
  sale_id,
  emp_id,
  amount,
  AVG(amount) OVER (
    PARTITION BY emp_id
    ORDER BY sale_date
    ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
  ) AS moving_avg
FROM sales;
```

**Output:**

```
sale_id | emp_id | amount | moving_avg
502     | 101    | 1000   | 1250       -- avg of 1500 & 1000
501     | 101    | 1500   | 1250
504     | 102    | 900    | 1050       -- avg of 1200 & 900
503     | 102    | 1200   | 1050
506     | 103    | 700    | 750        -- avg of 800 & 700
505     | 103    | 800   | 750
```

## 8.3 Window Clauses

### 8.3.1 PARTITION BY

Partition defines groups for window operations; without it, functions apply over the entire result set.

```sql
-- Cumulative sum over all sales (no partition)
SELECT
  sale_id,
  amount,
  SUM(amount) OVER (ORDER BY sale_date) AS cumulative
FROM sales;
```

**Output:**

```
sale_id | amount | cumulative
504     | 900    | 900
502     | 1000   | 1900
506     | 700    | 2600
503     | 1200   | 3800
501     | 1500   | 5300
505     | 800    | 6100
```

### 8.3.2 ORDER BY and Frame (ROWS vs RANGE)

- **ROWS** frames count physical rows; **RANGE** frames logical value ranges.

```sql
-- RANGE frame: sum of sales within ± interval
SELECT
  sale_id,
  sale_date,
  amount,
  SUM(amount) OVER (
    ORDER BY sale_date
    RANGE BETWEEN INTERVAL '5 days' PRECEDING AND CURRENT ROW
  ) AS range_sum
FROM sales;
```

**Output:**

```
sale_id | sale_date  | amount | range_sum
502     | 2024-01-10 | 1000   | 1000
504     | 2024-01-08 | 900    | 900
506     | 2024-01-11 | 700    | 2600   -- includes 900 & 1000 & 700
503     | 2024-01-12 | 1200   | 3800
501     | 2024-01-15 | 1500   | 4600
505     | 2024-01-14 | 800    | 3500
```

## 8.4 Analytical Patterns

### 8.4.1 Running Totals and Moving Averages

```sql
-- Daily running total of all sales
SELECT
  sale_date,
  SUM(amount) OVER (ORDER BY sale_date ROWS UNBOUNDED PRECEDING) AS daily_cum
FROM sales
GROUP BY sale_date
ORDER BY sale_date;
```

**Output:**

```
sale_date  | daily_cum
2024-01-08 | 900
2024-01-10 | 1900
2024-01-11 | 2600
2024-01-12 | 3800
2024-01-14 | 4600
2024-01-15 | 6100
```

### 8.4.2 Gaps-and-Islands Problems

```sql
-- Identify consecutive sale_date runs per employee
SELECT
  emp_id,
  sale_date,
  amount,
  sale_date
    - ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY sale_date) AS grp
FROM sales
ORDER BY emp_id, sale_date;
```

**Output:**

```
emp_id | sale_date  | amount | grp
101    | 2024-01-10 | 1000   | 2024-01-09
101    | 2024-01-15 | 1500   | 2024-01-13
102    | 2024-01-08 | 900    | 2024-01-07
102    | 2024-01-12 | 1200   | 2024-01-10
103    | 2024-01-11 | 700    | 2024-01-10
103    | 2024-01-14 | 800    | 2024-01-12
```

_Use `grp` value to group continuous sequences into “islands.”_
