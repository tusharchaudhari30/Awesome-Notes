# 1. Spring for Apache Kafka — Descriptive Explanations with Commented Code

Below is a thorough, production-oriented explanation of each commonly used Spring for Apache Kafka class/interface with concise, commented examples. Imports use `import *`, inline API names use `<code>`, and examples use `java`

## 1.1 Producers

### 1.1.1 KafkaTemplate

- Description: A high-level producer façade that manages a shared Kafka producer from a <code>ProducerFactory</code>, exposing simple <code>send</code> methods, header-aware <code>Message</code> sends, and transaction utilities. Optimized for async usage via futures/callbacks; can be configured with a default topic to reduce boilerplate.
- Key capabilities:
  - <code>send(topic, key, value)</code>, <code>sendDefault(value)</code> for convenience.
  - <code>executeInTransaction</code> ensures all sends inside the callback participate in a Kafka transaction.
  - <code>flush</code> provides bounded-latency delivery in batchy workloads.

```java
@Service
class OrderProducer {
  private final KafkaTemplate<String, String> template;

  OrderProducer(KafkaTemplate<String, String> template) {
    this.template = template;
    this.template.setDefaultTopic("orders"); // set default to avoid passing topic every time
  }

  // 1) Async send with callback — non-blocking hot path recommended
  void sendAsync(String key, String payload) {
    template.send("orders", key, payload)
        .whenComplete((md, ex) -> {
          if (ex != null) {
            // log, meter, or route to fallback DLQ
          } else {
            // md contains topic/partition/offset for observability
          }
        });
  }

  // 2) Headers via Spring Message — useful for correlation and routing
  void sendWithHeaders(String key, String payload) {
    Message<String> msg = MessageBuilder.withPayload(payload)
        .setHeader(KafkaHeaders.TOPIC, "orders")
        .setHeader(KafkaHeaders.MESSAGE_KEY, key)
        .setHeader("correlationId", java.util.UUID.randomUUID().toString())
        .build();
    template.send(msg);
  }

  // 3) Transactional send — requires transactional ProducerFactory configuration
  void sendInTransaction(String key, String payload) {
    template.executeInTransaction(ops -> {
      ops.send("orders", key, payload);
      // multiple ops.send(...) calls here are part of the same Kafka TX
      return null;
    });
  }

  // 4) Synchronous publish for rare admin/maintenance flows
  void sendSync(String key, String payload) throws Exception {
    var md = template.send("admin-orders", key, payload).get(); // avoid on high-throughput path
    // use md for confirmation logging in admin tasks
  }

  // 5) Use default topic and drain pending
  void sendDefaultAndFlush(String payload) {
    template.sendDefault(payload);
    template.flush(); // ensure timely delivery on batchy workloads
  }
}
```

### 1.1.2 RoutingKafkaTemplate

- Description: Routes send operations to different <code>ProducerFactory</code> instances based on topic name patterns. Enables per-topic clusters or per-topic performance/security profiles without changing call sites.
- Typical uses: Separate “hot-path” topics from durable audit topics; multi-cluster or multi-credential environments.

```java
@Configuration
class RoutingConfig {

  @Bean
  RoutingKafkaTemplate routingTemplate(
      ProducerFactory<Object, Object> lowLatencyPf,
      ProducerFactory<Object, Object> durablePf,
      ProducerFactory<Object, Object> defaultPf) {

    var routes = new LinkedHashMap<Pattern, ProducerFactory<Object, Object>>();
    routes.put(Pattern.compile("realtime-.*"), lowLatencyPf); // low latency route
    routes.put(Pattern.compile("audit-.*"), durablePf);       // high durability route

    // defaultPf used if no pattern matches
    return new RoutingKafkaTemplate(routes, defaultPf);
  }
}

@Service
class RoutedSender {
  private final RoutingKafkaTemplate rt;
  RoutedSender(RoutingKafkaTemplate rt) { this.rt = rt; }

  void sendRealtime(String k, String v) { rt.send("realtime-events", k, v); } // goes to lowLatencyPf
  void sendAudit(String k, String v)    { rt.send("audit-events", k, v); }    // goes to durablePf
  void sendOther(String k, String v)    { rt.send("misc", k, v); }            // falls back to defaultPf
}
```

