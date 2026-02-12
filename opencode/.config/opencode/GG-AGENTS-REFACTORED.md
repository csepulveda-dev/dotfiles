# GG Agent System - Refactored for All Core Services

## 🎯 **Major Refactoring Complete**

The GG Agent System has been successfully refactored from core-bookings specific implementation to a **service-agnostic system** that works with **all GlossGenius core-* microservices** (except core-api).

## ⭐ **Key Innovation: Universal Core Services Support**

### **Before (Core-Bookings Specific)**
```bash
# Only worked in core-bookings repository
/cb-domain-model BookingSlot      # core-bookings only
/cb-create-store BookingSlot      # core-bookings only
```

### **After (Universal Core Services)**
```bash
# Works in ANY core-* repository with auto-detection
/gg-domain-model PaymentSchedule  # Auto-detects core-payments context
/gg-domain-model UserProfile      # Auto-detects core-users context  
/gg-domain-model BookingSlot      # Auto-detects core-bookings context
/gg-domain-model NotificationTemplate --service=notifications  # Manual override
```

## 🔄 **Command Evolution**

### **Command Migration**
| Old (Core-Bookings Only) | New (Universal) | Auto-Detection |
|-------------------------|------------------|----------------|
| `/cb-domain-model` | `/gg-domain-model` | ✅ Service context |
| `/cb-create-store` | `/gg-create-store` | ✅ Service patterns |
| `/cb-create-operations` | `/gg-create-operations` | ✅ Business logic |
| `/cb-client-integration` | `/gg-client-integration` | ✅ Cross-service |
| `/cb-testing-suite` | `/gg-testing-suite` | ✅ Test patterns |
| `/cb-quality-check` | `/gg-quality-check` | ✅ Service validation |
| `/cb-analyze-architecture` | `/gg-analyze-architecture` | ✅ Service boundaries |
| `/cb-db-migration` | `/gg-db-migration` | ✅ Service schemas |
| `/cb-add-dependencies` | `/gg-add-dependencies` | ✅ Service deps |
| `/cb-feed-integration` | `/gg-feed-integration` | ✅ Event patterns |

### **Backward Compatibility**
- ✅ **Old `/cb-*` commands still work** during transition
- ✅ **Legacy skill remains available** but marked deprecated  
- ✅ **No breaking changes** to existing workflows
- ✅ **Gradual migration path** available

## 🧠 **Service Auto-Detection Intelligence**

### **Detection Methods (Priority Order)**
1. **Explicit Override**: `--service=payments` (100% confidence)
2. **Repository Name**: `core-{service}` directory pattern (90% confidence)
3. **Package Analysis**: `com.glossgenius.core.{service}` in code (80% confidence)
4. **Gradle Analysis**: Build file metadata (70% confidence)
5. **Path Analysis**: Any `core-*` in full path (60% confidence)

### **Supported Core Services**
- **core-bookings**: Booking lifecycle, availability, scheduling
- **core-payments**: Payment processing, billing, financial operations  
- **core-users**: User management, authentication, profiles
- **core-inventory**: Product catalog, inventory management
- **core-notifications**: Messaging, alerts, communication
- **core-analytics**: Data processing, metrics, reporting
- **core-integrations**: External API integrations, webhooks
- **core-reviews**: Review management, rating systems
- **core-marketing**: Campaign management, customer engagement
- **core-search**: Search indexing, query processing
- **core-reporting**: Business intelligence, dashboard data
- **[Any new core-* service]**: Automatically supported

## 🏗️ **Service-Adaptive Code Generation**

### **Example 1: Core Payments Service**
```bash
# In core-payments repository
/gg-domain-model PaymentSchedule

# Auto-generates:
package com.glossgenius.core.payments.models

data class PaymentSchedule(
    val nullableToken: PaymentScheduleToken? = null,     // Service-specific token
    val businessToken: BusinessToken,                     // Universal
    val paymentMethodToken: PaymentMethodToken,           // Service entity
    val amount: Amount,                                   // Payments-specific
    val scheduledAt: OffsetDateTime,
    // ... other payments-specific fields
)
```

### **Example 2: Core Users Service**
```bash
# In core-users repository  
/gg-domain-model UserProfile

# Auto-generates:
package com.glossgenius.core.users.models

data class UserProfile(
    val nullableToken: UserProfileToken? = null,         // Service-specific token
    val businessToken: BusinessToken,                     // Universal
    val userToken: UserToken,                             // Service entity
    val email: String,                                    // Users-specific
    val firstName: String,
    // ... other users-specific fields
)
```

