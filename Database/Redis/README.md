# Redis Notes Index

Welcome to the Redis section of Awesome-Notes! This folder provides end-to-end resources covering Redis fundamentals, advanced topics, integration with Spring, caching patterns, interview summaries, and hands-on guides.

---

## Index

1. [Redis Fundamentals and Core Concepts](1.%20Redis%20Fundamentals%20and%20Core%20Concepts.md)
   - What is Redis and Its Use Cases
   - Redis Data Types (String, Hash, List, Set, Sorted Set, Stream)
   - In-Memory Architecture and Performance
   - Redis vs Traditional Databases vs Memcached
   - Key-Value Operations and Key Management
   - Redis Commands & Common Operations
   - Binary-Safe Strings and Encoding

2. [Redis Data Persistence and High Availability](2.%20Redis%20Data%20persistence%20and%20High%20Availability.md)
   - RDB Snapshots vs AOF Persistence
   - AOF Rewrite and fsync Policies
   - Data Durability Trade-offs
   - Replication (Master-Slave)
   - Replication Offsets & Resynchronization
   - Redis Sentinel (Automatic Failover)
   - Sentinel Configuration and Monitoring
   - Redis Cluster (Scaling, Sharding)
   - Cluster Slots, Hash Tags, and Topology Changes

3. [Advanced Redis Concepts](3.%20Advanced%20Redis%20Concepts.md)
   - Transactions, MULTI/EXEC/WATCH/DISCARD
   - Optimistic Locking with WATCH
   - Pub/Sub Messaging
   - Pub/Sub vs Streams
   - Pipelining for Bulk Operations
   - Memory Management and Eviction Policies
   - MEMORY Commands & Analysis
   - Redis Lua Scripting
   - Atomic Lua Operations and Rate Limiting
   - Redis Security (AUTH, ACL, SSL)
   - Key Expiration & TTL Strategies
   - SCAN vs KEYS (Efficient Key Scanning)

4. [Spring Data Redis Integration](4.%20Spring%20Data%20Redis%20Integration.md)
   - Dependencies and Setup (Maven/Gradle)
   - RedisTemplate and StringRedisTemplate Usage
   - CRUD with Redis Repositories
   - @RedisHash Mapping and TTL
   - Redis Connection Factories (Lettuce/Jedis)
   - Pooling & Advanced Connectivity (Standalone, Sentinel, Cluster)
   - Lettuce vs Jedis
   - Pub/Sub Integration
   - Transactions in Spring Data Redis
   - Serialization Strategies

5. [Spring Boot Caching with Redis](5.%20Spring%20Boot%20Caching%20with%20Redis.md)
   - Spring Cache Abstraction & Annotations
   - @Cacheable, @CachePut, @CacheEvict
   - Conditional Caching and Key Generation
   - RedisCacheManager Configuration
   - TTL, Multi-Level (L1/L2) Caching
   - Cache Patterns (Aside, Write-Through, Write-Back)
   - Invalidation Strategies
   - Performance Tuning & Monitoring

6. [Redis & Spring Data Redis - Interview Cheat Sheet](Redis%20%26%20Spring%20Data%20Redis%20-%20Interview%20Cheat%20Sheet.md)
   - Redis Core Commands (String, List, Set, Hash, ZSet)
   - Key Management, Expiration & TTL
   - Transactions, WATCH, Pipelining
   - Pub/Sub, Streams, Geospatial, HyperLogLog, Bitmaps
   - Persistence (RDB/AOF), Replication, Cluster
   - Spring Data Redis usage intro
   - RedisTemplate/Cache usage
   - Common Interview Q&A & Best Practices

7. [Redis Spring for Data](Redis%20Spring%20for%20Data.md)
   - Step-by-step Spring Boot+Redis Caching Guide
   - Docker/local Redis Setup
   - Project, Entity & Repository Setup
   - CacheManager/Annotations Use
   - REST API, Testing, Customization
   - Production, Best Practices & Troubleshooting

---

> _Click any file link above to jump directly to the full notes and code examples for that topic!_

---

**How This Index Was Built**
- Each file lists its major headings for quick topic scan.
- All important config/code block areas are highlighted in sub-bullets within each file.

---