### 1.1.3 ProducerFactory, DefaultKafkaProducerFactory, ProducerListener

- Description: <code>ProducerFactory</code> builds Kafka producers; <code>DefaultKafkaProducerFactory</code> is the standard implementation used by <code>KafkaTemplate</code>; <code>ProducerListener</code> hooks into success/failure events for metrics and tracing.
- Guidance: Centralize producer config (idempotence, serializers, retries); attach a listener once for all producers.

```java
@Configuration
class ProducerBootstrapping {

  @Bean
  ProducerListener<String, String> producerListener() {
    // MicrometerProducerListener emits metrics; custom impls can add tags or tracing
    return new MicrometerProducerListener<>();
  }

  @Bean
  ProducerFactory<String, String> producerFactory(ProducerListener<String, String> listener) {
    var pf = new DefaultKafkaProducerFactory<String, String>(new HashMap<>());
    pf.addListener(listener); // one place to observe all sends
    return pf;
  }

  @Bean
  KafkaTemplate<String, String> kafkaTemplate(ProducerFactory<String, String> pf) {
    return new KafkaTemplate<>(pf);
  }
}
```

## 1.2 Consumers

### 1.2.1 @KafkaListener

- Description: Declarative listener that binds a method to consume records or batches. Works with container factories to control concurrency, ack mode, error handling, and transactions.
- Key tips:
  - Use manual ack for at-least-once control.
  - Use batch mode for throughput; ensure idempotent batch handling.

```java
@Component
class OrdersListener {

  // Record-by-record with manual commit for controlled at-least-once
  @KafkaListener(topics = "orders", groupId = "orders-app", containerFactory = "manualAckFactory")
  void onRecord(String value, Acknowledgment ack) {
    // process business logic
    ack.acknowledge(); // commit only after successful processing
  }

  // Batch listener for higher throughput; commit strategy depends on factory ack mode
  @KafkaListener(topics = "orders-batch", groupId = "orders-batch-app", containerFactory = "batchFactory")
  void onBatch(List<String> values) {
    // process the whole batch atomically in app domain
  }
}
```

### 1.2.2 KafkaListenerContainerFactory, ConcurrentKafkaListenerContainerFactory, KafkaMessageListenerContainer

- Description: Factories configure and create listener containers. <code>ConcurrentKafkaListenerContainerFactory</code> scales consumption across threads; it wraps one or more <code>KafkaMessageListenerContainer</code> instances under the hood.
- Important knobs:
  - <code>setBatchListener</code>, <code>setCommonErrorHandler</code>, <code>setConcurrency</code>, and <code>ContainerProperties.AckMode</code>.

```java
@Configuration
class ListenerFactoryConfig {

  @Bean
  ConcurrentKafkaListenerContainerFactory<String, String> manualAckFactory(
      ConsumerFactory<String, String> cf,
      DefaultErrorHandler errorHandler) {

    var f = new ConcurrentKafkaListenerContainerFactory<String, String>();
    f.setConsumerFactory(cf);
    f.setCommonErrorHandler(errorHandler); // consistent retry/DLT policy
    f.getContainerProperties().setAckMode(ContainerProperties.AckMode.MANUAL_IMMEDIATE);
    f.setConcurrency(3); // one thread per partition (up to partitions)
    return f;
  }

  @Bean
  ConcurrentKafkaListenerContainerFactory<String, String> batchFactory(ConsumerFactory<String, String> cf) {
    var f = new ConcurrentKafkaListenerContainerFactory<String, String>();
    f.setConsumerFactory(cf);
    f.setBatchListener(true); // batch delivery for throughput
    f.getContainerProperties().setAckMode(ContainerProperties.AckMode.BATCH);
    return f;
  }
}
```

### 1.2.3 MessageListener, Acknowledgment, ConsumerFactory, DefaultKafkaConsumerFactory, ConsumerAwareListenerErrorHandler, RecordFilterStrategy

