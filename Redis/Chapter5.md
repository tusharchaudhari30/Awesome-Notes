# Chapter 5: Spring Boot Caching with Redis

## 5.1 Spring Cache Abstraction Overview

### What is Spring Cache Abstraction?

Spring Cache Abstraction provides a declarative, annotation-based caching mechanism that abstracts the underlying cache implementation. It separates cache-related concerns from business logic, allowing developers to focus on domain logic while caching infrastructure is handled transparently.

### Key Components

**CacheManager**: Central interface managing named caches. Implementations include RedisCacheManager, ConcurrentMapCacheManager, and others.

**Cache**: Actual cache store where data is stored/retrieved. Spring provides implementations for various backends.

**Annotations**: Declarative cache operations applied to methods

**Spring Expression Language (SpEL)**: Dynamic cache key generation

### Layers of Abstraction

1. **Application Code**: Business logic with cache annotations
2. **Spring Cache Abstraction**: Common interface
3. **Cache Implementation**: Redis, Caffeine, Memcached, etc.

This abstraction allows switching cache implementations with minimal code changes.

## 5.2 @Cacheable Annotation and Cache Behavior

### @Cacheable Basics

**@Cacheable** marks methods whose return values should be cached. The first call executes the method; subsequent calls with same arguments return cached value.

**Basic Usage**

```java
@Cacheable("users")
public User getUser(String id) {
    // Database call
    return userRepository.findById(id).orElse(null);
}
```

Automatically caches result under key "users#id".

### Cache Key Generation

**Default Key Generation**

By default, Spring uses all method parameters as cache key:

```java
@Cacheable("products")
public Product getProduct(long id) {
    return productRepository.findById(id);
}

// Cache key: id parameter value
```

**Custom Key**

```java
@Cacheable(value = "users", key = "#id")
public User getUser(String id) {
    return userRepository.findById(id);
}

// Or combine multiple parameters
@Cacheable(value = "orders", key = "#userId + ':' + #orderId")
public Order getOrder(String userId, String orderId) {
    return orderRepository.findByUserAndOrder(userId, orderId);
}
```

### SpEL Expressions for Keys

**Common Expressions**

```java
@Cacheable(value = "cache", key = "#p0")                    // First parameter
@Cacheable(value = "cache", key = "#user.id")               // Nested field
@Cacheable(value = "cache", key = "#user.name.toUpperCase()") // Method call
@Cacheable(value = "cache", key = "T(java.util.UUID).randomUUID().toString()") // Static method
```

### Cache Attributes

```java
@Cacheable(
    value = "users",              // Cache name
    key = "#id",                  // Custom key
    condition = "#id > 0",        // Only cache if condition true
    unless = "#result == null"    // Don't cache if result null
)
public User getUser(String id) {
    return userRepository.findById(id);
}
```

**condition**: Evaluated before method execution; if false, method always executes

**unless**: Evaluated after method execution; if true, result not cached

### Cache Behavior

**First Call (Cache Miss)**

1. Method marked with @Cacheable is executed
2. Return value is stored in cache using generated key
3. Value returned to caller

**Second Call (Cache Hit)**

1. Cache checked before method execution
2. If key found, cached value returned directly
3. Method not executed

**Cache Parameters**

| Parameter | Purpose               | Example                    |
| --------- | --------------------- | -------------------------- |
| value     | Cache name (required) | @Cacheable("users")        |
| key       | Cache key expression  | key = "#id"                |
| condition | When to cache         | condition = "#id > 0"      |
| unless    | When NOT to cache     | unless = "#result == null" |

## 5.3 @CachePut for Cache Updates

### @CachePut Annotation

**@CachePut** always executes the method and updates cache with the return value. Unlike @Cacheable, the method is never skipped.

**Use Cases**: Updating data and refreshing cache simultaneously

### Basic Usage

```java
@CachePut(value = "users", key = "#user.id")
public User updateUser(User user) {
    return userRepository.save(user);
}
```

Each call:

1. Method executes completely
2. Database updated
3. Cache updated with new value

### Difference from @Cacheable

| Feature          | @Cacheable                  | @CachePut                |
| ---------------- | --------------------------- | ------------------------ |
| Method Execution | Skipped on cache hit        | Always executed          |
| Cache Update     | On first hit, stores result | Always updates           |
| Use Case         | Retrieve cached data        | Update and refresh cache |

### Complex Update Example

