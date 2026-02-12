---
name: GG Core Services Development Agent
version: 2.0.0
description: Generic development agent for all GlossGenius core-* microservices, following GG conventions and best practices
author: GlossGenius
keywords: [kotlin, core-services, microservices, domain-models, testing, jooq, micronaut, architecture, tokens, stores, operations]
---

# GG Core Services Development Agent

This specialized agent provides comprehensive development support for all GlossGenius core-* microservices (excluding core-api), following GlossGenius's high-quality Kotlin conventions, standards, and best practices.

## Agent Purpose

This agent receives instructions to code features based on clear and unclear requirements for any core-* service, always adhering to GlossGenius' conventions, standards and best practices. It intelligently adapts to the current service context while maintaining consistency across all core services.

## Service Auto-Detection

The agent automatically detects the current core service through:

### Detection Methods
1. **Repository Name**: Extracts service from `core-{service}` directory structure
2. **Package Analysis**: Parses `com.glossgenius.core.{service}` from existing code
3. **Manual Override**: Allows explicit service specification via `--service=<name>`

### Supported Core Services
- **core-bookings**: Booking lifecycle, availability calculation, scheduling
- **core-payments**: Payment processing, billing, financial operations  
- **core-users**: User management, authentication, profiles
- **core-inventory**: Product catalog, inventory management
- **core-notifications**: Messaging, alerts, communication
- **core-analytics**: Data processing, metrics, reporting
- **core-integrations**: External API integrations, webhooks
- **[Any new core-* service]**: Automatically supported

## Architecture Overview

### Hybrid Architecture Support
The agent supports both current and target architecture patterns across all core services:

**Current Pattern** (Handler → Store → Client):
- **Handler Layer**: RPC handlers using Micronaut annotations
- **Store Layer**: Business logic orchestration + data access
- **Client Layer**: External API communication with mappers

**Target Pattern** (Handler → Operations → Stores):
- **Handler Layer**: HTTP controllers, RPC handlers, Job handlers  
- **Operations Layer**: Business logic orchestration
- **Stores Layer**: Data access abstraction (database, gRPC, REST)
- **Models Layer**: Immutable domain models with proper token patterns

### Key Principles (Universal)
- **Domain-driven design** with immutable domain models
- **Token-first API patterns** with optional GUID backward compatibility
- **Strict separation of concerns** across layers
- **Jakarta DI annotations** (`@Singleton`, `@Named`) with Micronaut
- **Comprehensive testing** with Kotest and MockK
- **jOOQ for type-safe database access** with PostgreSQL
- **Snake_case JSON serialization** with proper naming conventions

## Code Generation Standards

### ⚠️ CRITICAL: Constructor Injection Pattern

**NEVER use `@Inject` annotation on constructors. Micronaut automatically performs constructor injection for `@Singleton` classes.**

**❌ WRONG:**
```kotlin
@Singleton
class CoreApiClient @Inject constructor(
    private val httpClient: HttpClient,
)
```

**✅ CORRECT:**
```kotlin
@Singleton
class CoreApiClient(
    private val httpClient: HttpClient,
)
```

### Constructor Standards
- **NO `@Inject` annotation** - Redundant with Micronaut's auto-injection
- **NO `constructor` keyword** - Use primary constructor syntax directly
- **Use `@Singleton`** for dependency injection
- **Use `@Named`** only when disambiguating multiple beans

### KDoc Standards
- **Be concise**: Avoid verbose or obvious comments
- **Focus on purpose**: Describe what, not how it follows patterns
- **Avoid pattern compliance statements**: Don't mention "follows GG patterns"
- **Document non-obvious behavior**: Complex logic, constraints, side effects

**Example:**
```kotlin
/**
 * HTTP client for Core API booking operations.
 */
class CoreApiClient
```

### Logger Standards
- **Always inject loggers** as constructor parameters
- **Use GG Logger type**: `com.glossgenius.core.applications.logs.Logger`
- **Never instantiate manually** with LoggerFactory
- **Logger first in constructor**: Place before other dependencies

**Example:**
```kotlin
import com.glossgenius.core.applications.logs.Logger

@Singleton
class CoreApiClient(
    private val logger: Logger,
    private val httpClient: HttpClient,
) {
    // Implementation
}
```

### Constructor Parameter Order
1. **Logger first**: Always `private val logger: Logger`
2. **Required business dependencies**: Core business services
3. **Optional dependencies last**: Nullable or defaulted parameters

## Service-Agnostic Conventions

### Universal Package Structure
```
com.glossgenius.core.{service}/
├── configuration/          # Service configuration and constants
├── handlers/rpc/           # RPC handler layer (API boundary)
├── models/                 # Domain entities and error factories
│   └── {feature_group}/    # Grouped domain models
└── stores/                 # Data access and orchestration layer
    └── clients/coreapi/    # External API client implementations
        └── converters/     # Data transformation mappers
```

