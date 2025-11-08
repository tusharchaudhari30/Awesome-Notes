# Chapter 9: Normalization & Schema Design

Normalization is the systematic process of organizing data in a relational database to minimize redundancy and dependency. It involves decomposing tables into smaller, well-structured tables and defining relationships between them. The goal is to eliminate data anomalies (insertion, update, deletion) while maintaining data integrity and reducing storage costs.

## Input Tables

```sql
-- unnormalized_student_courses (before normalization)
unnormalized_student_courses:
student_id | student_name | course_id | course_name | instructor_name | department | credits
1001       | Alice Smith  | CS101     | Databases   | Dr. Johnson     | CS         | 3
1001       | Alice Smith  | CS102     | Algorithms  | Dr. Williams    | CS         | 4
1002       | Bob Jones    | CS101     | Databases   | Dr. Johnson     | CS         | 3
1002       | Bob Jones    | MA201     | Calculus    | Dr. Brown       | Math       | 4

-- normalized tables (after normalization)
students:
student_id | student_name
1001       | Alice Smith
1002       | Bob Jones

courses:
course_id | course_name | instructor_name | department | credits
CS101     | Databases   | Dr. Johnson     | CS         | 3
CS102     | Algorithms  | Dr. Williams    | CS         | 4
MA201     | Calculus    | Dr. Brown       | Math       | 4

enrollments:
student_id | course_id | enrollment_date
1001       | CS101     | 2024-01-15
1001       | CS102     | 2024-01-15
1002       | CS101     | 2024-01-16
1002       | MA201     | 2024-01-16
```

## 9.1 Normal Forms

### 9.1.1 First Normal Form (1NF) & Second Normal Form (2NF)

**First Normal Form (1NF)** requires that:

- Each column contains atomic (indivisible) values
- Each column contains values of a single type
- Each column has a unique name
- The order of columns and rows doesn't matter

```sql
-- Violation of 1NF: multiple values in single column
CREATE TABLE students_bad (
    student_id INT,
    student_name VARCHAR(50),
    courses VARCHAR(200)  -- "CS101,CS102,MA201" - NOT atomic
);

-- 1NF compliant: atomic values only
CREATE TABLE student_courses_1nf (
    student_id INT,
    student_name VARCHAR(50),
    course_id VARCHAR(10),
    course_name VARCHAR(50),
    instructor_name VARCHAR(50),
    PRIMARY KEY (student_id, course_id)
);
```

**Second Normal Form (2NF)** requires:

- Must be in 1NF
- No partial dependencies (non-key attributes depend on entire primary key, not just part of it)

```sql
-- 2NF violation analysis: composite key (student_id, course_id)
-- student_name depends only on student_id (partial dependency)
-- course_name depends only on course_id (partial dependency)

-- 2NF solution: separate tables
CREATE TABLE students_2nf (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(50)
);

CREATE TABLE courses_2nf (
    course_id VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR(50),
    instructor_name VARCHAR(50),
    department VARCHAR(10),
    credits INT
);

CREATE TABLE enrollments_2nf (
    student_id INT,
    course_id VARCHAR(10),
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students_2nf(student_id),
    FOREIGN KEY (course_id) REFERENCES courses_2nf(course_id)
);
```

**Output (normalized tables):**

```
students_2nf:
student_id | student_name
1001       | Alice Smith
1002       | Bob Jones

courses_2nf:
course_id | course_name | instructor_name | department | credits
CS101     | Databases   | Dr. Johnson     | CS         | 3
CS102     | Algorithms  | Dr. Williams    | CS         | 4
MA201     | Calculus    | Dr. Brown       | Math       | 4

enrollments_2nf:
student_id | course_id | enrollment_date
1001       | CS101     | 2024-01-15
1001       | CS102     | 2024-01-15
1002       | CS101     | 2024-01-16
1002       | MA201     | 2024-01-16
```

### 9.1.2 Third Normal Form (3NF) & Boyce-Codd Normal Form (BCNF)

**Third Normal Form (3NF)** requires:

- Must be in 2NF
- No transitive dependencies (non-key attributes cannot depend on other non-key attributes)

```sql
-- 3NF violation: instructor_name determines department (transitive dependency)
-- course_id → instructor_name → department

-- 3NF solution: separate instructor information
CREATE TABLE instructors_3nf (
    instructor_id INT PRIMARY KEY,
    instructor_name VARCHAR(50),
    department VARCHAR(10)
);

CREATE TABLE courses_3nf (
    course_id VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR(50),
    instructor_id INT,
    credits INT,
    FOREIGN KEY (instructor_id) REFERENCES instructors_3nf(instructor_id)
);
```

**Boyce-Codd Normal Form (BCNF)** is stricter than 3NF:

- For every functional dependency X → Y, X must be a superkey
- Eliminates anomalies that can still exist in 3NF

