# 7. Topic Design, Brokers, and Operations

This combined chapter merges topic design/data contracts with day-2 operations, adding a practical view of brokers, multi-broker clusters, and cross-cluster mirroring. It is organized for production readiness and interview clarity.

## 7.1 Brokers and Multi-Broker Clusters

### 7.1.1 Broker roles and partition leadership

- A broker is a Kafka server that stores partition data and serves client reads/writes; each partition has a single leader on one broker and followers on others.
- Producers and consumers interact with leaders; followers replicate the leader’s log to stay in the In-Sync Replicas (ISR) set, which underpins durable acks when using <code>acks=all</code>.
- If a leader fails, a follower in ISR is promoted, keeping the partition available; clients refresh metadata and route to the new leader automatically.
- Evenly distribute leaders across brokers to avoid hotspots; skewed leadership causes uneven CPU, IO, and network load.

### 7.1.2 Multi-broker setup and rack awareness

- Deploy at least three brokers for fault tolerance and quorum-based control operations; start with more for high-throughput or many partitions.
- Enable rack/AZ labels so replicas are placed across failure domains; a rack loss should not remove all replicas of any partition.
- Use separate disks or high-performance NVMe for log directories; monitor disk usage and IO queues to prevent ISR lag due to storage contention.
- Size heap and page cache appropriately; Kafka relies heavily on the OS page cache—give the broker plenty of RAM while keeping GC pauses short.

## 7.2 Topic Design: Partitions, Replication, Capacity

### 7.2.1 Partitions

- Choose partition count to match target consumer parallelism and throughput; max active consumers per group equals partition count, so leave headroom for growth.
- Too few partitions limit scale; too many inflate metadata and file handles and may increase compaction work—scale gradually and validate broker metrics.
- Watch per-partition throughput; if a few partitions exceed healthy MB/s, consider more partitions or improve key distribution to reduce hotspots.
- Plan for future scaling: increasing partitions later is possible but operationally heavier than starting with a sensible baseline and adding as load grows.

### 7.2.2 Replication and ISR

- Replication factor 3 is the default for critical topics; with <code>min.insync.replicas=2</code> and producer <code>acks=all</code>, writes remain durable during a single broker failure.
- Monitor ISR size and under-replicated partitions; persistent ISR shrinkage signals disk/network issues that require attention before incidents.
- Avoid unclean leader election in production; it can cause data loss by promoting out-of-sync replicas when no ISR member is available.
- Balance replicas and leaders across brokers; after maintenance, trigger preferred leader election to restore even distribution.

## 7.3 Retention Policies: Delete, Compact, Mixed

### 7.3.1 Delete-based retention

- Retain data for a fixed window (by time/size) and delete old segments; ideal for event history and analytics windows with bounded storage.
- Set <code>retention.ms</code> and/or <code>retention.bytes</code> per topic; align windows with downstream SLAs and backfill needs.
- Tune segment size/roll to smooth deletion cadence and reduce disk churn, especially on busy topics.
- Archive long-term history to object storage or replicate to a lower-cost cluster if regulatory needs exceed Kafka retention.

### 7.3.2 Log compaction

- Keep only the latest value per key with tombstones to delete keys after a grace period; suited for changelogs and materialized views.
- Ensure stable keys and well-formed values that represent complete state; partial updates complicate downstream reconstruction.
- Tune compaction thresholds (e.g., <code>min.cleanable.dirty.ratio</code>) to balance on-disk size and cleanup cadence; monitor compaction lag.
- Be cautious with null or inconsistent keys; compaction correctness depends on stable keying.

### 7.3.3 Mixed mode

- Use <code>cleanup.policy=compact,delete</code> to keep recent history while converging to latest state; helpful for pipelines needing backfills and state recovery.
- Choose <code>retention.ms</code> to cover expected replays; confirm consumer assumptions so analysts don’t misinterpret compacted past beyond the window.
- Validate that compaction keeps pace with write rate; otherwise, segments may linger and inflate storage unexpectedly.
- Publish guidance to downstream teams about how to interpret mixed topics to prevent semantic confusion.

## 7.4 Keys, Schemas, and Contracts

### 7.4.1 Keys and ordering

