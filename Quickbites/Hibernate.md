# Hibernate with Spring Boot: Complete Interview Guide

## From Basics to Expert Level

---

## Table of Contents

1. [Introduction to Hibernate](#1-introduction-to-hibernate)
2. [Hibernate Architecture](#2-hibernate-architecture)
3. [Setting Up Hibernate with Spring Boot](#3-setting-up-hibernate-with-spring-boot)
4. [Entity Mapping and Annotations](#4-entity-mapping-and-annotations)
5. [Hibernate Entity Lifecycle](#5-hibernate-entity-lifecycle)
6. [Relationships and Associations](#6-relationships-and-associations)
7. [Querying in Hibernate](#7-querying-in-hibernate)
8. [Spring Data JPA Repository](#8-spring-data-jpa-repository)
9. [Hibernate Session and SessionFactory](#9-hibernate-session-and-sessionfactory)
10. [Transaction Management](#10-transaction-management)
11. [Caching in Hibernate](#11-caching-in-hibernate)
12. [Fetching Strategies](#12-fetching-strategies)
13. [N+1 Problem and Solutions](#13-n1-problem-and-solutions)
14. [Batch Processing](#14-batch-processing)
15. [Pagination](#15-pagination)
16. [Inheritance Strategies](#16-inheritance-strategies)
17. [Composite Primary Keys](#17-composite-primary-keys)
18. [Locking Mechanisms](#18-locking-mechanisms)
19. [Auditing](#19-auditing)
20. [Performance Optimization](#20-performance-optimization)
21. [Best Practices](#21-best-practices)

---

## 1. Introduction to Hibernate

### What is Hibernate?

Hibernate is an **Object-Relational Mapping (ORM)** framework for Java that simplifies database operations by mapping Java classes to database tables. It eliminates the need for manual JDBC code, providing cleaner and more maintainable applications.

### Key Features

- **ORM Support**: Maps Java objects to database tables, reducing boilerplate JDBC code
- **Database Independence**: Works with multiple databases using SQL dialects
- **HQL (Hibernate Query Language)**: Provides database-independent, object-oriented querying
- **Caching Mechanism**: Improves performance with first-level and second-level caching
- **Lazy Loading**: Loads data on-demand to optimize performance
- **Transaction Management**: Built-in transaction support

### Hibernate vs JDBC

| Feature                | JDBC   | Hibernate                    |
| ---------------------- | ------ | ---------------------------- |
| Boilerplate Code       | High   | Low                          |
| Database Independence  | No     | Yes                          |
| Caching                | No     | Yes (First and Second level) |
| Object Mapping         | Manual | Automatic                    |
| Transaction Management | Manual | Automatic                    |
| Query Language         | SQL    | HQL/JPQL                     |

### Hibernate vs JPA

- **JPA** (Java Persistence API) is a specification for ORM in Java
- **Hibernate** is an implementation of the JPA specification
- Hibernate also provides additional features beyond JPA

---

## 2. Hibernate Architecture

### Core Components

```
┌─────────────────────────────────────────────────────┐
│              Application Layer                       │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│           Hibernate Framework                        │
│  ┌──────────────┐  ┌─────────────┐  ┌───────────┐ │
│  │Configuration │  │ SessionFactory│  │  Session  │ │
│  └──────────────┘  └─────────────┘  └───────────┘ │
│  ┌──────────────┐  ┌─────────────┐  ┌───────────┐ │
│  │ Transaction  │  │    Query    │  │ Criteria  │ │
│  └──────────────┘  └─────────────┘  └───────────┘ │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│              Database Layer                          │
└─────────────────────────────────────────────────────┘
```

### Key Components:

1. **Configuration**: Holds database and mapping configuration
2. **SessionFactory**: Thread-safe factory for Session objects (one per application)
3. **Session**: Single-threaded, short-lived object for database operations
4. **Transaction**: Unit of work with the database
5. **Query/Criteria**: Interfaces for database querying

---

## 3. Setting Up Hibernate with Spring Boot

### Maven Dependencies (pom.xml)

```xml
<dependencies>
    <!-- Spring Boot Starter Data JPA (includes Hibernate) -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>

    <!-- Database Driver - MySQL example -->
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>8.0.33</version>
        <scope>runtime</scope>
    </dependency>

    <!-- H2 Database for testing -->
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <scope>runtime</scope>
    </dependency>

    <!-- Lombok (optional) -->
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <optional>true</optional>
    </dependency>
</dependencies>
```

### application.properties Configuration

```properties
# Database Configuration - MySQL
spring.datasource.url=jdbc:mysql://localhost:3306/mydb
spring.datasource.username=root
spring.datasource.password=password
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# JPA/Hibernate Properties
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect

# Connection Pool Configuration (HikariCP)
spring.datasource.hikari.maximum-pool-size=10
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.connection-timeout=30000

# Batch Processing
spring.jpa.properties.hibernate.jdbc.batch_size=50
spring.jpa.properties.hibernate.order_inserts=true
spring.jpa.properties.hibernate.order_updates=true

# Second Level Cache (optional)
spring.jpa.properties.hibernate.cache.use_second_level_cache=true
spring.jpa.properties.hibernate.cache.region.factory_class=org.hibernate.cache.ehcache.EhCacheRegionFactory

# Logging
logging.level.org.hibernate.SQL=DEBUG
logging.level.org.hibernate.type.descriptor.sql.BasicBinder=TRACE
```

### Main Application Class

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.transaction.annotation.EnableTransactionManagement;

@SpringBootApplication
@EnableTransactionManagement
@EnableJpaAuditing  // For auditing features
public class HibernateSpringBootApplication {
    public static void main(String[] args) {
        SpringApplication.run(HibernateSpringBootApplication.class, args);
    }
}
```

---

## 4. Entity Mapping and Annotations

### Basic Entity Example

```java
import javax.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "employees")
@Data  // Lombok: generates getters, setters, toString, equals, hashCode
@NoArgsConstructor
@AllArgsConstructor
public class Employee {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "employee_id")
    private Long id;

    @Column(name = "first_name", nullable = false, length = 50)
    private String firstName;

    @Column(name = "last_name", nullable = false, length = 50)
    private String lastName;

    @Column(unique = true, nullable = false)
    private String email;

    @Column(nullable = false)
    private Double salary;

    @Column(name = "hire_date")
    private LocalDateTime hireDate;

    @Column(name = "is_active")
    private Boolean isActive = true;

    @Transient  // Not persisted to database
    private String fullName;

    @PrePersist
    protected void onCreate() {
        hireDate = LocalDateTime.now();
    }
}
```

### Key Annotations Explained

#### @Entity

Marks the class as a JPA entity that should be mapped to a database table.

#### @Table

Specifies the table name and additional properties:

- `name`: Table name in database
- `schema`: Database schema
- `catalog`: Database catalog
- `uniqueConstraints`: Unique constraints

```java
@Table(
    name = "employees",
    schema = "hr_schema",
    uniqueConstraints = {
        @UniqueConstraint(columnNames = {"email"}),
        @UniqueConstraint(columnNames = {"ssn"})
    }
)
```

#### @Id and Primary Key Generation Strategies

```java
// 1. AUTO - Let JPA choose the strategy
@Id
@GeneratedValue(strategy = GenerationType.AUTO)
private Long id;

// 2. IDENTITY - Database auto-increment
@Id
@GeneratedValue(strategy = GenerationType.IDENTITY)
private Long id;

// 3. SEQUENCE - Database sequence
@Id
@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "emp_seq")
@SequenceGenerator(name = "emp_seq", sequenceName = "employee_seq", allocationSize = 1)
private Long id;

// 4. TABLE - Separate table for ID generation
@Id
@GeneratedValue(strategy = GenerationType.TABLE, generator = "emp_gen")
@TableGenerator(name = "emp_gen", table = "id_gen", pkColumnName = "gen_name",
                valueColumnName = "gen_value", allocationSize = 1)
private Long id;

// 5. UUID - Generate UUID
@Id
@GeneratedValue(strategy = GenerationType.UUID)
private String id;
```

#### @Column

Specifies the column mapping:

```java
@Column(
    name = "employee_name",      // Column name
    nullable = false,            // NOT NULL constraint
    unique = true,               // UNIQUE constraint
    length = 100,                // VARCHAR(100)
    precision = 10,              // For decimal types
    scale = 2,                   // For decimal types
    insertable = true,           // Include in INSERT
    updatable = true,            // Include in UPDATE
    columnDefinition = "VARCHAR(255) DEFAULT 'Unknown'"
)
private String name;
```

### Validation Annotations

```java
import javax.validation.constraints.*;

@Entity
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotNull(message = "Username cannot be null")
    @NotBlank(message = "Username cannot be blank")
    @Size(min = 3, max = 50, message = "Username must be between 3 and 50 characters")
    private String username;

    @Email(message = "Email should be valid")
    @NotEmpty(message = "Email cannot be empty")
    private String email;

    @Min(value = 18, message = "Age should not be less than 18")
    @Max(value = 150, message = "Age should not be greater than 150")
    private Integer age;

    @Pattern(regexp = "^[0-9]{10}$", message = "Phone number must be 10 digits")
    private String phoneNumber;

    @Positive
    private Double salary;

    @Past
    private LocalDate dateOfBirth;

    @Future
    private LocalDate contractEndDate;
}
```

---

## 5. Hibernate Entity Lifecycle

Hibernate entities can exist in four different states:

```
┌────────────┐    save()      ┌────────────┐    close()     ┌────────────┐
│ Transient  │────────────────>│ Persistent │────────────────>│  Detached  │
└────────────┘                 └────────────┘                 └────────────┘
      │                              │                               │
      │                              │ delete()                      │
      │                              │                               │
      │                              ▼                               │
      │                        ┌────────────┐                        │
      │                        │  Removed   │                        │
      │                        └────────────┘                        │
      │                                                               │
      └───────────────────────── update()/merge() ────────────────────┘
```

### 1. Transient State

- Entity is created using `new` operator
- Not associated with any Hibernate session
- No database representation

```java
Employee employee = new Employee();
employee.setFirstName("John");
employee.setLastName("Doe");
// Entity is in Transient state
```

### 2. Persistent State

- Entity is associated with a Hibernate session
- Any changes are tracked and synchronized with database
- Has database representation

```java
Session session = sessionFactory.openSession();
Transaction tx = session.beginTransaction();

Employee employee = new Employee();
employee.setFirstName("John");
session.save(employee);  // Now in Persistent state

employee.setFirstName("Jane");  // This change will be automatically persisted

tx.commit();
session.close();
```

### 3. Detached State

- Entity was persistent but session is closed
- Still has database identity but not tracked
- Changes won't be automatically persisted

```java
Session session1 = sessionFactory.openSession();
Transaction tx1 = session1.beginTransaction();
Employee employee = session1.get(Employee.class, 1L);
tx1.commit();
session1.close();  // Entity becomes Detached

employee.setFirstName("Updated");  // Change not tracked

// To persist changes, reattach to new session
Session session2 = sessionFactory.openSession();
Transaction tx2 = session2.beginTransaction();
session2.update(employee);  // Back to Persistent state
tx2.commit();
session2.close();
```

### 4. Removed State

- Entity is scheduled for deletion
- Will be removed from database on transaction commit

```java
Session session = sessionFactory.openSession();
Transaction tx = session.beginTransaction();

Employee employee = session.get(Employee.class, 1L);
session.delete(employee);  // Entity in Removed state

tx.commit();  // Now deleted from database
session.close();
```

### State Transition Methods

```java
// save() - Persist transient entity
session.save(entity);

// persist() - Similar to save() but returns void
session.persist(entity);

// update() - Reattach detached entity
session.update(entity);

// merge() - Copy state to persistent entity
Employee merged = session.merge(detachedEmployee);

// saveOrUpdate() - Save or update based on ID
session.saveOrUpdate(entity);

// get() - Retrieve entity (eager loading)
Employee emp = session.get(Employee.class, 1L);

// load() - Retrieve entity (lazy loading, returns proxy)
Employee emp = session.load(Employee.class, 1L);

// delete() - Mark entity for deletion
session.delete(entity);

// evict() - Detach entity from session
session.evict(entity);

// clear() - Detach all entities
session.clear();

// refresh() - Reload entity from database
session.refresh(entity);
```

---

## 6. Relationships and Associations

### @OneToOne Relationship

**Unidirectional One-to-One**

```java
@Entity
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String username;

    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "profile_id", referencedColumnName = "id")
    private UserProfile profile;
}

@Entity
public class UserProfile {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String bio;
    private String website;
}
```

**Bidirectional One-to-One**

```java
@Entity
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String username;

    @OneToOne(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private UserProfile profile;
}

@Entity
public class UserProfile {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String bio;

    @OneToOne
    @JoinColumn(name = "user_id")
    private User user;
}
```

### @OneToMany and @ManyToOne Relationship

**Bidirectional One-to-Many (Recommended)**

```java
@Entity
public class Department {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    @OneToMany(mappedBy = "department", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Employee> employees = new ArrayList<>();

    // Helper methods
    public void addEmployee(Employee employee) {
        employees.add(employee);
        employee.setDepartment(this);
    }

    public void removeEmployee(Employee employee) {
        employees.remove(employee);
        employee.setDepartment(null);
    }
}

@Entity
public class Employee {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "department_id")
    private Department department;
}
```

**Unidirectional One-to-Many (Not Recommended - Creates Extra Table)**

```java
@Entity
public class Cart {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "cart_id")  // Puts FK in Item table
    private List<Item> items = new ArrayList<>();
}

@Entity
public class Item {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
}
```

### @ManyToMany Relationship

**Bidirectional Many-to-Many**

```java
@Entity
public class Student {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    @ManyToMany(cascade = {CascadeType.PERSIST, CascadeType.MERGE})
    @JoinTable(
        name = "student_course",
        joinColumns = @JoinColumn(name = "student_id"),
        inverseJoinColumns = @JoinColumn(name = "course_id")
    )
    private Set<Course> courses = new HashSet<>();

    // Helper methods
    public void enrollCourse(Course course) {
        courses.add(course);
        course.getStudents().add(this);
    }

    public void unenrollCourse(Course course) {
        courses.remove(course);
        course.getStudents().remove(this);
    }
}

@Entity
public class Course {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;

    @ManyToMany(mappedBy = "courses")
    private Set<Student> students = new HashSet<>();
}
```

### Cascade Types

```java
public enum CascadeType {
    ALL,       // Apply all cascade operations
    PERSIST,   // Cascade save operations
    MERGE,     // Cascade merge operations
    REMOVE,    // Cascade delete operations
    REFRESH,   // Cascade refresh operations
    DETACH     // Cascade detach operations
}

// Example usage
@OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
private List<Employee> employees;

// Multiple cascade types
@OneToMany(cascade = {CascadeType.PERSIST, CascadeType.MERGE})
private List<Employee> employees;
```

---

## 7. Querying in Hibernate

### HQL (Hibernate Query Language)

**Basic HQL Queries**

```java
// Select all entities
String hql = "FROM Employee";
Query<Employee> query = session.createQuery(hql, Employee.class);
List<Employee> employees = query.getResultList();

// Select with WHERE clause
String hql = "FROM Employee e WHERE e.salary > :minSalary";
Query<Employee> query = session.createQuery(hql, Employee.class);
query.setParameter("minSalary", 50000.0);
List<Employee> employees = query.getResultList();

// Select specific columns
String hql = "SELECT e.firstName, e.lastName FROM Employee e";
Query<Object[]> query = session.createQuery(hql);
List<Object[]> results = query.getResultList();
for (Object[] row : results) {
    System.out.println(row[0] + " " + row[1]);
}

// Join query
String hql = "SELECT e FROM Employee e JOIN FETCH e.department WHERE e.salary > :salary";
Query<Employee> query = session.createQuery(hql, Employee.class);
query.setParameter("salary", 50000.0);
List<Employee> employees = query.getResultList();
```

**HQL Update and Delete**

```java
// Update query
String hql = "UPDATE Employee SET salary = salary * 1.1 WHERE department.name = :deptName";
Query query = session.createQuery(hql);
query.setParameter("deptName", "IT");
int updatedRows = query.executeUpdate();

// Delete query
String hql = "DELETE FROM Employee WHERE isActive = false";
Query query = session.createQuery(hql);
int deletedRows = query.executeUpdate();
```

**Aggregate Functions**

```java
// Count
String hql = "SELECT COUNT(e) FROM Employee e WHERE e.department.name = :deptName";
Query<Long> query = session.createQuery(hql, Long.class);
query.setParameter("deptName", "IT");
Long count = query.getSingleResult();

// Average, Max, Min, Sum
String hql = "SELECT AVG(e.salary), MAX(e.salary), MIN(e.salary), SUM(e.salary) FROM Employee e";
Query<Object[]> query = session.createQuery(hql);
Object[] result = query.getSingleResult();
```

**Named Queries**

```java
@Entity
@NamedQueries({
    @NamedQuery(
        name = "Employee.findAll",
        query = "FROM Employee"
    ),
    @NamedQuery(
        name = "Employee.findByDepartment",
        query = "FROM Employee e WHERE e.department.name = :deptName"
    )
})
public class Employee {
    // ... entity fields
}

// Using named query
Query<Employee> query = session.createNamedQuery("Employee.findByDepartment", Employee.class);
query.setParameter("deptName", "IT");
List<Employee> employees = query.getResultList();
```

### Criteria API

```java
// CriteriaBuilder approach
CriteriaBuilder cb = session.getCriteriaBuilder();
CriteriaQuery<Employee> cq = cb.createQuery(Employee.class);
Root<Employee> root = cq.from(Employee.class);

// Simple query
cq.select(root);
List<Employee> employees = session.createQuery(cq).getResultList();

// With WHERE clause
Predicate salaryCondition = cb.gt(root.get("salary"), 50000);
cq.select(root).where(salaryCondition);
List<Employee> employees = session.createQuery(cq).getResultList();

// Multiple conditions
Predicate condition1 = cb.gt(root.get("salary"), 50000);
Predicate condition2 = cb.equal(root.get("isActive"), true);
cq.select(root).where(cb.and(condition1, condition2));

// Order by
cq.select(root).orderBy(cb.desc(root.get("salary")));

// Group by and having
cq.multiselect(root.get("department"), cb.count(root))
  .groupBy(root.get("department"))
  .having(cb.gt(cb.count(root), 5));
```

### Native SQL Queries

```java
// Native SQL query
String sql = "SELECT * FROM employees WHERE salary > :salary";
Query<Employee> query = session.createNativeQuery(sql, Employee.class);
query.setParameter("salary", 50000);
List<Employee> employees = query.getResultList();

// Named native query
@Entity
@NamedNativeQuery(
    name = "Employee.getAllWithHighSalary",
    query = "SELECT e.id, e.first_name, e.last_name, e.salary " +
            "FROM employees e WHERE e.salary > :minSalary",
    resultClass = Employee.class
)
public class Employee {
    // ...
}
```

---

## 8. Spring Data JPA Repository

### Repository Hierarchy

```
Repository (marker interface)
    │
    ├── CrudRepository (basic CRUD operations)
    │       │
    │       └── PagingAndSortingRepository (pagination & sorting)
    │               │
    │               └── JpaRepository (JPA specific methods)
```

### Repository Interface

```java
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;
import java.util.Optional;

public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    // Derived query methods - Spring generates implementation

    // Find by single property
    List<Employee> findByFirstName(String firstName);

    // Find by multiple properties
    List<Employee> findByFirstNameAndLastName(String firstName, String lastName);

    // Find with comparison
    List<Employee> findBySalaryGreaterThan(Double salary);
    List<Employee> findBySalaryBetween(Double min, Double max);

    // Find with LIKE
    List<Employee> findByFirstNameContaining(String keyword);
    List<Employee> findByEmailStartingWith(String prefix);

    // Find with sorting
    List<Employee> findByDepartmentNameOrderBySalaryDesc(String deptName);

    // Find with boolean
    List<Employee> findByIsActiveTrue();

    // Find top results
    List<Employee> findTop10BySalaryOrderBySalaryDesc(Double salary);

    // Count
    Long countByDepartmentName(String deptName);

    // Exists
    Boolean existsByEmail(String email);

    // Delete
    void deleteByIsActiveFalse();

    // Custom JPQL queries with @Query
    @Query("SELECT e FROM Employee e WHERE e.salary > :salary")
    List<Employee> findEmployeesWithHighSalary(@Param("salary") Double salary);

    @Query("SELECT e FROM Employee e JOIN FETCH e.department WHERE e.id = :id")
    Optional<Employee> findByIdWithDepartment(@Param("id") Long id);

    // Native SQL query
    @Query(value = "SELECT * FROM employees WHERE salary > ?1", nativeQuery = true)
    List<Employee> findEmployeesWithHighSalaryNative(Double salary);

    // Update query
    @Modifying
    @Query("UPDATE Employee e SET e.salary = e.salary * 1.1 WHERE e.department.name = :deptName")
    int increaseSalaryByDepartment(@Param("deptName") String deptName);

    // Delete query
    @Modifying
    @Query("DELETE FROM Employee e WHERE e.isActive = false")
    int deleteInactiveEmployees();
}
```

### Service Layer Example

```java
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
@Transactional
public class EmployeeService {

    private final EmployeeRepository employeeRepository;

    // Create
    public Employee createEmployee(Employee employee) {
        return employeeRepository.save(employee);
    }

    // Read
    @Transactional(readOnly = true)
    public Optional<Employee> getEmployeeById(Long id) {
        return employeeRepository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<Employee> getAllEmployees() {
        return employeeRepository.findAll();
    }

    // Update
    public Employee updateEmployee(Long id, Employee updatedEmployee) {
        return employeeRepository.findById(id)
            .map(employee -> {
                employee.setFirstName(updatedEmployee.getFirstName());
                employee.setLastName(updatedEmployee.getLastName());
                employee.setSalary(updatedEmployee.getSalary());
                return employeeRepository.save(employee);
            })
            .orElseThrow(() -> new RuntimeException("Employee not found"));
    }

    // Delete
    public void deleteEmployee(Long id) {
        employeeRepository.deleteById(id);
    }

    // Custom methods
    @Transactional(readOnly = true)
    public List<Employee> getHighEarners(Double minSalary) {
        return employeeRepository.findBySalaryGreaterThan(minSalary);
    }
}
```

### Controller Example

```java
import org.springframework.web.bind.annotation.*;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/api/employees")
@RequiredArgsConstructor
public class EmployeeController {

    private final EmployeeService employeeService;

    @PostMapping
    public ResponseEntity<Employee> createEmployee(@Valid @RequestBody Employee employee) {
        Employee created = employeeService.createEmployee(employee);
        return ResponseEntity.ok(created);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Employee> getEmployee(@PathVariable Long id) {
        return employeeService.getEmployeeById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping
    public ResponseEntity<List<Employee>> getAllEmployees() {
        List<Employee> employees = employeeService.getAllEmployees();
        return ResponseEntity.ok(employees);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Employee> updateEmployee(
            @PathVariable Long id,
            @Valid @RequestBody Employee employee) {
        Employee updated = employeeService.updateEmployee(id, employee);
        return ResponseEntity.ok(updated);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteEmployee(@PathVariable Long id) {
        employeeService.deleteEmployee(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/high-earners")
    public ResponseEntity<List<Employee>> getHighEarners(@RequestParam Double minSalary) {
        List<Employee> employees = employeeService.getHighEarners(minSalary);
        return ResponseEntity.ok(employees);
    }
}
```

---

## 9. Hibernate Session and SessionFactory

### SessionFactory Configuration (Traditional Hibernate)

```java
import org.hibernate.SessionFactory;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.cfg.Configuration;
import org.hibernate.service.ServiceRegistry;

public class HibernateUtil {

    private static SessionFactory sessionFactory;

    public static SessionFactory getSessionFactory() {
        if (sessionFactory == null) {
            try {
                Configuration configuration = new Configuration();

                // Database settings
                configuration.setProperty("hibernate.connection.driver_class",
                    "com.mysql.cj.jdbc.Driver");
                configuration.setProperty("hibernate.connection.url",
                    "jdbc:mysql://localhost:3306/mydb");
                configuration.setProperty("hibernate.connection.username", "root");
                configuration.setProperty("hibernate.connection.password", "password");

                // Hibernate settings
                configuration.setProperty("hibernate.dialect",
                    "org.hibernate.dialect.MySQL8Dialect");
                configuration.setProperty("hibernate.hbm2ddl.auto", "update");
                configuration.setProperty("hibernate.show_sql", "true");
                configuration.setProperty("hibernate.format_sql", "true");

                // Add annotated classes
                configuration.addAnnotatedClass(Employee.class);
                configuration.addAnnotatedClass(Department.class);

                ServiceRegistry serviceRegistry = new StandardServiceRegistryBuilder()
                    .applySettings(configuration.getProperties())
                    .build();

                sessionFactory = configuration.buildSessionFactory(serviceRegistry);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return sessionFactory;
    }

    public static void shutdown() {
        if (sessionFactory != null) {
            sessionFactory.close();
        }
    }
}
```

### Using Session

```java
import org.hibernate.Session;
import org.hibernate.Transaction;

public class EmployeeDAO {

    // Create
    public void saveEmployee(Employee employee) {
        Transaction transaction = null;
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            transaction = session.beginTransaction();
            session.save(employee);
            transaction.commit();
        } catch (Exception e) {
            if (transaction != null) {
                transaction.rollback();
            }
            e.printStackTrace();
        }
    }

    // Read
    public Employee getEmployee(Long id) {
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            return session.get(Employee.class, id);
        }
    }

    // Update
    public void updateEmployee(Employee employee) {
        Transaction transaction = null;
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            transaction = session.beginTransaction();
            session.update(employee);
            transaction.commit();
        } catch (Exception e) {
            if (transaction != null) {
                transaction.rollback();
            }
            e.printStackTrace();
        }
    }

    // Delete
    public void deleteEmployee(Long id) {
        Transaction transaction = null;
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            transaction = session.beginTransaction();
            Employee employee = session.get(Employee.class, id);
            if (employee != null) {
                session.delete(employee);
            }
            transaction.commit();
        } catch (Exception e) {
            if (transaction != null) {
                transaction.rollback();
            }
            e.printStackTrace();
        }
    }

    // List all
    public List<Employee> getAllEmployees() {
        try (Session session = HibernateUtil.getSessionFactory().openSession()) {
            return session.createQuery("FROM Employee", Employee.class).list();
        }
    }
}
```

### getCurrentSession() vs openSession()

```java
// openSession() - Always opens a new session
Session session = sessionFactory.openSession();
// Must close manually
session.close();

// getCurrentSession() - Gets current session bound to context
Session session = sessionFactory.getCurrentSession();
// Automatically closed when transaction ends
// Requires configuration:
// <property name="hibernate.current_session_context_class">thread</property>
```

---

## 10. Transaction Management

### Declarative Transaction Management with @Transactional

```java
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Isolation;

@Service
public class TransactionService {

    // Basic @Transactional
    @Transactional
    public void performTransaction() {
        // All database operations in single transaction
    }

    // Read-only transaction (optimization)
    @Transactional(readOnly = true)
    public Employee getEmployee(Long id) {
        return employeeRepository.findById(id).orElse(null);
    }

    // Rollback on specific exceptions
    @Transactional(rollbackFor = CustomException.class)
    public void riskyOperation() throws CustomException {
        // Transaction will rollback on CustomException
    }

    // No rollback on specific exceptions
    @Transactional(noRollbackFor = ValidationException.class)
    public void operationWithValidation() throws ValidationException {
        // Transaction won't rollback on ValidationException
    }

    // Transaction timeout
    @Transactional(timeout = 30) // 30 seconds
    public void longRunningOperation() {
        // Transaction will timeout after 30 seconds
    }

    // Propagation levels
    @Transactional(propagation = Propagation.REQUIRED) // Default
    public void required() {
        // Use existing transaction or create new one
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void requiresNew() {
        // Always create new transaction, suspend existing one
    }

    @Transactional(propagation = Propagation.SUPPORTS)
    public void supports() {
        // Execute within transaction if one exists, otherwise non-transactional
    }

    @Transactional(propagation = Propagation.MANDATORY)
    public void mandatory() {
        // Must be called within existing transaction
    }

    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public void notSupported() {
        // Execute non-transactionally, suspend existing transaction
    }

    @Transactional(propagation = Propagation.NEVER)
    public void never() {
        // Execute non-transactionally, throw exception if transaction exists
    }

    @Transactional(propagation = Propagation.NESTED)
    public void nested() {
        // Execute within nested transaction if exists
    }

    // Isolation levels
    @Transactional(isolation = Isolation.READ_UNCOMMITTED)
    public void readUncommitted() {
        // Lowest isolation, allows dirty reads
    }

    @Transactional(isolation = Isolation.READ_COMMITTED)
    public void readCommitted() {
        // Prevents dirty reads
    }

    @Transactional(isolation = Isolation.REPEATABLE_READ)
    public void repeatableRead() {
        // Prevents dirty and non-repeatable reads
    }

    @Transactional(isolation = Isolation.SERIALIZABLE)
    public void serializable() {
        // Highest isolation, prevents phantom reads
    }
}
```

### Programmatic Transaction Management

```java
import org.springframework.transaction.support.TransactionTemplate;
import org.springframework.transaction.PlatformTransactionManager;

@Service
public class ProgrammaticTransactionService {

    private final TransactionTemplate transactionTemplate;

    public ProgrammaticTransactionService(PlatformTransactionManager transactionManager) {
        this.transactionTemplate = new TransactionTemplate(transactionManager);
    }

    public Employee saveEmployee(Employee employee) {
        return transactionTemplate.execute(status -> {
            try {
                return employeeRepository.save(employee);
            } catch (Exception e) {
                status.setRollbackOnly();
                throw e;
            }
        });
    }
}
```

---

## 11. Caching in Hibernate

### First-Level Cache (Session Cache)

```java
// First-level cache is enabled by default
Session session = sessionFactory.openSession();
Transaction tx = session.beginTransaction();

// First call - hits database
Employee emp1 = session.get(Employee.class, 1L);

// Second call - from cache (no SQL)
Employee emp2 = session.get(Employee.class, 1L);

// Same instance
System.out.println(emp1 == emp2); // true

tx.commit();
session.close();
```

### Second-Level Cache (SessionFactory Cache)

**Configuration (application.properties)**

```properties
# Enable second-level cache
spring.jpa.properties.hibernate.cache.use_second_level_cache=true
spring.jpa.properties.hibernate.cache.region.factory_class=org.hibernate.cache.jcache.JCacheRegionFactory

# Query cache (optional)
spring.jpa.properties.hibernate.cache.use_query_cache=true

# Cache provider - EhCache
spring.jpa.properties.hibernate.javax.cache.provider=org.ehcache.jsr107.EhcacheCachingProvider
```

**Entity Configuration**

```java
import org.hibernate.annotations.Cache;
import org.hibernate.annotations.CacheConcurrencyStrategy;

@Entity
@Cacheable
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
public class Employee {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String firstName;
    private String lastName;

    @Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
    @OneToMany(mappedBy = "employee")
    private List<Project> projects;
}
```

**Cache Concurrency Strategies**

```java
// READ_ONLY - Best for data that never changes
@Cache(usage = CacheConcurrencyStrategy.READ_ONLY)

// NONSTRICT_READ_WRITE - For occasional writes
@Cache(usage = CacheConcurrencyStrategy.NONSTRICT_READ_WRITE)

// READ_WRITE - For frequently updated data (default)
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)

// TRANSACTIONAL - JTA transactions
@Cache(usage = CacheConcurrencyStrategy.TRANSACTIONAL)
```

**Query Cache**

```java
// Enable query cache for specific query
@Query("SELECT e FROM Employee e WHERE e.salary > :salary")
@QueryHints(@QueryHint(name = "org.hibernate.cacheable", value = "true"))
List<Employee> findHighEarners(@Param("salary") Double salary);

// Or programmatically
Query<Employee> query = session.createQuery("FROM Employee", Employee.class);
query.setCacheable(true);
query.setCacheRegion("employeeCache");
List<Employee> employees = query.getResultList();
```

### Cache Operations

```java
// Evict entity from cache
sessionFactory.getCache().evict(Employee.class, employeeId);

// Evict all entities of a class
sessionFactory.getCache().evict(Employee.class);

// Evict entire cache
sessionFactory.getCache().evictAllRegions();

// Check if entity is in cache
boolean isCached = sessionFactory.getCache().contains(Employee.class, employeeId);
```

---

## 12. Fetching Strategies

### Lazy vs Eager Loading

```java
// LAZY Loading (default for @OneToMany, @ManyToMany)
@OneToMany(fetch = FetchType.LAZY, mappedBy = "department")
private List<Employee> employees; // Loaded when accessed

// EAGER Loading (default for @ManyToOne, @OneToOne)
@ManyToOne(fetch = FetchType.EAGER)
@JoinColumn(name = "department_id")
private Department department; // Loaded immediately
```

**Example**

```java
@Entity
public class Department {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    // Lazy loading - employees loaded only when accessed
    @OneToMany(mappedBy = "department", fetch = FetchType.LAZY)
    private List<Employee> employees;
}

// Usage
Department dept = departmentRepository.findById(1L).orElse(null);
System.out.println(dept.getName()); // No SQL for employees

// This triggers SQL to fetch employees
List<Employee> emps = dept.getEmployees(); // LazyInitializationException if session closed
```

### JOIN FETCH to Avoid LazyInitializationException

```java
// JPQL with JOIN FETCH
@Query("SELECT d FROM Department d JOIN FETCH d.employees WHERE d.id = :id")
Department findByIdWithEmployees(@Param("id") Long id);

// Multiple JOIN FETCH
@Query("SELECT e FROM Employee e " +
       "JOIN FETCH e.department " +
       "JOIN FETCH e.projects " +
       "WHERE e.id = :id")
Employee findByIdWithDepartmentAndProjects(@Param("id") Long id);
```

### @EntityGraph

```java
@Entity
@NamedEntityGraphs({
    @NamedEntityGraph(
        name = "Employee.detail",
        attributeNodes = {
            @NamedAttributeNode("department"),
            @NamedAttributeNode("projects")
        }
    )
})
public class Employee {
    // ...
}

// In repository
@EntityGraph(value = "Employee.detail", type = EntityGraphType.FETCH)
Optional<Employee> findById(Long id);

// Ad-hoc EntityGraph
@EntityGraph(attributePaths = {"department", "projects"})
List<Employee> findAll();
```

### Batch Fetching

```java
@Entity
public class Department {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Batch fetch employees in batches of 10
    @OneToMany(mappedBy = "department")
    @BatchSize(size = 10)
    private List<Employee> employees;
}
```

---

## 13. N+1 Problem and Solutions

### Understanding N+1 Problem

```java
// N+1 Problem Example
List<Department> departments = departmentRepository.findAll(); // 1 query
for (Department dept : departments) {
    List<Employee> employees = dept.getEmployees(); // N queries (one per department)
    System.out.println(dept.getName() + " has " + employees.size() + " employees");
}
// Total: 1 + N queries
```

### Solution 1: JOIN FETCH

```java
@Query("SELECT d FROM Department d JOIN FETCH d.employees")
List<Department> findAllWithEmployees();

// Usage - single query
List<Department> departments = departmentRepository.findAllWithEmployees();
for (Department dept : departments) {
    System.out.println(dept.getName() + " has " + dept.getEmployees().size() + " employees");
}
```

### Solution 2: @EntityGraph

```java
@EntityGraph(attributePaths = {"employees"})
List<Department> findAll();
```

### Solution 3: Batch Fetching

```java
@Entity
public class Department {
    @OneToMany(mappedBy = "department")
    @BatchSize(size = 10)
    private List<Employee> employees;
}

// Fetches employees for 10 departments at a time
```

### Solution 4: @Fetch(FetchMode.SUBSELECT)

```java
@Entity
public class Department {
    @OneToMany(mappedBy = "department")
    @Fetch(FetchMode.SUBSELECT)
    private List<Employee> employees;
}
```

### Enable SQL Logging to Detect N+1

```properties
# Show SQL
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true

# Show parameter binding
logging.level.org.hibernate.type.descriptor.sql.BasicBinder=TRACE

# Show statistics
spring.jpa.properties.hibernate.generate_statistics=true
logging.level.org.hibernate.stat=DEBUG
```

---

## 14. Batch Processing

### Configuration

```properties
# Batch size
spring.jpa.properties.hibernate.jdbc.batch_size=50
spring.jpa.properties.hibernate.order_inserts=true
spring.jpa.properties.hibernate.order_updates=true
spring.jpa.properties.hibernate.jdbc.batch_versioned_data=true
```

### Batch Insert Example

```java
@Transactional
public void batchInsertEmployees(List<Employee> employees) {
    int batchSize = 50;
    for (int i = 0; i < employees.size(); i++) {
        entityManager.persist(employees.get(i));

        if (i % batchSize == 0 && i > 0) {
            // Flush and clear every batch
            entityManager.flush();
            entityManager.clear();
        }
    }
    // Flush remaining
    entityManager.flush();
    entityManager.clear();
}
```

### Batch Update Example

```java
@Transactional
public void batchUpdateEmployees(List<Employee> employees) {
    int batchSize = 50;
    for (int i = 0; i < employees.size(); i++) {
        Employee employee = employees.get(i);
        employee.setSalary(employee.getSalary() * 1.1);
        entityManager.merge(employee);

        if (i % batchSize == 0 && i > 0) {
            entityManager.flush();
            entityManager.clear();
        }
    }
    entityManager.flush();
    entityManager.clear();
}
```

### Using StatelessSession for Large Batches

```java
public void batchInsertWithStatelessSession(List<Employee> employees) {
    StatelessSession session = sessionFactory.openStatelessSession();
    Transaction tx = session.beginTransaction();

    try {
        for (Employee employee : employees) {
            session.insert(employee);
        }
        tx.commit();
    } catch (Exception e) {
        tx.rollback();
        throw e;
    } finally {
        session.close();
    }
}
```

---

## 15. Pagination

### Using setFirstResult() and setMaxResults()

```java
@Repository
public class EmployeeDAO {

    @PersistenceContext
    private EntityManager entityManager;

    public List<Employee> getEmployeesPage(int pageNumber, int pageSize) {
        TypedQuery<Employee> query = entityManager.createQuery(
            "SELECT e FROM Employee e ORDER BY e.id", Employee.class);

        query.setFirstResult(pageNumber * pageSize);  // Offset
        query.setMaxResults(pageSize);                 // Limit

        return query.getResultList();
    }
}
```

### Spring Data JPA Pageable

```java
// Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    Page<Employee> findByDepartmentName(String deptName, Pageable pageable);

    @Query("SELECT e FROM Employee e WHERE e.salary > :salary")
    Page<Employee> findHighEarners(@Param("salary") Double salary, Pageable pageable);
}

// Service
@Service
public class EmployeeService {

    @Autowired
    private EmployeeRepository employeeRepository;

    public Page<Employee> getEmployees(int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by("salary").descending());
        return employeeRepository.findAll(pageable);
    }

    public Page<Employee> getEmployeesByDepartment(String deptName, int page, int size) {
        Pageable pageable = PageRequest.of(page, size);
        return employeeRepository.findByDepartmentName(deptName, pageable);
    }
}

// Controller
@RestController
@RequestMapping("/api/employees")
public class EmployeeController {

    @Autowired
    private EmployeeService employeeService;

    @GetMapping
    public ResponseEntity<Page<Employee>> getEmployees(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {

        Page<Employee> employeePage = employeeService.getEmployees(page, size);
        return ResponseEntity.ok(employeePage);
    }
}
```

### Custom Pagination Response

```java
@Data
public class PageResponse<T> {
    private List<T> content;
    private int pageNumber;
    private int pageSize;
    private long totalElements;
    private int totalPages;
    private boolean last;

    public static <T> PageResponse<T> of(Page<T> page) {
        PageResponse<T> response = new PageResponse<>();
        response.setContent(page.getContent());
        response.setPageNumber(page.getNumber());
        response.setPageSize(page.getSize());
        response.setTotalElements(page.getTotalElements());
        response.setTotalPages(page.getTotalPages());
        response.setLast(page.isLast());
        return response;
    }
}
```

---

## 16. Inheritance Strategies

### SINGLE_TABLE Strategy

```java
@Entity
@Table(name = "vehicles")
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
@DiscriminatorColumn(name = "vehicle_type", discriminatorType = DiscriminatorType.STRING)
public abstract class Vehicle {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String manufacturer;
    private String model;
}

@Entity
@DiscriminatorValue("CAR")
public class Car extends Vehicle {
    private Integer numberOfDoors;
}

@Entity
@DiscriminatorValue("BIKE")
public class Bike extends Vehicle {
    private Boolean hasCarrier;
}
```

**Advantages**:

- Simple, fast queries (no joins)
- Best performance

**Disadvantages**:

- Cannot use NOT NULL constraints on subclass fields
- Table can become large

### JOINED Strategy

```java
@Entity
@Table(name = "vehicles")
@Inheritance(strategy = InheritanceType.JOINED)
public abstract class Vehicle {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String manufacturer;
    private String model;
}

@Entity
@Table(name = "cars")
public class Car extends Vehicle {
    private Integer numberOfDoors;
}

@Entity
@Table(name = "bikes")
public class Bike extends Vehicle {
    private Boolean hasCarrier;
}
```

**Advantages**:

- Normalized database
- Can use constraints on subclass fields

**Disadvantages**:

- Requires joins for queries
- Slower performance

### TABLE_PER_CLASS Strategy

```java
@Entity
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)
public abstract class Vehicle {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    private String manufacturer;
    private String model;
}

@Entity
@Table(name = "cars")
public class Car extends Vehicle {
    private Integer numberOfDoors;
}

@Entity
@Table(name = "bikes")
public class Bike extends Vehicle {
    private Boolean hasCarrier;
}
```

**Advantages**:

- Each class has its own table
- No joins needed for subclass queries

**Disadvantages**:

- Duplicate columns in each table
- Polymorphic queries are slow (UNION)

---

## 17. Composite Primary Keys

### Using @IdClass

```java
// ID class
import java.io.Serializable;
import lombok.Data;

@Data
public class OrderItemId implements Serializable {
    private Long orderId;
    private Long productId;

    // Must implement equals() and hashCode()
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof OrderItemId)) return false;
        OrderItemId that = (OrderItemId) o;
        return Objects.equals(orderId, that.orderId) &&
               Objects.equals(productId, that.productId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(orderId, productId);
    }
}

// Entity
@Entity
@IdClass(OrderItemId.class)
public class OrderItem {
    @Id
    @Column(name = "order_id")
    private Long orderId;

    @Id
    @Column(name = "product_id")
    private Long productId;

    private Integer quantity;
    private Double price;
}

// Usage
OrderItem item = new OrderItem();
item.setOrderId(1L);
item.setProductId(100L);
item.setQuantity(5);
entityManager.persist(item);

// Find
OrderItemId id = new OrderItemId();
id.setOrderId(1L);
id.setProductId(100L);
OrderItem found = entityManager.find(OrderItem.class, id);
```

### Using @EmbeddedId

```java
// Embeddable ID class
@Embeddable
@Data
public class OrderItemId implements Serializable {
    @Column(name = "order_id")
    private Long orderId;

    @Column(name = "product_id")
    private Long productId;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof OrderItemId)) return false;
        OrderItemId that = (OrderItemId) o;
        return Objects.equals(orderId, that.orderId) &&
               Objects.equals(productId, that.productId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(orderId, productId);
    }
}

// Entity
@Entity
public class OrderItem {
    @EmbeddedId
    private OrderItemId id;

    private Integer quantity;
    private Double price;
}

// Usage
OrderItemId id = new OrderItemId();
id.setOrderId(1L);
id.setProductId(100L);

OrderItem item = new OrderItem();
item.setId(id);
item.setQuantity(5);
entityManager.persist(item);

// Find
OrderItem found = entityManager.find(OrderItem.class, id);
```

---

## 18. Locking Mechanisms

### Optimistic Locking

```java
@Entity
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private Integer quantity;

    @Version  // Optimistic locking
    private Integer version;
}

// Service
@Service
@Transactional
public class ProductService {

    @Autowired
    private ProductRepository productRepository;

    public void updateProductQuantity(Long productId, Integer newQuantity) {
        Product product = productRepository.findById(productId)
            .orElseThrow(() -> new RuntimeException("Product not found"));

        product.setQuantity(newQuantity);
        productRepository.save(product);
        // If version changed, throws OptimisticLockException
    }
}
```

### Pessimistic Locking

```java
// Repository
public interface ProductRepository extends JpaRepository<Product, Long> {

    // Pessimistic Write Lock
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT p FROM Product p WHERE p.id = :id")
    Optional<Product> findByIdWithWriteLock(@Param("id") Long id);

    // Pessimistic Read Lock
    @Lock(LockModeType.PESSIMISTIC_READ)
    @Query("SELECT p FROM Product p WHERE p.id = :id")
    Optional<Product> findByIdWithReadLock(@Param("id") Long id);
}

// Service
@Service
@Transactional
public class ProductService {

    @Autowired
    private ProductRepository productRepository;

    public void buyProduct(Long productId) {
        // This locks the row until transaction completes
        Product product = productRepository.findByIdWithWriteLock(productId)
            .orElseThrow(() -> new RuntimeException("Product not found"));

        if (product.getQuantity() > 0) {
            product.setQuantity(product.getQuantity() - 1);
            productRepository.save(product);
        } else {
            throw new RuntimeException("Out of stock");
        }
    }
}
```

### Lock Modes Comparison

| Lock Mode                   | Description         | Use Case                                |
| --------------------------- | ------------------- | --------------------------------------- |
| OPTIMISTIC                  | Version-based check | High read, low write contention         |
| OPTIMISTIC_FORCE_INCREMENT  | Increment version   | Prevent updates from other transactions |
| PESSIMISTIC_READ            | Shared lock         | Prevent modifications                   |
| PESSIMISTIC_WRITE           | Exclusive lock      | Prevent any access                      |
| PESSIMISTIC_FORCE_INCREMENT | Lock + increment    | Ensure serialized access                |

---

## 19. Auditing

### Basic Auditing with JPA

```java
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.annotation.CreatedBy;
import org.springframework.data.annotation.LastModifiedBy;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
@Data
public abstract class Auditable {

    @CreatedDate
    @Column(name = "created_date", nullable = false, updatable = false)
    private LocalDateTime createdDate;

    @LastModifiedDate
    @Column(name = "modified_date")
    private LocalDateTime modifiedDate;

    @CreatedBy
    @Column(name = "created_by", updatable = false)
    private String createdBy;

    @LastModifiedBy
    @Column(name = "modified_by")
    private String modifiedBy;
}

// Entity extends auditable base class
@Entity
public class Employee extends Auditable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String firstName;
    private String lastName;
}
```

### Auditor Provider

```java
import org.springframework.data.domain.AuditorAware;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import java.util.Optional;

@Component
public class AuditorAwareImpl implements AuditorAware<String> {

    @Override
    public Optional<String> getCurrentAuditor() {
        // Get current user from security context
        String username = SecurityContextHolder.getContext()
            .getAuthentication()
            .getName();
        return Optional.ofNullable(username);
    }
}
```

### Hibernate Envers (Advanced Auditing)

**Dependencies**

```xml
<dependency>
    <groupId>org.hibernate</groupId>
    <artifactId>hibernate-envers</artifactId>
</dependency>
```

**Entity Configuration**

```java
import org.hibernate.envers.Audited;
import org.hibernate.envers.NotAudited;

@Entity
@Audited  // Enable auditing for entire entity
public class Employee {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String firstName;
    private String lastName;

    @NotAudited  // Exclude from auditing
    private String tempData;
}
```

**Querying Audit History**

```java
import org.hibernate.envers.AuditReader;
import org.hibernate.envers.AuditReaderFactory;
import org.hibernate.envers.query.AuditEntity;

@Service
public class AuditService {

    @PersistenceContext
    private EntityManager entityManager;

    // Get all revisions of an entity
    public List<Number> getRevisions(Long employeeId) {
        AuditReader auditReader = AuditReaderFactory.get(entityManager);
        return auditReader.getRevisions(Employee.class, employeeId);
    }

    // Get entity at specific revision
    public Employee getEmployeeAtRevision(Long employeeId, Number revision) {
        AuditReader auditReader = AuditReaderFactory.get(entityManager);
        return auditReader.find(Employee.class, employeeId, revision);
    }

    // Get all historical versions
    public List<Employee> getEmployeeHistory(Long employeeId) {
        AuditReader auditReader = AuditReaderFactory.get(entityManager);

        List<Number> revisions = auditReader.getRevisions(Employee.class, employeeId);
        List<Employee> history = new ArrayList<>();

        for (Number revision : revisions) {
            Employee emp = auditReader.find(Employee.class, employeeId, revision);
            history.add(emp);
        }

        return history;
    }

    // Query audit trail
    public List<Employee> findEmployeesModifiedAfter(LocalDateTime date) {
        AuditReader auditReader = AuditReaderFactory.get(entityManager);

        return auditReader.createQuery()
            .forRevisionsOfEntity(Employee.class, false, true)
            .add(AuditEntity.revisionProperty("timestamp").ge(date))
            .getResultList();
    }
}
```

---

## 20. Performance Optimization

### Connection Pooling (HikariCP)

```properties
# HikariCP configuration
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.connection-timeout=30000
spring.datasource.hikari.idle-timeout=600000
spring.datasource.hikari.max-lifetime=1800000
spring.datasource.hikari.pool-name=HikariCP-Pool
```

### Query Optimization

```java
// Use DTOs/Projections instead of full entities
@Query("SELECT new com.example.dto.EmployeeDTO(e.id, e.firstName, e.lastName) " +
       "FROM Employee e WHERE e.department.name = :deptName")
List<EmployeeDTO> findEmployeeDTOsByDepartment(@Param("deptName") String deptName);

// Interface-based projection
public interface EmployeeProjection {
    Long getId();
    String getFirstName();
    String getLastName();
}

@Query("SELECT e.id as id, e.firstName as firstName, e.lastName as lastName " +
       "FROM Employee e WHERE e.salary > :salary")
List<EmployeeProjection> findEmployeeProjections(@Param("salary") Double salary);
```

### Index Usage

```java
@Entity
@Table(name = "employees", indexes = {
    @Index(name = "idx_email", columnList = "email", unique = true),
    @Index(name = "idx_dept_salary", columnList = "department_id, salary"),
    @Index(name = "idx_last_name", columnList = "last_name")
})
public class Employee {
    // ...
}
```

### Hibernate Statistics

```properties
# Enable statistics
spring.jpa.properties.hibernate.generate_statistics=true
logging.level.org.hibernate.stat=DEBUG
```

```java
import org.hibernate.stat.Statistics;
import org.hibernate.SessionFactory;

@Service
public class StatisticsService {

    @Autowired
    private EntityManagerFactory entityManagerFactory;

    public void printStatistics() {
        SessionFactory sessionFactory = entityManagerFactory.unwrap(SessionFactory.class);
        Statistics stats = sessionFactory.getStatistics();

        System.out.println("Entity Fetch Count: " + stats.getEntityFetchCount());
        System.out.println("Query Execution Count: " + stats.getQueryExecutionCount());
        System.out.println("Second Level Cache Hit Count: " + stats.getSecondLevelCacheHitCount());
        System.out.println("Second Level Cache Miss Count: " + stats.getSecondLevelCacheMissCount());

        // Clear statistics
        stats.clear();
    }
}
```

---

## 21. Best Practices

### 1. Entity Design Best Practices

```java
// ✅ DO: Use @Data from Lombok carefully
@Entity
@Getter
@Setter
@NoArgsConstructor
public class Employee {
    // Avoid @Data as it generates toString/equals/hashCode that can cause issues
}

// ✅ DO: Override equals() and hashCode() properly
@Entity
public class Employee {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Employee)) return false;
        Employee employee = (Employee) o;
        return Objects.equals(id, employee.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}

// ✅ DO: Use helper methods for bidirectional associations
@Entity
public class Department {
    @OneToMany(mappedBy = "department", cascade = CascadeType.ALL)
    private List<Employee> employees = new ArrayList<>();

    public void addEmployee(Employee employee) {
        employees.add(employee);
        employee.setDepartment(this);
    }

    public void removeEmployee(Employee employee) {
        employees.remove(employee);
        employee.setDepartment(null);
    }
}
```

### 2. Transaction Management Best Practices

```java
// ✅ DO: Keep transactions short
@Transactional
public void processOrder(Order order) {
    // Database operations only
    orderRepository.save(order);
}

// ❌ DON'T: Include long-running operations in transactions
@Transactional  // BAD
public void processOrderBad(Order order) {
    orderRepository.save(order);
    sendEmail(order);  // Long-running operation
    callExternalAPI(order);  // Network call
}

// ✅ DO: Use read-only transactions for read operations
@Transactional(readOnly = true)
public List<Employee> getAllEmployees() {
    return employeeRepository.findAll();
}
```

### 3. Fetching Best Practices

```java
// ✅ DO: Use appropriate fetch type
@Entity
public class Order {
    @ManyToOne(fetch = FetchType.LAZY)  // Default for @ManyToOne should be LAZY
    private Customer customer;

    @OneToMany(fetch = FetchType.LAZY)  // LAZY for collections
    private List<OrderItem> items;
}

// ✅ DO: Use JOIN FETCH for N+1 prevention
@Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.id = :id")
Order findByIdWithItems(@Param("id") Long id);

// ✅ DO: Use @EntityGraph for dynamic fetching
@EntityGraph(attributePaths = {"items", "customer"})
Optional<Order> findById(Long id);
```

### 4. Query Best Practices

```java
// ✅ DO: Use named parameters
@Query("SELECT e FROM Employee e WHERE e.firstName = :firstName")
List<Employee> findByFirstName(@Param("firstName") String firstName);

// ❌ DON'T: Use positional parameters
@Query("SELECT e FROM Employee e WHERE e.firstName = ?1")
List<Employee> findByFirstNameBad(String firstName);

// ✅ DO: Use pagination for large results
@Query("SELECT e FROM Employee e")
Page<Employee> findAllEmployees(Pageable pageable);

// ✅ DO: Use projections for specific data
@Query("SELECT new com.example.dto.EmployeeDTO(e.id, e.firstName) FROM Employee e")
List<EmployeeDTO> findAllEmployeeDTOs();
```

### 5. Session Management

```java
// ✅ DO: Close session properly
try (Session session = sessionFactory.openSession()) {
    Transaction tx = session.beginTransaction();
    // operations
    tx.commit();
} catch (Exception e) {
    tx.rollback();
    throw e;
}

// ✅ DO: Clear session periodically in batch operations
for (int i = 0; i < items.size(); i++) {
    entityManager.persist(items.get(i));
    if (i % 50 == 0) {
        entityManager.flush();
        entityManager.clear();
    }
}
```

### 6. Common Pitfalls to Avoid

```java
// ❌ AVOID: Using @OneToMany without mappedBy (creates extra table)
@OneToMany
private List<Item> items;  // BAD

// ✅ DO: Use bidirectional with mappedBy
@OneToMany(mappedBy = "order")
private List<Item> items;  // GOOD

// ❌ AVOID: Lazy loading outside transaction
public void problematicMethod() {
    Employee emp = employeeRepository.findById(1L).get();
    // Later, outside transaction:
    emp.getDepartment().getName();  // LazyInitializationException
}

// ✅ DO: Fetch within transaction or use JOIN FETCH
@Transactional(readOnly = true)
public void correctMethod() {
    Employee emp = employeeRepository.findByIdWithDepartment(1L);
    emp.getDepartment().getName();  // Works fine
}

// ❌ AVOID: Modifying @Version field manually
employee.setVersion(5);  // BAD - Let Hibernate manage this

// ❌ AVOID: Using toString() on entities with collections
@Entity
@ToString  // BAD - can cause LazyInitializationException
public class Employee {
    @OneToMany
    private List<Project> projects;
}
```

### 7. Performance Tips Summary

1. **Enable SQL logging during development**
2. **Use appropriate fetch strategies (prefer LAZY)**
3. **Avoid N+1 queries with JOIN FETCH or @EntityGraph**
4. **Use batch processing for bulk operations**
5. **Configure second-level cache for read-heavy entities**
6. **Use pagination for large result sets**
7. **Use DTOs/projections when you don't need full entities**
8. **Keep transactions short and focused**
9. **Monitor with Hibernate statistics**
10. **Use connection pooling (HikariCP)**

---
