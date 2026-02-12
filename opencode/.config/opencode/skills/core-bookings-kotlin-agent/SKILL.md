---
name: Core Bookings Specialized Kotlin Agent
version: 1.0.0
description: Specialized agent for Core Bookings microservice development, following GlossGenius high-quality Kotlin conventions, standards, and best practices
author: GlossGenius
keywords: [kotlin, core-bookings, microservices, domain-models, testing, jooq, micronaut, architecture, tokens, stores, operations]
---

# Core Bookings Specialized Kotlin Agent

This specialized agent is designed for Core Bookings microservice development, following GlossGenius's high-quality Kotlin conventions, standards, and best practices. The agent intelligently handles both current architecture patterns and guides migration to target patterns while maintaining backward compatibility.

## Agent Purpose

This agent receives instructions to code features based on clear and unclear requirements, always adhering to GlossGenius' conventions, standards and best practices. It bridges the gap between current Core Bookings patterns and ideal GlossGenius architecture while ensuring code quality and consistency.

## Architecture Overview

### Hybrid Architecture Support
The agent supports both current and target architecture patterns:

**Current Pattern** (Handler → Store → Client):
- **Handler Layer**: RPC handlers using Micronaut annotations
- **Store Layer**: Business logic orchestration + data access
- **Client Layer**: External API communication with mappers

**Target Pattern** (Handler → Operations → Stores):
- **Handler Layer**: HTTP controllers, RPC handlers, Job handlers  
- **Operations Layer**: Business logic orchestration
- **Stores Layer**: Data access abstraction (database, gRPC, REST)
- **Models Layer**: Immutable domain models with proper token patterns

### Key Principles
- **Domain-driven design** with immutable domain models
- **Token-first API patterns** with optional GUID backward compatibility
- **Strict separation of concerns** across layers
- **Jakarta DI annotations** (`@Singleton`, `@Named`) with Micronaut
- **Comprehensive testing** with Kotest and MockK
- **jOOQ for type-safe database access** with PostgreSQL
- **Snake_case JSON serialization** with proper naming conventions

## Project-Specific Conventions

### Core Bookings Standards
- **Package Structure**: `com.glossgenius.core.bookings.{layer}.{feature}`
- **Token + GUID Support**: Dual API methods for backward compatibility
- **OffsetDateTime Usage**: Timezone-aware date/time handling
- **ServiceException Patterns**: Factory functions for error creation
- **Gradle Lockfiles**: Dependency management with `--write-locks`
- **Architecture Testing**: ArchUnit rules for layer validation
- **Liquibase Migrations**: Database schema management

### GlossGenius Universal Standards
- **Nullable Token Pattern**: Service-assigned fields use nullable tokens with non-null getters
- **Immutable Collections**: All collections are `List`/`Map` (never `MutableList`)
- **Amount Type**: Monetary values use `Amount(BigDecimal, Currency)`
- **Computed Properties**: `by lazy` for expensive computations, direct `get()` for transformations
- **Business Validation**: `init` blocks with custom validators for business rules

## Available Commands

### /cb-domain-model
Create and maintain Core Bookings domain models following project and GlossGenius patterns.

**Usage:**
- `/cb-domain-model` - Interactive domain model creation/modification
- `/cb-domain-model <ModelName>` - Create specific domain model

**Key Features:**
- **Token-first design** with optional GUID support
- **OffsetDateTime defaults** for timezone awareness
- **Snake_case JSON serialization** with `@JsonNaming`
- **Amount type integration** for monetary values
- **Immutable collections** validation
- **ServiceException integration** for domain validation

**Package Structure:**
```
com.glossgenius.core.bookings.models.{group}/EntityName.kt
com.glossgenius.core.bookings.models/Amount.kt
com.glossgenius.core.bookings.models/Exceptions.kt
```

### /cb-create-store
Generate complete CRUD store layer with jOOQ, token/GUID support, and comprehensive tests.

**Usage:**
- `/cb-create-store <entity-name>` - Generate complete store layer
- `/cb-create-store <entity-name> --token-only` - Generate token-based only
- `/cb-create-store <entity-name> --with-guid` - Generate with GUID support

**Generated Components:**
- Store interface with CRUD operations (token-first)
- Store implementation with jOOQ queries
- Optional GUID-based methods for backward compatibility
- Domain-to-DB converters (bidirectional)
- Comprehensive test suite with MockK
- ServiceException error handling patterns

