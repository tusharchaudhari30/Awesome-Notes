# Spring Boot Unit Testing - Complete Guide (Basics to Expert)

## Table of Contents

1. [Introduction to Testing in Spring Boot](#1-introduction)
2. [Testing Fundamentals](#2-testing-fundamentals)
3. [Testing Annotations Overview](#3-testing-annotations)
4. [Mocking with Mockito](#4-mocking-with-mockito)
5. [REST API Testing with MockMvc](#5-rest-api-testing)
6. [Database Testing](#6-database-testing)
7. [Spring Boot Test Slices](#7-test-slices)
8. [Advanced Testing Techniques](#8-advanced-techniques)
9. [Best Practices](#9-best-practices)
10. [Common Pitfalls](#10-common-pitfalls)

---

## 1. Introduction to Testing in Spring Boot {#1-introduction}

### Testing Pyramid

- **Unit Tests**: Test individual components in isolation (fastest, most numerous)
- **Integration Tests**: Test interaction between components
- **End-to-End Tests**: Test the entire application flow (slowest, least numerous)

### Key Dependencies

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```

This includes:

- **JUnit 5** (Jupiter): Testing framework
- **Mockito**: Mocking framework
- **AssertJ**: Fluent assertions
- **Hamcrest**: Matcher library
- **Spring Test & Spring Boot Test**: Testing utilities
- **JSONassert**: JSON assertion library
- **JsonPath**: XPath for JSON

---

## 2. Testing Fundamentals {#2-testing-fundamentals}

### Basic Test Structure

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {

    @Test
    void testAddition() {
        // Given (Arrange)
        Calculator calculator = new Calculator();

        // When (Act)
        int result = calculator.add(2, 3);

        // Then (Assert)
        assertEquals(5, result);
    }
}
```

### JUnit 5 Annotations

```java
import org.junit.jupiter.api.*;

class LifecycleTest {

    @BeforeAll
    static void setupAll() {
        // Runs once before all tests
        System.out.println("@BeforeAll - runs once before all test methods");
    }

    @BeforeEach
    void setUp() {
        // Runs before each test
        System.out.println("@BeforeEach - runs before each test method");
    }

    @Test
    void testOne() {
        System.out.println("Test 1");
    }

    @Test
    @DisplayName("Test with custom name")
    void testTwo() {
        System.out.println("Test 2");
    }

    @Test
    @Disabled("Temporarily disabled")
    void testThree() {
        System.out.println("Test 3 - won't run");
    }

    @AfterEach
    void tearDown() {
        // Runs after each test
        System.out.println("@AfterEach - runs after each test method");
    }

    @AfterAll
    static void tearDownAll() {
        // Runs once after all tests
        System.out.println("@AfterAll - runs once after all test methods");
    }
}
```

### Assertions

```java
import static org.junit.jupiter.api.Assertions.*;
import static org.assertj.core.api.Assertions.assertThat;

class AssertionsExampleTest {

    @Test
    void standardAssertions() {
        assertEquals(2, 1 + 1);
        assertTrue(true);
        assertFalse(false);
        assertNotNull(new Object());
        assertNull(null);

        assertThrows(IllegalArgumentException.class, () -> {
            throw new IllegalArgumentException("Invalid argument");
        });
    }

    @Test
    void assertJAssertions() {
        // AssertJ provides more readable assertions
        assertThat("Hello").isNotNull()
                          .startsWith("H")
                          .endsWith("o")
                          .contains("ell");

        assertThat(List.of(1, 2, 3))
            .hasSize(3)
            .contains(1, 2)
            .doesNotContain(4);
    }
}
```

### Parameterized Tests

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;

class ParameterizedTestExamples {

    @ParameterizedTest
    @ValueSource(strings = {"hello", "world", "test"})
    void testWithValueSource(String word) {
        assertNotNull(word);
        assertTrue(word.length() > 0);
    }

    @ParameterizedTest
    @CsvSource({
        "1, 2, 3",
        "5, 5, 10",
        "10, 20, 30"
    })
    void testAddition(int a, int b, int expected) {
        assertEquals(expected, a + b);
    }

    @ParameterizedTest
    @MethodSource("provideTestData")
    void testWithMethodSource(String input, int expected) {
        assertEquals(expected, input.length());
    }

    private static Stream<Arguments> provideTestData() {
        return Stream.of(
            Arguments.of("hello", 5),
            Arguments.of("world", 5),
            Arguments.of("test", 4)
        );
    }

    @ParameterizedTest
    @EnumSource(TimeUnit.class)
    void testWithEnumSource(TimeUnit timeUnit) {
        assertNotNull(timeUnit);
    }
}
```

---

## 3. Testing Annotations Overview {#3-testing-annotations}

### Comparison of Test Annotations

| Annotation        | Purpose                 | Context Loaded             | Use Case                       |
| ----------------- | ----------------------- | -------------------------- | ------------------------------ |
| `@SpringBootTest` | Full integration test   | Entire application context | End-to-end testing             |
| `@WebMvcTest`     | Test web layer          | Only web layer components  | Controller testing             |
| `@DataJpaTest`    | Test JPA repositories   | Only JPA components        | Repository testing             |
| `@JsonTest`       | Test JSON serialization | JSON components            | JSON mapping testing           |
| `@RestClientTest` | Test REST clients       | REST client components     | RestTemplate/WebClient testing |
| `@JdbcTest`       | Test JDBC               | JDBC components            | JdbcTemplate testing           |

### Annotation Details

```java
// Full Application Context
@SpringBootTest
class FullContextTest {
    // Loads entire Spring context
    // Slowest but most comprehensive
}

// With specific configuration
@SpringBootTest(
    webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT,
    properties = {"spring.config.location=classpath:application-test.yml"}
)
class ConfiguredContextTest {
    @LocalServerPort
    private int port;
}

// Mock environment (no server)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
@AutoConfigureMockMvc
class MockWebEnvironmentTest {
    @Autowired
    private MockMvc mockMvc;
}
```

---

## 4. Mocking with Mockito {#4-mocking-with-mockito}

### @Mock vs @MockBean

```java
// @Mock - Plain Mockito (no Spring context)
@ExtendWith(MockitoExtension.class)
class PlainMockitoTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Test
    void testWithMock() {
        // Use when testing without Spring context
        when(userRepository.findById(1L))
            .thenReturn(Optional.of(new User("John")));

        User user = userService.getUserById(1L);
        assertEquals("John", user.getName());
    }
}

// @MockBean - Spring Boot Test (with Spring context)
@SpringBootTest
class SpringMockBeanTest {

    @MockBean
    private UserRepository userRepository;

    @Autowired
    private UserService userService;

    @Test
    void testWithMockBean() {
        // Use when testing with Spring context
        // MockBean replaces the bean in the Spring context
        when(userRepository.findById(1L))
            .thenReturn(Optional.of(new User("John")));

        User user = userService.getUserById(1L);
        assertEquals("John", user.getName());
    }
}
```

### Mockito Stubbing

```java
@ExtendWith(MockitoExtension.class)
class MockitoStubbingTest {

    @Mock
    private ProductRepository productRepository;

    @InjectMocks
    private ProductService productService;

    @Test
    void basicStubbing() {
        // When-Then
        when(productRepository.findById(1L))
            .thenReturn(Optional.of(new Product("Laptop", 1000.0)));

        // Multiple return values
        when(productRepository.count())
            .thenReturn(5L, 10L, 15L);

        assertEquals(5L, productRepository.count());
        assertEquals(10L, productRepository.count());
        assertEquals(15L, productRepository.count());
    }

    @Test
    void stubbingWithMatchers() {
        // Any matcher
        when(productRepository.findById(anyLong()))
            .thenReturn(Optional.of(new Product("Laptop", 1000.0)));

        // Specific matcher
        when(productRepository.findByName(eq("Laptop")))
            .thenReturn(List.of(new Product("Laptop", 1000.0)));

        // Custom matcher
        when(productRepository.save(argThat(product ->
            product.getPrice() > 0)))
            .thenAnswer(invocation -> invocation.getArgument(0));
    }

    @Test
    void stubbingWithExceptions() {
        when(productRepository.findById(999L))
            .thenThrow(new ProductNotFoundException("Product not found"));

        assertThrows(ProductNotFoundException.class, () -> {
            productService.getProductById(999L);
        });
    }

    @Test
    void stubbingWithAnswer() {
        when(productRepository.save(any(Product.class)))
            .thenAnswer(invocation -> {
                Product product = invocation.getArgument(0);
                product.setId(100L);
                return product;
            });
    }
}
```

### BDD Style with BDDMockito

```java
import static org.mockito.BDDMockito.*;

@ExtendWith(MockitoExtension.class)
class BDDMockitoTest {

    @Mock
    private OrderRepository orderRepository;

    @InjectMocks
    private OrderService orderService;

    @Test
    void testWithBDDStyle() {
        // Given
        Order order = new Order(1L, "Product", 100.0);
        given(orderRepository.findById(1L))
            .willReturn(Optional.of(order));

        // When
        Order result = orderService.getOrderById(1L);

        // Then
        then(orderRepository).should().findById(1L);
        assertThat(result).isNotNull();
        assertThat(result.getAmount()).isEqualTo(100.0);
    }
}
```

### Verification

```java
@ExtendWith(MockitoExtension.class)
class VerificationTest {

    @Mock
    private EmailService emailService;

    @InjectMocks
    private NotificationService notificationService;

    @Test
    void basicVerification() {
        notificationService.sendWelcomeEmail("user@example.com");

        // Verify method was called
        verify(emailService).sendEmail("user@example.com", "Welcome");

        // Verify exact number of times
        verify(emailService, times(1)).sendEmail(anyString(), anyString());

        // Verify never called
        verify(emailService, never()).sendSMS(anyString());

        // Verify at least/at most
        verify(emailService, atLeastOnce()).sendEmail(anyString(), anyString());
        verify(emailService, atMost(3)).sendEmail(anyString(), anyString());
    }

    @Test
    void verificationWithOrder() {
        InOrder inOrder = inOrder(emailService);

        notificationService.sendMultipleEmails();

        inOrder.verify(emailService).sendEmail("first@example.com", "First");
        inOrder.verify(emailService).sendEmail("second@example.com", "Second");
    }

    @Test
    void verifyNoMoreInteractions() {
        notificationService.sendWelcomeEmail("user@example.com");

        verify(emailService).sendEmail("user@example.com", "Welcome");
        verifyNoMoreInteractions(emailService);
    }
}
```

### ArgumentCaptor

```java
@ExtendWith(MockitoExtension.class)
class ArgumentCaptorTest {

    @Mock
    private EmailService emailService;

    @InjectMocks
    private UserService userService;

    @Captor
    private ArgumentCaptor<String> emailCaptor;

    @Captor
    private ArgumentCaptor<User> userCaptor;

    @Test
    void captureArguments() {
        User user = new User("John", "john@example.com");
        userService.registerUser(user);

        // Capture and verify
        verify(emailService).sendEmail(emailCaptor.capture(), anyString());
        assertEquals("john@example.com", emailCaptor.getValue());
    }

    @Test
    void captureMultipleInvocations() {
        userService.registerUsers(
            new User("John", "john@example.com"),
            new User("Jane", "jane@example.com")
        );

        verify(emailService, times(2)).sendEmail(emailCaptor.capture(), anyString());

        List<String> capturedEmails = emailCaptor.getAllValues();
        assertThat(capturedEmails).containsExactly(
            "john@example.com",
            "jane@example.com"
        );
    }

    @Test
    void captureComplexObjects() {
        userService.saveUser(new User("John", "john@example.com"));

        verify(emailService).notifyAdmin(userCaptor.capture());

        User capturedUser = userCaptor.getValue();
        assertThat(capturedUser.getName()).isEqualTo("John");
        assertThat(capturedUser.getEmail()).isEqualTo("john@example.com");
    }
}
```

### @Spy and @SpyBean

```java
@ExtendWith(MockitoExtension.class)
class SpyTest {

    @Spy
    private UserService userService = new UserService();

    @Test
    void testWithSpy() {
        // Spy calls real methods unless stubbed
        doReturn("Mocked Name").when(userService).getUserName(1L);

        // This calls the real method
        String realResult = userService.getUserEmail(1L);

        // This returns the mocked value
        String mockedResult = userService.getUserName(1L);

        assertEquals("Mocked Name", mockedResult);
    }
}

@SpringBootTest
class SpyBeanTest {

    @SpyBean
    private UserService userService;

    @Test
    void testWithSpyBean() {
        // Real method is called
        String result = userService.processUser(1L);

        // But we can verify interactions
        verify(userService, times(1)).processUser(1L);
    }
}
```

---

## 5. REST API Testing with MockMvc {#5-rest-api-testing}

### Basic MockMvc Setup

```java
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Test
    void testGetUser() throws Exception {
        // Given
        User user = new User(1L, "John", "john@example.com");
        when(userService.getUserById(1L)).thenReturn(user);

        // When & Then
        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isOk())
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.name").value("John"))
            .andExpect(jsonPath("$.email").value("john@example.com"));
    }
}
```

### Testing Different HTTP Methods

```java
@WebMvcTest(ProductController.class)
class ProductControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private ProductService productService;

    @Autowired
    private ObjectMapper objectMapper;

    // GET Request
    @Test
    void testGetAllProducts() throws Exception {
        List<Product> products = List.of(
            new Product(1L, "Laptop", 1000.0),
            new Product(2L, "Mouse", 20.0)
        );

        when(productService.getAllProducts()).thenReturn(products);

        mockMvc.perform(get("/api/products"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$", hasSize(2)))
            .andExpect(jsonPath("$[0].name").value("Laptop"))
            .andExpect(jsonPath("$[1].name").value("Mouse"));
    }

    // POST Request
    @Test
    void testCreateProduct() throws Exception {
        Product product = new Product(null, "Keyboard", 50.0);
        Product savedProduct = new Product(1L, "Keyboard", 50.0);

        when(productService.createProduct(any(Product.class)))
            .thenReturn(savedProduct);

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(product)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.name").value("Keyboard"))
            .andExpect(jsonPath("$.price").value(50.0));
    }

    // PUT Request
    @Test
    void testUpdateProduct() throws Exception {
        Product updatedProduct = new Product(1L, "Updated Laptop", 1200.0);

        when(productService.updateProduct(eq(1L), any(Product.class)))
            .thenReturn(updatedProduct);

        mockMvc.perform(put("/api/products/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updatedProduct)))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("Updated Laptop"))
            .andExpect(jsonPath("$.price").value(1200.0));
    }

    // DELETE Request
    @Test
    void testDeleteProduct() throws Exception {
        doNothing().when(productService).deleteProduct(1L);

        mockMvc.perform(delete("/api/products/1"))
            .andExpect(status().isNoContent());

        verify(productService, times(1)).deleteProduct(1L);
    }

    // PATCH Request
    @Test
    void testPartialUpdateProduct() throws Exception {
        Product patchedProduct = new Product(1L, "Laptop", 900.0);

        when(productService.patchProduct(eq(1L), anyMap()))
            .thenReturn(patchedProduct);

        Map<String, Object> updates = Map.of("price", 900.0);

        mockMvc.perform(patch("/api/products/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updates)))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.price").value(900.0));
    }
}
```

### Testing Request Parameters and Headers

```java
@WebMvcTest(SearchController.class)
class SearchControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private SearchService searchService;

    @Test
    void testWithQueryParameters() throws Exception {
        mockMvc.perform(get("/api/search")
                .param("query", "laptop")
                .param("page", "0")
                .param("size", "10"))
            .andExpect(status().isOk());

        verify(searchService).search("laptop", 0, 10);
    }

    @Test
    void testWithPathVariable() throws Exception {
        when(searchService.getById(1L)).thenReturn(new Item(1L, "Item"));

        mockMvc.perform(get("/api/search/{id}", 1L))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(1));
    }

    @Test
    void testWithHeaders() throws Exception {
        mockMvc.perform(get("/api/search/1")
                .header("Authorization", "Bearer token123")
                .header("X-Request-ID", "12345"))
            .andExpect(status().isOk())
            .andExpect(header().exists("X-Response-Time"));
    }
}
```

### Testing Validation

```java
@WebMvcTest(UserController.class)
class UserValidationTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void testValidationFailure() throws Exception {
        User invalidUser = new User(null, "", "invalid-email");

        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(invalidUser)))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.errors", hasSize(greaterThan(0))));
    }

    @Test
    void testValidUser() throws Exception {
        User validUser = new User(null, "John", "john@example.com");
        User savedUser = new User(1L, "John", "john@example.com");

        when(userService.createUser(any(User.class))).thenReturn(savedUser);

        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(validUser)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(1));
    }
}
```

### Testing Exception Handling

```java
@WebMvcTest(UserController.class)
class ExceptionHandlingTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Test
    void testResourceNotFoundException() throws Exception {
        when(userService.getUserById(999L))
            .thenThrow(new ResourceNotFoundException("User not found"));

        mockMvc.perform(get("/api/users/999"))
            .andExpect(status().isNotFound())
            .andExpect(jsonPath("$.message").value("User not found"));
    }

    @Test
    void testBadRequestException() throws Exception {
        when(userService.createUser(any()))
            .thenThrow(new BadRequestException("Invalid data"));

        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{}"))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.message").value("Invalid data"));
    }
}
```

### Advanced MockMvc Features

```java
@WebMvcTest(AdvancedController.class)
class AdvancedMockMvcTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void testWithResultActions() throws Exception {
        MvcResult result = mockMvc.perform(get("/api/data"))
            .andDo(print()) // Print request and response
            .andExpect(status().isOk())
            .andReturn();

        String content = result.getResponse().getContentAsString();
        assertNotNull(content);
    }

    @Test
    void testMultipartFileUpload() throws Exception {
        MockMultipartFile file = new MockMultipartFile(
            "file",
            "test.txt",
            MediaType.TEXT_PLAIN_VALUE,
            "Hello World".getBytes()
        );

        mockMvc.perform(multipart("/api/upload")
                .file(file)
                .param("description", "Test file"))
            .andExpect(status().isOk());
    }

    @Test
    void testJsonPath() throws Exception {
        mockMvc.perform(get("/api/complex"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.user.name").value("John"))
            .andExpect(jsonPath("$.user.address.city").value("New York"))
            .andExpect(jsonPath("$.orders[0].id").value(1))
            .andExpect(jsonPath("$.orders[*].status").value(hasItem("COMPLETED")));
    }
}
```

---

## 6. Database Testing {#6-database-testing}

### Testing with @DataJpaTest

```java
@DataJpaTest
class UserRepositoryTest {

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private UserRepository userRepository;

    @Test
    void testSaveUser() {
        // Given
        User user = new User("John", "john@example.com");

        // When
        User saved = userRepository.save(user);

        // Then
        assertThat(saved.getId()).isNotNull();
        assertThat(saved.getName()).isEqualTo("John");
    }

    @Test
    void testFindByEmail() {
        // Given
        User user = new User("John", "john@example.com");
        entityManager.persist(user);
        entityManager.flush();

        // When
        Optional<User> found = userRepository.findByEmail("john@example.com");

        // Then
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("John");
    }

    @Test
    void testFindAll() {
        // Given
        entityManager.persist(new User("John", "john@example.com"));
        entityManager.persist(new User("Jane", "jane@example.com"));
        entityManager.flush();

        // When
        List<User> users = userRepository.findAll();

        // Then
        assertThat(users).hasSize(2);
    }

    @Test
    void testDeleteUser() {
        // Given
        User user = entityManager.persist(new User("John", "john@example.com"));
        Long userId = user.getId();

        // When
        userRepository.deleteById(userId);

        // Then
        Optional<User> deleted = userRepository.findById(userId);
        assertThat(deleted).isEmpty();
    }

    @Test
    void testCustomQuery() {
        // Given
        entityManager.persist(new User("John", "john@example.com"));
        entityManager.persist(new User("Jane", "jane@example.com"));
        entityManager.flush();

        // When
        List<User> users = userRepository.findByNameContaining("J");

        // Then
        assertThat(users).hasSize(2);
    }
}
```

### Testing with H2 In-Memory Database

```yaml
# src/test/resources/application.yml
spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password:
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true
    properties:
      hibernate:
        format_sql: true
  h2:
    console:
      enabled: true
```

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class CustomDatabaseTest {
    // Uses the configured H2 database instead of the default
}
```

### Testing with Testcontainers

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>postgresql</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>junit-jupiter</artifactId>
    <scope>test</scope>
</dependency>
```

```java
@DataJpaTest
@Testcontainers
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class UserRepositoryTestContainersTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15-alpine")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    private UserRepository userRepository;

    @Test
    void testWithRealPostgres() {
        User user = new User("John", "john@example.com");
        User saved = userRepository.save(user);

        assertThat(saved.getId()).isNotNull();
    }
}
```

### Transaction Management in Tests

```java
@DataJpaTest
class TransactionalTest {

    @Autowired
    private UserRepository userRepository;

    @Test
    @Transactional
    void testWithTransaction() {
        // By default, @DataJpaTest is transactional
        // Changes are rolled back after test
        User user = new User("John", "john@example.com");
        userRepository.save(user);

        // This will be rolled back
    }

    @Test
    @Rollback(false)
    void testWithoutRollback() {
        // This won't be rolled back
        User user = new User("John", "john@example.com");
        userRepository.save(user);
    }

    @Test
    void testTransactionalBehavior() {
        userRepository.save(new User("John", "john@example.com"));

        // Query within same transaction
        List<User> users = userRepository.findAll();
        assertThat(users).hasSize(1);
    }
}
```

### Testing with @JdbcTest

```java
@JdbcTest
class JdbcUserRepositoryTest {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    private JdbcUserRepository repository;

    @BeforeEach
    void setUp() {
        repository = new JdbcUserRepository(jdbcTemplate);
    }

    @Test
    void testInsertUser() {
        User user = new User(null, "John", "john@example.com");

        User saved = repository.save(user);

        assertThat(saved.getId()).isNotNull();

        Long count = jdbcTemplate.queryForObject(
            "SELECT COUNT(*) FROM users WHERE email = ?",
            Long.class,
            "john@example.com"
        );

        assertThat(count).isEqualTo(1);
    }
}
```

---

## 7. Spring Boot Test Slices {#7-test-slices}

### @WebMvcTest - Web Layer Testing

```java
@WebMvcTest(UserController.class)
class WebLayerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Test
    void testControllerOnly() throws Exception {
        // Only web layer components are loaded
        // Services must be mocked
        when(userService.getUsers()).thenReturn(List.of());

        mockMvc.perform(get("/api/users"))
            .andExpect(status().isOk());
    }
}
```

### @JsonTest - JSON Serialization Testing

```java
@JsonTest
class JsonSerializationTest {

