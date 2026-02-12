# Core Bookings Kotlin Conventions Reference

This document serves as a comprehensive reference for all conventions, standards, and best practices that the Core Bookings Specialized Kotlin Agent follows.

## Project-Specific Conventions

### Package Structure
```
com.glossgenius.core.bookings/
├── configuration/          # Service configuration and constants
├── handlers/rpc/           # RPC handler layer (API boundary)
├── models/                 # Domain entities and error factories
│   └── {feature_group}/    # Grouped domain models
└── stores/                 # Data access and orchestration layer
    └── clients/coreapi/    # External API client implementations
        └── converters/     # Data transformation mappers
```

### Technology Stack
- **Kotlin 2.2.21** with JVM target
- **Java 21** toolchain
- **Micronaut 4.10.0** framework
- **JOOQ 3.20.8** for database access
- **Liquibase** for database migrations
- **Kotest 5** for testing
- **MockK** for mocking
- **Detekt 1.23.8** for static analysis

### Dependency Injection
- Use **Jakarta annotations**: `@Singleton`, `@Named`
- Constructor-based dependency injection preferred
- Micronaut's built-in DI container

### Error Handling
- **Factory functions** for consistent error creation
- **ServiceException/ServiceExceptions** pattern from core-libs
- Comprehensive exception mapping with context

### JSON Serialization
```kotlin
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy::class)
data class BookingPayload(...)
```

### Date/Time Handling
- **OffsetDateTime** for all timestamps
- Timezone-aware date handling
- Audit fields: `createdAt`, `updatedAt`

## GlossGenius Universal Standards

### Domain Models

#### Nullable Token Pattern
```kotlin
data class Booking(
    val nullableToken: BookingToken? = null,    // Service-assigned
    val businessToken: BusinessToken,           // Required multi-tenant
) {
    val token: BookingToken
        get() = nullableToken!!  // Intentionally unsafe - fails fast
}
```

#### Amount Type Usage
```kotlin
data class BookingLineItem(
    val amount: Amount,                    // Required amount
    val discount: Amount? = null,          // Optional amount  
)

// Amount structure (from GlossGenius core)
data class Amount(
    val value: BigDecimal,    // Value in smallest unit (cents)
    val currency: Currency    // java.util.Currency
)
```

#### Immutable Collections
```kotlin
data class Booking(
    val lineItems: List<BookingLineItem> = listOf(),     // ✅ Immutable
    val metadata: Map<String, String> = mapOf(),         // ✅ Immutable
    
    // ❌ Never use MutableList/MutableMap in domain models
)
```

#### Computed Properties
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

#### Business Validation
```kotlin
data class Booking(
    val scheduledAt: OffsetDateTime,
    val duration: Duration,
) {
    init {
        require(scheduledAt.isAfter(OffsetDateTime.now())) {
            "Booking cannot be scheduled in the past"
        }
        require(!duration.isNegative && !duration.isZero) {
            "Duration must be positive"
        }
    }
}
```

### API Design Patterns

#### Token-First with GUID Support
```kotlin
interface BookingStore {
    // Primary token-based methods
    fun findByToken(token: BookingToken): Booking?
    fun findByTokens(tokens: List<BookingToken>): List<Booking>
    
    // Legacy GUID support methods (optional)
    fun findByGuid(guid: UUID): Booking?
    fun findByGuids(guids: List<UUID>): List<Booking>
}
```

#### Client Integration Patterns
```kotlin
// Base client inheritance
class BookingClient : CoreApiBaseClient() {
    fun getBooking(token: BookingToken): BookingResponse? {
        return executeRequest(
            uri = buildUri("/bookings/${token.value}"),
            method = HttpMethod.GET
        )
    }
}

// Converter pattern
class BookingConverter {
    fun fromApiResponse(response: BookingResponse): Booking {
        return Booking(
            nullableToken = BookingToken(response.token),
            businessToken = BusinessToken(response.businessToken),
            // ... field mapping
        )
    }
}
```

## Testing Conventions

### Kotest FreeSpec Structure
```kotlin
class BookingStoreTest : FreeSpec({
    "findByToken" - {
        "should return booking when found" {
            // Given
            val bookingToken = BookingToken.random()
            every { mockBookingStore.findByToken(bookingToken) } returns mockBooking
            
            // When  
            val result = bookingStore.findByToken(bookingToken)
            
            // Then
            result shouldBe mockBooking
        }
        
        "should return null when not found" {
            // Test not found scenario
        }
        
        "should throw ServiceException on database error" {
            // Error scenario testing
        }
    }
})
```

### MockK Patterns
```kotlin
// Relaxed mock for non-critical dependencies (logging)
val mockLogger = mockk<Logger>(relaxed = true)

// Strict mock for critical business logic
val mockBookingStore = mockk<BookingStore>()

// Capture arguments for verification
val bookingSlot = slot<Booking>()
every { mockBookingStore.create(capture(bookingSlot)) } returns savedBooking

// Verify interactions
verify { mockBookingStore.findByToken(expectedToken) }
```

