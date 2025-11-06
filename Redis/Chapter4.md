# Chapter 4: Spring Data Redis Integration

## 4.1 Spring Data Redis Dependencies and Setup

### Adding Maven Dependencies

**Basic Spring Data Redis Starter**

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

This single dependency includes:

- Spring Data Redis core library
- Lettuce client (default Redis client since Spring Boot 1.4)
- Jedis client (optional, can be excluded)

**With Explicit Jedis Client**

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>

<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
</dependency>
```

### Basic Configuration

**application.properties**

```properties
spring.redis.host=localhost
spring.redis.port=6379
spring.redis.password=
spring.redis.database=0
spring.redis.timeout=2000ms
spring.redis.jedis.pool.max-active=8
spring.redis.jedis.pool.max-idle=8
spring.redis.jedis.pool.min-idle=0
spring.redis.jedis.pool.max-wait=-1ms
```

**application.yml**

```yaml
spring:
  redis:
    host: localhost
    port: 6379
    password:
    database: 0
    timeout: 2000ms
    jedis:
      pool:
        max-active: 8
        max-idle: 8
        min-idle: 0
        max-wait: -1ms
```

### Auto-Configuration

Spring Boot auto-configures:

- **RedisConnectionFactory**: Manages Redis connections
- **RedisTemplate**: Provides template for operations
- **StringRedisTemplate**: String-focused template

These beans are available automatically once starter dependency is added.

## 4.2 RedisTemplate and StringRedisTemplate Operations

### RedisTemplate Overview

**RedisTemplate** is the central class providing high-level access to Redis operations. It handles connection management, serialization/deserialization, and command execution.

**Type Parameters**

```java
RedisTemplate<K, V>
```

- K: Key type (usually String)
- V: Value type (can be any Object)

### Basic RedisTemplate Configuration

```java
@Configuration
public class RedisConfig {

    @Bean
    public RedisTemplate<String, Object> redisTemplate(
            RedisConnectionFactory connectionFactory) {

        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(connectionFactory);

        // Key serializer
        StringRedisSerializer stringSerializer = new StringRedisSerializer();
        template.setKeySerializer(stringSerializer);
        template.setHashKeySerializer(stringSerializer);

        // Value serializer
        GenericToStringSerializer<Object> valueSerializer =
            new GenericToStringSerializer<>(Object.class);
        template.setValueSerializer(valueSerializer);
        template.setHashValueSerializer(valueSerializer);

        template.afterPropertiesSet();
        return template;
    }
}
```

### ValueOperations (String Commands)

```java
@Autowired
private RedisTemplate<String, String> redisTemplate;

// Get value operations
ValueOperations<String, String> ops = redisTemplate.opsForValue();

// SET
ops.set("key1", "value1");
ops.set("key2", "value2", 300, TimeUnit.SECONDS);  // With expiration

// GET
String value = ops.get("key1");

// SET if absent
Boolean set = ops.setIfAbsent("key3", "value3");

// INCR
Long counter = ops.increment("counter");
Long incrementBy = ops.increment("counter", 5);

// APPEND
Integer length = ops.append("key", "append_text");

// GET and SET
String oldValue = ops.getAndSet("key1", "newvalue");

// MGET / MSET
ops.multiSet(Map.of("k1", "v1", "k2", "v2"));
List<String> values = ops.multiGet(Arrays.asList("k1", "k2", "k3"));
```

### HashOperations (Hash Commands)

```java
// Get hash operations
HashOperations<String, String, String> hashOps =
    redisTemplate.opsForHash();

// HSET - Set field in hash
hashOps.put("user:1", "name", "Alice");
hashOps.put("user:1", "email", "alice@example.com");

// HGET - Get field value
String name = hashOps.get("user:1", "name");

// HGETALL - Get all fields
Map<String, String> user = hashOps.entries("user:1");

