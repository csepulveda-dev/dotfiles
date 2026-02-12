# GG Agent System - Complete Implementation

## Overview

The GG Agent System provides comprehensive GlossGenius development assistance through three specialized agents that work alongside existing OpenCode Build and Plan agents.

## Agent Architecture

### 🎯 **gg** - Primary Development Assistant
**File**: `~/.config/opencode/agents/gg.md`
**Role**: Intelligent coordinator and general development assistant

**Key Features:**
- **Intelligent Request Routing**: Analyzes requests and recommends `ggplan` or `ggbuild` when appropriate
- **Command Conflict Resolution**: Handles overlapping commands between skills with user clarification
- **Skill Integration**: Direct access to all 10+ Core Bookings commands and GG skills
- **Quality Enforcement**: Built-in GlossGenius standards validation
- **Cross-cutting Concerns**: Code reviews, guidance, and skill coordination

**When to Use:**
- General development questions and guidance
- When unsure whether planning or implementation is needed
- Command conflicts and skill coordination
- Code reviews and quality checks
- Multi-phase tasks requiring both planning and implementation

### 📋 **ggplan** - Planning & Architecture Specialist
**File**: `~/.config/opencode/agents/ggplan.md`
**Role**: Strategic technical planning and architecture decisions

**Key Features:**
- **Architecture Analysis**: Comprehensive system design and pattern analysis
- **Technical Specifications**: Detailed feature specifications and ADRs
- **Migration Planning**: Step-by-step migration strategies
- **Requirements Analysis**: Breaking down complex features
- **Risk Assessment**: Technical risk identification and mitigation

**When to Use:**
- Complex architectural decisions
- Technical specification creation
- Requirements analysis and clarification
- Migration strategy development
- System design and planning

### 🔨 **ggbuild** - Implementation & Build Specialist
**File**: `~/.config/opencode/agents/ggbuild.md`
**Role**: High-quality code generation and deployment

**Key Features:**
- **Code Generation**: Complete feature implementation with GG patterns
- **Test Suite Creation**: Comprehensive Kotest/MockK test generation
- **Quality Assurance**: Automated quality checks and fixes
- **Build Optimization**: Gradle and CI/CD pipeline optimization
- **Deployment Management**: Safe deployment procedures with rollback

**When to Use:**
- Focused implementation tasks
- Test generation and validation
- Build optimization and troubleshooting
- Deployment pipeline work
- Performance optimization

## Unified Commands

### High-Level Development Commands

#### `/gg-feature <feature-name>`
**File**: `~/.config/opencode/commands/gg-feature.md`
**Purpose**: End-to-end feature development workflow

**Workflow:**
1. **Planning Phase** (via ggplan): Requirements analysis, architecture design, technical specs
2. **Implementation Phase** (via ggbuild): Domain models, store layers, operations, handlers, tests
3. **Integration Phase**: Database migrations, API docs, performance validation

**Options:**
- `--planning-only`: Only perform planning phase
- `--implementation-only`: Skip planning, implement from specs
- `--with-migration`: Include database migration planning/creation
- `--with-integration`: Include external API integration

#### `/gg-analyze [scope]`
**File**: `~/.config/opencode/commands/gg-analyze.md`
**Purpose**: Comprehensive codebase analysis

**Analysis Areas:**
- **Architecture Compliance**: Layer separation, pattern compliance, token usage
- **Code Quality**: Detekt analysis, test coverage, performance patterns
- **Migration Opportunities**: Current→Target patterns, technology upgrades

**Options:**
- `--architecture-only`: Focus on architecture compliance
- `--quality-only`: Focus on code quality assessment
- `--migration-plan`: Generate step-by-step migration recommendations

#### `/gg-migrate <from> <to>`
**File**: `~/.config/opencode/commands/gg-migrate.md`
**Purpose**: Guided migration between patterns and technologies

**Migration Types:**
- **Architecture**: Handler→Store→Client to Handler→Operations→Stores
- **APIs**: GUID-only to Token-first with GUID support
- **Testing**: JUnit+Mockito to Kotest+MockK
- **Technology**: Framework and dependency upgrades

