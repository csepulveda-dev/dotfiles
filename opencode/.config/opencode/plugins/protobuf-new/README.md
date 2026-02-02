# Protobuf New Plugin

An OpenCode plugin that helps create new protobuf methods, messages, or services following best practices and verifying no duplication exists in existing definitions.

## Overview

This plugin is converted from a Claude Skills system and provides guided creation of protobuf definitions. It ensures best practices are followed and prevents duplicate implementations.

## Features

- **Interactive Creation**: Guides you through creating protobuf methods, messages, and services
- **Duplication Detection**: Searches existing definitions to prevent duplicates
- **Best Practice Enforcement**: Follows project guidelines and contribution standards
- **Token Integration**: Suggests creating token types when appropriate
- **Safety Controls**: Restricts git operations to safe commands only
- **File Monitoring**: Tracks protobuf file changes for logging

## Installation

### From Local Files

1. Copy this plugin directory to your OpenCode plugins folder:
   ```bash
   cp -r protobuf-new ~/.config/opencode/plugins/
   ```

2. The plugin will be automatically loaded on next OpenCode startup.

### From Project

1. Copy this plugin directory to your project's plugins folder:
   ```bash
   cp -r protobuf-new .opencode/plugins/
   ```

## Usage

### Commands

- `/proto-new` - Start the protobuf creation process
- `/protobuf-new` - Alternative command name
- `/new-proto` - Another alternative command name

### What it does

1. **Collects Requirements**: Asks what you want to create with examples
2. **Validates Guidelines**: Checks against contribution guidelines
3. **Searches for Duplicates**: Scans existing protobuf definitions
4. **Gathers Details**: Asks clarifying questions with proactive suggestions
5. **Token Integration**: Suggests creating token types when appropriate
6. **Creates Files**: Generates the protobuf definitions following best practices

### Example Workflow

```
/proto-new
```

Then describe what you want:
- "I want to create a new method on core-users that searches for users by email"
- "I need a new message type for storing user preferences"
- "Create a new service for handling notifications"

### Token Integration

If your new message includes a `token` field, the plugin will ask if you want to create a new token type and suggest running the `/new-token` command to:
- Create token prefix
- Generate Kotlin class  
- Add registration

## Project Structure

The plugin expects your project to have:
- `docs/CONTRIBUTING.md` - Best practices and guidelines
- `src/com/glossgenius/services/` - Services directory
- Git repository for version control

## Safety Features

- **Restricted Git Commands**: Only allows `git add`, `git status`, and `git commit`
- **File Monitoring**: Tracks protobuf file edits
- **Error Prevention**: Blocks potentially harmful operations
- **Comprehensive Logging**: Detailed logs for debugging and monitoring

## Example Interactions

### Creating a User Search Method

```
User: I want to create a new method on core-users that searches for users by email
Plugin: I'll help you create this method. Let me first check existing definitions...
```

### Creating a New Message Type

```
User: Create a message for user notifications with a token field  
Plugin: I'll create the message. Since you mentioned a token field, would you like me to also create a new token type for this resource?
```

## Integration with Other Plugins

This plugin works well with:
- `new-token` plugin for token creation
- `improve-documentation` plugin for documentation review

## License

MIT License