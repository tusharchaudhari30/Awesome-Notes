# 6. Streams and Connect

Kafka Streams provides a high-level DSL to build event-driven, stateful processing topologies, while Kafka Connect moves data between Kafka and external systems with pluggable connectors; below are essentials, hands-on Spring for Kafka Streams examples, and when to choose Streams vs Connect.

## 6.1 Streams vs @KafkaListener

### 6.1.1 Mindset and use-cases

- @KafkaListener is record-driven: a consumer pulls records and custom code handles processing, making it great for imperative flows and external side effects.
- Kafka Streams is topology-driven: a graph of sources, transformations, and sinks processes continuous streams with built-in state, windowing, joins, and exactly-once guarantees.
- Choose Streams for event-time processing, aggregations, joins, and materialized views; choose @KafkaListener for simple handlers, orchestration, or heavy external calls.
- Both can coexist: a service may use Streams for core processing and @KafkaListener for ancillary tasks or DLT handling.

### 6.1.2 Code difference: listener vs streams

```java
// @KafkaListener: imperative consume → transform → produce
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
class OrdersListener {
  private final KafkaTemplate<String, String> template;
  OrdersListener(KafkaTemplate<String, String> template) { this.template = template; }

  @KafkaListener(topics = "orders", groupId = "orders-listener")
  public void consume(String value) {
    String transformed = "L|" + value; // simple logic
    template.send("orders-out", null, transformed);
  }
}
```

```java
// Kafka Streams: declarative topology with map/filter/branch/joins
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.kstream.KStream;
import org.springframework.context.annotation.Bean;
import org.springframework.kafka.annotation.EnableKafkaStreams;
import org.springframework.stereotype.Configuration;

@Configuration
@EnableKafkaStreams
class StreamsTopology {

  @Bean
  public KStream<String, String> ordersStream(StreamsBuilder builder) {
    KStream<String, String> in = builder.stream("orders");
    KStream<String, String> cleaned = in
        .filter((k, v) -> v != null && !v.isBlank())
        .mapValues(v -> "S|" + v); // simple logic
    cleaned.to("orders-out");
    return cleaned;
  }
}
```

## 6.2 Streams essentials: KStream, KTable, GlobalKTable

### 6.2.1 What they represent

- KStream is an unbounded stream of immutable events, ideal for filtering, mapping, branching, and windowed aggregations over time.
- KTable is a materialized view of the latest value per key (a changelog), ideal for lookups, deduplication, and building current-state projections.
- GlobalKTable replicates the entire table to each instance for local lookups without data shuffles, useful for small reference data across all partitions.
- Practical pattern: join a KStream of events with a KTable of reference data to enrich records before producing them to a sink topic.

### 6.2.2 Code: stream–table join

```java
import org.apache.kafka.streams.kstream.*;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.state.Stores;
import org.springframework.context.annotation.Bean;

@Bean
public KStream<String, String> enrich(StreamsBuilder builder) {
  KStream<String, String> events = builder.stream("payments");
  KTable<String, String> users = builder.table("users"); // userId -> profile
  KStream<String, String> enriched = events.leftJoin(users,
      (event, profile) -> event + "|u=" + (profile == null ? "unknown" : profile),
      Joined.with(Serdes.String(), Serdes.String(), Serdes.String()));
  enriched.to("payments-enriched");
  return enriched;
}
```

## 6.3 Stateless vs Stateful

### 6.3.1 Stateless operations

- Stateless transforms (map/filter/branch/flatMap) don’t maintain history; they scale linearly and avoid state stores.
- They’re ideal for cleansing, format conversion, and simple routing, keeping latency low and throughput high.
- When keys change mid-pipeline, repartitioning may be required (grouping or selectKey) to maintain correct partition-local semantics.
- Use stateless steps early to reduce payloads before expensive stateful aggregations.

### 6.3.2 Stateful operations and windows

