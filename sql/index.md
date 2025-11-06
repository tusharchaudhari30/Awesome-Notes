# Complete Table of Contents - RDBMS, SQL & NoSQL Interview Preparation

## 1. Relational Model & Architecture

1.1 Definitions  
 1.1.1 Relation, Tuple, Attribute  
 1.1.2 Relational Algebra Basics  
1.2 Three-Schema Architecture  
 1.2.1 Internal Schema  
 1.2.2 Conceptual Schema  
 1.2.3 External Schema  
1.3 Codd's 12 Rules  
 1.3.1 Information, Guaranteed Access, NULL treatment  
 1.3.2 Data sublanguage, View update rule  
1.4 ER Modeling  
 1.4.1 Entities, Attributes, Relationships  
 1.4.2 Weak Entities and Identifying Relationships

## 2. Keys & Integrity Constraints

2.1 Key Types  
 2.1.1 Primary, Candidate, Alternate Keys  
 2.1.2 Foreign Keys  
 2.1.3 Composite Keys: definition, creation, dependencies  
2.2 Constraint Types  
 2.2.1 Unique Constraints  
 2.2.2 Check Constraints  
 2.2.3 Not-Null Constraints  
 2.2.4 Default Constraints  
2.3 Referential Actions  
 2.3.1 ON DELETE/UPDATE CASCADE/SET NULL/RESTRICT  
 2.3.2 Deferrable and Initially Deferred Constraints

## 3. SQL Data Definition Language (DDL)

3.1 CREATE Statements  
 3.1.1 CREATE TABLE with Constraints  
 3.1.2 CREATE VIEW and CREATE INDEX  
3.2 ALTER Statements  
 3.2.1 ADD/DROP Column  
 3.2.2 ADD/DROP/MODIFY Constraints  
3.3 DROP & TRUNCATE  
 3.3.1 DROP Objects (CASCADE vs RESTRICT)  
 3.3.2 TRUNCATE vs DELETE  
3.4 Rename and CTAS  
 3.4.1 RENAME TABLE/COLUMN patterns  
 3.4.2 CREATE TABLE AS SELECT (with/without data)  
3.5 Sequences & Identity Columns  
 3.5.1 CREATE SEQUENCE, NEXTVAL/CURRVAL  
 3.5.2 IDENTITY columns and gap management

## 4. SQL Data Manipulation Language (DML)

4.1 INSERT Operations  
 4.1.1 Single-row vs Multi-row Inserts  
 4.1.2 Bulk Loads and Performance  
4.2 UPDATE Techniques  
 4.2.1 UPDATE with JOINs  
 4.2.2 UPDATE with Subqueries  
4.3 DELETE & MERGE  
 4.3.1 DELETE vs TRUNCATE  
 4.3.2 MERGE (Upsert) patterns  
4.4 Transactional DML  
 4.4.1 Savepoints & Nested Transactions  
 4.4.2 Error Handling and Rollbacks  
4.5 Temporary Objects  
 4.5.1 Temporary Tables and Table Variables  
 4.5.2 CTEs vs Temp Tables trade-offs

## 5. Joins & Set Operations

5.1 Join Types  
 5.1.1 Inner, Left, Right, Full Joins  
 5.1.2 Cross & Self-Joins  
 5.1.3 Semi-Join and Anti-Join via EXISTS/NOT EXISTS  
5.2 Set Operators  
 5.2.1 UNION vs UNION ALL  
 5.2.2 INTERSECT & EXCEPT  
5.3 Performance Considerations  
 5.3.1 Join Order and Join Hints  
 5.3.2 Index Usage and Statistics  
5.4 Lateral Joins  
 5.4.1 CROSS APPLY/OUTER APPLY  
 5.4.2 UNNEST/ARRAY operations (engine-specific)

## 6. Aggregation & Grouping

6.1 GROUP BY & HAVING  
 6.1.1 Basic GROUP BY  
 6.1.2 HAVING Filters  
6.2 Aggregate Functions  
 6.2.1 SUM, COUNT, AVG  
 6.2.2 MIN, MAX, STDDEV, VARIANCE  
6.3 Advanced Grouping  
 6.3.1 ROLLUP & CUBE  
 6.3.2 GROUPING SETS & GROUPING_ID  
