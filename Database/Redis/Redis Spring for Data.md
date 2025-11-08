# End-to-End Guide: Implementing Redis Caching in Spring Boot

## Overview

Redis caching in Spring Boot significantly improves application performance by reducing database load and response times. This guide walks you through the complete implementation process, from setup to production-ready configuration.

## Prerequisites

- Java 17 or later
- Maven or Gradle
- Redis server (local installation or Docker)
- Spring Boot 3.x
- Basic understanding of Spring Framework

## Step 1: Project Setup

### Add Dependencies

For Maven, add the following dependencies to your `pom.xml`:

```xml
<dependencies>
    <!-- Spring Boot Starter Web -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <!-- Spring Data Redis -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-redis</artifactId>
    </dependency>

    <!-- Spring Data JPA (if using database) -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>

    <!-- Database Driver (MySQL/PostgreSQL/H2) -->
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <scope>runtime</scope>
    </dependency>

    <!-- Lombok (Optional) -->
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <optional>true</optional>
    </dependency>
</dependencies>
```

For Gradle, add to your `build.gradle`:

```gradle
implementation 'org.springframework.boot:spring-boot-starter-data-redis'
implementation 'org.springframework.boot:spring-boot-starter-web'
implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
runtimeOnly 'com.h2database:h2'
```

**Note:** Spring Boot uses Lettuce as the default Redis client. If you prefer Jedis, add the following dependency:

```xml
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
</dependency>
```

## Step 2: Redis Server Setup

### Option A: Using Docker (Recommended)

Create a `docker-compose.yml` file in your project root:

```yaml
services:
  redis:
    image: redis:7.4.2
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
    driver: local
```

Start Redis:

```bash
docker-compose up -d
```

### Option B: Local Installation

**Windows:** Download from Microsoft's Redis archive  
**macOS:** Install via Homebrew: `brew install redis`  
**Linux:** Install via package manager: `sudo apt-get install redis-server`

Start Redis server:

```bash
redis-server
```

## Step 3: Configure Application Properties

Add Redis configuration to `application.properties`:

```properties
# Redis Configuration
spring.data.redis.host=localhost
spring.data.redis.port=6379
spring.cache.type=redis

# Optional: Redis Connection Pool Settings
spring.data.redis.lettuce.pool.max-active=8
spring.data.redis.lettuce.pool.max-idle=8
spring.data.redis.lettuce.pool.min-idle=0

# Database Configuration (if using)
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driver-class-name=org.h2.Driver
spring.jpa.show-sql=true
```

For YAML configuration (`application.yml`):

```yaml
spring:
  cache:
    type: redis
  data:
    redis:
      host: localhost
      port: 6379
      lettuce:
        pool:
          max-active: 8
          max-idle: 8
          min-idle: 0
```

## Step 4: Enable Caching

Annotate your main application class with `@EnableCaching`:

```java
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;

@SpringBootApplication
@EnableCaching
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

## Step 5: Configure Redis Cache Manager

Create a configuration class for customizing cache behavior:

```java
package com.example.demo.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.cache.RedisCacheConfiguration;
import org.springframework.data.redis.cache.RedisCacheManager;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.serializer.GenericJackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.RedisSerializationContext;
import org.springframework.data.redis.serializer.StringRedisSerializer;

import java.time.Duration;

@Configuration
public class RedisConfig {

    @Bean
    public RedisCacheManager cacheManager(RedisConnectionFactory connectionFactory) {
        // Default cache configuration
        RedisCacheConfiguration defaultConfig = RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofMinutes(10))  // Cache expires after 10 minutes
                .disableCachingNullValues()         // Don't cache null values
                .serializeKeysWith(RedisSerializationContext.SerializationPair
                        .fromSerializer(new StringRedisSerializer()))
                .serializeValuesWith(RedisSerializationContext.SerializationPair
                        .fromSerializer(new GenericJackson2JsonRedisSerializer()));