### /cb-create-operations
Generate missing Operations layer to bridge current Store pattern to target architecture.

**Usage:**
- `/cb-create-operations <feature-name>` - Generate operations layer
- `/cb-create-operations --migrate-store <store-name>` - Migrate existing store

**Generated Components:**
- Operations interface with business logic methods
- Operations implementation with proper orchestration
- Transaction boundary management
- Store layer delegation
- Comprehensive business logic tests

### /cb-client-integration
Create or enhance external API client integrations following project patterns.

**Usage:**
- `/cb-client-integration <client-name>` - Create new client integration
- `/cb-client-integration --enhance <existing-client>` - Enhance existing client

**Features:**
- Base client inheritance (`CoreApiBaseClient`)
- Token-based and GUID-based API methods
- URI builder patterns for dynamic URLs
- Payload classes for API contracts
- Converter classes for response transformation
- Comprehensive error handling

### /cb-testing-suite
Generate comprehensive test suites using Kotest FreeSpec and project patterns.

**Usage:**
- `/cb-testing-suite <class-to-test>` - Generate complete test suite
- `/cb-testing-suite --architecture` - Generate ArchUnit tests

**Testing Patterns:**
- **FreeSpec Structure**: Behavior-driven test organization
- **MockK Integration**: Relaxed loggers, strict business logic
- **Test Data Factories**: Realistic data builders
- **Architecture Testing**: Layer boundary validation
- **ServiceException Testing**: Error scenario coverage

### /cb-db-migration
Create Liquibase database migrations following Core Bookings patterns.

**Usage:**
- `/cb-db-migration <migration-name>` - Generate migration file
- `/cb-db-migration --table <table-name>` - Generate table creation
- `/cb-db-migration --index <table-name>` - Generate index migration

**Migration Features:**
- Liquibase XML format
- Token and GUID column patterns
- Proper constraint definitions
- Index optimization
- Backward compatibility considerations

### /cb-analyze-architecture
Analyze existing code for architecture compliance and improvement opportunities.

**Usage:**
- `/cb-analyze-architecture` - Analyze entire codebase
- `/cb-analyze-architecture <package>` - Analyze specific package
- `/cb-analyze-architecture --migration-plan` - Generate migration recommendations

**Analysis Areas:**
- Current vs target architecture assessment
- Layer separation validation
- Token/GUID usage patterns
- Error handling compliance
- Testing coverage assessment
- Performance optimization opportunities

### /cb-quality-check
Run comprehensive code quality validation and automated fixes.

**Usage:**
- `/cb-quality-check` - Run all quality checks
- `/cb-quality-check --detekt` - Run Detekt linting only
- `/cb-quality-check --fix` - Apply automated fixes

**Quality Checks:**
- Detekt static analysis with project config
- Test coverage validation
- Architecture rule enforcement
- Convention compliance checking
- Performance anti-pattern detection

### /cb-add-dependencies
Add dependencies to Gradle with proper version management and lockfile updates.

**Usage:**
- `/cb-add-dependencies <dependency-type>` - Add managed dependencies
- `/cb-add-dependencies --update-locks` - Update gradle lockfiles

**Dependency Categories:**
- Core framework (Micronaut, jOOQ, Liquibase)
- Testing (Kotest, MockK, ArchUnit)
- Database drivers and tools
- Monitoring and observability

### /cb-feed-integration
Create feed consumer/publisher for event-driven architecture.

**Usage:**
- `/cb-feed-integration --consumer <feed-name>` - Create feed consumer
- `/cb-feed-integration --publisher <event-type>` - Create event publisher

**Features:**
- Event processing with proper error handling
- Message serialization/deserialization
- Dead letter queue patterns
- Monitoring integration
- Backward compatibility support

## Domain Model Patterns

### Token-First Pattern with GUID Support
For entities that support both token and GUID identification:

```kotlin
data class Booking(
    val nullableToken: BookingToken? = null,    // Service-assigned
    val businessToken: BusinessToken,           // Required multi-tenant
    val guid: UUID? = null,                     // Legacy support
    val createdAt: OffsetDateTime? = null,
    val updatedAt: OffsetDateTime? = null,
) {
    val token: BookingToken
        get() = nullableToken!!  // Intentionally unsafe - fails fast
    
    val id: String
        get() = token.value  // Primary identifier
}
```

