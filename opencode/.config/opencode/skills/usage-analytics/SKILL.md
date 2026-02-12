---
name: Usage Analytics
version: 1.0.1
description: Comprehensive usage analytics and telemetry collection for OpenCode sessions with privacy-focused metrics
author: GlossGenius  
keywords: [analytics, telemetry, metrics, usage, monitoring, sessions]
---

# Usage Analytics

This skill provides comprehensive usage analytics and telemetry collection for OpenCode sessions, tracking user interaction patterns, command usage, and session metrics while maintaining privacy and security standards.

## Overview

The Usage Analytics skill automatically collects anonymized usage data to help improve OpenCode functionality and user experience. All metrics are collected with privacy considerations and focus on usage patterns rather than content analysis.

## Data Collection Points

### Session Tracking
**Automatic collection on session lifecycle events:**

- **Session Start**: Captures session initialization metrics
- **Session End**: Records session duration and completion status  
- **User Context**: Associates metrics with anonymized user identifiers
- **Repository Context**: Links sessions to repository types (without sensitive data)

### Command Usage Tracking
**Monitors interaction with OpenCode features:**

- **Slash Command Usage**: Tracks which commands are most frequently used
- **Tool Invocation**: Records tool usage patterns and frequency
- **Workflow Patterns**: Identifies common command sequences and workflows
- **Error Rates**: Monitors command failure rates and error patterns

### Prompt Analysis
**Analyzes user interaction patterns:**

- **Prompt Frequency**: Tracks user engagement levels
- **Request Categories**: Categorizes requests by type (coding, debugging, documentation)
- **Response Quality**: Monitors user satisfaction through interaction patterns
- **Feature Discovery**: Identifies underutilized features

## Privacy and Security

### Data Anonymization
- **User Identification**: Uses environment-based identifiers (`$USER`, `$GITHUB_USER`)
- **No Content Collection**: Never collects actual code, prompts, or responses
- **Repository Context**: Only collects repository names, not content or structure
- **Session IDs**: Uses temporary session identifiers that don't persist

### Security Considerations
- **Internal API Only**: All metrics sent to internal GlossGenius API endpoints
- **Encrypted Transmission**: All data transmission uses HTTPS
- **No Sensitive Data**: Never collects passwords, tokens, or confidential information
- **Opt-out Capability**: Can be disabled through OpenCode configuration

### Compliance
- Follows enterprise privacy standards
- Respects user consent and privacy preferences
- Maintains data retention policies
- Provides transparency in data collection

## Collected Metrics

### Session Metrics
```json
{
  "event": "session.start",
  "user": "anonymized_user_id", 
  "repository": "repository_basename",
  "timestamp": "2024-02-11T10:30:00Z",
  "session_id": "temporary_session_id"
}
```

### Command Metrics
```json
{
  "event": "command.execute",
  "user": "anonymized_user_id",
  "repository": "repository_basename", 
  "command": "git-commit",
  "success": true,
  "duration_ms": 2500,
  "timestamp": "2024-02-11T10:32:15Z"
}
```

### Prompt Metrics
```json
{
  "event": "prompt.submit",
  "user": "anonymized_user_id",
  "repository": "repository_basename",
  "category": "coding_request", 
  "length_chars": 150,
  "timestamp": "2024-02-11T10:31:00Z"
}
```

## Integration Architecture

### Hook-Based Collection
The analytics system integrates with OpenCode through lifecycle hooks:

- **SessionStart Hook**: Automatically triggered when OpenCode sessions begin
- **UserPromptSubmit Hook**: Captures user interaction events
- **PreToolUse Hook**: Records tool usage before execution
- **PostToolUse Hook**: Tracks tool completion and success rates

### API Integration
```bash
# Session tracking endpoint
GET https://api.glossgenius.com/internal/metrics/ai/?user=${user}&repository=${repo}&event=session.start

# Command tracking endpoint  
POST https://api.glossgenius.com/internal/metrics/ai/command
{
  "user": "user_id",
  "repository": "repo_name", 
  "command": "command_name",
  "status": "success|failure",
  "metadata": {}
}
```

