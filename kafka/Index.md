# Kafka + Spring for Kafka: 10-Chapter Interview Syllabus

## 1. Foundations and Core Concepts

### 1.1 Messaging vs streaming, event logs vs queues

### 1.2 Topics, partitions, offsets, records, keys

### 1.3 Ordering guarantees and per-key routing

### 1.4 Producers, consumers, consumer groups, brokers

### 1.5 When to use Kafka and common use cases

## 2. Architecture and Internals

### 2.1 Partition leadership, replication, ISR, HA

### 2.2 Storage internals: segments, indexes, retention

### 2.3 Log cleanup: delete vs compaction

### 2.4 Metadata control plane: ZooKeeper vs KRaft

### 2.5 Rebalancing (eager vs cooperative) and coordination

## 3. Producers: Design and Tuning

### 3.1 Record structure, serializers, partitioners

### 3.2 Durability/latency: acks, idempotence, retries

### 3.3 Throughput: batch.size, linger.ms, compression

### 3.4 Ordering per key, key selection strategies

## 4. Consumers and Groups

### 4.1 Poll loop, heartbeats, liveness

### 4.2 Offsets: auto vs manual commit, seek/replay

### 4.3 Rebalancing behavior and stability

### 4.4 Parallelism limits, fetch tuning, backpressure

## 5. Delivery Guarantees, Errors, and Transactions

### 5.1 At-most-once vs at-least-once vs exactly-once

### 5.2 Idempotence and transactions across consume–process–produce

### 5.3 Retries, backoff, and non-blocking retry topics

### 5.4 Dead Letter Topics (DLT/DLQ): patterns, routing, and recovery

## 6. Streams and Connect

### 6.1 Kafka Streams: KStream, KTable, joins, windows, state stores

### 6.2 Stateless vs stateful processing, repartitioning

### 6.3 Kafka Connect: source/sink connectors, SMTs, offsets, deployments

## 7. Topic Design and Data Contracts

### 7.1 Partitions, replication factor, capacity planning

### 7.2 Retention policies: delete, compact, or both

### 7.3 Keys, schemas, schema registry, compatibility modes

### 7.4 Event versioning and contract governance

## 8. Operations, Performance, and Reliability

### 8.1 Topic lifecycle, partition reassignments, rack awareness

### 8.2 Monitoring: consumer lag, broker health, disk/IO

### 8.3 Troubleshooting timeouts, slow consumers, hotspots

### 8.4 Sizing, partition counts, page cache, compression

### 8.5 DR and cross-cluster mirroring patterns

## 9. Security and Multi-Tenancy

### 9.1 Authentication and authorization (ACLs)

### 9.2 Encryption in transit and at rest

### 9.3 Tenant isolation, quotas, and governance

## 10. Spring for Apache Kafka

### 10.1 When to use Spring Kafka vs native clients

### 10.2 Project setup, Boot config, SerDes

### 10.3 Producers with KafkaTemplate, routing, callbacks

### 10.4 Consumers with @KafkaListener, acks, retries, DLTs

### 10.5 Topic management with KafkaAdmin/NewTopic

### 10.6 Transactions/EOS in Spring flows

### 10.7 Observability: metrics, health, graceful shutdown

### 10.8 Testing with @EmbeddedKafka and end-to-end tests
