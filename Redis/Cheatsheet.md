Now I'll compile a comprehensive Redis and Spring Data Redis cheat sheet with code examples covering all important topics.

# Redis & Spring Data Redis - Interview Cheat Sheet

## What is Redis?

Redis (Remote Dictionary Server) is an open-source, in-memory data structure store used as a database, cache, message broker, and streaming engine. It offers sub-millisecond latency, supports various data structures, and provides persistence options.

**Key Features:**

- In-memory storage for ultra-fast performance
- Supports multiple data structures
- Atomic operations
- Pub/Sub messaging
- Persistence (RDB & AOF)
- Replication and high availability
- Clustering for horizontal scaling

---

## Redis Data Structures

### 1. String

The simplest data type storing text, numbers, or serialized objects.

```bash
# Set and Get
SET key "value"
GET key

# Set with expiration (seconds)
SETEX key 60 "value"

# Set if not exists
SETNX key "value"

# Increment/Decrement
INCR counter
INCRBY counter 5
DECR counter
DECRBY counter 3

# Multiple operations
MSET key1 "value1" key2 "value2"
MGET key1 key2

# Append to string
APPEND key " additional_text"

# Get string length
STRLEN key
```

### 2. List

Ordered collection of strings, useful for queues and stacks.

```bash
# Push elements
LPUSH mylist "first"      # Push to head
RPUSH mylist "last"       # Push to tail

# Pop elements
LPOP mylist               # Pop from head
RPOP mylist               # Pop from tail

# Get range
LRANGE mylist 0 -1        # Get all elements
LRANGE mylist 0 5         # Get first 6 elements

# Get by index
LINDEX mylist 0

# Get length
LLEN mylist

# Trim list
LTRIM mylist 0 99         # Keep only first 100 elements

# Insert element
LINSERT mylist BEFORE "existing" "new"

# Blocking operations
BLPOP mylist 10           # Block for 10 seconds
BRPOP mylist 10
```

### 3. Set

Unordered collection of unique strings.

```bash
# Add members
SADD myset "member1" "member2"

# Remove members
SREM myset "member1"

# Get all members
SMEMBERS myset

# Check membership
SISMEMBER myset "member1"

# Get cardinality
SCARD myset

# Set operations
SUNION set1 set2          # Union
SINTER set1 set2          # Intersection
SDIFF set1 set2           # Difference

# Store result
SUNIONSTORE resultset set1 set2

# Random member
SRANDMEMBER myset
SPOP myset                # Remove random member
```

### 4. Sorted Set (ZSet)

Set with score for each member, sorted by score.

```bash
# Add members with scores
ZADD leaderboard 100 "player1" 200 "player2"

# Get by rank (ascending)
ZRANGE leaderboard 0 -1
ZRANGE leaderboard 0 -1 WITHSCORES

# Get by rank (descending)
ZREVRANGE leaderboard 0 -1

# Get by score range
ZRANGEBYSCORE leaderboard 100 200

# Get rank
ZRANK leaderboard "player1"
ZREVRANK leaderboard "player1"

# Get score
ZSCORE leaderboard "player1"

# Increment score
ZINCRBY leaderboard 50 "player1"

# Remove members
ZREM leaderboard "player1"
ZREMRANGEBYSCORE leaderboard 0 100

# Get cardinality
ZCARD leaderboard

# Count by score range
ZCOUNT leaderboard 100 200
```

### 5. Hash

Collection of field-value pairs, ideal for objects.

```bash
# Set fields
HSET user:1001 name "John" age "30"
HMSET user:1001 email "john@email.com" city "NYC"

# Get fields
HGET user:1001 name
HMGET user:1001 name age
HGETALL user:1001

# Check field exists
HEXISTS user:1001 name

# Delete fields
HDEL user:1001 age

# Get all keys or values
HKEYS user:1001
HVALS user:1001

# Get field count
HLEN user:1001

# Increment field value
HINCRBY user:1001 age 1
HINCRBYFLOAT user:1001 balance 10.5

# Set if not exists
HSETNX user:1001 status "active"
```

---

## Redis Key Management