```java
@CachePut(value = "products", key = "#product.id")
public Product updateProductPrice(Product product, double newPrice) {
    product.setPrice(newPrice);
    product.setLastUpdated(LocalDateTime.now());
    return productRepository.save(product);
}
```

Always updates cache with latest product data.

### Combination with @CacheEvict

```java
@Caching(
    put = @CachePut(value = "products", key = "#result.id"),
    evict = @CacheEvict(value = "productList", allEntries = true)
)
public Product saveProduct(Product product) {
    return productRepository.save(product);
}
```

Updates product cache, invalidates product list cache.

## 5.4 @CacheEvict for Cache Removal

### @CacheEvict Annotation

**@CacheEvict** removes data from cache. Useful for invalidating stale data when records change or delete.

### Basic Usage

```java
@CacheEvict(value = "users", key = "#id")
public void deleteUser(String id) {
    userRepository.deleteById(id);
}
```

After user deleted from database, cached entry also removed.

### Remove All Entries

```java
@CacheEvict(value = "users", allEntries = true)
public void refreshAllUsers() {
    // Clear entire cache
}
```

**allEntries = true**: Removes all entries from cache, not just specific key

### Conditional Eviction

```java
@CacheEvict(
    value = "users",
    key = "#id",
    condition = "#id > 100"
)
public void deleteUser(String id) {
    userRepository.deleteById(id);
}
```

Only evicts if condition satisfied.

### Before vs After Method Execution

```java
@CacheEvict(value = "users", key = "#id", beforeInvocation = false)
public void deleteUser(String id) {
    userRepository.deleteById(id);
}

@CacheEvict(value = "users", key = "#id", beforeInvocation = true)
public void archiveUser(String id) {
    userRepository.archive(id);
}
```

**beforeInvocation = false** (default): Method executes first, then cache evicted

**beforeInvocation = true**: Cache evicted before method execution

Use beforeInvocation=true if method might fail; true ensures cache cleared regardless.

## 5.5 @EnableCaching Configuration

### Enabling Caching

Add **@EnableCaching** to any @Configuration class to enable cache annotations:

```java
@Configuration
@EnableCaching
public class CacheConfig {

}
```

Or on application class:

```java
@SpringBootApplication
@EnableCaching
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### Auto-Configuration

Once @EnableCaching added and Redis dependency present, Spring Boot auto-configures:

- RedisConnectionFactory
- RedisCacheManager
- StringRedisTemplate

### Disabling Cache at Runtime

```java
@Configuration
@EnableCaching(proxyTargetClass = true)
public class CacheConfig {

}
```

**proxyTargetClass**: Uses CGLIB proxy instead of JDK proxy for more compatibility

## 5.6 Conditional Caching with condition Parameter

### condition Attribute

Evaluated **before** method execution. If false, caching skipped entirely.

### Common Conditions

**Condition Based on Parameter Value**

```java
@Cacheable(
    value = "users",
    key = "#id",
    condition = "#id > 0"
)
public User getUser(String id) {
    return userRepository.findById(id);
}
```

Only caches if id greater than 0.

**Condition Based on Multiple Parameters**

```java
@Cacheable(
    value = "orders",
    key = "#userId + ':' + #orderId",
    condition = "#userId != null && #orderId > 0"
)
public Order getOrder(String userId, String orderId) {
    return orderRepository.find(userId, orderId);
}
```

**Condition Using Method Parameters Directly**

```java
@Cacheable(
    value = "products",
    condition = "#includeCache"
)
public Product getProduct(String id, boolean includeCache) {
    return productRepository.findById(id);
}
```

Caller can control caching: `getProduct("123", true)` or `getProduct("123", false)`

## 5.7 Cache Key Generation Strategies

### Custom Key Strategy Implementation

```java
@Configuration
@EnableCaching
public class CacheConfig {

    @Bean
    public KeyGenerator customKeyGenerator() {
        return (target, method, params) -> {
            StringBuilder key = new StringBuilder();
            key.append(method.getName());

            for (Object param : params) {
                key.append("_");
                if (param == null) {
                    key.append("null");
                } else {
                    key.append(param.toString());
                }
            }

            return key.toString();
        };
    }
}
```

Use custom key generator:

```java
@Cacheable(value = "users", keyGenerator = "customKeyGenerator")
public User getUser(String id) {
    return userRepository.findById(id);
}
```

### Composite Key Strategy

```java
@Cacheable(
    value = "transactions",
    key = "T(com.example.CacheKeyUtil).generateKey(#accountId, #date)"
)
public List<Transaction> getTransactions(String accountId, LocalDate date) {
    return transactionRepository.findByAccountAndDate(accountId, date);
}
```

### Tenant-Aware Caching

```java
@Cacheable(
    value = "users",
    key = "#getTenantId() + ':' + #id"
)
public User getUser(String id) {
    return userRepository.findById(id);
}

