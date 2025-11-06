# Spring Boot Core - Complete Interview Notes (Basics to Expert)

## Table of Contents

1. [Introduction to Spring Boot](#introduction)
2. [Core Concepts](#core-concepts)
3. [Dependency Injection & IoC](#dependency-injection)
4. [Spring Boot Annotations](#annotations)
5. [Bean Scopes & Lifecycle](#bean-scopes)
6. [Configuration & Properties](#configuration)
7. [REST API Development](#rest-api)
8. [Data Access with JPA](#data-access)
9. [Exception Handling](#exception-handling)
10. [Validation](#validation)
11. [Transaction Management](#transactions)
12. [AOP (Aspect-Oriented Programming)](#aop)
13. [Profiles & Environment Configuration](#profiles)
14. [Spring Boot Actuator](#actuator)
15. [Testing](#testing)
16. [Security & JWT](#security)
17. [Caching with Redis](#caching)
18. [Microservices Architecture](#microservices)
19. [Advanced Topics](#advanced-topics)
20. [Best Practices](#best-practices)

---

## 1. Introduction to Spring Boot {#introduction}

### What is Spring Boot?

Spring Boot is an extension of the Spring Framework that simplifies building production-ready Spring applications with minimal configuration. It provides auto-configuration, embedded servers, and starter dependencies.

### Key Features

- **Auto-Configuration**: Automatically configures beans based on classpath
- **Embedded Servers**: Built-in Tomcat, Jetty, or Undertow
- **Starter Dependencies**: Pre-configured dependency sets
- **Production-Ready Features**: Actuator for monitoring and metrics
- **No XML Configuration**: Annotation-based configuration

### Spring Boot vs Spring Framework

| Feature          | Spring Framework         | Spring Boot        |
| ---------------- | ------------------------ | ------------------ |
| Configuration    | XML or Java-based        | Auto-configuration |
| Server Setup     | External server required | Embedded server    |
| Dependencies     | Manual configuration     | Starter POMs       |
| Development Time | Longer                   | Faster             |
| Boilerplate Code | More                     | Less               |

### Basic Spring Boot Application

```java
@SpringBootApplication
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

**Explanation:**

- `@SpringBootApplication` combines three annotations:
  - `@SpringBootConfiguration`: Marks class as configuration source
  - `@EnableAutoConfiguration`: Enables auto-configuration
  - `@ComponentScan`: Scans for components in current package

---

## 2. Core Concepts {#core-concepts}

### Spring IoC Container

The IoC (Inversion of Control) Container manages object creation, dependency injection, and lifecycle. Instead of objects creating their dependencies, the container injects them.

**Types of IoC Containers:**

1. **BeanFactory**: Basic container with lazy initialization
2. **ApplicationContext**: Advanced container with eager initialization

```java
// ApplicationContext example
ApplicationContext context = new AnnotationConfigApplicationContext(AppConfig.class);
MyService service = context.getBean(MyService.class);
```

### Dependency Injection (DI)

DI is a design pattern where objects receive their dependencies from external sources rather than creating them.

**Types of DI:**

1. Constructor Injection (Recommended)
2. Setter Injection
3. Field Injection

---

## 3. Dependency Injection & IoC {#dependency-injection}

### Constructor Injection (Best Practice)

```java
@Service
public class UserService {
    private final UserRepository userRepository;

    // Constructor injection
    @Autowired // Optional in Spring 4.3+
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));
    }
}
```

**Advantages:**

- Immutable dependencies (final fields)
- Mandatory dependencies enforced
- Better testability
- Thread-safe

### Setter Injection

```java
@Service
public class EmailService {
    private MailSender mailSender;

    @Autowired
    public void setMailSender(MailSender mailSender) {
        this.mailSender = mailSender;
    }

    public void sendEmail(String to, String message) {
        mailSender.send(to, message);
    }
}
```

**Use Case:** Optional dependencies

### Field Injection (Not Recommended)

```java
@RestController
public class UserController {

    @Autowired
    private UserService userService; // Field injection

    @GetMapping("/users/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.findById(id);
    }
}
```

**Disadvantages:**

- Cannot create immutable objects
- Difficult to test
- Hidden dependencies

### Complete IoC Example

```java
// Interface
public interface MessageService {
    String getMessage();
}

// Implementation
@Component
public class EmailMessageService implements MessageService {
    @Override
    public String getMessage() {
        return "Email message";
    }
}

// Consumer
@Component
public class MessageProcessor {
    private final MessageService messageService;

    @Autowired
    public MessageProcessor(MessageService messageService) {
        this.messageService = messageService;
    }

    public void processMessage() {
        System.out.println(messageService.getMessage());
    }
}
```

---

## 4. Spring Boot Annotations {#annotations}

### Core Annotations

#### @SpringBootApplication

```java
@SpringBootApplication
// Equivalent to:
// @SpringBootConfiguration
// @EnableAutoConfiguration
// @ComponentScan
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

#### @Component, @Service, @Repository, @Controller

```java
// Generic component
@Component
public class MyComponent {
    // Business logic
}

// Service layer
@Service
public class UserService {
    // Business logic
}

// Data access layer
@Repository
public class UserRepository {
    // Database operations
}

// Web layer
@Controller
public class UserController {
    // Handle web requests
}
```

#### @RestController

```java
@RestController // @Controller + @ResponseBody
@RequestMapping("/api/users")
public class UserRestController {

    @GetMapping("/{id}")
    public ResponseEntity<User> getUserById(@PathVariable Long id) {
        User user = userService.findById(id);
        return ResponseEntity.ok(user);
    }

    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody @Valid User user) {
        User savedUser = userService.save(user);
        return ResponseEntity.status(HttpStatus.CREATED).body(savedUser);
    }
}
```

### Configuration Annotations

#### @Configuration and @Bean

```java
@Configuration
public class AppConfig {

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    @ConditionalOnProperty(name = "feature.enabled", havingValue = "true")
    public FeatureService featureService() {
        return new FeatureServiceImpl();
    }
}
```

### Request Mapping Annotations

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {

    @GetMapping
    public List<Product> getAllProducts() {
        return productService.findAll();
    }

    @GetMapping("/{id}")
    public Product getProduct(@PathVariable Long id) {
        return productService.findById(id);
    }

    @PostMapping
    public Product createProduct(@RequestBody Product product) {
        return productService.save(product);
    }

    @PutMapping("/{id}")
    public Product updateProduct(@PathVariable Long id, @RequestBody Product product) {
        return productService.update(id, product);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProduct(@PathVariable Long id) {
        productService.delete(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/search")
    public List<Product> searchProducts(@RequestParam String keyword) {
        return productService.search(keyword);
    }
}
```

### Parameter Annotations

```java
@RestController
@RequestMapping("/api/orders")
public class OrderController {

    // @PathVariable - Extract from URL path
    @GetMapping("/{orderId}/items/{itemId}")
    public OrderItem getOrderItem(
        @PathVariable Long orderId,
        @PathVariable Long itemId) {
        return orderService.getItem(orderId, itemId);
    }

    // @RequestParam - Extract from query string
    @GetMapping
    public List<Order> getOrders(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "10") int size,
        @RequestParam(required = false) String status) {
        return orderService.findAll(page, size, status);
    }

    // @RequestBody - Extract from request body
    @PostMapping
    public Order createOrder(@RequestBody @Valid Order order) {
        return orderService.create(order);
    }

    // @RequestHeader - Extract from HTTP headers
    @GetMapping("/user-orders")
    public List<Order> getUserOrders(
        @RequestHeader("Authorization") String token) {
        return orderService.findByUser(token);
    }
}
```

### Conditional Annotations

```java
@Configuration
public class ConditionalConfig {

    @Bean
    @ConditionalOnProperty(name = "feature.cache.enabled", havingValue = "true")
    public CacheManager cacheManager() {
        return new ConcurrentMapCacheManager();
    }

    @Bean
    @ConditionalOnMissingBean
    public DataSource dataSource() {
        return new HikariDataSource();
    }

    @Bean
    @ConditionalOnClass(name = "redis.clients.jedis.Jedis")
    public RedisTemplate redisTemplate() {
        return new RedisTemplate();
    }
}
```

---

## 5. Bean Scopes & Lifecycle {#bean-scopes}

### Bean Scopes

#### 1. Singleton (Default)

```java
@Component
@Scope("singleton") // or @Scope(ConfigurableBeanFactory.SCOPE_SINGLETON)
public class SingletonBean {
    // Single instance per Spring container
}
```

#### 2. Prototype

```java
@Component
@Scope("prototype") // or @Scope(ConfigurableBeanFactory.SCOPE_PROTOTYPE)
public class PrototypeBean {
    // New instance each time requested
}
```

#### 3. Request Scope (Web)

```java
@Component
@Scope(value = WebApplicationContext.SCOPE_REQUEST, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class RequestScopedBean {
    // New instance per HTTP request
}
```

#### 4. Session Scope (Web)

```java
@Component
@Scope(value = WebApplicationContext.SCOPE_SESSION, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class SessionScopedBean {
    // One instance per HTTP session
}
```

### Prototype in Singleton Issue

```java
// Problem: Prototype bean injected into Singleton
@Service
public class SingletonService {

    @Autowired
    private PrototypeBean prototypeBean; // Same instance always!

    public void doSomething() {
        prototypeBean.execute(); // Always same instance
    }
}

// Solution 1: Using ObjectFactory
@Service
public class SingletonService {

    @Autowired
    private ObjectFactory<PrototypeBean> prototypeBeanFactory;

    public void doSomething() {
        PrototypeBean bean = prototypeBeanFactory.getObject(); // New instance
        bean.execute();
    }
}

// Solution 2: Using Provider
@Service
public class SingletonService {

    @Autowired
    private Provider<PrototypeBean> prototypeBeanProvider;

    public void doSomething() {
        PrototypeBean bean = prototypeBeanProvider.get(); // New instance
        bean.execute();
    }
}

// Solution 3: ApplicationContext lookup
@Service
public class SingletonService {

    @Autowired
    private ApplicationContext context;

    public void doSomething() {
        PrototypeBean bean = context.getBean(PrototypeBean.class);
        bean.execute();
    }
}
```

### Bean Lifecycle

```java
@Component
public class LifecycleBean {

    // 1. Constructor
    public LifecycleBean() {
        System.out.println("1. Constructor called");
    }

    // 2. Post-construct
    @PostConstruct
    public void init() {
        System.out.println("2. @PostConstruct - Initialization");
    }

    // 3. Custom init method
    @Bean(initMethod = "customInit")
    public void customInit() {
        System.out.println("3. Custom init method");
    }

    // 4. Pre-destroy
    @PreDestroy
    public void cleanup() {
        System.out.println("4. @PreDestroy - Cleanup");
    }

    // 5. Custom destroy method
    @Bean(destroyMethod = "customDestroy")
    public void customDestroy() {
        System.out.println("5. Custom destroy method");
    }
}

// Alternative: Implement InitializingBean and DisposableBean
@Component
public class LifecycleBeanAlternative implements InitializingBean, DisposableBean {

    @Override
    public void afterPropertiesSet() throws Exception {
        System.out.println("InitializingBean.afterPropertiesSet()");
    }

    @Override
    public void destroy() throws Exception {
        System.out.println("DisposableBean.destroy()");
    }
}
```

---

## 6. Configuration & Properties {#configuration}

### application.properties

```properties
# Server Configuration
server.port=8080
server.servlet.context-path=/api

# Database Configuration
spring.datasource.url=jdbc:mysql://localhost:3306/mydb
spring.datasource.username=root
spring.datasource.password=password
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# JPA/Hibernate
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect
spring.jpa.properties.hibernate.format_sql=true

# Logging
logging.level.root=INFO
logging.level.com.example=DEBUG
logging.file.name=application.log
logging.pattern.console=%d{yyyy-MM-dd HH:mm:ss} - %msg%n

# Actuator
management.endpoints.web.exposure.include=*
management.endpoint.health.show-details=always

# Custom Properties
app.name=My Application
app.version=1.0.0
```

### application.yml

```yaml
server:
  port: 8080
  servlet:
    context-path: /api

spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mydb
    username: root
    password: password
    driver-class-name: com.mysql.cj.jdbc.Driver

  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    properties:
      hibernate:
        dialect: org.hibernate.dialect.MySQL8Dialect
        format_sql: true

logging:
  level:
    root: INFO
    com.example: DEBUG
  file:
    name: application.log

app:
  name: My Application
  version: 1.0.0
```

### @ConfigurationProperties

```java
@Configuration
@ConfigurationProperties(prefix = "app")
@Data
public class AppProperties {
    private String name;
    private String version;
    private Security security;

    @Data
    public static class Security {
        private String jwtSecret;
        private long jwtExpirationMs;
    }
}

// Usage
@Service
public class AppService {
    private final AppProperties appProperties;

    @Autowired
    public AppService(AppProperties appProperties) {
        this.appProperties = appProperties;
    }

    public String getAppInfo() {
        return appProperties.getName() + " v" + appProperties.getVersion();
    }
}
```

### @Value Annotation

```java
@Component
public class ConfigComponent {

    @Value("${server.port}")
    private int serverPort;

    @Value("${app.name:Default App}") // Default value
    private String appName;

    @Value("${app.features:feature1,feature2}") // List
    private List<String> features;

    @Value("#{${app.config}}") // Map
    private Map<String, String> config;

    // SpEL expressions
    @Value("#{systemProperties['user.home']}")
    private String userHome;

    @Value("#{T(java.lang.Math).random() * 100}")
    private double randomNumber;
}
```

---

## 7. REST API Development {#rest-api}

### Complete REST Controller Example

```java
@RestController
@RequestMapping("/api/v1/users")
@Validated
public class UserController {

    private final UserService userService;

    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // GET all users with pagination
    @GetMapping
    public ResponseEntity<Page<UserDTO>> getAllUsers(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "10") int size,
        @RequestParam(defaultValue = "id") String sortBy) {

        Pageable pageable = PageRequest.of(page, size, Sort.by(sortBy));
        Page<UserDTO> users = userService.findAll(pageable);
        return ResponseEntity.ok(users);
    }

    // GET single user
    @GetMapping("/{id}")
    public ResponseEntity<UserDTO> getUserById(@PathVariable Long id) {
        UserDTO user = userService.findById(id);
        return ResponseEntity.ok(user);
    }

    // POST create user
    @PostMapping
    public ResponseEntity<UserDTO> createUser(@Valid @RequestBody UserDTO userDTO) {
        UserDTO savedUser = userService.create(userDTO);
        URI location = ServletUriComponentsBuilder
            .fromCurrentRequest()
            .path("/{id}")
            .buildAndExpand(savedUser.getId())
            .toUri();
        return ResponseEntity.created(location).body(savedUser);
    }

    // PUT update user
    @PutMapping("/{id}")
    public ResponseEntity<UserDTO> updateUser(
        @PathVariable Long id,
        @Valid @RequestBody UserDTO userDTO) {
        UserDTO updatedUser = userService.update(id, userDTO);
        return ResponseEntity.ok(updatedUser);
    }

    // PATCH partial update
    @PatchMapping("/{id}")
    public ResponseEntity<UserDTO> partialUpdateUser(
        @PathVariable Long id,
        @RequestBody Map<String, Object> updates) {
        UserDTO updatedUser = userService.partialUpdate(id, updates);
        return ResponseEntity.ok(updatedUser);
    }

    // DELETE user
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        userService.delete(id);
        return ResponseEntity.noContent().build();
    }

    // Search users
    @GetMapping("/search")
    public ResponseEntity<List<UserDTO>> searchUsers(
        @RequestParam String keyword) {
        List<UserDTO> users = userService.search(keyword);
        return ResponseEntity.ok(users);
    }
}
```

### DTOs and Entity Mapping

```java
// Entity
@Entity
@Table(name = "users")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String username;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String password;

    @Column(name = "created_at")
    @CreationTimestamp
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    @UpdateTimestamp
    private LocalDateTime updatedAt;
}

// DTO
@Data
@NoArgsConstructor
@AllArgsConstructor
public class UserDTO {
    private Long id;

    @NotBlank(message = "Username is required")
    @Size(min = 3, max = 50)
    private String username;

    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;

    @NotBlank(message = "Password is required")
    @Size(min = 6, message = "Password must be at least 6 characters")
    private String password;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}

// Mapper
@Component
public class UserMapper {

    public UserDTO toDTO(User user) {
        if (user == null) return null;

        return new UserDTO(
            user.getId(),
            user.getUsername(),
            user.getEmail(),
            null, // Don't expose password
            user.getCreatedAt(),
            user.getUpdatedAt()
        );
    }

    public User toEntity(UserDTO dto) {
        if (dto == null) return null;

        User user = new User();
        user.setId(dto.getId());
        user.setUsername(dto.getUsername());
        user.setEmail(dto.getEmail());
        user.setPassword(dto.getPassword());
        return user;
    }
}
```

---

## 8. Data Access with JPA {#data-access}

### JPA Repository

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    // Query Method
    Optional<User> findByUsername(String username);

    Optional<User> findByEmail(String email);

    List<User> findByUsernameContaining(String keyword);

    boolean existsByEmail(String email);

    // @Query - JPQL
    @Query("SELECT u FROM User u WHERE u.email = :email")
    Optional<User> findUserByEmail(@Param("email") String email);

    @Query("SELECT u FROM User u WHERE u.username LIKE %:keyword% OR u.email LIKE %:keyword%")
    List<User> searchUsers(@Param("keyword") String keyword);

    // @Query - Native SQL
    @Query(value = "SELECT * FROM users WHERE created_at > :date", nativeQuery = true)
    List<User> findUsersCreatedAfter(@Param("date") LocalDateTime date);

    // Modifying queries
    @Modifying
    @Query("UPDATE User u SET u.email = :email WHERE u.id = :id")
    int updateUserEmail(@Param("id") Long id, @Param("email") String email);

    @Modifying
    @Query("DELETE FROM User u WHERE u.createdAt < :date")
    int deleteOldUsers(@Param("date") LocalDateTime date);

    // Pagination and Sorting
    Page<User> findAll(Pageable pageable);

    Page<User> findByUsernameContaining(String keyword, Pageable pageable);

    // Projections
    @Query("SELECT new com.example.dto.UserSummary(u.id, u.username, u.email) FROM User u")
    List<UserSummary> findAllUserSummaries();
}
```

### Service Layer

```java
@Service
@Transactional(readOnly = true)
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final UserMapper userMapper;

    @Autowired
    public UserService(UserRepository userRepository,
                      PasswordEncoder passwordEncoder,
                      UserMapper userMapper) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.userMapper = userMapper;
    }

    // Find all with pagination
    public Page<UserDTO> findAll(Pageable pageable) {
        return userRepository.findAll(pageable)
            .map(userMapper::toDTO);
    }

    // Find by ID
    public UserDTO findById(Long id) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User not found with id: " + id));
        return userMapper.toDTO(user);
    }

    // Create user
    @Transactional
    public UserDTO create(UserDTO userDTO) {
        // Check if email exists
        if (userRepository.existsByEmail(userDTO.getEmail())) {
            throw new DuplicateResourceException("Email already exists");
        }

        User user = userMapper.toEntity(userDTO);
        user.setPassword(passwordEncoder.encode(userDTO.getPassword()));
        User savedUser = userRepository.save(user);
        return userMapper.toDTO(savedUser);
    }

    // Update user
    @Transactional
    public UserDTO update(Long id, UserDTO userDTO) {
        User existingUser = userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        existingUser.setUsername(userDTO.getUsername());
        existingUser.setEmail(userDTO.getEmail());

        if (userDTO.getPassword() != null) {
            existingUser.setPassword(passwordEncoder.encode(userDTO.getPassword()));
        }

        User updatedUser = userRepository.save(existingUser);
        return userMapper.toDTO(updatedUser);
    }

    // Delete user
    @Transactional
    public void delete(Long id) {
        if (!userRepository.existsById(id)) {
            throw new ResourceNotFoundException("User not found");
        }
        userRepository.deleteById(id);
    }

    // Search users
    public List<UserDTO> search(String keyword) {
        return userRepository.searchUsers(keyword)
            .stream()
            .map(userMapper::toDTO)
            .collect(Collectors.toList());
    }
}
```

### Pagination and Sorting

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {

    @Autowired
    private ProductService productService;

    @GetMapping
    public ResponseEntity<Page<Product>> getProducts(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "10") int size,
        @RequestParam(defaultValue = "id") String sortBy,
        @RequestParam(defaultValue = "ASC") String sortDir) {

        Sort sort = sortDir.equalsIgnoreCase("ASC")
            ? Sort.by(sortBy).ascending()
            : Sort.by(sortBy).descending();

        Pageable pageable = PageRequest.of(page, size, sort);
        Page<Product> products = productService.findAll(pageable);

        return ResponseEntity.ok(products);
    }

    // Multiple sorting
    @GetMapping("/sorted")
    public ResponseEntity<Page<Product>> getSortedProducts(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "10") int size) {

        Sort sort = Sort.by(
            Sort.Order.desc("createdAt"),
            Sort.Order.asc("name")
        );

        Pageable pageable = PageRequest.of(page, size, sort);
        Page<Product> products = productService.findAll(pageable);

        return ResponseEntity.ok(products);
    }
}
```

---

## 9. Exception Handling {#exception-handling}

### Custom Exceptions

```java
// Base Exception
public class BusinessException extends RuntimeException {
    private String errorCode;

    public BusinessException(String message) {
        super(message);
    }

    public BusinessException(String message, String errorCode) {
        super(message);
        this.errorCode = errorCode;
    }
}

// Specific Exceptions
public class ResourceNotFoundException extends BusinessException {
    public ResourceNotFoundException(String message) {
        super(message, "RESOURCE_NOT_FOUND");
    }
}

public class DuplicateResourceException extends BusinessException {
    public DuplicateResourceException(String message) {
        super(message, "DUPLICATE_RESOURCE");
    }
}

public class InvalidRequestException extends BusinessException {
    public InvalidRequestException(String message) {
        super(message, "INVALID_REQUEST");
    }
}
```

### Error Response DTO

```java
@Data
@AllArgsConstructor
@NoArgsConstructor
public class ErrorResponse {
    private LocalDateTime timestamp;
    private int status;
    private String error;
    private String message;
    private String path;
    private Map<String, String> validationErrors;

    public ErrorResponse(LocalDateTime timestamp, int status, String error,
                        String message, String path) {
        this.timestamp = timestamp;
        this.status = status;
        this.error = error;
        this.message = message;
        this.path = path;
    }
}
```

### Global Exception Handler

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    // Handle Resource Not Found
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFoundException(
        ResourceNotFoundException ex, WebRequest request) {

        ErrorResponse error = new ErrorResponse(
            LocalDateTime.now(),
            HttpStatus.NOT_FOUND.value(),
            "Not Found",
            ex.getMessage(),
            request.getDescription(false).replace("uri=", "")
        );

        return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
    }

    // Handle Duplicate Resource
    @ExceptionHandler(DuplicateResourceException.class)
    public ResponseEntity<ErrorResponse> handleDuplicateResourceException(
        DuplicateResourceException ex, WebRequest request) {

        ErrorResponse error = new ErrorResponse(
            LocalDateTime.now(),
            HttpStatus.CONFLICT.value(),
            "Conflict",
            ex.getMessage(),
            request.getDescription(false).replace("uri=", "")
        );

        return new ResponseEntity<>(error, HttpStatus.CONFLICT);
    }

    // Handle Validation Errors
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(
        MethodArgumentNotValidException ex, WebRequest request) {

        Map<String, String> validationErrors = new HashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(error ->
            validationErrors.put(error.getField(), error.getDefaultMessage())
        );

        ErrorResponse error = new ErrorResponse(
            LocalDateTime.now(),
            HttpStatus.BAD_REQUEST.value(),
            "Validation Failed",
            "Input validation failed",
            request.getDescription(false).replace("uri=", "")
        );
        error.setValidationErrors(validationErrors);

        return new ResponseEntity<>(error, HttpStatus.BAD_REQUEST);
    }

    // Handle Constraint Violations
    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<ErrorResponse> handleConstraintViolationException(
        ConstraintViolationException ex, WebRequest request) {

        Map<String, String> violations = new HashMap<>();
        ex.getConstraintViolations().forEach(violation ->
            violations.put(
                violation.getPropertyPath().toString(),
                violation.getMessage()
            )
        );

        ErrorResponse error = new ErrorResponse(
            LocalDateTime.now(),
            HttpStatus.BAD_REQUEST.value(),
            "Constraint Violation",
            "Validation constraints violated",
            request.getDescription(false).replace("uri=", "")
        );
        error.setValidationErrors(violations);

        return new ResponseEntity<>(error, HttpStatus.BAD_REQUEST);
    }

    // Handle Generic Exceptions
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGlobalException(
        Exception ex, WebRequest request) {

        ErrorResponse error = new ErrorResponse(
            LocalDateTime.now(),
            HttpStatus.INTERNAL_SERVER_ERROR.value(),
            "Internal Server Error",
            ex.getMessage(),
            request.getDescription(false).replace("uri=", "")
        );

        return new ResponseEntity<>(error, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
```

---

## 10. Validation {#validation}

### Bean Validation Annotations

```java
@Data
@NoArgsConstructor
@AllArgsConstructor
public class UserRegistrationDTO {

    @NotBlank(message = "Username is required")
    @Size(min = 3, max = 50, message = "Username must be between 3 and 50 characters")
    @Pattern(regexp = "^[a-zA-Z0-9_]+$", message = "Username can only contain letters, numbers, and underscores")
    private String username;

    @NotBlank(message = "Email is required")
    @Email(message = "Email should be valid")
    private String email;

    @NotBlank(message = "Password is required")
    @Size(min = 8, message = "Password must be at least 8 characters")
    @Pattern(
        regexp = "^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$",
        message = "Password must contain at least one digit, one lowercase, one uppercase, and one special character"
    )
    private String password;

    @NotNull(message = "Age is required")
    @Min(value = 18, message = "Age must be at least 18")
    @Max(value = 100, message = "Age must be less than 100")
    private Integer age;

    @NotBlank(message = "Phone number is required")
    @Pattern(regexp = "^\\d{10}$", message = "Phone number must be 10 digits")
    private String phoneNumber;

    @NotNull(message = "Date of birth is required")
    @Past(message = "Date of birth must be in the past")
    private LocalDate dateOfBirth;

    @NotEmpty(message = "At least one role is required")
    private List<@NotBlank String> roles;

    @Valid
    private AddressDTO address;
}

@Data
public class AddressDTO {
    @NotBlank(message = "Street is required")
    private String street;

    @NotBlank(message = "City is required")
    private String city;

    @NotBlank(message = "State is required")
    private String state;

    @NotBlank(message = "Zip code is required")
    @Pattern(regexp = "^\\d{5}$", message = "Zip code must be 5 digits")
    private String zipCode;
}
```

### Custom Validators

```java
// Custom annotation
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = UniqueEmailValidator.class)
@Documented
public @interface UniqueEmail {
    String message() default "Email already exists";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

// Validator implementation
@Component
public class UniqueEmailValidator implements ConstraintValidator<UniqueEmail, String> {

    @Autowired
    private UserRepository userRepository;

    @Override
    public boolean isValid(String email, ConstraintValidatorContext context) {
        if (email == null) return true;
        return !userRepository.existsByEmail(email);
    }
}

// Usage
@Data
public class UserDTO {
    @NotBlank
    @Email
    @UniqueEmail
    private String email;
}
```

### Validation Groups

```java
// Marker interfaces for groups
public interface OnCreate {}
public interface OnUpdate {}

@Data
public class UserDTO {
    @Null(groups = OnCreate.class, message = "ID must be null when creating")
    @NotNull(groups = OnUpdate.class, message = "ID is required when updating")
    private Long id;

    @NotBlank(groups = {OnCreate.class, OnUpdate.class})
    private String username;

    @NotBlank(groups = OnCreate.class, message = "Password is required")
    @Null(groups = OnUpdate.class, message = "Password cannot be updated this way")
    private String password;
}

// Controller usage
@RestController
@RequestMapping("/api/users")
@Validated
public class UserController {

    @PostMapping
    public ResponseEntity<UserDTO> createUser(
        @Validated(OnCreate.class) @RequestBody UserDTO userDTO) {
        return ResponseEntity.ok(userService.create(userDTO));
    }

    @PutMapping("/{id}")
    public ResponseEntity<UserDTO> updateUser(
        @PathVariable Long id,
        @Validated(OnUpdate.class) @RequestBody UserDTO userDTO) {
        return ResponseEntity.ok(userService.update(id, userDTO));
    }
}
```

---

## 11. Transaction Management {#transactions}

### @Transactional Annotation

```java
@Service
public class BankingService {

    @Autowired
    private AccountRepository accountRepository;

    @Autowired
    private TransactionRepository transactionRepository;

    // Default transaction
    @Transactional
    public void transferMoney(Long fromAccountId, Long toAccountId, BigDecimal amount) {
        Account fromAccount = accountRepository.findById(fromAccountId)
            .orElseThrow(() -> new ResourceNotFoundException("Account not found"));

        Account toAccount = accountRepository.findById(toAccountId)
            .orElseThrow(() -> new ResourceNotFoundException("Account not found"));

        // Debit from source
        fromAccount.setBalance(fromAccount.getBalance().subtract(amount));
        accountRepository.save(fromAccount);

        // Credit to destination
        toAccount.setBalance(toAccount.getBalance().add(amount));
        accountRepository.save(toAccount);

        // Record transaction
        Transaction transaction = new Transaction(fromAccountId, toAccountId, amount);
        transactionRepository.save(transaction);
    }

    // Read-only transaction (optimization)
    @Transactional(readOnly = true)
    public List<Account> getAllAccounts() {
        return accountRepository.findAll();
    }

    // Custom timeout
    @Transactional(timeout = 5) // 5 seconds
    public void processLongRunningTask() {
        // Long operation
    }

    // Custom isolation level
    @Transactional(isolation = Isolation.SERIALIZABLE)
    public void criticalOperation() {
        // Critical transaction
    }

    // Custom propagation
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void independentTransaction() {
        // This always runs in a new transaction
    }

    // Custom rollback rules
    @Transactional(
        rollbackFor = Exception.class,
        noRollbackFor = IgnorableException.class
    )
    public void customRollback() {
        // Rolls back on all exceptions except IgnorableException
    }
}
```

### Transaction Propagation

```java
@Service
public class OrderService {

    @Autowired
    private PaymentService paymentService;

    @Autowired
    private NotificationService notificationService;

    // REQUIRED (default) - Join existing or create new
    @Transactional(propagation = Propagation.REQUIRED)
    public void createOrder(Order order) {
        orderRepository.save(order);
        paymentService.processPayment(order); // Joins this transaction
    }

    // REQUIRES_NEW - Always create new transaction
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void auditLog(String message) {
        // This runs in separate transaction
        // Commits even if parent transaction fails
        auditRepository.save(new AuditLog(message));
    }

    // NESTED - Create nested transaction
    @Transactional(propagation = Propagation.NESTED)
    public void processOrderItems(Order order) {
        // Can rollback independently of parent
        for (OrderItem item : order.getItems()) {
            processItem(item);
        }
    }

    // MANDATORY - Must run within existing transaction
    @Transactional(propagation = Propagation.MANDATORY)
    public void updateOrderStatus(Long orderId, OrderStatus status) {
        // Throws exception if no transaction exists
        Order order = orderRepository.findById(orderId).orElseThrow();
        order.setStatus(status);
        orderRepository.save(order);
    }

    // NOT_SUPPORTED - Suspend current transaction
    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public void sendNotification(String message) {
        // Runs without transaction
        notificationService.send(message);
    }

    // NEVER - Must not run in transaction
    @Transactional(propagation = Propagation.NEVER)
    public void externalApiCall() {
        // Throws exception if transaction exists
        externalApi.call();
    }
}
```

### Programmatic Transaction Management

```java
@Service
public class ManualTransactionService {

    @Autowired
    private PlatformTransactionManager transactionManager;

    public void manualTransactionControl() {
        TransactionDefinition def = new DefaultTransactionDefinition();
        TransactionStatus status = transactionManager.getTransaction(def);

        try {
            // Business logic
            performOperation1();
            performOperation2();

            // Commit transaction
            transactionManager.commit(status);
        } catch (Exception ex) {
            // Rollback on error
            transactionManager.rollback(status);
            throw ex;
        }
    }

    // Using TransactionTemplate
    @Autowired
    private TransactionTemplate transactionTemplate;

    public void usingTransactionTemplate() {
        transactionTemplate.execute(status -> {
            try {
                performOperation1();
                performOperation2();
                return null;
            } catch (Exception ex) {
                status.setRollbackOnly();
                throw ex;
            }
        });
    }
}
```

---

## 12. AOP (Aspect-Oriented Programming) {#aop}

### Enable AOP

```java
@Configuration
@EnableAspectJAutoProxy
public class AopConfig {
    // AOP configuration
}
```

### Aspect Example

```java
@Aspect
@Component
public class LoggingAspect {

    private static final Logger logger = LoggerFactory.getLogger(LoggingAspect.class);

    // Pointcut for all methods in service package
    @Pointcut("execution(* com.example.service.*.*(..))")
    public void serviceMethods() {}

    // Before advice
    @Before("serviceMethods()")
    public void logBefore(JoinPoint joinPoint) {
        logger.info("Executing: " + joinPoint.getSignature().getName());
        logger.info("Arguments: " + Arrays.toString(joinPoint.getArgs()));
    }

    // After returning advice
    @AfterReturning(pointcut = "serviceMethods()", returning = "result")
    public void logAfterReturning(JoinPoint joinPoint, Object result) {
        logger.info("Method executed successfully: " + joinPoint.getSignature().getName());
        logger.info("Return value: " + result);
    }

    // After throwing advice
    @AfterThrowing(pointcut = "serviceMethods()", throwing = "exception")
    public void logAfterThrowing(JoinPoint joinPoint, Exception exception) {
        logger.error("Exception in method: " + joinPoint.getSignature().getName());
        logger.error("Exception: " + exception.getMessage());
    }

    // After (finally) advice
    @After("serviceMethods()")
    public void logAfter(JoinPoint joinPoint) {
        logger.info("Method completed: " + joinPoint.getSignature().getName());
    }

    // Around advice
    @Around("serviceMethods()")
    public Object logAround(ProceedingJoinPoint joinPoint) throws Throwable {
        long startTime = System.currentTimeMillis();

        logger.info("Starting method: " + joinPoint.getSignature().getName());

        Object result = null;
        try {
            result = joinPoint.proceed(); // Execute actual method
            return result;
        } finally {
            long endTime = System.currentTimeMillis();
            logger.info("Method executed in: " + (endTime - startTime) + "ms");
        }
    }
}
```

### Performance Monitoring Aspect

```java
@Aspect
@Component
public class PerformanceMonitoringAspect {

    private static final Logger logger = LoggerFactory.getLogger(PerformanceMonitoringAspect.class);

    @Around("@annotation(com.example.annotation.MonitorPerformance)")
    public Object monitorPerformance(ProceedingJoinPoint joinPoint) throws Throwable {
        long startTime = System.currentTimeMillis();
        String methodName = joinPoint.getSignature().getName();

        try {
            Object result = joinPoint.proceed();
            long endTime = System.currentTimeMillis();
            long executionTime = endTime - startTime;

            logger.info("Method: {} executed in {} ms", methodName, executionTime);

            if (executionTime > 1000) {
                logger.warn("Method: {} took longer than 1 second", methodName);
            }

            return result;
        } catch (Exception ex) {
            logger.error("Exception in method: {}", methodName, ex);
            throw ex;
        }
    }
}

// Custom annotation
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface MonitorPerformance {
}

// Usage
@Service
public class UserService {

    @MonitorPerformance
    public User findById(Long id) {
        return userRepository.findById(id).orElseThrow();
    }
}
```

### Security Aspect

```java
@Aspect
@Component
public class SecurityAspect {

    @Before("@annotation(requiresRole)")
    public void checkRole(RequiresRole requiresRole) {
        String requiredRole = requiresRole.value();
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();

        boolean hasRole = authentication.getAuthorities().stream()
            .anyMatch(authority -> authority.getAuthority().equals(requiredRole));

        if (!hasRole) {
            throw new AccessDeniedException("User does not have required role: " + requiredRole);
        }
    }
}

// Custom annotation
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface RequiresRole {
    String value();
}

// Usage
@Service
public class AdminService {

    @RequiresRole("ROLE_ADMIN")
    public void deleteUser(Long userId) {
        userRepository.deleteById(userId);
    }
}
```

---

## 13. Profiles & Environment Configuration {#profiles}

### Profile-Specific Properties

```
application.properties
application-dev.properties
application-test.properties
application-prod.properties
```

**application.properties**

```properties
spring.profiles.active=dev
```

**application-dev.properties**

```properties
server.port=8080
spring.datasource.url=jdbc:mysql://localhost:3306/dev_db
logging.level.root=DEBUG
```

**application-prod.properties**

```properties
server.port=80
spring.datasource.url=jdbc:mysql://prod-server:3306/prod_db
logging.level.root=ERROR
```

### Profile-Specific Beans

```java
@Configuration
public class DataSourceConfig {

    @Bean
    @Profile("dev")
    public DataSource devDataSource() {
        HikariDataSource dataSource = new HikariDataSource();
        dataSource.setJdbcUrl("jdbc:h2:mem:devdb");
        return dataSource;
    }

    @Bean
    @Profile("prod")
    public DataSource prodDataSource() {
        HikariDataSource dataSource = new HikariDataSource();
        dataSource.setJdbcUrl("jdbc:mysql://prod-server:3306/proddb");
        dataSource.setMaximumPoolSize(20);
        return dataSource;
    }

    @Bean
    @Profile("test")
    public DataSource testDataSource() {
        return new EmbeddedDatabaseBuilder()
            .setType(EmbeddedDatabaseType.H2)
            .build();
    }
}
```

### Component-Level Profiles

```java
@Service
@Profile("dev")
public class MockEmailService implements EmailService {
    @Override
    public void sendEmail(String to, String message) {
        System.out.println("Mock email sent to: " + to);
    }
}

@Service
@Profile("prod")
public class RealEmailService implements EmailService {
    @Override
    public void sendEmail(String to, String message) {
        // Real email sending logic
    }
}
```

### Activating Profiles

```bash
# Command line
java -jar app.jar --spring.profiles.active=prod

# Environment variable
export SPRING_PROFILES_ACTIVE=prod

# application.properties
spring.profiles.active=dev

# Programmatically
SpringApplication app = new SpringApplication(Application.class);
app.setAdditionalProfiles("dev");
app.run(args);
```

---

## 14. Spring Boot Actuator {#actuator}

### Enable Actuator

**pom.xml**

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

### Actuator Configuration

**application.properties**

```properties
# Expose all endpoints
management.endpoints.web.exposure.include=*

# Expose specific endpoints
management.endpoints.web.exposure.include=health,info,metrics

# Show detailed health information
management.endpoint.health.show-details=always

# Custom base path
management.endpoints.web.base-path=/actuator

# Enable/disable specific endpoints
management.endpoint.shutdown.enabled=true
```

### Built-in Endpoints

```
/actuator/health - Application health information
/actuator/info - Application information
/actuator/metrics - Application metrics
/actuator/env - Environment properties
/actuator/loggers - Logger configuration
/actuator/beans - All Spring beans
/actuator/mappings - All @RequestMapping paths
/actuator/threaddump - Thread dump
/actuator/heapdump - Heap dump
/actuator/shutdown - Graceful shutdown (POST)
```

### Custom Health Indicator

```java
@Component
public class CustomHealthIndicator implements HealthIndicator {

    @Override
    public Health health() {
        try {
            // Check custom health logic
            boolean isHealthy = checkCustomService();

            if (isHealthy) {
                return Health.up()
                    .withDetail("Custom Service", "Available")
                    .withDetail("Timestamp", LocalDateTime.now())
                    .build();
            } else {
                return Health.down()
                    .withDetail("Custom Service", "Unavailable")
                    .withDetail("Error", "Service check failed")
                    .build();
            }
        } catch (Exception ex) {
            return Health.down()
                .withDetail("Error", ex.getMessage())
                .build();
        }
    }

    private boolean checkCustomService() {
        // Custom health check logic
        return true;
    }
}
```

### Custom Info Contributor

```java
@Component
public class CustomInfoContributor implements InfoContributor {

    @Override
    public void contribute(Info.Builder builder) {
        Map<String, Object> customInfo = new HashMap<>();
        customInfo.put("app-version", "1.0.0");
        customInfo.put("build-time", LocalDateTime.now());
        customInfo.put("developer", "John Doe");

        builder.withDetail("custom-info", customInfo);
    }
}
```

### Custom Metrics

```java
@Service
public class UserService {

    private final MeterRegistry meterRegistry;
    private Counter userCreationCounter;
    private Timer userCreationTimer;

    @Autowired
    public UserService(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;

        // Counter
        this.userCreationCounter = Counter.builder("user.creation.count")
            .description("Number of users created")
            .tag("type", "registration")
            .register(meterRegistry);

        // Timer
        this.userCreationTimer = Timer.builder("user.creation.time")
            .description("Time taken to create user")
            .register(meterRegistry);
    }

    public User createUser(UserDTO userDTO) {
        return userCreationTimer.record(() -> {
            User user = userMapper.toEntity(userDTO);
            User savedUser = userRepository.save(user);
            userCreationCounter.increment();
            return savedUser;
        });
    }

    // Gauge example
    @PostConstruct
    public void registerGauges() {
        Gauge.builder("user.active.count", userRepository, UserRepository::countActiveUsers)
            .description("Number of active users")
            .register(meterRegistry);
    }
}
```

---

## 15. Testing {#testing}

### Unit Testing with JUnit 5 and Mockito

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @Mock
    private UserMapper userMapper;

    @InjectMocks
    private UserService userService;

    @Test
    void testFindById_Success() {
        // Arrange
        Long userId = 1L;
        User user = new User(userId, "john", "john@example.com", "password");
        UserDTO userDTO = new UserDTO(userId, "john", "john@example.com", null);

        when(userRepository.findById(userId)).thenReturn(Optional.of(user));
        when(userMapper.toDTO(user)).thenReturn(userDTO);

        // Act
        UserDTO result = userService.findById(userId);

        // Assert
        assertNotNull(result);
        assertEquals(userId, result.getId());
        assertEquals("john", result.getUsername());

        verify(userRepository).findById(userId);
        verify(userMapper).toDTO(user);
    }

    @Test
    void testFindById_NotFound() {
        // Arrange
        Long userId = 1L;
        when(userRepository.findById(userId)).thenReturn(Optional.empty());

        // Act & Assert
        assertThrows(ResourceNotFoundException.class, () -> {
            userService.findById(userId);
        });

        verify(userRepository).findById(userId);
    }

    @Test
    void testCreateUser_Success() {
        // Arrange
        UserDTO userDTO = new UserDTO(null, "john", "john@example.com", "password123");
        User user = new User(null, "john", "john@example.com", "encodedPassword");
        User savedUser = new User(1L, "john", "john@example.com", "encodedPassword");
        UserDTO savedUserDTO = new UserDTO(1L, "john", "john@example.com", null);

        when(userRepository.existsByEmail(userDTO.getEmail())).thenReturn(false);
        when(userMapper.toEntity(userDTO)).thenReturn(user);
        when(passwordEncoder.encode(userDTO.getPassword())).thenReturn("encodedPassword");
        when(userRepository.save(user)).thenReturn(savedUser);
        when(userMapper.toDTO(savedUser)).thenReturn(savedUserDTO);

        // Act
        UserDTO result = userService.create(userDTO);

        // Assert
        assertNotNull(result);
        assertEquals(1L, result.getId());

        verify(userRepository).existsByEmail(userDTO.getEmail());
        verify(passwordEncoder).encode(userDTO.getPassword());
        verify(userRepository).save(user);
    }
}
```

### Integration Testing with @SpringBootTest

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
@AutoConfigureTestDatabase
class UserControllerIntegrationTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Autowired
    private UserRepository userRepository;

    @BeforeEach
    void setUp() {
        userRepository.deleteAll();
    }

    @Test
    void testCreateUser_Success() {
        // Arrange
        UserDTO userDTO = new UserDTO(null, "john", "john@example.com", "password123");

        // Act
        ResponseEntity<UserDTO> response = restTemplate.postForEntity(
            "/api/v1/users",
            userDTO,
            UserDTO.class
        );

        // Assert
        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody());
        assertNotNull(response.getBody().getId());
        assertEquals("john", response.getBody().getUsername());
    }

    @Test
    void testGetUser_Success() {
        // Arrange
        User user = new User(null, "john", "john@example.com", "password");
        User savedUser = userRepository.save(user);

        // Act
        ResponseEntity<UserDTO> response = restTemplate.getForEntity(
            "/api/v1/users/" + savedUser.getId(),
            UserDTO.class
        );

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(savedUser.getId(), response.getBody().getId());
    }

    @Test
    void testGetUser_NotFound() {
        // Act
        ResponseEntity<ErrorResponse> response = restTemplate.getForEntity(
            "/api/v1/users/999",
            ErrorResponse.class
        );

        // Assert
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }
}
```

### Controller Testing with @WebMvcTest

```java
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void testGetUserById_Success() throws Exception {
        // Arrange
        Long userId = 1L;
        UserDTO userDTO = new UserDTO(userId, "john", "john@example.com", null);

        when(userService.findById(userId)).thenReturn(userDTO);

        // Act & Assert
        mockMvc.perform(get("/api/v1/users/{id}", userId))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(userId))
            .andExpect(jsonPath("$.username").value("john"))
            .andExpect(jsonPath("$.email").value("john@example.com"));

        verify(userService).findById(userId);
    }

    @Test
    void testCreateUser_Success() throws Exception {
        // Arrange
        UserDTO userDTO = new UserDTO(null, "john", "john@example.com", "password123");
        UserDTO savedUserDTO = new UserDTO(1L, "john", "john@example.com", null);

        when(userService.create(any(UserDTO.class))).thenReturn(savedUserDTO);

        // Act & Assert
        mockMvc.perform(post("/api/v1/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(userDTO)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(1L))
            .andExpect(jsonPath("$.username").value("john"));

        verify(userService).create(any(UserDTO.class));
    }

    @Test
    void testCreateUser_ValidationError() throws Exception {
        // Arrange - Invalid user (empty username)
        UserDTO userDTO = new UserDTO(null, "", "john@example.com", "password123");

        // Act & Assert
        mockMvc.perform(post("/api/v1/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(userDTO)))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.validationErrors.username").exists());
    }
}
```

### Repository Testing with @DataJpaTest

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class UserRepositoryTest {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private TestEntityManager entityManager;

    @Test
    void testFindByEmail_Success() {
        // Arrange
        User user = new User(null, "john", "john@example.com", "password");
        entityManager.persist(user);
        entityManager.flush();

        // Act
        Optional<User> found = userRepository.findByEmail("john@example.com");

        // Assert
        assertTrue(found.isPresent());
        assertEquals("john", found.get().getUsername());
    }

    @Test
    void testExistsByEmail() {
        // Arrange
        User user = new User(null, "john", "john@example.com", "password");
        entityManager.persist(user);
        entityManager.flush();

        // Act
        boolean exists = userRepository.existsByEmail("john@example.com");

        // Assert
        assertTrue(exists);
    }

    @Test
    void testFindByUsernameContaining() {
        // Arrange
        entityManager.persist(new User(null, "john_doe", "john@example.com", "pass"));
        entityManager.persist(new User(null, "jane_doe", "jane@example.com", "pass"));
        entityManager.persist(new User(null, "bob_smith", "bob@example.com", "pass"));
        entityManager.flush();

        // Act
        List<User> users = userRepository.findByUsernameContaining("doe");

        // Assert
        assertEquals(2, users.size());
    }
}
```

---

## 16. Security & JWT {#security}

### Spring Security Dependencies

**pom.xml**

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-api</artifactId>
    <version>0.11.5</version>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-impl</artifactId>
    <version>0.11.5</version>
    <scope>runtime</scope>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-jackson</artifactId>
    <version>0.11.5</version>
    <scope>runtime</scope>
</dependency>
```

### JWT Utility

```java
@Component
public class JwtUtils {

    @Value("${jwt.secret}")
    private String jwtSecret;

    @Value("${jwt.expiration}")
    private long jwtExpirationMs;

    public String generateToken(UserDetails userDetails) {
        Map<String, Object> claims = new HashMap<>();
        claims.put("roles", userDetails.getAuthorities());

        return Jwts.builder()
            .setClaims(claims)
            .setSubject(userDetails.getUsername())
            .setIssuedAt(new Date())
            .setExpiration(new Date(System.currentTimeMillis() + jwtExpirationMs))
            .signWith(SignatureAlgorithm.HS512, jwtSecret)
            .compact();
    }

    public String getUsernameFromToken(String token) {
        return Jwts.parser()
            .setSigningKey(jwtSecret)
            .parseClaimsJws(token)
            .getBody()
            .getSubject();
    }

    public boolean validateToken(String token) {
        try {
            Jwts.parser().setSigningKey(jwtSecret).parseClaimsJws(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }
}
```

### JWT Authentication Filter

```java
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    @Autowired
    private JwtUtils jwtUtils;

    @Autowired
    private UserDetailsService userDetailsService;

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                   HttpServletResponse response,
                                   FilterChain filterChain) throws ServletException, IOException {
        try {
            String jwt = getJwtFromRequest(request);

            if (jwt != null && jwtUtils.validateToken(jwt)) {
                String username = jwtUtils.getUsernameFromToken(jwt);
                UserDetails userDetails = userDetailsService.loadUserByUsername(username);

                UsernamePasswordAuthenticationToken authentication =
                    new UsernamePasswordAuthenticationToken(
                        userDetails, null, userDetails.getAuthorities());

                authentication.setDetails(new WebAuthenticationDetailsSource()
                    .buildDetails(request));

                SecurityContextHolder.getContext().setAuthentication(authentication);
            }
        } catch (Exception ex) {
            logger.error("Cannot set user authentication", ex);
        }

        filterChain.doFilter(request, response);
    }

    private String getJwtFromRequest(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (StringUtils.hasText(bearerToken) && bearerToken.startsWith("Bearer ")) {
            return bearerToken.substring(7);
        }
        return null;
    }
}
```

### Security Configuration

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    @Autowired
    private JwtAuthenticationFilter jwtAuthenticationFilter;

    @Autowired
    private AuthenticationEntryPoint authenticationEntryPoint;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .exceptionHandling(exception ->
                exception.authenticationEntryPoint(authenticationEntryPoint))
            .sessionManagement(session ->
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            );

        http.addFilterBefore(jwtAuthenticationFilter,
            UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(
        AuthenticationConfiguration authenticationConfiguration) throws Exception {
        return authenticationConfiguration.getAuthenticationManager();
    }
}
```

### Authentication Controller

```java
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private UserService userService;

    @Autowired
    private JwtUtils jwtUtils;

    @PostMapping("/login")
    public ResponseEntity<JwtResponse> authenticateUser(@Valid @RequestBody LoginRequest loginRequest) {
        Authentication authentication = authenticationManager.authenticate(
            new UsernamePasswordAuthenticationToken(
                loginRequest.getUsername(),
                loginRequest.getPassword()
            )
        );

        SecurityContextHolder.getContext().setAuthentication(authentication);

        UserDetails userDetails = (UserDetails) authentication.getPrincipal();
        String jwt = jwtUtils.generateToken(userDetails);

        return ResponseEntity.ok(new JwtResponse(jwt));
    }

    @PostMapping("/register")
    public ResponseEntity<UserDTO> registerUser(@Valid @RequestBody UserRegistrationDTO registrationDTO) {
        UserDTO user = userService.register(registrationDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }
}
```

### Method-Level Security

```java
@Service
public class UserService {

    @PreAuthorize("hasRole('ADMIN')")
    public void deleteUser(Long userId) {
        userRepository.deleteById(userId);
    }

    @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
    public User getCurrentUser() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        String username = authentication.getName();
        return userRepository.findByUsername(username).orElseThrow();
    }

    @PreAuthorize("#userId == authentication.principal.id or hasRole('ADMIN')")
    public User updateUser(Long userId, UserDTO userDTO) {
        // Only allow users to update their own profile or admins
        return userRepository.save(userMapper.toEntity(userDTO));
    }

    @PostAuthorize("returnObject.username == authentication.principal.username")
    public User getUserProfile(Long userId) {
        return userRepository.findById(userId).orElseThrow();
    }
}
```

---

## 17. Caching with Redis {#caching}

### Redis Dependencies

**pom.xml**

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-cache</artifactId>
</dependency>
```

### Redis Configuration

```java
@Configuration
@EnableCaching
public class RedisConfig {

    @Bean
    public RedisCacheManager cacheManager(RedisConnectionFactory connectionFactory) {
        RedisCacheConfiguration config = RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(10))
            .disableCachingNullValues()
            .serializeValuesWith(
                RedisSerializationContext.SerializationPair.fromSerializer(
                    new GenericJackson2JsonRedisSerializer()
                )
            );

        return RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(config)
            .build();
    }

    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory connectionFactory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(connectionFactory);

        Jackson2JsonRedisSerializer<Object> serializer = new Jackson2JsonRedisSerializer<>(Object.class);
        ObjectMapper mapper = new ObjectMapper();
        mapper.setVisibility(PropertyAccessor.ALL, JsonAutoDetect.Visibility.ANY);
        mapper.activateDefaultTyping(
            mapper.getPolymorphicTypeValidator(),
            ObjectMapper.DefaultTyping.NON_FINAL
        );
        serializer.setObjectMapper(mapper);

        template.setKeySerializer(new StringRedisSerializer());
        template.setValueSerializer(serializer);
        template.setHashKeySerializer(new StringRedisSerializer());
        template.setHashValueSerializer(serializer);

        template.afterPropertiesSet();
        return template;
    }
}
```

### Caching Annotations

```java
@Service
public class ProductService {

    @Autowired
    private ProductRepository productRepository;

    // Cache result
    @Cacheable(value = "products", key = "#id")
    public Product findById(Long id) {
        System.out.println("Fetching from database...");
        return productRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Product not found"));
    }

    // Cache all results
    @Cacheable(value = "products", key = "'all'")
    public List<Product> findAll() {
        return productRepository.findAll();
    }

    // Update cache after save
    @CachePut(value = "products", key = "#result.id")
    public Product save(Product product) {
        return productRepository.save(product);
    }

    // Evict specific cache entry
    @CacheEvict(value = "products", key = "#id")
    public void delete(Long id) {
        productRepository.deleteById(id);
    }

    // Evict all cache entries
    @CacheEvict(value = "products", allEntries = true)
    public void deleteAll() {
        productRepository.deleteAll();
    }

    // Multiple cache operations
    @Caching(
        cacheable = @Cacheable(value = "products", key = "#id"),
        evict = @CacheEvict(value = "products", key = "'all'")
    )
    public Product updateAndInvalidateAll(Long id, Product product) {
        return productRepository.save(product);
    }

    // Conditional caching
    @Cacheable(value = "products", key = "#id", condition = "#id > 10")
    public Product findByIdConditional(Long id) {
        return productRepository.findById(id).orElseThrow();
    }

    // Unless condition
    @Cacheable(value = "products", key = "#id", unless = "#result.price > 1000")
    public Product findByIdUnless(Long id) {
        return productRepository.findById(id).orElseThrow();
    }
}
```

### Manual Cache Operations

```java
@Service
public class CacheService {

    @Autowired
    private CacheManager cacheManager;

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    // Manual cache put
    public void putInCache(String cacheName, String key, Object value) {
        Cache cache = cacheManager.getCache(cacheName);
        if (cache != null) {
            cache.put(key, value);
        }
    }

    // Manual cache get
    public Object getFromCache(String cacheName, String key) {
        Cache cache = cacheManager.getCache(cacheName);
        if (cache != null) {
            Cache.ValueWrapper wrapper = cache.get(key);
            return wrapper != null ? wrapper.get() : null;
        }
        return null;
    }

    // Clear specific cache
    public void clearCache(String cacheName) {
        Cache cache = cacheManager.getCache(cacheName);
        if (cache != null) {
            cache.clear();
        }
    }

    // Using RedisTemplate directly
    public void setWithExpiry(String key, Object value, long timeout) {
        redisTemplate.opsForValue().set(key, value, timeout, TimeUnit.SECONDS);
    }

    public Object get(String key) {
        return redisTemplate.opsForValue().get(key);
    }

    public void delete(String key) {
        redisTemplate.delete(key);
    }
}
```

---

## 18. Microservices Architecture {#microservices}

### Microservices Core Concepts

**Key Components:**

1. Service Registry (Eureka)
2. API Gateway (Spring Cloud Gateway)
3. Config Server
4. Load Balancing
5. Circuit Breaker (Resilience4j)
6. Distributed Tracing (Sleuth + Zipkin)

### Service Registry (Eureka Server)

**pom.xml**

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
</dependency>
```

```java
@SpringBootApplication
@EnableEurekaServer
public class EurekaServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(EurekaServerApplication.class, args);
    }
}
```

**application.yml**

```yaml
server:
  port: 8761

eureka:
  client:
    register-with-eureka: false
    fetch-registry: false
```

### Microservice Client (Eureka Client)

**pom.xml**

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```

```java
@SpringBootApplication
@EnableDiscoveryClient
public class UserServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(UserServiceApplication.class, args);
    }
}
```

**application.yml**

```yaml
spring:
  application:
    name: user-service

eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
```

### Inter-Service Communication (Feign Client)

**pom.xml**

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

```java
@FeignClient(name = "user-service")
public interface UserServiceClient {

    @GetMapping("/api/users/{id}")
    UserDTO getUserById(@PathVariable Long id);

    @GetMapping("/api/users")
    List<UserDTO> getAllUsers();

    @PostMapping("/api/users")
    UserDTO createUser(@RequestBody UserDTO userDTO);
}

// Usage in another service
@Service
public class OrderService {

    @Autowired
    private UserServiceClient userServiceClient;

    public Order createOrder(OrderDTO orderDTO) {
        // Call user-service
        UserDTO user = userServiceClient.getUserById(orderDTO.getUserId());

        // Create order
        Order order = new Order();
        order.setUserId(user.getId());
        order.setUserName(user.getUsername());

        return orderRepository.save(order);
    }
}
```

### API Gateway

**pom.xml**

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-gateway</artifactId>
</dependency>
```

**application.yml**

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://user-service
          predicates:
            - Path=/api/users/**
          filters:
            - StripPrefix=1

        - id: order-service
          uri: lb://order-service
          predicates:
            - Path=/api/orders/**
          filters:
            - StripPrefix=1
```

### Circuit Breaker (Resilience4j)

**pom.xml**

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-circuitbreaker-resilience4j</artifactId>
</dependency>
```

```java
@Service
public class OrderService {

    @Autowired
    private UserServiceClient userServiceClient;

    @CircuitBreaker(name = "userService", fallbackMethod = "getUserFallback")
    @Retry(name = "userService")
    @RateLimiter(name = "userService")
    public UserDTO getUser(Long userId) {
        return userServiceClient.getUserById(userId);
    }

    // Fallback method
    public UserDTO getUserFallback(Long userId, Exception ex) {
        UserDTO fallbackUser = new UserDTO();
        fallbackUser.setId(userId);
        fallbackUser.setUsername("Unknown User");
        fallbackUser.setEmail("unavailable@example.com");
        return fallbackUser;
    }
}
```

**application.yml**

```yaml
resilience4j:
  circuitbreaker:
    instances:
      userService:
        sliding-window-size: 10
        failure-rate-threshold: 50
        wait-duration-in-open-state: 10000
        permitted-number-of-calls-in-half-open-state: 3
        automatic-transition-from-open-to-half-open-enabled: true

  retry:
    instances:
      userService:
        max-attempts: 3
        wait-duration: 1000

  ratelimiter:
    instances:
      userService:
        limit-for-period: 10
        limit-refresh-period: 1s
```

---

## 19. Advanced Topics {#advanced-topics}

### Lombok Annotations

```java
// @Data - Generates getters, setters, toString, equals, hashCode
@Data
public class User {
    private Long id;
    private String username;
    private String email;
}

// @Builder - Builder pattern
@Data
@Builder
public class Product {
    private Long id;
    private String name;
    private BigDecimal price;
}

// Usage
Product product = Product.builder()
    .id(1L)
    .name("Laptop")
    .price(new BigDecimal("999.99"))
    .build();

// @NoArgsConstructor, @AllArgsConstructor
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Order {
    private Long id;
    private String orderNumber;
}

// @RequiredArgsConstructor - Constructor for final fields
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
}

// @Slf4j - Logger
@Service
@Slf4j
public class ProductService {
    public void saveProduct(Product product) {
        log.info("Saving product: {}", product);
        log.debug("Product details: {}", product);
        log.error("Error saving product", exception);
    }
}
```

### Scheduled Tasks

```java
@Configuration
@EnableScheduling
public class SchedulingConfig {
}

@Component
public class ScheduledTasks {

    // Fixed rate - every 5 seconds
    @Scheduled(fixedRate = 5000)
    public void fixedRateTask() {
        System.out.println("Fixed rate task: " + LocalDateTime.now());
    }

    // Fixed delay - 5 seconds after previous execution
    @Scheduled(fixedDelay = 5000)
    public void fixedDelayTask() {
        System.out.println("Fixed delay task: " + LocalDateTime.now());
    }

    // Initial delay
    @Scheduled(fixedRate = 5000, initialDelay = 10000)
    public void initialDelayTask() {
        System.out.println("Task with initial delay: " + LocalDateTime.now());
    }

    // Cron expression - Every day at 2 AM
    @Scheduled(cron = "0 0 2 * * ?")
    public void cronTask() {
        System.out.println("Cron task executed at: " + LocalDateTime.now());
    }

    // Cron - Every 5 minutes
    @Scheduled(cron = "0 */5 * * * ?")
    public void everyFiveMinutes() {
        System.out.println("Runs every 5 minutes");
    }

    // Cron - Weekdays at 9 AM
    @Scheduled(cron = "0 0 9 ? * MON-FRI")
    public void weekdayTask() {
        System.out.println("Weekday morning task");
    }
}
```

### Async Processing

```java
@Configuration
@EnableAsync
public class AsyncConfig {

    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-");
        executor.initialize();
        return executor;
    }
}

@Service
public class EmailService {

    @Async("taskExecutor")
    public void sendEmailAsync(String to, String message) {
        System.out.println("Sending email on thread: " + Thread.currentThread().getName());
        // Send email logic
    }

    @Async
    public CompletableFuture<String> processAsync() {
        // Long running task
        return CompletableFuture.completedFuture("Result");
    }
}

// Usage
@RestController
public class UserController {

    @Autowired
    private EmailService emailService;

    @PostMapping("/register")
    public ResponseEntity<String> register(@RequestBody UserDTO userDTO) {
        // Register user
        userService.register(userDTO);

        // Send email asynchronously
        emailService.sendEmailAsync(userDTO.getEmail(), "Welcome!");

        return ResponseEntity.ok("Registration successful");
    }
}
```

### Filters and Interceptors

```java
// Filter
@Component
public class RequestLoggingFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response,
                        FilterChain chain) throws IOException, ServletException {
        HttpServletRequest req = (HttpServletRequest) request;
        System.out.println("Request: " + req.getMethod() + " " + req.getRequestURI());

        chain.doFilter(request, response);

        System.out.println("Response completed");
    }
}

// Interceptor
@Component
public class LoggingInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response,
                            Object handler) throws Exception {
        System.out.println("Pre Handle: " + request.getRequestURI());
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response,
                          Object handler, ModelAndView modelAndView) throws Exception {
        System.out.println("Post Handle");
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response,
                               Object handler, Exception ex) throws Exception {
        System.out.println("After Completion");
    }
}

// Register interceptor
@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

    @Autowired
    private LoggingInterceptor loggingInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(loggingInterceptor)
            .addPathPatterns("/api/**")
            .excludePathPatterns("/api/auth/**");
    }
}
```

### File Upload/Download

```java
@RestController
@RequestMapping("/api/files")
public class FileController {

    private final String uploadDir = "uploads/";

    // File upload
    @PostMapping("/upload")
    public ResponseEntity<String> uploadFile(@RequestParam("file") MultipartFile file) {
        try {
            // Create directory if not exists
            Path uploadPath = Paths.get(uploadDir);
            if (!Files.exists(uploadPath)) {
                Files.createDirectories(uploadPath);
            }

            // Save file
            String fileName = StringUtils.cleanPath(file.getOriginalFilename());
            Path filePath = uploadPath.resolve(fileName);
            Files.copy(file.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);

            return ResponseEntity.ok("File uploaded: " + fileName);
        } catch (IOException ex) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Failed to upload file");
        }
    }

    // Multiple file upload
    @PostMapping("/upload-multiple")
    public ResponseEntity<List<String>> uploadMultipleFiles(
        @RequestParam("files") MultipartFile[] files) {

        List<String> fileNames = Arrays.stream(files)
            .map(file -> {
                try {
                    String fileName = StringUtils.cleanPath(file.getOriginalFilename());
                    Path filePath = Paths.get(uploadDir).resolve(fileName);
                    Files.copy(file.getInputStream(), filePath,
                        StandardCopyOption.REPLACE_EXISTING);
                    return fileName;
                } catch (IOException ex) {
                    throw new RuntimeException("Failed to upload file", ex);
                }
            })
            .collect(Collectors.toList());

        return ResponseEntity.ok(fileNames);
    }

    // File download
    @GetMapping("/download/{fileName}")
    public ResponseEntity<Resource> downloadFile(@PathVariable String fileName) {
        try {
            Path filePath = Paths.get(uploadDir).resolve(fileName).normalize();
            Resource resource = new UrlResource(filePath.toUri());

            if (resource.exists()) {
                return ResponseEntity.ok()
                    .contentType(MediaType.APPLICATION_OCTET_STREAM)
                    .header(HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=\"" + resource.getFilename() + "\"")
                    .body(resource);
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (MalformedURLException ex) {
            return ResponseEntity.badRequest().build();
        }
    }
}
```

---

## 20. Best Practices {#best-practices}

### Project Structure

```
src/main/java/com/example/app/
├── controller/          # REST controllers
├── service/             # Business logic
├── repository/          # Data access
├── model/               # Entity classes
│   ├── entity/         # JPA entities
│   └── dto/            # Data Transfer Objects
├── config/              # Configuration classes
├── security/            # Security components
├── exception/           # Custom exceptions
├── util/                # Utility classes
├── mapper/              # Entity-DTO mappers
└── Application.java     # Main class
```

### Coding Best Practices

1. **Use Constructor Injection**

```java
// Good
@Service
public class UserService {
    private final UserRepository userRepository;

    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}

// Bad - Field injection
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
}
```

2. **Use DTOs for API**

```java
// Never expose entities directly
@RestController
public class UserController {
    // Good
    @GetMapping("/users/{id}")
    public ResponseEntity<UserDTO> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(userService.findById(id));
    }

    // Bad
    @GetMapping("/users/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(userRepository.findById(id));
    }
}
```

3. **Proper Exception Handling**

```java
// Use global exception handler
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
        // Handle exception
    }
}
```

4. **Use Validation**

```java
@PostMapping("/users")
public ResponseEntity<UserDTO> createUser(@Valid @RequestBody UserDTO userDTO) {
    return ResponseEntity.ok(userService.create(userDTO));
}
```

5. **Proper Transaction Management**

```java
@Service
@Transactional(readOnly = true) // Class level
public class UserService {

    @Transactional // Method level for write operations
    public User create(UserDTO userDTO) {
        return userRepository.save(userMapper.toEntity(userDTO));
    }
}
```

6. **Use Proper HTTP Status Codes**

```java
// 200 OK - Successful GET, PUT, PATCH
// 201 CREATED - Successful POST
// 204 NO CONTENT - Successful DELETE
// 400 BAD REQUEST - Validation error
// 401 UNAUTHORIZED - Authentication failed
// 403 FORBIDDEN - Authorization failed
// 404 NOT FOUND - Resource not found
// 500 INTERNAL SERVER ERROR - Server error
```

7. **Use Pagination for Large Datasets**

```java
@GetMapping("/users")
public ResponseEntity<Page<UserDTO>> getUsers(
    @RequestParam(defaultValue = "0") int page,
    @RequestParam(defaultValue = "10") int size) {

    Pageable pageable = PageRequest.of(page, size);
    return ResponseEntity.ok(userService.findAll(pageable));
}
```

8. **Implement Proper Logging**

```java
@Service
@Slf4j
public class UserService {
    public User findById(Long id) {
        log.debug("Finding user with id: {}", id);
        User user = userRepository.findById(id)
            .orElseThrow(() -> {
                log.error("User not found with id: {}", id);
                return new ResourceNotFoundException("User not found");
            });
        log.info("User found: {}", user.getUsername());
        return user;
    }
}
```

9. **Use Profiles for Environment-Specific Configuration**

```java
@Configuration
@Profile("prod")
public class ProdConfig {
    // Production-specific beans
}

@Configuration
@Profile("dev")
public class DevConfig {
    // Development-specific beans
}
```

10. **Write Tests**

```java
// Unit tests
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Test
    void testFindById() {
        // Test implementation
    }
}

// Integration tests
@SpringBootTest
@AutoConfigureTestDatabase
class UserControllerIntegrationTest {
    @Test
    void testCreateUser() {
        // Test implementation
    }
}
```

---

## Summary

This comprehensive guide covers Spring Boot from basics to expert level:

1. **Fundamentals**: IoC, DI, Annotations, Bean Scopes
2. **Web Development**: REST APIs, Controllers, Request Handling
3. **Data Access**: JPA, Repositories, Transactions
4. **Quality**: Validation, Exception Handling, Testing
5. **Advanced**: Security, Caching, Microservices, AOP
6. **Production**: Actuator, Profiles, Best Practices

### Key Takeaways for Interviews

- Understand **IoC and Dependency Injection** thoroughly
- Know different **bean scopes** and their use cases
- Master **REST API development** with proper HTTP methods
- Implement proper **exception handling** with `@ControllerAdvice`
- Use **validation** annotations and custom validators
- Understand **transaction management** and propagation
- Know **Spring Security** and JWT authentication
- Understand **microservices** patterns
- Write **unit and integration tests**
- Follow **best practices** for production-ready code

**Practice coding examples** and understand **why** each pattern is used, not just **how** to implement it. Good luck with your interview!