- Keys determine partitioning and per-key ordering; choose keys that reflect the entity needing strict order (userId, orderId).
- Avoid hot keys by sharding (e.g., <code>user-42#3</code>) when a few entities dominate traffic; ensure consumers can merge shards if required.
- Validate key distribution regularly; business growth can shift traffic patterns and create new hotspots.
- For compacted topics, keep keys stable; re-keying breaks compaction history and can bloat storage.

### 7.4.2 Schema registry and compatibility

- Adopt a schema registry and enforce compatibility (backward/forward/full) to allow rolling upgrades without breaking consumers.
- Prefer Avro/Protobuf (binary, schema-first) for performance and safety; JSON Schema is acceptable with strict validation and tooling.
- Version fields and document deprecations; avoid removing fields abruptly—introduce new topics for major changes and sunset old ones.
- Gate schema changes in CI/CD to block incompatible changes from reaching production.

## 7.5 Provisioning Topics with Spring

### 7.5.1 KafkaAdmin/NewTopic

```java
import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.context.annotation.Bean;
import org.springframework.kafka.config.TopicBuilder;

@Bean
public NewTopic orders() {
  return TopicBuilder.name("orders")
      .partitions(12)
      .replicas(3)
      .config("min.insync.replicas", "2")
      .config("retention.ms", "604800000")
      .build();
}
```

- Provision topics explicitly for repeatability; avoid auto-create to prevent weak defaults.
- Externalize partitions and retention via config to customize per environment; keep sane defaults for dev/stage.
- Encode SLAs in configs (min.insync.replicas, cleanup.policy) and document owners, data classification, and retention class in a catalog.
- Add health checks to ensure topics exist and match expected configs on startup.

### 7.5.2 Compacted and mixed topics

```java
@Bean
public NewTopic accountChangelog() {
  return TopicBuilder.name("account-changelog")
      .partitions(12)
      .replicas(3)
      .config("cleanup.policy", "compact")
      .config("min.cleanable.dirty.ratio", "0.5")
      .build();
}

@Bean
public NewTopic userState() {
  return TopicBuilder.name("user-state")
      .partitions(12)
      .replicas(3)
      .config("cleanup.policy", "compact,delete")
      .config("retention.ms", "2592000000")
      .build();
}
```

- For changelogs, ensure values are full-state representations or apply merge logic consistently; test compaction behavior with realistic data volumes.
- For mixed topics, set retention to cover expected reprocessing; verify analytics teams understand the mixed semantics.
- Monitor compaction lag and segment counts; adjust segment sizes and dirty ratios as traffic evolves.
- Keep keys stable and unique per entity across producer versions.

## 7.6 Operations: Monitoring and Troubleshooting

### 7.6.1 Lag, health, and hotspots

- Track consumer lag per partition/group; sustained increases indicate slow handlers, rebalances, or downstream pressure.
- Monitor broker metrics: request rates, queue times, network IO, disk usage, page cache hit ratio, ISR size, and under-replicated partitions.
- Diagnose producer timeouts with retry counts, delivery-timeout breaches, and accumulation time; consider tuning <code>linger.ms</code>, <code>batch.size</code>, and compression.
- Detect hot partitions and skewed leaders; rebalance leaders and improve key distribution to spread load.

### 7.6.2 Reassignments and leader balance

- Reassign partitions to balance disk and throughput or when adding brokers; throttle moves to protect clients and ISR.
- After maintenance, run preferred leader election to restore planned leader distribution and reduce hotspots.
- Observe ISR during moves; pause if under-replicated partitions persist to avoid data risk.
- Communicate planned changes to application teams to anticipate brief consumption pauses.

## 7.7 Multi-Cluster, DR, and MirrorMaker 2

### 7.7.1 Topologies and use-cases

- Active–passive DR: primary handles traffic, DR follows via mirroring; failover involves switching bootstrap endpoints and re-pointing consumers.
- Active–active: multiple regions accept writes and mirror to each other; requires idempotent models and conflict resolution policies for divergent updates.
- Hub-and-spoke analytics: regional clusters write locally, mirror centrally for batch/AI workloads; controls WAN egress and keeps local latency low.
- Keep topic partition counts and configs aligned across clusters to simplify failover/replay and capacity planning.

### 7.7.2 MirrorMaker 2 patterns

- MM2 (Kafka Connect-based) mirrors topics, ACLs, and optionally consumer group offsets; it supports renaming rules and checkpointing for offset translation.
- Run MM2 close to the source cluster, compress traffic, and size tasks for WAN bandwidth; isolate on a dedicated Connect cluster.
- Monitor replication lag, throughput, and errors; alert when lag exceeds RPO targets or WAN saturation occurs.
- Mirror retention and compaction policies to maintain consistent behavior post-failover; mismatches can break expectations.

### 7.7.3 Failover/failback runbooks

- Failover: switch producers/consumers to DR bootstrap; translate offsets via MM2 checkpoints to preserve approximate position; validate ISR and lag before ramp-up.
- Failback: reverse mirroring, drain backlogs, and move traffic back gradually; avoid split-brain by ensuring writes stop on the losing side first.
- Script and rehearse runbooks quarterly; include rollback steps, ownership, and observability gates for go/no-go decisions.
- Keep client configs (bootstrap lists) externalized to enable rapid cluster switching without code changes.

## 7.8 Practical Checklist

- Brokers: deploy ≥3, enable rack awareness, size RAM for page cache, and spread leaders; avoid unclean leader election.
- Partitions: plan for parallelism with headroom; avoid extremes; monitor per-partition throughput and adjust keys or counts as needed.
- Replication: use RF=3, <code>min.insync.replicas=2</code> for critical topics; watch ISR and under-replicated partitions continuously.
- Retention: choose delete/compact/mixed per use-case; align with SLAs and backfill needs; document semantics for consumers.
- Schemas: enforce via registry with compatibility; version intentionally; gate changes in CI.
- Operations: provision topics explicitly, balance leaders, throttle reassignments, and maintain dashboards for lag and ISR.
- Multi-cluster: pick topologies based on RPO/RTO; configure MM2 with checkpoints, compression, and isolation; rehearse failover/failback.