private String getTenantId() {
    return TenantContext.getCurrentTenantId();
}
```

Caches per tenant, preventing cross-tenant data leakage.

## 5.8 RedisCacheManager Configuration

### Basic Configuration

```java
@Configuration
@EnableCaching
public class RedisCacheConfig {

    @Bean
    public RedisCacheManager cacheManager(
            RedisConnectionFactory connectionFactory) {

        RedisCacheConfiguration config =
            RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofMinutes(10));

        return RedisCacheManager.builder(connectionFactory)
                .cacheDefaults(config)
                .build();
    }
}
```

### Advanced Configuration

```java
@Bean
public RedisCacheManager cacheManager(
        RedisConnectionFactory connectionFactory) {

    // Default config for all caches
    RedisCacheConfiguration defaultConfig =
        RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(10))
            .serializeKeysWith(SerializationPair.fromSerializer(
                new StringRedisSerializer()))
            .serializeValuesWith(SerializationPair.fromSerializer(
                new GenericJackson2JsonRedisSerializer()));

    // Custom config for specific cache
    RedisCacheConfiguration usersConfig =
        RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofHours(1))
            .prefixCacheNameWith("app.users.");

    return RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(defaultConfig)
            .withCacheConfiguration("users", usersConfig)
            .build();
}
```

### Null Value Handling

```java
RedisCacheConfiguration config =
    RedisCacheConfiguration.defaultCacheConfig()
        .disableCachingNullValues();  // Don't cache nulls
```

Prevents caching null values, useful to avoid caching missing records.

## 5.9 Cache Expiration and TTL Settings

### Global TTL Configuration

```java
@Bean
public RedisCacheManager cacheManager(
        RedisConnectionFactory connectionFactory) {

    RedisCacheConfiguration config =
        RedisCacheConfiguration.defaultCacheConfig()
            .enableTtl()
            .entryTtl(Duration.ofMinutes(30));

    return RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(config)
            .build();
}
```

All cache entries expire after 30 minutes.

### Per-Cache TTL Configuration

```java
@Bean
public RedisCacheManager cacheManager(
        RedisConnectionFactory connectionFactory) {

    RedisCacheConfiguration defaultConfig =
        RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(30));

    RedisCacheConfiguration sessionConfig =
        RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofHours(2));

    RedisCacheConfiguration quickConfig =
        RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofSeconds(5));

    Map<String, RedisCacheConfiguration> cacheConfigs =
        Map.of(
            "sessions", sessionConfig,
            "quick-results", quickConfig
        );

    return RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(defaultConfig)
            .withInitialCacheConfigurations(cacheConfigs)
            .build();
}
```

### Dynamic TTL Function

```java
@Bean
public RedisCacheManager cacheManager(
        RedisConnectionFactory connectionFactory) {

    RedisCacheWriter.TtlFunction ttlFunction = (key, value) -> {
        if (key.startsWith("session:")) {
            return Duration.ofHours(2);
        } else if (key.startsWith("temp:")) {
            return Duration.ofMinutes(5);
        } else {
            return Duration.ofMinutes(30);
        }
    };

    RedisCacheConfiguration config =
        RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(ttlFunction);

    return RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(config)
            .build();
}
```

Different TTL based on cache key pattern.

## 5.10 Multi-Level Caching Strategies

### Two-Level Caching (Local + Distributed)

```java
@Configuration
@EnableCaching
public class MultiLevelCacheConfig {

    @Bean
    public CacheManager cacheManager(
            RedisConnectionFactory redisConnectionFactory) {

        // Local (L1) cache
        Cache caffeineCache = new CaffeineCache("products",
            Caffeine.newBuilder()
                .maximumSize(1000)
                .expireAfterWrite(5, TimeUnit.MINUTES)
                .build());

        // Distributed (L2) cache
        RedisCacheConfiguration redisConfig =
            RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofMinutes(30));

        RedisCacheManager redisManager =
            RedisCacheManager.builder(redisConnectionFactory)
                .cacheDefaults(redisConfig)
                .build();

        // Composite manager
        CompositeCacheManager manager = new CompositeCacheManager();
        manager.setCacheManagers(Arrays.asList(
            new ConcurrentMapCacheManager("products"),
            redisManager
        ));

