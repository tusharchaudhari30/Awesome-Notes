# Spring boot kafka

## Kafka Producer

```java
package com.example.kafkademo;

import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;

import java.util.HashMap;
import java.util.Map;

@Configuration
public class KafkaProducerConfig {

    @Value("${spring.kafka.bootstrap-servers}")
    private String bootstrapServers;

    @Bean
    public ProducerFactory<String, String> producerFactory() {
        Map<String, Object> configProps = new HashMap<>();
        // Specify the Kafka broker address
        configProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        // Specify the serializer class for the message keys
        configProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        // Specify the serializer class for the message values
        configProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        // Other potential configurations like retries, batch size, acks, etc.
        // configProps.put(ProducerConfig.RETRIES_CONFIG, 0);

        return new DefaultKafkaProducerFactory<>(configProps);
    }

    @Bean
    public KafkaTemplate<String, String> kafkaTemplate() {
        return new KafkaTemplate<>(producerFactory());
    }
}
```

## Send methods choice

- **Fire-and-forget:** Maximizes throughput but ignores per-message errors; use only where occasional loss is acceptable and rely on metrics for detection.
- **Synchronous sends:** Simplify error handling by blocking for results, but can throttle throughput; reserve for low-volume critical flows.
- **Async with callbacks:** Offers the best balance, enabling non-blocking pipelines with explicit success/failure handling, retries, and DLT routing.
- **Correlation ID:** Always propagate a correlation ID in headers so callbacks can associate broker results with upstream requests.

```java
// Fire-and-forget
template.send("orders", "user-1", "payload");

// Synchronous
template.send("orders", "user-1", "payload").get();

// Asynchronous with callback
template.send("orders", "user-1", "payload")
    .whenComplete((md, ex) -> { /* handle success/failure */ });
```

## acks (all, 1, 0)

- **Meaning:** Controls how many broker acknowledgments are required before the send is considered successful.
- **Effects:**
  - **all:** Wait for leader and all in-sync replicas; highest durability, slightly higher latency.
  - **1:** Wait for leader only; moderate durability, lower latency.
  - **0:** Don’t wait; lowest latency, potential silent loss.

## Exactly once

- Enable idempotent producer with <code>acks=all</code> to deduplicate retries and ensure durability.
- This eliminates duplicates from producer retries, but does not bind consumed offsets; use when only producing (no read-process-write chain).

```yaml
spring:
  kafka:
    producer:
      acks: all
      properties:
        enable.idempotence: true
```

## Atleast once

- Disable <code>enable-auto-commit</code> so commits occur only after successful handling.
- Use manual acknowledgment to commit offsets after the work is done; keep handlers idempotent to tolerate replays.

```yaml
spring:
  kafka:
    consumer:
      group-id: orders-atleast
      enable-auto-commit: false
      auto-offset-reset: latest
```

## Manual commit (at-least-once)

- With <code>enable.auto.commit=false</code>, acknowledge offsets only after processing completes, ensuring replays after crashes rather than data loss; handlers must be idempotent to tolerate duplicates.
- Use <code>AckMode.MANUAL_IMMEDIATE</code> to commit per-record for minimal replay, or <code>AckMode.BATCH</code> to commit per-batch for higher throughput; align with downstream idempotency guarantees.
- Pair with cooperative rebalancing to reduce disruption during scaling or deployments while maintaining correctness.

```yaml
spring:
  kafka:
    consumer:
      enable-auto-commit: false
```

```java
import org.springframework.kafka.support.Acknowledgment;

@KafkaListener(topics = "orders", groupId = "orders-manual", containerFactory = "manualAckContainerFactory")
public void handleManual(String value, Acknowledgment ack) {
  // process safely (idempotent)
  ack.acknowledge(); // commit after success
}
```

