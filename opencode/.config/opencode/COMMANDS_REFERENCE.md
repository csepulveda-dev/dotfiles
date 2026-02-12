# OpenCode Slash Commands Reference

Generated from your Skills on Feb 11, 2026

## Git Workflow Commands
These commands use the Git Workflow Tools skill to automate git operations:

- `/git-commit` - Create well-formatted git commits with AI assistance
- `/git-commit-push-pr` - Full workflow: commit, push, and create PR
- `/git-push-and-pr` - Push existing commits and create PR
- `/git-auto-review` - Automated PR review focusing on security and performance
- `/git-create-worktree <branch-name>` - Create git worktree for parallel development
- `/git-rebase-from-main` - Safe rebasing from main with conflict resolution
- `/git-core-services-reviewer` - Specialized Kotlin/Java architecture review

## Protobuf Development Commands
These commands use the Protobuf Development Tools skill:

- `/protobuf-new` - Create new protobuf methods, messages, or services
- `/protobuf-new-token` - Create resource token with protobuf and Kotlin integration
- `/protobuf-improve-docs` - Review and improve protobuf documentation

## Kotlin Microservices Commands
These commands use the Kotlin Microservices Development skill:

- `/kotlin-domain-model` - Create/modify domain models following GlossGenius patterns
- `/kotlin-create-store <entity-name>` - Generate complete CRUD store with jOOQ
- `/kotlin-freespec-tests <class-name>` - Generate Kotest FreeSpec test suites
- `/kotlin-db-migration <migration-name>` - Create Flyway database migrations

## Jira Integration Commands
These commands use the Jira Integration skill:

- `/jira-prep-ticket <ticket-url> [mode]` - Fetch ticket details, create branch, generate requirements
- `/jira-setup` - Configure Jira authentication using OAuth 2.0

## Usage Notes

1. All commands automatically load the corresponding skill and follow best practices
2. Commands with `<argument>` require parameters, those with `[argument]` are optional
3. Commands maintain clean commit messages without AI attributions
4. All generated code follows GlossGenius 3-layer architecture patterns

## Testing Commands

You can now use any of these commands in OpenCode by typing the command name with a forward slash (e.g., `/git-commit`).