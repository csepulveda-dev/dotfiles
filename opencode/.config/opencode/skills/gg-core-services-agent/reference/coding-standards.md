# GlossGenius Coding Standards

This document defines the specific coding standards that all GG agents must follow when generating code.

## ⚠️ CRITICAL: Constructor Injection Standards

### ❌ **NEVER USE @Inject Annotation**

Micronaut automatically performs constructor injection for `@Singleton` classes. The `@Inject` annotation is **redundant and should NEVER be used**.

**WRONG - Do NOT use this pattern:**
```kotlin
import jakarta.inject.Inject
import jakarta.inject.Singleton

@Singleton
class CoreApiClient @Inject constructor(
    private val httpClient: HttpClient,
) {
    // Implementation
}
```

**CORRECT - Always use this pattern:**
```kotlin
import jakarta.inject.Singleton

@Singleton
class CoreApiClient(
    private val httpClient: HttpClient,
) {
    // Implementation
}
```

### Key Rules for Constructor Injection
1. **NO `@Inject` annotation** - Micronaut handles injection automatically
2. **NO `constructor` keyword** - Use primary constructor syntax directly
3. **Use `@Singleton`** on the class for dependency injection
4. **Use `@Named`** only when disambiguating multiple beans of the same type
5. **ALWAYS use `private val`** - Constructor parameters must be `private val` (not `val` or plain parameters)

### ⚠️ CRITICAL: Always Use `private val` for Constructor Parameters

Constructor parameters **MUST** be declared as `private val` when used in the class. Never use public `val`.

**Exception**: Parameters that are ONLY passed to a parent constructor do not need `private val`.

#### ❌ **WRONG - Plain Parameters (when used in class)**
```kotlin
@Singleton
class MyStore(
    logger: Logger,  // ❌ Missing private val (used in class methods)
    httpClient: HttpClient,  // ❌ Missing private val (used in class methods)
) {
    fun doSomething() {
        logger.info("test")  // Won't compile - logger not accessible
    }
}
```

#### ❌ **WRONG - Public Properties**
```kotlin
@Singleton
class CoreApiClient(
    val logger: Logger,  // ❌ Missing private modifier
    val httpClient: HttpClient,  // ❌ Missing private modifier
) {
    // Exposes internal dependencies publicly
}
```

#### ✅ **CORRECT - Private Val (parameters used in class)**
```kotlin
@Singleton
class MyStore(
    private val logger: Logger,  // ✅ Correct (used in methods)
    @Named("core-api") private val httpClient: HttpClient,  // ✅ Correct (used in methods)
) {
    fun fetchBookings(): List<Booking> {
        logger.debug("Fetching bookings from Core API")
        // Can access both logger and httpClient
    }
}
```

#### ✅ **CORRECT - Plain Parameters (only passed to parent)**
```kotlin
@Singleton
class CoreApiClient(
    @Named("core-api") configuration: HttpClientConfiguration,  // ✅ Correct (only passed to parent)
    requestContext: RequestContext,                              // ✅ Correct (only passed to parent)
    private val logger: Logger,                                  // ✅ Correct (used in class)
) : CoreApiBaseClient(configuration, requestContext) {
    fun getAvailableTimes(): Response {
        logger.debug("Fetching times")  // Logger is accessible
        // configuration and requestContext are NOT accessible (passed to parent)
    }
}
```

### Why `private val`?
1. **Encapsulation**: Dependencies are internal implementation details
2. **Immutability**: `val` prevents reassignment
3. **Accessibility**: Properties are accessible in all class methods
4. **Testability**: Private dependencies can still be mocked in tests

### When Plain Parameters Are OK
Plain parameters (without `private val`) are acceptable ONLY when:
- The parameter is ONLY passed to a parent class constructor
- The parameter is NOT used anywhere in the class body
- Example: CoreApiClient passing `configuration` and `requestContext` to `CoreApiBaseClient`

### Complete Correct Example
```kotlin
package com.glossgenius.core.bookings.clients

import com.glossgenius.core.applications.logs.Logger
import io.micronaut.http.client.HttpClient
import jakarta.inject.Named
import jakarta.inject.Singleton

/**
 * HTTP client for Core API booking operations.
 */
@Singleton
class CoreApiClient(
    private val logger: Logger,
    @Named("core-api") private val httpClient: HttpClient,
) {
    fun fetchBookings(): List<Booking> {
        logger.debug("Fetching bookings from Core API")
        // Implementation
    }
}
```

## ⚠️ CRITICAL: CoreApiClient Pattern

### **ALWAYS Extend CoreApiBaseClient**

When creating a client to interact with core-api, you **MUST** extend `CoreApiBaseClient` from `com.glossgenius.core.libs.clients:core-api`.