### **Example 3: Core Inventory Service**
```bash
# In core-inventory repository
/gg-domain-model Product

# Auto-generates:
package com.glossgenius.core.inventory.models

data class Product(
    val nullableToken: ProductToken? = null,             // Service-specific token
    val businessToken: BusinessToken,                     // Universal
    val productCategoryToken: ProductCategoryToken,       // Service entity
    val name: String,                                     // Inventory-specific
    val sku: String,
    // ... other inventory-specific fields
)
```

## 🔗 **Cross-Service Integration Patterns**

### **Service Boundary Enforcement**
```kotlin
// ✅ CORRECT: Token-only cross-service references
data class BookingPayment(
    val nullableToken: BookingPaymentToken? = null,
    val businessToken: BusinessToken,
    val bookingToken: BookingToken,                       // Own service
    val paymentScheduleToken: PaymentScheduleToken,       // Cross-service via token
    // Use API calls to get payment data via PaymentScheduleToken
)

// ❌ INCORRECT: Direct foreign keys to other services
data class BookingPayment(
    val paymentScheduleId: Long,  // Direct DB reference - violates service boundaries
    val paymentAmount: Amount,    // Data owned by payments service
)
```

### **Cross-Service Commands**
```bash
# Generate client for calling another core service
/gg-client-integration core-users --from-service=bookings

# Create event integration between services
/gg-feed-integration --publisher BookingCreated --target-service=payments

# Analyze cross-service dependencies
/gg-analyze-architecture --cross-service
```

## 📊 **Architecture Compliance**

### **Universal Standards (All Core Services)**
- **Token-first APIs**: Primary token methods with optional GUID support
- **3-layer Architecture**: Handler → Operations → Stores pattern
- **Immutable Domain Models**: All collections are `List`/`Map`, never `Mutable*`
- **Business Token Isolation**: Multi-tenant data separation
- **ServiceException Patterns**: Consistent error handling across services
- **Amount Types**: Monetary values with `BigDecimal` + `Currency`
- **Timezone Awareness**: `OffsetDateTime` for all timestamps
- **Snake_case JSON**: Consistent API serialization

### **Service-Specific Adaptations**
- **Token Naming**: Service-appropriate token types (PaymentToken, UserToken, etc.)
- **Domain Logic**: Service-specific business validation and rules
- **Database Schemas**: Service-appropriate table and index patterns
- **Integration Patterns**: Service-specific external API patterns
- **Event Types**: Service-appropriate domain event definitions

## 🛠️ **Updated Agent System**

### **Agent Capabilities Enhancement**

#### **`gg` - Primary Agent**
- ✅ **Universal service awareness** across all core-* repositories
- ✅ **Intelligent command routing** based on service context
- ✅ **Cross-service knowledge** for integration scenarios
- ✅ **Service boundary validation** and compliance enforcement

#### **`ggplan` - Planning Specialist**  
- ✅ **Multi-service architecture planning** with proper boundaries
- ✅ **Cross-service integration design** patterns and strategies
- ✅ **Service evolution planning** and migration strategies
- ✅ **Universal standards application** across service landscape

#### **`ggbuild` - Implementation Specialist**
- ✅ **Service-adaptive code generation** with context-appropriate patterns
- ✅ **Cross-service client generation** with proper integration patterns
- ✅ **Universal testing patterns** with service-specific test data
- ✅ **Quality validation** across all core services

### **Updated Configuration**
**File**: `~/.config/opencode/opencode.json`

```json
{
  "skills": {
    "core_services": {
      "path": "~/.config/opencode/skills/gg-core-services-agent",
      "commands": [
        "gg-domain-model", "gg-create-store", "gg-create-operations",
        "gg-client-integration", "gg-testing-suite", "gg-quality-check", 
        "gg-analyze-architecture", "gg-db-migration", "gg-add-dependencies",
        "gg-feed-integration"
      ],
      "supports": ["core-bookings", "core-payments", "core-users", "core-inventory",
                   "core-notifications", "core-analytics", "core-integrations"]
    },
    "core_bookings_legacy": {
      "path": "~/.config/opencode/skills/core-bookings-kotlin-agent", 
      "deprecated": true,
      "replacement": "core_services"
    }
  }
}
```

## 📂 **Complete File Structure**

