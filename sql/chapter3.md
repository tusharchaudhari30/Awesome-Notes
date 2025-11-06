# SQL Data Definition Language (DDL)

## CREATE Statements

### CREATE TABLE with Constraints

Define tables and enforce data rules at creation time.

```sql
-- Create 'employees' table with primary key and not-null constraints
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,            -- Unique identifier for each employee
    first_name VARCHAR(50) NOT NULL,   -- First name is required
    last_name VARCHAR(50) NOT NULL,    -- Last name is required
    email VARCHAR(100) UNIQUE,         -- Email must be unique across all rows
    hire_date DATE DEFAULT CURRENT_DATE -- Defaults to current date when omitted
);
```

### CREATE VIEW

Encapsulate complex queries as reusable virtual tables.

```sql
-- Create a view of active employees hired in the last year
CREATE VIEW recent_hires AS
SELECT emp_id, first_name, last_name, hire_date
FROM employees
WHERE hire_date >= DATEADD(year, -1, CURRENT_DATE);
```

### CREATE INDEX

Improve query performance on frequently filtered columns.

```sql
-- Create a nonclustered index on department for faster lookups
CREATE INDEX idx_employees_department
ON employees(department);
```

## ALTER Statements

### ADD/DROP Column

Modify table structures without full recreation.

```sql
-- Add a phone number column to employees
ALTER TABLE employees
ADD phone VARCHAR(15);

-- Remove the phone column if no longer needed
ALTER TABLE employees
DROP COLUMN phone;
```

### ADD/DROP/MODIFY Constraints

Introduce or remove data rules after table creation.

```sql
-- Add a check constraint to ensure salary is positive
ALTER TABLE employees
ADD CONSTRAINT chk_salary_positive
CHECK (salary > 0);

-- Drop the salary check constraint
ALTER TABLE employees
DROP CONSTRAINT chk_salary_positive;
```

## DROP & TRUNCATE

### DROP Objects

Permanently remove tables or other schema objects.

```sql
-- Drop the temporary table if it exists
DROP TABLE IF EXISTS temp_sales;
```

### TRUNCATE vs DELETE

Remove all rows quickly (TRUNCATE) versus row-by-row (DELETE).

```sql
-- Fast removal of all rows; cannot be rolled back in some systems
TRUNCATE TABLE employees;

-- Standard row deletion; can be rolled back and faster with fewer rows
DELETE FROM employees;
```

## Rename and CTAS

### RENAME TABLE/COLUMN

Adjust object names to reflect evolving requirements.

```sql
-- Rename table from 'employees' to 'staff'
ALTER TABLE employees
RENAME TO staff;

-- Rename column from 'emp_id' to 'staff_id'
ALTER TABLE staff
RENAME COLUMN emp_id TO staff_id;
```

### CREATE TABLE AS SELECT (CTAS)

Clone structure and data from an existing query.

```sql
-- Create backup of high-salary employees
CREATE TABLE high_earners AS
SELECT *
FROM employees
WHERE salary > 100000;
```

## Sequences & Identity Columns

### CREATE SEQUENCE

Generate unique numeric values independent of tables.

```sql
-- Create a sequence for order numbers
CREATE SEQUENCE order_seq
START WITH 1000
INCREMENT BY 1
MINVALUE 1000
MAXVALUE 9999
CACHE 20;
```

### IDENTITY Columns

Auto-increment column values within a table.

```sql
-- Use identity column for customer IDs
CREATE TABLE customers (
    customer_id INT GENERATED ALWAYS AS IDENTITY, -- Auto-increment
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