### Directory Structure
- **Location**: `stores/clients/coreapi/` (NOT `clients/`)
- **Supporting file**: `CoreApiPayloads.kt` for error response models

### Constructor Pattern (CRITICAL)

```kotlin
@Singleton
class CoreApiClient(
    @Named("core-api") configuration: HttpClientConfiguration,  // 1. FIRST - note: "configuration" not "config"
    requestContext: RequestContext,                              // 2. SECOND
) : CoreApiBaseClient(configuration, requestContext) {
    // Logger is optional and NOT first parameter
}
```

### Key Rules
1. **Constructor order**: `configuration` FIRST, `requestContext` SECOND
2. **Method pattern**: Return `.body()` directly: `call(...).body()`
3. **Use protected methods**: `call()`, `callAdmin()`, or non-blocking variants
4. **Configuration**: `services.http.core-api.url` in application.yml
5. **Dependency**: `implementation("com.glossgenius.core.libs.clients:core-api")`

### Complete Example

```kotlin
package com.glossgenius.core.bookings.stores.clients.coreapi

import com.glossgenius.core.applications.clients.HttpClientConfiguration
import com.glossgenius.core.applications.context.RequestContext
import com.glossgenius.core.clients.coreapi.CoreApiBaseClient
import io.micronaut.http.HttpRequest
import jakarta.inject.Named
import jakarta.inject.Singleton

@Singleton
class CoreApiClient(
    @Named("core-api") configuration: HttpClientConfiguration,
    requestContext: RequestContext,
) : CoreApiBaseClient(configuration, requestContext) {

    fun getAvailableTimes(request: AvailableTimesRequest): AvailableTimesResponse = call(
        HttpRequest.POST(buildUri(), request),
        AvailableTimesResponse::class.java,
        CoreApiErrorResponse::class.java
    ).body()
}
```

### Why CoreApiBaseClient?
- Automatic header propagation (request context, user-ip, user-id, etc.)
- Authentication handling (Bearer token, X-Token for admin)
- HTTP client initialization with timeouts
- Both blocking and non-blocking methods

### ⚠️ CRITICAL: Adding New CoreApiClient Endpoints

When instructed to add a new endpoint to a CoreApiClient, **ALWAYS follow this procedure**:

#### Step 1: Request Access to core-api Repository
```
"To implement this endpoint correctly, I need access to the core-api repository
to analyze the actual implementation. Can you confirm the path to core-api?
(typically ../core-api relative to the current service)"
```

#### Step 2: Confirm the Endpoint Details
Ask the user to confirm:
- Controller name (e.g., `available_times_controller.rb`)
- Action/method name (e.g., `get_available_times_including_resources`)
- HTTP method (GET, POST, PATCH, DELETE)

#### Step 3: Analyze core-api Implementation
Read and analyze:

1. **Controller file**: `../core-api/app/controllers/api/v3/[namespace]/[controller_name].rb`
   - Understand what the endpoint does
   - Check parameter preferences (tokens vs GUIDs)
   - Identify authentication requirements (user vs admin)

2. **Params contract**: `../core-api/app/contracts/params/[namespace]/[action]_params_contract.rb`
   - Understand validation rules
   - Identify required vs optional fields
   - Check for field dependencies

3. **Params schema**: `../core-api/app/schemas/params/[namespace]/[action]_params_schema.rb`
   - Get exact field names and types
   - Understand nested structures
   - Check for transformations (e.g., services_resources)

4. **Routes file**: `../core-api/config/routes.rb`
   - Verify the actual URL path
   - Check if `path: ''` is used (means no action name in URL)
   - Confirm the HTTP method

#### Step 4: Document Findings
Summarize findings before implementation:
```
## Endpoint Analysis: [endpoint_name]

**URL**: POST /api/v3/web/salons/:slug/available_times
**Controller**: Api::V3::Web::AvailableTimesController#get_available_times_including_resources
**Authentication**: User (via Bearer token)

**Required Parameters**:
- provider_business_member_tokens: List<String>
- services_resources: Map<String, List<List<String>>>
- month: String
- year: String

**Optional Parameters**:
- service_tokens: List<String> (preferred over service_guids)
- appointment_token: String (triggers reschedule flow)

**Key Behaviors**:
- Prefers tokens over GUIDs
- Converts service_tokens to GUIDs internally
- Returns paginated availability slots
```

#### Step 5: Implement Based on Analysis
Create models that match the **actual** core-api contract:
- Use exact field names from the schema
- Match required/optional status
- Include all transformations
- Add comments documenting token preferences

#### Example Discovery Process

