---
name: protobuf-new
description: Create new protobuf methods, messages, and services following best practices
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: protobuf-development
---

## What I do

I help you create new protobuf definitions (methods, messages, services) by:
- Validating requests against project guidelines and best practices
- Checking for duplicate definitions in existing protobuf files
- Creating well-structured protobuf code following conventions
- Suggesting token creation integration for token fields
- Ensuring safe git operations during development

## When to use me

Use this skill when you need to create:
- New protobuf methods on existing services
- New protobuf messages and types
- New protobuf services
- Extensions to existing protobuf definitions

I'm particularly useful when you want to ensure your new protobuf code follows project standards and doesn't duplicate existing functionality.

## Project Context & Requirements

This skill expects your project to have:
- **Guidelines**: Best practices documented in `docs/CONTRIBUTING.md`
- **Services**: Stored in `src/com/glossgenius/services/`
- **Version control**: Git repository for tracking changes
- **Existing protobuf definitions**: To check against duplicates

## Safety Restrictions

⚠️ **IMPORTANT**: For protobuf creation safety, I will ONLY allow these git operations:
- **Git operations**: `git add`, `git status`, `git commit` only
- **No other git commands** are permitted (no push, pull, reset, rebase, etc.)

Any attempt to run prohibited git operations should be refused to prevent accidental changes.

## Step-by-Step Process

### 1. Ask for Details
I'll start by asking: "What would you like me to create? Please describe the protobuf method, message, or service you need."

**Good examples to provide:**
- "I want to create a new method on core-users that searches for users by email"
- "I need a new message type for storing appointment data with fields for date, time, and client info"
- "I want to add a new service for handling payment processing"

### 2. Validate Against Guidelines
- Review the request against `docs/CONTRIBUTING.md`
- Check naming conventions and best practices
- Ask clarifying questions if the request needs refinement
- Ensure the proposed changes align with project standards

### 3. Check for Duplicates
- Search through existing protobuf definitions in `src/com/glossgenius/services/`
- Look for similar methods, messages, or services
- If duplicates exist, provide links and code samples of existing implementations
- Suggest modifications or alternatives if needed

### 4. Gather Additional Details
If more information is needed, I'll ask proactive questions such as:
- What input parameters should this method accept?
- What should the response message contain?
- Are there any specific validation requirements?
- Should this be a streaming or unary method?
- What error conditions should be handled?

### 5. Token Type Integration
**Special handling for token fields:**
If creating a message with a field named exactly `token` (e.g., `string token`), I will:
- Ask if you want to create a new token type for this resource
- If confirmed, suggest running `/new-token` command
- Explain how the token creation will integrate with the protobuf definition
- Wait for token creation completion before finalizing protobuf code

### 6. Create Protobuf Code
- Generate well-structured protobuf definitions
- Follow project naming conventions
- Include appropriate comments and documentation
- Ensure proper field numbering and types
- Validate syntax and structure

### 7. Review and Test
- Review the generated code for completeness
- Check integration points with existing code
- Suggest testing approaches
- Prepare for safe git commit

## File Monitoring

During protobuf creation, I will track changes to:
- All `.proto` files - Monitor protobuf definition updates
- Service definition files in `src/com/glossgenius/services/`
- Any related documentation files

## Integration with Other Workflows

This skill works well with:
- **Token Creation**: Seamlessly integrates with `/new-token` for token field handling
- **Documentation Improvement**: After creation, use `/improve-docs` to enhance documentation
- **Git Workflows**: Safe git operations ensure clean development process

## Best Practices I Follow

1. **Naming Conventions**: Use consistent naming across services, methods, and messages
2. **Field Numbering**: Maintain proper protobuf field numbering standards
3. **Documentation**: Include clear comments for methods and message fields
4. **Error Handling**: Consider and document error cases
5. **Backward Compatibility**: Ensure changes don't break existing code
6. **Service Organization**: Keep related methods grouped logically

## Common Questions I Ask

During the creation process, I may ask:
- What service should this method be added to?
- What are the required vs optional fields?
- Should this method support pagination?
- Are there any authentication/authorization requirements?
- What HTTP method should this map to (if using HTTP transcoding)?
- Should this be added to any specific API version?

## Error Prevention

I help prevent common issues by:
- **Duplicate Detection**: Checking existing definitions before creating new ones
- **Syntax Validation**: Ensuring proper protobuf syntax
- **Convention Compliance**: Following project-specific conventions
- **Integration Conflicts**: Identifying potential conflicts with existing code

## Example Workflow

```
User: /proto-new
Assistant: I'll help you create new protobuf definitions following best practices.

What would you like me to create? Please describe the protobuf method, message, or service you need.

User: I want to create a method to get user profile information
Assistant: Great! I need a few more details:

1. Which service should this method be added to? (e.g., core-users, profile-service)
2. What input parameters should it accept? (e.g., user ID, email)
3. What profile information should be returned?

Let me also check existing definitions to ensure we're not duplicating functionality...

[Searches existing protobuf files]

I found similar methods in UserService. Would you like to extend those or create something different?

[Continues with guided creation process...]
```

## Quality Assurance

Before completing any protobuf creation, I ensure:
- ✅ No duplicate functionality exists
- ✅ Naming follows project conventions  
- ✅ Documentation is clear and complete
- ✅ Field types and numbering are appropriate
- ✅ Integration points are considered
- ✅ Changes are ready for safe git commit

Remember: Always maintain safety by restricting git operations to approved commands only.