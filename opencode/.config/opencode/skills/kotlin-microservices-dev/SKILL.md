---
name: Kotlin Microservices Development
version: 1.0.0
description: Comprehensive Kotlin microservices development framework with 20+ specialized skills for the company 3-layer architecture
author: the company
keywords: [kotlin, microservices, domain-models, testing, jooq, micronaut, architecture]
---

# Kotlin Microservices Development

This skill provides comprehensive Kotlin microservices development tools following the company's 3-layer architecture (Handlers → Operations → Stores) with domain-driven design principles.

## Architecture Overview

### 3-Layer Architecture Pattern
- **Handler Layer**: HTTP controllers, RPC handlers, Job handlers
- **Operations Layer**: Business logic orchestration
- **Stores Layer**: Data access abstraction (database, gRPC, REST)
- **Models Layer**: Immutable domain models with proper token patterns

### Key Principles
- Domain-driven design with immutable domain models
- Strict separation of concerns across layers
- Token-based entity identification
- Comprehensive testing with Kotest and MockK
- jOOQ for type-safe database access
- Micronaut dependency injection

## Available Commands

### /kotlin-domain-model
Guide creation and maintenance of Kotlin domain models following the company patterns.

**Usage:**
- `/kotlin-domain-model` - Interactive domain model creation/modification

**Key Features:**
- **Nullable Token Pattern**: Service-assigned fields use nullable tokens with non-null getters
- **Immutable Collections**: All collections are `List`/`Map` (never `MutableList`)
- **Explicit Defaults**: All parameters have explicit defaults unless required
- **Business Validation**: `init` blocks with custom validators for business rules
- **Computed Properties**: `by lazy` for expensive computations, direct `get()` for transformations

**Package Structure:**
```
com.the company.core.{service}.models.{group}/EntityName.kt
com.the company.core.{service}.models/Amount.kt
com.the company.core.{service}.models/Exceptions.kt
```

### /kotlin-create-store
Complete CRUD store generation with jOOQ integration, converters, and comprehensive tests.

**Usage:**
- `/kotlin-create-store <entity-name>` - Generate complete store layer

**Generated Components:**
- Store interface with CRUD operations
- Store implementation with jOOQ queries
- Domain-to-DB converters (bidirectional)
- Comprehensive test suite with MockK
- Error handling and transaction patterns

**Features:**
- Type-safe database queries with jOOQ
- Proper transaction boundary management
- Optimistic locking patterns
- Comprehensive error handling

### /kotlin-db-converter
Create bidirectional converters between domain models and database records.

**Usage:**
- `/kotlin-db-converter <domain-model>` - Generate converter for domain/DB mapping

**Converter Patterns:**
- Domain model → jOOQ Record (for inserts/updates)
- jOOQ Record → Domain model (for queries)
- Amount field mapping (value/currency split)
- Token serialization/deserialization
- Null handling and default values

### /kotlin-testing-store
Generate comprehensive test suites for store layers using Kotest FreeSpec patterns.

**Usage:**
- `/kotlin-testing-store <store-name>` - Create complete test suite

**Testing Patterns:**
- **FreeSpec**: Behavior-driven test organization
- **MockK**: Advanced mocking with relaxed/strict modes
- **Test Data Factories**: Reusable test data builders
- **Transaction Testing**: Proper transaction boundary testing
- **Error Scenario Coverage**: Comprehensive error path testing

### /kotlin-freespec-tests
Write tests using Kotest FreeSpec patterns with proper structure and assertions.

**Usage:**
- `/kotlin-freespec-tests <class-to-test>` - Generate structured test suite

**FreeSpec Structure:**
```kotlin
class EntityStoreTest : FreeSpec({
    "findByToken" - {
        "should return entity when found" {
            // Given/When/Then structure
        }

        "should return null when not found" {
            // Test scenario
        }
    }

    "create" - {
        "should create new entity successfully" {
            // Creation test
        }
    }
})
```

### /kotlin-mockk-mocks
Create proper mocks using MockK with appropriate relaxed/strict configurations.

**Usage:**
- `/kotlin-mockk-mocks <interface-to-mock>` - Generate MockK mock setup

**MockK Patterns:**
- **Relaxed Mocks**: For non-critical interactions
- **Strict Mocks**: For critical business logic verification
- **Slot Capture**: Verify complex argument passing
- **Answer Patterns**: Custom response logic

### /kotlin-test-data-factories
Create reusable test data factories for consistent test data generation.

**Usage:**
- `/kotlin-test-data-factories <entity-name>` - Generate data factory

**Factory Patterns:**
- Default entity builders with sensible defaults
- Parameterized builders for specific test scenarios
- Relationship management (parent/child entities)
- Random data generation for properties

### /kotlin-feed-consumer
Create feed consumer for processing external events and data streams.

**Usage:**
- `/kotlin-feed-consumer <feed-name>` - Generate feed processing components

**Components:**
- Event handlers with proper error handling
- Message deserialization and validation
- Dead letter queue handling
- Monitoring and metrics integration

### /kotlin-feed-publisher
Add feed publisher for broadcasting domain events to external systems.

**Usage:**
- `/kotlin-feed-publisher <event-type>` - Generate event publishing

**Features:**
- Event serialization and schema validation
- Reliable delivery patterns
- Event versioning and backward compatibility
- Publisher interface abstraction

### /kotlin-db-migration
Create database migration files following the company patterns.

**Usage:**
- `/kotlin-db-migration <migration-name>` - Generate Flyway migration

**Migration Patterns:**
- Table creation with proper constraints
- Index creation for query optimization
- Foreign key relationships
- Backward compatibility considerations