// HEXISTS - Check if field exists
Boolean exists = hashOps.hasKey("user:1", "name");

// HDEL - Delete field
Long deleted = hashOps.delete("user:1", "email");

// HLEN - Count fields
Long size = hashOps.size("user:1");

// HINCRBYFLOAT - Increment float field
Double score = hashOps.increment("user:1", "score", 2.5);

// HSCAN - Iterate over hash
Cursor<Map.Entry<String, String>> cursor =
    hashOps.scan("user:1", ScanOptions.scanOptions().match("*").build());
```

### ListOperations (List Commands)

```java
// Get list operations
ListOperations<String, String> listOps = redisTemplate.opsForList();

// LPUSH - Push to left
Long size = listOps.leftPush("tasks", "task1");
Long sizeMultiple = listOps.leftPushAll("tasks", "task2", "task3");

// RPUSH - Push to right
listOps.rightPush("tasks", "task4");

// LPOP - Pop from left
String task = listOps.leftPop("tasks");

// LRANGE - Get range
List<String> tasks = listOps.range("tasks", 0, -1);

// LLEN - Get length
Long length = listOps.size("tasks");

// LINDEX - Get by index
String task = listOps.index("tasks", 0);

// LTRIM - Trim list
listOps.trim("tasks", 0, 9);
```

### SetOperations (Set Commands)

```java
// Get set operations
SetOperations<String, String> setOps = redisTemplate.opsForSet();

// SADD - Add members
Long added = setOps.add("tags:article1", "redis", "cache", "database");

// SMEMBERS - Get all members
Set<String> tags = setOps.members("tags:article1");

// SISMEMBER - Check membership
Boolean isMember = setOps.isMember("tags:article1", "redis");

// SCARD - Get size
Long size = setOps.size("tags:article1");

// SREM - Remove member
Long removed = setOps.remove("tags:article1", "cache");

// SINTER - Intersection
Set<String> intersection = setOps.intersect("tags:article1", "tags:article2");

// SUNION - Union
Set<String> union = setOps.union("tags:article1", "tags:article2");

// SDIFF - Difference
Set<String> difference = setOps.difference("tags:article1", "tags:article2");
```

### ZSetOperations (Sorted Set Commands)

```java
// Get sorted set operations
ZSetOperations<String, String> zsetOps = redisTemplate.opsForZSet();

// ZADD - Add members with score
Long added = zsetOps.add("leaderboard", "player1", 100);
zsetOps.add("leaderboard", Map.of("player2", 200.0, "player3", 150.0));

// ZRANGE - Get by rank
Set<String> top3 = zsetOps.range("leaderboard", 0, 2);

// ZREVRANGE - Get by rank (reverse)
Set<String> top3Reverse = zsetOps.reverseRange("leaderboard", 0, 2);

// ZRANK - Get rank of member
Long rank = zsetOps.rank("leaderboard", "player1");

// ZSCORE - Get score
Double score = zsetOps.score("leaderboard", "player1");

// ZREM - Remove member
Long removed = zsetOps.remove("leaderboard", "player1");

// ZCARD - Get size
Long size = zsetOps.size("leaderboard");

// ZINCRBY - Increment score
Double newScore = zsetOps.incrementScore("leaderboard", "player1", 50);
```

### StringRedisTemplate

**StringRedisTemplate** is optimized for String keys and values, avoiding serialization overhead.

```java
@Autowired
private StringRedisTemplate stringRedisTemplate;

@Service
public class UserService {

    // Uses ValueOperations<String, String> internally
    public void cacheUser(String userId, String userData) {
        stringRedisTemplate.opsForValue().set(
            "user:" + userId,
            userData,
            1,
            TimeUnit.HOURS
        );
    }