```bash
# Check key existence
EXISTS key

# Delete keys
DEL key1 key2 key3

# Get key type
TYPE key

# Rename key
RENAME oldkey newkey
RENAMENX oldkey newkey    # Rename if new key doesn't exist

# Get random key
RANDOMKEY

# Pattern matching
KEYS pattern              # Find keys matching pattern (avoid in production)
KEYS user:*
KEYS *name*

# Scan keys (production-safe)
SCAN 0 MATCH user:* COUNT 100

# Get all keys (use with caution)
KEYS *
```

---

## Expiration & TTL

```bash
# Set expiration (seconds)
EXPIRE key 60
EXPIREAT key 1640000000   # Unix timestamp

# Set expiration (milliseconds)
PEXPIRE key 60000
PEXPIREAT key 1640000000000

# Get TTL
TTL key                   # Returns -2 if not exists, -1 if no expiry
PTTL key                  # TTL in milliseconds

# Remove expiration
PERSIST key

# Set key with expiration
SETEX key 60 "value"
```

---

## Redis Transactions

Transactions group multiple commands for atomic execution.

```bash
# Start transaction
MULTI

# Queue commands
SET key1 "value1"
INCR counter
LPUSH mylist "item"

# Execute all commands
EXEC

# Discard transaction
DISCARD

# Optimistic locking with WATCH
WATCH key1
MULTI
SET key1 "newvalue"
EXEC                      # Returns nil if key1 changed
```

**Example with WATCH:**

```bash
WATCH balance
val = GET balance
MULTI
SET balance (val - 100)
EXEC                      # Fails if balance changed
```

---

## Redis Pub/Sub

Publish-Subscribe messaging pattern.

```bash
# Subscribe to channels
SUBSCRIBE channel1 channel2

# Subscribe to pattern
PSUBSCRIBE news:*

# Publish message
PUBLISH channel1 "Hello World"

# Unsubscribe
UNSUBSCRIBE channel1
PUNSUBSCRIBE news:*

# Get pub/sub info
PUBSUB CHANNELS           # List active channels
PUBSUB NUMSUB channel1    # Number of subscribers
PUBSUB NUMPAT             # Number of pattern subscriptions
```

---

## Redis Streams

Append-only log data structure for event sourcing.

```bash
# Add entry to stream
XADD mystream * sensor-id 1234 temperature 25.5

# Read from stream
XREAD COUNT 2 STREAMS mystream 0

# Read with blocking
XREAD BLOCK 5000 STREAMS mystream $

# Get stream length
XLEN mystream

# Get range of entries
XRANGE mystream - +
XRANGE mystream 1640000000000 1640100000000

# Delete entries
XDEL mystream 1640000000000-0

# Trim stream
XTRIM mystream MAXLEN 1000

# Consumer Groups
XGROUP CREATE mystream mygroup 0
XREADGROUP GROUP mygroup consumer1 STREAMS mystream >
XACK mystream mygroup 1640000000000-0
```

---

## Redis Geospatial

Store and query location-based data.

```bash
# Add locations
GEOADD locations -122.27652 37.805186 "San Francisco"
GEOADD locations -73.9654 40.7829 "New York"

# Get coordinates
GEOPOS locations "San Francisco"

# Calculate distance
GEODIST locations "San Francisco" "New York" km

# Search by radius (deprecated, use GEOSEARCH)
GEORADIUS locations -122.27652 37.805186 100 km

# Search locations
GEOSEARCH locations FROMLONLAT -122.27652 37.805186 BYRADIUS 100 km

# Get geohash
GEOHASH locations "San Francisco"

# Remove location (use ZREM)
ZREM locations "San Francisco"
```

---

## Redis HyperLogLog

Probabilistic data structure for cardinality estimation.

```bash
# Add elements
PFADD visitors "user1" "user2" "user3"

# Get approximate count
PFCOUNT visitors

# Merge HyperLogLogs
PFMERGE result visitors1 visitors2

# Check multiple keys
PFCOUNT visitors1 visitors2
```

**Use Case:** Count unique visitors with minimal memory (12KB per HyperLogLog).

---

## Redis Bitmaps

Bit-level operations on strings.

```bash
# Set bit
SETBIT mykey 7 1

# Get bit
GETBIT mykey 7

# Count set bits
BITCOUNT mykey

# Bitwise operations
BITOP AND result key1 key2
BITOP OR result key1 key2
BITOP XOR result key1 key2
BITOP NOT result key1

# Find first bit
BITPOS mykey 1            # Find first 1
BITPOS mykey 0            # Find first 0
```

