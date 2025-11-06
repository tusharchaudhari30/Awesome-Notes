# Spring Data JPA - Complete Interview Notes

## From Basics to Expert

---

## Table of Contents

1. [Spring Data JPA Basics](#1-spring-data-jpa-basics)
2. [Entity Mapping and Annotations](#2-entity-mapping-and-annotations)
3. [Repository Interfaces](#3-repository-interfaces)
4. [Query Methods](#4-query-methods)
5. [Custom Queries with @Query](#5-custom-queries-with-query)
6. [Native Queries](#6-native-queries)
7. [Entity Relationships](#7-entity-relationships)
8. [Pagination and Sorting](#8-pagination-and-sorting)
9. [Specifications and Criteria API](#9-specifications-and-criteria-api)
10. [Projections (DTO)](#10-projections-dto)
11. [Transaction Management](#11-transaction-management)
12. [Locking Mechanisms](#12-locking-mechanisms)
13. [Auditing](#13-auditing)
14. [Caching](#14-caching)
15. [Performance Optimization](#15-performance-optimization)
16. [Advanced Topics](#16-advanced-topics)

---

## 1. Spring Data JPA Basics

### What is Spring Data JPA?

Spring Data JPA is part of the Spring Data family that simplifies database operations by providing a repository abstraction layer for CRUD operations. It builds on top of JPA (Java Persistence API) and reduces boilerplate code.

**Key Features:**

- Less boilerplate code
- Easy repository creation by writing interfaces
- Automatic query generation from method names
- Seamless Spring integration
- Built-in pagination and sorting support

### Maven Dependencies

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>

<dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
    <scope>runtime</scope>
</dependency>
```

### Application Properties Configuration

```properties
# MySQL Configuration
spring.datasource.url=jdbc:mysql://localhost:3306/empdb
spring.datasource.username=root
spring.datasource.password=root
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# JPA Configuration
spring.jpa.database-platform=org.hibernate.dialect.MySQL8Dialect
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true

# Batch Processing
spring.jpa.properties.hibernate.jdbc.batch_size=25
spring.jpa.properties.hibernate.order_inserts=true
spring.jpa.properties.hibernate.order_updates=true
```

---

## 2. Entity Mapping and Annotations

### Basic Entity Class

```java
import jakarta.persistence.*;
import java.time.LocalDate;

@Entity
@Table(name = "employees")
public class Employee {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "first_name", nullable = false, length = 50)
    private String firstName;

    @Column(name = "last_name", nullable = false, length = 50)
    private String lastName;

    @Column(unique = true, nullable = false)
    private String email;

    @Column(name = "hire_date")
    private LocalDate hireDate;

    @Column(precision = 10, scale = 2)
    private Double salary;

    // Constructors
    public Employee() {}

    public Employee(String firstName, String lastName, String email) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public LocalDate getHireDate() {
        return hireDate;
    }

    public void setHireDate(LocalDate hireDate) {
        this.hireDate = hireDate;
    }

    public Double getSalary() {
        return salary;
    }

    public void setSalary(Double salary) {
        this.salary = salary;
    }
}
```

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

### Embedded and Embeddable

```java
@Embeddable
public class Address {
    private String street;
    private String city;
    private String state;
    private String zipCode;

    // Constructors, Getters, Setters
}

@Entity
public class Employee {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    @Embedded
    private Address address;

    // Other fields, constructors, getters, setters
}
```

---

## 3. Repository Interfaces

### Repository Hierarchy

Spring Data JPA provides several repository interfaces:

1. **Repository<T, ID>** - Marker interface
2. **CrudRepository<T, ID>** - CRUD operations
3. **PagingAndSortingRepository<T, ID>** - Pagination and sorting
4. **JpaRepository<T, ID>** - JPA-specific operations (most commonly used)

### Basic Repository

```java
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {
    // Custom query methods can be defined here
}
```

### Built-in Methods (JpaRepository)

```java
// Save operations
Employee save(Employee entity);
List<Employee> saveAll(Iterable<Employee> entities);

// Find operations
Optional<Employee> findById(Long id);
List<Employee> findAll();
List<Employee> findAllById(Iterable<Long> ids);
boolean existsById(Long id);
long count();

// Delete operations
void deleteById(Long id);
void delete(Employee entity);
void deleteAll();
void deleteAll(Iterable<Employee> entities);

// Flush operations
void flush();
Employee saveAndFlush(Employee entity);
void deleteInBatch(Iterable<Employee> entities);
void deleteAllInBatch();
```

### Service Layer Example

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;

@Service
public class EmployeeService {

    @Autowired
    private EmployeeRepository employeeRepository;

    // Create
    public Employee createEmployee(Employee employee) {
        return employeeRepository.save(employee);
    }

    // Read
    public List<Employee> getAllEmployees() {
        return employeeRepository.findAll();
    }

    public Optional<Employee> getEmployeeById(Long id) {
        return employeeRepository.findById(id);
    }

    // Update
    public Employee updateEmployee(Long id, Employee employeeDetails) {
        Employee employee = employeeRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Employee not found"));

        employee.setFirstName(employeeDetails.getFirstName());
        employee.setLastName(employeeDetails.getLastName());
        employee.setEmail(employeeDetails.getEmail());
        employee.setSalary(employeeDetails.getSalary());

        return employeeRepository.save(employee);
    }

    // Delete
    public void deleteEmployee(Long id) {
        employeeRepository.deleteById(id);
    }

    public long countEmployees() {
        return employeeRepository.count();
    }
}
```

---

## 4. Query Methods

Spring Data JPA can automatically generate queries from method names.

### Supported Keywords

| Keyword        | Example                               | JPQL Snippet                                        |
| -------------- | ------------------------------------- | --------------------------------------------------- |
| `findBy`       | `findByFirstName(String firstName)`   | `where x.firstName = ?1`                            |
| `And`          | `findByFirstNameAndLastName`          | `where x.firstName = ?1 and x.lastName = ?2`        |
| `Or`           | `findByFirstNameOrLastName`           | `where x.firstName = ?1 or x.lastName = ?2`         |
| `Between`      | `findBySalaryBetween`                 | `where x.salary between ?1 and ?2`                  |
| `LessThan`     | `findBySalaryLessThan`                | `where x.salary < ?1`                               |
| `GreaterThan`  | `findBySalaryGreaterThan`             | `where x.salary > ?1`                               |
| `Like`         | `findByFirstNameLike`                 | `where x.firstName like ?1`                         |
| `StartingWith` | `findByFirstNameStartingWith`         | `where x.firstName like ?1` (param bound with %)    |
| `EndingWith`   | `findByFirstNameEndingWith`           | `where x.firstName like ?1` (param bound with %)    |
| `Containing`   | `findByFirstNameContaining`           | `where x.firstName like ?1` (param bound with %?1%) |
| `OrderBy`      | `findByLastNameOrderBySalaryDesc`     | `where x.lastName = ?1 order by x.salary desc`      |
| `Not`          | `findByFirstNameNot`                  | `where x.firstName <> ?1`                           |
| `In`           | `findByIdIn(Collection<Long> ids)`    | `where x.id in ?1`                                  |
| `NotIn`        | `findByIdNotIn(Collection<Long> ids)` | `where x.id not in ?1`                              |
| `True`         | `findByActiveTrue()`                  | `where x.active = true`                             |
| `False`        | `findByActiveFalse()`                 | `where x.active = false`                            |
| `IsNull`       | `findByEmailIsNull()`                 | `where x.email is null`                             |
| `IsNotNull`    | `findByEmailIsNotNull()`              | `where x.email is not null`                         |

### Query Method Examples

```java
@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    // Find by single field
    List<Employee> findByFirstName(String firstName);

    // Find by multiple fields (AND)
    List<Employee> findByFirstNameAndLastName(String firstName, String lastName);

    // Find by multiple fields (OR)
    List<Employee> findByFirstNameOrLastName(String firstName, String lastName);

    // Comparison operators
    List<Employee> findBySalaryGreaterThan(Double salary);
    List<Employee> findBySalaryLessThanEqual(Double salary);
    List<Employee> findBySalaryBetween(Double minSalary, Double maxSalary);

    // Like queries
    List<Employee> findByFirstNameLike(String pattern);
    List<Employee> findByFirstNameStartingWith(String prefix);
    List<Employee> findByFirstNameEndingWith(String suffix);
    List<Employee> findByFirstNameContaining(String infix);

    // Ordering
    List<Employee> findByLastNameOrderBySalaryDesc(String lastName);
    List<Employee> findByDepartmentOrderByHireDateAsc(String department);

    // In queries
    List<Employee> findByIdIn(List<Long> ids);
    List<Employee> findByFirstNameIn(List<String> names);

    // Null checks
    List<Employee> findByEmailIsNull();
    List<Employee> findByEmailIsNotNull();

    // Boolean checks
    List<Employee> findByActiveTrue();
    List<Employee> findByActiveFalse();

    // Count queries
    long countByLastName(String lastName);

    // Exists queries
    boolean existsByEmail(String email);

    // Delete queries
    void deleteByLastName(String lastName);

    // Distinct
    List<Employee> findDistinctByLastName(String lastName);

    // Top/First
    List<Employee> findTop3ByOrderBySalaryDesc();
    Employee findFirstByOrderByHireDateAsc();

    // Ignoring case
    List<Employee> findByFirstNameIgnoreCase(String firstName);
}
```

---

## 5. Custom Queries with @Query

### JPQL Queries

JPQL (Java Persistence Query Language) operates on entity objects, not database tables.

```java
@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    // Simple JPQL query
    @Query("SELECT e FROM Employee e WHERE e.firstName = :firstName")
    List<Employee> findByFirstNameJPQL(@Param("firstName") String firstName);

    // Multiple parameters
    @Query("SELECT e FROM Employee e WHERE e.firstName = :firstName AND e.lastName = :lastName")
    List<Employee> findByFullName(@Param("firstName") String firstName,
                                  @Param("lastName") String lastName);

    // Like query
    @Query("SELECT e FROM Employee e WHERE e.firstName LIKE %:keyword%")
    List<Employee> searchByFirstName(@Param("keyword") String keyword);

    // Ordering
    @Query("SELECT e FROM Employee e ORDER BY e.salary DESC")
    List<Employee> findAllOrderedBySalary();

    // Aggregate functions
    @Query("SELECT AVG(e.salary) FROM Employee e")
    Double findAverageSalary();

    @Query("SELECT MAX(e.salary) FROM Employee e")
    Double findMaxSalary();

    @Query("SELECT COUNT(e) FROM Employee e WHERE e.department = :dept")
    long countByDepartment(@Param("dept") String department);

    // Group by
    @Query("SELECT e.department, COUNT(e) FROM Employee e GROUP BY e.department")
    List<Object[]> countEmployeesByDepartment();

    // Join query
    @Query("SELECT e FROM Employee e JOIN e.department d WHERE d.name = :deptName")
    List<Employee> findByDepartmentName(@Param("deptName") String deptName);

    // Custom DTO projection
    @Query("SELECT new com.example.dto.EmployeeDTO(e.id, e.firstName, e.lastName) " +
           "FROM Employee e WHERE e.salary > :minSalary")
    List<EmployeeDTO> findHighEarners(@Param("minSalary") Double minSalary);
}
```

### @Modifying Queries

For UPDATE, DELETE, and INSERT operations.

```java
@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    // Update query
    @Modifying
    @Transactional
    @Query("UPDATE Employee e SET e.salary = :salary WHERE e.id = :id")
    int updateEmployeeSalary(@Param("id") Long id, @Param("salary") Double salary);

    // Bulk update
    @Modifying
    @Transactional
    @Query("UPDATE Employee e SET e.salary = e.salary * 1.1 WHERE e.department = :dept")
    int increaseSalaryByDepartment(@Param("dept") String department);

    // Delete query
    @Modifying
    @Transactional
    @Query("DELETE FROM Employee e WHERE e.hireDate < :date")
    int deleteEmployeesHiredBefore(@Param("date") LocalDate date);

    // Update with multiple conditions
    @Modifying
    @Transactional
    @Query("UPDATE Employee e SET e.active = false WHERE e.salary < :minSalary")
    int deactivateLowSalaryEmployees(@Param("minSalary") Double minSalary);
}
```

**Important Notes:**

- `@Modifying` annotation is required for UPDATE/DELETE queries
- Methods should be annotated with `@Transactional`
- Return type can be `int` or `void` (number of rows affected)
- After modifying operations, you may need to clear the persistence context

---

## 6. Native Queries

Native SQL queries operate directly on database tables.

```java
@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    // Simple native query
    @Query(value = "SELECT * FROM employees WHERE first_name = :firstName",
           nativeQuery = true)
    List<Employee> findByFirstNameNative(@Param("firstName") String firstName);

    // Native query with multiple conditions
    @Query(value = "SELECT * FROM employees WHERE salary BETWEEN :minSalary AND :maxSalary",
           nativeQuery = true)
    List<Employee> findBySalaryRangeNative(@Param("minSalary") Double minSalary,
                                           @Param("maxSalary") Double maxSalary);

    // Native query with JOIN
    @Query(value = "SELECT e.* FROM employees e " +
                   "INNER JOIN departments d ON e.department_id = d.id " +
                   "WHERE d.name = :deptName",
           nativeQuery = true)
    List<Employee> findByDepartmentNameNative(@Param("deptName") String deptName);

    // Native query with aggregation
    @Query(value = "SELECT AVG(salary) FROM employees WHERE department_id = :deptId",
           nativeQuery = true)
    Double findAverageSalaryByDepartmentNative(@Param("deptId") Long deptId);

    // Native modifying query
    @Modifying
    @Transactional
    @Query(value = "UPDATE employees SET salary = :salary WHERE id = :id",
           nativeQuery = true)
    int updateSalaryNative(@Param("id") Long id, @Param("salary") Double salary);

    // Native delete query
    @Modifying
    @Transactional
    @Query(value = "DELETE FROM employees WHERE active = false",
           nativeQuery = true)
    int deleteInactiveEmployeesNative();

    // Database-specific features
    @Query(value = "SELECT * FROM employees ORDER BY RAND() LIMIT :limit",
           nativeQuery = true)
    List<Employee> findRandomEmployees(@Param("limit") int limit);
}
```

---

## 7. Entity Relationships

### @OneToOne Relationship

```java
// Bidirectional One-to-One
@Entity
public class Employee {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    @OneToOne(cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JoinColumn(name = "address_id", referencedColumnName = "id")
    private Address address;

    // Getters and Setters
}

@Entity
public class Address {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String street;
    private String city;

    @OneToOne(mappedBy = "address")
    private Employee employee;

    // Getters and Setters
}
```

### @OneToMany and @ManyToOne Relationship

```java
// One Department has Many Employees
@Entity
public class Department {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    @OneToMany(mappedBy = "department", cascade = CascadeType.ALL,
               orphanRemoval = true, fetch = FetchType.LAZY)
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

    // Getters and Setters
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

    // Getters and Setters
}
```

### @ManyToMany Relationship

```java
// Many Students can enroll in Many Courses
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

    // Getters and Setters
}

@Entity
public class Course {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;

    @ManyToMany(mappedBy = "courses")
    private Set<Student> students = new HashSet<>();

    // Getters and Setters
}
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

### Fetch Types

```java
// LAZY (default for @OneToMany and @ManyToMany)
@OneToMany(fetch = FetchType.LAZY)
private List<Employee> employees;

// EAGER (default for @ManyToOne and @OneToOne)
@ManyToOne(fetch = FetchType.EAGER)
private Department department;
```

**Best Practice:** Use LAZY loading by default and fetch eagerly only when necessary.

### orphanRemoval

```java
@OneToMany(mappedBy = "parent", orphanRemoval = true)
private List<Child> children;
```

**Difference between `orphanRemoval` and `CascadeType.REMOVE`:**

- `orphanRemoval = true`: Removes child when it's no longer referenced by parent
- `CascadeType.REMOVE`: Removes all children when parent is deleted

---

## 8. Pagination and Sorting

### Pageable Interface

```java
@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    // Pagination and Sorting are built-in with JpaRepository
    // Page<Employee> findAll(Pageable pageable);
}
```

### Service Layer with Pagination

```java
@Service
public class EmployeeService {

    @Autowired
    private EmployeeRepository employeeRepository;

    // Simple pagination
    public Page<Employee> getEmployees(int page, int size) {
        Pageable pageable = PageRequest.of(page, size);
        return employeeRepository.findAll(pageable);
    }

    // Pagination with sorting
    public Page<Employee> getEmployeesSorted(int page, int size, String sortBy, String direction) {
        Sort sort = direction.equalsIgnoreCase("asc")
                    ? Sort.by(sortBy).ascending()
                    : Sort.by(sortBy).descending();

        Pageable pageable = PageRequest.of(page, size, sort);
        return employeeRepository.findAll(pageable);
    }

    // Multiple field sorting
    public Page<Employee> getEmployeesMultiSort(int page, int size) {
        Sort sort = Sort.by("department").ascending()
                       .and(Sort.by("salary").descending());

        Pageable pageable = PageRequest.of(page, size, sort);
        return employeeRepository.findAll(pageable);
    }
}
```

### Controller Example

```java
@RestController
@RequestMapping("/api/employees")
public class EmployeeController {

    @Autowired
    private EmployeeService employeeService;

    @GetMapping
    public ResponseEntity<Page<Employee>> getAllEmployees(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction) {

        Page<Employee> employees = employeeService.getEmployeesSorted(page, size, sortBy, direction);
        return ResponseEntity.ok(employees);
    }
}
```

### Custom Query Methods with Pagination

```java
@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    // Query method with pagination
    Page<Employee> findByDepartment(String department, Pageable pageable);

    // Query method with sorting
    List<Employee> findByLastName(String lastName, Sort sort);

    // Custom JPQL query with pagination
    @Query("SELECT e FROM Employee e WHERE e.salary > :minSalary")
    Page<Employee> findHighEarners(@Param("minSalary") Double minSalary, Pageable pageable);
}
```

### Page Object Methods

```java
Page<Employee> page = employeeRepository.findAll(pageable);

// Get content
List<Employee> employees = page.getContent();

// Get pagination info
int totalPages = page.getTotalPages();
long totalElements = page.getTotalElements();
int currentPage = page.getNumber();
int pageSize = page.getSize();
boolean hasNext = page.hasNext();
boolean hasPrevious = page.hasPrevious();
boolean isFirst = page.isFirst();
boolean isLast = page.isLast();
```

---

## 9. Specifications and Criteria API

Dynamic query building using JPA Criteria API.

### Enable Specifications

```java
@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long>,
                                           JpaSpecificationExecutor<Employee> {
}
```

### Creating Specifications

```java
import org.springframework.data.jpa.domain.Specification;
import jakarta.persistence.criteria.Predicate;

public class EmployeeSpecifications {

    // Specification for firstName
    public static Specification<Employee> hasFirstName(String firstName) {
        return (root, query, criteriaBuilder) ->
            firstName == null ? null : criteriaBuilder.equal(root.get("firstName"), firstName);
    }

    // Specification for lastName
    public static Specification<Employee> hasLastName(String lastName) {
        return (root, query, criteriaBuilder) ->
            lastName == null ? null : criteriaBuilder.equal(root.get("lastName"), lastName);
    }

    // Specification for salary range
    public static Specification<Employee> hasSalaryBetween(Double minSalary, Double maxSalary) {
        return (root, query, criteriaBuilder) -> {
            if (minSalary == null && maxSalary == null) return null;
            if (minSalary == null) return criteriaBuilder.lessThanOrEqualTo(root.get("salary"), maxSalary);
            if (maxSalary == null) return criteriaBuilder.greaterThanOrEqualTo(root.get("salary"), minSalary);
            return criteriaBuilder.between(root.get("salary"), minSalary, maxSalary);
        };
    }

    // Specification for department
    public static Specification<Employee> hasDepartment(String department) {
        return (root, query, criteriaBuilder) ->
            department == null ? null : criteriaBuilder.equal(root.get("department"), department);
    }

    // Specification for name like
    public static Specification<Employee> hasNameLike(String name) {
        return (root, query, criteriaBuilder) ->
            name == null ? null : criteriaBuilder.like(
                criteriaBuilder.lower(root.get("firstName")),
                "%" + name.toLowerCase() + "%");
    }

    // Specification for hire date after
    public static Specification<Employee> hiredAfter(LocalDate date) {
        return (root, query, criteriaBuilder) ->
            date == null ? null : criteriaBuilder.greaterThanOrEqualTo(root.get("hireDate"), date);
    }
}
```

### Using Specifications

```java
@Service
public class EmployeeService {

    @Autowired
    private EmployeeRepository employeeRepository;

    // Combining specifications with AND
    public List<Employee> searchEmployees(String firstName, String lastName,
                                         Double minSalary, Double maxSalary) {
        Specification<Employee> spec = Specification.where(
            EmployeeSpecifications.hasFirstName(firstName))
            .and(EmployeeSpecifications.hasLastName(lastName))
            .and(EmployeeSpecifications.hasSalaryBetween(minSalary, maxSalary));

        return employeeRepository.findAll(spec);
    }

    // Combining specifications with OR
    public List<Employee> searchEmployeesOr(String firstName, String lastName) {
        Specification<Employee> spec = Specification.where(
            EmployeeSpecifications.hasFirstName(firstName))
            .or(EmployeeSpecifications.hasLastName(lastName));

        return employeeRepository.findAll(spec);
    }

    // With pagination and sorting
    public Page<Employee> searchEmployeesWithPaging(String department,
                                                    Double minSalary,
                                                    Pageable pageable) {
        Specification<Employee> spec = Specification.where(
            EmployeeSpecifications.hasDepartment(department))
            .and(EmployeeSpecifications.hasSalaryBetween(minSalary, null));

        return employeeRepository.findAll(spec, pageable);
    }
}
```

### Complex Specification Example

```java
public static Specification<Employee> searchEmployees(EmployeeSearchCriteria criteria) {
    return (root, query, criteriaBuilder) -> {
        List<Predicate> predicates = new ArrayList<>();

        if (criteria.getFirstName() != null) {
            predicates.add(criteriaBuilder.like(
                criteriaBuilder.lower(root.get("firstName")),
                "%" + criteria.getFirstName().toLowerCase() + "%"));
        }

        if (criteria.getLastName() != null) {
            predicates.add(criteriaBuilder.like(
                criteriaBuilder.lower(root.get("lastName")),
                "%" + criteria.getLastName().toLowerCase() + "%"));
        }

        if (criteria.getMinSalary() != null) {
            predicates.add(criteriaBuilder.greaterThanOrEqualTo(
                root.get("salary"), criteria.getMinSalary()));
        }

        if (criteria.getMaxSalary() != null) {
            predicates.add(criteriaBuilder.lessThanOrEqualTo(
                root.get("salary"), criteria.getMaxSalary()));
        }

        if (criteria.getDepartments() != null && !criteria.getDepartments().isEmpty()) {
            predicates.add(root.get("department").in(criteria.getDepartments()));
        }

        return criteriaBuilder.and(predicates.toArray(new Predicate[0]));
    };
}
```

---

## 10. Projections (DTO)

Projections allow you to retrieve only specific fields instead of entire entities.

### Interface-Based Projections

```java
// Define projection interface
public interface EmployeeSummary {
    String getFirstName();
    String getLastName();
    Double getSalary();
}

@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    // Returns only firstName, lastName, and salary
    List<EmployeeSummary> findAllProjectedBy();

    EmployeeSummary findProjectedById(Long id);

    @Query("SELECT e.firstName as firstName, e.lastName as lastName, e.salary as salary " +
           "FROM Employee e WHERE e.department = :dept")
    List<EmployeeSummary> findByDepartmentProjected(@Param("dept") String department);
}
```

### Class-Based Projections (DTO)

```java
// DTO class
public class EmployeeDTO {
    private Long id;
    private String firstName;
    private String lastName;
    private Double salary;

    // Constructor for JPQL constructor expression
    public EmployeeDTO(Long id, String firstName, String lastName, Double salary) {
        this.id = id;
        this.firstName = firstName;
        this.lastName = lastName;
        this.salary = salary;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public Double getSalary() {
        return salary;
    }

    public void setSalary(Double salary) {
        this.salary = salary;
    }
}

@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    // Using constructor expression in JPQL
    @Query("SELECT new com.example.dto.EmployeeDTO(e.id, e.firstName, e.lastName, e.salary) " +
           "FROM Employee e WHERE e.department = :dept")
    List<EmployeeDTO> findEmployeeDTOByDepartment(@Param("dept") String department);

    @Query("SELECT new com.example.dto.EmployeeDTO(e.id, e.firstName, e.lastName, e.salary) " +
           "FROM Employee e")
    List<EmployeeDTO> findAllEmployeeDTO();
}
```

### Dynamic Projections

```java
@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    <T> List<T> findByDepartment(String department, Class<T> type);
}

// Usage
List<EmployeeSummary> summaries = repository.findByDepartment("IT", EmployeeSummary.class);
List<Employee> entities = repository.findByDepartment("IT", Employee.class);
```

---

## 11. Transaction Management

### @Transactional Annotation

```java
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Isolation;

@Service
public class EmployeeService {

    @Autowired
    private EmployeeRepository employeeRepository;

    @Autowired
    private DepartmentRepository departmentRepository;

    // Basic transactional method
    @Transactional
    public Employee createEmployee(Employee employee) {
        return employeeRepository.save(employee);
    }

    // Read-only transaction (optimization)
    @Transactional(readOnly = true)
    public List<Employee> getAllEmployees() {
        return employeeRepository.findAll();
    }

    // Transaction with timeout
    @Transactional(timeout = 30)
    public void updateEmployees() {
        // Long-running operation
    }

    // Transaction with custom rollback rules
    @Transactional(rollbackFor = Exception.class)
    public void updateEmployeeSafely(Employee employee) {
        employeeRepository.save(employee);
    }

    // No rollback for specific exceptions
    @Transactional(noRollbackFor = ResourceNotFoundException.class)
    public void updateEmployeeNoRollback(Employee employee) {
        employeeRepository.save(employee);
    }

    // Complex transaction involving multiple operations
    @Transactional
    public void transferEmployee(Long employeeId, Long newDeptId) {
        Employee employee = employeeRepository.findById(employeeId)
            .orElseThrow(() -> new ResourceNotFoundException("Employee not found"));

        Department newDept = departmentRepository.findById(newDeptId)
            .orElseThrow(() -> new ResourceNotFoundException("Department not found"));

        employee.setDepartment(newDept);
        employeeRepository.save(employee);
    }
}
```

### Propagation Types

```java
// REQUIRED (default) - Use existing transaction or create new
@Transactional(propagation = Propagation.REQUIRED)
public void method1() { }

// REQUIRES_NEW - Always create a new transaction
@Transactional(propagation = Propagation.REQUIRES_NEW)
public void method2() { }

// MANDATORY - Must have existing transaction
@Transactional(propagation = Propagation.MANDATORY)
public void method3() { }

// NESTED - Execute within nested transaction if exists
@Transactional(propagation = Propagation.NESTED)
public void method4() { }

// SUPPORTS - Execute with transaction if exists, without if not
@Transactional(propagation = Propagation.SUPPORTS)
public void method5() { }

// NOT_SUPPORTED - Execute without transaction
@Transactional(propagation = Propagation.NOT_SUPPORTED)
public void method6() { }

// NEVER - Throw exception if transaction exists
@Transactional(propagation = Propagation.NEVER)
public void method7() { }
```

### Isolation Levels

```java
// DEFAULT - Use database default isolation level
@Transactional(isolation = Isolation.DEFAULT)

// READ_UNCOMMITTED - Allows dirty reads
@Transactional(isolation = Isolation.READ_UNCOMMITTED)

// READ_COMMITTED - Prevents dirty reads
@Transactional(isolation = Isolation.READ_COMMITTED)

// REPEATABLE_READ - Prevents dirty and non-repeatable reads
@Transactional(isolation = Isolation.REPEATABLE_READ)

// SERIALIZABLE - Highest isolation level
@Transactional(isolation = Isolation.SERIALIZABLE)
```

---

## 12. Locking Mechanisms

### Optimistic Locking

Uses version field to detect concurrent modifications.

```java
@Entity
public class Employee {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private Double salary;

    @Version
    private Long version;

    // Getters and Setters
}

@Service
public class EmployeeService {

    @Autowired
    private EmployeeRepository employeeRepository;

    @Transactional
    public void updateEmployeeSalary(Long id, Double newSalary) {
        try {
            Employee employee = employeeRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Employee not found"));

            employee.setSalary(newSalary);
            employeeRepository.save(employee);
        } catch (OptimisticLockException e) {
            // Handle concurrent modification
            throw new ConcurrentModificationException("Employee was modified by another transaction");
        }
    }
}
```

### Pessimistic Locking

Locks the database row to prevent concurrent modifications.

```java
@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    // Pessimistic Write Lock - Prevents reads and writes
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT e FROM Employee e WHERE e.id = :id")
    Optional<Employee> findByIdWithWriteLock(@Param("id") Long id);

    // Pessimistic Read Lock - Prevents writes, allows reads
    @Lock(LockModeType.PESSIMISTIC_READ)
    @Query("SELECT e FROM Employee e WHERE e.id = :id")
    Optional<Employee> findByIdWithReadLock(@Param("id") Long id);

    // Force increment - Increments version even if no changes
    @Lock(LockModeType.PESSIMISTIC_FORCE_INCREMENT)
    Optional<Employee> findById(Long id);
}

@Service
public class EmployeeService {

    @Autowired
    private EmployeeRepository employeeRepository;

    @Transactional
    public void updateEmployeeWithLock(Long id, String newName, Double newSalary) {
        // Acquire lock
        Employee employee = employeeRepository.findByIdWithWriteLock(id)
            .orElseThrow(() -> new ResourceNotFoundException("Employee not found"));

        // Modify employee
        employee.setName(newName);
        employee.setSalary(newSalary);

        // Save - lock is released after transaction commits
        employeeRepository.save(employee);
    }
}
```

### Lock Modes Summary

| Lock Mode                     | Description                                |
| ----------------------------- | ------------------------------------------ |
| `OPTIMISTIC`                  | Optimistic lock using version field        |
| `OPTIMISTIC_FORCE_INCREMENT`  | Force version increment                    |
| `PESSIMISTIC_READ`            | Shared lock - prevents writes              |
| `PESSIMISTIC_WRITE`           | Exclusive lock - prevents reads and writes |
| `PESSIMISTIC_FORCE_INCREMENT` | Pessimistic lock with version increment    |

---

## 13. Auditing

Track who created/modified entities and when.

### Enable JPA Auditing

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@Configuration
@EnableJpaAuditing
public class JpaConfig {
}
```

### Auditable Base Entity

```java
import org.springframework.data.annotation.CreatedBy;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedBy;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;
import jakarta.persistence.*;
import java.time.LocalDateTime;

@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class Auditable {

    @CreatedBy
    @Column(name = "created_by", updatable = false)
    private String createdBy;

    @CreatedDate
    @Column(name = "created_date", updatable = false)
    private LocalDateTime createdDate;

    @LastModifiedBy
    @Column(name = "last_modified_by")
    private String lastModifiedBy;

    @LastModifiedDate
    @Column(name = "last_modified_date")
    private LocalDateTime lastModifiedDate;

    // Getters and Setters
    public String getCreatedBy() {
        return createdBy;
    }

    public void setCreatedBy(String createdBy) {
        this.createdBy = createdBy;
    }

    public LocalDateTime getCreatedDate() {
        return createdDate;
    }

    public void setCreatedDate(LocalDateTime createdDate) {
        this.createdDate = createdDate;
    }

    public String getLastModifiedBy() {
        return lastModifiedBy;
    }

    public void setLastModifiedBy(String lastModifiedBy) {
        this.lastModifiedBy = lastModifiedBy;
    }

    public LocalDateTime getLastModifiedDate() {
        return lastModifiedDate;
    }

    public void setLastModifiedDate(LocalDateTime lastModifiedDate) {
        this.lastModifiedDate = lastModifiedDate;
    }
}
```

### Entity Using Auditing

```java
@Entity
public class Employee extends Auditable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String firstName;
    private String lastName;
    private Double salary;

    // Getters and Setters
}
```

### AuditorAware Implementation (for CreatedBy/LastModifiedBy)

```java
import org.springframework.data.domain.AuditorAware;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import java.util.Optional;

@Component
public class AuditorAwareImpl implements AuditorAware<String> {

    @Override
    public Optional<String> getCurrentAuditor() {
        // Get current user from Spring Security context
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();

        if (authentication == null || !authentication.isAuthenticated()) {
            return Optional.of("system");
        }

        return Optional.of(authentication.getName());
    }
}
```

---

## 14. Caching

### Enable Caching

```java
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableCaching
public class CacheConfig {
}
```

### Using Cache Annotations

```java
import org.springframework.cache.annotation.Cacheable;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.CachePut;
import org.springframework.cache.annotation.Caching;

@Service
public class EmployeeService {

    @Autowired
    private EmployeeRepository employeeRepository;

    // Cache the result
    @Cacheable(value = "employees", key = "#id")
    public Employee getEmployeeById(Long id) {
        System.out.println("Fetching from database...");
        return employeeRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Employee not found"));
    }

    // Cache all employees
    @Cacheable(value = "employees")
    public List<Employee> getAllEmployees() {
        System.out.println("Fetching all from database...");
        return employeeRepository.findAll();
    }

    // Update cache
    @CachePut(value = "employees", key = "#employee.id")
    public Employee updateEmployee(Employee employee) {
        return employeeRepository.save(employee);
    }

    // Evict specific cache entry
    @CacheEvict(value = "employees", key = "#id")
    public void deleteEmployee(Long id) {
        employeeRepository.deleteById(id);
    }

    // Evict all cache entries
    @CacheEvict(value = "employees", allEntries = true)
    public void deleteAllEmployees() {
        employeeRepository.deleteAll();
    }

    // Conditional caching
    @Cacheable(value = "employees", key = "#lastName",
               condition = "#lastName.length() > 3")
    public List<Employee> findByLastName(String lastName) {
        return employeeRepository.findByLastName(lastName);
    }

    // Multiple cache operations
    @Caching(
        cacheable = {
            @Cacheable(value = "employees", key = "#id")
        },
        evict = {
            @CacheEvict(value = "employeeList", allEntries = true)
        }
    )
    public Employee getAndEvictList(Long id) {
        return employeeRepository.findById(id).orElse(null);
    }
}
```

### Entity-Level Caching

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

    private String name;
    private Double salary;

    // Getters and Setters
}
```

---

## 15. Performance Optimization

### N+1 Query Problem and Solutions

#### Problem Example

```java
// This causes N+1 queries
List<Employee> employees = employeeRepository.findAll();
for (Employee emp : employees) {
    // Each department access triggers a new query
    System.out.println(emp.getDepartment().getName());
}
```

#### Solution 1: JOIN FETCH

```java
@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    @Query("SELECT e FROM Employee e JOIN FETCH e.department")
    List<Employee> findAllWithDepartment();
}
```

#### Solution 2: @EntityGraph

```java
@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    @EntityGraph(attributePaths = {"department"})
    List<Employee> findAll();

    @EntityGraph(attributePaths = {"department", "address"})
    Optional<Employee> findById(Long id);
}
```

#### Solution 3: @NamedEntityGraph

```java
@Entity
@NamedEntityGraph(
    name = "Employee.withDepartment",
    attributeNodes = @NamedAttributeNode("department")
)
public class Employee {
    // Entity fields
}

@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    @EntityGraph(value = "Employee.withDepartment", type = EntityGraphType.LOAD)
    List<Employee> findAll();
}
```

### Batch Processing

```java
@Service
public class EmployeeBatchService {

    @Autowired
    private EmployeeRepository employeeRepository;

    @Transactional
    public void batchInsertEmployees(List<Employee> employees) {
        int batchSize = 25;

        for (int i = 0; i < employees.size(); i++) {
            employeeRepository.save(employees.get(i));

            // Flush and clear every batchSize
            if (i > 0 && i % batchSize == 0) {
                employeeRepository.flush();
                // Clear persistence context to free memory
            }
        }
    }
}
```

### Stream Query Results

```java
@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    @QueryHints(value = @QueryHint(name = org.hibernate.annotations.QueryHints.FETCH_SIZE, value = "50"))
    Stream<Employee> findAllByDepartment(String department);
}

@Service
public class EmployeeService {

    @Autowired
    private EmployeeRepository employeeRepository;

    @Transactional(readOnly = true)
    public void processLargeDataset(String department) {
        try (Stream<Employee> stream = employeeRepository.findAllByDepartment(department)) {
            stream.forEach(employee -> {
                // Process each employee
                System.out.println(employee.getName());
            });
        }
    }
}
```

### Query Hints

```java
@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    @QueryHints(value = {
        @QueryHint(name = org.hibernate.annotations.QueryHints.COMMENT, value = "Custom query for reporting"),
        @QueryHint(name = org.hibernate.annotations.QueryHints.FETCH_SIZE, value = "50"),
        @QueryHint(name = org.hibernate.annotations.QueryHints.CACHEABLE, value = "true")
    })
    List<Employee> findByDepartment(String department);
}
```

---

## 16. Advanced Topics

### Composite Primary Keys

#### Using @IdClass

```java
// Composite Key Class
public class EmployeeProjectId implements Serializable {
    private Long employeeId;
    private Long projectId;

    public EmployeeProjectId() {}

    public EmployeeProjectId(Long employeeId, Long projectId) {
        this.employeeId = employeeId;
        this.projectId = projectId;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        EmployeeProjectId that = (EmployeeProjectId) o;
        return Objects.equals(employeeId, that.employeeId) &&
               Objects.equals(projectId, that.projectId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(employeeId, projectId);
    }

    // Getters and Setters
}

// Entity with @IdClass
@Entity
@IdClass(EmployeeProjectId.class)
public class EmployeeProject {
    @Id
    private Long employeeId;

    @Id
    private Long projectId;

    private String role;

    // Getters and Setters
}
```

#### Using @EmbeddedId

```java
// Embeddable Composite Key
@Embeddable
public class EmployeeProjectId implements Serializable {
    private Long employeeId;
    private Long projectId;

    // Constructors, equals, hashCode, getters, setters
}

// Entity with @EmbeddedId
@Entity
public class EmployeeProject {
    @EmbeddedId
    private EmployeeProjectId id;

    private String role;

    // Getters and Setters
}
```

### Custom Repository Implementation

```java
// Custom repository interface
public interface CustomEmployeeRepository {
    List<Employee> findEmployeesCustom(String criteria);
}

// Implementation
@Repository
public class CustomEmployeeRepositoryImpl implements CustomEmployeeRepository {

    @PersistenceContext
    private EntityManager entityManager;

    @Override
    public List<Employee> findEmployeesCustom(String criteria) {
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<Employee> query = cb.createQuery(Employee.class);
        Root<Employee> root = query.from(Employee.class);

        // Build custom query logic
        query.select(root).where(cb.like(root.get("name"), "%" + criteria + "%"));

        return entityManager.createQuery(query).getResultList();
    }
}

// Extend both JpaRepository and custom repository
@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long>,
                                           CustomEmployeeRepository {
}
```

### Named Queries

```java
@Entity
@NamedQuery(
    name = "Employee.findByDepartmentNamed",
    query = "SELECT e FROM Employee e WHERE e.department = :department"
)
@NamedNativeQuery(
    name = "Employee.findBySalaryRangeNative",
    query = "SELECT * FROM employees WHERE salary BETWEEN :minSalary AND :maxSalary",
    resultClass = Employee.class
)
public class Employee {
    // Entity fields
}

@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    // Reference named query
    List<Employee> findByDepartmentNamed(@Param("department") String department);

    List<Employee> findBySalaryRangeNative(@Param("minSalary") Double minSalary,
                                          @Param("maxSalary") Double maxSalary);
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

---

## Best Practices

1. **Always use `@Transactional` for write operations**
2. **Use LAZY loading by default, EAGER only when necessary**
3. **Prefer projections (DTO) for read-only queries**
4. **Use pagination for large datasets**
5. **Implement proper exception handling**
6. **Use batch processing for bulk operations**
7. **Enable second-level cache for frequently accessed data**
8. **Use @EntityGraph or JOIN FETCH to avoid N+1 queries**
9. **Use optimistic locking for better concurrency**
10. **Enable SQL logging in development, disable in production**
11. **Use specifications for dynamic queries**
12. **Implement auditing for tracking changes**
13. **Use composite keys carefully, prefer surrogate keys**
14. **Keep transactions short**
15. **Use appropriate cascade types**

---
