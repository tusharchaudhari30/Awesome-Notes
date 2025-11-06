# Keys & Integrity Constraints

## Key Types

### Primary, Candidate, Alternate Keys

A **primary key** uniquely identifies each row in a table and cannot contain NULL values. **Candidate keys** are all possible unique identifiers for a table, while **alternate keys** are candidate keys not chosen as the primary key.

```sql
-- Example table with multiple candidate keys
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,           -- Primary key chosen from candidates
    ssn VARCHAR(11) UNIQUE NOT NULL,  -- Alternate key (candidate key)
    email VARCHAR(100) UNIQUE NOT NULL, -- Another alternate key
    emp_name VARCHAR(50) NOT NULL,
    department VARCHAR(30)
);

-- Insert valid data
INSERT INTO employees VALUES
(101, '123-45-6789', 'john.doe@company.com', 'John Doe', 'Engineering'),
(102, '987-65-4321', 'jane.smith@company.com', 'Jane Smith', 'Marketing');

-- This would fail due to primary key violation
-- INSERT INTO employees VALUES (101, '111-11-1111', 'duplicate@company.com', 'Duplicate ID', 'Sales');

-- This would fail due to alternate key (email) violation
-- INSERT INTO employees VALUES (103, '555-55-5555', 'john.doe@company.com', 'Another John', 'Sales');
```

### Foreign Keys

Foreign keys establish and maintain referential integrity between tables by ensuring values in the referencing table exist in the referenced table.

```sql
-- Parent table (referenced)
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL,
    manager_id INT
);

-- Child table (referencing)
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50) NOT NULL,
    dept_id INT,                      -- Foreign key column
    salary DECIMAL(10,2),
    CONSTRAINT fk_emp_dept
        FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

-- Insert departments first (parent)
INSERT INTO departments VALUES
(1, 'Engineering', NULL),
(2, 'Marketing', NULL),
(3, 'Sales', NULL);

-- Insert employees with valid dept_id references
INSERT INTO employees VALUES
(101, 'Alice Johnson', 1, 75000.00),    -- Valid: dept_id 1 exists
(102, 'Bob Wilson', 2, 65000.00),       -- Valid: dept_id 2 exists
(103, 'Carol Davis', 1, 80000.00);      -- Valid: dept_id 1 exists

-- This would fail due to foreign key constraint violation
-- INSERT INTO employees VALUES (104, 'Dave Brown', 99, 70000.00);  -- dept_id 99 doesn't exist
```

### Composite Keys

Composite keys use multiple columns together to uniquely identify rows, often used in junction tables for many-to-many relationships.

```sql
-- Junction table for many-to-many relationship between students and courses
CREATE TABLE student_courses (
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date DATE NOT NULL,
    grade CHAR(2),
    -- Composite primary key: combination of student_id and course_id must be unique
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Order details table with composite key
CREATE TABLE order_items (
    order_id INT NOT NULL,
    item_number INT NOT NULL,       -- Sequential item number within each order
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(8,2) NOT NULL,
    -- Composite primary key ensures unique item number per order
    PRIMARY KEY (order_id, item_number),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Insert sample data
INSERT INTO order_items VALUES
(1001, 1, 501, 2, 25.99),    -- Order 1001, Item 1
(1001, 2, 502, 1, 45.50),    -- Order 1001, Item 2
(1002, 1, 501, 3, 25.99),    -- Order 1002, Item 1 (same product, different order)
(1002, 2, 503, 1, 15.75);    -- Order 1002, Item 2

-- This would fail - duplicate composite key
-- INSERT INTO order_items VALUES (1001, 1, 504, 1, 12.00);  -- order_id=1001, item_number=1 already exists
```

## Constraint Types

### Unique Constraints

Unique constraints ensure no duplicate values in specified columns, allowing NULL values (unlike primary keys).