    @Autowired
    private JacksonTester<User> json;

    @Test
    void testSerialization() throws Exception {
        User user = new User(1L, "John", "john@example.com");

        assertThat(json.write(user))
            .hasJsonPathValue("$.id")
            .hasJsonPathValue("$.name", "John")
            .hasJsonPathValue("$.email", "john@example.com");

        String expected = "{\"id\":1,\"name\":\"John\",\"email\":\"john@example.com\"}";
        assertThat(json.write(user)).isEqualToJson(expected);
    }

    @Test
    void testDeserialization() throws Exception {
        String content = "{\"id\":1,\"name\":\"John\",\"email\":\"john@example.com\"}";

        User user = json.parse(content).getObject();

        assertThat(user.getId()).isEqualTo(1L);
        assertThat(user.getName()).isEqualTo("John");
        assertThat(user.getEmail()).isEqualTo("john@example.com");
    }
}
```

### @RestClientTest - REST Client Testing

```java
@RestClientTest(UserApiClient.class)
class RestClientTestExample {

    @Autowired
    private UserApiClient client;

    @Autowired
    private MockRestServiceServer server;

    @Test
    void testRestClient() {
        // Mock the external API
        server.expect(requestTo("/api/users/1"))
            .andRespond(withSuccess(
                "{\"id\":1,\"name\":\"John\"}",
                MediaType.APPLICATION_JSON
            ));

        // Call the client
        User user = client.getUserById(1L);

        // Verify
        assertThat(user.getName()).isEqualTo("John");
        server.verify();
    }
}
```

---

## 8. Advanced Testing Techniques {#8-advanced-techniques}

### Testing with Profiles

```java
@SpringBootTest
@ActiveProfiles("test")
class ProfileBasedTest {
    // Loads application-test.yml