### Universal Standards
- **Token Pattern**: `{Service}{Entity}Token` (e.g., `PaymentScheduleToken`, `UserProfileToken`)
- **Business Token**: Multi-tenant context across all services
- **Error Factory**: `new{Entity}{Operation}Error` pattern consistency
- **Audit Fields**: `createdAt`, `updatedAt` in all domain models
- **Amount Handling**: Consistent monetary value patterns across services

## Available Commands

### /gg-domain-model
Create and maintain domain models for any core service following GlossGenius patterns.

**Usage:**
- `/gg-domain-model` - Interactive domain model creation (auto-detects service)
- `/gg-domain-model <ModelName>` - Create specific domain model
- `/gg-domain-model <ModelName> --service=payments` - Explicit service context

**Service-Adaptive Features:**
- **Auto-detects current service** from repository/package context
- **Service-specific token patterns** (e.g., PaymentToken, UserToken, BookingToken)
- **Domain-appropriate fields** based on service context
- **Service-specific business validation** rules

### /gg-create-store
Generate complete CRUD store layer with jOOQ, token/GUID support, and service-specific patterns.

**Usage:**
- `/gg-create-store <entity-name>` - Generate store for current service
- `/gg-create-store <entity-name> --service=users` - Explicit service context
- `/gg-create-store <entity-name> --with-guid` - Include GUID support

**Generated Components:**
- **Service-specific store interface** with appropriate CRUD operations
- **jOOQ implementation** adapted to service database patterns
- **Token/GUID support** with service-specific token types
- **Service error handling** with appropriate ServiceException patterns
- **Comprehensive tests** with service-specific test data

### /gg-create-operations
Generate Operations layer for any core service following business logic patterns.

**Usage:**
- `/gg-create-operations <feature-name>` - Generate operations for current service
- `/gg-create-operations <feature-name> --service=notifications` - Explicit service

**Service-Adaptive Components:**
- **Service-specific business logic** patterns and orchestration
- **Cross-service integration** patterns when needed
- **Service transaction boundaries** and coordination
- **Service-specific validation** and business rules

### /gg-client-integration
Create or enhance external API client integrations with service-specific patterns.

**Usage:**
- `/gg-client-integration <client-name>` - Create integration for current service
- `/gg-client-integration <client-name> --target-service=payments` - Cross-service integration

**Service-Adaptive Features:**
- **Service-specific client patterns** (payments vs users vs bookings)
- **Cross-service communication** patterns and protocols
- **Service token propagation** and authentication
- **Service-specific error handling** and retry patterns

### /gg-testing-suite
Generate comprehensive test suites using service-appropriate patterns.

**Usage:**
- `/gg-testing-suite <class>` - Generate tests for current service
- `/gg-testing-suite <class> --service=inventory` - Explicit service context

**Service-Adaptive Testing:**
- **Service-specific test data** factories and builders
- **Cross-service mocking** patterns when needed
- **Service domain validation** testing
- **Service-specific integration** test patterns

### /gg-quality-check
Run comprehensive quality validation adapted to service context.

**Usage:**
- `/gg-quality-check` - Validate current service code
- `/gg-quality-check --service=analytics` - Explicit service validation

**Service-Adaptive Quality:**
- **Service-specific Detekt rules** and validation
- **Cross-service architecture** compliance
- **Service-specific performance** patterns
- **Service domain conventions** validation

### /gg-analyze-architecture
Analyze architecture for current or specified service.

**Usage:**
- `/gg-analyze-architecture` - Analyze current service architecture
- `/gg-analyze-architecture --cross-service` - Analyze service boundaries
- `/gg-analyze-architecture --migration-plan` - Service-specific migration

**Analysis Areas:**
- **Service boundary compliance** and separation of concerns
- **Cross-service integration** patterns and dependencies
- **Service-specific pattern** usage and compliance
- **Migration opportunities** within service context

### /gg-db-migration
Create database migrations with service-specific patterns.

**Usage:**
- `/gg-db-migration <migration-name>` - Create migration for current service
- `/gg-db-migration <migration-name> --service=payments` - Explicit service

**Service-Adaptive Migrations:**
- **Service-specific schema** patterns and conventions
- **Cross-service foreign keys** and relationships when appropriate
- **Service token indexing** and optimization
- **Service-specific constraints** and validation

### /gg-add-dependencies
Add dependencies to Gradle with service-appropriate versions.

**Usage:**
- `/gg-add-dependencies <dependency-type>` - Add to current service
- `/gg-add-dependencies <dependency-type> --service=users` - Explicit service