    public String getUser(String userId) {
        return stringRedisTemplate.opsForValue()
            .get("user:" + userId);
    }
}
```

**Why StringRedisTemplate?**

- No serialization overhead for strings
- More efficient for string-heavy operations
- Faster performance than generic RedisTemplate
- Cleaner API for string operations

## 4.3 Redis Repositories with CrudRepository

### CrudRepository Pattern

Spring Data Redis allows using repository pattern similar to JPA, eliminating direct template usage for common operations.

### Entity Definition with @RedisHash

```java
@RedisHash("user")
public class User {

    @Id
    private String id;

    @Indexed
    private String email;

    private String name;
    private String phoneNumber;

    // Getters and setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}
```

**@RedisHash**: Marks class for Redis persistence, specifies key prefix

**@Id**: Identifies primary key field

**@Indexed**: Creates secondary index for querying

### Creating Repository

```java
@Repository
public interface UserRepository extends CrudRepository<User, String> {

    // Finder methods using indexed fields
    Optional<User> findByEmail(String email);
    List<User> findByName(String name);
}
```

### Using Repository

```java
@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    // Create
    public User createUser(User user) {
        user.setId(UUID.randomUUID().toString());
        return userRepository.save(user);
    }

    // Read
    public Optional<User> getUser(String id) {
        return userRepository.findById(id);
    }

    // Find by indexed field
    public Optional<User> getUserByEmail(String email) {
        return userRepository.findByEmail(email);
    }

    // Update
    public User updateUser(User user) {
        return userRepository.save(user);
    }

    // Delete
    public void deleteUser(String id) {
        userRepository.deleteById(id);
    }

    // Get all
    public List<User> getAllUsers() {
        return (List<User>) userRepository.findAll();
    }
}
```

### Repository Key Storage

Keys stored with format: `keyPrefix:id`

```
user:550e8400-e29b-41d4-a716-446655440000
user:550e8400-e29b-41d4-a716-446655440001
```

Redis stores hash for each entity:

```
HGETALL user:550e8400-e29b-41d4-a716-446655440000
# Returns: {id, email, name, phoneNumber, ...}
```

## 4.4 @RedisHash Annotation for Entity Mapping

### @RedisHash Configuration

```java
@RedisHash(value = "user", timeToLive = 3600)
public class User {

    @Id
    private String id;

    private String name;
    private String email;
}
```

**value**: Redis key prefix

**timeToLive**: Automatic expiration in seconds (optional)

### Field Annotations

**@Id**: Primary key, required for repository pattern

```java
@RedisHash("user")
public class User {
    @Id
    private String userId;  // Automatically used as key
}
```

**@Indexed**: Creates secondary index for finder methods

```java
@RedisHash("user")
public class User {
    @Id
    private String id;

    @Indexed
    private String email;      // Can use findByEmail()

    @Indexed
    private String phoneNumber; // Can use findByPhoneNumber()

    private String name;        // Cannot directly query
}
```

### Nested Objects

```java
@RedisHash("user")
public class User {
    @Id
    private String id;

    private String name;
    private Address address;  // Nested object serialized as part of hash
}

public class Address {
    private String street;
    private String city;
    private String zipCode;
}
```

Entire Address object stored in Redis hash with flattened keys.

### Time-To-Live (TTL)

**Global TTL**

```java
@RedisHash(value = "session", timeToLive = 1800)  // 30 minutes
public class UserSession {
    @Id
    private String sessionId;
    private String userId;
}
```

Keys automatically expire after specified time.

**Querying with TTL**

```java
public Optional<UserSession> findSession(String sessionId) {
    return sessionRepository.findById(sessionId);
    // Returns empty if expired
}
```

## 4.5 Redis Connection Factory Configuration

### Connection Factory Types

**LettuceConnectionFactory** (Default)

```java
@Bean
public LettuceConnectionFactory lettuceConnectionFactory() {
    return new LettuceConnectionFactory();
}
```

Non-blocking, async-capable, recommended for most applications.

**JedisConnectionFactory**

```java
@Bean
public JedisConnectionFactory jedisConnectionFactory() {
    return new JedisConnectionFactory();
}
```

Simpler, synchronous, easier to use.

### Advanced Configuration

**Redis Standalone**

```java
@Configuration
public class RedisConfig {

