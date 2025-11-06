# 9. Dead Letter Topics (DLT) and Retry Patterns

Dead Letter Topics capture records that could not be processed successfully after configured retries, enabling durable triage and controlled replay without stalling partitions. This chapter standardizes terminology, shows blocking vs non-blocking retry setups, and provides concise Spring for Kafka snippets with comments. Package names are intentionally omitted in code.

## 9.1 DLT fundamentals

### 9.1.1 Why DLTs

- DLTs isolate poisoned records from the hot path so main consumers keep pace; they also preserve evidence for analysis and replay after fixes.
- Use DLTs to protect SLAs when transient and permanent errors occur; route non-retriable errors directly, and send retriable ones only after bounded attempts.
- Enrich DLT messages with headers (error type, original topic/partition/offset, correlation id) to accelerate triage and safe replay.
- Provision DLT topics explicitly with sufficient retention and appropriate ACLs to meet audit and privacy requirements.

## 9.2 Error classification and routing

### 9.2.1 Retriable vs non-retriable

- Retriable: timeouts, temporary downstream outages; apply exponential backoff and a retry cap before DLT.
- Non-retriable: schema/validation failures, missing required fields; route straight to DLT to avoid head-of-line blocking.
- Maintain an error catalog and metrics per class to identify systemic issues and prioritize fixes.
- Keep callbacks lightweight; heavy logging or synchronous calls inside callbacks can exacerbate latency under failure bursts.

## 9.3 Blocking retries + DLT (DefaultErrorHandler)

### 9.3.1 Configuration and behavior

- Blocking retries happen on the main consumer thread, preserving partition order but potentially stalling it during retries.
- After attempts are exhausted, the recoverer publishes the original record to a DLT (default naming: <code>topic.DLT</code>) with standard headers.
- Use for strict ordering pipelines with low error rates; otherwise, consider non-blocking retries.

```java
// Registers a blocking retry handler with 3 attempts and 1s backoff.
// After retries, messages are published to <topic>.DLT using the provided KafkaTemplate.
@Bean
DefaultErrorHandler defaultErrorHandler(KafkaTemplate<Object, Object> template) {
  var recoverer = new DeadLetterPublishingRecoverer(template);
  return new DefaultErrorHandler(recoverer, new FixedBackOff(1000L, 3L));
}
```

## 9.4 Non-blocking retries + DLT (@RetryableTopic)

### 9.4.1 Configuration and behavior

- Non-blocking retries offload failed records to retry topics with backoff, allowing the main consumer to continue processing other messages.
- After the configured attempts, messages land in the DLT automatically; suffixing strategy controls retry topic names.
- This pattern protects throughput and tail latency for high-SLA pipelines.

```java
// Sends failures to retry topics with exponential backoff; after 5 attempts, routes to DLT.
// The main consumer keeps flowing because retries are offloaded to retry topics.
@RetryableTopic(
    attempts = "5",
    backoff = @Backoff(delay = 1000, multiplier = 2.0),
    topicSuffixingStrategy = TopicSuffixingStrategy.SUFFIX_WITH_INDEX_VALUE)
@KafkaListener(topics = "orders", groupId = "orders-rtr")
public void handle(String value) {
  // Throw exceptions to trigger retry routing and eventual DLT
  throw new RuntimeException("simulate failure");
}
```

## 9.5 DLT headers and schema

### 9.5.1 Recommended headers

- <code>x-exception-class</code>, <code>x-exception-message</code> for diagnostics; avoid full stack trace in headers to limit size.
- <code>x-original-topic</code>, <code>x-original-partition</code>, <code>x-original-offset</code>, <code>x-original-timestamp</code> for lineage and precise replay.
- <code>x-correlation-id</code>, <code>x-schema-version</code> for tracing and compatibility decisions.
- Keep headers concise and store full error context in observability systems linked by IDs.

```java
// Publishes a message to an explicit DLT with diagnostic headers attached.
// In real flows, prefer using the recoverer to preserve the original record and headers automatically.
Message<?> dltMsg = MessageBuilder.withPayload("payload")
  .setHeader(KafkaHeaders.TOPIC, "orders.DLT")
  .setHeader("x-exception-class", "ValidationException")
  .setHeader("x-original-topic", "orders")
  .build();

template.send(dltMsg);
```

## 9.6 DLT topic design and provisioning

### 9.6.1 Naming, partitions, retention

- Name predictably (e.g., <code>orders.DLT</code> or <code>orders-dlt</code>) and match partitions to the source topic for 1:1 replay when feasible.
- Set retention to cover investigation windows (days to weeks); balance storage cost against compliance and operational needs.
- Prefer delete-based retention for full incident visibility; compaction only when messages are deduplicated by key.
- Secure DLTs with ACLs mirroring main topics, with additional restrictions if sensitive data may appear.

```java
// Provisions a DLT with matching partitions for deterministic replay.
// Adjust retention to your investigation/audit window.
@Bean
NewTopic ordersDlt() {
  return TopicBuilder.name("orders.DLT")
      .partitions(12)
      .replicas(3)
      .config("retention.ms", "1209600000") // 14 days
      .build();
}
```

## 9.7 Replay strategies

### 9.7.1 Full vs selective replay

- Full replay republishes the entire DLT back to the main topic after fixes; simple but risky if side effects are not idempotent.
- Selective replay filters by time range, error type, or correlation ID to limit scope and reduce risk during recovery.
- Preserve original headers on replay (lineage + schema version) and add <code>x-replayed</code> and operator metadata for audit trails.
- Throttle replay and monitor consumer lag to avoid overwhelming downstream systems during catch-up.

```java
// Simple DLT consumer that republishes to the main topic (headers preservation omitted here for brevity).
@KafkaListener(topics = "orders.DLT", groupId = "orders-dlt-replay")
public void replay(String value) {
  template.send("orders", null, value); // For real tools, forward original headers as well
}
```

## 9.8 Observability and SLOs

### 9.8.1 Metrics and alerts

- Track retry volumes by topic and error class, DLT inflow rate, oldest message age in DLT, and replay success rates.
- Alert on DLT spikes, rising oldest-age, or replay failures; these indicate upstream schema issues or persistent downstream outages.
- Correlate with deploy timelines and schema registry changes to accelerate root cause analysis.
- Regularly sample DLT records for PII and compliance adherence; apply the same security controls as production topics.

## 9.9 Quick checklist

- Choose blocking retries for strict ordering and low error rates; prefer non-blocking retries for high-throughput pipelines to protect tail latency.
- Enrich DLT headers consistently and cap header sizes; store detailed diagnostics externally and link via correlation IDs.
- Provision DLTs explicitly with retention aligned to investigation windows; secure them with appropriate ACLs.
- Build safe replay tooling that preserves lineage, filters scope, and throttles throughput; document runbooks for on-call use.
- Treat DLT metrics as first-class SLOs; recurring patterns should trigger schema hardening, validation improvements, or upstream contract fixes.