**Options:**
- `--analyze-only`: Analyze migration requirements only
- `--dry-run`: Show changes without executing
- `--phase=<number>`: Execute specific migration phase
- `--rollback`: Rollback to previous state

#### `/gg-deploy <environment>`
**File**: `~/.config/opencode/commands/gg-deploy.md`
**Purpose**: Safe and reliable deployment assistance

**Environments:** dev, qa, staging, prod
**Strategies:** blue-green, rolling, canary, hotfix

**Features:**
- **Safety Checks**: Automated tests, quality gates, security scanning
- **Confirmation Points**: Manual approval for critical changes
- **Rollback Capabilities**: Automatic and manual rollback procedures
- **Monitoring Integration**: Health checks and performance validation

## Core Bookings Specialized Commands

All commands from the Core Bookings Specialized Kotlin Agent are available:

### Domain & Store Operations
- `/cb-domain-model [ModelName]` - Create domain models with GG patterns
- `/cb-create-store <entity> [--with-guid]` - Generate complete store layer
- `/cb-create-operations <feature>` - Create operations layer for business logic
- `/cb-client-integration <client>` - External API client integrations

### Testing & Quality
- `/cb-testing-suite <class>` - Generate comprehensive test suites
- `/cb-quality-check [--fix]` - Run quality validation and fixes
- `/cb-analyze-architecture [--migration-plan]` - Architecture compliance analysis

### Database & Infrastructure
- `/cb-db-migration <name>` - Create Liquibase migrations
- `/cb-add-dependencies <type>` - Manage Gradle dependencies
- `/cb-feed-integration [--consumer|--publisher]` - Event-driven architecture

## Agent Behavior & Integration

### Request Routing Logic

The **gg** agent analyzes incoming requests and routes appropriately:

**Planning Keywords** → Recommend `ggplan`:
- "architecture", "design", "plan", "strategy"
- "requirements", "specification", "analysis"
- "evaluate", "assess", "review architecture"
- "migration planning", "technical decisions"

**Implementation Keywords** → Recommend `ggbuild`:
- "implement", "code", "build", "create"
- "test", "deploy", "fix", "generate"
- "refactor", "optimize", "debug"

**Hybrid/Complex Tasks** → Handle in `gg` or coordinate between agents

### Command Conflict Resolution

When multiple skills provide similar commands:
1. **Identify conflicts** and present options to user
2. **Ask for clarification** on preferred implementation
3. **Explain differences** between available options
4. **Remember user preferences** for future decisions

**Example:**
```
I found multiple commands for creating domain models:
1. /cb-domain-model - Core Bookings specific (token-first, ServiceException patterns)
2. /kotlin-domain-model - General Kotlin (GlossGenius universal patterns)

Which would you prefer? I can also explain the differences if helpful.
```

### Integration Guidelines

#### Existing Tool Integration
- **JIRA**: Available but requires user confirmation before actions
- **Git Operations**: Can suggest workflows but ask before executing
- **Build Systems**: Can analyze and suggest improvements but confirm before changes
- **CI/CD Pipelines**: Review and recommend but don't modify without permission

#### Confirmation Requirements
Always ask for user confirmation before:
- Making changes to build configurations
- Creating JIRA tickets or updating existing ones
- Modifying CI/CD pipeline files
- Making git commits or pushes
- Deploying to any environment
- Installing or updating dependencies

## Configuration

### OpenCode Configuration
**File**: `~/.config/opencode/opencode.json`

```json
{
  "agents": {
    "gg": {
      "description": "Primary GlossGenius development assistant",
      "mode": "primary",
      "capabilities": ["planning", "implementation", "analysis", "coordination"]
    },
    "ggplan": {
      "description": "GlossGenius planning and architecture specialist",
      "mode": "planning", 
      "capabilities": ["architecture", "requirements", "technical_specs", "migration_planning"]
    },
    "ggbuild": {
      "description": "GlossGenius implementation and build specialist",
      "mode": "implementation",
      "capabilities": ["code_generation", "testing", "deployment", "quality_assurance"]
    }
  },
  "skills": {
    "core_bookings": {
      "path": "~/.config/opencode/skills/core-bookings-kotlin-agent",
      "commands": [
        "cb-domain-model", "cb-create-store", "cb-create-operations",
        "cb-client-integration", "cb-testing-suite", "cb-quality-check",
        "cb-analyze-architecture", "cb-db-migration", "cb-add-dependencies",
        "cb-feed-integration"
      ]
    }
  }
}
```