    @Value("${app.feature.enabled}")
    private boolean featureEnabled;

    @Test
    void testWithTestProfile() {
        assertFalse(featureEnabled);
    }
}
```

### Custom Test Configuration

```java
@TestConfiguration
class TestConfig {

    @Bean
    @Primary
    public UserService testUserService() {
        return new MockUserService();
    }
}

@SpringBootTest
@Import(TestConfig.class)
class CustomConfigTest {

    @Autowired
    private UserService userService;

    @Test
    void testWithCustomBean() {
        // Uses MockUserService instead of real UserService
    }
}
```

### @TestPropertySource

```java
@SpringBootTest
@TestPropertySource(properties = {
    "app.name=TestApp",
    "app.version=1.0.0-TEST"
})
class PropertySourceTest {

    @Value("${app.name}")
    private String appName;

    @Test
    void testProperties() {
        assertEquals("TestApp", appName);
    }
}

@SpringBootTest
@TestPropertySource(locations = "classpath:test.properties")
class PropertyFileTest {
    // Loads properties from test.properties
}
```

### Testing Async Methods

```java
@SpringBootTest
@EnableAsync
class AsyncTest {

    @Autowired
    private AsyncService asyncService;

    @Test
    void testAsyncMethod() throws Exception {
        CompletableFuture<String> future = asyncService.processAsync();

        // Wait for async operation
        String result = future.get(5, TimeUnit.SECONDS);

        assertThat(result).isNotNull();
    }
}
```

### Testing with WireMock

```xml
<dependency>
    <groupId>org.wiremock</groupId>
    <artifactId>wiremock-standalone</artifactId>
    <scope>test</scope>