    @Bean
    public LettuceConnectionFactory connectionFactory() {
        RedisStandaloneConfiguration config =
            new RedisStandaloneConfiguration("localhost", 6379);
        config.setPassword("password");
        config.setDatabase(0);

        return new LettuceConnectionFactory(config);
    }
}
```

**Redis Sentinel**

```java
@Bean
public LettuceConnectionFactory sentinelConnectionFactory() {
    RedisSentinelConfiguration sentinelConfig =
        new RedisSentinelConfiguration()
            .master("mymaster")
            .sentinel("127.0.0.1", 26379)
            .sentinel("127.0.0.1", 26380);

    return new LettuceConnectionFactory(sentinelConfig);
}
```

**Redis Cluster**

```java
@Bean
public LettuceConnectionFactory clusterConnectionFactory() {
    RedisClusterConfiguration clusterConfig =
        new RedisClusterConfiguration()
            .clusterNode("127.0.0.1", 6379)
            .clusterNode("127.0.0.1", 6380)
            .clusterNode("127.0.0.1", 6381);

    return new LettuceConnectionFactory(clusterConfig);
}
```

**Connection Pooling (Jedis)**

```java
@Bean
public JedisConnectionFactory jedisConnectionFactory() {
    JedisPoolConfig poolConfig = new JedisPoolConfig();
    poolConfig.setMaxTotal(8);
    poolConfig.setMaxIdle(8);
    poolConfig.setMinIdle(0);
    poolConfig.setTestOnBorrow(true);
    poolConfig.setTestOnReturn(true);
    poolConfig.setTestWhileIdle(true);

    JedisConnectionFactory connectionFactory =
        new JedisConnectionFactory(poolConfig);

    return connectionFactory;
}
```

### SSL/TLS Configuration

```java
@Bean
public LettuceConnectionFactory lettuceConnectionFactory() {
    LettuceConnectionFactory connectionFactory =
        new LettuceConnectionFactory();

    connectionFactory.setUseSsl(true);
    connectionFactory.setVerifyPeer(false);

    return connectionFactory;
}
```

## 4.6 Jedis vs Lettuce Clients Comparison

| Feature                    | Jedis                      | Lettuce                         |
| -------------------------- | -------------------------- | ------------------------------- |
| **Architecture**           | Synchronous, blocking      | Non-blocking, async/reactive    |
| **Threading**              | Thread-per-connection pool | Single connection reusable      |
| **Async Support**          | No                         | Full async and reactive support |
| **Cluster Support**        | Synchronous only           | Sync, async, and reactive       |
| **Sentinel Support**       | Limited                    | Full support                    |
| **Memory Usage**           | Higher (connection pool)   | Lower (single connection)       |
| **Performance**            | Good with connection pool  | Better with single connection   |
| **Complexity**             | Simple                     | More complex                    |
| **Ease of Use**            | Easier to learn            | Steeper learning curve          |
| **Default in Spring Boot** | Not default                | Default since 1.4               |

### Performance Characteristics

**Jedis**

- Throughput increases with connection pool size
- Plateaus once thread count exceeds pool size
- Better for simple synchronous applications

**Lettuce**

- Single connection scales with thread count
- Linear performance scaling
- Better for high-concurrency applications

### When to Use Each

**Choose Jedis If**

- Building simple applications with basic needs
- Don't need async/reactive features
- Synchronous code is sufficient
- Prefer simpler implementation

**Choose Lettuce If**

- Building reactive Spring applications
- Need async capabilities
- Requires high throughput with many threads
- Want single connection benefits
- Building microservices

## 4.7 Connection Pooling and Configuration

### Jedis Connection Pool

**Default Pool Configuration**

```
max-active: 8        # Maximum connections
max-idle: 8          # Maximum idle connections
min-idle: 0          # Minimum idle connections
max-wait: -1ms       # Wait indefinitely
```

**Custom Configuration**

```yaml
spring:
  redis:
    jedis:
      pool:
        max-active: 50
        max-idle: 25
        min-idle: 5
        max-wait: 2000ms