```java
import org.apache.kafka.streams.kstream.TimeWindows;
import org.apache.kafka.streams.kstream.Materialized;
import java.time.Duration;

@Bean
public KTable<org.apache.kafka.streams.kstream.Windowed<String>, Long> countOrders(StreamsBuilder builder) {
  return builder.stream("orders")
      .selectKey((k, v) -> v.split(":")[0]) // e.g., key by userId
      .groupByKey()
      .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(1)))
      .count(Materialized.as("orders-per-minute-store")); // state store
}
```

- Stateful operations like groupBy, aggregate, and windowed counts create local state backed by changelog topics; they enable time-based analytics and materialized views.
- State stores are fault-tolerant (recovered on restart from changelog) and can be queried locally for low-latency reads.
- Tuning retention and window grace is key to balance correctness (late arrivals) versus memory footprint and result stability.
- Always use stable keys before grouping; accidental key skew can create hotspots and uneven load.

## 6.4 Serdes and schemas

### 6.4.1 Configuring Serdes in Spring

```java
import org.apache.kafka.streams.StreamsConfig;
import org.springframework.context.annotation.Bean;
import org.springframework.kafka.config.KafkaStreamsConfiguration;

@Bean(name = org.springframework.kafka.config.KafkaStreamsDefaultConfiguration.DEFAULT_STREAMS_CONFIG_BEAN_NAME)
public KafkaStreamsConfiguration streamsConfig() {
  var props = new java.util.HashMap<String, Object>();
  props.put(StreamsConfig.APPLICATION_ID_CONFIG, "orders-streams-app");
  props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
  props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, org.apache.kafka.common.serialization.Serdes.StringSerde.class);
  props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, org.apache.kafka.common.serialization.Serdes.StringSerde.class);
  return new KafkaStreamsConfiguration(props);
}
```

- Serdes define how keys and values are serialized/deserialized; consistent Serdes on both sides are required for correct processing.
- Use StringSerde for simple payloads, and switch to schema-aware formats (Avro/Protobuf/JSON) with matching Serdes when contracts evolve across teams.
- For performance, prefer binary Serdes and avoid large JSON payloads in stateful pipelines due to serialization overhead.
- Keep Serdes declarations explicit in joins and aggregations to avoid implicit defaults causing subtle bugs.

## 6.5 Repartitioning and keys

### 6.5.1 Why repartition happens

- Repartitioning is required when the key used by a stateful operator differs from the current record key, ensuring related keys co-locate on the same partition.
- Operations like groupBy or selectKey can trigger repartition topics implicitly to shuffle data correctly.
- Excessive repartitions increase network IO; pre-key records earlier to minimize shuffles and batch key changes together where possible.
- Monitor repartition topics for throughput spikes and optimize key selection to reduce unnecessary reshuffles.

### 6.5.2 Code: selectKey then group

```java
@Bean
public KTable<String, Long> perAccountCount(StreamsBuilder builder) {
  return builder.stream("tx")
      .selectKey((k, v) -> v.split(",")[1]) // accountId as new key
      .groupByKey()
      .count(Materialized.as("tx-per-account-store"));
}
```

## 6.6 Exactly-once (EOS) in Streams

### 6.6.1 Processing guarantee

```java
import org.apache.kafka.streams.StreamsConfig;

@Bean(name = org.springframework.kafka.config.KafkaStreamsDefaultConfiguration.DEFAULT_STREAMS_CONFIG_BEAN_NAME)
public KafkaStreamsConfiguration eosConfig() {
  var props = new java.util.HashMap<String, Object>();
  props.put(StreamsConfig.APPLICATION_ID_CONFIG, "orders-eos-app");
  props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
  props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG, StreamsConfig.EXACTLY_ONCE_V2);
  return new KafkaStreamsConfiguration(props);
}
```

- Exactly-once v2 ensures transactional writes to output topics and state stores, preventing duplicates and partial results even during failures.
- It coordinates producer idempotence, transactional sinks, and state-store changelog commits under a single guarantee.
- EOS adds overhead; use it for financial, inventory, or critical compliance logic where duplicates are unacceptable.
- Keep transactions short and topologies focused to reduce coordination overhead and improve stability.

## 6.7 Error handling in Streams

### 6.7.1 Handling deserialization/production errors