</dependency>
```

```java
@SpringBootTest
@AutoConfigureWireMock(port = 8080)
class WireMockTest {

    @Autowired
    private ExternalApiClient apiClient;

    @Test
    void testExternalApiCall() {
        // Stub the external API
        stubFor(get(urlEqualTo("/api/users/1"))
            .willReturn(aResponse()
                .withHeader("Content-Type", "application/json")
                .withBody("{\"id\":1,\"name\":\"John\"}")
                .withStatus(200)));

        // Call the client
        User user = apiClient.getUser(1L);

        // Verify
        assertThat(user.getName()).isEqualTo("John");

        // Verify the request was made
        verify(getRequestedFor(urlEqualTo("/api/users/1")));
    }
}
```

### ReflectionTestUtils - Testing Private Fields

```java
class ReflectionTestUtilsExample {

    @Test
    void testPrivateField() {
        UserService service = new UserService();

        // Set private field
        ReflectionTestUtils.setField(service, "maxRetries", 5);

        // Get private field
        Integer maxRetries = (Integer) ReflectionTestUtils.getField(service, "maxRetries");

        assertThat(maxRetries).isEqualTo(5);
    }

    @Test
    void testPrivateMethod() {
        UserService service = new UserService();

        // Invoke private method
        String result = ReflectionTestUtils.invokeMethod(
            service,
            "formatUserName",
            "john"
        );

        assertThat(result).isEqualTo("JOHN");
    }
}
```

---

## 9. Best Practices {#9-best-practices}

### 1. Follow AAA Pattern (Arrange-Act-Assert)

```java
@Test
void testUserCreation() {
    // Arrange (Given)
    User user = new User("John", "john@example.com");
    when(userRepository.save(any())).thenReturn(user);

    // Act (When)
    User created = userService.createUser(user);

    // Assert (Then)
    assertThat(created.getName()).isEqualTo("John");
    verify(userRepository, times(1)).save(any());
}
```

### 2. Use Descriptive Test Names

```java
// Good
@Test
void createUser_WithValidData_ShouldReturnSavedUser() { }