**Use Case:** Track user login status, feature flags.

---

## Redis Pipelining

Send multiple commands without waiting for replies.

```bash
# Redis CLI
redis-cli --pipe

# Commands are sent in batch
SET key1 "value1"
SET key2 "value2"
GET key1
GET key2
```

**Benefits:** Reduces RTT (Round Trip Time), improves throughput.

---

## Redis Lua Scripting

Execute Lua scripts atomically on Redis server.

```bash
# Execute script
EVAL "return redis.call('SET', KEYS[1], ARGV[1])" 1 mykey myvalue

# Load script and get SHA
SCRIPT LOAD "return redis.call('GET', KEYS[1])"

# Execute by SHA
EVALSHA <sha1> 1 mykey

# Check if script exists
SCRIPT EXISTS <sha1>

# Flush all scripts
SCRIPT FLUSH

# Kill running script
SCRIPT KILL
```

**Example - Increment with max limit:**

```lua
local current = redis.call('GET', KEYS[1])
if current and tonumber(current) >= tonumber(ARGV[1]) then
    return 0
end
return redis.call('INCR', KEYS[1])
```

---

## Redis Persistence

### RDB (Redis Database)

Point-in-time snapshots at intervals.

```bash
# Manual snapshot
SAVE                      # Blocking
BGSAVE                    # Background

# Configuration in redis.conf
save 900 1               # Save after 900s if 1 key changed
save 300 10              # Save after 300s if 10 keys changed
save 60 10000            # Save after 60s if 10000 keys changed
```

**Advantages:** Fast restarts, compact, good for backups
**Disadvantages:** Potential data loss between saves

### AOF (Append Only File)

Logs every write operation.

```bash
# Configuration in redis.conf
appendonly yes
appendfsync everysec     # Sync every second (recommended)
appendfsync always       # Sync on every write (slower)
appendfsync no           # OS decides (fastest, risky)

# Manual rewrite
BGREWRITEAOF
```

**Advantages:** Better durability, readable logs
**Disadvantages:** Larger files, slower restarts

---

## Redis Replication

Master-replica model for data redundancy.

```bash
# In replica redis.conf
replicaof <master-ip> <master-port>
replicaof 127.0.0.1 6379

# Check replication status
INFO REPLICATION

# Stop replication
REPLICAOF NO ONE

# Make replica read-only
replica-read-only yes
```

---

## Redis Cluster

Horizontal partitioning with 16384 hash slots.

**Key Concepts:**

- Data automatically sharded across nodes
- Each node handles subset of hash slots
- Master-replica pairs for availability
- Hash tags for multi-key operations: `{user123}:profile`

```bash
# Create cluster
redis-cli --cluster create <node1>:6379 <node2>:6379 --cluster-replicas 1

# Check cluster info
CLUSTER INFO
CLUSTER NODES

# Get key's hash slot
CLUSTER KEYSLOT mykey

# Resharding
redis-cli --cluster reshard <node>:6379
```

---

## Spring Data Redis Configuration

### Maven Dependencies

```xml
<!-- Spring Boot Starter (includes Lettuce) -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>

<!-- For Jedis instead of Lettuce -->
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
</dependency>
```

### application.properties

```properties
# Redis Configuration
spring.redis.host=localhost
spring.redis.port=6379
spring.redis.password=
spring.redis.database=0
spring.redis.timeout=60000

# Connection Pool (Lettuce)
spring.redis.lettuce.pool.max-active=8
spring.redis.lettuce.pool.max-idle=8
spring.redis.lettuce.pool.min-idle=0

# Connection Pool (Jedis)
spring.redis.jedis.pool.max-active=8
spring.redis.jedis.pool.max-idle=8
spring.redis.jedis.pool.min-idle=0

# Cache Configuration
spring.cache.type=redis
spring.cache.redis.time-to-live=600000
spring.cache.redis.cache-null-values=false
```

---

## Spring Data Redis - RedisTemplate

### Basic Configuration