- Description: Lower-level and supportive contracts. <code>MessageListener</code> is the functional callback; <code>Acknowledgment</code> commits manually; <code>ConsumerFactory</code> creates Kafka consumers; <code>ConsumerAwareListenerErrorHandler</code> lets the listener handle errors and access the consumer; <code>RecordFilterStrategy</code> skips records before reaching the business method.
- Use cases: Programmatic container setup, upstream filtering, fine-grained error handling.

```java
@Configuration
class ConsumerFineGrainConfig {

  @Bean
  ConsumerFactory<String, String> consumerFactory() {
    return new DefaultKafkaConsumerFactory<>(new HashMap<>());
  }

  @Bean
  RecordFilterStrategy<String, String> dropBlanks() {
    // return true to filter (skip) a record
    return rec -> rec.value() == null || rec.value().isBlank();
  }

  @Bean
  ConcurrentKafkaListenerContainerFactory<String, String> filteredFactory(ConsumerFactory<String, String> cf) {
    var f = new ConcurrentKafkaListenerContainerFactory<String, String>();
    f.setConsumerFactory(cf);
    f.setRecordFilterStrategy(dropBlanks()); // upstream filtering
    return f;
  }

  @Bean
  ConsumerAwareListenerErrorHandler consumerAwareEh() {
    return (msg, ex, consumer) -> {
      // can inspect consumer position, seek, or record headers
      return null;
    };
  }
}
```

## 1.3 Listener containers and properties

### 1.3.1 ContainerProperties, CommonContainerStoppingErrorHandler, BatchErrorHandler, GenericMessageListenerContainer

- Description:
  - <code>ContainerProperties</code> holds core container behavior: ack mode, idle events, TX manager, poll timeouts, and more.
  - <code>CommonContainerStoppingErrorHandler</code> stops the container on unrecoverable errors (fail-fast).
  - <code>BatchErrorHandler</code> defines how batch consumption errors are handled.
  - <code>GenericMessageListenerContainer</code> general abstraction implemented by concrete containers.
- Guidance: Emit idle events for liveness probes; use stopping handler for critical pipes that must not continue after certain failures.

```java
@Configuration
class ContainerBehaviorConfig {

  @Bean
  ConcurrentKafkaListenerContainerFactory<String, String> stoppableFactory(ConsumerFactory<String, String> cf) {
    var f = new ConcurrentKafkaListenerContainerFactory<String, String>();
    f.setConsumerFactory(cf);
    f.setCommonErrorHandler(new CommonContainerStoppingErrorHandler()); // fail-fast
    f.getContainerProperties().setIdleEventInterval(15000L); // emit idle event every 15s
    return f;
  }
}
```

## 1.4 Error handling, retries, DLT

### 1.4.1 DefaultErrorHandler, DeadLetterPublishingRecoverer, SeekToCurrentErrorHandler, BackOff, FixedBackOff, ExponentialBackOffWithMaxRetries, ErrorHandlingDeserializer, ErrorHandlingDeserializer2

- Description:
  - <code>DefaultErrorHandler</code> performs blocking retries within the same partition context and delegates to a recoverer (like <code>DeadLetterPublishingRecoverer</code>) after max attempts.
  - <code>DeadLetterPublishingRecoverer</code> sends failed records to DLT, with customizable topic/partition mapping.
  - <code>SeekToCurrentErrorHandler</code> is an older approach; use only when on older Spring Kafka versions.
  - <code>BackOff</code> family controls retry timing; <code>ErrorHandlingDeserializer(2)</code> wraps underlying deserializers so errors surface predictably to handlers.
- Guidance: Always define a DLT policy; exclude non-retryable exception types to avoid partition stalls.