        return RedisCacheManager.builder(connectionFactory)
                .cacheDefaults(defaultConfig)
                .build();
    }
}
```

### Advanced Configuration with Multiple TTL Values

For different cache expiration times:

```java
@Bean
public RedisCacheManager cacheManager(RedisConnectionFactory connectionFactory) {
    RedisCacheConfiguration defaultConfig = RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(10))
            .disableCachingNullValues();

    // Different TTL for specific caches
    Map<String, RedisCacheConfiguration> cacheConfigurations = new HashMap<>();
    cacheConfigurations.put("products",
            defaultConfig.entryTtl(Duration.ofHours(1)));
    cacheConfigurations.put("users",
            defaultConfig.entryTtl(Duration.ofMinutes(30)));

    return RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(defaultConfig)
            .withInitialCacheConfigurations(cacheConfigurations)
            .build();
}
```

## Step 6: Create Entity Class

```java
package com.example.demo.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Product implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String description;
    private Double price;
}
```

**Important:** Entities must implement `Serializable` for Redis caching.

## Step 7: Create Repository

```java
package com.example.demo.repository;

import com.example.demo.model.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
}
```

## Step 8: Implement Service Layer with Cache Annotations

```java
package com.example.demo.service;

import com.example.demo.model.Product;
import com.example.demo.repository.ProductRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.CachePut;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class ProductService {

    private final ProductRepository productRepository;

    // Cache the result with key as product ID
    @Cacheable(value = "products", key = "#id")
    public Optional<Product> getProductById(Long id) {
        log.info("Fetching product from database for id: {}", id);
        return productRepository.findById(id);
    }

    // Cache all products
    @Cacheable(value = "products", key = "'all'")
    public List<Product> getAllProducts() {
        log.info("Fetching all products from database");
        return productRepository.findAll();
    }

    // Update cache after saving
    @CachePut(value = "products", key = "#product.id")
    public Product saveProduct(Product product) {
        log.info("Saving product: {}", product);
        return productRepository.save(product);
    }

    // Remove from cache after deletion
    @CacheEvict(value = "products", key = "#id")
    public void deleteProduct(Long id) {
        log.info("Deleting product with id: {}", id);
        productRepository.deleteById(id);
    }

    // Clear all products cache
    @CacheEvict(value = "products", allEntries = true)
    public void clearCache() {
        log.info("Clearing all products cache");
    }
}
```

### Understanding Cache Annotations

**@Cacheable:** Caches the method result. Subsequent calls with the same parameters return cached data without executing the method.

**@CachePut:** Always executes the method and updates the cache with the result. Use for update operations.

**@CacheEvict:** Removes entries from the cache. Use for delete operations or when data becomes stale.

**Key Expression:** The `key` attribute uses SpEL (Spring Expression Language). Examples:

- `key = "#id"` - uses method parameter
- `key = "'all'"` - static string key
- `key = "#product.id"` - uses object property

## Step 9: Create REST Controller

```java
package com.example.demo.controller;

import com.example.demo.model.Product;
import com.example.demo.service.ProductService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/products")
@RequiredArgsConstructor
public class ProductController {

    private final ProductService productService;