@Test
void createUser_WithDuplicateEmail_ShouldThrowException() { }

// Bad
@Test
void test1() { }

@Test
void testCreateUser() { }
```

### 3. One Assertion Per Test Concept

```java
// Good - Tests one specific behavior
@Test
void getUserById_WhenUserExists_ShouldReturnUser() {
    User user = userService.getUserById(1L);
    assertThat(user).isNotNull();
}

@Test
void getUserById_WhenUserExists_ShouldHaveCorrectName() {
    User user = userService.getUserById(1L);
    assertThat(user.getName()).isEqualTo("John");
}

// Acceptable - Related assertions
@Test
void getUserById_WhenUserExists_ShouldReturnCompleteUser() {
    User user = userService.getUserById(1L);
    assertThat(user).isNotNull();
    assertThat(user.getName()).isEqualTo("John");
    assertThat(user.getEmail()).isEqualTo("john@example.com");
}
```

### 4. Use Test Slices for Faster Tests

```java
// Slow - Loads entire context
@SpringBootTest
class SlowTest { }

// Fast - Loads only web layer
@WebMvcTest(UserController.class)
class FastControllerTest { }

// Fast - Loads only JPA layer
@DataJpaTest
class FastRepositoryTest { }
```

### 5. Avoid Testing Framework Code

```java
// Bad - Testing Spring's functionality
@Test
void testAutowiring() {
    assertNotNull(userService);
}