```kotlin
// ❌ WRONG - Guessing the implementation
fun getAvailableTimes(slug: String): Response {
    return call(
        HttpRequest.GET("/salons/$slug/available_times"),
        Response::class.java
    ).body()
}

// ✅ CORRECT - Based on actual core-api analysis
/**
 * Calls the get_available_times_including_resources endpoint.
 *
 * Route: POST /api/v3/web/salons/:slug/available_times (note: path: '' in routes.rb)
 * Controller: Api::V3::Web::AvailableTimesController#get_available_times_including_resources
 *
 * Prefers tokens over GUIDs (service_tokens > service_guids).
 */
fun getAvailableTimesIncludingResources(
    request: AvailableTimesRequest
): AvailableTimesResponse = call(
    HttpRequest.POST(buildUri(request.slug), request),
    AvailableTimesResponse::class.java,
    CoreApiErrorResponse::class.java
).body()
```

#### Why This Matters
- **Prevents incorrect URLs**: Rails `path: ''` doesn't append action names
- **Ensures correct parameters**: Match exact field names and types
- **Respects token preferences**: Use tokens over GUIDs where supported
- **Handles edge cases**: Transformations, validations, dependencies

## KDoc Standards

### ❌ **Avoid: Overly Verbose/Obvious Comments**
```kotlin
/**
 * HTTP client for interacting with Core API service.
 * 
 * This class follows GlossGenius patterns for external service communication
 * and implements proper error handling, logging, and retry mechanisms
 * following the established patterns for service-to-service communication.
 */
class CoreApiClient
```

### ✅ **Prefer: Concise, Meaningful Documentation**
```kotlin
/**
 * HTTP client for Core API service operations.
 */
class CoreApiClient
```

### KDoc Guidelines
1. **Be concise**: Avoid stating the obvious or repeating class/method names
2. **Focus on purpose**: What does this do, not how it follows patterns
3. **Document non-obvious behavior**: Complex business logic, side effects, constraints
4. **Omit pattern compliance**: Don't mention "follows GG patterns" - code should demonstrate this

### Examples of Good KDoc

#### Classes
```kotlin
/**
 * Manages user authentication tokens and session lifecycle.
 */
class AuthenticationManager

/**
 * Calculates booking availability considering business rules and constraints.
 */
class AvailabilityCalculator

/**
 * Processes payment schedules and handles retry logic for failed transactions.
 */
class PaymentProcessor
```

#### Methods
```kotlin
/**
 * Creates a new booking slot, validating business rules and time conflicts.
 * 
 * @param slot The booking slot to create
 * @return The created slot with assigned token
 * @throws BookingConflictException if slot conflicts with existing bookings
 */
fun createBookingSlot(slot: BookingSlot): BookingSlot

/**
 * Calculates the next payment date based on billing frequency.
 */
fun calculateNextPaymentDate(frequency: BillingFrequency): OffsetDateTime
```

#### Fields (Only When Non-Obvious)
```kotlin
/**
 * Maximum retry attempts for failed API calls.
 */
private val maxRetries: Int = 3

/**
 * Grace period before marking a payment as overdue.
 */
private val gracePeriod: Duration = Duration.ofDays(7)
```

## Logger Standards

### ❌ **Incorrect: Manual Logger Instantiation**
```kotlin
import org.slf4j.LoggerFactory

class CoreApiClient {
    private val logger = LoggerFactory.getLogger(CoreApiClient::class.java)
}
```

### ✅ **Correct: Constructor Injection**
```kotlin
import com.glossgenius.core.applications.logs.Logger

class CoreApiClient(
    private val logger: Logger,
    // ... other dependencies
) {
    // Implementation
}
```

### Logger Injection Guidelines
1. **Always inject loggers** as constructor parameters
2. **Use GG Logger type**: `com.glossgenius.core.applications.logs.Logger`
3. **Never instantiate manually** with LoggerFactory
4. **Include logger in dependency injection** setup

### ⚠️ CRITICAL: Use Lambda-Based Logging Methods

The string-based logging methods are **deprecated**. Always use lambda-based methods for lazy evaluation.

#### ❌ **WRONG - Deprecated String-Based Methods**
```kotlin
// ❌ Deprecated - Do NOT use
logger.info("Fetching booking slot: ${token.value}")
logger.debug("Processing payment: ${payment.id}")
logger.warn("Retry attempt: ${attempt}")
logger.error("Failed to process: ${id}", exception)
```

#### ✅ **CORRECT - Lambda-Based Methods**
```kotlin
// ✅ Correct - Use lambda syntax
logger.info { "Fetching booking slot: ${token.value}" }
logger.debug { "Processing payment: ${payment.id}" }
logger.warn { "Retry attempt: $attempt" }
logger.error(exception) { "Failed to process: $id" }
```

