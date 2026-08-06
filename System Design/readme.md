# System Design Awesome Notes

> End-to-end system design and distributed-systems architecture notes, motivated by *Designing Data-Intensive Applications* (Martin Kleppmann) — from storage engines and replication to consensus, streams, and a full interview playbook.

## Table of Contents

- [Index](#index)

## Index

1. [Foundations Reliability Scalability Maintainability](1.%20Foundations%20Reliability%20Scalability%20Maintainability.md) — Data-intensive building blocks, faults vs failures, load parameters, percentiles/tail latency, scaling strategies
2. [Data Models and Query Languages](2.%20Data%20Models%20and%20Query%20Languages.md) — Relational vs document vs graph, normalization, schema-on-read/write, declarative queries
3. [Storage and Retrieval](3.%20Storage%20and%20Retrieval.md) — LSM-trees vs B-trees, SSTables, Bloom filters, indexes, OLTP vs OLAP, column-oriented storage
4. [Encoding Evolution and Data Flow](4.%20Encoding%20Evolution%20and%20Data%20Flow.md) — Forward/backward compatibility, JSON vs Protobuf vs Avro, REST vs gRPC, message brokers
5. [Replication](5.%20Replication.md) — Single-leader, multi-leader, leaderless/quorums, replication lag anomalies, conflict resolution
6. [Partitioning and Sharding](6.%20Partitioning%20and%20Sharding.md) — Range vs hash partitioning, hot keys, secondary indexes, rebalancing, consistent hashing, request routing
7. [Transactions](7.%20Transactions.md) — ACID precisely, isolation levels, MVCC, lost updates/write skew/phantoms, 2PL vs SSI, distributed transactions & sagas
8. [The Trouble with Distributed Systems](8.%20The%20Trouble%20with%20Distributed%20Systems.md) — Partial failure, unreliable networks & clocks, process pauses, fencing tokens, quorum truth
9. [Consistency and Consensus](9.%20Consistency%20and%20Consensus.md) — Linearizability, CAP done right, causality, Lamport clocks, Raft/Paxos, ZooKeeper/etcd
10. [Batch Processing](10.%20Batch%20Processing.md) — Unix philosophy, MapReduce, distributed joins, skew, dataflow engines (Spark/Flink)
11. [Stream Processing and Event Driven Architecture](11.%20Stream%20Processing%20and%20Event%20Driven%20Architecture.md) — Log-based brokers, CDC, event sourcing, windows & watermarks, exactly-once
12. [Caching Load Balancing and CDNs](12.%20Caching%20Load%20Balancing%20and%20CDNs.md) — Caching patterns, stampede/penetration/avalanche, L4/L7 balancing, CDN strategy
13. [Scalable System Building Blocks](13.%20Scalable%20System%20Building%20Blocks.md) — API gateways, rate limiting, ID generation, task queues, fan-out, blob storage, observability
14. [System Design Interview Playbook](14.%20System%20Design%20Interview%20Playbook.md) — 5-step framework, back-of-envelope numbers, worked designs (URL shortener, chat system)

## Companion

- **[Top 20 System Design Interview Questions](Top%2020%20System%20Design%20Interview%20Questions/readme.md)** — 20 fully worked "design X" questions (URL shortener, rate limiter, chat app, news feed, ride-sharing, payment system, collaborative editor, and more), each with requirements, estimation, a Mermaid architecture diagram, and a deep dive into the hard part.
