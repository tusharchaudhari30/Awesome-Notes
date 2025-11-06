# Chapter 2: Architecture and Internals

This chapter explains how Kafka achieves scalability, durability, and high availability through partition leadership, replication, storage mechanics, metadata management, and coordination. It also highlights practical settings and gotchas, with focused Java examples where configuration choices make a difference.

## 2.1 Partition Leadership, Replication, HA

### Single-leader model

- Each partition has one leader replica that serves reads and writes; follower replicas pull data from the leader to stay in sync.
- On leader failure, a follower in the in-sync replica set (ISR) is promoted to leader, keeping the partition available.

### Write durability knobs

```java
// Producer-side durability vs latency
props.put(ProducerConfig.ACKS_CONFIG, "1");   // leader-only ack -> lower latency, lower durability
props.put(ProducerConfig.ACKS_CONFIG, "all"); // leader + ISR ack -> higher durability
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, "true"); // dedupe on retry
```

- Combine acks=all with topic-level <code>min.insync.replicas</code> (e.g., 2 with replication factor 3) to avoid data loss during broker failures.

## 2.2 Storage Internals: Segments, Indexes, Retention

### Segmented logs

- Each partition is an append-only log split into segment files; when a segment reaches size/time limits, Kafka “rolls” to a new segment.
- Per-segment indexes (offset and time) accelerate lookups and retention cleanup, keeping IO mostly sequential.

### Retention policies

- Delete-based retention removes old segments by size/time to maintain a bounded history.
- Log compaction keeps only the latest value per key (plus tombstones temporarily), ideal for change-log/state topics; delete and compact can be combined.

## 2.3 Log Cleanup: Delete vs Compaction

### Choosing policies

- Use delete retention for event streams where historical replay over a window is needed.
- Use compaction for materialized state topics (e.g., latest account balance per user).

### Example: topic configs

```java
// Delete-based retention (e.g., 7 days)
--config retention.ms=604800000 --config cleanup.policy=delete

// Compaction (keep latest record per key)
--config cleanup.policy=compact --config min.cleanable.dirty.ratio=0.5

// Mixed (retain recent history + compact)
--config cleanup.policy=compact,delete --config retention.ms=604800000
```

## 2.4 Metadata Control Plane: ZooKeeper vs KRaft

### Evolution

- Legacy clusters relied on ZooKeeper for controller election and metadata storage.
- KRaft embeds metadata management inside Kafka using a controller quorum and a replicated metadata log, removing the external ZooKeeper dependency.

### Why it matters

- Fewer moving parts, faster failover, and more scalable metadata handling for large clusters with many partitions.

## 2.5 Rebalancing and Coordination

### Consumer group rebalancing

- Rebalances occur when consumers join/leave, subscriptions change, or partitions are added; assignments are redistributed across instances.
- Eager protocol pauses all consumers during rebalance; cooperative (incremental) protocol only moves what's necessary, reducing disruption.

### Enabling cooperative rebalancing

```java
props.put(ConsumerConfig.PARTITION_ASSIGNMENT_STRATEGY_CONFIG,
  "org.apache.kafka.clients.consumer.CooperativeStickyAssignor");
```

## 2.6 Designing for Reliability

### Replication and ISR

- Start with replication factor 3 for important topics; monitor ISR size and under-replicated partitions.
- Set <code>min.insync.replicas</code> to at least 2 and use producer <code>acks=all</code> for strong write durability.

### Rack awareness

- Distribute replicas across racks/AZs to survive a rack outage; avoid leader hotspots by balancing leaders across brokers.

## 2.7 Performance Implications

### IO patterns and batching

- Kafka leans on sequential disk IO and the OS page cache; larger batches and compression reduce overhead and improve throughput.
- Too many tiny partitions increase file handles, metadata, and context switching; size partitions to match target throughput and consumer parallelism.

### Producer and consumer tuning

```java
// Producer throughput hints
props.put(ProducerConfig.BATCH_SIZE_CONFIG, 64_000);
props.put(ProducerConfig.LINGER_MS_CONFIG, 20);
props.put(ProducerConfig.COMPRESSION_TYPE_CONFIG, "lz4");

// Consumer fetch tuning
props.put(ConsumerConfig.FETCH_MIN_BYTES_CONFIG, 1_048_576); // 1MB
props.put(ConsumerConfig.MAX_PARTITION_FETCH_BYTES_CONFIG, 1_048_576);
```

## 2.8 Practical Checklist

### Operations

- Replication factor ≥ 3 for critical topics; min.insync.replicas ≥ 2; producers use acks=all and idempotence.
- Enable rack awareness; balance leaders; watch for under-replicated partitions, ISR shrinkage, and long GC pauses.

### Data layout

- Choose delete vs compact vs mixed per topic; align segment size/roll with retention and compaction goals.
- Keep partition counts reasonable; plan ahead for growth to avoid frequent costly reassignments.

## 2.9 Handy Admin and Spring Snippets

### CLI topic creation

```bash
kafka-topics --create \
  --topic orders \
  --partitions 6 \
  --replication-factor 3 \
  --bootstrap-server localhost:9092 \
  --config min.insync.replicas=2 \
  --config cleanup.policy=delete \
  --config retention.ms=604800000
```

### Spring Topic beans

```java
import org.springframework.context.annotation.Bean;
import org.springframework.kafka.config.TopicBuilder;
import org.springframework.kafka.core.KafkaAdmin;
import org.apache.kafka.clients.admin.NewTopic;

public class TopicsConfig {
  @Bean
  public KafkaAdmin.NewTopics topics() {
    return new KafkaAdmin.NewTopics(
        TopicBuilder.name("orders")
            .partitions(6)
            .replicas(3)
            .config("min.insync.replicas", "2")
            .config("cleanup.policy", "delete")
            .config("retention.ms", "604800000")
            .build(),
        TopicBuilder.name("account-changelog")
            .partitions(6)
            .replicas(3)
            .config("cleanup.policy", "compact")
            .build()
    );
  }
}
```

### Consumer cooperative assignor (Spring Boot)

```yaml
spring:
  kafka:
    consumer:
      properties:
        partition.assignment.strategy: org.apache.kafka.clients.consumer.CooperativeStickyAssignor
```