```sql
-- BCNF example: consider a table where students can have multiple advisors
-- and advisors can advise in multiple subjects
CREATE TABLE student_advisor_subject (
    student_id INT,
    advisor_id INT,
    subject VARCHAR(50),
    PRIMARY KEY (student_id, advisor_id, subject),
    -- Functional dependency: advisor_id → subject (each advisor specializes in one subject)
    -- But advisor_id is not a superkey, violating BCNF
);

-- BCNF solution: decompose further
CREATE TABLE advisors_bcnf (
    advisor_id INT PRIMARY KEY,
    subject VARCHAR(50)
);

CREATE TABLE student_advisors_bcnf (
    student_id INT,
    advisor_id INT,
    PRIMARY KEY (student_id, advisor_id),
    FOREIGN KEY (advisor_id) REFERENCES advisors_bcnf(advisor_id)
);
```

**Output (BCNF tables):**

```
advisors_bcnf:
advisor_id | subject
201        | Database Systems
202        | Algorithms
203        | Mathematics

student_advisors_bcnf:
student_id | advisor_id
1001       | 201
1001       | 202
1002       | 201
1002       | 203
```

## 9.2 Functional Dependencies

### 9.2.1 Identifying and Testing Functional Dependencies

Functional dependencies (FDs) describe relationships between attributes. X → Y means "X functionally determines Y" - for any two rows with the same X value, the Y values must also be the same.

```sql
-- Example table to analyze FDs
CREATE TABLE employee_projects (
    emp_id INT,
    emp_name VARCHAR(50),
    project_id INT,
    project_name VARCHAR(50),
    hours_worked INT,
    hourly_rate DECIMAL(8,2)
);

-- Functional dependencies identified:
-- emp_id → emp_name (each employee has one name)
-- emp_id → hourly_rate (each employee has one rate)
-- project_id → project_name (each project has one name)
-- emp_id, project_id → hours_worked (hours depend on both employee and project)
```

**Testing FD Violations:**

```sql
-- Test if emp_id → hourly_rate holds
SELECT emp_id, COUNT(DISTINCT hourly_rate) as rate_count
FROM employee_projects
GROUP BY emp_id
HAVING COUNT(DISTINCT hourly_rate) > 1;
-- If this returns rows, the FD is violated
```

**Output (if FD violated):**

```
emp_id | rate_count
105    | 2          -- Employee 105 has different rates in different projects
```

### 9.2.2 Minimal Cover and Inference Rules

A minimal cover is a reduced set of FDs that is equivalent to the original set but with no redundant dependencies.

**Armstrong's Axioms for FD inference:**

- Reflexivity: If Y ⊆ X, then X → Y
- Augmentation: If X → Y, then XZ → YZ
- Transitivity: If X → Y and Y → Z, then X → Z

```sql
-- Example: derive minimal cover
-- Given FDs: {A → BC, B → C, A → B, AB → C}
-- Step 1: Decompose right side: {A → B, A → C, B → C, A → B, AB → C}
-- Step 2: Remove redundant: A → C (redundant due to A → B and B → C)
-- Step 3: Remove AB → C (redundant due to A → B and B → C)
-- Minimal cover: {A → B, B → C}
```

## 9.3 Denormalization

### 9.3.1 Use Cases and Patterns

Denormalization intentionally introduces redundancy to improve query performance, often at the cost of storage space and update complexity.

```sql
-- Normalized (3NF) design
CREATE TABLE orders_normalized (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items_normalized (
    order_id INT,
    item_id INT,
    quantity INT,
    unit_price DECIMAL(8,2),
    PRIMARY KEY (order_id, item_id),
    FOREIGN KEY (order_id) REFERENCES orders_normalized(order_id)
);

-- Denormalized design: add order_total to orders table
CREATE TABLE orders_denormalized (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    order_total DECIMAL(10,2), -- Calculated from order_items
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

**Benefits of denormalization:**

- Faster queries (avoid expensive JOINs)
- Simpler application code
- Better performance for read-heavy workloads

**Drawbacks:**

- Data redundancy and potential inconsistencies
- More complex update operations
- Increased storage requirements

### 9.3.2 Materialized Views vs Redundant Columns

```sql
-- Option 1: Materialized View (preferred for denormalization)
CREATE MATERIALIZED VIEW order_summary AS
SELECT
    o.order_id,
    o.customer_id,
    o.order_date,
    SUM(oi.quantity * oi.unit_price) AS order_total,
    COUNT(oi.item_id) AS item_count
FROM orders_normalized o
JOIN order_items_normalized oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.customer_id, o.order_date;

