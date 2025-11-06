# 10. Spring Kafka Transactions — Cheat Sheet (with commented code)

Practical, copy-ready snippets to enable exactly-once consume–process–produce pipelines in Spring for Kafka, with inline comments to explain the why and how.

## 10.1 Producer and Consumer Configuration

### application.yml

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:9092

    # Producer must be idempotent and transactional for EOS
    producer:
      acks: all
      transaction-id-prefix: tx-app- # unique per app; instance suffix added by Spring
      properties:
        enable.idempotence: true # dedupe retries on broker

    # Consumer must not auto-commit; use read_committed to hide aborted writes
    consumer:
      group-id: eos-app
      enable-auto-commit: false
      properties:
        isolation.level: read_committed # only see committed transactional writes
```

## 10.2 Transaction Manager Bean

```java
// Binds the ProducerFactory to Kafka transactions so KafkaTemplate participates
@Bean
KafkaTransactionManager<String, String> kafkaTxManager(ProducerFactory<String, String> pf) {
  return new KafkaTransactionManager<>(pf);
}
```

## 10.3 Transactional Listener Container

```java
// Container uses the transaction manager; ack mode RECORD commits one-by-one
@Bean
ConcurrentKafkaListenerContainerFactory<String, String> txContainerFactory(
    ConsumerFactory<String, String> cf,
    KafkaTransactionManager<String, String> txManager) {

  var f = new ConcurrentKafkaListenerContainerFactory<String, String>();
  f.setConsumerFactory(cf);
  f.getContainerProperties().setTransactionManager(txManager); // start tx per poll
  f.getContainerProperties().setAckMode(
      org.springframework.kafka.listener.ContainerProperties.AckMode.RECORD); // commit per record
  return f;
}
```

## 10.4 Consume–Process–Produce Atomically (Container-managed)

```java
// The container starts a Kafka transaction before invoking this method.
// All template.send(...) calls are enlisted automatically.
// On success, the container commits produced records + consumed offsets atomically.
// On exception, the transaction is aborted; records are redelivered, no partial output leaks.
@KafkaListener(topics = "in", groupId = "eos-app", containerFactory = "txContainerFactory")
public void handle(String value, KafkaTemplate<String, String> template) {

  // 1) Transform the input (keep work fast to avoid long open transactions)
  String out = "processed-" + value;

  // 2) Produce to an output topic using the same KafkaTemplate bound to the transaction
  template.send("out", null, out);

  // 3) Do NOT call ack here; the container will commit offsets in the same Kafka transaction
  //    If an exception is thrown before this method returns, the tx will abort and offsets won't commit
}
```

## 10.5 Manual Transaction Control (Advanced)

```java
// For fine-grained control (multi-topic, external prechecks), wrap work in executeInTransaction.
// Include consumed offsets in the same tx via sendOffsetsToTransaction(...).
public void processWithManualTx(
    KafkaTemplate<String, String> template,
    String inTopic, int partition, long lastProcessedOffset,
    String outTopic, String key, String value) {

  template.executeInTransaction(ops -> {
    // 1) Produce all required outputs within the tx
    ops.send(outTopic, key, value);

    // 2) Commit consumed offsets atomically with outputs (offset+1 is the next to consume)
    var tp = new org.apache.kafka.common.TopicPartition(inTopic, partition);
    var om = new org.apache.kafka.clients.consumer.OffsetAndMetadata(lastProcessedOffset + 1);

    // The 'groupId' must match the consumer group reading the input
    ops.sendOffsetsToTransaction(java.util.Map.of(tp, om), "eos-app");

    // 3) Returning normally commits the transaction; throw to abort
    return null;
  });
}
```

## 10.6 Error Handling and Retries

```java
// Prefer short transactions: catch non-retriable errors and route to DLT outside the tx,
// let retriable exceptions bubble so the container aborts and redelivers cleanly.

@KafkaListener(topics = "in", groupId = "eos-app", containerFactory = "txContainerFactory")
public void handleWithDLT(String value, KafkaTemplate<String, String> t) {
  if (!isValid(value)) {
    // Non-retriable: produce to DLT outside the tx (no offsets committed in tx)
    t.executeInTransaction(tx -> null); // ensure any active tx is closed cleanly
    t.send("in.DLT", null, value);      // side-channel for bad records
    return;                             // container still controls offset commit in tx
  }
  t.send("out", null, transform(value));
}
```

Notes:

- Keep per-call work small; long transactions increase coordinator pressure and risk timeouts.
- Align <code>delivery.timeout.ms</code> and <code>max.poll.interval.ms</code> with worst-case under load so transactions don’t abort unexpectedly.
- Use DLT for non-retriable failures; for transient issues, let exceptions propagate so the container aborts and retries safely.

## 10.7 Testing EOS

```java
// Use @EmbeddedKafka to simulate end-to-end EOS:
// 1) Send to 'in'
// 2) Start transactional listener -> produces to 'out'
// 3) Assert 'out' only has records visible to read_committed consumers
@EmbeddedKafka(partitions = 1, topics = { "in", "out" })
class TxTests {
  // write inputs, read outputs with a consumer set to isolation.level=read_committed
  // inject faults to verify aborts redeliver and do not leak partial results
}
```

## 10.8 Operational Guardrails

- Transactional IDs must be unique per running instance; prefix via <code>transaction-id-prefix</code> and let Spring suffix per-producer to avoid fencing.
- Never mix transactional and non-transactional sends for the same flow; always use the transactional template within the listener.
- Monitor producer retries, transaction aborts, and <code>read_committed</code> consumer lag; spikes indicate coordinator pressure or slow downstreams.
- Prefer record- or small-batch-scoped transactions; large multi-minute transactions complicate recovery and increase failure blast radius.