```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) UNIQUE,        -- Simple unique constraint (allows NULL)
    tax_id VARCHAR(20) UNIQUE,       -- Another unique constraint
    email VARCHAR(100),
    address VARCHAR(200),
    -- Named unique constraint on combination of columns
    CONSTRAINT uk_customer_name_address UNIQUE (customer_name, address)
);

-- Valid inserts
INSERT INTO customers VALUES
(1, 'ABC Corp', '555-1234', 'TAX123', 'contact@abc.com', '123 Main St'),
(2, 'XYZ Inc', NULL, 'TAX456', 'info@xyz.com', '456 Oak Ave'),    -- NULL phone is allowed
(3, 'ABC Corp', '555-9999', 'TAX789', 'sales@abc.com', '789 Pine Rd'); -- Same name, different address

-- This would fail due to unique constraint violation
-- INSERT INTO customers VALUES (4, 'DEF Ltd', '555-1234', 'TAX999', 'def@def.com', '999 Elm St');
```

### Check Constraints

Check constraints enforce domain integrity by restricting values to meet specified conditions.

```sql
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    discount_percent DECIMAL(5,2) DEFAULT 0,
    category VARCHAR(30) NOT NULL,
    status VARCHAR(10) DEFAULT 'ACTIVE',

    -- Check constraints with descriptive names
    CONSTRAINT chk_price_positive
        CHECK (price > 0),                                    -- Price must be positive

    CONSTRAINT chk_discount_range
        CHECK (discount_percent >= 0 AND discount_percent <= 100), -- Discount 0-100%

    CONSTRAINT chk_valid_category
        CHECK (category IN ('Electronics', 'Clothing', 'Books', 'Home', 'Sports')),

    CONSTRAINT chk_valid_status
        CHECK (status IN ('ACTIVE', 'INACTIVE', 'DISCONTINUED'))
);

-- Valid inserts
INSERT INTO products VALUES
(1, 'Laptop', 999.99, 10.0, 'Electronics', 'ACTIVE'),
(2, 'T-Shirt', 19.99, 0, 'Clothing', 'ACTIVE'),
(3, 'Novel', 12.50, 15.0, 'Books', 'ACTIVE');

-- These would fail due to check constraint violations:
-- INSERT INTO products VALUES (4, 'Invalid Price', -50.00, 0, 'Electronics', 'ACTIVE');  -- Negative price
-- INSERT INTO products VALUES (5, 'Invalid Discount', 25.00, 150, 'Electronics', 'ACTIVE'); -- Discount > 100%
-- INSERT INTO products VALUES (6, 'Invalid Category', 50.00, 0, 'InvalidCat', 'ACTIVE');   -- Invalid category
```

### Not-Null Constraints

Not-null constraints ensure required fields always have values, preventing NULL assignments.

```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,              -- Must have customer
    order_date DATE NOT NULL DEFAULT CURRENT_DATE, -- Must have date, defaults to today
    ship_date DATE,                        -- Optional - can be NULL until shipped
    total_amount DECIMAL(10,2) NOT NULL,   -- Must have total
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING', -- Must have status, defaults to PENDING

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Valid insert with required fields
INSERT INTO orders (order_id, customer_id, total_amount)
VALUES (1001, 1, 150.75);  -- order_date and status get default values

-- Valid insert with all fields
INSERT INTO orders VALUES
(1002, 2, '2024-01-15', '2024-01-17', 89.50, 'SHIPPED');

-- These would fail due to NOT NULL violations:
-- INSERT INTO orders (order_id, order_date, total_amount) VALUES (1003, '2024-01-16', 200.00);  -- Missing customer_id
-- INSERT INTO orders (order_id, customer_id) VALUES (1004, 1);  -- Missing total_amount
```

### Default Constraints

Default constraints provide automatic values when no explicit value is provided during insertion.

```sql
CREATE TABLE user_accounts (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    -- Auto-set to current time
    last_login TIMESTAMP,                                -- Can be NULL initially
    account_status VARCHAR(10) DEFAULT 'ACTIVE',         -- Defaults to ACTIVE
    login_attempts INT DEFAULT 0,                        -- Defaults to 0
    is_verified BOOLEAN DEFAULT FALSE                    -- Defaults to FALSE
);

-- Insert with minimal required data - defaults will be applied
INSERT INTO user_accounts (user_id, username, email)
VALUES (1, 'john_doe', 'john@example.com');
-- created_date = current timestamp, account_status = 'ACTIVE', login_attempts = 0, is_verified = FALSE

-- Insert overriding some defaults
INSERT INTO user_accounts (user_id, username, email, account_status, is_verified)
VALUES (2, 'jane_smith', 'jane@example.com', 'PENDING', TRUE);

-- Query to see the results
SELECT user_id, username, created_date, account_status, login_attempts, is_verified
FROM user_accounts;
```