## Usage Examples

### Feature Development Workflow
```
User: "I need to create a new payment scheduling feature"

gg Response: "I can help you create a payment scheduling feature following GG patterns. This is a comprehensive task that benefits from both planning and implementation.

Would you like me to:
1. Start with architecture planning (I recommend `ggplan` for this)
2. Jump into implementation (I can coordinate with `ggbuild`) 
3. Handle it end-to-end here with step-by-step guidance

I have access to Core Bookings patterns and can generate domain models, stores, operations, and tests."
```

### Architecture Analysis
```
User: "Review our current booking system architecture"

gg Response: "I'll analyze your booking system architecture. Since this is primarily analysis, I recommend using `ggplan` which specializes in architectural review, but I can start the initial analysis here.

Let me examine your current codebase structure and provide detailed findings."
```

### Code Quality Issues  
```
User: "Fix the failing tests in BookingStore"

ggbuild Response: "I'll help fix the failing BookingStore tests. Let me:

1. **Analyze the failing tests** and identify root causes
2. **Review test patterns** against GG standards (Kotest FreeSpec, MockK)
3. **Fix the issues** following proper testing conventions
4. **Validate the fixes** with comprehensive test execution

Proceeding with analysis..."
```

## File Structure

```
~/.config/opencode/
├── opencode.json                     # Updated with agent configurations
├── agents/
│   ├── gg-review.md                  # Existing GG PR review agent
│   ├── gg.md                         # ✅ Primary GG development assistant
│   ├── ggplan.md                     # ✅ Planning & architecture specialist  
│   └── ggbuild.md                    # ✅ Implementation & build specialist
├── commands/
│   ├── gg-feature.md                 # ✅ End-to-end feature development
│   ├── gg-analyze.md                 # ✅ Comprehensive codebase analysis
│   ├── gg-migrate.md                 # ✅ Migration assistance
│   ├── gg-deploy.md                  # ✅ Deployment management
│   ├── [existing commands...]        # All existing commands remain
└── skills/
    └── core-bookings-kotlin-agent/   # ✅ Specialized Core Bookings skill
        ├── SKILL.md                  # Main skill definition
        ├── templates/                # Code generation templates
        ├── scripts/                  # Quality and analysis tools
        └── reference/                # Conventions documentation
```

## Benefits

### For Developers
- **Unified Interface**: Single `gg` command for most development tasks
- **Intelligent Routing**: Automatic recommendation of specialized agents
- **Comprehensive Coverage**: Planning through deployment support
- **Quality Focus**: Built-in GG standards enforcement
- **Reduced Complexity**: Simplified command structure with powerful capabilities

### For Teams
- **Consistent Patterns**: Enforced GlossGenius conventions
- **Knowledge Sharing**: Embedded best practices and patterns
- **Quality Assurance**: Automated quality checks and validation
- **Productivity**: Faster development cycles with comprehensive tooling
- **Maintainability**: Clean, well-tested, documented code generation

### For Architecture
- **Pattern Evolution**: Smooth migration between architecture patterns
- **Compliance**: Automated architecture validation and enforcement
- **Documentation**: Auto-generated technical specifications and ADRs
- **Risk Management**: Built-in risk assessment and mitigation
- **Scalability**: Support for complex, multi-service architectures

## Getting Started

1. **Start with `gg`**: Use the main agent for general development assistance
2. **Try unified commands**: Use `/gg-feature`, `/gg-analyze`, etc. for complex workflows
3. **Leverage specialization**: Use `ggplan` for planning, `ggbuild` for implementation when needed
4. **Explore Core Bookings commands**: Try `/cb-*` commands for specialized development
5. **Customize preferences**: Let the system learn your preferences for command conflicts

The GG Agent System is ready to accelerate your GlossGenius development with intelligent assistance, comprehensive tooling, and unwavering focus on quality! 🚀