```java
@Configuration
public class RedisConfig {

    @Bean
    public RedisConnectionFactory redisConnectionFactory() {
        RedisStandaloneConfiguration config =
            new RedisStandaloneConfiguration("localhost", 6379);
        return new LettuceConnectionFactory(config);
    }

    @Bean
    public RedisTemplate<String, Object> redisTemplate(
            RedisConnectionFactory connectionFactory) {

        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(connectionFactory);

        // String serializer for keys
        template.setKeySerializer(new StringRedisSerializer());
        template.setHashKeySerializer(new StringRedisSerializer());

        // JSON serializer for values
        Jackson2JsonRedisSerializer<Object> serializer =
            new Jackson2JsonRedisSerializer<>(Object.class);

        ObjectMapper mapper = new ObjectMapper();
        mapper.setVisibility(PropertyAccessor.ALL, JsonAutoDetect.Visibility.ANY);
        mapper.activateDefaultTyping(
            LaissezFaireSubTypeValidator.instance,
            ObjectMapper.DefaultTyping.NON_FINAL);

        serializer.setObjectMapper(mapper);
        template.setValueSerializer(serializer);
        template.setHashValueSerializer(serializer);

        template.afterPropertiesSet();
        return template;
    }

    @Bean
    public StringRedisTemplate stringRedisTemplate(
            RedisConnectionFactory connectionFactory) {
        return new StringRedisTemplate(connectionFactory);
    }
}
```

### Using RedisTemplate

```java
@Service
public class RedisService {

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    @Autowired
    private StringRedisTemplate stringRedisTemplate;

    // String Operations
    public void setString(String key, String value) {
        stringRedisTemplate.opsForValue().set(key, value);
    }

    public String getString(String key) {
        return stringRedisTemplate.opsForValue().get(key);
    }

    public void setWithExpiry(String key, String value, long seconds) {
        stringRedisTemplate.opsForValue()
            .set(key, value, seconds, TimeUnit.SECONDS);
    }

    // Hash Operations
    public void setHash(String key, String field, Object value) {
        redisTemplate.opsForHash().put(key, field, value);
    }

    public Object getHashField(String key, String field) {
        return redisTemplate.opsForHash().get(key, field);
    }

    public Map<Object, Object> getHash(String key) {
        return redisTemplate.opsForHash().entries(key);
    }

    // List Operations
    public void pushToList(String key, Object value) {
        redisTemplate.opsForList().rightPush(key, value);
    }

    public List<Object> getList(String key) {
        return redisTemplate.opsForList().range(key, 0, -1);
    }

    public Object popFromList(String key) {
        return redisTemplate.opsForList().leftPop(key);
    }

    // Set Operations
    public void addToSet(String key, Object... values) {
        redisTemplate.opsForSet().add(key, values);
    }

    public Set<Object> getSet(String key) {
        return redisTemplate.opsForSet().members(key);
    }

    public Boolean isMember(String key, Object value) {
        return redisTemplate.opsForSet().isMember(key, value);
    }

    // Sorted Set Operations
    public void addToZSet(String key, Object value, double score) {
        redisTemplate.opsForZSet().add(key, value, score);
    }

    public Set<Object> getZSetRange(String key, long start, long end) {
        return redisTemplate.opsForZSet().range(key, start, end);
    }

    public Set<Object> getZSetByScore(String key, double min, double max) {
        return redisTemplate.opsForZSet()
            .rangeByScore(key, min, max);
    }

    public Double getScore(String key, Object value) {
        return redisTemplate.opsForZSet().score(key, value);
    }

    // Key Operations
    public Boolean hasKey(String key) {
        return redisTemplate.hasKey(key);
    }

    public Boolean delete(String key) {
        return redisTemplate.delete(key);
    }

    public Boolean expire(String key, long timeout, TimeUnit unit) {
        return redisTemplate.expire(key, timeout, unit);
    }

    public Long getExpire(String key) {
        return redisTemplate.getExpire(key, TimeUnit.SECONDS);
    }
}
```

---

## Spring Data Redis - Caching

### Enable Caching

```java
@Configuration
@EnableCaching
public class CacheConfig {

    @Bean
    public CacheManager cacheManager(
            RedisConnectionFactory connectionFactory) {

        RedisCacheConfiguration config =
            RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofMinutes(10))
                .disableCachingNullValues()
                .serializeKeysWith(
                    RedisSerializationContext.SerializationPair
                        .fromSerializer(new StringRedisSerializer()))
                .serializeValuesWith(
                    RedisSerializationContext.SerializationPair
                        .fromSerializer(
                            new GenericJackson2JsonRedisSerializer()));

        return RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(config)
            .build();
    }
}
```

