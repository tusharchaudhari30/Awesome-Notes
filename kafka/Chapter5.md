# 5. Delivery Guarantees and Transactions

This chapter explains at-most-once, at-least-once, and exactly-once semantics, then shows how to implement each in Spring for Kafka, including transactional consume–process–produce pipelines, proper isolation on the consumer side, and error-handling patterns that maintain correctness under failures.

## 5.1 Delivery models overview

### 5.1.1 At-most-once

- Messages are acknowledged before or as they are processed, so failures after acknowledgment can cause data loss.
- This model favors latency and simplicity, and is reasonable for best-effort telemetry where occasional drops are acceptable.
- It avoids duplicates by never reprocessing acknowledged data, but the trade-off is potential message loss during crashes.
- In Spring for Kafka, this usually means auto-commit on and processing that never throws, or manual commits before the core work is performed.

### 5.1.2 At-least-once

- Messages are acknowledged after successful processing, ensuring that crashes result in reprocessing instead of data loss.
- This model can generate duplicates if failures occur after a side effect but before the offset commit, so handlers must be idempotent.
- It balances durability and operational simplicity without requiring transactions in Kafka.
- In Spring for Kafka, disable auto-commit and acknowledge after the business logic completes.

### 5.1.3 Exactly-once (EOS)

- Messages are processed with atomicity between reading input and producing output so that the outcome is neither lost nor duplicated.
- Broker-level idempotence eliminates duplicates on producer retries, and transactions atomically include produced records and consumed offsets.
- Consumers configured with <code>read_committed</code> see only committed (non-aborted) transactional results.
- In Spring for Kafka, enable producer transactions and wire a <code>KafkaTransactionManager</code> into the listener container to bind offset commits and produce operations in a single transaction.

## 5.2 At-most-once in Spring for Kafka

### 5.2.1 Configuration

- Turn on <code>enable-auto-commit</code> so the consumer periodically commits offsets regardless of processing status.
- Use simple listeners that do not throw, or handle exceptions internally without retrying to avoid reprocessing.
- Prefer for low-value, best-effort streams where occasional loss is acceptable.

```yaml
spring:
  kafka:
    consumer:
      group-id: orders-atmost
      enable-auto-commit: true
      auto-offset-reset: earliest
```

```java
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class AtMostOnceListener {
  @KafkaListener(topics = "orders", groupId = "orders-atmost")
  public void handle(String value) {
    // quick, best-effort processing; auto-commit advances offsets periodically
  }
}
```

## 5.3 At-least-once in Spring for Kafka

### 5.3.1 Configuration

- Disable <code>enable-auto-commit</code> so commits occur only after successful handling.
- Use manual acknowledgment to commit offsets after the work is done; keep handlers idempotent to tolerate replays.

```yaml
spring:
  kafka:
    consumer:
      group-id: orders-atleast
      enable-auto-commit: false
      auto-offset-reset: latest
```

```java
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class AtLeastOnceListener {
  @KafkaListener(topics = "orders", groupId = "orders-atleast", containerFactory = "manualAckFactory")
  public void handle(String value, Acknowledgment ack) {
    // 1) process business logic (idempotent)
    // 2) commit offsets only after success
    ack.acknowledge();
  }
}
```

```java
import org.springframework.context.annotation.Bean;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.stereotype.Configuration;

@Configuration
public class ManualAckConfig {
  @Bean
  public ConcurrentKafkaListenerContainerFactory<String, String> manualAckFactory(
      ConsumerFactory<String, String> cf) {
    var f = new ConcurrentKafkaListenerContainerFactory<String, String>();
    f.setConsumerFactory(cf);
    f.getContainerProperties().setAckMode(
        org.springframework.kafka.listener.ContainerProperties.AckMode.MANUAL_IMMEDIATE);
    return f;
  }
}
```

## 5.4 Exactly-once for producers (produce-only EOS)

### 5.4.1 Configuration