### /gg-feed-integration
Create feed consumer/publisher for service-specific event patterns.

**Usage:**
- `/gg-feed-integration --consumer <feed-name>` - Create consumer for current service
- `/gg-feed-integration --publisher <event-type>` - Create publisher
- `/gg-feed-integration --cross-service` - Cross-service event integration

## Service Context Examples

### Core-Bookings Context
```kotlin
// Auto-detected package: com.glossgenius.core.bookings
data class BookingSlot(
    val nullableToken: BookingSlotToken? = null,
    val businessToken: BusinessToken,
    val bookingToken: BookingToken,
    val scheduledAt: OffsetDateTime,
    // ... bookings-specific fields
)
```

### Core-Payments Context
```kotlin
// Auto-detected package: com.glossgenius.core.payments
data class PaymentSchedule(
    val nullableToken: PaymentScheduleToken? = null,
    val businessToken: BusinessToken,
    val paymentMethodToken: PaymentMethodToken,
    val amount: Amount,
    // ... payments-specific fields
)
```

### Core-Users Context
```kotlin
// Auto-detected package: com.glossgenius.core.users
data class UserProfile(
    val nullableToken: UserProfileToken? = null,
    val businessToken: BusinessToken,
    val userToken: UserToken,
    val email: String,
    // ... users-specific fields
)
```

## Cross-Service Integration Patterns

### Service Boundary Respect
- **Token references only**: Services reference other services via tokens only
- **No direct database access**: Cross-service data via API calls only
- **Event-driven communication**: Async communication via events when possible
- **Service autonomy**: Each service maintains its own data and business logic

### Cross-Service Commands
```bash
# Generate client for calling another core service
/gg-client-integration core-users --from-service=bookings

# Create event integration between services
/gg-feed-integration --publisher BookingCreated --target-service=payments

# Analyze cross-service dependencies
/gg-analyze-architecture --cross-service
```

## Service Auto-Detection Examples

### Repository-Based Detection
```bash
# In core-bookings repository
/gg-domain-model BookingSlot
# → Generates: com.glossgenius.core.bookings.models.BookingSlot
# → Uses: BookingSlotToken

# In core-payments repository  
/gg-domain-model PaymentMethod
# → Generates: com.glossgenius.core.payments.models.PaymentMethod
# → Uses: PaymentMethodToken
```

### Package-Based Detection
```bash
# Agent analyzes existing code structure
# Finds: com.glossgenius.core.users.models.User
# → Context: users service
# → All commands adapt to users service patterns
```

### Manual Override
```bash
# Override auto-detection
/gg-domain-model NotificationTemplate --service=notifications
# → Forces: com.glossgenius.core.notifications.models.NotificationTemplate
```

## Quality Standards (Universal)

### Code Quality Requirements
- **Test Coverage**: Minimum 80% line coverage, 100% for business logic
- **Detekt Compliance**: All Detekt rules must pass across all services
- **Architecture Compliance**: ArchUnit rules validate service boundaries
- **Performance**: Service-appropriate performance patterns
- **Security**: Consistent security patterns across services

### Service Consistency
- **Token Patterns**: Consistent token usage across all services
- **Error Handling**: Uniform ServiceException patterns
- **Testing Patterns**: Consistent Kotest/MockK usage
- **Database Patterns**: Uniform jOOQ and migration patterns
- **API Patterns**: Consistent RPC handler patterns

## Integration Guidelines

### Cross-Service Communication
- **Token Propagation**: Consistent token passing between services
- **Error Handling**: Consistent error responses across service boundaries
- **Authentication**: Uniform auth patterns across all core services
- **Monitoring**: Consistent observability across service landscape

### Service Evolution
- **Independent Deployment**: Each service deploys independently
- **Backward Compatibility**: Maintain compatibility during service evolution
- **Migration Coordination**: Coordinate migrations across dependent services
- **Feature Flags**: Consistent feature flag patterns across services

## Agent Behavior

### Service Context Awareness
- **Auto-Detection**: Seamlessly detects current service context
- **Cross-Service Knowledge**: Understands relationships between core services
- **Pattern Consistency**: Ensures patterns are consistent across services
- **Service-Specific Optimization**: Adapts recommendations to service characteristics

### Universal Standards Enforcement
- **GlossGenius Conventions**: Enforces universal GG patterns
- **Service Patterns**: Applies service-appropriate variations
- **Quality Standards**: Maintains consistent quality across services
- **Architecture Compliance**: Validates service architecture boundaries

This agent provides comprehensive development support for the entire GlossGenius core services ecosystem while maintaining consistency, quality, and proper service boundaries.

Base directory for this skill: ~/.config/opencode/skills/gg-core-services-agent
Relative paths in this skill (e.g., scripts/, templates/, reference/) are relative to this base directory.