        return manager;
    }
}
```

Checks local cache first, then distributed Redis.

### Caffeine + Redis

```java
@Configuration
public class HybridCacheConfig {

    @Bean
    public CacheManager cacheManager(
            RedisConnectionFactory connectionFactory) {

        // Caffeine config
        CacheBuilder cacheBuilder = CacheBuilder.newBuilder()
                .maximumSize(500)
                .expireAfterWrite(5, TimeUnit.MINUTES);

        // Create Caffeine cache manager
        CaffeineCacheManager caffeineManager = new CaffeineCacheManager();
        caffeineManager.setCacheBuilder(cacheBuilder);
        caffeineManager.setCacheNames("users", "products");

        // Redis manager for distributed cache
        RedisCacheManager redisManager =
            RedisCacheManager.builder(connectionFactory).build();

        // Composite with fallback
        CompositeCacheManager composite = new CompositeCacheManager();
        composite.setCacheManagers(
            Arrays.asList(caffeineManager, redisManager));
        composite.setFallbackToNoOpCache(true);

        return composite;
    }
}
```

## 5.11 Cache Patterns (Cache-Aside, Write-Through, Write-Behind)

### Cache-Aside Pattern (Default)

Application manages cache and database interaction.

```java
@Service
public class UserService {

    @Cacheable("users")
    public User getUser(String id) {
        // On cache miss, database is queried
        return userRepository.findById(id);
    }

    public void updateUser(User user) {
        // Application updates database
        userRepository.save(user);

        // Application updates cache
        userCache.put(user.getId(), user);
    }

    public void deleteUser(String id) {
        // Application deletes from database
        userRepository.deleteById(id);

        // Application invalidates cache
        userCache.delete(id);
    }
}
```

**When to Use**: Simple, flexible, cache-database consistency controlled by application

### Write-Through Pattern

Data written to cache and database simultaneously.

```java
@Service
public class ProductService {

    @CachePut(value = "products", key = "#result.id")
    public Product updateProduct(Product product) {
        // Write to database first
        Product saved = productRepository.save(product);

        // Cache automatically updated due to @CachePut
        return saved;
    }

    @Caching(
        put = @CachePut(value = "products", key = "#result.id"),
        evict = @CacheEvict(value = "productList", allEntries = true)
    )
    public Product createProduct(Product product) {
        Product saved = productRepository.save(product);
        return saved;
    }
}
```

**When to Use**: Consistency critical, can tolerate write latency

### Write-Behind (Write-Back) Pattern

Cache updated immediately, database update delayed.

```java
@Service
public class CacheService {

    private final Cache cache;
    private final ScheduledExecutorService executor;

    @CachePut(value = "records", key = "#id")
    public void updateRecord(String id, RecordData data) {
        // Update cache immediately
        cache.put(id, data);

        // Schedule database update asynchronously
        executor.schedule(() -> {
            try {
                database.update(id, data);
            } catch (Exception e) {
                log.error("Failed to update database", e);
            }
        }, 1, TimeUnit.SECONDS);
    }
}
```

**When to Use**: Performance critical, eventual consistency acceptable

### Comparison

| Pattern       | Database Update | Cache Update | Consistency | Performance |
| ------------- | --------------- | ------------ | ----------- | ----------- |
| Cache-Aside   | Immediate       | On demand    | Manual      | Moderate    |
| Write-Through | Immediate       | Synchronous  | Strong      | Slower      |
| Write-Behind  | Delayed         | Immediate    | Eventual    | Faster      |

## 5.12 Cache Invalidation Strategies

### Time-Based Invalidation (TTL)

```java
@Configuration
public class CacheConfig {

    @Bean
    public RedisCacheManager cacheManager(
            RedisConnectionFactory connectionFactory) {

        RedisCacheConfiguration config =
            RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofMinutes(10));  // Auto-expire

        return RedisCacheManager.builder(connectionFactory)
                .cacheDefaults(config)
                .build();
    }
}
```

Data automatically expires after configured duration. Simple, effective for predictable update intervals.

### Event-Driven Invalidation

```java
@Service
public class UserService {

    @Autowired
    private ApplicationEventPublisher eventPublisher;

    public void updateUser(User user) {
        User updated = userRepository.save(user);

        // Publish event to invalidate cache
        eventPublisher.publishEvent(
            new UserUpdatedEvent(updated.getId()));
    }
}

@Component
public class CacheInvalidationListener {

    @Autowired
    private CacheManager cacheManager;