### Cache Annotations

```java
@Service
public class ProductService {

    @Autowired
    private ProductRepository productRepository;

    // Cache result, key = productId
    @Cacheable(value = "products", key = "#id")
    public Product getProduct(Long id) {
        System.out.println("Fetching from database: " + id);
        return productRepository.findById(id).orElse(null);
    }

    // Cache with condition
    @Cacheable(value = "products", key = "#id",
               condition = "#id > 0")
    public Product getProductConditional(Long id) {
        return productRepository.findById(id).orElse(null);
    }

    // Update cache after method execution
    @CachePut(value = "products", key = "#product.id")
    public Product updateProduct(Product product) {
        return productRepository.save(product);
    }

    // Evict cache entry
    @CacheEvict(value = "products", key = "#id")
    public void deleteProduct(Long id) {
        productRepository.deleteById(id);
    }

    // Evict all entries in cache
    @CacheEvict(value = "products", allEntries = true)
    public void clearCache() {
        System.out.println("Cache cleared");
    }

    // Multiple cache operations
    @Caching(
        cacheable = @Cacheable(value = "products", key = "#id"),
        evict = @CacheEvict(value = "productList", allEntries = true)
    )
    public Product getAndEvict(Long id) {
        return productRepository.findById(id).orElse(null);
    }
}
```

---

## Spring Data Redis - Repository Pattern

### Entity with @RedisHash

```java
@RedisHash("users")
public class User implements Serializable {

    @Id
    private String id;

    @Indexed
    private String email;

    private String name;
    private Integer age;

    @Reference
    private Address address;

    @TimeToLive
    private Long ttl;

    // Constructors, getters, setters

    public User() {}

    public User(String name, String email, Integer age) {
        this.name = name;
        this.email = email;
        this.age = age;
    }

    // Getters and Setters
}

@RedisHash("addresses")
public class Address implements Serializable {

    @Id
    private String id;

    private String street;
    private String city;
    private String zipCode;

    // Constructors, getters, setters
}
```

### Repository Interface

```java
@Repository
public interface UserRepository extends CrudRepository<User, String> {

    // Derived query methods
    List<User> findByName(String name);

    List<User> findByEmail(String email);

    List<User> findByAgeGreaterThan(Integer age);

    List<User> findByNameAndEmail(String name, String email);

    @Query("SELECT * FROM users WHERE age > :age")
    List<User> findUsersOlderThan(@Param("age") Integer age);
}
```

### Enable Redis Repositories

```java
@Configuration
@EnableRedisRepositories(basePackages = "com.example.repository")
public class RedisRepositoryConfig {

    @Bean
    public RedisConnectionFactory connectionFactory() {
        return new LettuceConnectionFactory();
    }

    @Bean
    public RedisTemplate<?, ?> redisTemplate(
            RedisConnectionFactory factory) {
        RedisTemplate<byte[], byte[]> template = new RedisTemplate<>();
        template.setConnectionFactory(factory);
        return template;
    }
}
```

### Using Repository

```java
@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public User createUser(User user) {
        return userRepository.save(user);
    }

    public Optional<User> getUser(String id) {
        return userRepository.findById(id);
    }

    public List<User> getAllUsers() {
        return (List<User>) userRepository.findAll();
    }

    public List<User> findByEmail(String email) {
        return userRepository.findByEmail(email);
    }

    public void deleteUser(String id) {
        userRepository.deleteById(id);
    }

    public long countUsers() {
        return userRepository.count();
    }
}
```

---

## Spring Data Redis - Pub/Sub

### Message Listener

```java
@Component
public class RedisMessageSubscriber implements MessageListener {

    @Override
    public void onMessage(Message message, byte[] pattern) {
        String channel = new String(message.getChannel());
        String body = new String(message.getBody());

        System.out.println("Received message: " + body
                         + " from channel: " + channel);
    }
}
```

### Configuration

```java
@Configuration
public class RedisPubSubConfig {

    @Bean
    public RedisMessageListenerContainer redisContainer(
            RedisConnectionFactory connectionFactory,
            MessageListener messageListener) {

        RedisMessageListenerContainer container =
            new RedisMessageListenerContainer();
        container.setConnectionFactory(connectionFactory);

        container.addMessageListener(messageListener,
            new ChannelTopic("notifications"));

        return container;
    }

    @Bean
    public MessageListener messageListener() {
        return new RedisMessageSubscriber();
    }
}
```

