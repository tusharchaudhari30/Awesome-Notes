# Chapter 12: Indexing Strategies & Performance Tuning

Indexing is fundamental for database performance, enabling fast access to rows and efficient query execution. Well-designed indexes can dramatically speed up SELECT queries, joins, and filtering, while excessive or poorly chosen indexes may slow down data modifications (INSERT/UPDATE/DELETE) and waste resources. Performance tuning balances query speed, update costs, and resource usage across real-world workloads.

---

## Input Tables

```sql
-- products table
products:
product_id | product_name | category | price | stock | rowversion
501        | Widget A     | Electronics | 150.00 | 10 | 2
502        | Widget B     | Electronics | 99.99  | 50 | 4
503        | Widget C     | Sports      | 45.00  | 100 | 3

-- sales table
sales:
sale_id | product_id | sale_date  | amount
10001   | 501        | 2024-01-10 | 2
10002   | 501        | 2024-01-11 | 3
10003   | 502        | 2024-01-12 | 1
10004   | 503        | 2024-01-15 | 4
```

## 12.1 Index Types

### 12.1.1 B-Tree, Hash, Bitmap Indexes

- **B-Tree Indexes** are balanced tree structures used for fast range and equality searches. Most default index type in modern relational databases.
- **Hash Indexes** offer fast equality searches but don’t support range queries; common in in-memory and NoSQL databases.
- **Bitmap Indexes** use bitmap vectors for categorical data with low cardinality, efficient for complex multi-column filtering.

```sql
-- Create B-tree index (most common)
CREATE INDEX idx_products_name ON products(product_name);

-- Hash index (PostgreSQL-specific syntax)
CREATE INDEX idx_products_id_hash ON products USING HASH(product_id);

-- Bitmap index (Oracle syntax - cannot create explicitly in all RDBMS)
CREATE BITMAP INDEX idx_products_category ON products(category);
```

**Output (effect):**

- Queries searching by product_name or product_id are much faster.
- Category-based queries benefit from compact bitmaps.

---

### 12.1.2 Full-Text and Spatial Indexes

- **Full-Text Indexes** enable fast searching within large text columns (documents, descriptions).
- **Spatial Indexes** support efficient querying of geometric data (location, shape).

```sql
-- Full-text index for searching product descriptions
CREATE FULLTEXT INDEX idx_products_desc ON products(product_description);

-- Spatial index for location
CREATE SPATIAL INDEX idx_store_location ON stores(location);
```

**Output:**

- Text and location-based searches complete rapidly.

---

## 12.2 Composite & Covering Indexes

### 12.2.1 Column Order and Selectivity

- A **composite index** spans multiple columns; order matters: queries can use leading columns efficiently.
- **Selectivity** is the proportion of unique values, higher selectivity yields better performance.

```sql
-- Composite index for frequent search
CREATE INDEX idx_sales_product_date ON sales(product_id, sale_date);
```

**Output:**

- Queries filtering by product_id and ordering by sale_date are accelerated.
- Only queries matching the leading column(s) use the index well.

---

### 12.2.2 Read vs Write Trade-Offs

- More indexes = faster reads, but slower writes (because every index must be updated when data changes).
- Analyze workload: OLTP favors balanced indexing, OLAP favors heavy indexing for quick reads.

---

## 12.3 Query Plan Analysis

### 12.3.1 EXPLAIN/EXPLAIN ANALYZE

Query planners determine the fastest data access strategies. Use `EXPLAIN` to view the plan and optimize queries.

```sql
EXPLAIN SELECT * FROM sales WHERE product_id = 501;
```

**Output:**

- Plan shows if an index is used or if a full table scan occurs.

### 12.3.2 Operator Costs & Bottlenecks

The plan details cost estimates and highlights expensive steps (joins, sorts, scans). Tuning means reducing these costs.

---

## 12.4 Clustered vs Nonclustered Indexes

### 12.4.1 Storage and Ordering Implications

- **Clustered Index** sorts the physical table on the index columns (one per table).
- **Nonclustered Index** is a separate structure pointing to table rows.

```sql
-- Clustered index (SQL Server syntax; most tables have a default clustered index on PK)
CREATE CLUSTERED INDEX idx_products_price ON products(price);

-- Nonclustered index
CREATE NONCLUSTERED INDEX idx_products_stock ON products(stock);
```

**Output:**

- Range queries over price use physical ordering.
- Stock lookups use the separate index for quick navigation.

---

### 12.4.2 Seek vs Scan Behaviors

- Seek: Jumps straight to matching rows via index
- Scan: Reads every row, slower for large tables

Tuned indexes turn scans into seeks, reducing query times.

---

## 12.5 SARGability

### 12.5.1 Avoid Functions on Indexed Columns

**SARGable**: "Search Argument Able"—queries that can use indexes.

- Expressions applied to indexed columns (like `LOWER()`, `CAST()`) prevent index usage.

```sql
-- Index not used (non-SARGable)
SELECT * FROM products WHERE LOWER(product_name) = 'widget a';

-- Index used (SARGable)
SELECT * FROM products WHERE product_name = 'Widget A';
```

### 12.5.2 Predicate Rewrites for Index Usage

Rewrite queries to make them SARGable—move functions to constants.

```sql
-- Not SARGable: index can't help
SELECT * FROM products WHERE YEAR(created_at) = 2024;

-- SARGable rewrite:
SELECT * FROM products WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';
```

**Output:**

- The rewritten query uses the index for efficient date range filtering.

---

## Performance Tuning Best Practices

- Create indexes on columns used for filtering, joining, and sorting.
- Review and prune unused indexes to accelerate writes.
- Periodically run `ANALYZE` and update statistics for accurate plans.
- Use composite and covering indexes for complex queries.
- Always check query plans and adapt indexing based on actual workload performance.

**Summary:**  
A strategic indexing plan dramatically boosts database performance and scalability. Thoughtful use—balancing query speed, modification costs, and SARGability—ensures responsive applications and manageable maintenance.
