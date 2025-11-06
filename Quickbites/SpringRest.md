# Spring Boot REST API - Complete Interview Guide

## From Basics to Expert Level

---

## Table of Contents

1. [Introduction to REST & Spring Boot](#introduction)
2. [Core Annotations](#core-annotations)
3. [Building Basic REST Controllers](#basic-controllers)
4. [Request & Response Handling](#request-response)
5. [Exception Handling](#exception-handling)
6. [Validation](#validation)
7. [HTTP Status Codes & ResponseEntity](#response-entity)
8. [Content Negotiation](#content-negotiation)
9. [HATEOAS (Hypermedia)](#hateoas)
10. [API Documentation (Swagger/OpenAPI)](#swagger)
11. [Security & JWT Authentication](#security)
12. [Testing REST APIs](#testing)
13. [Asynchronous REST APIs](#async)
14. [API Versioning](#versioning)
15. [REST Clients (RestTemplate, WebClient, RestClient)](#rest-clients)
16. [File Upload & Download](#file-operations)
17. [Pagination & Sorting](#pagination)
18. [Caching](#caching)
19. [CORS Configuration](#cors)
20. [Monitoring with Actuator](#actuator)
21. [Best Practices](#best-practices)
22. [Reactive REST with WebFlux](#webflux)

---

## 1. Introduction to REST & Spring Boot {#introduction}

### What is REST?

**REST** (Representational State Transfer) is an architectural style for building web services that use HTTP methods to perform CRUD operations.

**Key Principles:**

- **Stateless**: Each request contains all information needed
- **Client-Server**: Separation of concerns
- **Cacheable**: Responses can be cached
- **Uniform Interface**: Consistent resource identification
- **Layered System**: Architecture can be composed of layers

**HTTP Methods:**

- **GET**: Retrieve resources
- **POST**: Create new resources
- **PUT**: Update/replace entire resource
- **PATCH**: Partial update of resource
- **DELETE**: Remove resources

### Why Spring Boot for REST?

- Auto-configuration
- Embedded servers (Tomcat, Jetty, Undertow)
- Production-ready features (Actuator)
- Easy dependency management
- Convention over configuration

---

## 2. Core Annotations {#core-annotations}

### @RestController

Combines `@Controller` and `@ResponseBody`. Methods return data directly (usually JSON).

```java
@RestController
@RequestMapping("/api")
public class EmployeeController {
    // Methods here
}
```

### @RequestMapping

Maps HTTP requests to handler methods. Can specify method, path, headers, params, etc.

```java
@RequestMapping(value = "/employees", method = RequestMethod.GET)
public List<Employee> getAllEmployees() {
    return employeeService.findAll();
}
```

### Specialized Mapping Annotations

More concise alternatives to `@RequestMapping`:

```java
@GetMapping("/employees")           // GET request
@PostMapping("/employees")          // POST request
@PutMapping("/employees/{id}")      // PUT request
@PatchMapping("/employees/{id}")    // PATCH request
@DeleteMapping("/employees/{id}")   // DELETE request
```

### @PathVariable

Extracts values from URI path.

```java
@GetMapping("/employees/{id}")
public Employee getEmployee(@PathVariable Long id) {
    return employeeService.findById(id);
}

// Multiple path variables
@GetMapping("/departments/{deptId}/employees/{empId}")
public Employee getEmployeeInDept(
    @PathVariable Long deptId,
    @PathVariable Long empId) {
    return employeeService.findByDeptAndId(deptId, empId);
}

// Optional path variable with default
@GetMapping("/employees/{id}")
public Employee getEmployee(
    @PathVariable(required = false) Long id) {
    return id != null ? employeeService.findById(id) : null;
}
```

### @RequestParam

Extracts query parameters from URL.

```java
// URL: /employees/search?name=John&age=30
@GetMapping("/employees/search")
public List<Employee> searchEmployees(
    @RequestParam String name,
    @RequestParam(required = false, defaultValue = "0") Integer age) {
    return employeeService.search(name, age);
}
```

### @RequestBody

Binds HTTP request body to method parameter (JSON/XML to Java object).

```java
@PostMapping("/employees")
public Employee createEmployee(@RequestBody Employee employee) {
    return employeeService.save(employee);
}
```

### @ResponseStatus

Sets HTTP status code for response.

```java
@PostMapping("/employees")
@ResponseStatus(HttpStatus.CREATED)
public Employee createEmployee(@RequestBody Employee employee) {
    return employeeService.save(employee);
}
```

---

## 3. Building Basic REST Controllers {#basic-controllers}

### Complete CRUD Example

**Entity:**

```java
package com.example.demo.model;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "employees")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Employee {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String firstName;

    @Column(nullable = false)
    private String lastName;

    @Column(unique = true, nullable = false)
    private String email;

    private String department;
    private Double salary;
}
```

**Repository:**

```java
package com.example.demo.repository;

import com.example.demo.model.Employee;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {
    List<Employee> findByDepartment(String department);
}
```

**Service:**

```java
package com.example.demo.service;

import com.example.demo.model.Employee;
import com.example.demo.repository.EmployeeRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
@RequiredArgsConstructor
public class EmployeeService {

    private final EmployeeRepository employeeRepository;

    public List<Employee> findAll() {
        return employeeRepository.findAll();
    }

    public Employee findById(Long id) {
        return employeeRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Employee not found with id: " + id));
    }

    public Employee save(Employee employee) {
        return employeeRepository.save(employee);
    }

    public Employee update(Long id, Employee employeeDetails) {
        Employee employee = findById(id);
        employee.setFirstName(employeeDetails.getFirstName());
        employee.setLastName(employeeDetails.getLastName());
        employee.setEmail(employeeDetails.getEmail());
        employee.setDepartment(employeeDetails.getDepartment());
        employee.setSalary(employeeDetails.getSalary());
        return employeeRepository.save(employee);
    }

    public void delete(Long id) {
        Employee employee = findById(id);
        employeeRepository.delete(employee);
    }
}
```

**Controller:**

```java
package com.example.demo.controller;

import com.example.demo.model.Employee;
import com.example.demo.service.EmployeeService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/employees")
@RequiredArgsConstructor
public class EmployeeController {

    private final EmployeeService employeeService;

    // GET all employees
    @GetMapping
    public ResponseEntity<List<Employee>> getAllEmployees() {
        List<Employee> employees = employeeService.findAll();
        return ResponseEntity.ok(employees);
    }

    // GET employee by ID
    @GetMapping("/{id}")
    public ResponseEntity<Employee> getEmployeeById(@PathVariable Long id) {
        Employee employee = employeeService.findById(id);
        return ResponseEntity.ok(employee);
    }

    // POST - Create new employee
    @PostMapping
    public ResponseEntity<Employee> createEmployee(@RequestBody Employee employee) {
        Employee savedEmployee = employeeService.save(employee);
        return ResponseEntity.status(HttpStatus.CREATED).body(savedEmployee);
    }

    // PUT - Update employee
    @PutMapping("/{id}")
    public ResponseEntity<Employee> updateEmployee(
            @PathVariable Long id,
            @RequestBody Employee employeeDetails) {
        Employee updatedEmployee = employeeService.update(id, employeeDetails);
        return ResponseEntity.ok(updatedEmployee);
    }

    // DELETE - Remove employee
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteEmployee(@PathVariable Long id) {
        employeeService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
```

---

## 4. Request & Response Handling {#request-response}

### @RequestHeader

Access HTTP headers.

```java
@GetMapping("/employees")
public List<Employee> getEmployees(
    @RequestHeader("User-Agent") String userAgent,
    @RequestHeader(value = "Authorization", required = false) String token) {
    // Use header values
    return employeeService.findAll();
}
```

### @CookieValue

Access cookies.

```java
@GetMapping("/preferences")
public String getPreferences(
    @CookieValue(name = "theme", defaultValue = "light") String theme) {
    return "User theme: " + theme;
}
```

### Request Body with Validation

```java
@PostMapping("/employees")
public ResponseEntity<Employee> createEmployee(
    @Valid @RequestBody Employee employee) {
    Employee saved = employeeService.save(employee);
    return ResponseEntity.status(HttpStatus.CREATED).body(saved);
}
```

### Multiple @RequestParam

```java
@GetMapping("/search")
public List<Employee> search(
    @RequestParam(required = false) String name,
    @RequestParam(required = false) String department,
    @RequestParam(required = false, defaultValue = "0") Integer minSalary) {
    return employeeService.search(name, department, minSalary);
}
```

---

## 5. Exception Handling {#exception-handling}

### Custom Exception

```java
package com.example.demo.exception;

public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}

public class BadRequestException extends RuntimeException {
    public BadRequestException(String message) {
        super(message);
    }
}
```

### Error Response DTO

```java
package com.example.demo.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@AllArgsConstructor
public class ErrorResponse {
    private LocalDateTime timestamp;
    private int status;
    private String error;
    private String message;
    private String path;
}
```

### Global Exception Handler

```java
package com.example.demo.exception;

import com.example.demo.dto.ErrorResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.context.request.WebRequest;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFound(
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

    @ExceptionHandler(BadRequestException.class)
    public ResponseEntity<ErrorResponse> handleBadRequest(
            BadRequestException ex, WebRequest request) {
        ErrorResponse error = new ErrorResponse(
            LocalDateTime.now(),
            HttpStatus.BAD_REQUEST.value(),
            "Bad Request",
            ex.getMessage(),
            request.getDescription(false).replace("uri=", "")
        );
        return new ResponseEntity<>(error, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, Object>> handleValidationExceptions(
            MethodArgumentNotValidException ex) {
        Map<String, Object> errors = new HashMap<>();
        errors.put("timestamp", LocalDateTime.now());
        errors.put("status", HttpStatus.BAD_REQUEST.value());

        Map<String, String> fieldErrors = new HashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(error ->
            fieldErrors.put(error.getField(), error.getDefaultMessage())
        );
        errors.put("errors", fieldErrors);

        return new ResponseEntity<>(errors, HttpStatus.BAD_REQUEST);
    }

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

## 6. Validation {#validation}

### Validation Annotations

Add dependency:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

**Entity with Validation:**

```java
package com.example.demo.model;

import jakarta.validation.constraints.*;
import lombok.Data;

@Data
public class Employee {

    private Long id;

    @NotBlank(message = "First name is required")
    @Size(min = 2, max = 50, message = "First name must be between 2 and 50 characters")
    private String firstName;

    @NotBlank(message = "Last name is required")
    private String lastName;

    @NotBlank(message = "Email is required")
    @Email(message = "Email should be valid")
    private String email;

    @NotNull(message = "Department is required")
    private String department;

    @Min(value = 0, message = "Salary must be positive")
    @Max(value = 1000000, message = "Salary cannot exceed 1,000,000")
    private Double salary;

    @Pattern(regexp = "^\\d{10}$", message = "Phone number must be 10 digits")
    private String phoneNumber;

    @Past(message = "Date of birth must be in the past")
    private LocalDate dateOfBirth;
}
```

**Controller with Validation:**

```java
@PostMapping("/employees")
public ResponseEntity<Employee> createEmployee(
        @Valid @RequestBody Employee employee,
        BindingResult result) {

    if (result.hasErrors()) {
        // Handle validation errors
        throw new BadRequestException("Validation failed");
    }

    Employee saved = employeeService.save(employee);
    return ResponseEntity.status(HttpStatus.CREATED).body(saved);
}
```

### Custom Validator

```java
// Custom annotation
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = AgeValidator.class)
public @interface ValidAge {
    String message() default "Age must be between 18 and 65";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
    int min() default 18;
    int max() default 65;
}

// Validator implementation
public class AgeValidator implements ConstraintValidator<ValidAge, Integer> {
    private int min;
    private int max;

    @Override
    public void initialize(ValidAge constraintAnnotation) {
        this.min = constraintAnnotation.min();
        this.max = constraintAnnotation.max();
    }

    @Override
    public boolean isValid(Integer age, ConstraintValidatorContext context) {
        return age != null && age >= min && age <= max;
    }
}

// Usage
public class Employee {
    @ValidAge(min = 21, max = 60)
    private Integer age;
}
```

---

## 7. HTTP Status Codes & ResponseEntity {#response-entity}

### Common HTTP Status Codes

- **200 OK**: Successful GET, PUT, PATCH
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Invalid request
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

### ResponseEntity Examples

```java
@RestController
@RequestMapping("/api/employees")
public class EmployeeController {

    // 200 OK
    @GetMapping("/{id}")
    public ResponseEntity<Employee> getEmployee(@PathVariable Long id) {
        Employee employee = employeeService.findById(id);
        return ResponseEntity.ok(employee);
    }

    // 201 Created with Location header
    @PostMapping
    public ResponseEntity<Employee> createEmployee(@RequestBody Employee employee) {
        Employee saved = employeeService.save(employee);
        URI location = ServletUriComponentsBuilder
            .fromCurrentRequest()
            .path("/{id}")
            .buildAndExpand(saved.getId())
            .toUri();
        return ResponseEntity.created(location).body(saved);
    }

    // 204 No Content
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteEmployee(@PathVariable Long id) {
        employeeService.delete(id);
        return ResponseEntity.noContent().build();
    }

    // 404 Not Found
    @GetMapping("/{id}")
    public ResponseEntity<Employee> getEmployee(@PathVariable Long id) {
        Optional<Employee> employee = employeeService.findById(id);
        return employee.map(ResponseEntity::ok)
                       .orElse(ResponseEntity.notFound().build());
    }

    // Custom status with headers
    @PostMapping
    public ResponseEntity<Employee> createEmployee(@RequestBody Employee employee) {
        Employee saved = employeeService.save(employee);
        return ResponseEntity
            .status(HttpStatus.CREATED)
            .header("Custom-Header", "value")
            .body(saved);
    }

    // Conditional response
    @GetMapping("/{id}")
    public ResponseEntity<?> getEmployee(@PathVariable Long id) {
        try {
            Employee employee = employeeService.findById(id);
            return ResponseEntity.ok(employee);
        } catch (ResourceNotFoundException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(Map.of("error", e.getMessage()));
        }
    }
}
```

---

## 8. Content Negotiation {#content-negotiation}

### XML & JSON Support

Add dependency:

```xml
<dependency>
    <groupId>com.fasterxml.jackson.dataformat</groupId>
    <artifactId>jackson-dataformat-xml</artifactId>
</dependency>
```

**Configuration:**

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void configureContentNegotiation(ContentNegotiationConfigurer configurer) {
        configurer
            .favorParameter(true)
            .parameterName("mediaType")
            .defaultContentType(MediaType.APPLICATION_JSON)
            .mediaType("json", MediaType.APPLICATION_JSON)
            .mediaType("xml", MediaType.APPLICATION_XML);
    }
}
```

**Usage:**

```java
@RestController
@RequestMapping("/api/employees")
public class EmployeeController {

    // Returns JSON or XML based on Accept header
    @GetMapping(produces = {MediaType.APPLICATION_JSON_VALUE,
                             MediaType.APPLICATION_XML_VALUE})
    public List<Employee> getAllEmployees() {
        return employeeService.findAll();
    }

    // Consumes JSON or XML
    @PostMapping(consumes = {MediaType.APPLICATION_JSON_VALUE,
                              MediaType.APPLICATION_XML_VALUE})
    public Employee createEmployee(@RequestBody Employee employee) {
        return employeeService.save(employee);
    }
}
```

**Requests:**

```bash
# JSON request
curl -H "Accept: application/json" http://localhost:8080/api/employees

# XML request
curl -H "Accept: application/xml" http://localhost:8080/api/employees

# Using query parameter
curl http://localhost:8080/api/employees?mediaType=xml
```

---

## 9. HATEOAS (Hypermedia) {#hateoas}

### Add Dependency

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-hateoas</artifactId>
</dependency>
```

### Model Assembler

```java
package com.example.demo.assembler;

import com.example.demo.controller.EmployeeController;
import com.example.demo.model.Employee;
import org.springframework.hateoas.EntityModel;
import org.springframework.hateoas.server.RepresentationModelAssembler;
import org.springframework.stereotype.Component;

import static org.springframework.hateoas.server.mvc.WebMvcLinkBuilder.*;

@Component
public class EmployeeModelAssembler
        implements RepresentationModelAssembler<Employee, EntityModel<Employee>> {

    @Override
    public EntityModel<Employee> toModel(Employee employee) {
        return EntityModel.of(employee,
            linkTo(methodOn(EmployeeController.class).getEmployee(employee.getId())).withSelfRel(),
            linkTo(methodOn(EmployeeController.class).getAllEmployees()).withRel("employees"));
    }
}
```

### Controller with HATEOAS

```java
@RestController
@RequestMapping("/api/employees")
@RequiredArgsConstructor
public class EmployeeController {

    private final EmployeeService employeeService;
    private final EmployeeModelAssembler assembler;

    @GetMapping("/{id}")
    public EntityModel<Employee> getEmployee(@PathVariable Long id) {
        Employee employee = employeeService.findById(id);
        return assembler.toModel(employee);
    }

    @GetMapping
    public CollectionModel<EntityModel<Employee>> getAllEmployees() {
        List<EntityModel<Employee>> employees = employeeService.findAll().stream()
            .map(assembler::toModel)
            .collect(Collectors.toList());

        return CollectionModel.of(employees,
            linkTo(methodOn(EmployeeController.class).getAllEmployees()).withSelfRel());
    }

    @PostMapping
    public ResponseEntity<EntityModel<Employee>> createEmployee(@RequestBody Employee employee) {
        Employee saved = employeeService.save(employee);
        EntityModel<Employee> entityModel = assembler.toModel(saved);

        return ResponseEntity
            .created(entityModel.getRequiredLink(IanaLinkRelations.SELF).toUri())
            .body(entityModel);
    }
}
```

**Response Example:**

```json
{
  "id": 1,
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "_links": {
    "self": {
      "href": "http://localhost:8080/api/employees/1"
    },
    "employees": {
      "href": "http://localhost:8080/api/employees"
    }
  }
}
```

---

## 10. API Documentation (Swagger/OpenAPI) {#swagger}

### Add Dependency (SpringDoc)

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.2.0</version>
</dependency>
```

### Configuration

```java
package com.example.demo.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenAPIConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("Employee Management API")
                .version("1.0")
                .description("REST API for managing employees")
                .contact(new Contact()
                    .name("Your Name")
                    .email("your.email@example.com")
                    .url("https://example.com"))
                .license(new License()
                    .name("Apache 2.0")
                    .url("https://www.apache.org/licenses/LICENSE-2.0")));
    }
}
```

### Annotated Controller

```java
@RestController
@RequestMapping("/api/employees")
@Tag(name = "Employee Management", description = "APIs for managing employees")
public class EmployeeController {

    @Operation(
        summary = "Get all employees",
        description = "Retrieves a list of all employees in the system"
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Successfully retrieved list"),
        @ApiResponse(responseCode = "500", description = "Internal server error")
    })
    @GetMapping
    public List<Employee> getAllEmployees() {
        return employeeService.findAll();
    }

    @Operation(summary = "Get employee by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Employee found"),
        @ApiResponse(responseCode = "404", description = "Employee not found")
    })
    @GetMapping("/{id}")
    public ResponseEntity<Employee> getEmployee(
            @Parameter(description = "Employee ID") @PathVariable Long id) {
        Employee employee = employeeService.findById(id);
        return ResponseEntity.ok(employee);
    }

    @Operation(summary = "Create a new employee")
    @ApiResponse(responseCode = "201", description = "Employee created successfully")
    @PostMapping
    public ResponseEntity<Employee> createEmployee(
            @io.swagger.v3.oas.annotations.parameters.RequestBody(
                description = "Employee object to be created",
                required = true
            ) @RequestBody Employee employee) {
        Employee saved = employeeService.save(employee);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }
}
```

**Access Swagger UI:**

- URL: `http://localhost:8080/swagger-ui.html`
- API Docs JSON: `http://localhost:8080/v3/api-docs`

### application.properties

```properties
# Swagger UI customization
springdoc.swagger-ui.path=/swagger-ui.html
springdoc.api-docs.path=/v3/api-docs
springdoc.swagger-ui.operationsSorter=method
```

---

## 11. Security & JWT Authentication {#security}

### Dependencies

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
package com.example.demo.security;

import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

@Component
public class JwtUtil {

    @Value("${jwt.secret}")
    private String secret;

    @Value("${jwt.expiration}")
    private Long expiration;

    private SecretKey getSigningKey() {
        return Keys.hmacShaKeyFor(secret.getBytes());
    }

    public String generateToken(UserDetails userDetails) {
        Map<String, Object> claims = new HashMap<>();
        return createToken(claims, userDetails.getUsername());
    }

    private String createToken(Map<String, Object> claims, String subject) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + expiration);

        return Jwts.builder()
            .setClaims(claims)
            .setSubject(subject)
            .setIssuedAt(now)
            .setExpiration(expiryDate)
            .signWith(getSigningKey(), SignatureAlgorithm.HS256)
            .compact();
    }

    public String extractUsername(String token) {
        return extractClaim(token, Claims::getSubject);
    }

    public Date extractExpiration(String token) {
        return extractClaim(token, Claims::getExpiration);
    }

    public <T> T extractClaim(String token, Function<Claims, T> claimsResolver) {
        final Claims claims = extractAllClaims(token);
        return claimsResolver.apply(claims);
    }

    private Claims extractAllClaims(String token) {
        return Jwts.parserBuilder()
            .setSigningKey(getSigningKey())
            .build()
            .parseClaimsJws(token)
            .getBody();
    }

    private Boolean isTokenExpired(String token) {
        return extractExpiration(token).before(new Date());
    }

    public Boolean validateToken(String token, UserDetails userDetails) {
        final String username = extractUsername(token);
        return (username.equals(userDetails.getUsername()) && !isTokenExpired(token));
    }
}
```

### JWT Filter

```java
package com.example.demo.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

@Component
@RequiredArgsConstructor
public class JwtRequestFilter extends OncePerRequestFilter {

    private final UserDetailsService userDetailsService;
    private final JwtUtil jwtUtil;

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
                                    FilterChain chain) throws ServletException, IOException {

        final String authorizationHeader = request.getHeader("Authorization");

        String username = null;
        String jwt = null;

        if (authorizationHeader != null && authorizationHeader.startsWith("Bearer ")) {
            jwt = authorizationHeader.substring(7);
            username = jwtUtil.extractUsername(jwt);
        }

        if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            UserDetails userDetails = this.userDetailsService.loadUserByUsername(username);

            if (jwtUtil.validateToken(jwt, userDetails)) {
                UsernamePasswordAuthenticationToken authToken =
                    new UsernamePasswordAuthenticationToken(
                        userDetails, null, userDetails.getAuthorities());
                authToken.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }
        chain.doFilter(request, response);
    }
}
```

### Security Configuration

```java
package com.example.demo.config;

import com.example.demo.security.JwtRequestFilter;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtRequestFilter jwtRequestFilter;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**", "/swagger-ui/**", "/v3/api-docs/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .sessionManagement(session ->
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .addFilterBefore(jwtRequestFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(
            AuthenticationConfiguration authConfig) throws Exception {
        return authConfig.getAuthenticationManager();
    }
}
```

### Auth Controller

```java
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthenticationManager authenticationManager;
    private final UserDetailsService userDetailsService;
    private final JwtUtil jwtUtil;

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody AuthRequest authRequest) {
        try {
            authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                    authRequest.getUsername(),
                    authRequest.getPassword()
                )
            );
        } catch (BadCredentialsException e) {
            throw new BadRequestException("Invalid credentials");
        }

        final UserDetails userDetails = userDetailsService
            .loadUserByUsername(authRequest.getUsername());
        final String jwt = jwtUtil.generateToken(userDetails);

        return ResponseEntity.ok(new AuthResponse(jwt));
    }
}
```

---

## 12. Testing REST APIs {#testing}

### Dependencies

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```

### Unit Test - Controller

```java
package com.example.demo.controller;

import com.example.demo.model.Employee;
import com.example.demo.service.EmployeeService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Arrays;
import java.util.List;

import static org.hamcrest.Matchers.hasSize;
import static org.hamcrest.Matchers.is;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(EmployeeController.class)
class EmployeeControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private EmployeeService employeeService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void shouldGetAllEmployees() throws Exception {
        Employee emp1 = new Employee(1L, "John", "Doe", "john@example.com", "IT", 50000.0);
        Employee emp2 = new Employee(2L, "Jane", "Smith", "jane@example.com", "HR", 60000.0);
        List<Employee> employees = Arrays.asList(emp1, emp2);

        when(employeeService.findAll()).thenReturn(employees);

        mockMvc.perform(get("/api/employees"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$", hasSize(2)))
            .andExpect(jsonPath("$[0].firstName", is("John")))
            .andExpect(jsonPath("$[1].firstName", is("Jane")));

        verify(employeeService, times(1)).findAll();
    }

    @Test
    void shouldGetEmployeeById() throws Exception {
        Employee employee = new Employee(1L, "John", "Doe", "john@example.com", "IT", 50000.0);

        when(employeeService.findById(1L)).thenReturn(employee);

        mockMvc.perform(get("/api/employees/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.firstName", is("John")))
            .andExpect(jsonPath("$.email", is("john@example.com")));
    }

    @Test
    void shouldCreateEmployee() throws Exception {
        Employee employee = new Employee(null, "John", "Doe", "john@example.com", "IT", 50000.0);
        Employee savedEmployee = new Employee(1L, "John", "Doe", "john@example.com", "IT", 50000.0);

        when(employeeService.save(any(Employee.class))).thenReturn(savedEmployee);

        mockMvc.perform(post("/api/employees")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(employee)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id", is(1)))
            .andExpect(jsonPath("$.firstName", is("John")));
    }

    @Test
    void shouldUpdateEmployee() throws Exception {
        Employee updatedEmployee = new Employee(1L, "John", "Updated", "john@example.com", "IT", 55000.0);

        when(employeeService.update(eq(1L), any(Employee.class))).thenReturn(updatedEmployee);

        mockMvc.perform(put("/api/employees/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updatedEmployee)))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.lastName", is("Updated")))
            .andExpect(jsonPath("$.salary", is(55000.0)));
    }

    @Test
    void shouldDeleteEmployee() throws Exception {
        doNothing().when(employeeService).delete(1L);

        mockMvc.perform(delete("/api/employees/1"))
            .andExpect(status().isNoContent());

        verify(employeeService, times(1)).delete(1L);
    }

    @Test
    void shouldReturn404WhenEmployeeNotFound() throws Exception {
        when(employeeService.findById(999L))
            .thenThrow(new ResourceNotFoundException("Employee not found"));

        mockMvc.perform(get("/api/employees/999"))
            .andExpect(status().isNotFound());
    }
}
```

### Integration Test

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureTestDatabase
@TestPropertySource(locations = "classpath:application-test.properties")
class EmployeeIntegrationTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Autowired
    private EmployeeRepository employeeRepository;

    @BeforeEach
    void setUp() {
        employeeRepository.deleteAll();
    }

    @Test
    void shouldCreateAndRetrieveEmployee() {
        Employee employee = new Employee(null, "John", "Doe", "john@example.com", "IT", 50000.0);

        ResponseEntity<Employee> createResponse = restTemplate
            .postForEntity("/api/employees", employee, Employee.class);

        assertThat(createResponse.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(createResponse.getBody()).isNotNull();
        assertThat(createResponse.getBody().getId()).isNotNull();

        Long id = createResponse.getBody().getId();

        ResponseEntity<Employee> getResponse = restTemplate
            .getForEntity("/api/employees/" + id, Employee.class);

        assertThat(getResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(getResponse.getBody().getFirstName()).isEqualTo("John");
    }
}
```

---

## 13. Asynchronous REST APIs {#async}

### Enable Async Support

```java
@Configuration
@EnableAsync
public class AsyncConfig {

    @Bean(name = "asyncExecutor")
    public Executor asyncExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-");
        executor.initialize();
        return executor;
    }
}
```

### Async Service

```java
@Service
public class AsyncService {

    @Async("asyncExecutor")
    public CompletableFuture<String> processTask1() throws InterruptedException {
        Thread.sleep(2000);
        return CompletableFuture.completedFuture("Task 1 completed");
    }

    @Async("asyncExecutor")
    public CompletableFuture<String> processTask2() throws InterruptedException {
        Thread.sleep(3000);
        return CompletableFuture.completedFuture("Task 2 completed");
    }

    @Async("asyncExecutor")
    public CompletableFuture<String> processTask3() throws InterruptedException {
        Thread.sleep(1000);
        return CompletableFuture.completedFuture("Task 3 completed");
    }
}
```

### Async Controller

```java
@RestController
@RequestMapping("/api/async")
@RequiredArgsConstructor
public class AsyncController {

    private final AsyncService asyncService;

    @GetMapping("/process")
    public CompletableFuture<Map<String, String>> processAsync() {
        CompletableFuture<String> task1 = asyncService.processTask1();
        CompletableFuture<String> task2 = asyncService.processTask2();
        CompletableFuture<String> task3 = asyncService.processTask3();

        return CompletableFuture.allOf(task1, task2, task3)
            .thenApply(v -> {
                Map<String, String> results = new HashMap<>();
                try {
                    results.put("task1", task1.get());
                    results.put("task2", task2.get());
                    results.put("task3", task3.get());
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
                return results;
            });
    }

    @GetMapping("/deferred")
    public DeferredResult<String> getDeferredResult() {
        DeferredResult<String> result = new DeferredResult<>(5000L);

        CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(3000);
                return "Deferred result ready";
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }).whenComplete((res, ex) -> {
            if (ex != null) {
                result.setErrorResult(ex);
            } else {
                result.setResult(res);
            }
        });

        return result;
    }
}
```

---

## 14. API Versioning {#versioning}

### URI Path Versioning

```java
@RestController
@RequestMapping("/api/v1/employees")
public class EmployeeV1Controller {
    @GetMapping("/{id}")
    public EmployeeV1 getEmployee(@PathVariable Long id) {
        return employeeService.findByIdV1(id);
    }
}

@RestController
@RequestMapping("/api/v2/employees")
public class EmployeeV2Controller {
    @GetMapping("/{id}")
    public EmployeeV2 getEmployee(@PathVariable Long id) {
        return employeeService.findByIdV2(id);
    }
}
```

### Request Parameter Versioning

```java
@RestController
@RequestMapping("/api/employees")
public class EmployeeController {

    @GetMapping(params = "version=1")
    public EmployeeV1 getEmployeeV1(@PathVariable Long id) {
        return employeeService.findByIdV1(id);
    }

    @GetMapping(params = "version=2")
    public EmployeeV2 getEmployeeV2(@PathVariable Long id) {
        return employeeService.findByIdV2(id);
    }
}
```

### Custom Header Versioning

```java
@RestController
@RequestMapping("/api/employees")
public class EmployeeController {

    @GetMapping(headers = "X-API-VERSION=1")
    public EmployeeV1 getEmployeeV1(@PathVariable Long id) {
        return employeeService.findByIdV1(id);
    }

    @GetMapping(headers = "X-API-VERSION=2")
    public EmployeeV2 getEmployeeV2(@PathVariable Long id) {
        return employeeService.findByIdV2(id);
    }
}
```

### Content Negotiation Versioning

```java
@RestController
@RequestMapping("/api/employees")
public class EmployeeController {

    @GetMapping(produces = "application/vnd.company.app-v1+json")
    public EmployeeV1 getEmployeeV1(@PathVariable Long id) {
        return employeeService.findByIdV1(id);
    }

    @GetMapping(produces = "application/vnd.company.app-v2+json")
    public EmployeeV2 getEmployeeV2(@PathVariable Long id) {
        return employeeService.findByIdV2(id);
    }
}
```

---

## 15. REST Clients {#rest-clients}

### RestTemplate (Legacy)

```java
@Configuration
public class RestTemplateConfig {

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}

@Service
@RequiredArgsConstructor
public class EmployeeClient {

    private final RestTemplate restTemplate;
    private static final String BASE_URL = "http://localhost:8080/api/employees";

    public List<Employee> getAllEmployees() {
        ResponseEntity<Employee[]> response = restTemplate
            .getForEntity(BASE_URL, Employee[].class);
        return Arrays.asList(response.getBody());
    }

    public Employee getEmployeeById(Long id) {
        return restTemplate.getForObject(BASE_URL + "/" + id, Employee.class);
    }

    public Employee createEmployee(Employee employee) {
        return restTemplate.postForObject(BASE_URL, employee, Employee.class);
    }

    public void updateEmployee(Long id, Employee employee) {
        restTemplate.put(BASE_URL + "/" + id, employee);
    }

    public void deleteEmployee(Long id) {
        restTemplate.delete(BASE_URL + "/" + id);
    }
}
```

### RestClient (Spring Boot 3.2+)

```java
@Service
public class EmployeeClient {

    private final RestClient restClient;

    public EmployeeClient(RestClient.Builder builder) {
        this.restClient = builder.baseUrl("http://localhost:8080/api").build();
    }

    public List<Employee> getAllEmployees() {
        return restClient.get()
            .uri("/employees")
            .retrieve()
            .body(new ParameterizedTypeReference<List<Employee>>() {});
    }

    public Employee getEmployeeById(Long id) {
        return restClient.get()
            .uri("/employees/{id}", id)
            .retrieve()
            .body(Employee.class);
    }

    public Employee createEmployee(Employee employee) {
        return restClient.post()
            .uri("/employees")
            .contentType(MediaType.APPLICATION_JSON)
            .body(employee)
            .retrieve()
            .body(Employee.class);
    }
}
```

### WebClient (Reactive)

```java
@Service
public class EmployeeClient {

    private final WebClient webClient;

    public EmployeeClient(WebClient.Builder builder) {
        this.webClient = builder.baseUrl("http://localhost:8080/api").build();
    }

    public Mono<Employee> getEmployeeById(Long id) {
        return webClient.get()
            .uri("/employees/{id}", id)
            .retrieve()
            .bodyToMono(Employee.class);
    }

    public Flux<Employee> getAllEmployees() {
        return webClient.get()
            .uri("/employees")
            .retrieve()
            .bodyToFlux(Employee.class);
    }

    public Mono<Employee> createEmployee(Employee employee) {
        return webClient.post()
            .uri("/employees")
            .contentType(MediaType.APPLICATION_JSON)
            .body(Mono.just(employee), Employee.class)
            .retrieve()
            .bodyToMono(Employee.class);
    }
}
```

---

## 16. File Upload & Download {#file-operations}

### Configuration

```properties
# application.properties
spring.servlet.multipart.enabled=true
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB
file.upload-dir=./uploads
```

### File Storage Service

```java
@Service
public class FileStorageService {

    private final Path fileStorageLocation;

    @Autowired
    public FileStorageService(@Value("${file.upload-dir}") String uploadDir) {
        this.fileStorageLocation = Paths.get(uploadDir).toAbsolutePath().normalize();
        try {
            Files.createDirectories(this.fileStorageLocation);
        } catch (Exception ex) {
            throw new RuntimeException("Could not create upload directory", ex);
        }
    }

    public String storeFile(MultipartFile file) {
        String fileName = StringUtils.cleanPath(file.getOriginalFilename());

        try {
            if (fileName.contains("..")) {
                throw new RuntimeException("Invalid file path");
            }

            Path targetLocation = this.fileStorageLocation.resolve(fileName);
            Files.copy(file.getInputStream(), targetLocation, StandardCopyOption.REPLACE_EXISTING);

            return fileName;
        } catch (IOException ex) {
            throw new RuntimeException("Could not store file " + fileName, ex);
        }
    }

    public Resource loadFileAsResource(String fileName) {
        try {
            Path filePath = this.fileStorageLocation.resolve(fileName).normalize();
            Resource resource = new UrlResource(filePath.toUri());
            if (resource.exists()) {
                return resource;
            } else {
                throw new RuntimeException("File not found " + fileName);
            }
        } catch (MalformedURLException ex) {
            throw new RuntimeException("File not found " + fileName, ex);
        }
    }
}
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

---

## 17. Pagination & Sorting {#pagination}

### Repository

```java
public interface EmployeeRepository extends JpaRepository<Employee, Long> {
    Page<Employee> findByDepartment(String department, Pageable pageable);
}
```

### Service

```java
@Service
@RequiredArgsConstructor
public class EmployeeService {

    private final EmployeeRepository employeeRepository;

    public Page<Employee> findAll(int page, int size, String sortBy, String direction) {
        Sort.Direction sortDirection = direction.equalsIgnoreCase("desc")
            ? Sort.Direction.DESC : Sort.Direction.ASC;
        Pageable pageable = PageRequest.of(page, size, Sort.by(sortDirection, sortBy));
        return employeeRepository.findAll(pageable);
    }
}
```

### Controller

```java
@RestController
@RequestMapping("/api/employees")
@RequiredArgsConstructor
public class EmployeeController {

    private final EmployeeService employeeService;

    @GetMapping
    public ResponseEntity<PagedResponse<Employee>> getAllEmployees(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction) {

        Page<Employee> employeePage = employeeService.findAll(page, size, sortBy, direction);

        PagedResponse<Employee> response = new PagedResponse<>(
            employeePage.getContent(),
            employeePage.getNumber(),
            employeePage.getSize(),
            employeePage.getTotalElements(),
            employeePage.getTotalPages(),
            employeePage.isLast()
        );

        return ResponseEntity.ok(response);
    }
}
```

### PagedResponse DTO

```java
@Data
@AllArgsConstructor
public class PagedResponse<T> {
    private List<T> content;
    private int page;
    private int size;
    private long totalElements;
    private int totalPages;
    private boolean last;
}
```

**Example Request:**

```
GET /api/employees?page=0&size=10&sortBy=salary&direction=desc
```

---

## 18. Caching {#caching}

### Enable Caching

```java
@Configuration
@EnableCaching
public class CacheConfig {

    @Bean
    public CacheManager cacheManager() {
        return new ConcurrentMapCacheManager("employees");
    }
}
```

### Service with Caching

```java
@Service
@RequiredArgsConstructor
public class EmployeeService {

    private final EmployeeRepository employeeRepository;

    @Cacheable(value = "employees", key = "#id")
    public Employee findById(Long id) {
        System.out.println("Fetching from database...");
        return employeeRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Employee not found"));
    }

    @Cacheable(value = "employees")
    public List<Employee> findAll() {
        System.out.println("Fetching all from database...");
        return employeeRepository.findAll();
    }

    @CachePut(value = "employees", key = "#result.id")
    public Employee save(Employee employee) {
        return employeeRepository.save(employee);
    }

    @CacheEvict(value = "employees", key = "#id")
    public void delete(Long id) {
        employeeRepository.deleteById(id);
    }

    @CacheEvict(value = "employees", allEntries = true)
    public void clearCache() {
        System.out.println("Cache cleared");
    }
}
```

### Redis Caching

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

```java
@Configuration
@EnableCaching
public class RedisCacheConfig {

    @Bean
    public RedisCacheConfiguration cacheConfiguration() {
        return RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(10))
            .disableCachingNullValues()
            .serializeValuesWith(
                SerializationPair.fromSerializer(new GenericJackson2JsonRedisSerializer())
            );
    }
}
```

---

## 19. CORS Configuration {#cors}

### Method-Level CORS

```java
@RestController
@RequestMapping("/api/employees")
@CrossOrigin(origins = "http://localhost:3000")
public class EmployeeController {

    @GetMapping
    public List<Employee> getAllEmployees() {
        return employeeService.findAll();
    }
}
```

### Global CORS Configuration

```java
@Configuration
public class CorsConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins("http://localhost:3000", "http://localhost:4200")
            .allowedMethods("GET", "POST", "PUT", "DELETE", "PATCH")
            .allowedHeaders("*")
            .allowCredentials(true)
            .maxAge(3600);
    }
}
```

### CORS with Security

```java
@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            .csrf(csrf -> csrf.disable())
            // ... other configurations
        return http.build();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOrigins(Arrays.asList("http://localhost:3000"));
        configuration.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE"));
        configuration.setAllowedHeaders(Arrays.asList("*"));
        configuration.setAllowCredentials(true);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/api/**", configuration);
        return source;
    }
}
```

---

## 20. Monitoring with Actuator {#actuator}

### Add Dependency

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

### Configuration

```properties
# application.properties
management.endpoints.web.exposure.include=*
management.endpoint.health.show-details=always
management.metrics.export.prometheus.enabled=true
```

### Custom Health Indicator

```java
@Component
public class CustomHealthIndicator implements HealthIndicator {

    @Override
    public Health health() {
        try {
            // Check custom health logic
            boolean serviceUp = checkExternalService();
            if (serviceUp) {
                return Health.up()
                    .withDetail("service", "External service is running")
                    .build();
            } else {
                return Health.down()
                    .withDetail("service", "External service is down")
                    .build();
            }
        } catch (Exception e) {
            return Health.down()
                .withDetail("error", e.getMessage())
                .build();
        }
    }

    private boolean checkExternalService() {
        // Implementation
        return true;
    }
}
```

### Custom Metrics

```java
@Service
@RequiredArgsConstructor
public class EmployeeService {

    private final MeterRegistry meterRegistry;
    private final EmployeeRepository employeeRepository;

    public Employee save(Employee employee) {
        meterRegistry.counter("employees.created").increment();
        return employeeRepository.save(employee);
    }

    public void delete(Long id) {
        meterRegistry.counter("employees.deleted").increment();
        employeeRepository.deleteById(id);
    }
}
```

**Access Actuator Endpoints:**

- Health: `http://localhost:8080/actuator/health`
- Metrics: `http://localhost:8080/actuator/metrics`
- Info: `http://localhost:8080/actuator/info`

---

## 21. Best Practices {#best-practices}

### 1. Use DTOs for API Contracts

```java
// Don't expose entities directly
@Data
public class EmployeeDTO {
    private Long id;
    private String fullName;
    private String email;
    private String department;
}

// Use MapStruct for mapping
@Mapper(componentModel = "spring")
public interface EmployeeMapper {
    EmployeeDTO toDto(Employee employee);
    Employee toEntity(EmployeeDTO dto);
}
```

### 2. Proper HTTP Status Codes

- 200 OK for successful GET, PUT, PATCH
- 201 Created for successful POST
- 204 No Content for successful DELETE
- 400 Bad Request for validation errors
- 404 Not Found for missing resources
- 500 Internal Server Error for server errors

### 3. API Response Wrapper

```java
@Data
@AllArgsConstructor
public class ApiResponse<T> {
    private boolean success;
    private String message;
    private T data;
    private LocalDateTime timestamp;
}
```

### 4. Logging

```java
@RestController
@Slf4j
public class EmployeeController {

    @GetMapping("/{id}")
    public ResponseEntity<Employee> getEmployee(@PathVariable Long id) {
        log.info("Fetching employee with id: {}", id);
        Employee employee = employeeService.findById(id);
        log.debug("Employee found: {}", employee);
        return ResponseEntity.ok(employee);
    }
}
```

### 5. Rate Limiting

```java
// Using Bucket4j
@Service
public class RateLimitService {
    private final Map<String, Bucket> cache = new ConcurrentHashMap<>();

    public Bucket resolveBucket(String key) {
        return cache.computeIfAbsent(key, k -> createNewBucket());
    }

    private Bucket createNewBucket() {
        Bandwidth limit = Bandwidth.classic(10, Refill.intervally(10, Duration.ofMinutes(1)));
        return Bucket4j.builder()
            .addLimit(limit)
            .build();
    }
}
```

### 6. API Documentation Standards

- Use meaningful endpoint names
- Follow REST conventions
- Version your APIs
- Document all endpoints with Swagger
- Provide request/response examples

---

## 22. Reactive REST with WebFlux {#webflux}

### Dependencies

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-mongodb-reactive</artifactId>
</dependency>
```

### Reactive Repository

```java
public interface EmployeeRepository extends ReactiveMongoRepository<Employee, String> {
    Flux<Employee> findByDepartment(String department);
}
```

### Reactive Controller

```java
@RestController
@RequestMapping("/api/employees")
@RequiredArgsConstructor
public class EmployeeController {

    private final EmployeeRepository employeeRepository;

    @GetMapping
    public Flux<Employee> getAllEmployees() {
        return employeeRepository.findAll();
    }

    @GetMapping("/{id}")
    public Mono<ResponseEntity<Employee>> getEmployee(@PathVariable String id) {
        return employeeRepository.findById(id)
            .map(ResponseEntity::ok)
            .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @PostMapping
    public Mono<Employee> createEmployee(@RequestBody Employee employee) {
        return employeeRepository.save(employee);
    }

    @PutMapping("/{id}")
    public Mono<ResponseEntity<Employee>> updateEmployee(
            @PathVariable String id,
            @RequestBody Employee employee) {
        return employeeRepository.findById(id)
            .flatMap(existingEmployee -> {
                existingEmployee.setFirstName(employee.getFirstName());
                existingEmployee.setLastName(employee.getLastName());
                return employeeRepository.save(existingEmployee);
            })
            .map(ResponseEntity::ok)
            .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public Mono<ResponseEntity<Void>> deleteEmployee(@PathVariable String id) {
        return employeeRepository.deleteById(id)
            .then(Mono.just(ResponseEntity.noContent().<Void>build()))
            .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    // Streaming example
    @GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<Employee> streamEmployees() {
        return employeeRepository.findAll()
            .delayElements(Duration.ofSeconds(1));
    }
}
```

---

## Interview Questions

### Basics

1. **What is REST?** - Architectural style for distributed hypermedia systems
2. **Difference between @Controller and @RestController?** - @RestController = @Controller + @ResponseBody
3. **What are HTTP methods?** - GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
4. **Difference between PUT and PATCH?** - PUT replaces entire resource, PATCH updates partially
5. **What is @PathVariable?** - Extracts value from URI path
6. **What is @RequestParam?** - Extracts query parameters from URL

### Intermediate

7. **How to handle exceptions in REST?** - Use @RestControllerAdvice and @ExceptionHandler
8. **What is ResponseEntity?** - Represents entire HTTP response (status, headers, body)
9. **How to validate request body?** - Use @Valid with Jakarta validation annotations
10. **What is HATEOAS?** - Hypermedia as the Engine of Application State
11. **How to secure REST API?** - Use Spring Security with JWT tokens
12. **What is content negotiation?** - Returning different representations (JSON/XML) based on client request

### Advanced

13. **Explain API versioning strategies** - URI path, request param, header, content negotiation
14. **How to implement pagination?** - Use Pageable with PageRequest
15. **What is the difference between RestTemplate, WebClient, and RestClient?** - RestTemplate (blocking), WebClient (reactive), RestClient (blocking, modern)
16. **How to handle file uploads?** - Use MultipartFile with @RequestParam
17. **What is reactive programming?** - Non-blocking, event-driven programming with Mono/Flux
18. **How to monitor REST APIs?** - Use Spring Boot Actuator with metrics and health checks

---

## Summary

This comprehensive guide covers all aspects of Spring Boot REST API development from basics to expert level. Practice these concepts with hands-on coding to excel in interviews and real-world projects.

**Key Takeaways:**

- Master core annotations (@RestController, @RequestMapping, etc.)
- Implement proper exception handling and validation
- Use ResponseEntity for fine-grained HTTP control
- Secure APIs with JWT authentication
- Document APIs with Swagger/OpenAPI
- Test thoroughly with MockMvc and integration tests
- Follow REST best practices and conventions
- Understand advanced topics like HATEOAS, caching, and reactive programming

**Next Steps:**

- Build a complete project implementing all these concepts
- Practice common interview scenarios
- Explore microservices architecture
- Learn Kubernetes deployment for REST APIs
