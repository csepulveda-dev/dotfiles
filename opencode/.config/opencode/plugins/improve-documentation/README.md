# Improve Documentation Plugin

An OpenCode plugin that helps review local protobuf changes and improve documentation quality, ensuring field names and descriptions accurately reflect their purpose.

## Overview

This plugin is converted from a Claude Skills system and provides automated documentation improvement for protobuf files. It analyzes git changes and helps maintain high-quality documentation standards.

## Features

- **Git Integration**: Analyzes changes between local branch and main
- **Documentation Review**: Identifies areas where documentation can be improved
- **Safety Controls**: Restricts git operations to safe commands only
- **Interactive Guidance**: Asks for clarification when changes are unclear
- **Best Practice Enforcement**: Follows project guidelines and linter rules

## Installation

### From Local Files

1. Copy this plugin directory to your OpenCode plugins folder:
   ```bash
   cp -r improve-documentation ~/.config/opencode/plugins/
   ```

2. The plugin will be automatically loaded on next OpenCode startup.

### From Project

1. Copy this plugin directory to your project's plugins folder:
   ```bash
   cp -r improve-documentation .opencode/plugins/
   ```

## Usage

### Commands

- `/improve-docs` - Start the documentation improvement process
- `/improve-documentation` - Alternative command name

### What it does

1. **Identifies Changes**: Compares current branch with main to find modified protobuf files
2. **Reviews Documentation**: Analyzes field names, descriptions, and overall documentation quality
3. **Provides Suggestions**: Offers improvements or asks for clarification
4. **Safe Operations**: Only allows safe git operations (add, status, commit)

### Example Workflow

```
/improve-docs
```

The plugin will:
1. Check git status for changes
2. Compare with main branch to identify modifications
3. Analyze protobuf files for documentation issues
4. Suggest improvements or request clarification
5. Help commit improved documentation

## Configuration

The plugin expects your project to have:
- `docs/CONTRIBUTING.md` - Best practices and guidelines
- `linter/linter.py` - Linter rules
- `src/` - Directory containing protobuf files
- Git repository with `main` branch

## Safety Features

- **Restricted Git Commands**: Only allows `git add`, `git status`, and `git commit`
- **Error Prevention**: Blocks potentially harmful git operations
- **Logging**: Comprehensive logging for debugging and monitoring

## Original Context

This plugin is based on the Claude Skills system with the following original context:
- Versioning managed through `git`
- Best practices in `docs/CONTRIBUTING.md`
- Linter rules in `linter/linter.py`
- Protobuf files in `src/`

## License

MIT License