### Publishing Messages

```java
@Service
public class RedisPublisher {

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    public void publish(String channel, Object message) {
        redisTemplate.convertAndSend(channel, message);
    }
}

// Usage
@RestController
public class NotificationController {

    @Autowired
    private RedisPublisher publisher;

    @PostMapping("/notify")
    public void sendNotification(@RequestBody String message) {
        publisher.publish("notifications", message);
    }
}
```

---

## Spring Data Redis - Pipelining

```java
@Service
public class RedisPipelineService {

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    public List<Object> executePipeline() {
        return redisTemplate.executePipelined(
            new RedisCallback<Object>() {
                @Override
                public Object doInRedis(RedisConnection connection) {
                    StringRedisConnection conn =
                        (StringRedisConnection) connection;

                    for (int i = 0; i < 100; i++) {
                        conn.set("key" + i, "value" + i);
                    }

                    for (int i = 0; i < 100; i++) {
                        conn.get("key" + i);
                    }

                    return null;
                }
            });
    }
}
```

---

## Spring Data Redis - Transactions

```java
@Service
public class RedisTransactionService {

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    public void executeTransaction() {
        redisTemplate.execute(new SessionCallback<List<Object>>() {
            @Override
            public List<Object> execute(RedisOperations operations) {
                operations.multi();

                operations.opsForValue().set("key1", "value1");
                operations.opsForValue().increment("counter");
                operations.opsForList().rightPush("list", "item");

                return operations.exec();
            }
        });
    }

    // With WATCH for optimistic locking
    public boolean transferWithWatch(String fromKey, String toKey,
                                    double amount) {
        return redisTemplate.execute(new SessionCallback<Boolean>() {
            @Override
            public Boolean execute(RedisOperations operations) {
                operations.watch(fromKey);

                Double balance = (Double) operations.opsForValue()
                    .get(fromKey);

                if (balance < amount) {
                    operations.unwatch();
                    return false;
                }

                operations.multi();
                operations.opsForValue().increment(fromKey, -amount);
                operations.opsForValue().increment(toKey, amount);

                List<Object> results = operations.exec();
                return results != null;
            }
        });
    }
}
```

---

## Common Interview Questions

### 1. Why use Redis?

- **Speed:** In-memory storage with sub-millisecond latency
- **Data Structures:** Rich set of data types
- **Persistence:** Optional RDB/AOF persistence
- **Scalability:** Clustering and replication support
- **Atomic Operations:** Thread-safe operations

### 2. Redis vs Memcached?

- Redis supports multiple data structures; Memcached only key-value
- Redis has persistence; Memcached is volatile
- Redis has pub/sub, transactions; Memcached doesn't
- Redis is single-threaded; Memcached is multi-threaded

### 3. When to use Redis caching?

- Frequently accessed data
- Expensive database queries
- Session storage
- Real-time analytics
- Rate limiting

### 4. Redis Cluster vs Sentinel?

- **Cluster:** Horizontal scaling, automatic sharding
- **Sentinel:** High availability, automatic failover, monitoring

### 5. Redis single-threaded - is it a limitation?

- No, Redis uses I/O multiplexing and event loop
- CPU is rarely bottleneck (I/O bound workload)
- Simplifies design, no locking needed
- Can run multiple instances for CPU utilization

---

## Best Practices

### Performance

- Use pipelining for bulk operations
- Avoid KEYS command in production (use SCAN)
- Set appropriate TTL to prevent memory overflow
- Use connection pooling
- Monitor memory usage

### Data Modeling

- Keep keys short but meaningful
- Use consistent naming conventions (e.g., `user:1001:profile`)
- Denormalize data when needed
- Use hash for objects instead of multiple keys
- Consider data access patterns

### Security

- Enable authentication (`requirepass`)
- Bind to specific interfaces
- Use TLS for data in transit
- Disable dangerous commands in production
- Regular backups

### Spring Boot Integration

- Use `@EnableCaching` for declarative caching
- Configure appropriate serializers
- Set reasonable cache TTL
- Handle cache failures gracefully
- Monitor cache hit/miss ratios

---

This comprehensive cheat sheet covers all essential Redis and Spring Data Redis concepts with practical code examples for interview preparation.