```

```java
@Configuration
public class RedisConfig {

    @Bean
    public JedisConnectionFactory jedisConnectionFactory(
            @Value("${spring.redis.jedis.pool.max-active}") int maxActive,
            @Value("${spring.redis.jedis.pool.max-idle}") int maxIdle,
            @Value("${spring.redis.jedis.pool.min-idle}") int minIdle) {

        JedisPoolConfig poolConfig = new JedisPoolConfig();
        poolConfig.setMaxTotal(maxActive);
        poolConfig.setMaxIdle(maxIdle);
        poolConfig.setMinIdle(minIdle);
        poolConfig.setTestOnBorrow(true);      // Test on borrow
        poolConfig.setTestOnReturn(true);      // Test on return
        poolConfig.setTestWhileIdle(true);     // Test idle
        poolConfig.setMinEvictableIdleTimeMillis(60000);
        poolConfig.setTimeBetweenEvictionRunsMillis(30000);
        poolConfig.setNumTestsPerEvictionRun(3);
        poolConfig.setBlockWhenExhausted(true);

        return new JedisConnectionFactory(poolConfig);
    }
}
```

### Lettuce Connection Pool

Lettuce uses connection pooling at a different level (optional).

```java
@Configuration
public class RedisConfig {

    @Bean
    public LettuceConnectionFactory lettuceConnectionFactory() {
        LettuceClientConfiguration clientConfig =
            LettuceClientConfiguration.builder()
                .shutdownTimeout(Duration.ofSeconds(2))
                .build();

        return new LettuceConnectionFactory(clientConfig);
    }
}
```

### Pool Sizing Guidelines

**Calculate Pool Size**

```
Pool Size = (connections per thread) * (max application threads)
```

**Typical Values**

- Small app (< 50 concurrent users): 8-10
- Medium app (50-500 concurrent users): 20-30
- Large app (500+ concurrent users): 50-100

**Monitor Pool Usage**

```java
public void logPoolStats(JedisConnectionFactory factory) {
    JedisPool pool = factory.getJedisPool();
    BorrowedConnectionMetrics metrics =
        pool.getResource().getConnectionInfo();

    log.info("Active: {}, Idle: {}",
        metrics.getActive(),
        metrics.getIdle());
}
```

## 4.8 RedisMessageListenerContainer for Pub/Sub

### Configuration

```java
@Configuration
public class PubSubConfig {

    @Bean
    public RedisMessageListenerContainer container(
            RedisConnectionFactory connectionFactory,
            MessageListenerAdapter adapter) {

        RedisMessageListenerContainer container =
            new RedisMessageListenerContainer();

        container.setConnectionFactory(connectionFactory);
        container.addMessageListener(adapter, new ChannelTopic("orders"));
        container.addMessageListener(adapter, new PatternTopic("notifications:*"));

        return container;
    }
}
```

### Message Listener Adapter

```java
@Component
public class RedisMessageHandler {

    @Autowired
    private OrderService orderService;

    public void handleMessage(String message) {
        log.info("Received message: {}", message);
        OrderEvent event = parseEvent(message);
        orderService.processEvent(event);
    }

    private OrderEvent parseEvent(String message) {
        // Parse message from JSON
        return new ObjectMapper().readValue(message, OrderEvent.class);
    }
}

