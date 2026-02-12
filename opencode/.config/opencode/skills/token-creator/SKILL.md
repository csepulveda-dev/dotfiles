---
name: token-creator
description: Create resource token prefixes with protobuf registration and Kotlin integration
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: protobuf-kotlin
---

## What I do

I help you create a complete resource token prefix implementation by:
- Registering token prefixes in protobuf definitions
- Generating Kotlin token classes in domain-specific directories  
- Adding tokens to TokenResource.kt registry
- Running tests to verify the implementation
- Organizing tokens by domain structure

## When to use me

Use this skill when you need to create a new resource token type for your protobuf and Kotlin project. I follow a systematic 7-step process to ensure complete and correct token implementation.

## Project Context & Requirements

This skill is designed for projects with the following structure:
- **Versioning**: Managed through `git`
- **Token prefixes**: Registered in `src/com.glossgenius/tokens/token_prefix.proto`
- **Kotlin classes**: Located in `packages/kotlin/src/main/kotlin/com/glossgenius/core/libs/tokens/domains` under corresponding domains
- **Token registry**: Recorded in `packages/kotlin/src/main/kotlin/com/glossgenius/core/libs/tokens/TokenResource.kt`
- **Domains**: Directories under `packages/kotlin/src/main/kotlin/com/glossgenius/core/libs/tokens/domains/`
- **Testing**: Execute with `cd packages/kotlin && ./gradlew test`

## Safety Restrictions

⚠️ **IMPORTANT**: For token creation safety, I will ONLY allow these operations:
- **Git operations**: `git add`, `git status`, `git commit` only
- **Test operations**: `./gradlew test` (in packages/kotlin directory) only
- **No other bash commands** are permitted during token creation

Any attempt to run other git commands (like push, pull, reset, etc.) or other bash operations should be refused to prevent accidental changes.

## Step-by-Step Process

### 1. Ask for Token Name
First, I'll ask: "What's the name of the token you're trying to create?" 
- Request a descriptive name for the new token type
- Ensure the name follows naming conventions

### 2. Get Description  
- Based on the token name, suggest a short description
- Ask for clarification if the purpose isn't clear
- Ensure description accurately reflects the token's purpose

### 3. Determine Domain
- Propose an appropriate domain based on the token name and purpose
- Ask for confirmation or alternative domain name
- Verify the domain directory exists in the tokens structure

### 4. Create Token Prefix
- Register the new token in `src/com.glossgenius/tokens/token_prefix.proto`
- Follow existing patterns and naming conventions
- Ensure no duplicate token names exist

### 5. Generate Kotlin Class
- Create the Kotlin token class in the appropriate domain directory
- Follow existing class patterns and structure
- Include proper imports and class structure
- Ensure class name matches token naming conventions

### 6. Register Token
- Add the token to `packages/kotlin/src/main/kotlin/com/glossgenius/core/libs/tokens/TokenResource.kt`
- Follow existing registration patterns
- Maintain alphabetical or logical ordering

### 7. Run Tests
- Execute `cd packages/kotlin && ./gradlew test` to verify implementation
- Check for any test failures
- If tests fail, analyze and fix issues before completing

## File Monitoring

During the token creation process, I will pay special attention to changes in:
- `token_prefix.proto` - Token prefix registrations
- `TokenResource.kt` - Token registry updates  
- `/tokens/domains/` - Domain-specific token class files

## Error Handling

If any step fails:
1. **Duplicate tokens**: Check existing definitions and suggest alternatives
2. **Test failures**: Analyze error output and fix implementation issues
3. **Invalid domains**: Suggest valid domain options or create new domain if appropriate
4. **File conflicts**: Resolve conflicts while preserving existing functionality

## Integration Notes

This token creation skill works well with:
- **Protobuf creation workflows**: When creating new protobuf definitions that need token fields
- **Documentation improvement**: After token creation, documentation can be enhanced
- **Git workflows**: Safe git operations ensure clean commits of token implementations

## Best Practices

1. **Naming consistency**: Ensure token names are consistent across protobuf and Kotlin
2. **Domain organization**: Keep related tokens in appropriate domains
3. **Test coverage**: Always run tests to verify implementation
4. **Documentation**: Include clear descriptions for token purposes
5. **Clean commits**: Use descriptive commit messages for token additions

## Example Workflow

```
User: /new-token
Assistant: I'll help you create a new resource token prefix...

What's the name of the token you're trying to create?

User: appointment
Assistant: Great! For an "appointment" token, I suggest the description "Token for appointment resources". 

I propose placing this in the "scheduling" domain. Does this sound appropriate?

User: Yes
Assistant: Perfect! I'll now:
1. ✅ Register "appointment" token in token_prefix.proto
2. ✅ Create AppointmentToken.kt in scheduling domain
3. ✅ Add to TokenResource.kt registry
4. ✅ Run tests to verify implementation

[Proceeds with implementation steps...]
```

## Questions to Ask During Process

- What's the name of the token you want to create?
- What description best describes this token's purpose?
- Which domain should this token belong to?
- Should I create a new domain if the appropriate one doesn't exist?
- Are there any specific requirements for this token implementation?

Remember: Always maintain safety by restricting operations to the approved git and gradle commands only.