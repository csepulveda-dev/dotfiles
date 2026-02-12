---
name: Jira Integration
version: 2.0.2
description: Jira integration for automated ticket preparation, epic processing, and workflow automation with comprehensive requirements documentation
author: GlossGenius
keywords: [jira, integration, tickets, requirements, workflow, automation]
---

# Jira Integration

This skill provides comprehensive Jira integration for automated ticket preparation, branch creation, and requirements documentation with optional technical analysis and implementation planning.

## Available Commands

### /jira-prep-ticket
Fetch Jira ticket details, create a new revision using jujutsu vcs, use the jira ticket ID and title as the description for the new revision, and generate comprehensive requirements document with optional technical analysis and implementation plan.

**Usage:**
- `/jira-prep-ticket <ticket-url> [mode]`

**Arguments:**
- `ticket-url` (required): Full Jira ticket URL or just ticket ID
  - Format: `https://domain.atlassian.net/browse/ENG-123` or `ENG-123`
- `mode` (optional): Analysis mode - `minimal` (default) or `full`
  - `minimal`: Organized ticket information in structured markdown
  - `full`: Includes technical analysis + implementation plan with task breakdown

**Examples:**
```bash
# Minimal analysis (default)
/jira-prep-ticket https://company.atlassian.net/browse/ENG-123

# Full analysis with technical recommendations  
/jira-prep-ticket ENG-456 full

# Using just ticket ID
/jira-prep-ticket ENG-789
```

**Process:**
1. **Validates Jira CLI Configuration**: Checks for properly configured Atlassian CLI
2. **Parses Ticket Identifier**: Extracts ticket ID from URL or validates ID format
3. **Determines Analysis Mode**: Default minimal or explicit full mode
4. **Fetches Ticket Details**: Retrieves comprehensive ticket data from Jira
5. **Generates Revision Description**: Creates jujutsu revision with a description following `{TICKET-ID}/{description}` convention
6. **Analyzes Content**: Performs analysis based on selected mode
7. **Generates Requirements Document**: Creates detailed markdown file with all information

### /jira-setup
Configure Jira authentication and CLI access using OAuth 2.0 for secure credential management.

**Usage:**
- `/jira-setup` - Interactive setup for Jira authentication

**Features:**
- OAuth 2.0 authentication (no API tokens stored)
- Official Atlassian MCP server integration
- Secure credential management
- Auto-configuration of CLI tools

## Analysis Modes

### Minimal Mode (Default)
**Use when:** Standard ticket preparation without deep technical analysis

**Includes:**
- Structured ticket information extraction
- Organized acceptance criteria as checklists
- Related tickets and dependencies mapping
- Chronological comment formatting
- Complete ticket metadata (status, priority, assignee, etc.)
- Attachments and links preservation

**Does NOT include:**
- Codebase searching or analysis
- Technical recommendations
- Task breakdowns or implementation planning

### Full Mode
**Use when:** Complex tickets requiring detailed technical planning

**Includes everything from Minimal Mode PLUS:**

**Technical Analysis:**
- Codebase search for relevant files and components
- Architecture pattern identification
- Security considerations assessment
- Component/module impact analysis

**Implementation Planning:**
- Detailed task breakdown with complexity estimates
- Suggested implementation order with reasoning
- Dependency identification between tasks
- Testing requirements (unit, integration, e2e)

**Additional Considerations:**
- Database migration requirements
- API changes and backward compatibility
- Documentation updates needed
- Performance impact assessment

## Requirements Document Structure

### Generated Markdown File: `{TICKET-ID}.md`

**Core Structure (Both Modes):**
```markdown
# [TICKET-ID] Ticket Summary

**Status**: [Status] | **Priority**: [Priority] | **Type**: [Type]
**Jira Link**: [Full URL]

## Description
[Full formatted description]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Details
- **Assignee**: [Name]
- **Reporter**: [Name]  
- **Sprint**: [Sprint info]
- **Story Points**: [Points]
- **Labels**: [Tags]

## Related Issues
- **Blocks**: [Blocked tickets]
- **Blocked By**: [Blocking tickets]
- **Relates To**: [Related tickets]

## Comments
[Chronological comment history]

## Attachments
[Links to attachments and files]
```