## Referential Actions

### ON DELETE/UPDATE CASCADE/SET NULL/RESTRICT

Referential actions define what happens to child records when parent records are modified or deleted.

```sql
-- Parent table
CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL
);

-- Child table with different referential actions
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category_id INT,
    supplier_id INT,

    -- CASCADE: Delete products when category is deleted
    CONSTRAINT fk_product_category
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON DELETE CASCADE ON UPDATE CASCADE,

    -- SET NULL: Set supplier_id to NULL when supplier is deleted
    CONSTRAINT fk_product_supplier
        FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Sample data setup
INSERT INTO categories VALUES (1, 'Electronics'), (2, 'Books');
INSERT INTO suppliers VALUES (10, 'Tech Supplier'), (20, 'Book Supplier');
INSERT INTO products VALUES
(101, 'Laptop', 1, 10),
(102, 'Smartphone', 1, 10),
(103, 'Novel', 2, 20);

-- Demonstrate CASCADE: Deleting category deletes all its products
DELETE FROM categories WHERE category_id = 1;
-- Products 101 and 102 are automatically deleted

-- Demonstrate SET NULL: Deleting supplier sets supplier_id to NULL
DELETE FROM suppliers WHERE supplier_id = 20;
-- Product 103's supplier_id becomes NULL, but product remains
```

### Deferrable and Initially Deferred Constraints

Deferrable constraints can be checked at transaction end rather than immediately, useful for complex multi-table operations.

```sql
-- Enable deferred constraint checking (PostgreSQL syntax)
CREATE TABLE parent_table (
    id INT PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE child_table (
    id INT PRIMARY KEY,
    parent_id INT,
    CONSTRAINT fk_child_parent
        FOREIGN KEY (parent_id) REFERENCES parent_table(id)
        DEFERRABLE INITIALLY DEFERRED  -- Check at transaction end
);

-- Transaction that would fail with immediate checking
BEGIN;
    -- Insert child first (normally would fail foreign key check)
    INSERT INTO child_table VALUES (1, 100);

    -- Insert parent later in same transaction
    INSERT INTO parent_table VALUES (100, 'Parent Name');
COMMIT;  -- Constraints checked here - transaction succeeds

-- Alternative: Set constraint checking mode within transaction
BEGIN;
    SET CONSTRAINTS ALL DEFERRED;  -- Defer all deferrable constraints

    -- Complex operations that might temporarily violate constraints
    UPDATE parent_table SET id = 200 WHERE id = 100;
    UPDATE child_table SET parent_id = 200 WHERE parent_id = 100;

COMMIT;  -- All constraints validated at commit time
```

## Common Interview Scenarios

### Choosing Primary vs Alternate Keys

```sql
-- Decision factors for key selection
CREATE TABLE customers (
    -- Option 1: Surrogate key (recommended for most cases)
    customer_id INT IDENTITY(1,1) PRIMARY KEY,  -- Auto-incrementing, stable

    -- Option 2: Natural key candidates
    ssn VARCHAR(11) UNIQUE NOT NULL,           -- Alternate key - private, may change
    email VARCHAR(100) UNIQUE NOT NULL,        -- Alternate key - can change

    customer_name VARCHAR(100) NOT NULL
);
-- Primary key choice: customer_id (surrogate) - stable, simple, performance-friendly
-- Alternate keys: ssn, email - business-meaningful but potentially volatile
```

### Composite Key Design Patterns

```sql
-- Time-series data with composite key
CREATE TABLE sensor_readings (
    sensor_id INT NOT NULL,
    timestamp DATETIME NOT NULL,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),

    PRIMARY KEY (sensor_id, timestamp),  -- Composite key prevents duplicate readings
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id)
);

-- Avoid common composite key mistakes:
-- ❌ Including auto-increment column in composite key
-- ❌ Too many columns (impacts performance)
-- ❌ Using mutable columns (business codes that might change)
-- ✅ Use immutable, meaningful columns that reflect natural uniqueness
```