### Why Lambda-Based Logging?
1. **Lazy Evaluation**: Message is only constructed if log level is enabled
2. **Performance**: Avoids string concatenation when logging is disabled
3. **Modern Standard**: Kotlin idiomatic approach
4. **Type Safety**: Better IDE support and compile-time checking

### Error Logging Pattern
For logging with exceptions, the throwable comes **before** the lambda:

```kotlin
// ✅ Correct - Exception before lambda
logger.error(exception) { "Failed to fetch booking slot: ${token.value}" }

// ❌ Wrong - Old deprecated pattern
logger.error("Failed to fetch booking slot: ${token.value}", exception)
```

### Complete Example
```kotlin
package com.glossgenius.core.bookings.stores.clients

import com.glossgenius.core.applications.logs.Logger
import com.glossgenius.core.bookings.models.BookingSlot
import com.glossgenius.core.libs.models.BookingSlotToken
import io.micronaut.context.annotation.Singleton

/**
 * HTTP client for Core API booking operations.
 */
@Singleton
class CoreApiClient(
    private val logger: Logger,
    private val httpClient: HttpClient,
) {

    fun getBookingSlot(token: BookingSlotToken): BookingSlot? {
        logger.debug { "Fetching booking slot: ${token.value}" }

        return try {
            // Implementation
        } catch (exception: Exception) {
            logger.error(exception) { "Failed to fetch booking slot: ${token.value}" }
            throw newBookingSlotRetrievalError(
                message = "Failed to retrieve booking slot",
                cause = exception,
                token = token
            )
        }
    }
}
```

## Import Standards

### Standard Imports for Common Patterns
```kotlin
// Logging
import com.glossgenius.core.applications.logs.Logger

// Domain Models  
import com.glossgenius.core.libs.models.*

// Jakarta DI
import jakarta.inject.Singleton
import jakarta.inject.Named

// Micronaut (when needed)
import io.micronaut.context.annotation.Singleton

// JSON
import com.fasterxml.jackson.databind.PropertyNamingStrategies
import com.fasterxml.jackson.databind.annotation.JsonNaming

// Testing
import io.kotest.core.spec.style.FreeSpec
import io.kotest.matchers.shouldBe
import io.mockk.mockk
import io.mockk.every
import io.mockk.verify
```

## Class Structure Standards

### Constructor Parameter Order

#### For Stores, Operations, and most Services:
```kotlin
class ServiceClass(
    private val logger: Logger,                    // 1. Logger first
    private val requiredDependencies: Type,       // 2. Required business dependencies
    private val optionalDependencies: Type? = null, // 3. Optional dependencies last
) {
    // Implementation
}
```

#### ⚠️ Exception: CoreApiClient (extends CoreApiBaseClient)
```kotlin
@Singleton
class CoreApiClient(
    @Named("core-api") configuration: HttpClientConfiguration,  // 1. FIRST
    requestContext: RequestContext,                              // 2. SECOND
    // Logger is optional and NOT first
) : CoreApiBaseClient(configuration, requestContext) {
    // Implementation
}
```

**Note**: CoreApiClient follows a different pattern because it extends `CoreApiBaseClient` which requires specific parameters.

### Method Organization
```kotlin
class ServiceClass(
    private val logger: Logger,
) {
    // 1. Public business methods first
    fun publicBusinessMethod(): ReturnType { }
    
    // 2. Public utility methods
    fun publicUtilityMethod(): ReturnType { }
    
    // 3. Private helper methods last
    private fun privateHelper(): ReturnType { }
}
```

## Error Handling Standards

### ⚠️ CRITICAL: Use ServiceException with Factory Functions

All domain errors must use `ServiceException` from `com.glossgenius.core.libs.exceptions` with factory functions defined in `models/Exceptions.kt`.

#### ✅ **CORRECT - Exception Factory Functions**

**Create factory functions in `models/Exceptions.kt`:**
```kotlin
package com.glossgenius.core.bookings.models

import com.glossgenius.core.libs.exceptions.ServiceException
import com.glossgenius.protos.common.requests.Requests.ErrorType.ERROR_INTERNAL
import com.glossgenius.protos.common.requests.Requests.ErrorType.ERROR_TYPE_NOT_FOUND

/**
 * @return an error when failing to fetch available times from core-api.
 */
fun newAvailableTimesFetchError(slug: String) = ServiceException(
    type = ERROR_INTERNAL,
    code = "AVAILABLE_TIMES_FETCH_ERROR",
    field = "booking.slug",
    value = slug,
    details = "Failed to fetch available times from core-api for salon: $slug"
)

/**
 * @return an error when the salon is not found in core-api.
 */
fun newSalonNotFoundError(slug: String) = ServiceException(
    type = ERROR_TYPE_NOT_FOUND,
    code = "SALON_NOT_FOUND",
    field = "booking.slug",
    value = slug,
    details = "The salon with slug '$slug' was not found in core-api"
)
```