6.4 DISTINCT vs GROUP BY  
 6.4.1 De-duplication semantics  
 6.4.2 Performance trade-offs

## 7. Subqueries & Common Table Expressions (CTEs)

7.1 Subquery Types  
 7.1.1 Single-row vs Multi-row  
 7.1.2 Correlated vs Uncorrelated  
7.2 CTEs  
 7.2.1 Non-recursive CTEs for modularity  
 7.2.2 Recursive CTEs for hierarchies  
7.3 Derived Tables & Inline Views  
 7.3.1 When to prefer derived tables  
 7.3.2 Inlining vs materialization

## 8. Window Functions & Analytics

8.1 Ranking Functions  
 8.1.1 ROW_NUMBER(), RANK(), DENSE_RANK()  
 8.1.2 NTILE() distributions  
8.2 Aggregate OVER()  
 8.2.1 SUM() OVER partitions  
 8.2.2 AVG() OVER orderings  
8.3 Window Clauses  
 8.3.1 PARTITION BY  
 8.3.2 ORDER BY and frame (ROWS vs RANGE)  
8.4 Analytical Patterns  
 8.4.1 Running totals and moving averages  
 8.4.2 Gaps-and-islands problems

## 9. Normalization & Schema Design

9.1 Normal Forms  
 9.1.1 1NF & 2NF  
 9.1.2 3NF & BCNF  
9.2 Functional Dependencies  
 9.2.1 Identifying and testing FDs  
 9.2.2 Minimal cover and inference rules  
9.3 Denormalization  
 9.3.1 Use cases and patterns  
 9.3.2 MVs vs redundant columns  
9.4 Surrogate vs Natural Keys  
 9.4.1 Trade-offs and stability  
 9.4.2 Impact on joins and indexes  
9.5 ER-to-Relational Mapping  
 9.5.1 One-to-one, one-to-many, many-to-many  
 9.5.2 Junction tables and constraints

## 10. Transactions & ACID Properties

10.1 Transaction Lifecycle  
 10.1.1 BEGIN, COMMIT, ROLLBACK  
 10.1.2 Savepoints and nesting  
10.2 ACID Guarantees  
 10.2.1 Atomicity & Consistency  
 10.2.2 Isolation & Durability  
 10.2.3 WAL and crash recovery basics  
10.3 Two-Phase Commit (2PC)  
 10.3.1 Prepare and commit phases  
 10.3.2 Coordinator failures and recovery  
10.4 Isolation Anomalies  
 10.4.1 Dirty, Non-repeatable, Phantom reads  
 10.4.2 Lost update and write skew

## 11. Concurrency Control & Locking

11.1 Locking Mechanisms  
 11.1.1 Pessimistic vs Optimistic  
 11.1.2 Row, Page, Table locks  
11.2 Deadlocks  
 11.2.1 Detection algorithms  
 11.2.2 Resolution strategies  
11.3 MVCC & Snapshot Isolation  
 11.3.1 Version chains and readers-writers  
 11.3.2 Phantom prevention approaches  
11.4 Optimistic Concurrency Tokens  
 11.4.1 Rowversion/timestamp, ETags  
 11.4.2 Compare-and-swap patterns

## 12. Indexing Strategies & Performance Tuning

12.1 Index Types  
 12.1.1 B-Tree, Hash, Bitmap  
 12.1.2 Full-Text and Spatial Indexes  
12.2 Composite & Covering Indexes  
 12.2.1 Column order and selectivity  
 12.2.2 Read vs write trade-offs  
12.3 Query Plan Analysis  
 12.3.1 EXPLAIN/EXPLAIN ANALYZE  
 12.3.2 Operator costs and bottlenecks  
12.4 Clustered vs Nonclustered Indexes  
 12.4.1 Storage and ordering implications  
 12.4.2 Seek vs scan behaviors  
12.5 SARGability  
 12.5.1 Avoid functions on indexed columns  
 12.5.2 Predicate rewrites for index usage

## 13. Query Execution & Optimization

13.1 Execution Phases  
 13.1.1 Parsing & Validation  
 13.1.2 Optimization & Plan Generation  
 13.1.3 Execution & Result Retrieval  
13.2 Plans & Join Algorithms  
 13.2.1 Logical vs Physical Operators  
 13.2.2 Nested Loop, Hash, Merge Joins  
