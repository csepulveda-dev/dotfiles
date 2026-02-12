# OpenCode Skills - Quick Reference

## 🚀 Most Used Commands

### Git Workflow
```bash
/git-commit                 # Clean commit with conventional format (NO AI attribution)
/git-commit-push-pr         # Full workflow: commit + push + PR
/git-push-and-pr           # Push existing commits + create PR
/git-auto-review           # Automated security-focused code review
```

### Jira Integration  
```bash
/jira-prep-ticket EN-123 full    # Full analysis with technical plan
/jira-prep-ticket EN-123         # Minimal analysis (default)
/jira-setup                      # OAuth authentication setup
```

### Kotlin Development
```bash
/kotlin-domain-model             # Create domain models with GG patterns
/kotlin-create-store OrderStore  # Generate complete CRUD store + tests
/kotlin-testing-store OrderStore # Comprehensive test suite generation
/kotlin-freespec-tests          # Kotest FreeSpec patterns
```

### Protobuf Development
```bash
/protobuf-new                   # Create new methods/messages/services
/protobuf-new-token            # Create token prefixes + Kotlin classes
/protobuf-improve-docs         # Review and improve documentation
```

### Project Management
```bash
/project-work                   # End-to-end project lifecycle management
```

## 🔥 Power Workflows

### Complete Feature Development
```bash
/jira-prep-ticket EN-123 full   # 1. Prepare ticket with analysis
/kotlin-domain-model            # 2. Create domain models  
/kotlin-create-store MyStore    # 3. Generate store + tests
/git-commit                     # 4. Clean commit
/git-push-and-pr               # 5. Push + create PR
/git-auto-review               # 6. Automated review
```

### Protobuf Service Development
```bash
/protobuf-new                   # 1. Create service method
/protobuf-new-token            # 2. Create token (if needed)
/kotlin-create-store TokenStore # 3. Generate Kotlin integration
/protobuf-improve-docs         # 4. Improve documentation
```

## ⚠️ Critical Requirements

### Git Commits
- **NEVER** include AI attributions in commit messages
- **ALWAYS** use conventional commit format: `[TICKET-ID] type(scope): description`
- **CLEAN** commits are absolutely required

### Authentication
```bash
gh auth login      # GitHub CLI authentication
acli auth login    # Atlassian/Jira authentication  
```

### Environment Variables
```bash
export GITHUB_USER=your-username
export OPENCODE_ANALYTICS_ENABLED=false  # Optional: disable analytics
```

## 📁 File Locations

- **Skills**: `~/.config/opencode/skills/` (symlinked via stow)
- **Documentation**: `~/.config/opencode/SKILLS.md` (detailed docs)
- **Stow Source**: `~/dotfiles/opencode/.config/opencode/`

## 🏗️ Architecture Patterns (Kotlin)

### 3-Layer Architecture
- **Handlers**: HTTP controllers, RPC handlers, Job handlers
- **Operations**: Business logic orchestration  
- **Stores**: Data access abstraction (jOOQ, gRPC, REST)
- **Models**: Immutable domain models with token patterns

### Key Patterns
- **Nullable Tokens**: `val nullableToken: Token? = null` + `val token: Token get() = nullableToken!!`
- **Immutable Collections**: Always `List`/`Map`, never `MutableList`/`MutableMap`
- **Amount Type**: `Amount(value: BigDecimal, currency: Currency)` for money
- **Timestamps**: `OffsetDateTime` (never `LocalDateTime`)

## 🔧 Quick Troubleshooting

1. **Skills not loading**: Check `~/.config/opencode/skills/` exists and is symlinked
2. **Auth failures**: Run `gh auth login` and `acli auth login`
3. **Missing tools**: Install `git`, `gh`, `acli`, `node`
4. **Clean commits failing**: Ensure no AI attribution text in commit messages

## 📚 Full Documentation

See `~/.config/opencode/SKILLS.md` for comprehensive documentation of all skills and features.