```java
import org.springframework.context.annotation.Bean;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.ConsumerFactory;

@Bean
public ConcurrentKafkaListenerContainerFactory<String, String> manualAckContainerFactory(
    ConsumerFactory<String, String> cf) {
  var factory = new ConcurrentKafkaListenerContainerFactory<String, String>();
  factory.setConsumerFactory(cf);
  factory.getContainerProperties().setAckMode(
      org.springframework.kafka.listener.ContainerProperties.AckMode.MANUAL_IMMEDIATE);
  return factory;
}
```

# Spring For KAFKA DLT

Create a comprehensive error handler with DLQ support:

```java
@Configuration
public class KafkaErrorHandlerConfig {

    @Bean
    public DefaultErrorHandler defaultErrorHandler(
            KafkaTemplate<String, Object> kafkaTemplate) {

        // Configure Dead Letter Publishing Recoverer
        DeadLetterPublishingRecoverer recoverer = new DeadLetterPublishingRecoverer(
            kafkaTemplate,
            // Route to DLT topic with single partition
            (record, exception) -> new TopicPartition(
                record.topic() + ".DLT", 0)
        );

        // Configure exponential backoff
        ExponentialBackOffWithMaxRetries backOff =
            new ExponentialBackOffWithMaxRetries(3);
        backOff.setInitialInterval(1000L);     // 1 second
        backOff.setMultiplier(2.0);            // Double each retry
        backOff.setMaxInterval(10000L);        // Max 10 seconds

        // Create error handler
        DefaultErrorHandler errorHandler = new DefaultErrorHandler(recoverer, backOff);

        // Add non-retryable exceptions
        errorHandler.addNotRetryableExceptions(
            ValidationException.class,
            MethodArgumentNotValidException.class,
            DeserializationException.class
        );

        return errorHandler;
    }

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, Order>
            kafkaListenerContainerFactory(
                ConsumerFactory<String, Order> consumerFactory,
                DefaultErrorHandler errorHandler) {

        ConcurrentKafkaListenerContainerFactory<String, Order> factory =
            new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory);
        factory.setCommonErrorHandler(errorHandler);

        return factory;
    }
}
```

# Spring Boot

## Bean Life Cycle

![alt text](image.png)

## Custom Exception Handling

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    // Handle Resource Not Found
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFoundException(
        ResourceNotFoundException ex, WebRequest request) {
        ErrorResponse error = custom class;
        return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
    }
}
```

## AOP

![alt text](image-1.png)

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

### Web Clients

```java
    public Employee createEmployee(Employee employee) {
        return restTemplate.postForObject(BASE_URL, employee, Employee.class);
    }

    public Employee createEmployee(Employee employee) {
        return restTemplate.postForObject(BASE_URL, employee, Employee.class);
    }

    public List<Employee> getAllEmployees() {
        return restClient.get()
            .uri("/employees")
            .retrieve()
            .body(new ParameterizedTypeReference<List<Employee>>() {});
    }

    public Employee createEmployee(Employee employee) {
        return restClient.post()
            .uri("/employees")
            .contentType(MediaType.APPLICATION_JSON)
            .body(employee)
            .retrieve()
            .body(Employee.class);
    }
    public Mono<Employee> createEmployee(Employee employee) {
        return webClient.post()
            .uri("/employees")
            .contentType(MediaType.APPLICATION_JSON)
            .body(Mono.just(employee), Employee.class)
            .retrieve()
            .bodyToMono(Employee.class);
    }

```

### Feign client

```java
// This Feign client will communicate with a service named "address-service"
@FeignClient(name = "address-service")
public interface AddressClient {

    // This method maps to a GET request on the address-service
    // It retrieves an address using the employee's ID
    @GetMapping("/addresses/employee/{id}")
    AddressResponse getAddressByEmployeeId(@PathVariable("id") Long id);
}
```

```yaml
my-service:
  url: https://api.example.com/v1
```

### File Controller

```java
@RestController
@RequestMapping("/api/files")
@RequiredArgsConstructor
public class FileController {

    private final FileStorageService fileStorageService;