### /kotlin-add-dependencies
Add dependencies to Gradle build files with proper version management.

**Usage:**
- `/kotlin-add-dependencies <dependency-type>` - Add managed dependencies

**Dependency Categories:**
- Core framework dependencies (Micronaut, jOOQ)
- Testing dependencies (Kotest, MockK)
- Database drivers and migration tools
- Monitoring and observability libraries

### /kotlin-detekt-linting
Configure and run Detekt linting with the company code style rules.

**Usage:**
- `/kotlin-detekt-linting` - Run code analysis and fix issues

**Linting Rules:**
- Code style consistency
- Complexity analysis
- Security vulnerability detection
- Performance anti-pattern detection

### /kotlin-analyze-endpoint
Analyze existing endpoints for architecture compliance and improvement opportunities.

**Usage:**
- `/kotlin-analyze-endpoint <endpoint-path>` - Comprehensive endpoint analysis

**Analysis Areas:**
- Architecture layer separation
- Error handling patterns
- Security considerations
- Performance optimizations
- Testing coverage assessment

### /kotlin-test-validation
Test validation workflow to ensure comprehensive test coverage and quality.

**Usage:**
- `/kotlin-test-validation` - Run complete test validation

**Validation Checks:**
- Test coverage metrics
- Test quality assessment
- Performance test validation
- Integration test completeness

## Domain Model Patterns

### Nullable Token Pattern
For service-assigned fields that aren't known at construction:

```kotlin
data class Order(
    val nullableToken: OrderToken? = null,    // Assigned by service
    val businessToken: BusinessToken,         // Required - multi-tenant
) {
    val token: OrderToken
        get() = nullableToken!!  // Intentionally unsafe - fails fast
}
```

### Amount Type Usage
Always use `Amount` for monetary values:

```kotlin
data class Order(
    val subtotal: Amount,                    // Required amount
    val discount: Amount? = null,            // Optional amount
)

// Amount structure
data class Amount(
    val value: BigDecimal,    // Value in smallest unit (cents)
    val currency: Currency    // java.util.Currency
)
```

### Timestamp Handling
Use `OffsetDateTime` for all timestamps:

```kotlin
data class Order(
    val createdAt: OffsetDateTime? = null,      // Audit timestamp
    val updatedAt: OffsetDateTime? = null,      // Audit timestamp
    val processedAt: OffsetDateTime? = null,    // State transition
)
```

### Immutable Collections
All collections must be immutable:

```kotlin
data class Order(
    val lineItems: List<OrderLineItem> = listOf(),     // ✅ Immutable
    val taxes: Map<String, Tax> = mapOf(),             // ✅ Immutable

    // ❌ Never use MutableList/MutableMap
)
```

### Computed Properties
Use appropriate patterns for derived values:

```kotlin
data class Order(
    val lineItems: List<OrderLineItem> = listOf(),
) {
    // Expensive computation - cached with lazy
    val subtotal: BigDecimal by lazy {
        lineItems.sumOf { item ->
            if (item.isVoided) BigDecimal.ZERO
            else item.subtotal
        }
    }

    // Simple transformation - direct getter
    val allTokens: List<Token>
        get() = lineItems.flatMap { it.tokens }.distinct()
}
```

## Testing Patterns

### FreeSpec Structure
Organize tests using behavior-driven patterns:

```kotlin
class OrderStoreTest : FreeSpec({
    "findByToken" - {
        "should return order when found" {
            // Given
            val orderToken = OrderToken.random()
            every { mockOrderStore.findByToken(orderToken) } returns mockOrder

            // When
            val result = orderStore.findByToken(orderToken)

            // Then
            result shouldBe mockOrder
        }

        "should return null when not found" {
            // Test not found scenario
        }
    }
})
```

### MockK Patterns
Use appropriate mock configurations:

```kotlin
// Relaxed mock for non-critical dependencies
val mockLogger = mockk<Logger>(relaxed = true)

// Strict mock for critical business logic
val mockOrderStore = mockk<OrderStore>()

// Capture arguments for verification
val orderSlot = slot<Order>()
every { mockOrderStore.create(capture(orderSlot)) } returns savedOrder
```

## Architecture Compliance

### Handler Layer
- HTTP controllers using Micronaut annotations
- Input validation and error handling
- Authentication and authorization
- Request/response transformation

### Operations Layer
- Business logic orchestration
- Transaction boundary management
- Domain model manipulation
- Cross-cutting concerns (logging, metrics)

### Stores Layer
- Data access abstraction
- jOOQ query implementation
- Database transaction handling
- External service integration

## Security Considerations

### Input Validation
- Validate all user inputs at handler layer
- Use domain model validation for business rules
- Sanitize data before database operations

### Authentication Integration
- Proper authentication method enforcement for RPC handlers
- Token validation and session management
- Role-based access control patterns

### Secure Logging
- Use RequestContext for correlation
- Never log sensitive data (tokens, PII)
- Structured logging with proper levels

## Performance Guidelines

### Database Optimization
- Use jOOQ for type-safe, optimized queries
- Implement proper indexing strategies
- Avoid N+1 query problems
- Use connection pooling effectively

### Memory Management
- Immutable objects reduce memory leaks
- Lazy evaluation for expensive computations
- Proper cleanup of resources
- Avoid excessive object creation in loops

### Transaction Boundaries
- Keep transactions as short as possible
- Never perform distributed transactions
- Use proper isolation levels
- Handle transaction failures gracefully

## Tool Requirements

This skill requires access to:
- Kotlin compilation and runtime
- Gradle build system
- jOOQ code generation
- Kotest test framework
- MockK mocking library
- Detekt static analysis
- Database connectivity (PostgreSQL)
- Micronaut framework