```java
@Configuration
class ErrorHandlingConfig {

  @Bean
  DefaultErrorHandler defaultErrorHandler(KafkaTemplate<Object, Object> template) {
    // Recoverer to publish to <topic>.DLT; keep partition by default or customize below
    var recoverer = new DeadLetterPublishingRecoverer(
        template,
        (rec, ex) -> new org.apache.kafka.common.TopicPartition(rec.topic() + ".DLT", rec.partition())
    );

    // Retry 3 times with 1s delay between attempts
    var eh = new DefaultErrorHandler(recoverer, new FixedBackOff(1000L, 3L));

    // Avoid pointless retries for known invalid data
    eh.addNotRetryableExceptions(IllegalArgumentException.class);

    // Mark recovered as committed to move on from poison pills
    eh.setCommitRecovered(true);

    // Optional: observe each retry for metrics
    eh.setRetryListeners((rec, ex, attempt) -> { /* custom metrics */ });

    return eh;
  }

  @Bean
  DefaultKafkaConsumerFactory<String, String> consumerFactoryWithEHD() {
    var props = new HashMap<String, Object>();
    // Wrap value deserializer so deserialization errors can be handled uniformly
    props.put(ErrorHandlingDeserializer.VALUE_DESERIALIZER_CLASS, org.apache.kafka.common.serialization.StringDeserializer.class);
    props.put(org.apache.kafka.clients.consumer.ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, ErrorHandlingDeserializer2.class);
    return new DefaultKafkaConsumerFactory<>(props);
  }
}
```

## 1.5 Retryable topics

### 1.5.1 RetryableTopic, Backoff (annotation), DltHandler, TopicSuffixingStrategy

- Description: Enables non-blocking retries by routing failures to retry topics with backoff policies; after attempts are exhausted, messages land in DLT. Keeps the main partition flowing and scales retry consumers independently.
- Guidance: Use for high-throughput flows where blocking the partition is unacceptable.

```java
@Component
class PaymentsHandler {

  @RetryableTopic(
      attempts = "5",
      backoff = @Backoff(delay = 1000, multiplier = 2.0),
      topicSuffixingStrategy = TopicSuffixingStrategy.SUFFIX_WITH_INDEX_VALUE,
      autoCreateTopics = "true" // convenient for dev/test
  )
  @KafkaListener(topics = "payments", groupId = "pay-app")
  void handle(String value) {
    // Throwing triggers retry topic chain; exhausted => DLT
    if (!value.startsWith("OK|")) throw new RuntimeException("transient");
  }

  @DltHandler
  void onDlt(String value) {
    // Terminal remediation, alerting, or parking
  }
}
```

### 1.5.2 RetryTopicConfiguration, RetryTopicConfigurationBuilder

- Description: Programmatic alternative to annotations; useful when centralizing retry policy for many topics or setting dynamic policies.
- Guidance: Prefer builder when annotation duplication would be high.

```java
@Configuration
class RetryProgrammaticConfig {

  @Bean
  RetryTopicConfiguration retryConfig(KafkaTemplate<String, String> template) {
    return RetryTopicConfigurationBuilder
        .newInstance()
        .fixedBackOff(1000)   // 1s fixed delay
        .maxAttempts(4)       // total attempts including original
        .includeTopic("payments")
        .dltSuffix(".DLT")
        .create(template);
  }
}
```

## 1.6 Transactions

### 1.6.1 KafkaTransactionManager, KafkaAwareTransactionManager, ChainedKafkaTransactionManager, ProducerFactoryUtils

- Description:
  - <code>KafkaTransactionManager</code> bridges Spring transactions to Kafka producer transactions so <code>@Transactional</code> methods send atomically.
  - <code>KafkaAwareTransactionManager</code> marks transaction managers that understand Kafka semantics.
  - <code>ChainedKafkaTransactionManager</code> composes multiple managers (e.g., DB + Kafka) for a single atomic unit.
  - <code>ProducerFactoryUtils</code> contains low-level helpers; often unnecessary when using the manager and template.
- Guidance: Use container-managed transactions for consume–process–produce EOS; use <code>Chained</code> manager only if multi-resource atomicity is essential.