- Enable idempotent producer with <code>acks=all</code> to deduplicate retries and ensure durability.
- This eliminates duplicates from producer retries, but does not bind consumed offsets; use when only producing (no read-process-write chain).

```yaml
spring:
  kafka:
    producer:
      acks: all
      properties:
        enable.idempotence: true
```

```java
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class ProduceOnlyService {
  private final KafkaTemplate<String, String> template;

  public ProduceOnlyService(KafkaTemplate<String, String> template) {
    this.template = template;
  }

  public void send(String key, String payload) {
    template.send("outbound", key, payload); // idempotent producer prevents duplicates on retry
  }
}
```

## 5.5 Exactly-once consume–process–produce (EOS) with transactions

### 5.5.1 Configuration

- Assign a unique <code>transaction-id-prefix</code> to enable transactions; the producer factory becomes transactional.
- Configure consumers with <code>read_committed</code> to hide uncommitted or aborted results, and disable auto-commit so offset commits are transactional.
- Wire a <code>KafkaTransactionManager</code> into the listener container; the container binds consumed offsets and produced records into a single Kafka transaction.

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:9092
    producer:
      acks: all
      transaction-id-prefix: tx-orders-
      properties:
        enable.idempotence: true
    consumer:
      group-id: orders-eos
      enable-auto-commit: false
      properties:
        isolation.level: read_committed
```

```java
import org.springframework.context.annotation.Bean;
import org.springframework.kafka.core.ProducerFactory;
import org.springframework.kafka.transaction.KafkaTransactionManager;

@Bean
public KafkaTransactionManager<String, String> kafkaTxManager(
    ProducerFactory<String, String> pf) {
  return new KafkaTransactionManager<>(pf);
}
```

```java
import org.springframework.context.annotation.Bean;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.transaction.KafkaTransactionManager;

@Bean
public ConcurrentKafkaListenerContainerFactory<String, String> txContainerFactory(
    ConsumerFactory<String, String> cf,
    KafkaTransactionManager<String, String> txManager) {
  var f = new ConcurrentKafkaListenerContainerFactory<String, String>();
  f.setConsumerFactory(cf);
  f.getContainerProperties().setTransactionManager(txManager);
  f.getContainerProperties().setAckMode(
      org.springframework.kafka.listener.ContainerProperties.AckMode.RECORD);
  return f;
}
```

```java
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
public class EosListener {
  private final KafkaTemplate<String, String> template;

  public EosListener(KafkaTemplate<String, String> template) {
    this.template = template;
  }

  // With txContainerFactory, the container starts a Kafka transaction per poll
  // and commits consumed offsets together with produced records
  @KafkaListener(topics = "orders", groupId = "orders-eos", containerFactory = "txContainerFactory")
  public void process(String value) {
    String transformed = "processed-" + value;
    template.send("orders-processed", null, transformed);
    // Offsets are committed to the transaction by the container on successful completion
  }
}
```

### 5.5.2 Explicit transactional block (alternative)

- For fine-grained control, wrap sends and offset commits in <code>executeInTransaction</code>, then use <code>sendOffsetsToTransaction</code> to include consumed offsets in the same transaction.
- This pattern is useful when combining Kafka with other operations that must occur within the same Kafka transaction boundary.

```java
import org.apache.kafka.clients.consumer.OffsetAndMetadata;
import org.apache.kafka.common.TopicPartition;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import java.util.Map;

@Service
public class EosManualService {
  private final KafkaTemplate<String, String> template;

  public EosManualService(KafkaTemplate<String, String> template) {
    this.template = template;
  }