    @EventListener
    public void handleUserUpdate(UserUpdatedEvent event) {
        Cache cache = cacheManager.getCache("users");
        cache.evict(event.getUserId());
    }
}
```

Manual control for critical data updates.

### Scheduled Cache Refresh

```java
@Component
public class CacheRefresher {

    @Autowired
    private UserService userService;

    @Scheduled(fixedRate = 3600000)  // Hourly
    public void refreshUserCache() {
        // Periodic cache refresh
        List<User> users = userService.getAllUsers();
        // Trigger cache updates
    }
}
```

Proactively refresh cache before expiration.

### Stale-While-Revalidate

```java
@Component
public class SmartCache {

    @Cacheable("data")
    public Data getData(String id) {
        return fetchFromDatabase(id);
    }

    public Data getDataWithRevalidation(String id) {
        // Return cached value immediately if exists
        Data cached = cache.get(id);

        if (cached != null) {
            // Check if stale, revalidate in background
            if (isCacheStale(id)) {
                asyncRefreshCache(id);
            }
            return cached;
        }

        // Cache miss, fetch synchronously
        return getData(id);
    }
}
```

Serve stale data while updating in background.

## 5.13 Performance Tuning and Monitoring

### Monitoring Cache Metrics

**Spring Boot Actuator Metrics**

```yaml
management:
  endpoints:
    web:
      exposure:
        include: metrics
  metrics:
    tags:
      application: my-app
```

Access metrics: `/actuator/metrics/cache.gets`

**Custom Metrics**

```java
@Component
public class CacheMetrics {

    private final MeterRegistry meterRegistry;
    private final AtomicInteger hits = new AtomicInteger(0);
    private final AtomicInteger misses = new AtomicInteger(0);

    public CacheMetrics(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;

        Gauge.builder("cache.hits", hits, AtomicInteger::get)
            .register(meterRegistry);

        Gauge.builder("cache.misses", misses, AtomicInteger::get)
            .register(meterRegistry);
    }

    public void recordHit() {
        hits.incrementAndGet();
    }

    public void recordMiss() {
        misses.incrementAndGet();
    }

    public double getHitRate() {
        int total = hits.get() + misses.get();
        return total == 0 ? 0 : (double) hits.get() / total;
    }
}
```

### Performance Tuning Guidelines

**Cache Size Optimization**

```java
RedisCacheConfiguration config =
    RedisCacheConfiguration.defaultCacheConfig()
        .prefixCacheNameWith("app.")  // Smaller keys
        .disableCachingNullValues();  // Reduce size
```

Keep cache size appropriate:

- Too small: High miss rate, thrashing
- Too large: Wasted memory, slower eviction

**Key Length Impact**

```
Short key: app:u:123      (12 bytes)
Long key:  application_user_123_detail  (35 bytes)
```

Shorter keys reduce memory overhead.

**Serialization Performance**

Use fastest appropriate serializer:

1. **String** (fastest): For primitive strings
2. **JSON** (balanced): General purpose
3. **Binary** (compact): Space-conscious

**Connection Pool Tuning**

```yaml
spring:
  redis:
    jedis:
      pool:
        max-active: 16 # Increase for high concurrency
        max-idle: 8
        min-idle: 4
```

### Monitoring Tools

**Prometheus + Grafana**

```java
@Configuration
public class PrometheusConfig {

    @Bean
    public MeterRegistry meterRegistry() {
        return new PrometheusMeterRegistry(
            PrometheusConfig.DEFAULT);
    }
}
```

**Micrometer Integration**

```java
@Service
public class CachedService {

    @Timed(value = "user.cache", description = "User cache operations")
    @Cacheable("users")
    public User getUser(String id) {
        return userRepository.findById(id);
    }
}
```

**Redis CLI Monitoring**

```bash
redis-cli
> INFO stats
> KEYS *
> MEMORY STATS
```

### Common Performance Issues

**Issue: High Cache Miss Rate**

- **Cause**: Cache too small or TTL too short
- **Solution**: Increase cache size or TTL, analyze access patterns

**Issue: High Memory Usage**

- **Cause**: Large objects cached or nulls cached
- **Solution**: Compress data, disable null caching, increase TTL

**Issue: Inconsistency Between Cache and DB**

- **Cause**: Cache invalidation not triggered
- **Solution**: Implement event-driven invalidation, audit logs

**Issue: Slow Read Performance**

- **Cause**: Serialization overhead
- **Solution**: Use faster serializer, optimize network round trips
