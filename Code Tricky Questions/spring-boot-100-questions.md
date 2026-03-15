# 100 Spring Boot Tricky Code Questions with Output & Explanations

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Bean Lifecycle & Scopes](#bean-lifecycle-scopes)
  - [Question 1: @PostConstruct and @PreDestroy Execution Order](#question-1-postconstruct-and-predestroy-execution-order)
  - [Question 2: Singleton vs Prototype Scope](#question-2-singleton-vs-prototype-scope)
  - [Question 3: Request Scope Without Web Context](#question-3-request-scope-without-web-context)
  - [Question 4: @PreDestroy Not Called for Prototype Beans](#question-4-predestroy-not-called-for-prototype-beans)
  - [Question 5: Circular Reference Detection](#question-5-circular-reference-detection)
  - [Question 6: @Lazy Annotation Impact](#question-6-lazy-annotation-impact)
  - [Question 7: Multiple Beans of Same Type](#question-7-multiple-beans-of-same-type)
  - [Question 8: Bean Initialization Order with @DependsOn](#question-8-bean-initialization-order-with-dependson)
  - [Question 9: Session Scoped Bean Injection](#question-9-session-scoped-bean-injection)
  - [Question 10: @Bean Method Called Directly](#question-10-bean-method-called-directly)
- [Dependency Injection](#dependency-injection)
  - [Question 11: @Autowired on Constructor](#question-11-autowired-on-constructor)
  - [Question 12: Field Injection vs Constructor Injection](#question-12-field-injection-vs-constructor-injection)
  - [Question 13: @Qualifier with Multiple Candidates](#question-13-qualifier-with-multiple-candidates)
  - [Question 14: @Primary Annotation Priority](#question-14-primary-annotation-priority)
  - [Question 15: Optional Dependencies](#question-15-optional-dependencies)
  - [Question 16: Injecting Collections](#question-16-injecting-collections)
  - [Question 17: @Resource vs @Autowired](#question-17-resource-vs-autowired)
  - [Question 18: Setter Injection with Immutability](#question-18-setter-injection-with-immutability)
  - [Question 19: Generic Type Injection](#question-19-generic-type-injection)
  - [Question 20: Null Safety with @Nullable and @NonNull](#question-20-null-safety-with-nullable-and-nonnull)
- [Configuration & Properties](#configuration-properties)
  - [Question 21: @Value with Default Values](#question-21-value-with-default-values)
  - [Question 22: @ConfigurationProperties vs @Value](#question-22-configurationproperties-vs-value)
  - [Question 23: SpEL Expression in @Value](#question-23-spel-expression-in-value)
  - [Question 24: Profile-Specific Configuration](#question-24-profile-specific-configuration)
  - [Question 25: @ConditionalOnProperty Example](#question-25-conditionalonproperty-example)
  - [Question 26: Property Placeholder with Environment](#question-26-property-placeholder-with-environment)
  - [Question 27: @PropertySource Order](#question-27-propertysource-order)
  - [Question 28: Relaxed Binding in @ConfigurationProperties](#question-28-relaxed-binding-in-configurationproperties)
  - [Question 29: @Value Cannot Inject into Static Fields](#question-29-value-cannot-inject-into-static-fields)
  - [Question 30: YAML List and Map Binding](#question-30-yaml-list-and-map-binding)
- [AOP - Aspect Oriented Programming](#aop-aspect-oriented-programming)
  - [Question 31: @Before Advice Execution](#question-31-before-advice-execution)
  - [Question 32: @AfterReturning with Return Value](#question-32-afterreturning-with-return-value)
  - [Question 33: @Around Advice Control](#question-33-around-advice-control)
  - [Question 34: @AfterThrowing Exception Handling](#question-34-afterthrowing-exception-handling)
  - [Question 35: Pointcut Expression Combining](#question-35-pointcut-expression-combining)
  - [Question 36: Accessing Method Arguments](#question-36-accessing-method-arguments)
  - [Question 37: @After (Finally) Advice](#question-37-after-finally-advice)
  - [Question 38: Custom Annotation with AOP](#question-38-custom-annotation-with-aop)
  - [Question 39: Order of Multiple Aspects](#question-39-order-of-multiple-aspects)
  - [Question 40: Proxy Limitations with AOP](#question-40-proxy-limitations-with-aop)
- [Spring Data JPA & Hibernate](#spring-data-jpa-hibernate)
  - [Question 41: N+1 Query Problem](#question-41-n1-query-problem)
  - [Question 42: @EntityGraph for Eager Loading](#question-42-entitygraph-for-eager-loading)
  - [Question 43: Derived Query Method Naming](#question-43-derived-query-method-naming)
  - [Question 44: @Query with Named Parameters](#question-44-query-with-named-parameters)
  - [Question 45: @Modifying for Update/Delete](#question-45-modifying-for-updatedelete)
  - [Question 46: findById vs getById](#question-46-findbyid-vs-getbyid)
  - [Question 47: Projection Interface](#question-47-projection-interface)
  - [Question 48: @Transient vs transient](#question-48-transient-vs-transient)
  - [Question 49: Optimistic Locking with @Version](#question-49-optimistic-locking-with-version)
  - [Question 50: CascadeType Effects](#question-50-cascadetype-effects)
- [Transaction Management](#transaction-management)
  - [Question 51: @Transactional Default Behavior](#question-51-transactional-default-behavior)
  - [Question 52: Checked Exception No Rollback](#question-52-checked-exception-no-rollback)
  - [Question 53: Transaction Propagation REQUIRES_NEW](#question-53-transaction-propagation-requires_new)
  - [Question 54: @Transactional Not Working on Private Methods](#question-54-transactional-not-working-on-private-methods)
  - [Question 55: readOnly=true Optimization](#question-55-readonlytrue-optimization)
  - [Question 56: Transaction Timeout](#question-56-transaction-timeout)
  - [Question 57: Nested @Transactional with Propagation.REQUIRED](#question-57-nested-transactional-with-propagationrequired)
  - [Question 58: Programmatic Transaction with TransactionTemplate](#question-58-programmatic-transaction-with-transactiontemplate)
  - [Question 59: Isolation Level Impact](#question-59-isolation-level-impact)
  - [Question 60: Transaction Rollback with try-catch](#question-60-transaction-rollback-with-try-catch)
- [REST API & Exception Handling](#rest-api-exception-handling)
  - [Question 61: @RestController vs @Controller](#question-61-restcontroller-vs-controller)
  - [Question 62: @PathVariable and @RequestParam](#question-62-pathvariable-and-requestparam)
  - [Question 63: @ControllerAdvice for Global Exception Handling](#question-63-controlleradvice-for-global-exception-handling)
  - [Question 64: ResponseEntity for Custom Responses](#question-64-responseentity-for-custom-responses)
  - [Question 65: @Valid and Validation Errors](#question-65-valid-and-validation-errors)
  - [Question 66: Custom Validation Error Response](#question-66-custom-validation-error-response)
  - [Question 67: Content Negotiation](#question-67-content-negotiation)
  - [Question 68: @RequestBody vs @ModelAttribute](#question-68-requestbody-vs-modelattribute)
  - [Question 69: HTTP Method Mappings](#question-69-http-method-mappings)
  - [Question 70: CORS Configuration](#question-70-cors-configuration)
- [Validation & Security](#validation-security)
  - [Question 71: Custom Constraint Validator](#question-71-custom-constraint-validator)
  - [Question 72: Validation Groups](#question-72-validation-groups)
  - [Question 73: Spring Security Basic Configuration](#question-73-spring-security-basic-configuration)
  - [Question 74: @PreAuthorize for Method Security](#question-74-preauthorize-for-method-security)
  - [Question 75: Password Encoding](#question-75-password-encoding)
  - [Question 76: JWT Token Authentication](#question-76-jwt-token-authentication)
  - [Question 77: CSRF Protection](#question-77-csrf-protection)
  - [Question 78: Custom Authentication Provider](#question-78-custom-authentication-provider)
  - [Question 79: Role Hierarchy](#question-79-role-hierarchy)
  - [Question 80: Remember Me Authentication](#question-80-remember-me-authentication)
- [Caching & Async Programming](#caching-async-programming)
  - [Question 81: @Cacheable Basic Usage](#question-81-cacheable-basic-usage)
  - [Question 82: @CacheEvict to Clear Cache](#question-82-cacheevict-to-clear-cache)
  - [Question 83: @CachePut to Update Cache](#question-83-cacheput-to-update-cache)
  - [Question 84: Conditional Caching](#question-84-conditional-caching)
  - [Question 85: Redis Cache Configuration](#question-85-redis-cache-configuration)
  - [Question 86: @Async Method Execution](#question-86-async-method-execution)
  - [Question 87: @Async with CompletableFuture](#question-87-async-with-completablefuture)
  - [Question 88: @Scheduled Fixed Rate](#question-88-scheduled-fixed-rate)
  - [Question 89: Async Exception Handling](#question-89-async-exception-handling)
  - [Question 90: Cache with Multiple Cache Managers](#question-90-cache-with-multiple-cache-managers)
- [Testing & Advanced Topics](#testing-advanced-topics)
  - [Question 91: @WebMvcTest for Controller Testing](#question-91-webmvctest-for-controller-testing)
  - [Question 92: @DataJpaTest for Repository Testing](#question-92-datajpatest-for-repository-testing)
  - [Question 93: @MockBean vs @Mock](#question-93-mockbean-vs-mock)
  - [Question 94: @TestConfiguration for Test Beans](#question-94-testconfiguration-for-test-beans)
  - [Question 95: @Sql for Test Data](#question-95-sql-for-test-data)
  - [Question 96: WebFlux Reactive Controller](#question-96-webflux-reactive-controller)
  - [Question 97: Kafka Producer and Consumer](#question-97-kafka-producer-and-consumer)
  - [Question 98: CommandLineRunner vs ApplicationRunner](#question-98-commandlinerunner-vs-applicationrunner)
  - [Question 99: Custom Auto-Configuration](#question-99-custom-auto-configuration)
  - [Question 100: Multiple Datasource Configuration](#question-100-multiple-datasource-configuration)
- [Conclusion](#conclusion)

## Bean Lifecycle & Scopes

### Question 1: @PostConstruct and @PreDestroy Execution Order

```java
@Component
public class LifecycleBean {
    public LifecycleBean() {
        System.out.println("1. Constructor called");
    }
    
    @PostConstruct
    public void init() {
        System.out.println("2. PostConstruct called");
    }
    
    @PreDestroy
    public void destroy() {
        System.out.println("3. PreDestroy called");
    }
}

// Output:
// 1. Constructor called
// 2. PostConstruct called
// 3. PreDestroy called (on application shutdown)
```

**Explanation:** The bean lifecycle follows this order: Constructor → Dependencies Injection → @PostConstruct → Bean Ready → @PreDestroy (on shutdown). @PostConstruct runs after all dependencies are injected but before the bean is used.

---

### Question 2: Singleton vs Prototype Scope

```java
@Component
@Scope("prototype")
public class PrototypeBean {
    public PrototypeBean() {
        System.out.println("PrototypeBean created");
    }
}

@Component
public class SingletonBean {
    @Autowired
    private PrototypeBean prototypeBean;
}

// Output:
// PrototypeBean created (only once!)
```

**Explanation:** When a prototype bean is injected into a singleton bean via field injection, Spring creates the prototype bean only once during singleton initialization. To get new instances each time, use Provider<T> or ObjectFactory<T>, or method injection via @Lookup.

---

### Question 3: Request Scope Without Web Context

```java
@Component
@Scope(value = "request", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class RequestScopedBean {
    private String data;
}

// Without web context:
// Output: BeanCreationException: Error creating bean with name 'requestScopedBean': 
// Scope 'request' is not active for the current thread
```

**Explanation:** Request-scoped beans only work in web applications with an active HTTP request. Running this in a standalone application throws an exception because there's no request context. Always use request scope with @WebMvcTest or actual web requests.

---

### Question 4: @PreDestroy Not Called for Prototype Beans

```java
@Component
@Scope("prototype")
public class PrototypeLifecycle {
    @PreDestroy
    public void cleanup() {
        System.out.println("Cleanup called");
    }
}

@Autowired
private PrototypeLifecycle prototype;

// Output:
// (No output on shutdown - @PreDestroy is NOT called)
```

**Explanation:** Spring doesn't manage the complete lifecycle of prototype beans. After creation, Spring hands them off to the client. The container never calls @PreDestroy on prototype beans. You must manually call cleanup methods.

---

### Question 5: Circular Reference Detection

```java
@Component
public class BeanA {
    private final BeanB beanB;
    
    @Autowired
    public BeanA(BeanB beanB) {
        this.beanB = beanB;
    }
}

@Component
public class BeanB {
    private final BeanA beanA;
    
    @Autowired
    public BeanB(BeanA beanA) {
        this.beanA = beanA;
    }
}

// Output:
// BeanCurrentlyInCreationException: Error creating bean with name 'beanA': 
// Requested bean is currently in creation: Is there an unresolvable circular reference?
```

**Explanation:** Constructor injection creates circular dependency that Spring cannot resolve. Spring Boot 2.6+ disables circular references by default. Solutions: Use @Lazy on one constructor parameter, use setter injection, or refactor to break the cycle.

---

### Question 6: @Lazy Annotation Impact

```java
@Component
@Lazy
public class LazyBean {
    public LazyBean() {
        System.out.println("LazyBean initialized");
    }
}

@Component
public class EagerBean {
    @Autowired
    private LazyBean lazyBean;
    
    public void useLazy() {
        lazyBean.toString(); // First access
    }
}

// Output:
// (LazyBean initialized only when useLazy() is called, not at startup)
```

**Explanation:** @Lazy defers bean initialization until it's first accessed. The bean is not created during application startup but when first referenced. This reduces startup time but may delay error detection.

---

### Question 7: Multiple Beans of Same Type

```java
@Bean
public PaymentService creditCard() {
    return new CreditCardPayment();
}

@Bean
public PaymentService paypal() {
    return new PaypalPayment();
}

@Autowired
private PaymentService paymentService; // Which one?

// Output:
// NoUniqueBeanDefinitionException: No qualifying bean of type 'PaymentService' available: 
// expected single matching bean but found 2: creditCard,paypal
```

**Explanation:** When multiple beans of the same type exist, Spring cannot decide which to inject. Solutions: Use @Primary on preferred bean, use @Qualifier to specify bean name, or inject by specific method name.

---

### Question 8: Bean Initialization Order with @DependsOn

```java
@Component
@DependsOn("secondBean")
public class FirstBean {
    public FirstBean() {
        System.out.println("FirstBean created");
    }
}

@Component
public class SecondBean {
    public SecondBean() {
        System.out.println("SecondBean created");
    }
}

// Output:
// SecondBean created
// FirstBean created
```

**Explanation:** @DependsOn forces Spring to initialize SecondBean before FirstBean, even though there's no dependency injection relationship. This is useful for initialization ordering without direct dependencies.

---

### Question 9: Session Scoped Bean Injection

```java
@Component
@Scope(value = "session", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class UserPreferences {
    private String theme;
}

@Service
public class UserService {
    @Autowired
    private UserPreferences preferences; // Singleton injecting session-scoped
}

// Output:
// Works correctly - Spring creates a proxy
```

**Explanation:** When injecting a shorter-lived scope (session) into a longer-lived scope (singleton), proxyMode=TARGET_CLASS creates a CGLIB proxy. Each method call on the proxy retrieves the current session's instance. Without proxy mode, you'd get the same instance for all sessions.

---

### Question 10: @Bean Method Called Directly

```java
@Configuration
public class AppConfig {
    @Bean
    public ServiceA serviceA() {
        System.out.println("Creating ServiceA");
        return new ServiceA(serviceB());
    }
    
    @Bean
    public ServiceB serviceB() {
        System.out.println("Creating ServiceB");
        return new ServiceB();
    }
}

// Output:
// Creating ServiceB
// Creating ServiceA
```

**Explanation:** In @Configuration classes, Spring uses CGLIB to proxy bean methods. When serviceA() calls serviceB(), Spring intercepts it and returns the singleton instance instead of creating a new one. Only prints "Creating ServiceB" once, not twice.

---

## Dependency Injection

### Question 11: @Autowired on Constructor

```java
@Service
public class UserService {
    private final UserRepository repository;
    
    // @Autowired is optional on single constructor since Spring 4.3
    public UserService(UserRepository repository) {
        this.repository = repository;
    }
}

// Output: Works without @Autowired annotation
```

**Explanation:** If a class has only one constructor, Spring automatically uses it for dependency injection without requiring @Autowired. For multiple constructors, you must explicitly annotate one with @Autowired.

---

### Question 12: Field Injection vs Constructor Injection

```java
@Service
public class OrderService {
    @Autowired
    private OrderRepository repository; // Field injection
    
    public void testWithNull() {
        repository.findAll(); // NPE in unit tests!
    }
}

// Output: NullPointerException in unit tests without Spring context
```

**Explanation:** Field injection makes testing harder because you cannot instantiate the class with dependencies. Constructor injection is preferred as it makes dependencies explicit, enables immutability, and allows easy testing without reflection.

---

### Question 13: @Qualifier with Multiple Candidates

```java
@Service("primaryEmail")
public class EmailNotification implements NotificationService {}

@Service("primarySms")
public class SmsNotification implements NotificationService {}

@Component
public class NotificationSender {
    @Autowired
    @Qualifier("primaryEmail")
    private NotificationService service;
}

// Output: EmailNotification is injected
```

**Explanation:** @Qualifier resolves ambiguity by specifying the bean name. The value must match the bean name (either explicitly set or auto-generated from class name). Case-sensitive matching is applied.

---

### Question 14: @Primary Annotation Priority

```java
@Service
@Primary
public class DefaultPayment implements PaymentProcessor {}

@Service
public class BackupPayment implements PaymentProcessor {}

@Autowired
private PaymentProcessor processor; // Gets DefaultPayment

@Autowired
@Qualifier("backupPayment")
private PaymentProcessor backup; // Gets BackupPayment
```

**Explanation:** @Primary marks a bean as the default choice when multiple candidates exist. However, @Qualifier always takes precedence over @Primary. Use @Primary for common cases and @Qualifier for specific needs.

---

### Question 15: Optional Dependencies

```java
@Service
public class ReportService {
    private final EmailService emailService;
    
    @Autowired(required = false)
    public ReportService(EmailService emailService) {
        this.emailService = emailService; // Can be null!
    }
    
    public void sendReport() {
        if (emailService != null) {
            emailService.send("report");
        }
    }
}

// Output: Works even if EmailService bean doesn't exist
```

**Explanation:** Setting required=false makes dependency optional. If the bean is not found, null is injected. Better alternatives: use Optional<T> or provide a default implementation to avoid null checks.

---

### Question 16: Injecting Collections

```java
@Component
public class Plugin1 implements Plugin {}

@Component
public class Plugin2 implements Plugin {}

@Service
public class PluginManager {
    @Autowired
    private List<Plugin> plugins; // Injects ALL Plugin beans
    
    public void loadPlugins() {
        System.out.println("Found " + plugins.size() + " plugins");
    }
}

// Output: Found 2 plugins
```

**Explanation:** Spring can inject all beans of a type into a List, Set, or array. The collection contains all matching beans from the application context. Map<String, T> injects beans with their names as keys.

---

### Question 17: @Resource vs @Autowired

```java
@Service
public class DataService {
    @Resource(name = "productRepository")
    private Repository repository; // By name first
    
    @Autowired
    @Qualifier("productRepository")
    private Repository repo2; // By type, then name
}
```

**Explanation:** @Resource (from JSR-250) injects by name first, then by type. @Autowired (Spring-specific) injects by type first, then by qualifier/name. @Resource is Java standard but @Autowired is more flexible with @Primary and @Qualifier.

---

### Question 18: Setter Injection with Immutability

```java
@Service
public class CustomerService {
    private CustomerRepository repository;
    
    @Autowired
    public void setRepository(CustomerRepository repository) {
        this.repository = repository;
    }
}

// Output: Works but field is mutable after construction
```

**Explanation:** Setter injection breaks immutability as the field cannot be final. Constructor injection is preferred for mandatory dependencies as it ensures the object is fully initialized and immutable. Use setter injection only for optional dependencies.

---

### Question 19: Generic Type Injection

```java
@Component
public class StringProcessor implements Processor<String> {}

@Component
public class IntegerProcessor implements Processor<Integer> {}

@Autowired
private Processor<String> processor; // Gets StringProcessor

// Output: StringProcessor is injected based on generic type
```

**Explanation:** Spring 4+ supports generic type matching. It can inject the correct bean based on the generic type parameter. This works because Spring preserves type information at runtime through ResolvableType.

---

### Question 20: Null Safety with @Nullable and @NonNull

```java
@Service
public class UserService {
    private final EmailService emailService;
    
    public UserService(@Nullable EmailService emailService) {
        this.emailService = emailService;
    }
    
    @NonNull
    public User findUser(@NonNull String id) {
        // Must not return null
        return repository.findById(id).orElseThrow();
    }
}
```

**Explanation:** Spring supports null-safety annotations (@Nullable, @NonNull) from various libraries. These provide compile-time warnings and runtime validation. They document which parameters/returns can be null, improving code safety.

---

## Configuration & Properties

### Question 21: @Value with Default Values

```java
@Component
public class AppConfig {
    @Value("${app.timeout:5000}")
    private int timeout;
    
    @Value("${app.missing:default}")
    private String missing;
}

// Output: timeout = 5000 (if property not found), missing = "default"
```

**Explanation:** The syntax ${property:default} provides a fallback value if the property is not defined. Without a default, missing properties cause application startup failure with IllegalArgumentException.

---

### Question 22: @ConfigurationProperties vs @Value

```java
@ConfigurationProperties(prefix = "app")
public class AppProperties {
    private int timeout;
    private String name;
    // getters/setters
}

@Component
public class Service {
    @Value("${app.timeout}")
    private int timeout;
}

// @ConfigurationProperties is type-safe, supports validation, and groups related properties
// @Value is scattered and harder to test
```

**Explanation:** @ConfigurationProperties is preferred for grouped configuration as it provides type safety, validation support, IDE auto-completion, and easier testing. @Value is suitable only for simple, isolated properties.

---

### Question 23: SpEL Expression in @Value

```java
@Component
public class Calculator {
    @Value("#{20 + 30}")
    private int sum; // 50
    
    @Value("#{'Hello ' + 'World'}")
    private String greeting; // "Hello World"
    
    @Value("#{T(Math).random() * 100}")
    private double random;
    
    @Value("#{systemProperties['user.home']}")
    private String home;
}

// Output: sum=50, greeting="Hello World", random=(random number), home=(user's home dir)
```

**Explanation:** Spring Expression Language (SpEL) uses #{} syntax and supports arithmetic, string concatenation, method calls, and system property access. ${} is for property placeholders, while #{} evaluates expressions.

---

### Question 24: Profile-Specific Configuration

```java
@Configuration
@Profile("dev")
public class DevConfig {
    @Bean
    public DataSource dataSource() {
        return new H2DataSource();
    }
}

@Configuration
@Profile("prod")
public class ProdConfig {
    @Bean
    public DataSource dataSource() {
        return new PostgresDataSource();
    }
}

// Output: Only beans from active profile are created
```

**Explanation:** @Profile conditionally registers beans based on active profiles. Set profiles via spring.profiles.active property, command line (--spring.profiles.active=dev), or programmatically. Multiple profiles can be active simultaneously.

---

### Question 25: @ConditionalOnProperty Example

```java
@Configuration
public class FeatureConfig {
    @Bean
    @ConditionalOnProperty(name = "feature.enabled", havingValue = "true")
    public FeatureService enabledFeature() {
        return new FeatureService();
    }
}

// If feature.enabled=false or missing, bean is not created
// Output: Bean created only when feature.enabled=true
```

**Explanation:** @ConditionalOnProperty creates beans based on property values. Use havingValue for exact match and matchIfMissing=true to create bean if property is absent. Useful for feature toggles.

---

### Question 26: Property Placeholder with Environment

```java
@Component
public class ConfigReader {
    @Autowired
    private Environment env;
    
    public void readProps() {
        String name = env.getProperty("app.name", "DefaultApp");
        String[] activeProfiles = env.getActiveProfiles();
        System.out.println("App: " + name + ", Profiles: " + Arrays.toString(activeProfiles));
    }
}

// Output: App: MyApp, Profiles: [dev]
```

**Explanation:** Environment interface provides programmatic access to properties and profiles. It supports type conversion, default values, and property source precedence. More flexible than @Value for dynamic property access.

---

### Question 27: @PropertySource Order

```java
@Configuration
@PropertySource("classpath:default.properties")
@PropertySource("classpath:override.properties")
public class MultiPropertyConfig {}

// If both files define 'app.name':
// override.properties value takes precedence (last wins)
```

**Explanation:** Multiple @PropertySource annotations are processed in order. Later sources override earlier ones for duplicate keys. Spring Boot's application.properties has higher precedence than @PropertySource files.

---

### Question 28: Relaxed Binding in @ConfigurationProperties

```java
@ConfigurationProperties(prefix = "my-app")
public class AppProps {
    private String firstName; // Binds to my-app.first-name, my-app.firstName, MY_APP_FIRSTNAME
}

// In application.properties:
// my-app.first-name=John  ✓
// my-app.firstName=John   ✓
// MY_APP_FIRSTNAME=John   ✓ (environment variable)
```

**Explanation:** @ConfigurationProperties uses relaxed binding, supporting kebab-case, camelCase, snake_case, and uppercase with underscores. This makes it flexible across different configuration sources (properties files, YAML, environment variables).

---

### Question 29: @Value Cannot Inject into Static Fields

```java
@Component
public class Config {
    @Value("${app.name}")
    private static String appName; // DOES NOT WORK!
    
    @Value("${app.name}")
    private String instanceName; // Works
}

// Output: appName remains null (no error thrown!)
```

**Explanation:** Spring cannot inject values into static fields because dependency injection occurs on instances. Static fields belong to the class, not instances. Workaround: Use non-static field or setter method with @Value.

---

### Question 30: YAML List and Map Binding

```java
@ConfigurationProperties(prefix = "app")
public class AppConfig {
    private List<String> servers;
    private Map<String, String> credentials;
}

// In application.yml:
// app:
//   servers:
//     - server1.com
//     - server2.com
//   credentials:
//     username: admin
//     password: secret

// Output: servers=[server1.com, server2.com], credentials={username=admin, password=secret}
```

**Explanation:** @ConfigurationProperties automatically binds YAML/properties lists and maps to Java collections. YAML provides better readability for complex structures. Properties files use indexed notation: app.servers[0]=server1.com.

---

## AOP - Aspect Oriented Programming

### Question 31: @Before Advice Execution

```java
@Aspect
@Component
public class LoggingAspect {
    @Before("execution(* com.example.service.*.*(..))")
    public void logBefore(JoinPoint joinPoint) {
        System.out.println("Before: " + joinPoint.getSignature().getName());
    }
}

@Service
public class UserService {
    public void createUser() {
        System.out.println("Creating user");
    }
}

// Output:
// Before: createUser
// Creating user
```

**Explanation:** @Before advice executes before the target method. It cannot prevent method execution (unless throwing exception). JoinPoint provides method signature, arguments, and target object information.

---

### Question 32: @AfterReturning with Return Value

```java
@Aspect
@Component
public class ResultAspect {
    @AfterReturning(pointcut = "execution(* com.example.service.*.find*(..))", 
                    returning = "result")
    public void logResult(JoinPoint joinPoint, Object result) {
        System.out.println("Method returned: " + result);
    }
}

// Output: 
// Method returned: User[id=1, name=John]
```

**Explanation:** @AfterReturning executes after successful method completion. The 'returning' attribute binds the return value to the advice parameter. This advice doesn't run if an exception is thrown.

---

### Question 33: @Around Advice Control

```java
@Aspect
@Component
public class PerformanceAspect {
    @Around("execution(* com.example.service.*.*(..))")
    public Object measureTime(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = pjp.proceed(); // Must call to execute method
        long duration = System.currentTimeMillis() - start;
        System.out.println("Execution time: " + duration + "ms");
        return result; // Must return the result
    }
}

// Output:
// Execution time: 150ms
```

**Explanation:** @Around is the most powerful advice type. It wraps the method execution, allowing you to control if/when the method executes via proceed(). You can modify arguments with proceed(args) and the return value.

---

### Question 34: @AfterThrowing Exception Handling

```java
@Aspect
@Component
public class ExceptionAspect {
    @AfterThrowing(pointcut = "execution(* com.example.service.*.*(..))", 
                   throwing = "ex")
    public void logException(JoinPoint joinPoint, Exception ex) {
        System.out.println("Exception in " + joinPoint.getSignature().getName() 
                          + ": " + ex.getMessage());
    }
}

// Output (when exception occurs):
// Exception in createUser: User already exists
```

**Explanation:** @AfterThrowing executes only when the target method throws an exception. The 'throwing' attribute binds the exception to advice parameter. This advice doesn't suppress the exception—it still propagates to the caller.

---

### Question 35: Pointcut Expression Combining

```java
@Aspect
@Component
public class SecurityAspect {
    @Pointcut("execution(* com.example.service.*.*(..))")
    public void serviceMethods() {}
    
    @Pointcut("@annotation(com.example.Secured)")
    public void securedMethods() {}
    
    @Before("serviceMethods() && securedMethods()")
    public void checkSecurity() {
        System.out.println("Checking security");
    }
}

// Output: Checks security only for @Secured methods in service package
```

**Explanation:** @Pointcut defines reusable pointcut expressions. Combine them using && (and), || (or), ! (not). This improves maintainability by centralizing pointcut definitions and enabling complex matching logic.

---

### Question 36: Accessing Method Arguments

```java
@Aspect
@Component
public class ValidationAspect {
    @Before("execution(* com.example.service.*.create*(..)) && args(name,..)")
    public void validateName(String name) {
        if (name == null || name.isEmpty()) {
            throw new IllegalArgumentException("Name cannot be empty");
        }
        System.out.println("Validating: " + name);
    }
}

// Output (if name is valid):
// Validating: John
```

**Explanation:** The args() pointcut expression binds method arguments to advice parameters. Use (..) for remaining arguments. Position matters—args(String, ..) matches methods where the first parameter is String.

---

### Question 37: @After (Finally) Advice

```java
@Aspect
@Component
public class ResourceAspect {
    @After("execution(* com.example.service.*.*(..))")
    public void cleanup(JoinPoint joinPoint) {
        System.out.println("Cleanup after " + joinPoint.getSignature().getName());
    }
}

// Output (always executes, even if exception thrown):
// Cleanup after processData
```

**Explanation:** @After is like a finally block—it executes after method completion regardless of outcome (success or exception). Use it for cleanup operations. For exception-specific logic, use @AfterThrowing instead.

---

### Question 38: Custom Annotation with AOP

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface TrackTime {}

@Aspect
@Component
public class TimeTrackingAspect {
    @Around("@annotation(TrackTime)")
    public Object track(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = pjp.proceed();
        System.out.println("Time: " + (System.currentTimeMillis() - start) + "ms");
        return result;
    }
}

@Service
public class DataService {
    @TrackTime
    public void process() {
        // method body
    }
}

// Output: Time: 200ms
```

**Explanation:** Custom annotations + AOP create powerful, reusable cross-cutting concerns. @annotation(AnnotationName) pointcut matches methods annotated with the specified annotation. This approach is cleaner than class/package-based pointcuts.

---

### Question 39: Order of Multiple Aspects

```java
@Aspect
@Component
@Order(1)
public class FirstAspect {
    @Before("execution(* com.example..*(..))")
    public void first() {
        System.out.println("First aspect");
    }
}

@Aspect
@Component
@Order(2)
public class SecondAspect {
    @Before("execution(* com.example..*(..))")
    public void second() {
        System.out.println("Second aspect");
    }
}

// Output:
// First aspect
// Second aspect
```

**Explanation:** @Order controls aspect execution order. Lower values execute first for @Before advice and last for @After advice. Without @Order, execution order is undefined. Use Ordered interface or @Order annotation.

---

### Question 40: Proxy Limitations with AOP

```java
@Service
public class PaymentService {
    @Transactional
    public void processPayment() {
        this.sendNotification(); // AOP not applied!
    }
    
    @Transactional
    public void sendNotification() {
        // Transaction advice bypassed
    }
}

// Output: @Transactional on sendNotification is ignored
```

**Explanation:** Spring AOP uses proxies. When a method calls another method on the same object (this.method()), the call bypasses the proxy, so aspects aren't applied. Solution: Inject the bean into itself or use AspectJ weaving instead of Spring AOP.

---

## Spring Data JPA & Hibernate

### Question 41: N+1 Query Problem

```java
@Entity
public class User {
    @Id
    private Long id;
    
    @OneToMany(mappedBy = "user")
    private List<Order> orders;
}

List<User> users = userRepository.findAll(); // 1 query
for (User user : users) {
    user.getOrders().size(); // N additional queries (one per user)
}

// Output: 1 + N queries executed (performance issue!)
```

**Explanation:** Lazy loading causes N+1 problem: 1 query for users + N queries for orders (one per user). Solutions: Use @EntityGraph, JOIN FETCH in JPQL, or @BatchSize. Always monitor SQL queries to detect this issue.

---

### Question 42: @EntityGraph for Eager Loading

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    @EntityGraph(attributePaths = {"orders", "orders.items"})
    List<User> findAll();
}

// Output: Single query with LEFT JOIN to fetch users, orders, and items
```

**Explanation:** @EntityGraph overrides lazy loading for specific queries, fetching related entities in one query. attributePaths specifies which associations to fetch eagerly. This solves N+1 but may cause cartesian product with multiple collections.

---

### Question 43: Derived Query Method Naming

```java
@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    List<Product> findByNameAndPriceGreaterThan(String name, BigDecimal price);
    
    List<Product> findByNameContainingIgnoreCase(String keyword);
    
    Long countByStatus(String status);
}

// Spring generates queries from method names automatically
// No @Query needed!
```

**Explanation:** Spring Data JPA derives queries from method names following conventions: findBy/countBy/deleteBy + property + condition (GreaterThan, LessThan, Containing, etc.). Combine with And/Or. Type-safe but limited for complex queries.

---

### Question 44: @Query with Named Parameters

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    @Query("SELECT u FROM User u WHERE u.age > :minAge AND u.city = :city")
    List<User> findByAgeAndCity(@Param("minAge") int age, @Param("city") String city);
    
    // Native query
    @Query(value = "SELECT * FROM users WHERE age > :age", nativeQuery = true)
    List<User> findByNative(@Param("age") int age);
}
```

**Explanation:** @Query allows custom JPQL or native SQL. Named parameters (:name) are clearer than positional (?1). Use @Param to bind parameters. nativeQuery=true enables database-specific SQL but loses database portability.

---

### Question 45: @Modifying for Update/Delete

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    @Modifying
    @Transactional
    @Query("UPDATE User u SET u.status = :status WHERE u.id = :id")
    int updateStatus(@Param("id") Long id, @Param("status") String status);
}

// Returns: Number of affected rows
```

**Explanation:** @Modifying is required for UPDATE/DELETE queries with @Query. Must be used with @Transactional. Returns int (affected rows) or void. Note: This bypasses Hibernate's first-level cache, so entity changes aren't reflected automatically.

---

### Question 46: findById vs getById

```java
Optional<User> user1 = userRepository.findById(1L); // Immediately queries DB
User user2 = userRepository.getById(1L); // Returns proxy, queries DB on first access

user1.ifPresent(u -> System.out.println(u.getName())); // Safe
System.out.println(user2.getName()); // May throw EntityNotFoundException if ID doesn't exist
```

**Explanation:** findById() immediately hits the database and returns Optional. getById() (deprecated) returns a lazy-loaded proxy. Use findById() for null safety and immediate validation. getReferenceById() is the new alternative to getById().

---

### Question 47: Projection Interface

```java
public interface UserProjection {
    String getName();
    String getEmail();
}

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    List<UserProjection> findByCity(String city);
}

// Output: Only name and email columns are selected (not all fields)
```

**Explanation:** Projection interfaces select only specific fields, improving performance. Spring Data JPA creates proxy implementations. Closed projections (all getters match entity properties) optimize queries. Open projections allow @Value with SpEL but fetch all columns.

---

### Question 48: @Transient vs transient

```java
@Entity
public class User {
    @Id
    private Long id;
    
    @Transient // JPA annotation - not persisted
    private String temporaryData;
    
    private transient String calculatedField; // Java keyword - not serialized or persisted
}
```

**Explanation:** @Transient (JPA) excludes field from database persistence. transient (Java keyword) excludes from serialization. Use @Transient for derived/calculated fields. Both prevent persistence, but @Transient is preferred for clarity in JPA entities.

---

### Question 49: Optimistic Locking with @Version

```java
@Entity
public class Product {
    @Id
    private Long id;
    
    @Version
    private Long version;
    
    private String name;
}

// Transaction 1: Loads product (version=1), updates name
// Transaction 2: Loads same product (version=1), updates name
// Transaction 1: Commits (version becomes 2)
// Transaction 2: Commits -> OptimisticLockException (expected version=1, found version=2)
```

**Explanation:** @Version enables optimistic locking. Hibernate automatically increments version on updates and checks it before committing. If versions don't match, OptimisticLockException is thrown, preventing lost updates. Preferred for concurrent access scenarios.

---

### Question 50: CascadeType Effects

```java
@Entity
public class Order {
    @Id
    private Long id;
    
    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItem> items;
}

orderRepository.delete(order); 
// Output: Deletes order AND all associated items (due to CascadeType.ALL)
```

**Explanation:** CascadeType propagates operations: ALL (all operations), PERSIST (save), MERGE (update), REMOVE (delete), REFRESH, DETACH. orphanRemoval=true deletes child entities when removed from collection. Use carefully to avoid unintended deletions.

---

## Transaction Management

### Question 51: @Transactional Default Behavior

```java
@Service
public class UserService {
    @Transactional
    public void createUser(User user) {
        userRepository.save(user);
        throw new RuntimeException("Error"); // Rolls back
    }
}

// Output: Transaction rolled back, user not saved
```

**Explanation:** @Transactional defaults: propagation=REQUIRED, isolation=DEFAULT, rollback on RuntimeException/Error, no rollback on checked exceptions, readOnly=false. Transaction starts at method entry, commits on success, rolls back on unchecked exceptions.

---

### Question 52: Checked Exception No Rollback

```java
@Service
public class OrderService {
    @Transactional
    public void processOrder() throws Exception {
        orderRepository.save(order);
        throw new Exception("Checked exception"); // NO rollback by default!
    }
}

// Output: Transaction committed, order saved (unexpected!)
```

**Explanation:** By default, @Transactional only rolls back on RuntimeException and Error, not checked exceptions. To rollback on checked exceptions, use @Transactional(rollbackFor = Exception.class). This is a common source of bugs.

---

### Question 53: Transaction Propagation REQUIRES_NEW

```java
@Service
public class OuterService {
    @Autowired
    private InnerService innerService;
    
    @Transactional
    public void outerMethod() {
        // Transaction 1 starts
        innerService.innerMethod(); // Transaction 2 starts (suspends 1)
        throw new RuntimeException(); // Rolls back Transaction 1, but not Transaction 2!
    }
}

@Service
public class InnerService {
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void innerMethod() {
        // Executes in new transaction
    }
}

// Output: innerMethod changes committed, outerMethod changes rolled back
```

**Explanation:** REQUIRES_NEW suspends current transaction and starts a new one. Inner transaction commits independently. Outer transaction failure doesn't rollback inner. Use for audit logs or critical operations that should succeed regardless of outer transaction.

---

### Question 54: @Transactional Not Working on Private Methods

```java
@Service
public class PaymentService {
    @Transactional
    private void processPayment() { // Doesn't work!
        paymentRepository.save(payment);
    }
    
    public void makePayment() {
        processPayment(); // Transaction not started!
    }
}

// Output: No transaction, auto-commit mode
```

**Explanation:** @Transactional only works on public methods because Spring AOP uses proxies. Private methods cannot be proxied. Internal calls (this.method()) also bypass proxy. Solution: Make method public or move to separate bean.

---

### Question 55: readOnly=true Optimization

```java
@Service
public class ReportService {
    @Transactional(readOnly = true)
    public List<Report> generateReport() {
        return reportRepository.findAll(); // Optimized read-only transaction
    }
}

// Output: Better performance, no dirty checking
```

**Explanation:** readOnly=true hints to JDBC driver and Hibernate for optimizations: skip dirty checking, route to read replica, optimize flush mode. Some databases provide better query optimization. Still prevents data modification but doesn't enforce it—validation happens at flush time.

---

### Question 56: Transaction Timeout

```java
@Service
public class DataService {
    @Transactional(timeout = 5) // 5 seconds
    public void processLargeData() {
        // If takes longer than 5 seconds -> TransactionTimedOutException
        largeDataRepository.batchProcess();
    }
}

// Output: Exception if operation exceeds 5 seconds
```

**Explanation:** timeout attribute sets maximum transaction duration in seconds. Helps prevent long-running transactions locking resources. Database must support timeout. Throws TransactionTimedOutException on expiry. Default is -1 (no timeout).

---

### Question 57: Nested @Transactional with Propagation.REQUIRED

```java
@Service
public class OuterService {
    @Transactional
    public void outerMethod() { // Transaction 1
        innerService.innerMethod(); // Joins Transaction 1 (same transaction)
        throw new RuntimeException(); // Rolls back everything
    }
}

@Service
public class InnerService {
    @Transactional(propagation = Propagation.REQUIRED) // Default
    public void innerMethod() {
        // Part of same transaction
    }
}

// Output: Both inner and outer rolled back
```

**Explanation:** REQUIRED (default) joins existing transaction or creates new one if none exists. Inner and outer methods share same transaction. Any exception rolls back all changes. Most common propagation level.

---

### Question 58: Programmatic Transaction with TransactionTemplate

```java
@Service
public class PaymentService {
    @Autowired
    private TransactionTemplate transactionTemplate;
    
    public void processPayment() {
        transactionTemplate.execute(status -> {
            try {
                paymentRepository.save(payment);
                return payment;
            } catch (Exception e) {
                status.setRollbackOnly();
                throw e;
            }
        });
    }
}
```

**Explanation:** TransactionTemplate provides programmatic transaction control, useful when you need fine-grained control or conditional transactions. setRollbackOnly() marks transaction for rollback. More verbose than @Transactional but more flexible.

---

### Question 59: Isolation Level Impact

```java
@Service
public class InventoryService {
    @Transactional(isolation = Isolation.SERIALIZABLE)
    public void updateStock(Long productId, int quantity) {
        Product product = productRepository.findById(productId);
        product.setStock(product.getStock() - quantity);
        // Highest isolation, prevents phantom reads but slowest
    }
}

// Output: Prevents concurrent modifications but impacts performance
```

**Explanation:** Isolation levels: READ_UNCOMMITTED (dirty reads), READ_COMMITTED (prevents dirty reads), REPEATABLE_READ (prevents non-repeatable reads), SERIALIZABLE (full isolation). Higher isolation = more consistency but lower concurrency. Choose based on use case.

---

### Question 60: Transaction Rollback with try-catch

```java
@Service
public class UserService {
    @Transactional
    public void createUser(User user) {
        try {
            userRepository.save(user);
            riskyOperation();
        } catch (Exception e) {
            // Exception caught, transaction NOT rolled back!
            log.error("Error", e);
        }
    }
}

// Output: Transaction commits even if riskyOperation() throws exception
```

**Explanation:** Catching exceptions prevents transaction rollback. Spring sees method completed successfully. To rollback, either: don't catch exception, rethrow it, or call TransactionAspectSupport.currentTransactionStatus().setRollbackOnly(). Avoid catching exceptions unless necessary.

---

## REST API & Exception Handling

### Question 61: @RestController vs @Controller

```java
@Controller
public class WebController {
    @GetMapping("/page")
    public String page() {
        return "viewName"; // Returns view name for template engine
    }
}

@RestController // = @Controller + @ResponseBody
public class ApiController {
    @GetMapping("/data")
    public User data() {
        return new User(); // Automatically serialized to JSON
    }
}

// Output: ApiController returns JSON, WebController returns HTML page
```

**Explanation:** @RestController combines @Controller and @ResponseBody. Every method returns data (serialized to JSON/XML) instead of view names. Use @RestController for REST APIs, @Controller for MVC web applications with templates.

---

### Question 62: @PathVariable and @RequestParam

```java
@RestController
public class ProductController {
    @GetMapping("/products/{id}")
    public Product getProduct(@PathVariable Long id, 
                             @RequestParam(required = false) String filter) {
        // URL: /products/123?filter=active
        // id = 123, filter = "active"
    }
}

// @PathVariable: extracts from URI path
// @RequestParam: extracts from query string
```

**Explanation:** @PathVariable extracts values from URI template (path segments). @RequestParam extracts from query parameters. PathVariable is required by default, RequestParam can be optional. Use PathVariable for resource identifiers, RequestParam for filters/options.

---

### Question 63: @ControllerAdvice for Global Exception Handling

```java
@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(ResourceNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(ResourceNotFoundException ex) {
        return new ErrorResponse(ex.getMessage(), 404);
    }
    
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ErrorResponse handleGeneral(Exception ex) {
        return new ErrorResponse("Internal error", 500);
    }
}

// Output: Consistent error responses across all controllers
```

**Explanation:** @ControllerAdvice applies exception handlers globally to all controllers. @ExceptionHandler specifies which exception to handle. @ResponseStatus sets HTTP status code. This centralizes error handling, ensuring consistent error responses.

---

### Question 64: ResponseEntity for Custom Responses

```java
@RestController
public class UserController {
    @PostMapping("/users")
    public ResponseEntity<User> createUser(@RequestBody User user) {
        User saved = userService.save(user);
        return ResponseEntity
            .status(HttpStatus.CREATED)
            .header("Location", "/users/" + saved.getId())
            .body(saved);
    }
    
    @GetMapping("/users/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }
}

// Output: Full control over status codes, headers, and body
```

**Explanation:** ResponseEntity provides complete control over HTTP response: status code, headers, body. Use for complex responses. Return type can be Optional, and you can chain operations. More flexible than @ResponseStatus annotation.

---

### Question 65: @Valid and Validation Errors

```java
@RestController
public class UserController {
    @PostMapping("/users")
    public User createUser(@Valid @RequestBody User user) {
        return userService.save(user);
    }
}

@Entity
public class User {
    @NotBlank(message = "Name required")
    private String name;
    
    @Email(message = "Invalid email")
    private String email;
}

// If validation fails:
// Output: 400 Bad Request with MethodArgumentNotValidException
```

**Explanation:** @Valid triggers JSR-303 validation on request body. Validation annotations (@NotNull, @Size, @Email, etc.) are checked before method execution. Failed validation throws MethodArgumentNotValidException. Handle it in @ControllerAdvice to customize error response.

---

### Question 66: Custom Validation Error Response

```java
@ControllerAdvice
public class ValidationExceptionHandler {
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public Map<String, String> handleValidation(MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(error -> 
            errors.put(error.getField(), error.getDefaultMessage())
        );
        return errors;
    }
}

// Output: {"name": "Name required", "email": "Invalid email"}
```

**Explanation:** MethodArgumentNotValidException contains BindingResult with all validation errors. Extract field names and messages to create user-friendly error response. This approach provides clear, actionable error information to API clients.

---

### Question 67: Content Negotiation

```java
@RestController
public class DataController {
    @GetMapping(value = "/data", produces = {
        MediaType.APPLICATION_JSON_VALUE,
        MediaType.APPLICATION_XML_VALUE
    })
    public Data getData() {
        return new Data();
    }
}

// Request with Accept: application/json -> JSON response
// Request with Accept: application/xml -> XML response
```

**Explanation:** produces attribute specifies supported response formats. Spring selects format based on Accept header (content negotiation). Requires appropriate message converters (Jackson for JSON, JAXB for XML). Default is JSON if Accept header is missing or */*.

---

### Question 68: @RequestBody vs @ModelAttribute

```java
@RestController
public class FormController {
    @PostMapping("/json")
    public void handleJson(@RequestBody User user) {
        // Expects JSON: {"name":"John","email":"john@example.com"}
    }
    
    @PostMapping("/form")
    public void handleForm(@ModelAttribute User user) {
        // Expects form data: name=John&email=john@example.com
    }
}

// @RequestBody: for JSON/XML, Content-Type: application/json
// @ModelAttribute: for form data, Content-Type: application/x-www-form-urlencoded
```

**Explanation:** @RequestBody deserializes request body (JSON/XML) to object. @ModelAttribute binds form parameters to object fields. Use RequestBody for REST APIs, ModelAttribute for traditional HTML forms. They use different message converters.

---

### Question 69: HTTP Method Mappings

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {
    @GetMapping // Read all
    public List<Product> getAll() {}
    
    @GetMapping("/{id}") // Read one
    public Product getOne(@PathVariable Long id) {}
    
    @PostMapping // Create
    public Product create(@RequestBody Product product) {}
    
    @PutMapping("/{id}") // Update (full)
    public Product update(@PathVariable Long id, @RequestBody Product product) {}
    
    @PatchMapping("/{id}") // Update (partial)
    public Product patch(@PathVariable Long id, @RequestBody Map<String, Object> updates) {}
    
    @DeleteMapping("/{id}") // Delete
    public void delete(@PathVariable Long id) {}
}
```

**Explanation:** RESTful conventions: GET (read), POST (create), PUT (full update), PATCH (partial update), DELETE (remove). @RequestMapping can specify method, but specific annotations (@GetMapping, etc.) are clearer. Follow REST principles for intuitive APIs.

---

### Question 70: CORS Configuration

```java
@RestController
@CrossOrigin(origins = "http://localhost:3000")
public class ApiController {
    @GetMapping("/data")
    public Data getData() {
        return new Data();
    }
}

// Global CORS configuration
@Configuration
public class CorsConfig {
    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/api/**")
                    .allowedOrigins("http://localhost:3000")
                    .allowedMethods("GET", "POST", "PUT", "DELETE");
            }
        };
    }
}
```

**Explanation:** @CrossOrigin enables Cross-Origin Resource Sharing for specific controller/method. For global CORS, configure WebMvcConfigurer. CORS allows browsers to make requests from different origins. Required for frontend apps on different domains/ports.

---

## Validation & Security

### Question 71: Custom Constraint Validator

```java
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = AgeValidator.class)
public @interface ValidAge {
    String message() default "Age must be between 18 and 100";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

public class AgeValidator implements ConstraintValidator<ValidAge, Integer> {
    @Override
    public boolean isValid(Integer age, ConstraintValidatorContext context) {
        return age != null && age >= 18 && age <= 100;
    }
}

public class User {
    @ValidAge
    private Integer age;
}

// Output: Validation fails if age < 18 or age > 100
```

**Explanation:** Create custom validators by: 1) Define annotation with @Constraint, 2) Implement ConstraintValidator<Annotation, Type>, 3) Override isValid(). Custom validators encapsulate complex validation logic reusable across fields.

---

### Question 72: Validation Groups

```java
public interface CreateValidation {}
public interface UpdateValidation {}

public class User {
    @NotNull(groups = UpdateValidation.class)
    private Long id;
    
    @NotBlank(groups = {CreateValidation.class, UpdateValidation.class})
    private String name;
}

@RestController
public class UserController {
    @PostMapping
    public User create(@Validated(CreateValidation.class) @RequestBody User user) {
        // id not required
    }
    
    @PutMapping
    public User update(@Validated(UpdateValidation.class) @RequestBody User user) {
        // id required
    }
}
```

**Explanation:** Validation groups allow different validation rules for different scenarios. Define marker interfaces, assign to constraints with groups attribute, activate with @Validated. More flexible than separate DTOs for create/update operations.

---

### Question 73: Spring Security Basic Configuration

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests(auth -> auth
                .requestMatchers("/public/**").permitAll()
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .formLogin(Customizer.withDefaults())
            .httpBasic(Customizer.withDefaults());
        return http.build();
    }
    
    @Bean
    public UserDetailsService userDetailsService() {
        UserDetails user = User.withDefaultPasswordEncoder()
            .username("user")
            .password("password")
            .roles("USER")
            .build();
        return new InMemoryUserDetailsManager(user);
    }
}

// Output: /public/** accessible without auth, /admin/** requires ADMIN role
```

**Explanation:** SecurityFilterChain defines authorization rules. requestMatchers() specifies patterns, permitAll()/authenticated()/hasRole() sets access rules. Order matters—first match wins. UserDetailsService provides user authentication details.

---

### Question 74: @PreAuthorize for Method Security

```java
@Configuration
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class MethodSecurityConfig {}

@Service
public class DataService {
    @PreAuthorize("hasRole('ADMIN')")
    public void deleteData() {
        // Only ADMIN can execute
    }
    
    @PreAuthorize("#username == authentication.principal.username")
    public User getUserData(String username) {
        // Users can only access their own data
    }
    
    @PreAuthorize("hasPermission(#id, 'User', 'read')")
    public User findById(Long id) {
        // Custom permission check
    }
}

// Output: AccessDeniedException if authorization fails
```

**Explanation:** @PreAuthorize checks authorization before method execution using SpEL expressions. Access current user via authentication.principal, method parameters via #paramName. More fine-grained than URL-based security. Requires @EnableGlobalMethodSecurity.

---

### Question 75: Password Encoding

```java
@Configuration
public class SecurityConfig {
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}

@Service
public class UserService {
    @Autowired
    private PasswordEncoder passwordEncoder;
    
    public void createUser(String username, String rawPassword) {
        String encoded = passwordEncoder.encode(rawPassword);
        // Store encoded password in database
    }
    
    public boolean checkPassword(String raw, String encoded) {
        return passwordEncoder.matches(raw, encoded);
    }
}

// Output: Password hashed with BCrypt algorithm
```

**Explanation:** Never store plain-text passwords. PasswordEncoder provides secure hashing. BCryptPasswordEncoder uses bcrypt with salt and configurable strength. encode() hashes password, matches() verifies. Spring Security automatically uses configured encoder for authentication.

---

### Question 76: JWT Token Authentication

```java
@Component
public class JwtTokenProvider {
    @Value("${jwt.secret}")
    private String secret;
    
    public String generateToken(Authentication auth) {
        return Jwts.builder()
            .setSubject(auth.getName())
            .setIssuedAt(new Date())
            .setExpiration(new Date(System.currentTimeMillis() + 86400000))
            .signWith(SignatureAlgorithm.HS512, secret)
            .compact();
    }
    
    public String getUsernameFromToken(String token) {
        return Jwts.parser()
            .setSigningKey(secret)
            .parseClaimsJws(token)
            .getBody()
            .getSubject();
    }
}

// Output: JWT token: eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ1c2VyIiwiaWF0Ijo...
```

**Explanation:** JWT (JSON Web Token) provides stateless authentication. Token contains encoded claims signed with secret. Client sends token in Authorization header. Server validates signature without database lookup. Use short expiration and refresh tokens for security.

---

### Question 77: CSRF Protection

```java
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.csrf().disable(); // ⚠️ Disables CSRF protection
        
        // For REST APIs with JWT, CSRF not needed
        // For session-based apps, keep CSRF enabled
        return http.build();
    }
}

// CSRF token in form:
// <input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}"/>
```

**Explanation:** CSRF (Cross-Site Request Forgery) protection prevents unauthorized commands from trusted users. Spring Security enables it by default for session-based auth. Disable for stateless REST APIs with token authentication. For forms, include CSRF token.

---

### Question 78: Custom Authentication Provider

```java
@Component
public class CustomAuthProvider implements AuthenticationProvider {
    @Override
    public Authentication authenticate(Authentication auth) throws AuthenticationException {
        String username = auth.getName();
        String password = auth.getCredentials().toString();
        
        // Custom authentication logic
        if (customValidation(username, password)) {
            return new UsernamePasswordAuthenticationToken(
                username, password, Collections.emptyList());
        }
        throw new BadCredentialsException("Authentication failed");
    }
    
    @Override
    public boolean supports(Class<?> authentication) {
        return UsernamePasswordAuthenticationToken.class.isAssignableFrom(authentication);
    }
}
```

**Explanation:** AuthenticationProvider allows custom authentication logic. authenticate() verifies credentials and returns Authentication object. supports() indicates which authentication types it handles. Useful for LDAP, OAuth, or custom authentication mechanisms.

---

### Question 79: Role Hierarchy

```java
@Bean
public RoleHierarchy roleHierarchy() {
    RoleHierarchyImpl hierarchy = new RoleHierarchyImpl();
    hierarchy.setHierarchy("ROLE_ADMIN > ROLE_USER\nROLE_USER > ROLE_GUEST");
    return hierarchy;
}

@Service
public class ContentService {
    @PreAuthorize("hasRole('USER')")
    public void accessContent() {
        // ADMIN can also access (inherits USER role)
    }
}

// Output: ADMIN users can access USER-level resources
```

**Explanation:** RoleHierarchy defines role inheritance. ADMIN > USER means ADMIN implicitly has USER role. Reduces duplication in security rules. Configure hierarchy string with ">" separator. Applies to all hasRole() checks.

---

### Question 80: Remember Me Authentication

```java
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.rememberMe()
            .key("uniqueAndSecret")
            .tokenValiditySeconds(86400) // 24 hours
            .rememberMeParameter("remember-me");
        return http.build();
    }
}

// In login form:
// <input type="checkbox" name="remember-me"/> Remember Me
```

**Explanation:** Remember-me creates a persistent token cookie for automatic login. Token stored in cookie, validated on subsequent requests. tokenValiditySeconds sets expiration. Requires unique key for token generation. Use HTTPS to protect remember-me cookies.

---

## Caching & Async Programming

### Question 81: @Cacheable Basic Usage

```java
@Service
public class ProductService {
    @Cacheable(value = "products", key = "#id")
    public Product findById(Long id) {
        System.out.println("Fetching from DB");
        return productRepository.findById(id).orElse(null);
    }
}

// First call: Fetching from DB (Output: Product object)
// Second call with same id: No output (returns from cache)
```

**Explanation:** @Cacheable caches method results. On first call, method executes and result is cached. Subsequent calls with same arguments return cached value without method execution. value specifies cache name, key is cache key (defaults to all parameters).

---

### Question 82: @CacheEvict to Clear Cache

```java
@Service
public class ProductService {
    @Cacheable("products")
    public Product findById(Long id) {
        return productRepository.findById(id).orElse(null);
    }
    
    @CacheEvict(value = "products", key = "#product.id")
    public Product update(Product product) {
        return productRepository.save(product);
    }
    
    @CacheEvict(value = "products", allEntries = true)
    public void deleteAll() {
        productRepository.deleteAll();
    }
}

// Output: update() removes specific entry, deleteAll() clears entire cache
```

**Explanation:** @CacheEvict removes entries from cache. Use key to remove specific entry or allEntries=true to clear entire cache. beforeInvocation=false (default) evicts after method success, beforeInvocation=true evicts before execution.

---

### Question 83: @CachePut to Update Cache

```java
@Service
public class UserService {
    @Cacheable(value = "users", key = "#id")
    public User findById(Long id) {
        return userRepository.findById(id).orElse(null);
    }
    
    @CachePut(value = "users", key = "#user.id")
    public User update(User user) {
        return userRepository.save(user);
    }
}

// Output: update() executes method AND updates cache with result
```

**Explanation:** @CachePut always executes method and updates cache with result. Unlike @Cacheable (skips execution if cached), @CachePut ensures cache stays synchronized with database after updates. Use for update operations.

---

### Question 84: Conditional Caching

```java
@Service
public class DataService {
    @Cacheable(value = "data", condition = "#length > 5", unless = "#result == null")
    public String getData(int length) {
        return dataRepository.fetch(length);
    }
}

// Output: 
// getData(3) -> not cached (condition false)
// getData(10) -> cached (if result not null)
```

**Explanation:** condition evaluates before method execution (uses parameters). unless evaluates after execution (uses #result). condition determines if caching should happen, unless prevents caching specific results. Useful for caching only large/valid results.

---

### Question 85: Redis Cache Configuration

```java
@Configuration
@EnableCaching
public class CacheConfig {
    @Bean
    public RedisCacheManager cacheManager(RedisConnectionFactory connectionFactory) {
        RedisCacheConfiguration config = RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(10))
            .serializeValuesWith(RedisSerializationContext.SerializationPair
                .fromSerializer(new GenericJackson2JsonRedisSerializer()));
        
        return RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(config)
            .build();
    }
}

// Output: Cache entries expire after 10 minutes, stored in Redis
```

**Explanation:** Spring Boot supports multiple cache providers. Redis is popular for distributed caching. RedisCacheManager configures TTL, serialization, and cache-specific settings. Requires spring-boot-starter-data-redis dependency. Shared cache across multiple application instances.

---

### Question 86: @Async Method Execution

```java
@Configuration
@EnableAsync
public class AsyncConfig {
    @Bean
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.initialize();
        return executor;
    }
}

@Service
public class EmailService {
    @Async
    public void sendEmail(String to, String message) {
        System.out.println("Sending email in thread: " + Thread.currentThread().getName());
        // Email sending logic
    }
}

// Output: Sends email in separate thread from pool
```

**Explanation:** @EnableAsync enables asynchronous method execution. @Async runs method in separate thread from configured executor. Method must be public and in Spring-managed bean. Calling @Async method from same class bypasses async (proxy limitation).

---

### Question 87: @Async with CompletableFuture

```java
@Service
public class DataService {
    @Async
    public CompletableFuture<String> fetchData(String source) {
        // Simulate delay
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return CompletableFuture.completedFuture("Data from " + source);
    }
}

@RestController
public class DataController {
    @Autowired
    private DataService dataService;
    
    @GetMapping("/data")
    public CompletableFuture<String> getData() {
        CompletableFuture<String> data1 = dataService.fetchData("DB");
        CompletableFuture<String> data2 = dataService.fetchData("API");
        
        return CompletableFuture.allOf(data1, data2)
            .thenApply(v -> data1.join() + ", " + data2.join());
    }
}

// Output: Both fetches run in parallel, combined result returned
```

**Explanation:** @Async methods can return CompletableFuture for non-blocking async operations. CompletableFuture.allOf() waits for multiple futures. join() retrieves result. This enables parallel processing and composition of async operations.

---

### Question 88: @Scheduled Fixed Rate

```java
@Component
@EnableScheduling
public class ScheduledTasks {
    @Scheduled(fixedRate = 5000)
    public void fixedRateTask() {
        System.out.println("Fixed rate task - " + System.currentTimeMillis());
    }
    
    @Scheduled(fixedDelay = 5000)
    public void fixedDelayTask() {
        System.out.println("Fixed delay task - " + System.currentTimeMillis());
    }
    
    @Scheduled(cron = "0 0 1 * * ?") // Daily at 1 AM
    public void cronTask() {
        System.out.println("Cron task executed");
    }
}

// Output: 
// fixedRate: Runs every 5s (regardless of execution time)
// fixedDelay: Waits 5s after previous execution completes
// cron: Runs at specified time
```

**Explanation:** @EnableScheduling enables task scheduling. fixedRate runs at fixed intervals from start time. fixedDelay waits after completion. cron uses cron expressions for complex schedules. All scheduled methods must return void and take no parameters.

---

### Question 89: Async Exception Handling

```java
@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {
    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return (ex, method, params) -> {
            System.err.println("Exception in async method: " + method.getName());
            System.err.println("Exception message: " + ex.getMessage());
        };
    }
}

@Service
public class AsyncService {
    @Async
    public void riskyOperation() {
        throw new RuntimeException("Async failure");
    }
}

// Output: Exception logged but doesn't propagate to caller
```

**Explanation:** Exceptions in @Async void methods are swallowed unless you configure AsyncUncaughtExceptionHandler. For CompletableFuture return types, exceptions are captured in the future. Always handle exceptions in async methods or configure global handler.

---

### Question 90: Cache with Multiple Cache Managers

```java
@Configuration
@EnableCaching
public class CacheConfig {
    @Bean
    @Primary
    public CacheManager redisCacheManager(RedisConnectionFactory factory) {
        return RedisCacheManager.create(factory);
    }
    
    @Bean
    public CacheManager caffeineCacheManager() {
        CaffeineCacheManager cacheManager = new CaffeineCacheManager("localCache");
        return cacheManager;
    }
}

@Service
public class DataService {
    @Cacheable(value = "remoteCache", cacheManager = "redisCacheManager")
    public String getRemoteData() {}
    
    @Cacheable(value = "localCache", cacheManager = "caffeineCacheManager")
    public String getLocalData() {}
}

// Output: Different methods use different cache managers
```

**Explanation:** Multiple cache managers enable different caching strategies. Specify cacheManager in @Cacheable to choose which manager to use. @Primary marks default manager. Useful for combining in-memory (fast) and distributed (shared) caches.

---

## Testing & Advanced Topics

### Question 91: @WebMvcTest for Controller Testing

```java
@WebMvcTest(UserController.class)
public class UserControllerTest {
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private UserService userService;
    
    @Test
    public void testGetUser() throws Exception {
        when(userService.findById(1L)).thenReturn(new User(1L, "John"));
        
        mockMvc.perform(get("/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("John"));
    }
}

// Output: Test passes, only web layer loaded (not full context)
```

**Explanation:** @WebMvcTest loads only web layer (controllers, filters, etc.), not services or repositories. MockMvc simulates HTTP requests. @MockBean creates mock for dependencies. Faster than @SpringBootTest as it loads minimal context.

---

### Question 92: @DataJpaTest for Repository Testing

```java
@DataJpaTest
public class UserRepositoryTest {
    @Autowired
    private TestEntityManager entityManager;
    
    @Autowired
    private UserRepository repository;
    
    @Test
    public void testFindByName() {
        User user = new User("John", "john@example.com");
        entityManager.persist(user);
        entityManager.flush();
        
        User found = repository.findByName("John");
        assertThat(found.getEmail()).isEqualTo("john@example.com");
    }
}

// Output: Test uses in-memory H2 database, transaction rolled back after test
```

**Explanation:** @DataJpaTest configures in-memory database and JPA components. Tests are @Transactional by default (rolled back after each test). TestEntityManager manages test data. Only JPA repositories and entities are loaded, making tests fast.

---

### Question 93: @MockBean vs @Mock

```java
// @Mock (Mockito) - Plain unit test
@ExtendWith(MockitoExtension.class)
public class ServiceTest {
    @Mock
    private Repository repository;
    
    @InjectMocks
    private Service service;
    
    // No Spring context
}

// @MockBean (Spring Boot) - Integration test with mocked bean
@SpringBootTest
public class ServiceIntegrationTest {
    @MockBean
    private Repository repository;
    
    @Autowired
    private Service service; // Real bean with mocked dependency
    
    // Spring context loaded
}

// @Mock: Plain Mockito, no Spring
// @MockBean: Replaces bean in Spring context
```

**Explanation:** @Mock is pure Mockito, no Spring involvement. @MockBean adds mock to Spring context, replacing actual bean. Use @Mock for unit tests (faster), @MockBean for integration tests needing Spring context. @MockBean is Spring Boot specific.

---

### Question 94: @TestConfiguration for Test Beans

```java
@SpringBootTest
public class ServiceTest {
    @TestConfiguration
    static class TestConfig {
        @Bean
        @Primary
        public ExternalService externalService() {
            return new MockExternalService(); // Use mock instead of real service
        }
    }
    
    @Autowired
    private ServiceToTest service;
    
    @Test
    public void test() {
        // Uses MockExternalService
    }
}
```

**Explanation:** @TestConfiguration defines beans only for tests. Can be inner class or separate. Use @Primary to override production beans. Useful for providing test doubles or specialized test configurations without affecting production code.

---

### Question 95: @Sql for Test Data

```java
@SpringBootTest
@Sql("/test-data.sql") // Runs before each test method
@Sql(scripts = "/cleanup.sql", executionPhase = Sql.ExecutionPhase.AFTER_TEST_METHOD)
public class IntegrationTest {
    @Autowired
    private UserRepository userRepository;
    
    @Test
    public void testWithData() {
        List<User> users = userRepository.findAll();
        assertThat(users).hasSize(5);
    }
}

// test-data.sql:
// INSERT INTO users (name, email) VALUES ('John', 'john@example.com');
```

**Explanation:** @Sql executes SQL scripts before/after tests. Default is BEFORE_TEST_METHOD. Use for loading test data or cleanup. More maintainable than Java code for complex data setup. Scripts run in transaction if test is transactional.

---

### Question 96: WebFlux Reactive Controller

```java
@RestController
public class ReactiveController {
    @GetMapping("/users")
    public Flux<User> getAllUsers() {
        return userRepository.findAll(); // Returns Flux (0..N items)
    }
    
    @GetMapping("/users/{id}")
    public Mono<User> getUser(@PathVariable Long id) {
        return userRepository.findById(id); // Returns Mono (0..1 item)
    }
    
    @PostMapping("/users")
    public Mono<User> createUser(@RequestBody Mono<User> userMono) {
        return userMono.flatMap(userRepository::save);
    }
}

// Output: Non-blocking reactive streams
```

**Explanation:** Spring WebFlux enables reactive programming. Mono represents 0-1 items, Flux represents 0-N items. Operations are non-blocking and event-driven. Use for high-concurrency scenarios. Requires reactive repositories (R2DBC, not JPA).

---

### Question 97: Kafka Producer and Consumer

```java
// Producer
@Service
public class KafkaProducer {
    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;
    
    public void sendMessage(String message) {
        kafkaTemplate.send("topic-name", message);
    }
}

// Consumer
@Service
public class KafkaConsumer {
    @KafkaListener(topics = "topic-name", groupId = "group-1")
    public void consume(String message) {
        System.out.println("Received: " + message);
    }
}

// Output: Producer sends message, Consumer receives it asynchronously
```

**Explanation:** KafkaTemplate sends messages to topics. @KafkaListener consumes messages from topics. groupId enables load balancing across consumers. Spring Boot auto-configures Kafka with spring-kafka dependency. Messages processed asynchronously.

---

### Question 98: CommandLineRunner vs ApplicationRunner

```java
@Component
public class MyCommandLineRunner implements CommandLineRunner {
    @Override
    public void run(String... args) throws Exception {
        System.out.println("CommandLineRunner: " + Arrays.toString(args));
        // args = ["--arg1=value1", "--arg2=value2"]
    }
}

@Component
public class MyApplicationRunner implements ApplicationRunner {
    @Override
    public void run(ApplicationArguments args) throws Exception {
        System.out.println("ApplicationRunner: " + args.getOptionNames());
        // Parsed options: [arg1, arg2]
        System.out.println("arg1 value: " + args.getOptionValues("arg1"));
    }
}

// Output: Both run at startup, ApplicationRunner provides better argument parsing
```

**Explanation:** Both interfaces run code after application startup. CommandLineRunner receives raw String[] args. ApplicationRunner gets parsed ApplicationArguments with getOptionNames(), getOptionValues(). Use ApplicationRunner for better argument handling.

---

### Question 99: Custom Auto-Configuration

```java
@Configuration
@ConditionalOnClass(SomeLibrary.class)
@EnableConfigurationProperties(CustomProperties.class)
public class CustomAutoConfiguration {
    @Bean
    @ConditionalOnMissingBean
    public CustomService customService(CustomProperties properties) {
        return new CustomService(properties);
    }
}

// Create META-INF/spring.factories:
// org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
// com.example.CustomAutoConfiguration

// Output: Auto-configuration runs if SomeLibrary is on classpath
```

**Explanation:** Auto-configuration automatically configures beans based on classpath and properties. @ConditionalOnClass checks for class presence. @ConditionalOnMissingBean creates bean only if none exists (allows override). Register in spring.factories or use @AutoConfiguration (Spring Boot 2.7+).

---

### Question 100: Multiple Datasource Configuration

```java
@Configuration
public class DataSourceConfig {
    @Bean
    @Primary
    @ConfigurationProperties("spring.datasource.primary")
    public DataSource primaryDataSource() {
        return DataSourceBuilder.create().build();
    }
    
    @Bean
    @ConfigurationProperties("spring.datasource.secondary")
    public DataSource secondaryDataSource() {
        return DataSourceBuilder.create().build();
    }
    
    @Bean
    @Primary
    public JdbcTemplate primaryJdbcTemplate(@Qualifier("primaryDataSource") DataSource ds) {
        return new JdbcTemplate(ds);
    }
    
    @Bean
    public JdbcTemplate secondaryJdbcTemplate(@Qualifier("secondaryDataSource") DataSource ds) {
        return new JdbcTemplate(ds);
    }
}

// application.properties:
// spring.datasource.primary.url=jdbc:mysql://localhost/db1
// spring.datasource.secondary.url=jdbc:mysql://localhost/db2

// Output: Two separate datasources configured
```

**Explanation:** Multiple datasources require explicit configuration. @Primary marks default datasource. Each datasource needs separate EntityManagerFactory and TransactionManager for JPA. Use @Qualifier to specify which datasource to inject. Useful for read/write splitting or multi-tenant applications.

---

## Conclusion

These 100 questions cover the most critical and tricky aspects of Spring Boot:

- **Bean Management**: Lifecycle, scopes, and initialization
- **Dependency Injection**: Various injection types and resolution strategies
- **Configuration**: Properties, profiles, and conditional beans
- **AOP**: Aspect-oriented programming for cross-cutting concerns
- **Data Access**: JPA, Hibernate, and transaction management
- **REST APIs**: Controllers, exception handling, and validation
- **Security**: Authentication, authorization, and best practices
- **Advanced Topics**: Caching, async processing, reactive programming, testing

Understanding these concepts with their outputs and edge cases will help you master Spring Boot and handle real-world scenarios effectively. Always test your understanding by running code examples and experimenting with variations.

---

**Tips for Interview Preparation:**

1. Run each example to see actual behavior
2. Understand the "why" behind each output
3. Know common pitfalls (circular dependencies, proxy limitations, etc.)
4. Practice explaining concepts clearly
5. Be ready to discuss alternatives and trade-offs
6. Know when to use each approach in production
7. Understand performance implications
8. Keep up with Spring Boot version changes

**Best Practices:**

- Prefer constructor injection over field injection
- Use @ConfigurationProperties over scattered @Value
- Always handle exceptions in async methods
- Enable transaction management explicitly where needed
- Use appropriate bean scopes for your use case
- Configure proper cache eviction strategies
- Test with @WebMvcTest and @DataJpaTest for focused testing
- Use Spring Boot Actuator for production monitoring

Good luck with your Spring Boot journey! 🚀