```java
@Configuration
class TxConfig {

  @Bean
  KafkaTransactionManager<String, String> kafkaTxManager(ProducerFactory<String, String> pf) {
    return new KafkaTransactionManager<>(pf); // requires transaction-id-prefix in PF config
  }

  @Bean
  ConcurrentKafkaListenerContainerFactory<String, String> txFactory(
      ConsumerFactory<String, String> cf,
      KafkaTransactionManager<String, String> txManager) {
    var f = new ConcurrentKafkaListenerContainerFactory<String, String>();
    f.setConsumerFactory(cf);
    f.getContainerProperties().setTransactionManager(txManager);
    f.getContainerProperties().setAckMode(ContainerProperties.AckMode.RECORD);
    return f;
  }
}

@Component
class EosPipeline {
  private final KafkaTemplate<String, String> template;
  EosPipeline(KafkaTemplate<String, String> template) { this.template = template; }

  @KafkaListener(topics = "in", groupId = "eos", containerFactory = "txFactory")
  void on(String v) {
    // This send and the offset commit are part of the same Kafka transaction
    template.send("out", "processed|" + v);
  }
}
```

## 1.7 Admin and provisioning

### 1.7.1 KafkaAdmin, NewTopic, TopicBuilder, AdminClientConfig

- Description:
  - <code>KafkaAdmin</code> registers admin client properties and enables bean-driven topic provisioning at startup.
  - <code>NewTopic</code> and <code>TopicBuilder</code> declare topics idempotently with partitions, replicas, and configs (e.g., retention, compaction).
  - <code>AdminClientConfig</code> offers constants for client keys used in the properties map.
- Guidance: Avoid auto-create in production; encode SLAs (retention, min ISR) in <code>NewTopic</code> beans for repeatable environments.

```java
@Configuration
class TopicProvisioning {

  @Bean
  KafkaAdmin kafkaAdmin() {
    var props = new HashMap<String, Object>();
    props.put(org.apache.kafka.clients.admin.AdminClientConfig.CLIENT_ID_CONFIG, "spring-admin"); // readable client.id
    return new KafkaAdmin(props);
  }

  @Bean
  NewTopic orders() {
    return TopicBuilder.name("orders")
        .partitions(12)
        .replicas(3)
        .config("min.insync.replicas", "2")
        .config("retention.ms", "604800000") // 7 days
        .build();
  }

  @Bean
  NewTopic ordersDlt() {
    return TopicBuilder.name("orders.DLT")
        .partitions(12)
        .replicas(3)
        .config("retention.ms", "1209600000") // 14 days
        .build();
  }
}
```

## 1.8 Messaging integration

### 1.8.1 KafkaHeaders, Messaging adapters and converters

- Description:
  - <code>KafkaHeaders</code> defines standard header keys (topic, key, partition, timestamp), enabling routing and tracing via Spring <code>Message</code>.
  - <code>MessagingMessageListenerAdapter</code>, <code>MessagingMessageConverter</code>, <code>RecordMessageConverter</code>, and <code>StringJsonMessageConverter</code> bridge between Spring Messaging and Kafka record formats.
  - <code>JsonSerializer</code> and <code>JsonDeserializer</code> help serialize structured payloads (POJOs) without manual conversion.
- Guidance: Favor headers for correlation IDs and schema versioning; configure JSON converters when using typed payloads.

```java
@Configuration
class JsonMessageConfig {

  @Bean
  ProducerFactory<String, Object> jsonProducerFactory() {
    var props = new HashMap<String, Object>();
    props.put(org.apache.kafka.clients.producer.ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, JsonSerializer.class);
    return new DefaultKafkaProducerFactory<>(props);
  }

  @Bean
  ConsumerFactory<String, Object> jsonConsumerFactory() {
    var props = new HashMap<String, Object>();
    props.put(org.apache.kafka.clients.consumer.ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, JsonDeserializer.class);
    props.put(JsonDeserializer.TRUSTED_PACKAGES, "*"); // trust app packages; restrict in prod
    return new DefaultKafkaConsumerFactory<>(props);
  }

  @Bean
  ConcurrentKafkaListenerContainerFactory<String, Object> jsonListenerFactory(ConsumerFactory<String, Object> cf) {
    var f = new ConcurrentKafkaListenerContainerFactory<String, Object>();
    f.setConsumerFactory(cf);
    f.setMessageConverter(new StringJsonMessageConverter()); // converts String<->JSON payloads
    return f;
  }
}

@Service
class HeaderedSender {
  private final KafkaTemplate<String, Object> template;
  HeaderedSender(KafkaTemplate<String, Object> template) { this.template = template; }

  void send(Object payload, String topic, String key) {
    var msg = MessageBuilder.withPayload(payload)
        .setHeader(KafkaHeaders.TOPIC, topic)
        .setHeader(KafkaHeaders.MESSAGE_KEY, key)
        .setHeader("schemaVersion", "v3") // track schema evolution
        .build();
    template.send(msg);
  }
}
```