### Repository Context
Automatically extracts repository information:
- Git remote origin URLs (anonymized)
- Repository base names (without full paths)
- Project type detection (language, framework)
- No source code or file content collection

## Analytics Insights

### Usage Pattern Analysis
- **Peak Usage Times**: When developers are most active
- **Popular Features**: Most frequently used commands and tools
- **Workflow Efficiency**: Common command sequences and optimizations
- **Error Hotspots**: Areas where users encounter most difficulties

### Performance Metrics
- **Response Times**: How quickly OpenCode responds to requests
- **Success Rates**: Percentage of successful command executions
- **Session Duration**: Average time users spend in sessions
- **Feature Adoption**: Rate of new feature adoption and usage

### User Experience Insights
- **Feature Discovery**: Which features users find and use
- **Learning Curves**: How quickly users adopt new capabilities
- **Pain Points**: Areas where users struggle or encounter errors
- **Satisfaction Indicators**: Engagement levels and return usage

## Implementation Details

### Script Architecture
The analytics system uses lightweight bash scripts for data collection:

- **`publish-session-metric.sh`**: Session lifecycle tracking
- **`publish-command-metric.sh`**: Command execution monitoring  
- **`publish-prompt-metric.sh`**: User interaction analysis
- **`lib/common.sh`**: Shared utilities and helper functions

### Data Processing Pipeline
1. **Collection**: Hooks trigger metric collection scripts
2. **Anonymization**: Scripts anonymize sensitive data
3. **Transmission**: Secure HTTPS POST to internal API
4. **Storage**: Metrics stored in secure, access-controlled database
5. **Analysis**: Aggregate analysis for insights and improvements

### Error Handling
- **Graceful Failures**: Analytics failures never interrupt user workflows
- **Retry Logic**: Implements exponential backoff for network failures
- **Fallback Modes**: Continues operation even if analytics is unavailable
- **Logging**: Maintains internal logs for troubleshooting

## Configuration Options

### Environment Variables
```bash
# Enable/disable analytics collection
export OPENCODE_ANALYTICS_ENABLED=true

# Custom API endpoint (for testing/development)
export OPENCODE_ANALYTICS_ENDPOINT=https://api.example.com/metrics

# User identification override  
export OPENCODE_USER_ID=custom_user_id

# Repository context override
export OPENCODE_REPO_CONTEXT=custom_project_name
```

### Opt-out Configuration
Users can disable analytics through:
- Environment variable: `OPENCODE_ANALYTICS_ENABLED=false`
- Configuration file: `~/.opencode/config.json`
- Command line flag: `--no-analytics`

## Monitoring and Alerting

### System Health Metrics
- **Collection Success Rate**: Percentage of successful metric submissions
- **API Response Times**: Performance of analytics API endpoints
- **Error Rates**: Frequency of collection and transmission errors
- **Data Quality**: Validation of collected metric format and completeness

### Operational Dashboards
- Real-time usage monitoring
- Feature adoption tracking  
- Error rate monitoring
- Performance trend analysis

## Benefits for Development

### Product Improvement
- **Feature Prioritization**: Data-driven decisions on feature development
- **Performance Optimization**: Identify and resolve performance bottlenecks
- **User Experience Enhancement**: Improve workflows based on usage patterns
- **Bug Detection**: Early identification of issues through error tracking

### User Support
- **Proactive Issue Resolution**: Identify problems before they impact users
- **Usage Training**: Develop training materials based on actual usage patterns
- **Feature Guidance**: Help users discover and adopt powerful features
- **Success Metrics**: Measure impact of improvements and new features

## Technical Requirements

### Dependencies
- **Bash**: Shell scripting environment
- **curl**: HTTP client for API communication
- **jq**: JSON processing for data manipulation
- **Git**: Repository context extraction

### Network Requirements
- HTTPS access to internal API endpoints
- Reliable internet connectivity for metric transmission
- Firewall configuration for API access

### System Integration
- Compatible with OpenCode hook system
- Minimal performance impact on user workflows
- Graceful degradation when analytics unavailable
- Cross-platform compatibility (macOS, Linux, Windows)