**Additional Sections (Full Mode Only):**
```markdown
## Technical Analysis
### Affected Components
### Architecture Notes
### Security Considerations

## Implementation Plan
### Task Breakdown
### Implementation Order
### Dependencies

## Testing Requirements
### Unit Tests
### Integration Tests
### Manual Testing Checklist

## Additional Considerations
### Database Changes
### API Changes
### Documentation Updates
### Performance Impact
```

## Revision Description Convention

Automatically generates a jujutsu vcs revision, with a description following the pattern:
`{TICKET-ID}/{short-description}`

**Examples:**
- `ENG-123/add-user-authentication`
- `PROJ-456/fix-memory-leak-background`  
- `BUG-789/update-api-documentation-v2`

**Rules:**
- Converts summary to lowercase
- Replaces spaces with hyphens
- Removes special characters
- Limits to 4-6 meaningful words
- Maximum 50 characters total

## Security Considerations

### Authentication
- **OAuth 2.0 Flow**: Secure browser-based authentication
- **No Token Storage**: Credentials managed by official Atlassian MCP server
- **Permission Control**: OAuth scope grants for controlled access
- **Secure API Communication**: All requests through encrypted channels

### Data Handling
- **Read-Only Operations**: No modification of Jira tickets during preparation
- **Local File Creation**: Requirements documents created locally only
- **Revision Isolation**: Each ticket gets isolated jujutsu revision
- **No Sensitive Data Exposure**: Ticket content handled securely

## Technical Requirements

### Prerequisites
- Git repository initialization using jj git init --colocate
- Atlassian CLI (`acli`) installed and configured
- Network access for Jira API communication
- Proper Jira project permissions

### Dependencies
- **Atlassian CLI**: Official command-line interface
- **Atlassian MCP Server**: Auto-configured for OAuth integration
- **Jujutsu CLI**: For revision creation and management
- **Node.js**: Required for MCP server operation

### API Integration
- **Jira REST API v2**: Comprehensive ticket data retrieval
- **GitHub Integration**: For repository context and analysis
- **MCP Protocol**: Secure communication with Atlassian services

## Error Handling

### Configuration Errors
- **CLI Not Configured**: Clear guidance to run `/jira-setup`
- **Authentication Failures**: OAuth flow restart recommendations
- **Permission Issues**: Project access verification guidance

### Ticket Access Errors
- **404 Not Found**: Ticket existence and access verification
- **401 Unauthorized**: Token expiration and re-authentication
- **403 Forbidden**: Permission verification and escalation guidance

### Jujutsu Errors
- **Revision Description Exists**: Options to edit the revision, rename, or cancel
- **Repository Not Initialized**: Clear jujutsu/git setup requirements
- **Network Issues**: Connection troubleshooting guidance

## Integration Features

### Cross-Plugin Compatibility
- **Project Management**: Compatible with `/project-work` workflows
- **Code Review**: Prepared for automated review processes

### Workflow Automation
```bash
# Complete workflow example
/jira-prep-ticket ENG-123 full    # Prepare ticket with full analysis
# ... implement features ...
```

### Enterprise Features
- **Sprint Integration**: Automatic sprint context extraction
- **Epic Management**: Hierarchical ticket relationship mapping  
- **Multi-Project Support**: Works across different Jira projects
- **Custom Field Support**: Handles organization-specific fields

## Best Practices

### When to Use Each Mode
- **Minimal Mode**: Straightforward tickets, bug fixes, simple features
- **Full Mode**: Complex features, architectural changes, cross-team coordination

### Documentation Standards
- Always review generated requirements before starting implementation
- Update acceptance criteria as work progresses
- Use as reference throughout development lifecycle
- Include in PR descriptions for reviewer context

### Revision Management
- One revision per ticket for clear separation
- Follow consistent naming conventions
- Link revisions to tickets through naming