    @GetMapping("/{id}")
    public ResponseEntity<Product> getProduct(@PathVariable Long id) {
        return productService.getProductById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping
    public ResponseEntity<List<Product>> getAllProducts() {
        return ResponseEntity.ok(productService.getAllProducts());
    }

    @PostMapping
    public ResponseEntity<Product> createProduct(@RequestBody Product product) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(productService.saveProduct(product));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Product> updateProduct(
            @PathVariable Long id,
            @RequestBody Product product) {
        product.setId(id);
        return ResponseEntity.ok(productService.saveProduct(product));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProduct(@PathVariable Long id) {
        productService.deleteProduct(id);
        return ResponseEntity.noContent().build();
    }

    @DeleteMapping("/cache/clear")
    public ResponseEntity<String> clearCache() {
        productService.clearCache();
        return ResponseEntity.ok("Cache cleared successfully");
    }
}
```

## Step 10: Testing the Application

### Start the Application

```bash
mvn spring-boot:run
```

### Test Cache Operations

**Create a Product:**

```bash
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","description":"Gaming laptop","price":1500.00}'
```

**Get Product (First Call - Database Hit):**

```bash
curl http://localhost:8080/api/products/1
```

Check logs: You should see "Fetching product from database for id: 1"

**Get Product Again (Second Call - Cache Hit):**

```bash
curl http://localhost:8080/api/products/1
```

Check logs: No database fetch message appears - data comes from cache!

**Update Product:**

```bash
curl -X PUT http://localhost:8080/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Gaming Laptop","description":"Updated laptop","price":1600.00}'
```

**Delete Product:**

```bash
curl -X DELETE http://localhost:8080/api/products/1
```

**Clear All Cache:**

```bash
curl -X DELETE http://localhost:8080/api/products/cache/clear
```

## Step 11: Verify Cache in Redis

### Using Redis CLI

```bash
redis-cli

# List all keys
KEYS *

# Get cache value
GET products::1

# Check TTL
TTL products::1

# Delete specific key
DEL products::1

# Clear all cache
FLUSHALL
```

## Advanced Configurations

### Custom Serialization with Jackson

For better JSON serialization control:

```java
@Bean
public RedisCacheConfiguration redisCacheConfiguration(ObjectMapper objectMapper) {
    ObjectMapper cacheObjectMapper = objectMapper.copy();
    cacheObjectMapper.activateDefaultTyping(
            cacheObjectMapper.getPolymorphicTypeValidator(),
            ObjectMapper.DefaultTyping.NON_FINAL
    );

    Jackson2JsonRedisSerializer<Object> serializer =
            new Jackson2JsonRedisSerializer<>(cacheObjectMapper, Object.class);

    return RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(10))
            .serializeValuesWith(RedisSerializationContext.SerializationPair
                    .fromSerializer(serializer));
}
```

### Conditional Caching

Cache only when certain conditions are met:

```java
@Cacheable(value = "products", key = "#id", condition = "#id > 10")
public Optional<Product> getProductById(Long id) {
    return productRepository.findById(id);
}

@Cacheable(value = "products", unless = "#result == null")
public Product findProduct(Long id) {
    return productRepository.findById(id).orElse(null);
}
```

### Cache with Multiple Keys

```java
@Cacheable(value = "products", key = "#name + '_' + #category")
public List<Product> findByNameAndCategory(String name, String category) {
    return productRepository.findByNameAndCategory(name, category);
}
```

## Best Practices

### Choose Appropriate TTL Values

- Frequently changing data: 1-5 minutes
- Moderately stable data: 10-30 minutes
- Rarely changing data: 1-24 hours
- Static data: Multiple days

### Implement Cache Warming

Populate cache proactively during startup:

```java
@Component
public class CacheWarmer implements ApplicationListener<ApplicationReadyEvent> {

    @Autowired
    private ProductService productService;

    @Override
    public void onApplicationEvent(ApplicationReadyEvent event) {
        productService.getAllProducts();
    }
}
```

### Handle Cache Failures Gracefully

Ensure application works even if Redis is unavailable:

```java
@Bean
public CacheErrorHandler errorHandler() {
    return new CacheErrorHandler() {
        @Override
        public void handleCacheGetError(RuntimeException exception,
                                       Cache cache, Object key) {
            log.error("Cache get error: {}", exception.getMessage());
        }

        @Override
        public void handleCachePutError(RuntimeException exception,
                                       Cache cache, Object key, Object value) {
            log.error("Cache put error: {}", exception.getMessage());
        }

        @Override
        public void handleCacheEvictError(RuntimeException exception,
                                         Cache cache, Object key) {
            log.error("Cache evict error: {}", exception.getMessage());
        }

        @Override
        public void handleCacheClearError(RuntimeException exception, Cache cache) {
            log.error("Cache clear error: {}", exception.getMessage());
        }
    };
}
```

### Use Appropriate Eviction Policies

Configure eviction strategies based on your use case:

- **LRU (Least Recently Used):** Default and most common
- **LFU (Least Frequently Used):** For data accessed in bursts
- **TTL-based:** Time-sensitive data

### Monitor Cache Performance

Track cache hit/miss ratios to optimize caching strategy:

```java
@Service
public class CacheMetricsService {