#### Key Rules for Exception Factories:
1. **Use ErrorType enums** from `com.glossgenius.protos.common.requests.Requests.ErrorType`
2. **Provide error code** - Uppercase with underscores (e.g., "SALON_NOT_FOUND")
3. **Include field and value** - Context for what failed
4. **Clear details message** - Describe what went wrong
5. **NO cause parameter** - ServiceException doesn't accept cause

### ⚠️ CRITICAL: Only Catch Expected Exceptions

**Never catch all exceptions** - let unexpected errors bubble up for debugging.

#### ❌ **WRONG - Catching All Exceptions**
```kotlin
suspend fun getAvailableTimes(request: AvailableTimesRequest): List<Availability> {
    return try {
        val response = coreApiClient.getAvailableTimesIncludingResources(request)
        response.data
    } catch (e: Exception) {  // ❌ Too broad - hides bugs
        logger.error(e) { "Error fetching times" }
        throw newAvailableTimesFetchError(request.slug)
    }
}
```

#### ✅ **CORRECT - Only Catch Expected Exceptions**
```kotlin
suspend fun getAvailableTimesIncludingResources(request: AvailableTimesRequest): List<Availability> {
    logger.info { "Fetching available times for slug: ${request.slug}" }

    return try {
        val response = coreApiClient.getAvailableTimesIncludingResources(request)
        logger.info { "Successfully retrieved ${response.data.size} availability slots" }
        response.data
    } catch (e: HttpClientResponseException) {
        logger.error(e) { "Core API error while fetching available times: ${e.message}" }

        when (e.status) {
            HttpStatus.NOT_FOUND -> throw newSalonNotFoundError(request.slug)
            else -> throw newAvailableTimesFetchError(request.slug)
        }
    }
    // All other exceptions bubble up naturally for debugging
}
```

### Exception Handling Rules

1. ✅ **Catch `HttpClientResponseException`** - Expected errors from core-api calls
2. ✅ **Map HTTP status codes to domain errors** - Use `when` to handle specific statuses
3. ✅ **Let unexpected exceptions propagate** - Don't catch `Exception` or `Throwable`
4. ❌ **Don't catch ServiceException just to re-throw** - Let it bubble up naturally
5. ✅ **Log before throwing** - Always log the error with context
6. ✅ **Include context in logs** - Use structured logging with relevant fields

### Complete Store Error Handling Example

```kotlin
@Singleton
class CoreApiStore(
    private val logger: Logger,
    private val coreApiClient: CoreApiClient
) {
    suspend fun getAvailableTimesIncludingResources(request: AvailableTimesRequest): List<Availability> {
        logger.info { "Fetching available times for slug: ${request.slug}, month: ${request.month}/${request.year}" }

        return try {
            val response = coreApiClient.getAvailableTimesIncludingResources(request)

            logger.info { "Successfully retrieved ${response.data.size} availability slots" }
            response.data
        } catch (e: HttpClientResponseException) {
            logger.error(e) { "Core API error while fetching available times: ${e.message}" }

            when (e.status) {
                HttpStatus.NOT_FOUND -> throw newSalonNotFoundError(request.slug)
                else -> throw newAvailableTimesFetchError(request.slug)
            }
        }
    }
}
```

### Why This Pattern?
- **Debuggability**: Unexpected exceptions surface with full stack traces
- **Visibility**: Edge cases become immediately apparent in monitoring/logs
- **No false confidence**: Don't mask unexpected issues behind generic errors
- **Follows GG standards**: Same approach as core-users, core-catalogs, core-payrolls

### Logging Standards
```kotlin
// Debug: Detailed information for development
logger.debug { "Processing payment: token=$token, amount=$amount" }

// Info: Important business events
logger.info { "Payment processed successfully: token=$token" }

// Warn: Recoverable issues
logger.warn { "Retrying failed payment: token=$token, attempt=$attempt" }

// Error: Exceptions and critical failures (exception comes BEFORE lambda)
logger.error(exception) { "Payment processing failed: token=$token" }
```

## Store Layer Standards

### ⚠️ CRITICAL: Stores Should Not Contain Validation Logic

Stores are **data access layers** and should focus exclusively on data operations. Validation should happen at the operations/endpoint layer.