  public void processAndCommit(String inTopic, int partition, long offset, String outTopic, String key, String value) {
    template.executeInTransaction(ops -> {
      ops.send(outTopic, key, value);
      ops.sendOffsetsToTransaction(
          Map.of(new TopicPartition(inTopic, partition), new OffsetAndMetadata(offset + 1)),
          "orders-eos");
      return null;
    });
  }
}
```

## 5.6 Consumer isolation for transactions

### 5.6.1 Read committed vs read uncommitted

- <code>read_committed</code> ensures consumers only see records from committed transactions, avoiding partial or aborted results at the cost of slightly higher latency.
- <code>read_uncommitted</code> exposes in-flight writes and aborted records; suitable only for special analytics scenarios where strict correctness is not required.
- For EOS pipelines, always use <code>read_committed</code> on the consumer to align visibility with producer transaction boundaries.
- Verify that upstream producers are actually transactional; otherwise, <code>read_committed</code> yields no practical benefit.

```yaml
spring:
  kafka:
    consumer:
      properties:
        isolation.level: read_committed
```

## 5.7 Error handling with transactions

### 5.7.1 Retriable vs non-retriable exceptions

- Retriable exceptions (timeouts, transient broker errors) should trigger retry within the same transaction boundary or a new transaction after rollback.
- Non-retriable errors (serialization, validation) should short-circuit to a Dead Letter Topic while preserving original headers and context for analysis.
- Keep transactions short to reduce the chance of fencing or timeouts; long-running work should be split or offloaded to minimize open transaction time.
- Always log the transaction state on error to simplify root cause analysis and recovery.

```java
import org.springframework.kafka.annotation.RetryableTopic;
import org.springframework.retry.annotation.Backoff;
import org.springframework.kafka.retrytopic.TopicSuffixingStrategy;

@RetryableTopic(
    attempts = "4",
    backoff = @Backoff(delay = 1000, multiplier = 2.0),
    topicSuffixingStrategy = TopicSuffixingStrategy.SUFFIX_WITH_INDEX_VALUE)
@org.springframework.kafka.annotation.KafkaListener(topics = "orders", containerFactory = "txContainerFactory")
public void processWithRetry(String value) {
  // throw to move to retry topics and eventually DLT while the container manages tx boundaries
}
```

## 5.8 Fencing, timeouts, and best practices

### 5.8.1 Producer fencing and transactional IDs

- Each transactional producer must have a unique <code>transactional.id</code>; duplicated IDs across instances cause fencing and immediate failures to protect correctness.
- Use a stable prefix with unique instance suffixes (e.g., <code>tx-orders-</code> + hostname or pod UID) so restarts resume safely without clashing.
- Monitor for fencing exceptions to detect misconfigured prefixes or duplicate deployments that reuse IDs inadvertently.
- Rotate IDs thoughtfully during blue/green deploys to avoid overlapping producers with the same transactional ID.

### 5.8.2 Transaction timeouts

- Transactions that remain open too long risk timeouts or coordinator pressure; break work into smaller units so each transaction completes quickly.
- Align <code>delivery.timeout.ms</code>, consumer <code>max.poll.interval.ms</code>, and any custom backoffs so retries don’t exceed transaction limits.
- Prefer record- or small-batch-scoped transactions for steady flow; large multi-minute transactions amplify recovery complexity on failure.
- Combine transactional sends with idempotent downstream effects (e.g., id-based upserts) to further reduce duplicate risk in cross-system integrations.

## 5.9 Code comparison: at-least-once vs exactly-once

### 5.9.1 At-least-once (manual ack, no transaction)

```java
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.kafka.annotation.KafkaListener;

@KafkaListener(topics = "orders", groupId = "orders-al", containerFactory = "manualAckFactory")
public void handleAl(String value, Acknowledgment ack) {
  // process (idempotent)
  // produce side effects (idempotent)
  ack.acknowledge(); // commit after success (replays possible on crash before commit)
}
```

### 5.9.2 Exactly-once (transactional container, offsets + output atomically)

```java
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;

@KafkaListener(topics = "orders", groupId = "orders-eos", containerFactory = "txContainerFactory")
public void handleEos(String value, KafkaTemplate<String, String> template) {
  // process
  template.send("orders-processed", null, "processed-" + value);
  // on success, the container commits consumed offsets and produced records in one Kafka transaction
}
```
