---
name: Git Workflow Tools
version: 1.5.0
description: Advanced Git workflow automation with AI-powered commit messages, PR generation, code review, and worktree management
author: GlossGenius
keywords: [git, commit, workflow, pr, review, automation]
---

# Git Workflow Tools

This skill provides comprehensive Git workflow automation tools for professional development teams, with strict requirements for clean commit messages and automated code review.

## Available Commands

### /git-commit
Create a well-formatted git commit with AI assistance while ensuring NO AI attributions in the commit message.

**Usage:**
- `/git-commit` - Interactive commit creation with conventional commit format

**Critical Requirements:**
- **NEVER** add ANY AI-related attribution to commits
- NO "Generated with Claude Code", "Co-Authored-By: Claude", or ANY tool attribution
- Commits must be completely CLEAN and professional

**Process:**
1. Reviews current changes (staged/unstaged)
2. Extracts ticket ID from branch name or asks user
3. Determines appropriate commit type and scope
4. Crafts conventional commit message: `[TICKET-ID] type(scope): description`
5. Presents message for user approval
6. Creates clean commit

**Commit Types:**
- `feat`: New feature or functionality
- `fix`: Bug fix  
- `chore`: Maintenance, dependencies, tooling
- `refactor`: Code refactoring (no functional changes)
- `test`: Adding or updating tests
- `docs`: Documentation changes
- `style`: Code formatting
- `perf`: Performance improvements
- `ci`: CI/CD changes
- `build`: Build system changes

### /git-commit-push-pr
Full workflow: commit changes, push to remote, and create pull request.

**Usage:**
- `/git-commit-push-pr` - Complete workflow from changes to PR

**Process:**
1. Creates clean commit (using same process as `/git-commit`)
2. Pushes changes to remote branch
3. Generates AI-powered PR description with technical context
4. Creates pull request via GitHub CLI

### /git-push-and-pr  
Push existing commits and create pull request for current branch.

**Usage:**
- `/git-push-and-pr` - Push and create PR for existing commits

**Process:**
1. Pushes current branch to remote
2. Analyzes all commits since diverging from main
3. Generates comprehensive PR description
4. Creates pull request with technical context

### /git-auto-review
Automated PR review with inline comments focusing on security, bugs, and performance.

**Usage:**
- `/git-auto-review` - Performs automated code review

**Focus Areas:**
- Security vulnerabilities and best practices
- Bug detection and edge cases
- Performance optimization opportunities
- Code quality and maintainability
- Architecture compliance

### /git-create-worktree
Git worktree automation for parallel development environments.

**Usage:**
- `/git-create-worktree <branch-name>` - Creates new worktree for parallel work

**Process:**
1. Creates new worktree directory
2. Sets up proper branch tracking
3. Configures development environment
4. Enables parallel development without conflicts

### /git-rebase-from-main
Safe rebasing from main branch with conflict resolution assistance.

**Usage:**
- `/git-rebase-from-main` - Safely rebase current branch from main

**Process:**
1. Fetches latest main branch
2. Performs interactive rebase with safety checks
3. Provides conflict resolution guidance
4. Ensures clean commit history

### /git-core-services-reviewer
Specialized reviewer for Kotlin/Java services following GlossGenius architecture guidelines.

**Usage:**
- `/git-core-services-reviewer` - Architecture-specific code review

**Features:**
- 2,000+ lines of GlossGenius architecture guidelines
- Kotlin/Java best practices enforcement
- Micronaut framework patterns validation
- Domain model architecture compliance
- Security and performance standards

## Security Considerations

- **Clean Commits**: Absolutely NO AI attributions in any commit messages
- **Branch Protection**: Prevents commits to main/master branches without proper review
- **Pre-commit Verification**: Runs lint checks and tests before committing
- **Secure PR Creation**: Uses GitHub CLI with proper authentication
- **Code Review**: Automated security vulnerability detection

## Technical Requirements

### Git Configuration
- Repository must be initialized
- Git user.name and user.email configured
- GitHub CLI (`gh`) installed and authenticated

### Branch Naming
- Supports ticket ID extraction from branch names
- Formats: `EN-123-feature-name`, `PROJ-456/bug-fix`, etc.
- Fallback to `[NO-TASK]` if no ticket ID found

### Commit Message Format
```
[TICKET-ID] type(scope): Description
```

Examples:
- `[EN-123] feat(auth): Add OAuth2 authentication flow`
- `[PROJ-456] fix(api): Fix race condition in user session handling`
- `[NO-TASK] chore(deps): Update React to v18.2.0`

### PR Description Generation
Automatically generates comprehensive PR descriptions including:
- Summary of changes with technical context
- Impact assessment and testing notes
- Breaking changes documentation
- Checklist for reviewers

## Tool Requirements

This skill requires access to:
- Git CLI (all standard git operations)
- GitHub CLI (`gh`) for PR creation and management
- Bash for automation scripts
- File system access for worktree management
- Network access for GitHub API operations

## Best Practices

### Commit Strategy
- Atomic commits (one logical change per commit)
- Clear, descriptive commit messages
- Proper type and scope selection
- Ticket ID linking for traceability

### PR Workflow
- Descriptive PR titles and descriptions
- Technical context for complex changes
- Testing instructions included
- Breaking changes highlighted

### Code Review
- Focus on security, performance, and maintainability
- Constructive feedback with specific suggestions
- Architecture compliance verification
- Documentation quality assessment

## Error Handling

- Graceful handling of merge conflicts
- Clear guidance for failed pre-commit hooks
- Rollback capabilities for failed operations
- Detailed error messages with next steps

## Integration Points

- **Jira Integration**: Automatic ticket ID extraction and linking
- **CI/CD Systems**: Pre-commit hook integration
- **GitHub Actions**: Automated testing triggers
- **Code Quality Tools**: Linting and analysis integration