@Bean
public MessageListenerAdapter messageListenerAdapter(
        RedisMessageHandler handler) {

    return new MessageListenerAdapter(handler, "handleMessage");
}
```

### Channel Topics

**Direct Channel Subscription**

```java
@Bean
public ChannelTopic orderTopic() {
    return new ChannelTopic("orders");
}
```

**Pattern Topic Subscription**

```java
@Bean
public PatternTopic notificationPattern() {
    return new PatternTopic("notifications:*");
}
```

## 4.9 Message Listeners and Handlers

### Basic Message Listener

```java
@Component
public class CustomMessageListener implements MessageListener {

    @Override
    public void onMessage(Message message, byte[] pattern) {
        String channel = new String(message.getChannel());
        String body = new String(message.getBody());

        log.info("Channel: {}, Message: {}", channel, body);
    }
}
```

### Using SubscriptionListener

```java
public class SmartMessageListener
        implements MessageListener, SubscriptionListener {

    @Override
    public void onMessage(Message message, byte[] pattern) {
        // Message handling
    }

    @Override
    public void onChannelSubscribed(byte[] channel, long count) {
        log.info("Subscribed to channel: {}", new String(channel));
    }

    @Override
    public void onChannelUnsubscribed(byte[] channel, long count) {
        log.info("Unsubscribed from channel: {}", new String(channel));
    }
}
```

## 4.10 Redis Transactions in Spring

### Using @Transactional

```java
@Service
public class TransactionService {

    @Autowired
    private RedisTemplate<String, String> redisTemplate;

    @Transactional
    public void transferFunds(String from, String to, int amount) {
        redisTemplate.multi();

        redisTemplate.opsForValue()
            .decrement(from, amount);

        redisTemplate.opsForValue()
            .increment(to, amount);

        redisTemplate.exec();
    }
}
```

### Using SessionCallback

```java
public void executeTransaction() {
    redisTemplate.execute(new SessionCallback<Void>() {
        @Override
        public Void execute(RedisOperations ops) throws DataAccessException {
            ops.multi();

            ops.opsForValue().set("key1", "value1");
            ops.opsForValue().set("key2", "value2");

            ops.exec();
            return null;
        }
    });
}
```

## 4.11 Spring Data Redis Serialization (Jackson, Kryo, JdkSerialization)

### Default Serialization

By default, RedisTemplate uses **JdkSerializationRedisSerializer**:

```java
JdkSerializationRedisSerializer serializer =
    new JdkSerializationRedisSerializer();
```

Downsides: Binary format, not human-readable, performance overhead.

### Jackson JSON Serialization

```java
@Configuration
public class RedisConfig {

    @Bean
    public RedisTemplate<String, Object> redisTemplate(
            RedisConnectionFactory connectionFactory) {

        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(connectionFactory);

        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        objectMapper.registerModule(new JavaTimeModule());

        GenericJackson2JsonRedisSerializer jackson2JsonRedisSerializer =
            new GenericJackson2JsonRedisSerializer(objectMapper);

        StringRedisSerializer stringRedisSerializer =
            new StringRedisSerializer();

        // Keys as strings, values as JSON
        template.setKeySerializer(stringRedisSerializer);
        template.setHashKeySerializer(stringRedisSerializer);

        template.setValueSerializer(jackson2JsonRedisSerializer);
        template.setHashValueSerializer(jackson2JsonRedisSerializer);

        template.afterPropertiesSet();
        return template;
    }
}
```

**Advantages**: Human-readable, debuggable, interoperable

**Disadvantages**: Larger size, serialization overhead

### Kryo Serialization

```java
<!-- Add dependency -->
<dependency>
    <groupId>com.esotericsoftware</groupId>
    <artifactId>kryo</artifactId>
    <version>5.4.1</version>
</dependency>