// Good - Testing your business logic
@Test
void createUser_ShouldSaveToDatabase() {
    User user = userService.createUser(new User("John", "john@example.com"));
    verify(userRepository).save(any());
}
```

### 6. Mock External Dependencies

```java
@SpringBootTest
class ServiceTest {

    @MockBean
    private ExternalApiClient externalApi;

    @Autowired
    private UserService userService;

    @Test
    void testServiceWithMockedExternalDependency() {
        when(externalApi.validateEmail(anyString())).thenReturn(true);

        User user = userService.createUser(new User("John", "john@example.com"));

        assertThat(user).isNotNull();
    }
}
```

### 7. Keep Tests Independent

```java
// Bad - Tests depend on execution order
class BadTest {
    private static User sharedUser;

    @Test
    void test1() {
        sharedUser = userService.create(new User());
    }

    @Test
    void test2() {
        userService.update(sharedUser); // Depends on test1
    }
}

// Good - Each test is independent
class GoodTest {

    @Test
    void testCreate() {
        User user = userService.create(new User());
        assertNotNull(user.getId());
    }

    @Test
    void testUpdate() {
        User user = userService.create(new User());
        User updated = userService.update(user);
        assertNotNull(updated);
    }
}
```

---

## 10. Common Pitfalls {#10-common-pitfalls}

### 1. Not Using @Transactional Correctly

```java
// Pitfall - Data persists between tests
@DataJpaTest
@Rollback(false)
class BadTest {
    @Test
    void test1() {
        userRepository.save(new User("John"));
        // Data persists!
    }
}