#### ❌ **WRONG - Validation in Store**
```kotlin
@Singleton
class AvailableTimesStore(
    private val logger: Logger,
    private val coreApiClient: CoreApiClient
) {
    suspend fun getAvailableTimes(request: AvailableTimesRequest): List<Availability> {
        // Implementation
    }

    // ❌ WRONG - Stores should NOT have validation methods
    fun validateRequest(request: AvailableTimesRequest) {
        val errors = mutableListOf<String>()

        if (request.slug.isBlank()) {
            errors.add("Slug cannot be blank")
        }

        if (errors.isNotEmpty()) {
            throw ValidationException(errors.joinToString(", "))
        }
    }
}
```

#### ✅ **CORRECT - Store Focuses on Data Operations**
```kotlin
@Singleton
class CoreApiStore(
    private val logger: Logger,
    private val coreApiClient: CoreApiClient
) {
    /**
     * Retrieves available times from core-api.
     */
    suspend fun getAvailableTimesIncludingResources(request: AvailableTimesRequest): List<Availability> {
        logger.info { "Fetching available times for slug: ${request.slug}" }

        return try {
            val response = coreApiClient.getAvailableTimesIncludingResources(request)
            logger.info { "Successfully retrieved ${response.data.size} availability slots" }
            response.data
        } catch (e: HttpClientResponseException) {
            logger.error(e) { "Core API error: ${e.message}" }

            when (e.status) {
                HttpStatus.NOT_FOUND -> throw newSalonNotFoundError(request.slug)
                else -> throw newAvailableTimesFetchError(request.slug)
            }
        }
    }
}
```

### Store Responsibilities
Stores should **ONLY**:
1. ✅ Retrieve data from external services or databases
2. ✅ Transform data between external and domain models
3. ✅ Handle errors from downstream dependencies
4. ✅ Log data operations

Stores should **NEVER**:
1. ❌ Validate request parameters
2. ❌ Contain business logic
3. ❌ Orchestrate multiple operations
4. ❌ Make business decisions

### Where Validation Belongs
- **Operations Layer**: Business validation, orchestration, workflows
- **Endpoint Layer**: HTTP request validation, parameter parsing
- **Domain Models**: Type constraints, invariants
- **NOT in Stores**: Stores trust their callers

### Error Handling in Stores
Stores should:
- Catch exceptions from downstream dependencies
- Convert to domain-specific exceptions
- Include relevant context (tokens, IDs, etc.)
- Log errors with appropriate levels

```kotlin
suspend fun getBooking(token: BookingToken): Booking {
    return try {
        coreApiClient.getBooking(token)
    } catch (e: CoreApiException) {
        logger.error(e) { "Failed to fetch booking: token=${token.value}" }
        throw BookingStoreException(
            "Failed to fetch booking from core-api: ${e.message}",
            e.statusCode,
            e
        )
    }
}
```

## Testing Standards

### ⚠️ CRITICAL: Do NOT Use Deep Mocking

**Never mock internal protected methods** of base classes or internal implementation details.

#### ❌ **WRONG - Deep Mocking Internal Methods**
```kotlin
class CoreApiClientTest : FreeSpec({
    "should make HTTP request" {
        val client = spyk(CoreApiClient(config, requestContext))
        val mockResponse = mockk<HttpResponse<*>>()

        // ❌ WRONG - Mocking internal protected method
        every {
            client["call"](any(), any<Class<*>>(), any<Class<*>>())
        } returns mockResponse

        client.getAvailableTimes(request)
    }
})
```

**Why This Is Wrong:**
- Mocking internal methods couples tests to implementation details
- Breaks when refactoring internal behavior
- Doesn't test actual HTTP behavior
- Fragile and hard to maintain

#### ✅ **CORRECT - Integration Tests with WireMock**
```kotlin
@MicronautTest
@Property(name = "services.http.core-api.url", value = "http://localhost:1080/")
class CoreApiClientTest(
    @Named("core-api") val configuration: HttpClientConfiguration,
    private val objectMapper: ObjectMapper,
) : FreeSpec({

    val wireMockServer = WireMockHttpServer.create()

    beforeSpec {
        wireMockServer.start()
    }

    afterSpec {
        wireMockServer.stop()
    }

    "getAvailableTimes" - {
        "should make POST request and parse response" {
            wireMockServer.stub(
                method = HttpMethod.POST,
                urlPath = "/api/v3/web/salons/my-salon/available_times",
                responseBody = """
                    {
                        "data": [
                            {"id": "avail-1", "start_time": "2024-01-01T10:00:00Z"}
                        ]
                    }
                """.trimIndent(),
                statusCode = 200
            )

            val client = CoreApiClient(configuration, RequestContext())
            val request = AvailableTimesRequest(slug = "my-salon", ...)

            val response = client.getAvailableTimesIncludingResources(request)

            response.data.size shouldBe 1
            response.data[0].id shouldBe "avail-1"
        }
    }
})
```