-- Option 2: Trigger-maintained redundant columns
CREATE TRIGGER update_order_total
AFTER INSERT OR UPDATE OR DELETE ON order_items_normalized
FOR EACH ROW
EXECUTE PROCEDURE recalculate_order_total();
```

## 9.4 Surrogate vs Natural Keys

### 9.4.1 Trade-offs and Stability

**Natural Keys** use business-meaningful data as primary keys.

```sql
-- Natural key example: using SSN
CREATE TABLE employees_natural (
    ssn VARCHAR(11) PRIMARY KEY,  -- Natural key
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100)
);
```

**Surrogate Keys** use system-generated values with no business meaning.

```sql
-- Surrogate key example: auto-increment ID
CREATE TABLE employees_surrogate (
    emp_id INT IDENTITY(1,1) PRIMARY KEY,  -- Surrogate key
    ssn VARCHAR(11) UNIQUE,                -- Natural key as alternate key
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100)
);
```

**Output comparison:**

```
employees_natural:
ssn         | first_name | last_name | email
123-45-6789 | John       | Doe       | john@company.com

employees_surrogate:
emp_id | ssn         | first_name | last_name | email
1001   | 123-45-6789 | John       | Doe       | john@company.com
```

### 9.4.2 Impact on Joins and Indexes

```sql
-- Performance comparison: surrogate vs natural keys in joins
-- Surrogate key join (typically faster - integer comparison)
SELECT e.first_name, d.dept_name
FROM employees_surrogate e
JOIN departments d ON e.dept_id = d.dept_id;  -- Integer join

-- Natural key join (potentially slower - string comparison)
SELECT e.first_name, d.dept_name
FROM employees_natural_alt e
JOIN departments_natural d ON e.dept_code = d.dept_code;  -- String join
```

## 9.5 ER-to-Relational Mapping

### 9.5.1 One-to-One, One-to-Many, Many-to-Many Relationships

**One-to-One:** Each entity instance relates to exactly one instance of another entity.

```sql
-- One-to-One: Employee to Office Assignment
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE offices (
    office_id INT PRIMARY KEY,
    location VARCHAR(50),
    emp_id INT UNIQUE,  -- Foreign key with UNIQUE constraint
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);
```

**One-to-Many:** One entity instance relates to multiple instances of another entity.

```sql
-- One-to-Many: Department to Employees
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(50)
);

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(50),
    dept_id INT,  -- Foreign key (no UNIQUE constraint)
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);
```

### 9.5.2 Junction Tables and Constraints

**Many-to-Many:** Multiple instances of each entity can relate to multiple instances of the other.

```sql
-- Many-to-Many: Students to Courses (requires junction table)
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(50)
);

CREATE TABLE courses (
    course_id VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR(50)
);

CREATE TABLE student_courses (
    student_id INT,
    course_id VARCHAR(10),
    enrollment_date DATE,
    grade CHAR(2),
    PRIMARY KEY (student_id, course_id),  -- Composite primary key
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

**Output (Many-to-Many implementation):**

```
students:
student_id | student_name
1001       | Alice Smith
1002       | Bob Jones

courses:
course_id | course_name
CS101     | Databases
CS102     | Algorithms
MA201     | Calculus

student_courses:
student_id | course_id | enrollment_date | grade
1001       | CS101     | 2024-01-15      | A
1001       | CS102     | 2024-01-15      | B+
1002       | CS101     | 2024-01-16      | A-
1002       | MA201     | 2024-01-16      | B
```

## Common Interview Scenarios

### Normalization Process Example

```sql
-- Step-by-step normalization of a problematic table
-- Original table (violates multiple normal forms)
CREATE TABLE course_registration_bad (
    reg_id INT,
    student_id INT,
    student_name VARCHAR(50),
    student_major VARCHAR(30),
    course_id VARCHAR(10),
    course_name VARCHAR(50),
    instructor_name VARCHAR(50),
    instructor_dept VARCHAR(20),
    semester VARCHAR(10),
    grade CHAR(2)
);

-- Problems identified:
-- 1NF: All columns are atomic ✓
-- 2NF: student_name depends only on student_id (partial dependency) ✗
-- 3NF: instructor_dept depends on instructor_name (transitive dependency) ✗

-- Final normalized design (3NF)
CREATE TABLE students_final (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(50),
    student_major VARCHAR(30)
);

CREATE TABLE instructors_final (
    instructor_id INT PRIMARY KEY,
    instructor_name VARCHAR(50),
    instructor_dept VARCHAR(20)
);

CREATE TABLE courses_final (
    course_id VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR(50),
    instructor_id INT,
    FOREIGN KEY (instructor_id) REFERENCES instructors_final(instructor_id)
);

CREATE TABLE registrations_final (
    reg_id INT PRIMARY KEY,
    student_id INT,
    course_id VARCHAR(10),
    semester VARCHAR(10),
    grade CHAR(2),
    FOREIGN KEY (student_id) REFERENCES students_final(student_id),
    FOREIGN KEY (course_id) REFERENCES courses_final(course_id)
);
```

This normalization eliminates update anomalies, reduces data redundancy, and ensures data consistency while maintaining all original information through proper relationships.
