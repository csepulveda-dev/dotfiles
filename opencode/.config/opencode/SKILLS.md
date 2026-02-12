# OpenCode Skills - GlossGenius Development Tools

This document provides a comprehensive overview of all available skills in your OpenCode configuration.

## Available Skills

### 🔧 **Protobuf Development Tools** (`protobuf-dev-tools/`)
**Version**: 1.1.0 | **Converted from**: `core-protos` Claude plugin

**Commands:**
- `/protobuf-new` - Create new protobuf methods, messages, or services
- `/protobuf-new-token` - Create resource token prefixes with Kotlin integration  
- `/protobuf-improve-docs` - Review and improve protobuf documentation

**Use Cases:**
- Creating new gRPC service methods
- Adding message definitions with proper validation
- Managing token types with full Kotlin integration
- Improving protobuf documentation quality

---

### 🚀 **Git Workflow Tools** (`git-workflow-tools/`)
**Version**: 1.5.0 | **Converted from**: `git` Claude plugin

**Commands:**
- `/git-commit` - AI-powered commit creation with conventional format (**NO AI attribution**)
- `/git-commit-push-pr` - Full workflow: commit + push + PR creation
- `/git-push-and-pr` - Push existing commits and create PR
- `/git-auto-review` - Automated code review with security focus
- `/git-create-worktree` - Git worktree automation for parallel development
- `/git-rebase-from-main` - Safe rebasing with conflict resolution
- `/git-core-services-reviewer` - Specialized Kotlin/Java architecture compliance review

**Critical Features:**
- **Clean Commits**: Absolutely NO AI attributions in commit messages (strict requirement)
- **Conventional Commits**: Automatic `[TICKET-ID] type(scope): description` format
- **PR Automation**: AI-generated PR descriptions with technical context
- **Security Review**: Automated vulnerability detection and architecture compliance

---

### 🎯 **Jira Integration** (`jira-integration/`)
**Version**: 2.0.2 | **Converted from**: `jira` Claude plugin

**Commands:**
- `/jira-prep-ticket` - Complete ticket preparation with branch creation and requirements documentation
- `/jira-setup` - OAuth 2.0 authentication setup

**Features:**
- **Automatic Branch Creation**: Creates properly formatted git branches from Jira ticket IDs
- **Requirements Documents**: Extracts all ticket information into structured markdown
- **Analysis Modes**: 
  - `minimal`: Organized ticket information (default)
  - `full`: Technical analysis + implementation plan with task breakdown
- **OAuth 2.0**: Secure authentication with official Atlassian MCP server

**Example Usage:**
```bash
/jira-prep-ticket EN-123 full  # Full analysis with technical recommendations
/jira-prep-ticket EN-456       # Minimal analysis (default)
```

---

### ⚙️ **Kotlin Microservices Development** (`kotlin-microservices-dev/`)
**Version**: 1.0.0 | **Converted from**: `core-services-kt` Claude plugin

**Architecture**: GlossGenius 3-Layer Pattern (Handlers → Operations → Stores)

**Core Commands:**
- `/kotlin-domain-model` - Domain model creation with nullable token patterns
- `/kotlin-create-store` - Complete CRUD store generation with jOOQ
- `/kotlin-db-converter` - Bidirectional domain/database mapping converters
- `/kotlin-testing-store` - Comprehensive test suite generation with Kotest FreeSpec

**Testing Commands:**
- `/kotlin-freespec-tests` - Kotest FreeSpec pattern implementation
- `/kotlin-mockk-mocks` - Advanced MockK mock creation
- `/kotlin-test-data-factories` - Reusable test data builders
- `/kotlin-test-validation` - Comprehensive test validation workflow

**Data & Messaging:**
- `/kotlin-feed-consumer` - Event processing components for external data streams
- `/kotlin-feed-publisher` - Event broadcasting system for domain events

**Infrastructure:**
- `/kotlin-db-migration` - Database migration management with Flyway
- `/kotlin-add-dependencies` - Gradle dependency management
- `/kotlin-detekt-linting` - Code quality and security analysis

**Analysis:**
- `/kotlin-analyze-endpoint` - Architecture compliance analysis
- `/kotlin-test-validation` - Complete test coverage validation

**Key Patterns:**
- **Nullable Token Pattern**: Service-assigned fields with non-null getters
- **Immutable Collections**: All collections are `List`/`Map` (never `MutableList`)
- **Amount Type**: Always use `Amount` for monetary values (value + currency)
- **OffsetDateTime**: All timestamps use `OffsetDateTime` (never `LocalDateTime`)

---

### 📊 **Usage Analytics** (`usage-analytics/`)
**Version**: 1.0.1 | **Converted from**: `metrics` Claude plugin

**Features:**
- **Session Tracking**: Automatic session lifecycle monitoring
- **Command Usage**: Tracks command frequency and success rates
- **Prompt Analysis**: User interaction pattern analysis
- **Privacy-Focused**: Anonymized data collection with full opt-out capability