## 1.9 Events and lifecycle

### 1.9.1 ListenerContainerIdleEvent, ConsumerPausedEvent, ConsumerResumedEvent, ConsumerStartedEvent, ConsumerStoppedEvent, NonResponsiveConsumerEvent, ContainerStoppedEvent

- Description: The container emits Spring application events covering liveness and lifecycle. These events are ideal for metrics, alerts, and operational dashboards.
- Guidance: Use idle events to implement heartbeats; act on pause/resume for backpressure observability; alert on non-responsive consumers.

```java
@Component
class ListenerEventsObserver {

  @EventListener
  void onIdle(ListenerContainerIdleEvent e) {
    // heartbeat metric: container has been idle for configured interval
  }

  @EventListener
  void onPaused(ConsumerPausedEvent e) {
    // record backpressure condition; consider scaling downstream
  }

  @EventListener
  void onResumed(ConsumerResumedEvent e) {
    // clear backpressure flag
  }

  @EventListener
  void onStarted(ConsumerStartedEvent e) { /* lifecycle hook */ }

  @EventListener
  void onStopped(ConsumerStoppedEvent e) { /* lifecycle hook */ }

  @EventListener
  void onNonResponsive(NonResponsiveConsumerEvent e) {
    // alert: consumer not processing for too long; investigate GC/network
  }
}
```

## 1.10 Interceptors and observability

### 1.10.1 ProducerInterceptor, ConsumerInterceptor, MicrometerProducerListener, MicrometerConsumerListener

- Description:
  - Kafka client interceptors run in-producer or in-consumer for pre/post hooks; keep them lightweight to avoid blocking IO threads.
  - Micrometer listeners provide turnkey metrics integration without altering business code.
- Guidance: Prefer listener-based metrics in Spring where possible; use interceptors for cross-cutting enrichment like trace IDs.

```java
@Configuration
class ObservabilityConfig {

  @Bean
  ProducerFactory<String, String> producerFactoryWithMetrics() {
    var pf = new DefaultKafkaProducerFactory<String, String>(new HashMap<>());
    pf.addListener(new MicrometerProducerListener<>()); // emits producer metrics
    return pf;
  }

  @Bean
  ConsumerFactory<String, String> consumerFactoryWithMetrics() {
    var cf = new DefaultKafkaConsumerFactory<String, String>(new HashMap<>());
    cf.addListener(new MicrometerConsumerListener<>()); // emits consumer metrics
    return cf;
  }
}
```

## 1.11 Kafka Streams integration

### 1.11.1 EnableKafkaStreams, KafkaStreamsConfiguration, KafkaStreamsDefaultConfiguration, StreamsBuilderFactoryBean, KStream, KTable, GlobalKTable

- Description: Spring manages Kafka Streams lifecycle and configuration via beans, while the DSL types (<code>KStream</code>, <code>KTable</code>) define the topology. Choose processing guarantees based on requirements; EXACTLY_ONCE_V2 adds overhead—enable only when necessary.
- Guidance: Keep topologies small, focused, and observable; size and monitor state stores.

