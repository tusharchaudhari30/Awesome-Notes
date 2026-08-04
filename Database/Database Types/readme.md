# Database Types Awesome Notes

> One chapter per database family: the data model, **how it physically stores data on disk**, the performance profile that follows, its scaling/consistency story, and when to choose (or avoid) it.

## Table of Contents

- [Index](#index)

## Index

1. [The Database Landscape and How to Choose](1.%20The%20Database%20Landscape%20and%20How%20to%20Choose.md) — Taxonomy, the three deciding axes (model / engine / distribution), decision flow, polyglot persistence
2. [Relational OLTP Databases](2.%20Relational%20OLTP%20Databases.md) — B-trees, pages, WAL + buffer pool, MVCC/VACUUM, clustered vs heap, scaling ladder
3. [Key-Value Stores](3.%20Key-Value%20Stores.md) — Redis internals (hash table, single thread, RDB/AOF), DynamoDB partitions & GSIs, hot keys
4. [Document Databases](4.%20Document%20Databases.md) — BSON + WiredTiger B-trees, embed vs reference, multikey indexes, shard keys
5. [Wide-Column Stores](5.%20Wide-Column%20Stores.md) — Cassandra's two-level map, LSM write path, tombstones, tunable consistency, query-first modeling
6. [Columnar OLAP Databases](6.%20Columnar%20OLAP%20Databases.md) — Column segments, dictionary/RLE compression, zone maps, vectorized execution, lakehouse
7. [Graph Databases](7.%20Graph%20Databases.md) — Index-free adjacency, O(1) traversals vs joins, supernodes, why graphs shard badly
8. [Time-Series Databases](8.%20Time-Series%20Databases.md) — Time chunks, Gorilla compression (delta-of-delta, XOR), cardinality, downsampling, retention
9. [Search Engine Databases](9.%20Search%20Engine%20Databases.md) — Inverted index, analyzers, immutable segments, BM25, NRT, scatter-gather shards
10. [Vector Databases](10.%20Vector%20Databases.md) — Embeddings, HNSW/IVF-PQ, quantization, filtered ANN, RAG & hybrid search
11. [NewSQL and Distributed SQL](11.%20NewSQL%20and%20Distributed%20SQL.md) — Ranges + Raft, TrueTime/HLC, non-blocking 2PC, the consensus latency tax
12. [Choosing a Database Comparison Cheat Sheet](12.%20Choosing%20a%20Database%20Comparison%20Cheat%20Sheet.md) — Master comparison tables, decision table, rapid-fire Q&A

## Companion

Deep dives on the shared theory live in **[System Design Awesome Notes](../../System%20Design/readme.md)** — storage engines (LSM vs B-tree), replication, partitioning, transactions, and consensus.