// Configuration not directly in Spring, use Redisson wrapper
@Bean
public Redisson redisson() {
    Config config = new Config();
    config.useSingleServer()
        .setAddress("redis://localhost:6379")
        .setCodec(new KryoCodec());  // Use Kryo codec

    return Redisson.create(config);
}
```

**Advantages**: Compact binary format, fastest serialization

**Disadvantages**: Binary, less debuggable, requires specific library

### Custom Serializer

```java
public class CustomJsonSerializer<T>
        implements RedisSerializer<T> {

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final Class<T> type;

    public CustomJsonSerializer(Class<T> type) {
        this.type = type;
    }

    @Override
    public byte[] serialize(T t) throws SerializationException {
        try {
            return objectMapper.writeValueAsBytes(t);
        } catch (JsonProcessingException e) {
            throw new SerializationException("Failed to serialize", e);
        }
    }

    @Override
    public T deserialize(byte[] bytes) throws SerializationException {
        try {
            return objectMapper.readValue(bytes, type);
        } catch (IOException e) {
            throw new SerializationException("Failed to deserialize", e);
        }
    }
}

// Usage
GenericJackson2JsonRedisSerializer serializer =
    new GenericJackson2JsonRedisSerializer(new ObjectMapper());
```

## 4.12 Custom Serialization Strategies

### Type-Specific Serialization

```java
@Configuration
public class MultiSerializerRedisConfig {

    @Bean
    public RedisTemplate<String, Object> redisTemplate(
            RedisConnectionFactory connectionFactory) {

        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(connectionFactory);

        StringRedisSerializer stringSerializer =
            new StringRedisSerializer();

        // Strings as plain text
        StringRedisSerializer stringValue = new StringRedisSerializer();

        // Complex objects as JSON
        GenericJackson2JsonRedisSerializer jsonSerializer =
            new GenericJackson2JsonRedisSerializer();

        template.setKeySerializer(stringSerializer);
        template.setHashKeySerializer(stringSerializer);

        // Default to JSON for values
        template.setDefaultSerializer(jsonSerializer);
        template.setValueSerializer(jsonSerializer);
        template.setHashValueSerializer(jsonSerializer);

        template.afterPropertiesSet();
        return template;
    }
}
```

### Conditional Serialization by Key Pattern

```java
public class PatternBasedSerializer implements RedisSerializer<Object> {

    private final StringRedisSerializer stringSerializer =
        new StringRedisSerializer();
    private final GenericJackson2JsonRedisSerializer jsonSerializer =
        new GenericJackson2JsonRedisSerializer();

    @Override
    public byte[] serialize(Object obj) throws SerializationException {
        // Use JSON by default
        return jsonSerializer.serialize(obj);
    }

    @Override
    public Object deserialize(byte[] bytes) throws SerializationException {
        // Try JSON first, fallback to string
        try {
            return jsonSerializer.deserialize(bytes);
        } catch (Exception e) {
            return stringSerializer.deserialize(bytes);
        }
    }
}
```

### Compression with Serialization

```java
public class CompressedRedisSerializer implements RedisSerializer<Object> {

    private final GenericJackson2JsonRedisSerializer jsonSerializer =
        new GenericJackson2JsonRedisSerializer();

    @Override
    public byte[] serialize(Object obj) throws SerializationException {
        byte[] serialized = jsonSerializer.serialize(obj);
        return compress(serialized);
    }

    @Override
    public Object deserialize(byte[] bytes) throws SerializationException {
        byte[] decompressed = decompress(bytes);
        return jsonSerializer.deserialize(decompressed);
    }

    private byte[] compress(byte[] data) {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        try (GZIPOutputStream gzipOut = new GZIPOutputStream(baos)) {
            gzipOut.write(data);
        } catch (IOException e) {
            throw new RuntimeException("Compression failed", e);
        }
        return baos.toByteArray();
    }

    private byte[] decompress(byte[] data) {
        try (GZIPInputStream gzipIn =
                new GZIPInputStream(new ByteArrayInputStream(data))) {
            return gzipIn.readAllBytes();
        } catch (IOException e) {
            throw new RuntimeException("Decompression failed", e);
        }
    }
}
```