// Solution - Use default @Transactional behavior
@DataJpaTest
class GoodTest {
    @Test
    void test1() {
        userRepository.save(new User("John"));
        // Data is rolled back automatically
    }
}
```

### 2. Overusing @SpringBootTest

```java
// Slow - Loads entire Spring context
@SpringBootTest
class SlowControllerTest {
    @Autowired
    private MockMvc mockMvc; // MockMvc not auto-configured here
}

// Fast - Use test slice
@WebMvcTest(UserController.class)
class FastControllerTest {
    @Autowired
    private MockMvc mockMvc;
}
```

### 3. Not Verifying Mock Interactions

```java
// Bad - No verification
@Test
void testBad() {
    when(userService.getUser(1L)).thenReturn(new User());
    // Method might not be called!
}

// Good - Verify interactions
@Test
void testGood() {
    when(userService.getUser(1L)).thenReturn(new User());
    User user = controller.getUser(1L);
    verify(userService).getUser(1L);
}
```

### 4. Testing Implementation Instead of Behavior

```java
// Bad - Testing implementation details
@Test
void testImplementation() {
    userService.processUser(1L);
    verify(userRepository).findById(1L);
    verify(validator).validate(any());
    verify(userRepository).save(any());
}

// Good - Testing behavior
@Test
void processUser_ShouldUpdateUserStatus() {
    User user = userService.processUser(1L);
    assertThat(user.getStatus()).isEqualTo(Status.PROCESSED);
}
```

### 5. Ignoring Test Data Setup

```java
// Bad - Magic numbers and unclear data
@Test
void testBad() {
    User user = new User();
    user.setId(1L);
    user.setName("John");
}

