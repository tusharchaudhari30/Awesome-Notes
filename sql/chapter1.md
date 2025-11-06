# Relational Model & Architecture

## Definitions

### Relation, Tuple, Attribute

- A relation is a table with a defined structure where each row represents a tuple and each column represents an attribute.
- Tuples are unordered rows; attributes have domains that constrain permissible values.
- Relations follow properties like unique rows, atomic (indivisible) attribute values, and no ordering guarantees for rows or columns.

### Relational Algebra Basics

- Core operators: selection (filter rows), projection (select columns), union, set difference, Cartesian product, and rename.
- Derived operators: join (theta, equi, natural), intersection, division, and outer joins.
- Algebra underpins query optimization and reasoning about equivalences and transformations.

## Three-Schema Architecture

### Internal Schema

- Physical storage view: files, pages, indexes, partitioning, and access paths.
- Concerns include I/O patterns, compression, and storage engines.

### Conceptual Schema

- Logical database view shared across applications: entities, relationships, constraints.
- Captures global structure independent of physical details.

### External Schema

- Multiple user/application-specific views that expose subsets or transformations of the conceptual schema.
- Implemented via views, permissions, and API-level projections.

## Codd’s 12 Rules

### Information, Guaranteed Access, NULL Treatment

- All data represented as values in tables; each fact accessible by table name, primary key, and column name.
- NULLs represent missing/unknown/inapplicable and must be systematically treated in operations and constraints.

### Data Sublanguage, View Update Rule

- A comprehensive relational sublanguage supports definition, manipulation, integrity, and transaction control.
- Updatable views reflect changes back to base tables when criteria are satisfied.

## ER Modeling

### Entities, Attributes, Relationships

- Entities model real-world concepts; attributes describe them; relationships capture associations (1:1, 1:N, M:N).
- Keys (primary, candidate) uniquely identify entity instances.

### Weak Entities and Identifying Relationships

- Weak entities depend on strong entities, using partial keys plus owner’s key.
- Identifying relationships enforce existence and cascading integrity.

## Common Interview Pitfalls

### Concept vs Implementation

- Confusing logical relations with physical tables and assuming row/column order is guaranteed.

### NULL and Keys

- Using NULLs in primary keys or misunderstanding how NULLs affect joins, aggregates, and predicates.

## Quick SQL Examples

### Selection and Projection

```sql
-- Select employees in Sales, projecting only id and name
SELECT emp_id, emp_name
FROM employees
WHERE department = 'Sales';
```

### Basic Join (Conceptual to Relational)

```sql
-- Employees with their department names (1:N relationship)
SELECT e.emp_id, e.emp_name, d.dept_name
FROM employees AS e
JOIN departments AS d
  ON e.dept_id = d.dept_id;
```

### Updatable View Example

```sql
CREATE VIEW sales_staff AS
SELECT emp_id, emp_name, dept_id
FROM employees
WHERE department = 'Sales';

-- If engine permits and constraints are satisfied:
UPDATE sales_staff
SET emp_name = 'Anya Gupta'
WHERE emp_id = 104;
```

### Handling NULLs Carefully

```sql
-- Count employees with and without phone numbers
SELECT
  COUNT(*) AS total_employees,
  COUNT(phone) AS with_phone,
  COUNT(*) - COUNT(phone) AS without_phone
FROM employees;
```

### Key Concepts Checklist

- Relations are sets of tuples with atomic attributes; no implicit ordering.
- Relational algebra operators and their equivalences guide optimization.
- Three-schema separation: internal vs conceptual vs external views.
- Codd’s rules motivate consistent, declarative data management.
- ER modeling drives logical design; keys anchor identity and integrity.
