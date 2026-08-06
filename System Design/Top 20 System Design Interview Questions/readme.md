# Top 20 System Design Interview Questions

> The 20 most commonly asked "design X" interview questions, each worked through the same lens: requirements, estimation, a high-level architecture (with a Mermaid diagram), a deep dive into the one or two ideas that actually make the question hard, scaling/failure handling, and common follow-ups. Builds directly on the theory in **[System Design Awesome Notes](../readme.md)** — partitioning, replication, caching, consensus, and streaming all reappear here applied to concrete products.

## Table of Contents

- [Index](#index)
- [Which Question Tests What](#which-question-tests-what)

## Index

1. [Design a URL Shortener](1.%20Design%20a%20URL%20Shortener.md) — Key generation service, base62 encoding, cache-aside redirects, 301 vs 302
2. [Design Pastebin](2.%20Design%20Pastebin.md) — Metadata/blob split, object storage, content-addressing, immutability as a caching superpower
3. [Design a Rate Limiter](3.%20Design%20a%20Rate%20Limiter.md) — Token bucket vs sliding window, atomic Lua-script counters, fail-open vs fail-closed
4. [Design a Distributed Cache](4.%20Design%20a%20Distributed%20Cache.md) — Consistent hashing, virtual nodes, eviction policies, stampede/penetration/avalanche
5. [Design a Distributed Key-Value Store](5.%20Design%20a%20Distributed%20Key-Value%20Store.md) — Dynamo-style quorums (R/W/N), vector clocks, hinted handoff, read repair
6. [Design a Unique ID Generator](6.%20Design%20a%20Unique%20ID%20Generator.md) — Snowflake bit layout, clock-skew handling, ticket-server alternative
7. [Design a Chat / Messaging App](7.%20Design%20a%20Chat%20Messaging%20App.md) — Stateful gateways, session registry, Kafka ordering by conversation_id, wide-column storage
8. [Design a News Feed System](8.%20Design%20a%20News%20Feed%20System.md) — Push vs pull fan-out, the celebrity problem, hybrid fan-out, ranking as a pluggable stage
9. [Design a Notification System](9.%20Design%20a%20Notification%20System.md) — Decoupled channel routing, idempotent dedup, quiet hours, digest batching
10. [Design a Search Autocomplete System](10.%20Design%20a%20Search%20Autocomplete%20System.md) — Trie with cached top-K per node, offline build vs online serving split
11. [Design a Web Crawler](11.%20Design%20a%20Web%20Crawler.md) — Politeness-aware URL frontier, Bloom-filter dedup, crawler traps
12. [Design a Content Delivery Network](12.%20Design%20a%20Content%20Delivery%20Network.md) — Anycast/GeoDNS routing, origin shielding, purge vs TTL invalidation
13. [Design a Video Streaming Platform](13.%20Design%20a%20Video%20Streaming%20Platform.md) — Async transcoding pipeline, adaptive bitrate streaming (HLS/DASH), CDN as primary serving path
14. [Design a Ride-Sharing System](14.%20Design%20a%20Ride-Sharing%20System.md) — Geohash/quadtree indexing, regional sharding, sequential-offer matching
15. [Design a File Storage and Sync Service](15.%20Design%20a%20File%20Storage%20and%20Sync%20Service.md) — Content-defined chunking, block-level dedup, optimistic-concurrency conflict detection
16. [Design a Distributed Message Queue](16.%20Design%20a%20Distributed%20Message%20Queue.md) — Append-only log, partition ordering, ISR replication, delivery-semantics table
17. [Design a Distributed Task Scheduler](17.%20Design%20a%20Distributed%20Task%20Scheduler.md) — Atomic job claiming, leases + reaper, timing wheels, recurring-job materialization
18. [Design a Payment System](18.%20Design%20a%20Payment%20System.md) — Double-entry immutable ledger, idempotency keys, saga pattern, reconciliation
19. [Design a Distributed Search Engine](19.%20Design%20a%20Distributed%20Search%20Engine.md) — Inverted index, BM25 ranking, scatter-gather queries, CDC-driven freshness
20. [Design a Collaborative Document Editor](20.%20Design%20a%20Collaborative%20Document%20Editor.md) — Operational Transformation vs CRDTs, why locking and LWW both fail

## Which Question Tests What

| Core idea | Questions that exercise it |
|---|---|
| Consistent hashing / partitioning | Distributed Cache (4), KV Store (5), Ride-Sharing (14) |
| Fan-out & derived views | News Feed (8), Notification System (9) |
| Append-only log as the core primitive | Message Queue (16), Search Engine (19), Payment Ledger (18) |
| Strong consistency where invariants live | Unique-alias claims (1), Idempotent claims (17, 18) |
| CDN / edge caching | URL Shortener (1), Pastebin (2), CDN (12), Video Streaming (13) |
| Real-time bidirectional connections | Chat (7), Collaborative Editor (20) |
| Concurrent-write conflict resolution | KV Store (5, vector clocks), File Sync (15, conflicted copies), Collaborative Editor (20, OT/CRDT) |