```java
@Configuration
@EnableKafkaStreams
class StreamsTopology {

  @Bean(name = KafkaStreamsDefaultConfiguration.DEFAULT_STREAMS_CONFIG_BEAN_NAME)
  KafkaStreamsConfiguration streamsConfig() {
    var props = new HashMap<String, Object>();
    props.put(org.apache.kafka.streams.StreamsConfig.APPLICATION_ID_CONFIG, "streams-app");
    props.put(org.apache.kafka.streams.StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
    // Add PROCESSING_GUARANTEE if EOS is required
    // props.put(org.apache.kafka.streams.StreamsConfig.PROCESSING_GUARANTEE_CONFIG, "exactly_once_v2");
    return new KafkaStreamsConfiguration(props);
  }

  @Bean
  org.apache.kafka.streams.kstream.KStream<String, String> pipeline(org.apache.kafka.streams.StreamsBuilder b) {
    var in = b.stream("orders");
    // Branch and route; keep logic simple for operational clarity
    var branches = in.branch(
        (k, v) -> v != null && v.startsWith("A"),
        (k, v) -> true
    );
    branches[0].mapValues(v -> "A|" + v).to("orders-A");
    branches[1].mapValues(v -> "X|" + v).to("orders-X");
    return in;
  }
}
```

## 1.12 Testing

### 1.12.1 EmbeddedKafka, EmbeddedKafkaBroker, KafkaTestUtils, OutputDestination

- Description: Spin up an in-memory Kafka for integration tests. Produce test inputs, start listeners or Streams topologies, then consume from output topics to assert behavior. Keeps tests hermetic and reproducible.
- Guidance: Use time-bounded polls; clean up resources via test framework lifecycle.

```java
@org.springframework.kafka.test.context.EmbeddedKafka(partitions = 1, topics = { "in", "out" })
@org.springframework.boot.test.context.SpringBootTest
class KafkaIT {

  @Autowired
  KafkaTemplate<String, String> template;

  @Autowired
  org.apache.kafka.clients.consumer.Consumer<String, String> testConsumer;

  @Test
  void endToEnd() {
    // Arrange
    template.send("in", "k1", "v1");

    // Act: listener or streams topology processes messages

    // Assert: consume output and validate
    var records = testConsumer.poll(java.time.Duration.ofSeconds(5));
    // assertions on records contents and count
  }
}

@Component
class TransformListener {
  private final KafkaTemplate<String, String> template;
  TransformListener(KafkaTemplate<String, String> template) { this.template = template; }

  @KafkaListener(topics = "in", groupId = "it")
  void on(String v) { template.send("out", "T|" + v); }
}
```

## 1.13 Serialization, conversion, and record types

### 1.13.1 StringSerializer, StringDeserializer, ByteArraySerializer, ByteArrayDeserializer, JsonSerde, RecordHeaders, ConsumerRecord, ProducerRecord

- Description: Core serializers/deserializers define wire formats; choose String for simple text, JSON for structured events, and byte[] for opaque payloads. <code>RecordHeaders</code> carry metadata; raw <code>ConsumerRecord</code>/<code>ProducerRecord</code> give full control when needed.
- Guidance: Standardize serdes across services to avoid schema drift; use headers for correlation and schema versioning.

```java
@Configuration
class SerdeConfig {

  @Bean
  ProducerFactory<String, byte[]> bytePf() {
    var props = new HashMap<String, Object>();
    props.put(org.apache.kafka.clients.producer.ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, org.apache.kafka.common.serialization.StringSerializer.class);
    props.put(org.apache.kafka.clients.producer.ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, org.apache.kafka.common.serialization.ByteArraySerializer.class);
    return new DefaultKafkaProducerFactory<>(props);
  }

  @Bean
  ConsumerFactory<String, byte[]> byteCf() {
    var props = new HashMap<String, Object>();
    props.put(org.apache.kafka.clients.consumer.ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, org.apache.kafka.common.serialization.StringDeserializer.class);
    props.put(org.apache.kafka.clients.consumer.ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, org.apache.kafka.common.serialization.ByteArrayDeserializer.class);
    return new DefaultKafkaConsumerFactory<>(props);
  }
}
```

## 1.14 Utility and support

### 1.14.1 ContainerProperties.AckMode, RecordInterceptor, AfterRollbackProcessor, SeekingStatus, DeliveryAttemptHeader, RetryListener