#### ✅ **CORRECT - Unit Tests Mock at Public Interface**
```kotlin
class AvailableTimesStoreTest : FreeSpec({

    lateinit var logger: Logger
    lateinit var coreApiClient: CoreApiClient  // Mock the PUBLIC interface
    lateinit var store: AvailableTimesStore

    beforeEach {
        logger = mockk(relaxed = true)
        coreApiClient = mockk()  // ✅ Mock the whole client, not internal methods
        store = AvailableTimesStore(logger, coreApiClient)
    }

    "getAvailableTimes" - {
        "should return availabilities from client" {
            val request = AvailableTimesFactories.availableTimesRequest()
            val expectedResponse = AvailableTimesFactories.availableTimesResponse()

            // ✅ Mock the public method
            coEvery {
                coreApiClient.getAvailableTimesIncludingResources(request)
            } returns expectedResponse

            runBlocking {
                val result = store.getAvailableTimes(request)
                result shouldBe expectedResponse.data
            }
        }
    }
})
```

### Test Class Structure
```kotlin
class ServiceClassTest : FreeSpec({
    val mockLogger = mockk<Logger>(relaxed = true)  // Relaxed logger
    val mockDependency = mockk<Dependency>()        // Strict business mocks

    val service = ServiceClass(mockLogger, mockDependency)

    "methodName" - {
        "should do expected behavior" {
            // Test implementation
        }

        "should handle error conditions" {
            // Error testing
        }
    }
})
```

### Testing Guidelines

1. **Unit Tests**: Mock dependencies at public interface level
   - Mock entire client classes, not their internal methods
   - Test business logic and error handling
   - Use factories for test data

2. **Integration Tests**: Use WireMock or test containers
   - Test actual HTTP behavior
   - Verify request/response serialization
   - Test error scenarios (4xx, 5xx responses)

3. **Avoid**:
   - ❌ Mocking internal protected methods (`client["call"]`)
   - ❌ Mocking base class methods
   - ❌ Testing implementation details
   - ❌ Complex test setup with spies and deep mocking

### Test Data Factory Standards
```kotlin
/**
 * Creates a test booking slot with realistic defaults.
 */
fun newTestBookingSlot(
    token: BookingSlotToken? = BookingSlotToken.random(),
    businessToken: BusinessToken = BusinessToken.random(),
    scheduledAt: OffsetDateTime = OffsetDateTime.now().plusHours(1),
): BookingSlot {
    return BookingSlot(
        nullableToken = token,
        businessToken = businessToken,
        scheduledAt = scheduledAt,
    )
}
```

## Token vs GUID Standards

### ⚠️ **ALWAYS Prefer Tokens Over GUIDs**

When interacting with core-api or working in core-services, **always prefer tokens over GUIDs**.

### Why Tokens?
- **Tokens are the modern standard** for entity identification in GG systems
- **GUIDs are legacy** and maintained only for backward compatibility
- **Tokens provide better consistency** across microservices
- **Core-API prefers tokens** and converts them internally when needed

### Examples of Token Preference

#### ✅ Correct - Using Tokens
```kotlin
data class AvailableTimesRequest(
    @JsonProperty("provider_business_member_tokens")
    val providerBusinessMemberTokens: List<String>,  // ✅ Tokens

    @JsonProperty("service_tokens")
    val serviceTokens: List<String>? = null,  // ✅ Tokens (preferred)

    @JsonProperty("appointment_token")
    val appointmentToken: String? = null,  // ✅ Token
)
```

#### ❌ Wrong - Using GUIDs as Primary
```kotlin
data class AvailableTimesRequest(
    @JsonProperty("provider_guids")
    val providerGuids: List<String>,  // ❌ GUIDs (legacy)

    @JsonProperty("service_guids")
    val serviceGuids: List<String>,  // ❌ GUIDs (use only as fallback)

    @JsonProperty("appointment_guid")
    val appointmentGuid: String? = null,  // ❌ GUID
)
```

### Token Field Naming Pattern
- **Business members**: `business_member_token` or `space_member_token`
- **Services**: `service_token` or `catalog_item_token`
- **Appointments**: `appointment_token`
- **Locations**: `location_token`
- **Resources**: `resource_token`

### When GUIDs Are Acceptable
GUIDs should only be used as **fallback options** when:
1. Working with legacy systems that don't support tokens
2. Maintaining backward compatibility
3. Internal core-api operations that require GUIDs

Always document why GUIDs are used:
```kotlin
/**
 * Service GUIDs (legacy, prefer service_tokens).
 * Only use when tokens are unavailable.
 */
@JsonProperty("service_guids")
val serviceGuids: List<String>? = null
```

## Build Dependencies

### Micronaut Serialization (Required for @Serdeable)

When using `@Serdeable` annotations in payload models (especially `CoreApiPayloads.kt`), you **MUST** include these dependencies:

