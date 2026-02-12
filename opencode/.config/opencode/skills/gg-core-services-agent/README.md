# GG Core Services Development Agent

## Overview

The GG Core Services Development Agent provides comprehensive, service-agnostic development support for all GlossGenius core-* microservices (excluding core-api). It automatically detects the current service context and adapts all code generation, testing, and quality patterns accordingly.

## Key Innovation: Service Auto-Detection

Unlike the previous core-bookings specific agent, this system automatically detects which core service you're working on and adapts all patterns accordingly.

### Supported Core Services

- **core-bookings**: Booking lifecycle, availability calculation, scheduling
- **core-payments**: Payment processing, billing, financial operations  
- **core-users**: User management, authentication, profiles
- **core-inventory**: Product catalog, inventory management
- **core-notifications**: Messaging, alerts, communication
- **core-analytics**: Data processing, metrics, reporting
- **core-integrations**: External API integrations, webhooks
- **[Any new core-* service]**: Automatically supported

### Auto-Detection Methods

1. **Repository Name**: Extracts service from `core-{service}` directory name
2. **Package Analysis**: Parses `com.glossgenius.core.{service}` from existing code
3. **Manual Override**: `--service=<name>` parameter for explicit context

## Universal Commands (Service-Agnostic)

### Primary Development Commands

#### `/gg-domain-model [ModelName]`
**Auto-adapts to any core service**

**Examples:**
```bash
# In core-bookings repo → generates BookingSlotToken, core.bookings.models package
/gg-domain-model BookingSlot

# In core-payments repo → generates PaymentScheduleToken, core.payments.models package  
/gg-domain-model PaymentSchedule

# In core-users repo → generates UserProfileToken, core.users.models package
/gg-domain-model UserProfile

# Manual override
/gg-domain-model NotificationTemplate --service=notifications
```

#### `/gg-create-store <entity>`
**Generates service-appropriate store layers**

**Examples:**
```bash
# Auto-detects service and generates appropriate patterns
/gg-create-store PaymentSchedule    # → PaymentScheduleStore with payment-specific methods
/gg-create-store UserProfile       # → UserProfileStore with user-specific methods  
/gg-create-store BookingSlot        # → BookingSlotStore with booking-specific methods
```

#### `/gg-create-operations <feature>`
**Creates service-specific business logic operations**

#### `/gg-client-integration <client>`
**Handles both internal service clients and cross-service integration**

#### `/gg-testing-suite <class>`
**Generates service-appropriate test suites with realistic test data**

#### `/gg-quality-check [--fix]`
**Validates code against universal GG standards + service-specific patterns**

#### `/gg-analyze-architecture [--cross-service]`
**Analyzes architecture compliance including service boundaries**

#### `/gg-db-migration <name>`
**Creates database migrations with service-appropriate schemas**

#### `/gg-add-dependencies <type>`
**Manages Gradle dependencies for core services**

#### `/gg-feed-integration [--consumer|--publisher]`
**Event-driven architecture with service context**

## Service Context Examples

### Core Bookings Context
```kotlin
// Auto-generated in core-bookings service
package com.glossgenius.core.bookings.models

data class BookingSlot(
    val nullableToken: BookingSlotToken? = null,      // Service-specific token
    val businessToken: BusinessToken,                 // Universal
    val bookingToken: BookingToken,                   // Service entity reference
    val scheduledAt: OffsetDateTime,                  // Bookings-specific field
    val duration: Duration,                           // Bookings-specific field
    // ... other bookings-specific fields
)
```

### Core Payments Context  
```kotlin
// Auto-generated in core-payments service
package com.glossgenius.core.payments.models

data class PaymentSchedule(
    val nullableToken: PaymentScheduleToken? = null, // Service-specific token
    val businessToken: BusinessToken,                 // Universal
    val paymentMethodToken: PaymentMethodToken,       // Service entity reference
    val amount: Amount,                               // Payments-specific field
    val scheduledAt: OffsetDateTime,                  // Payments-specific field
    // ... other payments-specific fields
)
```

### Core Users Context
```kotlin
// Auto-generated in core-users service
package com.glossgenius.core.users.models

data class UserProfile(
    val nullableToken: UserProfileToken? = null,     // Service-specific token
    val businessToken: BusinessToken,                 // Universal
    val userToken: UserToken,                         // Service entity reference
    val email: String,                                // Users-specific field
    val firstName: String,                            // Users-specific field
    // ... other users-specific fields
)
```

## Cross-Service Integration

### Service Boundary Compliance
The agent enforces proper service boundaries:

