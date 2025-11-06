# Chapter 3: Producer Configuration Meanings

This section explains each major producer configuration in clear, practical terms with how it affects durability, ordering, throughput, and failure handling. Examples use Spring for Kafka.

## 3.1 Connection and Serialization

### 3.1.1 bootstrap.servers

- **Meaning:** The initial list of brokers the client contacts to fetch cluster metadata, leader locations, and topic partition info.
- **Why it matters:** If the listed node is down, the client tries the others; include multiple brokers to improve startup reliability and prefer endpoints close to the client to reduce connection time.
- **Tips:** Keep DNS entries updated during broker rotation; avoid using load balancers that hide broker identity, because the client needs real broker addresses after bootstrap.

```yaml
spring:
  kafka:
    bootstrap-servers: broker-1:9092,broker-2:9092,broker-3:9092
```

### 3.1.2 key.serializer

- **Meaning:** The class that converts the key object into bytes before sending to Kafka.
- **Why it matters:** Keys drive partitioning and ordering; using a consistent and deterministic serializer ensures that the same logical key routes to the same partition.
- **Tips:** Prefer lightweight, deterministic encodings for keys; if using complex key objects, ensure stable field order and explicit charset to avoid routing drift.

```yaml
spring:
  kafka:
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
```

### 3.1.3 value.serializer

- **Meaning:** The class that converts the value object (payload) into bytes.
- **Why it matters:** It determines interoperability, payload size, and evolution strategy; schema-aware serializers enable safe rolling upgrades across teams.
- **Tips:** Start with JSON for simplicity, then adopt Avro/Protobuf with a schema registry for large multi-team estates; document compatibility rules.

```yaml
spring:
  kafka:
    producer:
      value-serializer: org.apache.kafka.common.serialization.StringSerializer
```

## 3.2 Durability and Failure Semantics

### 3.2.1 acks (all, 1, 0)

- **Meaning:** Controls how many broker acknowledgments are required before the send is considered successful.
- **Effects:**
  - **all:** Wait for leader and all in-sync replicas; highest durability, slightly higher latency.
  - **1:** Wait for leader only; moderate durability, lower latency.
  - **0:** Don’t wait; lowest latency, potential silent loss.
- **Tips:** For critical data, use all with proper topic min.insync.replicas; for best-effort telemetry, 1 or 0 may suffice.

```yaml
spring:
  kafka:
    producer:
      acks: all
```

### 3.2.2 enable.idempotence

- **Meaning:** Ensures the broker deduplicates retried records from the same producer session using sequence numbers.
- **Why it matters:** Prevents duplicates when retries occur due to transient failures; a cornerstone for exactly-once processing in producer pipelines.
- **Tips:** Pair with acks=all; avoid disabling unless knowingly accepting duplicates for higher throughput edge cases.

```yaml
spring:
  kafka:
    producer:
      properties:
        enable.idempotence: true
```

### 3.2.3 retries

- **Meaning:** The max number of resend attempts when transient failures happen (timeouts, disconnects, temporary unavailable leaders).
- **Why it matters:** More retries improve resilience but can increase end-to-end latency; safe when idempotence is enabled to avoid duplicates.
- **Tips:** Set high (e.g., 10+) with idempotence; watch delivery.timeout.ms so retries have time to complete.

```yaml
spring:
  kafka:
    producer:
      properties:
        retries: 10
```

### 3.2.4 delivery.timeout.ms

- **Meaning:** The total time budget for delivering a record, including all retries and backoffs.
- **Why it matters:** If exceeded, the future completes with an error, even if more retries remain; protects the app from hanging indefinitely.
- **Tips:** Set comfortably above expected network jitter and broker failover windows; align with business SLAs.

```yaml
spring:
  kafka:
    producer:
      properties:
        delivery.timeout.ms: 120000
```

### 3.2.5 max.in.flight.requests.per.connection

- **Meaning:** The number of unacknowledged requests allowed per connection at once.
- **Why it matters:** Values >1 can reorder batches under retry; set to 1 with idempotence to ensure strict ordering, at the cost of throughput.
- **Tips:** Use 1 when order is critical; 2–5 when occasional reordering is acceptable for higher throughput.

```yaml
spring:
  kafka:
    producer:
      properties:
        max.in.flight.requests.per.connection: 1
```

## 3.3 Throughput Controls

### 3.3.1 batch.size

- **Meaning:** Max size (in bytes) of the per-partition batch buffer before it’s sent.
- **Why it matters:** Larger batches improve IO efficiency and compression, lowering CPU and network overhead per message.
- **Tips:** Increase gradually while monitoring memory and latency; ensure traffic volume can actually fill larger batches.

```yaml
spring:
  kafka:
    producer:
      batch-size: 65536
```

### 3.3.2 linger.ms

- **Meaning:** The maximum time to wait for additional messages to fill a batch before sending.
- **Why it matters:** Small positive values can dramatically improve throughput by enabling larger batches with minimal added latency.
- **Tips:** Start with 5–20 ms for back-end services; set to 0 for ultra-low latency needs at the expense of throughput.

```yaml
spring:
  kafka:
    producer:
      linger-ms: 20
```

### 3.3.3 compression.type (none, gzip, snappy, lz4, zstd)

- **Meaning:** Compression algorithm applied per batch to reduce bytes over the network and on disk.
- **Effects:** gzip compresses well but is CPU-heavy; snappy is fast with moderate ratios; lz4 and zstd often give the best balance for streaming workloads.
- **Tips:** Favor lz4 or zstd for general use; validate with production-like data and watch CPU headroom on both producers and brokers.