```java
@Bean(name = org.springframework.kafka.config.KafkaStreamsDefaultConfiguration.DEFAULT_STREAMS_CONFIG_BEAN_NAME)
public KafkaStreamsConfiguration errorAwareConfig() {
  var props = new java.util.HashMap<String, Object>();
  props.put(org.apache.kafka.streams.StreamsConfig.APPLICATION_ID_CONFIG, "orders-err-app");
  props.put(org.apache.kafka.streams.StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
  props.put(org.apache.kafka.streams.StreamsConfig.DEFAULT_DESERIALIZATION_EXCEPTION_HANDLER_CLASS_CONFIG,
      org.apache.kafka.streams.errors.LogAndContinueExceptionHandler.class);
  props.put(org.apache.kafka.streams.StreamsConfig.DEFAULT_PRODUCTION_EXCEPTION_HANDLER_CLASS_CONFIG,
      org.apache.kafka.streams.errors.DefaultProductionExceptionHandler.class);
  return new KafkaStreamsConfiguration(props);
}
```

- DeserializationExceptionHandler can skip or fail on bad records; LogAndContinue avoids pipeline stops but may drop invalid messages—pair with side channels if you need DLTs.
- ProductionExceptionHandler decides whether to continue or fail on send errors; in EOS mode, production failures typically cause task restarts.
- Validation errors are application-level; branch invalid records to a DLT topic explicitly to preserve evidence and enable replay.
- Always capture metrics on dropped or failed records to trigger alerts and drive schema fixes.

### 6.7.2 Code: validation branch to DLT

```java
@Bean
public KStream<String, String> validateAndRoute(StreamsBuilder builder) {
  KStream<String, String> in = builder.stream("orders");
  KStream<String, String>[] branches = in.branch(
      (k, v) -> v != null && v.startsWith("OK|"),
      (k, v) -> true
  );
  branches[0].to("orders-ok");
  branches[1].to("orders-dlt"); // application-defined DLT for invalid payloads
  return branches[0];
}
```

## 6.8 State stores and interactive queries

### 6.8.1 Materialized store and querying

```java
import org.apache.kafka.streams.state.QueryableStoreTypes;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.config.StreamsBuilderFactoryBean;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/counts")
class CountsController {

  @Autowired
  private StreamsBuilderFactoryBean fb;

  @GetMapping("/{key}")
  public String getCount(@PathVariable String key) {
    var streams = fb.getKafkaStreams();
    var store = streams.store("orders-per-minute-store", QueryableStoreTypes.<String, Long>keyValueStore());
    var value = store.get(key);
    return value == null ? "0" : value.toString();
  }
}
```

- Materialized.as creates a named local state store that Kafka Streams maintains and restores from a changelog topic on restart.
- Interactive queries allow low-latency reads directly from the local store (or via a routing layer to the host owning the key’s partition).
- For correctness under rebalances, expose endpoint discovery so callers can route to the instance hosting the key’s state.
- Secure and rate-limit interactive queries; they share resources with stream processing and should not starve the pipeline.

## 6.9 Connect essentials (conceptual)

### 6.9.1 What Kafka Connect solves

- Connect moves data between Kafka and external systems using declarative connectors (source: external → Kafka, sink: Kafka → external) without custom code.
- It tracks offsets for sources and supports Single Message Transforms for lightweight changes, making pipelines repeatable and operations-friendly.
- Choose distributed mode for production to scale and tolerate failures; standalone mode suits development or single-node tasks.
- Prefer Connect when integrating databases, object stores, or SaaS systems; prefer Streams or @KafkaListener for custom business logic, joins, and stateful processing.

## 6.10 Choosing Streams vs Connect

### 6.10.1 Selection guide

- Use Streams for continuous transformations, windowed aggregations, joins, and materialized views with exactly-once guarantees and local state.
- Use Connect to ingest/extract data from external systems with minimal code, leveraging robust offset management and connector ecosystems.
- In a typical pipeline, Connect ingests data, Streams processes and enriches it, and a sink connector delivers curated outputs to analytics or OLTP stores.
- Keep responsibilities clear: Connect for data movement, Streams for computation; avoid mixing heavy business logic into connectors to retain testability and portability.
