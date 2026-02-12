---
name: improve-documentation
description: Review local protobuf changes and improve documentation quality
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: documentation-review
---

## What I do

I help you improve protobuf documentation by:
- Analyzing git changes between your local branch and main
- Identifying documentation gaps and inconsistencies
- Suggesting improvements for field names and descriptions
- Ensuring documentation accurately reflects the code's purpose
- Following project contribution guidelines and linter rules

## When to use me

Use this skill when you:
- Have made protobuf changes that need documentation review
- Want to improve existing protobuf documentation
- Need to ensure field names match their actual purpose
- Want to follow project documentation standards
- Are preparing changes for code review

## Project Context & Requirements

This skill expects your project to have:
- **Version control**: Git repository with main branch
- **Guidelines**: Best practices documented in `docs/CONTRIBUTING.md`
- **Linter rules**: Documentation standards in `linter/linter.py`
- **Protobuf files**: Located in `src/` directory structure
- **Active branch**: Working on a feature branch with changes to review

## Safety Restrictions

⚠️ **IMPORTANT**: For documentation improvement safety, I will ONLY allow these git operations:
- **Git operations**: `git add`, `git status`, `git commit` only
- **No other git commands** are permitted (no push, pull, reset, rebase, merge, etc.)

Any attempt to run prohibited git operations should be refused to prevent accidental changes or conflicts.

## Step-by-Step Process

### 1. Examine Current Status
I'll start by examining the current git status and recent changes:
- Run `git status` to see modified files
- Check current branch and relationship to main
- Identify protobuf files that have been changed

### 2. Identify Changes from Main
- Use `git diff main...HEAD` to see all changes since branching from main
- Focus specifically on protobuf (.proto) file changes
- Identify new fields, methods, messages, or services
- Note any modified documentation or comments

### 3. Analyze Documentation Quality
For each change, I will review:
- **Field descriptions**: Do they accurately describe the field's purpose?
- **Method documentation**: Are parameters and return values clearly explained?
- **Message comments**: Do they provide context for when/how to use the message?
- **Service descriptions**: Are the service's responsibilities clear?
- **Field naming**: Do field names match their documented purpose?

### 4. Check Against Guidelines
- Review changes against `docs/CONTRIBUTING.md` standards
- Validate against linter rules in `linter/linter.py`
- Ensure consistency with existing documentation patterns
- Check for required documentation elements

### 5. Identify Improvement Opportunities
I will look for:
- Missing field descriptions
- Vague or unclear documentation
- Field names that don't match their purpose
- Inconsistent documentation styles
- Missing method parameter documentation
- Unclear error condition documentation

### 6. Make Improvement Suggestions
For each issue found, I will:
- **Straightforward fixes**: Make direct suggestions for better documentation
- **Unclear changes**: Ask for clarification about the intended purpose
- **Field naming issues**: Suggest better names or ask for context
- **Missing context**: Request additional information from you

### 7. Implement Improvements
- Update protobuf files with improved documentation
- Ensure consistency across related definitions
- Follow project formatting and style standards
- Prepare clean git commits with descriptive messages

## Questions I Ask for Clarification

When I encounter unclear changes, I may ask:
- What is the intended purpose of this new field?
- How should this method be used by clients?
- What are the expected values for this field?
- When would someone use this message type?
- Are there any constraints or validation rules for this field?
- What error conditions should be documented?

## Common Documentation Improvements

I typically help with:
- **Field descriptions**: Adding clear, concise descriptions
- **Parameter documentation**: Explaining method inputs and outputs
- **Usage examples**: Providing context for when to use features
- **Error documentation**: Describing possible error conditions
- **Validation rules**: Documenting field constraints
- **Relationship clarity**: Explaining how fields relate to each other

## Field Name Analysis

When reviewing field names, I check for:
- **Accuracy**: Does the name match the documented purpose?
- **Clarity**: Is the name self-explanatory?
- **Consistency**: Does it follow project naming conventions?
- **Specificity**: Is it specific enough to avoid confusion?

If I find mismatches, I will:
- Ask for clarification if the purpose is unclear
- Suggest better field names if the improvement is obvious
- Explain the reasoning behind suggested changes

## Integration with Development Workflow

This skill works well:
- **After protobuf creation**: Use `/proto-new` then `/improve-docs`
- **Before code review**: Ensure documentation is review-ready
- **After token creation**: Use `/new-token` then `/improve-docs`
- **During feature development**: Iterative documentation improvement

## Quality Standards I Maintain

I ensure documentation:
- ✅ Clearly describes field purposes and usage
- ✅ Follows project style and formatting guidelines
- ✅ Provides sufficient context for other developers
- ✅ Includes error conditions and constraints where relevant
- ✅ Uses consistent terminology across the project
- ✅ Matches the actual implementation behavior

## Example Workflow

```
User: /improve-docs
Assistant: I'll help improve the documentation for your protobuf changes.

Let me start by examining the current git status and recent changes...

[Runs git status and git diff main...HEAD]

I found changes in these protobuf files:
- src/com/glossgenius/services/users.proto
- src/com/glossgenius/services/appointments.proto

I see you've added a new field `client_preferences` but there's no description. 
Could you clarify what type of preferences this field should contain?

User: It stores user notification preferences like email, SMS settings
Assistant: Perfect! I'll add a clear description:

```proto
// User notification preferences including email and SMS settings
string client_preferences = 5;
```

I also notice the field name might be more specific. Would `notification_preferences` be more accurate?

[Continues with improvement suggestions...]
```

## File Monitoring

During documentation improvement, I track changes to:
- All `.proto` files - Monitor documentation updates
- `docs/CONTRIBUTING.md` - Reference current guidelines
- `linter/linter.py` - Understand documentation standards

Remember: Always maintain safety by restricting git operations to approved commands and asking for clarification when changes aren't clear.