- Description:
  - <code>AckMode</code> controls commit granularity: RECORD, BATCH, MANUAL, MANUAL_IMMEDIATE.
  - <code>RecordInterceptor</code> inspects/modifies a record before listener invocation (e.g., short-circuit filtering, metrics).
  - <code>AfterRollbackProcessor</code> performs actions for records after a TX rollback (e.g., logging, parking).
  - <code>DeliveryAttemptHeader</code> exposes retry attempt count in headers; <code>RetryListener</code> provides callbacks during retry cycles.
- Guidance: Use interceptor for low-overhead cross-cutting logic; keep it fast to avoid impacting IO threads.

```java
@Configuration
class AdvancedHooks {

  @Bean
  ConcurrentKafkaListenerContainerFactory<String, String> factoryWithHooks(ConsumerFactory<String, String> cf) {
    var f = new ConcurrentKafkaListenerContainerFactory<String, String>();
    f.setConsumerFactory(cf);

    // Intercept records pre-listener; can return null to skip delivery
    f.setRecordInterceptor(rec -> {
      // example: drop “TEST|” messages cheaply before business logic
      if (rec.value() != null && rec.value().startsWith("TEST|")) return null;
      return rec;
    });

    // Handle records after rollback (e.g., custom parking or alerting)
    f.setAfterRollbackProcessor((record, ex, consumer, container) -> {
      // log and tag metrics with ex.getClass().getSimpleName()
    });

    return f;
  }
}
```

# 2. Minimal End-to-End Blueprint (Descriptive, Commented)

```java
@Configuration
class AppWiring {

  // Producer side with metrics listener
  @Bean
  ProducerFactory<String, String> pf() {
    var pf = new DefaultKafkaProducerFactory<String, String>(new HashMap<>());
    pf.addListener(new MicrometerProducerListener<>()); // metrics without touching business code
    return pf;
  }

  @Bean
  KafkaTemplate<String, String> kt(ProducerFactory<String, String> pf) {
    var t = new KafkaTemplate<>(pf);
    t.setDefaultTopic("events"); // fallback destination
    return t;
  }

  // Consumer side
  @Bean
  ConsumerFactory<String, String> cf() { return new DefaultKafkaConsumerFactory<>(new HashMap<>()); }

  // Unified error handling: 3 retries then publish to <topic>.DLT
  @Bean
  DefaultErrorHandler errorHandler(KafkaTemplate<Object, Object> t) {
    return new DefaultErrorHandler(new DeadLetterPublishingRecoverer(t), new FixedBackOff(500L, 3L));
  }

  @Bean
  ConcurrentKafkaListenerContainerFactory<String, String> factory(ConsumerFactory<String, String> cf, DefaultErrorHandler eh) {
    var f = new ConcurrentKafkaListenerContainerFactory<String, String>();
    f.setConsumerFactory(cf);
    f.setCommonErrorHandler(eh);
    f.getContainerProperties().setAckMode(ContainerProperties.AckMode.RECORD); // one-by-one commits
    return f;
  }

  // Topics with explicit SLAs
  @Bean NewTopic main() { return TopicBuilder.name("orders").partitions(6).replicas(3).config("min.insync.replicas","2").build(); }
  @Bean NewTopic dlt()  { return TopicBuilder.name("orders.DLT").partitions(6).replicas(3).config("retention.ms","1209600000").build(); }
}

@Service
class Pipeline {
  private final KafkaTemplate<String, String> template;
  Pipeline(KafkaTemplate<String, String> template) { this.template = template; }

  // Main processor: transform and forward; failures go through DefaultErrorHandler -> DLT
  @KafkaListener(topics = "orders", groupId = "orders-app", containerFactory = "factory")
  void on(String v) {
    if (v.contains("fail")) throw new RuntimeException("transient"); // triggers retry/DLT
    template.send("events", "ok|" + v); // forward result
  }

  // Observe dead letters for remediation
  @KafkaListener(topics = "orders.DLT", groupId = "orders-dlt")
  void onDlt(String v) {
    // alert, store, or schedule replay with fix
  }
}
```

If a deeper dive is needed for any specific class (e.g., all important methods on <code>KafkaTemplate</code> or advanced <code>DefaultErrorHandler</code> tuning), specify the target and an expanded section with additional commented examples will be added.