```
~/.config/opencode/
├── opencode.json                     # ✅ Updated with universal core services config
├── GG-AGENTS-REFACTORED.md          # ✅ This refactoring summary
├── agents/
│   ├── gg.md                         # ✅ Updated with universal service awareness
│   ├── ggplan.md                     # ✅ Enhanced with cross-service planning
│   └── ggbuild.md                    # ✅ Enhanced with service-adaptive generation
├── commands/
│   ├── gg-domain-model.md            # ✅ Service-agnostic domain modeling
│   ├── gg-create-store.md            # ✅ Service-adaptive store generation
│   ├── gg-feature.md                 # ✅ Universal feature development
│   ├── gg-analyze.md                 # ✅ Cross-service analysis
│   ├── gg-migrate.md                 # ✅ Universal migration assistance
│   ├── gg-deploy.md                  # ✅ Universal deployment
│   └── [existing commands remain]    # All existing functionality preserved
└── skills/
    ├── gg-core-services-agent/       # ✅ NEW: Universal core services skill
    │   ├── SKILL.md                  # Service-agnostic skill definition
    │   ├── README.md                 # Comprehensive universal guide
    │   ├── templates/                # Service-adaptive templates
    │   ├── scripts/                  # Universal automation + service detection
    │   └── reference/                # Universal conventions guide
    └── core-bookings-kotlin-agent/   # ✅ LEGACY: Maintained for compatibility
        └── [original files preserved] # Backward compatibility
```

## 🚀 **Benefits of Refactoring**

### **For Developers**
- ✅ **One command set** works across all core services
- ✅ **Automatic context detection** - no manual service specification
- ✅ **Consistent patterns** while respecting service-specific needs  
- ✅ **Cross-service integration** knowledge built-in
- ✅ **Reduced learning curve** - same commands everywhere

### **For Architecture**
- ✅ **Service boundary enforcement** prevents architectural violations
- ✅ **Consistent standards** across entire core services ecosystem
- ✅ **Proper service autonomy** with necessary integration patterns
- ✅ **Scalable design** supports new core services automatically
- ✅ **Universal quality** standards with service-appropriate variations

### **For Teams**
- ✅ **Knowledge consistency** across teams and services
- ✅ **Pattern reuse** and shared best practices  
- ✅ **Quality assurance** at ecosystem level
- ✅ **Faster onboarding** to new core services
- ✅ **Cross-service collaboration** support

## ⚡ **Getting Started with Refactored System**

### **Immediate Usage (Any Core Service)**
```bash
# Works in any core-* repository
/gg-domain-model YourEntity           # Auto-detects service context
/gg-create-store YourEntity          # Generates service-appropriate store  
/gg-create-operations YourFeature    # Creates service-specific operations
/gg-quality-check --fix              # Validates universal + service standards
```

### **Cross-Service Development**
```bash
# Analyze service boundaries
/gg-analyze-architecture --cross-service

# Generate cross-service integration
/gg-client-integration core-payments --from-service=bookings

# Validate service autonomy
/gg-quality-check --service-boundaries
```

### **Testing Service Detection**
```bash
# Check current service detection
~/.config/opencode/skills/gg-core-services-agent/scripts/service-detector.py

# Test with explicit override
/gg-domain-model TestEntity --service=notifications
```

## 🎖️ **Refactoring Achievement Summary**

✅ **Universal Core Services Support**: All core-* services (except core-api)  
✅ **Automatic Service Detection**: Intelligent context recognition  
✅ **Service-Adaptive Patterns**: Context-appropriate code generation  
✅ **Cross-Service Integration**: Proper service boundary enforcement  
✅ **Backward Compatibility**: Legacy commands and skills preserved  
✅ **Enhanced Agent Intelligence**: Service-aware planning and implementation  
✅ **Universal Quality Standards**: Consistent excellence across all services  
✅ **Scalable Architecture**: Supports new services automatically  

**The GG Agent System now provides unified, intelligent development assistance across the entire GlossGenius core services ecosystem!** 🚀

This refactoring transforms the system from a single-service tool into a comprehensive platform that scales across all current and future core services while maintaining the highest standards of quality and architectural excellence.

## 🔄 **Migration Path**

1. **Continue using existing workflows** - no immediate changes required
2. **Gradually adopt new `/gg-*` commands** for new development
3. **Test service auto-detection** in different core-* repositories  
4. **Leverage cross-service features** for integration scenarios
5. **Enjoy universal consistency** across all core services

The refactored system represents a significant evolution in development tooling, providing comprehensive support for the entire GlossGenius core services architecture! 🎯