```gradle
dependencies {
    // Micronaut Serialization - Required for @Serdeable annotations
    kapt("io.micronaut.serde:micronaut-serde-processor")
    implementation("io.micronaut.serde:micronaut-serde-jackson")

    // Other dependencies...
}
```

### When These Are Required
- Using `@Serdeable` annotation on data classes
- Creating `CoreApiPayloads.kt` with error response models
- Any JSON serialization with Micronaut Serde

### Example Payload Using @Serdeable
```kotlin
package com.glossgenius.core.bookings.stores.clients.coreapi

import com.fasterxml.jackson.databind.PropertyNamingStrategies
import com.fasterxml.jackson.databind.annotation.JsonNaming
import io.micronaut.serde.annotation.Serdeable  // Requires micronaut-serde-jackson

@Serdeable
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy::class)
data class CoreApiErrorResponse(
    val errors: List<CoreApiError>
)

@Serdeable
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy::class)
data class CoreApiError(
    val type: String,
    val message: String
)
```

### Build Configuration Checklist
When setting up a new core-service or adding CoreApiClient:

1. ✅ Add `com.glossgenius.core.libs.clients:core-api` dependency
2. ✅ Add Micronaut Serialization dependencies (kapt + implementation)
3. ✅ Configure `services.http.core-api.url` in application.yml
4. ✅ Update dependency lockfile: `./gradlew dependencies --write-locks`

## Code Generation Rules

When generating code, agents must:

1. **Use `private val` for constructor parameters used in class** - Exception: plain parameters OK when only passed to parent constructor
2. **Use concise KDoc** - Focus on purpose, not pattern compliance
3. **Inject loggers** - Never instantiate with LoggerFactory
4. **Use GG Logger import** - `com.glossgenius.core.applications.logs.Logger`
5. **Use lambda-based logging** - `logger.info { "msg" }` NOT `logger.info("msg")` (deprecated)
6. **Follow constructor order** - Logger first (except CoreApiClient), required deps, optional deps
7. **Prefer tokens over GUIDs** - Always use tokens when available
8. **Include meaningful error context** - Relevant tokens, amounts, etc. in error messages
9. **Use relaxed logger mocks** - `mockk<Logger>(relaxed = true)` in tests
10. **Generate realistic test data** - Avoid hardcoded test values when possible
11. **Analyze core-api before implementing** - Always inspect actual endpoints before adding to CoreApiClient
12. **Stores have no validation** - Never add validation methods to stores
13. **No deep mocking in tests** - Never mock internal protected methods; use WireMock for HTTP client tests
14. **Include Micronaut Serde dependencies** - Required when using `@Serdeable` annotations
15. **Use ServiceException with factory functions** - Never create custom exception classes; use factory functions in models/Exceptions.kt
16. **Only catch expected exceptions** - Catch HttpClientResponseException; let unexpected exceptions bubble up for debugging

### Special Rule: CoreApiClient Endpoints

When adding endpoints to CoreApiClient, **NEVER guess the implementation**. Always:
1. Request access to core-api repository
2. Analyze controller, params contract, schema, and routes
3. Document findings before implementation
4. Match exact field names, types, and URL paths
5. Document token preferences and special behaviors

### Special Rule: Store Layer

Stores are **data access only**. When implementing stores:
1. ✅ Focus on data retrieval and transformation
2. ✅ Handle errors from downstream dependencies
3. ✅ Log data operations
4. ❌ Never add validation methods
5. ❌ Never include business logic
6. ❌ Never orchestrate multiple operations

Validation belongs in the **operations layer**, not stores.

### Special Rule: Testing

When writing tests for clients extending base classes:
1. ✅ Use WireMock for HTTP integration tests (like core-users)
2. ✅ Mock at the public interface level in unit tests
3. ❌ Never mock internal protected methods (`client["call"]`)
4. ❌ Never use spies to mock parent class methods

Tests should verify behavior, not implementation details.

### Special Rule: Error Handling

When handling errors in stores and operations:
1. ✅ Use `ServiceException` with factory functions from `models/Exceptions.kt`
2. ✅ Only catch `HttpClientResponseException` (expected errors from core-api)
3. ✅ Map HTTP status codes to domain errors with `when` expression
4. ✅ Log errors before throwing with structured context
5. ❌ Never catch all exceptions (`Exception`, `Throwable`)
6. ❌ Never catch `ServiceException` just to re-throw it
7. ❌ Never create custom exception classes (use ServiceException)

**Rationale**: Unexpected exceptions should bubble up with full stack traces for debugging. Only handle errors you expect and can recover from or provide better context for.

These standards ensure consistency, maintainability, and proper integration with GlossGenius infrastructure.