13.3 Hints & Rewriting  
 13.3.1 Index and join hints  
 13.3.2 Query refactoring patterns  
13.4 Engine-Specific Top-N & Pagination  
 13.4.1 LIMIT/OFFSET, TOP, FETCH FIRST  
 13.4.2 Keyset pagination for performance  
13.5 Statistics Management  
 13.5.1 Auto-stats and stale stats issues  
 13.5.2 Cardinality estimation pitfalls

## 14. Views, Materialized Views & Stored Procedures

14.1 Views  
 14.1.1 Inline vs Indexed Views  
 14.1.2 Security/ownership chaining  
14.2 Materialized Views  
 14.2.1 Refresh on commit/interval/manual  
 14.2.2 Storage and staleness trade-offs  
14.3 Stored Procedures & Functions  
 14.3.1 Parameters, overloading, errors  
 14.3.2 Transaction scope and side-effects  
14.4 MERGE/Upsert Patterns  
 14.4.1 Idempotent designs  
 14.4.2 Constraint interactions

## 15. Triggers & User-Defined Functions

15.1 Triggers  
 15.1.1 BEFORE, AFTER, INSTEAD OF  
 15.1.2 Auditing, cascades, validations  
15.2 Functions  
 15.2.1 Scalar, Inline Table, Multi-Statement  
 15.2.2 Deterministic vs Non-Deterministic  
15.3 Audit & Automation Patterns  
 15.3.1 Change logging strategies  
 15.3.2 Pitfalls and performance costs

## 16. NoSQL Databases Overview

16.1 Characteristics  
 16.1.1 Schema flexibility and agility  
 16.1.2 Horizontal scaling and partitioning  
16.2 NoSQL Types  
 16.2.1 Key-Value  
 16.2.2 Document, Column-Family, Graph  
16.3 Data Modeling Basics  
 16.3.1 Embed vs reference  
 16.3.2 Access-pattern-driven design

## 17. CAP Theorem & Consistency Models

17.1 CAP Theorem  
 17.1.1 Consistency vs Availability  
 17.1.2 Partition Tolerance  
17.2 Consistency Models  
 17.2.1 Strong, Eventual, Causal  
 17.2.2 Quorum reads/writes  
17.3 Tunable Consistency  
 17.3.1 Read/Write consistency levels  
 17.3.2 Latency vs correctness trade-offs

## 18. NoSQL Data Models

18.1 Key–Value Model  
 18.1.1 Data access and sharding  
 18.1.2 Popular systems  
18.2 Document Model  
 18.2.1 Nested documents & arrays  
 18.2.2 Aggregation pipelines and map-reduce  
18.3 Column-Family Model  
 18.3.1 Table/column family design  
 18.3.2 TTL, compactions, tuning  
18.4 Graph Model  
 18.4.1 Nodes, edges, properties  
 18.4.2 Traversal patterns and indexes

## 19. Key–Value Stores

19.1 Interfaces  
 19.1.1 GET/PUT/DELETE semantics  
 19.1.2 Expiration and eviction  
19.2 In-Memory vs Persistent  
 19.2.1 Redis architecture  
 19.2.2 Dynamo-style stores (e.g., Riak)  
19.3 Use Cases & Patterns  
 19.3.1 Caching and session storage  
 19.3.2 Rate-limiting and leaderboards

## 20. Document Stores

20.1 Document Design  
 20.1.1 Schema evolution strategies  
 20.1.2 Indexing nested fields  
20.2 Aggregation & Queries  
 20.2.1 Pipeline stages  
 20.2.2 Performance optimization  
20.3 Platforms  
 20.3.1 MongoDB replication & sharding  
 20.3.2 Couchbase and N1QL basics

## 21. Column-Family Stores

21.1 Wide-Column Tables  
 21.1.1 Row key and partition key design  
 21.1.2 Column families and clustering  
21.2 Maintenance  
 21.2.1 TTL and compactions  
 21.2.2 Throughput tuning and write path  
21.3 Systems  
 21.3.1 Cassandra data model  
 21.3.2 HBase architecture

## 22. Graph Databases

22.1 Graph Components  
 22.1.1 Nodes, edges, properties  
 22.1.2 Labels and relationship types  
22.2 Query Languages  
 22.2.1 Cypher patterns  
 22.2.2 Gremlin traversals  