    @PostMapping("/upload")
    public ResponseEntity<FileUploadResponse> uploadFile(
            @RequestParam("file") MultipartFile file) {
        String fileName = fileStorageService.storeFile(file);

        String fileDownloadUri = ServletUriComponentsBuilder.fromCurrentContextPath()
            .path("/api/files/download/")
            .path(fileName)
            .toUriString();

        FileUploadResponse response = new FileUploadResponse(
            fileName,
            fileDownloadUri,
            file.getContentType(),
            file.getSize()
        );

        return ResponseEntity.ok(response);
    }

    @PostMapping("/uploadMultiple")
    public ResponseEntity<List<FileUploadResponse>> uploadMultipleFiles(
            @RequestParam("files") MultipartFile[] files) {
        List<FileUploadResponse> responses = Arrays.stream(files)
            .map(file -> {
                String fileName = fileStorageService.storeFile(file);
                String fileDownloadUri = ServletUriComponentsBuilder.fromCurrentContextPath()
                    .path("/api/files/download/")
                    .path(fileName)
                    .toUriString();
                return new FileUploadResponse(fileName, fileDownloadUri,
                    file.getContentType(), file.getSize());
            })
            .collect(Collectors.toList());

        return ResponseEntity.ok(responses);
    }

    @GetMapping("/download/{fileName:.+}")
    public ResponseEntity<Resource> downloadFile(
            @PathVariable String fileName, HttpServletRequest request) {
        Resource resource = fileStorageService.loadFileAsResource(fileName);

        String contentType = null;
        try {
            contentType = request.getServletContext().getMimeType(resource.getFile().getAbsolutePath());
        } catch (IOException ex) {
            contentType = "application/octet-stream";
        }

        return ResponseEntity.ok()
            .contentType(MediaType.parseMediaType(contentType))
            .header(HttpHeaders.CONTENT_DISPOSITION,
                "attachment; filename=\"" + resource.getFilename() + "\"")
            .body(resource);
    }
}
```

# JPA

### Key Annotations

| Annotation        | Purpose                         | Example                                               |
| ----------------- | ------------------------------- | ----------------------------------------------------- |
| `@Entity`         | Marks class as JPA entity       | `@Entity`                                             |
| `@Table`          | Specifies table name            | `@Table(name = "employees")`                          |
| `@Id`             | Marks primary key field         | `@Id`                                                 |
| `@GeneratedValue` | Auto-generate primary key       | `@GeneratedValue(strategy = GenerationType.IDENTITY)` |
| `@Column`         | Maps field to database column   | `@Column(name = "first_name", length = 50)`           |
| `@Transient`      | Excludes field from persistence | `@Transient`                                          |
| `@Temporal`       | Maps Date/Time types            | `@Temporal(TemporalType.DATE)`                        |
| `@Enumerated`     | Maps enum types                 | `@Enumerated(EnumType.STRING)`                        |
| `@Lob`            | Maps large objects (BLOB/CLOB)  | `@Lob`                                                |

### Generation Strategies

![alt text](image-2.png)

```java
// AUTO - Let JPA provider choose
@GeneratedValue(strategy = GenerationType.AUTO)

// IDENTITY - Database auto-increment
@GeneratedValue(strategy = GenerationType.IDENTITY)

// SEQUENCE - Database sequence
@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "emp_seq")
@SequenceGenerator(name = "emp_seq", sequenceName = "employee_sequence", allocationSize = 1)