- **Token References Only**: Services reference other services via tokens, never direct foreign keys
- **No Direct Database Access**: Cross-service data access via API calls only
- **Event-Driven Communication**: Async communication patterns for service decoupling
- **Service Autonomy**: Each service maintains its own data and business logic

### Cross-Service Examples
```bash
# Generate client for calling another core service
/gg-client-integration core-users --from-service=bookings

# Create event integration between services  
/gg-feed-integration --publisher BookingCreated --target-service=payments

# Analyze cross-service dependencies
/gg-analyze-architecture --cross-service
```

**Generated Cross-Service Code:**
```kotlin
// In core-bookings, referencing payments (proper pattern)
data class BookingPayment(
    val nullableToken: BookingPaymentToken? = null,
    val businessToken: BusinessToken,
    val bookingToken: BookingToken,                   // Own service entity
    val paymentScheduleToken: PaymentScheduleToken,   // Cross-service reference via token only
    // No payment data directly - must use API calls via PaymentScheduleToken
)

// ❌ NEVER: Direct foreign key to payments service database
// ✅ ALWAYS: Token reference + API call pattern
```

## Migration from Core-Bookings Specific Agent

### Command Migration
**Old Core-Bookings Commands** → **New Generic Commands**
- `/cb-domain-model` → `/gg-domain-model` (auto-detects service)
- `/cb-create-store` → `/gg-create-store` (auto-detects service)  
- `/cb-create-operations` → `/gg-create-operations` (auto-detects service)
- `/cb-testing-suite` → `/gg-testing-suite` (auto-detects service)
- `/cb-quality-check` → `/gg-quality-check` (auto-detects service)
- `/cb-analyze-architecture` → `/gg-analyze-architecture` (auto-detects service)

### Backward Compatibility
- **Old commands still work** during transition period
- **Legacy skill remains available** but marked deprecated
- **Gradual migration** - use new commands for new work
- **No breaking changes** to existing workflows

## File Structure

```
~/.config/opencode/skills/gg-core-services-agent/
├── SKILL.md                          # ✅ Main service-agnostic skill definition
├── README.md                         # ✅ This comprehensive guide
├── templates/                        # ✅ Service-agnostic templates
│   ├── domain-model.kt.template      # Auto-adapts to service context
│   ├── store-interface.kt.template   # Service-specific patterns
│   └── operations-interface.kt.template # Service business logic patterns
├── scripts/                          # ✅ Service-aware automation
│   ├── service-detector.py           # Auto-detects current service context
│   ├── quality-check.sh              # Universal quality validation
│   └── architecture-analyzer.py      # Cross-service architecture analysis
└── reference/                        # ✅ Universal conventions
    └── conventions.md                # GG standards for all core services
```

## Benefits of Service-Agnostic Approach

### For Developers
- **One set of commands** works across all core services
- **Automatic context awareness** - no manual service specification needed
- **Consistent patterns** across all core services while respecting service-specific needs
- **Cross-service knowledge** built into the tooling

### For Architecture  
- **Service boundary enforcement** prevents architectural violations
- **Consistent standards** across the entire core services ecosystem
- **Proper service autonomy** while enabling necessary integration
- **Scalable patterns** that support new core services automatically

### For Teams
- **Reduced learning curve** - same commands work everywhere
- **Pattern consistency** across team and services  
- **Knowledge sharing** embedded in tooling
- **Quality assurance** across all core services

## Getting Started

1. **Use in any core-* repository**: Commands automatically detect service context
2. **Start with domain modeling**: `/gg-domain-model YourEntity`
3. **Generate complete layers**: `/gg-create-store YourEntity`
4. **Add business logic**: `/gg-create-operations YourFeature`
5. **Validate quality**: `/gg-quality-check --fix`

The system seamlessly adapts to your current service while maintaining universal GlossGenius quality standards and architectural patterns.

## Advanced Features

### Service Detection Testing
```bash
# Test service detection
~/.config/opencode/skills/gg-core-services-agent/scripts/service-detector.py --json

# Manual service override
/gg-domain-model PaymentMethod --service=payments

# Cross-service analysis
/gg-analyze-architecture --cross-service
```

### Quality Validation
```bash
# Validate service-specific patterns
/gg-quality-check --service-boundaries

# Check cross-service integration compliance  
/gg-analyze-architecture --integration-patterns
```

The GG Core Services Development Agent represents the evolution of specialized tooling into a unified, intelligent system that scales across the entire GlossGenius core services ecosystem! 🚀