22.3 Use Cases & Optimization  
 22.3.1 Social and knowledge graphs  
 22.3.2 Recommendation and pathfinding

## 23. Multi-Model & Polyglot Persistence

23.1 Multi-Model Engines  
 23.1.1 ArangoDB capabilities  
 23.1.2 Cosmos DB APIs  
23.2 Polyglot Architectures  
 23.2.1 Service-level patterns  
 23.2.2 Change data capture sync  
23.3 Data Integration  
 23.3.1 ETL vs CDC pipelines  
 23.3.2 Data contracts and governance

## 24. Use Cases & Comparative Analysis

24.1 Workload Types  
 24.1.1 OLTP vs OLAP vs HTAP  
 24.1.2 Batch vs Stream processing  
24.2 Architecture Decisions  
 24.2.1 RDBMS vs NoSQL criteria  
 24.2.2 Hybrid and federated approaches  
24.3 Migration & Coexistence  
 24.3.1 Strangler and dual-write patterns  
 24.3.2 Data validation and rollback plans

## 25. SQL Data Types & Conversions

25.1 Data Types  
 25.1.1 Character, Numeric, Temporal, Binary  
 25.1.2 Collations and character sets  
25.2 Conversions & Null-Handling  
 25.2.1 CAST/CONVERT, COALESCE/NVL  
 25.2.2 Date/time extractors and formats  
25.3 Precision & Rounding  
 25.3.1 DECIMAL/NUMERIC pitfalls  
 25.3.2 Implicit casts and surprises

## 26. NULL Semantics & Predicates

26.1 NULL Behavior  
 26.1.1 NULL vs blank/zero  
 26.1.2 NULLs in joins and filters  
26.2 Predicate Patterns  
 26.2.1 IN/NOT IN and NULL traps  
 26.2.2 EXISTS/NOT EXISTS correctness  
26.3 Three-Valued Logic  
 26.3.1 TRUE/FALSE/UNKNOWN  
 26.3.2 Defensive query patterns

## 27. Partitioned Tables

27.1 Rationale & Layout  
 27.1.1 Partition pruning benefits  
 27.1.2 Maintenance windows and SLAs  
27.2 Strategies  
 27.2.1 Range, Hash, List  
 27.2.2 Hybrid and sub-partitioning  
27.3 Indexing & Queries  
 27.3.1 Local vs global indexes  
 27.3.2 Skew and hotspot mitigation

## 28. RDBMS Engine Essentials

28.1 Oracle  
 28.1.1 ROWID/ROWNUM, DUAL, NVL/DECODE  
 28.1.2 MERGE, analytical functions  
28.2 MySQL/InnoDB  
 28.2.1 Storage engines and transactions  
 28.2.2 EXPLAIN, optimizer traces  
28.3 PostgreSQL  
 28.3.1 MVCC specifics and VACUUM  
 28.3.2 Extensions and windowing strengths

## 29. Date/Time Handling

29.1 Current Time Functions  
 29.1.1 NOW(), GETDATE(), SYSDATE, LOCALTIMESTAMP  
 29.1.2 Precision, timezone, session settings  
29.2 Ranges & Arithmetic  
 29.2.1 BETWEEN and inclusivity  
 29.2.2 DATEDIFF, interval math, truncation  
29.3 Timezone Handling  
 29.3.1 Conversion and storage strategies  
 29.3.2 Display vs persistence formats

## 30. Vendor-Specific NoSQL Topics

30.1 MongoDB  
 30.1.1 Shards, config servers, query routers  
 30.1.2 Collections, documents, ObjectId, embed vs reference  
30.2 Cassandra  
 30.2.1 Partitions, tokens, consistency trade-offs  
 30.2.2 Clustering keys, compaction, read/write paths  
30.3 Redis  
 30.3.1 Types: strings, lists, sets, hashes  
 30.3.2 MULTI/EXEC/WATCH, replication, persistence  
30.4 HBase  
 30.4.1 Tombstones, major compaction, filters  
 30.4.2 put/get/scan/delete and admin tools  
30.5 Elasticsearch  
 30.5.1 Indices, mappings, near-real-time, CAT APIs  
 30.5.2 Query DSL: match/term/range/geo  
30.6 Neo4j  
 30.6.1 Cypher, nodes, relationships, properties  
 30.6.2 Bloom, Browser, AuraDB, clustering