**Privacy Features:**
- Uses environment-based identifiers (`$USER`, `$GITHUB_USER`)
- Never collects actual code, prompts, or responses
- Only collects repository names, not content or structure
- Full opt-out via `OPENCODE_ANALYTICS_ENABLED=false`

**Data Collection:**
- Session start/end metrics
- Command execution patterns
- Error rates and failure analysis
- Feature usage and adoption rates

---

### 📋 **Project Lifecycle Management** (`project-lifecycle-management/`)
**Version**: 1.0.3 | **Converted from**: `project` Claude plugin

**Commands:**
- `/project-work` - End-to-end project lifecycle management

**Project Phases:**
1. **Design Phase**: Problem analysis, scope assessment, design documentation
2. **Implementation Phase**: Multi-repository coordination, quality verification

**Features:**
- **Jira Integration**: Full initiative/epic management with workflow tracking
- **Local Project Structure**: Organized under `~/Development/projects/<TICKET-ID>`
- **Multi-Repository Coordination**: Handles projects spanning multiple codebases
- **Learning Documentation**: Systematic knowledge capture under `docs/learnings/`
- **Feedback Integration**: Handles feedback from Jira, GitHub, and direct user input

**Project Structure:**
```
~/Development/projects/EN-123/
├── docs/
│   ├── plan.md              # Living implementation plan
│   └── learnings/           # Documented insights and lessons
└── repos/                   # Cloned repositories
```

---

## Legacy Skills (Individual Protobuf Tools)

These are the original individual skills that were consolidated into the comprehensive tools above:

### 📝 **improve-documentation** 
**Commands**: `/improve-docs`, `/improve-documentation`
- Reviews local protobuf changes and improves documentation quality

### 🔄 **protobuf-new**
**Commands**: `/proto-new`, `/protobuf-new`, `/new-proto`  
- Creates new protobuf definitions following best practices

### 🎫 **token-creator**
**Commands**: `/new-token`, `/create-token`, `/token-new`
- Creates complete token implementation with Kotlin integration

---

## Quick Start Workflows

### Complete Development Workflow
```bash
# 1. Prepare Jira ticket with full technical analysis
/jira-prep-ticket EN-123 full

# 2. Create domain models following GG patterns
/kotlin-domain-model

# 3. Generate complete store layer with jOOQ
/kotlin-create-store OrderStore

# 4. Create comprehensive test suite
/kotlin-testing-store OrderStore

# 5. Commit with clean, conventional format
/git-commit

# 6. Push and create PR with AI-generated description
/git-push-and-pr

# 7. Perform automated security-focused code review
/git-auto-review
```

### Project Management Workflow
```bash
# Initiate comprehensive project management
/project-work

# System guides through:
# - Jira initiative/epic creation
# - Local project structure setup
# - Repository coordination
# - Task delegation and monitoring
# - Learning documentation
```

### Protobuf Development Workflow
```bash
# Create new service method
/protobuf-new

# Create token type with Kotlin classes
/protobuf-new-token

# Improve documentation quality
/protobuf-improve-docs
```

---

## Integration Patterns

### Cross-Skill Workflows
1. **Jira → Git → Review**: `/jira-prep-ticket` → `/git-commit-push-pr` → `/git-auto-review`
2. **Project → Development → Analytics**: `/project-work` → Kotlin development → automatic usage tracking
3. **Protobuf → Kotlin → Testing**: `/protobuf-new` → `/kotlin-create-store` → `/kotlin-testing-store`

### Tool Requirements
- **Git CLI**: All git operations
- **GitHub CLI (`gh`)**: PR creation and management
- **Atlassian CLI (`acli`)**: Jira integration and OAuth
- **Node.js**: MCP server operations
- **Kotlin/Java**: Microservices development
- **jOOQ**: Database integration
- **Kotest**: Testing framework

---

## Environment Configuration

```bash
# Optional: Disable analytics
export OPENCODE_ANALYTICS_ENABLED=false

# GitHub user identification
export GITHUB_USER=your-github-username

# Custom analytics endpoint
export OPENCODE_ANALYTICS_ENDPOINT=https://api.glossgenius.com/internal/metrics/ai/
```

---

## Security & Compliance

### Critical Security Requirements
- **Git Commits**: NEVER include AI attributions (absolute requirement)
- **OAuth Integration**: Secure Jira authentication via official Atlassian MCP
- **Data Privacy**: Analytics are anonymized with full opt-out capability
- **Clean Operations**: All tools maintain enterprise security standards

### Architecture Compliance
- **3-Layer Architecture**: Handlers → Operations → Stores pattern enforcement
- **Domain Models**: Immutable models with proper token patterns
- **Testing Standards**: Comprehensive coverage with proper mocking
- **Code Quality**: Automated security and performance analysis

---

**Note**: These skills represent a sophisticated development workflow automation system specifically tailored for GlossGenius's Kotlin microservices architecture, with enterprise-grade security, comprehensive testing patterns, and detailed architectural guidelines.

All skills maintain identical functionality to their original Claude Code plugin counterparts while being fully compatible with OpenCode's skill system.