### Test Data Factories
```kotlin
fun newTestBooking(
    token: BookingToken? = BookingToken.random(),
    businessToken: BusinessToken = BusinessToken.random(),
    scheduledAt: OffsetDateTime = OffsetDateTime.now().plusHours(1),
): Booking {
    return Booking(
        nullableToken = token,
        businessToken = businessToken,
        scheduledAt = scheduledAt,
        // ... other defaults
    )
}
```

### Architecture Testing
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

## Database Conventions

### jOOQ Patterns
```kotlin
class BookingQueries(private val dsl: DSLContext) {
    fun findByToken(token: BookingToken): BookingRecord? {
        return dsl.selectFrom(BOOKINGS)
            .where(BOOKINGS.TOKEN.eq(token.value))
            .fetchOne()
    }
    
    fun create(booking: Booking): BookingRecord {
        val record = dsl.newRecord(BOOKINGS)
        // Map booking to record
        return record.also { it.store() }
    }
}
```

### Liquibase Migration Patterns
```xml
<changeSet id="create-bookings-table" author="core-bookings-agent">
    <createTable tableName="bookings">
        <!-- Primary identifier - token-first design -->
        <column name="token" type="varchar(255)">
            <constraints primaryKey="true" nullable="false"/>
        </column>
        
        <!-- Legacy GUID support -->
        <column name="guid" type="uuid">
            <constraints nullable="true" unique="true"/>
        </column>
        
        <!-- Multi-tenant business context -->
        <column name="business_token" type="varchar(255)">
            <constraints nullable="false"/>
        </column>
        
        <!-- Audit timestamps -->
        <column name="created_at" type="timestamp with time zone"/>
        <column name="updated_at" type="timestamp with time zone"/>
    </createTable>
    
    <!-- Performance indexes -->
    <createIndex indexName="idx_bookings_business_token" tableName="bookings">
        <column name="business_token"/>
    </createIndex>
</changeSet>
```

## Architecture Patterns

### Current Pattern (Handler → Store → Client)
```kotlin
// Handler
@Controller("/rpc/bookings")
class BookingHandler(private val bookingStore: BookingStore) {
    fun getBooking(request: GetBookingRequest): Booking? {
        return bookingStore.findByToken(request.token)
    }
}

// Store (combines business logic + data access)
@Singleton
class BookingStore(private val bookingClient: BookingClient) {
    fun findByToken(token: BookingToken): Booking? {
        // Business logic + external API call
        return bookingClient.getBooking(token)?.let { response ->
            // Convert and apply business rules
            convertAndValidate(response)
        }
    }
}
```

### Target Pattern (Handler → Operations → Stores)
```kotlin
// Handler
@Controller("/rpc/bookings")
class BookingHandler(private val bookingOperations: BookingOperations) {
    fun getBooking(request: GetBookingRequest): Booking? {
        return bookingOperations.getBooking(request.token)
    }
}

// Operations (business logic orchestration)
@Singleton
class BookingOperations(private val bookingStore: BookingStore) {
    fun getBooking(token: BookingToken): Booking? {
        // Business logic orchestration
        return bookingStore.findByToken(token)?.let { booking ->
            // Apply business rules, validation, etc.
            validateAndEnrich(booking)
        }
    }
}

// Store (pure data access)
@Singleton
class BookingStore(private val bookingClient: BookingClient) {
    fun findByToken(token: BookingToken): Booking? {
        // Pure data access - no business logic
        return bookingClient.getBooking(token)
    }
}
```

## Code Quality Standards

### Detekt Configuration
- **Complexity limits**: Cyclomatic complexity < 15
- **Method length**: < 30 lines
- **Class length**: < 300 lines
- **Parameter count**: < 6 parameters
- **Naming conventions**: camelCase, PascalCase as appropriate

### Test Coverage Requirements
- **Minimum line coverage**: 80%
- **Business logic coverage**: 100% (operations layer)
- **Error scenario testing**: Comprehensive
- **Architecture rule validation**: Required

### Performance Guidelines
- Use lazy evaluation for expensive computations
- Avoid N+1 query problems with jOOQ
- Proper connection pooling configuration
- Immutable objects reduce memory leaks

## Migration Guidelines

### Current → Target Architecture
1. **Extract business logic** from stores to operations
2. **Create operations layer** for each existing store
3. **Update handlers** to use operations instead of stores directly
4. **Simplify stores** to pure data access
5. **Add architecture tests** to enforce boundaries

### GUID → Token-First Migration
1. **Add token fields** to existing entities
2. **Create token-based methods** alongside GUID methods
3. **Migrate callers** to use token methods
4. **Deprecate GUID methods** (but keep for backward compatibility)
5. **Update tests** to use token patterns

### Testing Migration
1. **Convert to Kotest FreeSpec** from JUnit
2. **Replace Mockito** with MockK
3. **Add test data factories** for consistent data
4. **Create architecture tests** with ArchUnit
5. **Improve coverage** to meet thresholds