    @Autowired
    private CacheManager cacheManager;

    public Map<String, Object> getCacheStats() {
        Map<String, Object> stats = new HashMap<>();
        cacheManager.getCacheNames().forEach(cacheName -> {
            Cache cache = cacheManager.getCache(cacheName);
            if (cache instanceof RedisCache) {
                // Add custom metrics tracking
                stats.put(cacheName, "Cache statistics");
            }
        });
        return stats;
    }
}
```

## Testing Cache Implementation

### Integration Test with Testcontainers

```java
@SpringBootTest
@Testcontainers
class ProductServiceCacheTest {

    @Container
    static GenericContainer<?> redis = new GenericContainer<>("redis:7.4.2")
            .withExposedPorts(6379);

    @DynamicPropertySource
    static void redisProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.data.redis.host", redis::getHost);
        registry.add("spring.data.redis.port", redis::getFirstMappedPort);
    }

    @Autowired
    private ProductService productService;

    @Autowired
    private ProductRepository productRepository;

    @Test
    void testCaching() {
        Product product = new Product(1L, "Laptop", "Gaming", 1500.0);
        productRepository.save(product);

        // First call - database hit
        productService.getProductById(1L);

        // Second call - cache hit
        productService.getProductById(1L);

        // Verify only one database query was made
        verify(productRepository, times(1)).findById(1L);
    }
}
```

## Troubleshooting

### Common Issues and Solutions

**Connection Refused Error:**

- Verify Redis is running: `redis-cli ping`
- Check host and port configuration
- Ensure firewall allows port 6379

**Serialization Errors:**

- Ensure entities implement `Serializable`
- Configure appropriate serializer
- Check Jackson configuration for complex objects

**Cache Not Working:**

- Verify `@EnableCaching` is present
- Check cache manager bean is created
- Ensure method calls are external (not internal class calls)

**Memory Issues:**

- Set appropriate TTL values
- Configure max memory in Redis: `maxmemory 256mb`
- Set eviction policy: `maxmemory-policy allkeys-lru`

## Production Considerations

### Redis Configuration for Production

```properties
# Connection pool
spring.data.redis.lettuce.pool.max-active=20
spring.data.redis.lettuce.pool.max-idle=10
spring.data.redis.lettuce.pool.min-idle=5
spring.data.redis.lettuce.pool.max-wait=-1ms

# Timeout settings
spring.data.redis.timeout=60000

# Enable cluster mode (if using Redis Cluster)
spring.data.redis.cluster.nodes=node1:6379,node2:6379,node3:6379
```

### Use Redis Sentinel for High Availability

```java
@Bean
public RedisConnectionFactory redisConnectionFactory() {
    RedisSentinelConfiguration sentinelConfig = new RedisSentinelConfiguration()
            .master("mymaster")
            .sentinel("127.0.0.1", 26379)
            .sentinel("127.0.0.1", 26380);

    return new LettuceConnectionFactory(sentinelConfig);
}
```

### Security Best Practices

- Enable Redis authentication
- Use SSL/TLS for connections
- Implement proper access controls
- Never cache sensitive data without encryption

## Summary

This guide covered the complete implementation of Redis caching in Spring Boot, including:

- Project setup with required dependencies
- Redis server configuration (Docker and local)
- Cache manager configuration with custom TTL
- Implementation of cache annotations
- REST API integration
- Testing and verification
- Advanced configurations and best practices
- Production considerations

Redis caching significantly improves application performance by reducing database load and response times. Follow the best practices outlined to ensure efficient and reliable caching in your Spring Boot applications.