```yaml
spring:
  kafka:
    producer:
      compression-type: lz4
```

## 3.4 Backpressure and Resource Limits

### 3.4.1 buffer.memory

- **Meaning:** Total memory (bytes) the producer can use to buffer unsent records across partitions.
- **Why it matters:** If full, send() blocks up to max.block.ms; too small buffers cause frequent blocking in bursts, too large can increase GC pressure.
- **Tips:** Size based on peak throughput and batch sizes; correlate with JVM heap and GC tuning.

```yaml
spring:
  kafka:
    producer:
      properties:
        buffer.memory: 67108864
```

### 3.4.2 max.block.ms

- **Meaning:** Max time that <code>send()</code>, <code>partitionsFor()</code>, or <code>initTransactions()</code> will block when metadata is unavailable or buffers are full.
- **Why it matters:** Prevents indefinite stalls and surfaces backpressure as exceptions the app can handle.
- **Tips:** Align with retry policies and upstream timeouts; log and alert on max-block breaches.

```yaml
spring:
  kafka:
    producer:
      properties:
        max.block.ms: 60000
```

## 3.5 Observability and Control

### 3.5.1 client.id

- **Meaning:** Logical identifier for the producer instance used in broker metrics and quotas.
- **Why it matters:** Enables per-service monitoring and quota management; makes it easier to pinpoint “noisy neighbor” producers.
- **Tips:** Use a stable, descriptive value per service/component and include version or environment when helpful.

```yaml
spring:
  kafka:
    producer:
      properties:
        client.id: orders-service-v1
```

### 3.5.2 interceptor.classes

- **Meaning:** List of producer interceptor classes to run before send and on acknowledgement.
- **Why it matters:** Adds cross-cutting behaviors like tracing, metrics, or sanitization without touching business logic.
- **Tips:** Keep interceptors lightweight to avoid adding jitter; do not perform blocking IO in interceptors.

```yaml
spring:
  kafka:
    producer:
      properties:
        interceptor.classes: com.example.kafka.interceptor.TracingProducerInterceptor
```

## 3.6 Message Semantics and Methods

### 3.6.1 Send methods choice

- **Fire-and-forget:** Maximizes throughput but ignores per-message errors; use only where occasional loss is acceptable and rely on metrics for detection.
- **Synchronous sends:** Simplify error handling by blocking for results, but can throttle throughput; reserve for low-volume critical flows.
- **Async with callbacks:** Offers the best balance, enabling non-blocking pipelines with explicit success/failure handling, retries, and DLT routing.
- **Correlation ID:** Always propagate a correlation ID in headers so callbacks can associate broker results with upstream requests.

```java
// Fire-and-forget
template.send("orders", "user-1", "payload");

// Synchronous
template.send("orders", "user-1", "payload").get();

// Asynchronous with callback
template.send("orders", "user-1", "payload")
    .whenComplete((md, ex) -> { /* handle success/failure */ });
```

## 3.7 Partitioning Behavior

### 3.7.1 partitioner.class

- **Meaning:** Chooses the partition for each record; default hashes the key, sticky is used for null keys to improve batching.
- **Why it matters:** Affects ordering, hotspot risk, and batch efficiency; consistent routing keeps per-key order intact across restarts.
- **Tips:** Provide stable keys for entities that require order; if keys are skewed, shard them or introduce a custom partitioner to distribute load while meeting ordering constraints.

```java
@Bean
public org.springframework.boot.autoconfigure.kafka.KafkaPropertiesCustomizer customPartitioner() {
  return props -> props.getProducer().getProperties()
      .put("partitioner.class", "com.example.kafka.partitioning.RegionPartitioner");
}
```

## 3.8 Headers and Metadata

### 3.8.1 Using headers

- **Meaning:** Key-value metadata attached to the record outside the payload; useful for tracing, schema versioning, and routing hints.
- **Why it matters:** Enables cross-cutting capabilities without changing payload contracts; consumers can branch logic based on headers.
- **Tips:** Use headers for correlation IDs and schema versions; avoid storing secrets unless encrypted and governed.

```java
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.support.MessageBuilder;

var msg = MessageBuilder.withPayload("payload")
    .setHeader(KafkaHeaders.TOPIC, "orders")
    .setHeader(KafkaHeaders.MESSAGE_KEY, "user-1")
    .setHeader("schemaVersion", "v3")
    .build();

template.send(msg);
```

## 3.9 Quotas and Throttling

### 3.9.1 Broker quotas

- **Meaning:** Per-client or per-user limits on bandwidth and request rate enforced by brokers to protect cluster stability.
- **Why it matters:** Exceeding quotas triggers server-side throttling, increasing latency until traffic conforms, which can mask or amplify downstream issues.
- **Tips:** Assign unique client.id values, watch throttle time metrics, and tune batching/compression to reduce byte rates before requesting higher quotas.

```yaml
spring:
  kafka:
    producer:
      properties:
        client.id: orders-service-v1
```

### 3.9.2 Client-side throttling

- **Meaning:** Application-enforced rate limiting and backoff policies to keep production rates within safe bounds and respond gracefully to throttling.
- **Why it matters:** Prevents cascading failures by aligning send rates with broker capacity and downstream consumer throughput.
- **Tips:** Implement exponential backoff with jitter on retriable errors; prioritize critical topics and shed non-essential load under sustained pressure.