// Good - Use test data builders
@Test
void testGood() {
    User user = UserTestDataBuilder.aUser()
        .withName("John")
        .withEmail("john@example.com")
        .build();
}

// Test Data Builder
class UserTestDataBuilder {
    private String name = "Default Name";
    private String email = "default@example.com";

    static UserTestDataBuilder aUser() {
        return new UserTestDataBuilder();
    }

    UserTestDataBuilder withName(String name) {
        this.name = name;
        return this;
    }

    UserTestDataBuilder withEmail(String email) {
        this.email = email;
        return this;
    }

    User build() {
        return new User(name, email);
    }
}
```

---

## Complete Example: Testing a Full Service Layer

```java
// Entity
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    private String name;

    @Email
    private String email;

    private LocalDateTime createdAt;
}

// Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    List<User> findByNameContaining(String name);
}

// Service
@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final EmailService emailService;

    public User createUser(User user) {
        if (userRepository.findByEmail(user.getEmail()).isPresent()) {
            throw new DuplicateEmailException("Email already exists");
        }

        user.setCreatedAt(LocalDateTime.now());
        User saved = userRepository.save(user);

        emailService.sendWelcomeEmail(saved.getEmail());

        return saved;
    }

    public User getUserById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));
    }

    public List<User> searchUsers(String query) {
        return userRepository.findByNameContaining(query);
    }
}

// Service Test - Unit Test
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private EmailService emailService;

    @InjectMocks
    private UserService userService;

    @Test
    void createUser_WithValidData_ShouldSaveAndSendEmail() {
        // Given
        User user = new User(null, "John", "john@example.com", null);
        User savedUser = new User(1L, "John", "john@example.com", LocalDateTime.now());

        when(userRepository.findByEmail("john@example.com")).thenReturn(Optional.empty());
        when(userRepository.save(any(User.class))).thenReturn(savedUser);
        doNothing().when(emailService).sendWelcomeEmail(anyString());

        // When
        User result = userService.createUser(user);

        // Then
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getCreatedAt()).isNotNull();

        verify(userRepository).findByEmail("john@example.com");
        verify(userRepository).save(any(User.class));
        verify(emailService).sendWelcomeEmail("john@example.com");
    }

    @Test
    void createUser_WithDuplicateEmail_ShouldThrowException() {
        // Given
        User user = new User(null, "John", "john@example.com", null);
        when(userRepository.findByEmail("john@example.com"))
            .thenReturn(Optional.of(user));

        // When & Then
        assertThatThrownBy(() -> userService.createUser(user))
            .isInstanceOf(DuplicateEmailException.class)
            .hasMessage("Email already exists");

        verify(userRepository, never()).save(any());
        verify(emailService, never()).sendWelcomeEmail(anyString());
    }
}

// Repository Test - Integration Test
@DataJpaTest
class UserRepositoryTest {

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private UserRepository userRepository;

    @Test
    void findByEmail_WhenUserExists_ShouldReturnUser() {
        // Given
        User user = new User(null, "John", "john@example.com", LocalDateTime.now());
        entityManager.persist(user);
        entityManager.flush();

        // When
        Optional<User> found = userRepository.findByEmail("john@example.com");

        // Then
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("John");
    }
}

// Controller Test
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void createUser_WithValidData_ShouldReturn201() throws Exception {
        // Given
        User user = new User(null, "John", "john@example.com", null);
        User savedUser = new User(1L, "John", "john@example.com", LocalDateTime.now());

        when(userService.createUser(any(User.class))).thenReturn(savedUser);

        // When & Then
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(user)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.name").value("John"))
            .andExpect(jsonPath("$.email").value("john@example.com"));
    }
}
```

---

## Summary

This guide covers comprehensive Spring Boot testing from basics to expert level:

1. **Fundamentals**: JUnit 5, assertions, test lifecycle
2. **Mocking**: Mockito, @Mock, @MockBean, verification, ArgumentCaptor
3. **REST Testing**: MockMvc, different HTTP methods, validation, exception handling
4. **Database Testing**: @DataJpaTest, H2, Testcontainers, transactions
5. **Test Slices**: @WebMvcTest, @JsonTest, @RestClientTest
6. **Advanced**: Profiles, async testing, WireMock, ReflectionTestUtils
7. **Best Practices**: AAA pattern, descriptive names, test independence
8. **Common Pitfalls**: Transaction management, overusing @SpringBootTest

Remember:

- ✅ Write tests at the appropriate level (unit vs integration)
- ✅ Use test slices for faster execution
- ✅ Keep tests independent and isolated
- ✅ Mock external dependencies
- ✅ Follow AAA pattern (Arrange-Act-Assert)
- ✅ Use descriptive test names
- ✅ Verify mock interactions
- ✅ Test behavior, not implementation

Happy Testing! 🚀
