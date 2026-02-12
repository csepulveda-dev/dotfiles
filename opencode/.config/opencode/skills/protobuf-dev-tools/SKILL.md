---
name: Protobuf Development Tools
version: 1.1.0
description: Commands and agents for building and developing protobuf services and messages, including creating new methods/messages, token management, and documentation improvement.
author: GlossGenius
keywords: [protobuf, grpc, services, tokens, documentation]
---

# Protobuf Development Tools

This skill provides comprehensive tools for protobuf service development and management, following GlossGenius best practices.

## Available Commands

### /protobuf-new
Create new protobuf methods, messages, or services following best practices and verifying no duplication exists in existing definitions.

**Usage:**
- `/protobuf-new` - Interactive mode to create new protobuf definitions
- Example: "I want to create a new method on core-users that searches for users by email."

**Process:**
1. Asks user what they want to create
2. Verifies request doesn't violate contribution guidelines
3. Checks for existing definitions to prevent duplication
4. Creates new protobuf definitions following best practices
5. Suggests token creation if message includes a `token` field

### /protobuf-new-token
Create a new resource token prefix by registering it in protobuf definitions, generating Kotlin token classes, and running tests.

**Usage:**
- `/protobuf-new-token` - Interactive token creation workflow

**Process:**
1. Asks for token name
2. Suggests or asks for token description
3. Proposes or asks for domain name
4. Creates token prefix in `token_prefix.proto`
5. Creates Kotlin class in corresponding domain
6. Registers token in `TokenResource.kt`
7. Runs tests to verify implementation

### /protobuf-improve-docs
Review local protobuf changes and improve documentation quality, ensuring field names and descriptions accurately reflect their purpose.

**Usage:**
- `/protobuf-improve-docs` - Reviews and improves protobuf documentation

**Process:**
1. Identifies changes made on local branch vs main
2. Writes or improves documentation for identified changes
3. Validates field names match documentation
4. Suggests corrections for mismatched or unclear field names

## Context and Structure

- **Best practices**: Guidelines are in `docs/CONTRIBUTING.md`
- **Services**: Stored in `src/com/glossgenius/services/`
- **Token prefixes**: Registered in `src/com.glossgenius/tokens/token_prefix.proto`
- **Kotlin tokens**: Located in `packages/kotlin/src/main/kotlin/com/glossgenius/core/libs/tokens/domains/`
- **Token registration**: `packages/kotlin/src/main/kotlin/com/glossgenius/core/libs/tokens/TokenResource.kt`
- **Testing**: Run with `cd packages/kotlin && ./gradlew test`
- **Linting**: Rules in `linter/linter.py`

## Security Considerations

- All changes are tracked through git version control
- Follows established contribution guidelines
- Validates against existing definitions to prevent conflicts
- Runs comprehensive tests before finalizing changes
- Maintains proper domain separation for token classes

## Tool Requirements

This skill requires access to:
- Bash (for git operations: add, status, commit)
- File reading and editing capabilities
- Directory traversal for protobuf definition validation