// TABLE - Uses a database table
@GeneratedValue(strategy = GenerationType.TABLE, generator = "emp_table")
@TableGenerator(name = "emp_table", table = "id_gen", pkColumnName = "gen_name", valueColumnName = "gen_val")
```

## Entity Relationships

### Relationship

```java
    @OneToOne(cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JoinColumn(name = "address_id", referencedColumnName = "id")
    private Address address;

    @OneToMany(mappedBy = "department", cascade = CascadeType.ALL,
               orphanRemoval = true, fetch = FetchType.LAZY)
    private List<Employee> employees = new ArrayList<>();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "department_id")
    private Department department;

    @ManyToMany(cascade = {CascadeType.PERSIST, CascadeType.MERGE})
    @JoinTable(
        name = "student_course",
        joinColumns = @JoinColumn(name = "student_id"),
        inverseJoinColumns = @JoinColumn(name = "course_id")
    )
    private Set<Course> courses = new HashSet<>();

    // LAZY (default for @OneToMany and @ManyToMany)
    @OneToMany(fetch = FetchType.LAZY)
    private List<Employee> employees;

    // EAGER (default for @ManyToOne and @OneToOne)
    @ManyToOne(fetch = FetchType.EAGER)
    private Department department;
```

### Cascade Types

| Cascade Type          | Description                |
| --------------------- | -------------------------- |
| `CascadeType.PERSIST` | Cascade save operations    |
| `CascadeType.MERGE`   | Cascade merge operations   |
| `CascadeType.REMOVE`  | Cascade delete operations  |
| `CascadeType.REFRESH` | Cascade refresh operations |
| `CascadeType.DETACH`  | Cascade detach operations  |
| `CascadeType.ALL`     | All of the above           |

### Paging and Sorting

```java
    public Page<Employee> getEmployeesMultiSort(int page, int size) {
        Sort sort = Sort.by("department").ascending()
                       .and(Sort.by("salary").descending());

        Pageable pageable = PageRequest.of(page, size, sort);
        return employeeRepository.findAll(pageable);
    }
```

### Stored Procedures

```java
@Entity
@NamedStoredProcedureQuery(
    name = "Employee.calculateBonus",
    procedureName = "calculate_employee_bonus",
    parameters = {
        @StoredProcedureParameter(mode = ParameterMode.IN, name = "emp_id", type = Long.class),
        @StoredProcedureParameter(mode = ParameterMode.OUT, name = "bonus", type = Double.class)
    }
)
public class Employee {
    // Entity fields
}

@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    @Procedure(name = "calculate_employee_bonus")
    Double calculateBonus(@Param("emp_id") Long employeeId);
}
```

# SQL

## Keys and Constraints

```sql
-- Parent Table: Departments (now using a composite PRIMARY KEY)
CREATE TABLE Departments (
    DepartmentName VARCHAR(50) NOT NULL,
    Location VARCHAR(50) NOT NULL DEFAULT 'Head Office',
    DeptCode VARCHAR(10) UNIQUE, -- UNIQUE constraint

    -- Composite PRIMARY KEY defined at the table level
    CONSTRAINT pk_department_composite PRIMARY KEY (DepartmentName, Location)
);


-- Child Table: Employees
CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY, -- Primary Key, implicitly NOT NULL and UNIQUE
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Salary DECIMAL(10, 2) CHECK (Salary >= 30000.00), -- CHECK constraint
    HireDate DATE DEFAULT CURRENT_DATE, -- DEFAULT constraint

    -- Columns to link to the composite primary key in the Departments table
    DeptNameRef VARCHAR(50) NOT NULL,
    DeptLocationRef VARCHAR(50) NOT NULL,

    -- Foreign Key definition referencing the composite key of the Departments table
    CONSTRAINT fk_department_link
        FOREIGN KEY (DeptNameRef, DeptLocationRef)
        REFERENCES Departments(DepartmentName, Location)
        ON DELETE RESTRICT -- Prevent deletion of a department if employees exist
);
```

### CREATE INDEX

Improve query performance on frequently filtered columns.

```sql
-- Create a nonclustered index on department for faster lookups
CREATE INDEX idx_employees_department
ON employees(department);
```

### ADD/DROP Column

Modify table structures without full recreation.

```sql
-- Add a phone number column to employees
ALTER TABLE employees
ADD phone VARCHAR(15);

-- Remove the phone column if no longer needed
ALTER TABLE employees
DROP COLUMN phone;
```