### Amount Type Usage
Always use `Amount` for monetary values following project patterns:

```kotlin
data class BookingLineItem(
    val amount: Amount,                    // Required amount
    val discount: Amount? = null,          // Optional amount  
    val taxAmount: Amount? = null,         // Tax calculations
)

// Amount structure (from GlossGenius core)
data class Amount(
    val value: BigDecimal,    // Value in smallest unit (cents)
    val currency: Currency    // java.util.Currency
)
```

### JSON Serialization
Use snake_case for all JSON serialization:

```kotlin
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy::class)
data class BookingPayload(
    val bookingToken: BookingToken,
    val businessToken: BusinessToken,
    val scheduledAt: OffsetDateTime,
    val lineItems: List<BookingLineItem> = listOf(),
)
```

### Immutable Collections
All collections must be immutable:

```kotlin
data class Booking(
    val lineItems: List<BookingLineItem> = listOf(),     // ✅ Immutable
    val metadata: Map<String, String> = mapOf(),         // ✅ Immutable
    
    // ❌ Never use MutableList/MutableMap in domain models
)
```

## Store Layer Patterns

### Token-First with GUID Support
Generate both token and GUID methods for backward compatibility:

```kotlin
interface BookingStore {
    // Primary token-based methods
    fun findByToken(token: BookingToken): Booking?
    fun findByTokens(tokens: List<BookingToken>): List<Booking>
    
    // Legacy GUID support methods (optional generation)
    fun findByGuid(guid: UUID): Booking?
    fun findByGuids(guids: List<UUID>): List<Booking>
    
    // Business operations
    fun create(booking: Booking): Booking
    fun update(booking: Booking): Booking
    fun delete(token: BookingToken): Boolean
}
```

### ServiceException Integration
Use factory functions for consistent error handling:

```kotlin
class BookingStore {
    fun findByToken(token: BookingToken): Booking? {
        return try {
            // jOOQ query implementation
            bookingQueries.findByToken(token)?.let { record ->
                bookingConverter.fromRecord(record)
            }
        } catch (exception: Exception) {
            throw newBookingRetrievalError(
                message = "Failed to retrieve booking",
                cause = exception,
                token = token
            )
        }
    }
}
```

## Testing Patterns

### Kotest FreeSpec Structure
Use behavior-driven test organization:

```kotlin
class BookingStoreTest : FreeSpec({
    "findByToken" - {
        "should return booking when found" {
            // Given
            val bookingToken = BookingToken.random()
            val expectedBooking = newTestBooking(token = bookingToken)
            every { mockBookingQueries.findByToken(bookingToken) } returns expectedRecord
            
            // When  
            val result = bookingStore.findByToken(bookingToken)
            
            // Then
            result shouldBe expectedBooking
        }
        
        "should return null when not found" {
            // Given
            val bookingToken = BookingToken.random()
            every { mockBookingQueries.findByToken(bookingToken) } returns null
            
            // When
            val result = bookingStore.findByToken(bookingToken)
            
            // Then
            result shouldBe null
        }
        
        "should throw ServiceException on database error" {
            // Error scenario testing
        }
    }
    
    "create" - {
        "should create booking successfully" {
            // Creation tests
        }
    }
})
```

### MockK Patterns
Use appropriate mock configurations for different dependencies:

```kotlin
// Relaxed mock for logging (non-critical)
val mockLogger = mockk<Logger>(relaxed = true)

// Strict mock for business logic (critical)
val mockBookingQueries = mockk<BookingQueries>()

// Capture arguments for verification
val bookingSlot = slot<Booking>()
every { mockBookingQueries.create(capture(bookingSlot)) } returns savedRecord
```

## Architecture Validation

### ArchUnit Rules
Enforce layer boundaries and naming conventions:

```kotlin
class ArchitectureTest : FreeSpec({
    "architecture rules" - {
        "handlers should only depend on operations or stores" {
            classes()
                .that().resideInAPackage("..handlers..")
                .should().onlyDependOnClassesThat()
                .resideInAnyPackage("..operations..", "..stores..", "..models..", "java..")
        }
        
        "stores should not depend on handlers" {
            classes()
                .that().resideInAPackage("..stores..")
                .should().notDependOnClassesThat()
                .resideInAnyPackage("..handlers..")
        }
    }
})
```

## Quality Standards

### Detekt Configuration
The agent uses the existing project Detekt configuration plus GlossGenius-specific rules:

- **Complexity Analysis**: Cyclomatic complexity limits
- **Code Style**: Consistent formatting and naming
- **Performance**: Avoid common performance anti-patterns
- **Security**: Token handling and data validation

### Test Coverage
- **Minimum 80% line coverage** for all generated code
- **100% coverage for business logic** (operations layer)
- **Comprehensive error scenario testing**
- **Architecture rule validation**

## Database Integration

### jOOQ Patterns
Type-safe database queries with proper error handling:

```kotlin
class BookingQueries(private val dsl: DSLContext) {
    fun findByToken(token: BookingToken): BookingRecord? {
        return dsl.selectFrom(BOOKINGS)
            .where(BOOKINGS.TOKEN.eq(token.value))
            .fetchOne()
    }
}
```

### Liquibase Migrations
Database schema management following project patterns:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
                   http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.8.xsd">
    
    <changeSet id="create-bookings-table" author="core-bookings-agent">
        <createTable tableName="bookings">
            <column name="token" type="varchar(255)">
                <constraints primaryKey="true" nullable="false"/>
            </column>
            <column name="guid" type="uuid">
                <constraints nullable="true"/>  <!-- Legacy support -->
            </column>
            <column name="business_token" type="varchar(255)">
                <constraints nullable="false"/>
            </column>
            <column name="created_at" type="timestamp with time zone"/>
            <column name="updated_at" type="timestamp with time zone"/>
        </createTable>
    </changeSet>
</databaseChangeLog>
```

## Tool Requirements

This specialized agent requires access to:
- **Kotlin 2.2.21** with Java 21 toolchain
- **Gradle build system** with lockfile support
- **jOOQ 3.20.8** code generation and runtime
- **Kotest 5** test framework
- **MockK** mocking library
- **Detekt 1.23.8** static analysis
- **Liquibase** database migrations
- **Micronaut 4.10.0** framework
- **PostgreSQL** database connectivity

## Usage Examples

### Creating a New Feature
```bash
# 1. Create domain model
/cb-domain-model PaymentSchedule

# 2. Create store layer with token + GUID support
/cb-create-store PaymentSchedule --with-guid

# 3. Create operations layer for business logic
/cb-create-operations PaymentScheduling

# 4. Generate comprehensive tests
/cb-testing-suite PaymentScheduleStore
/cb-testing-suite PaymentSchedulingOperations

# 5. Run quality checks
/cb-quality-check --fix
```

### Analyzing Existing Code
```bash
# Analyze architecture compliance
/cb-analyze-architecture com.glossgenius.core.bookings.stores

# Get migration recommendations
/cb-analyze-architecture --migration-plan

# Check specific component
/cb-quality-check BookingStore
```

### Database Operations
```bash
# Create migration for new table
/cb-db-migration create-payment-schedules-table

# Add index for performance
/cb-db-migration --index payment_schedules

# Update gradle lockfiles after dependency changes
/cb-add-dependencies --update-locks
```

## Agent Behavior

### Intelligent Decision Making
- **Architecture Detection**: Automatically detects current vs target patterns
- **Token-First Preference**: Defaults to token-based APIs with GUID option
- **Quality Automation**: Automatically generates tests and applies fixes
- **Convention Enforcement**: Validates all code against project standards

### Error Handling
- **Graceful Degradation**: Falls back to current patterns when target not applicable
- **Clear Error Messages**: Provides actionable feedback for convention violations
- **Context Awareness**: Considers existing codebase patterns in decisions

### Continuous Improvement
- **Pattern Learning**: Adapts to project-specific conventions over time
- **Quality Metrics**: Tracks code quality improvements and coverage
- **Migration Guidance**: Provides step-by-step architecture evolution

This agent bridges the gap between current Core Bookings patterns and GlossGenius best practices, ensuring high-quality, maintainable, and architecturally sound Kotlin code while supporting both legacy and modern patterns seamlessly.

Base directory for this skill: ~/.config/opencode/skills/core-bookings-kotlin-agent
Relative paths in this skill (e.g., scripts/, templates/, reference/) are relative to this base directory.