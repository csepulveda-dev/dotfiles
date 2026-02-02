# Token Creator Plugin

An OpenCode plugin that creates new resource token prefixes by registering them in protobuf definitions, generating Kotlin token classes, and running tests.

## Overview

This plugin is converted from a Claude Skills system and provides end-to-end token creation for projects using protobuf and Kotlin. It handles the complete workflow from protobuf registration to Kotlin class generation and test execution.

## Features

- **Complete Token Workflow**: Handles the entire token creation process
- **Protobuf Integration**: Registers tokens in `token_prefix.proto`
- **Kotlin Class Generation**: Creates Kotlin token classes in proper domains
- **Token Registration**: Adds tokens to `TokenResource.kt`
- **Test Execution**: Runs Gradle tests to verify implementation
- **Safety Controls**: Restricts operations to safe commands only
- **File Monitoring**: Tracks token-related file changes

## Installation

### From Local Files

1. Copy this plugin directory to your OpenCode plugins folder:
   ```bash
   cp -r token-creator ~/.config/opencode/plugins/
   ```

2. The plugin will be automatically loaded on next OpenCode startup.

### From Project

1. Copy this plugin directory to your project's plugins folder:
   ```bash
   cp -r token-creator .opencode/plugins/
   ```

## Usage

### Commands

- `/new-token` - Start the token creation process
- `/create-token` - Alternative command name
- `/token-new` - Another alternative command name

### What it does

1. **Asks for Token Name**: Collects the name of the token to create
2. **Gets Description**: Suggests or asks for a token description
3. **Determines Domain**: Proposes or asks for the domain name
4. **Creates Token Prefix**: Registers in `token_prefix.proto`
5. **Generates Kotlin Class**: Creates class in the corresponding domain
6. **Registers Token**: Adds to `TokenResource.kt`
7. **Runs Tests**: Executes `./gradlew test` to verify everything works

### Example Workflow

```
/new-token
```

Follow the interactive prompts:
1. **Token Name**: "UserSession"
2. **Description**: "Token for user session management"
3. **Domain**: "users" (or suggest based on name)
4. **Implementation**: Plugin handles all file creation and registration
5. **Testing**: Automatically runs test suite

## Project Structure

The plugin expects your project to have:
- `src/com.glossgenius/tokens/token_prefix.proto` - Token prefix definitions
- `packages/kotlin/src/main/kotlin/com/glossgenius/core/libs/tokens/domains/` - Domain directories
- `packages/kotlin/src/main/kotlin/com/glossgenius/core/libs/tokens/TokenResource.kt` - Token registration
- Gradle build system with test support

### Domain Structure

Token classes are organized by domain:
```
packages/kotlin/src/main/kotlin/com/glossgenius/core/libs/tokens/domains/
├── users/
├── appointments/
├── payments/
└── ... (other domains)
```

## Safety Features

- **Restricted Commands**: Only allows safe git operations and gradle test
- **File Monitoring**: Tracks edits to token-related files
- **Test Verification**: Ensures tests pass after token creation
- **Error Prevention**: Blocks potentially harmful operations
- **Comprehensive Logging**: Detailed logs for debugging and monitoring

## Test Integration

The plugin automatically runs:
```bash
cd packages/kotlin && ./gradlew test
```

This ensures:
- Token classes compile correctly
- No conflicts with existing tokens
- All tests continue to pass

## Example Token Creation

### Input
- **Name**: "OrderTracking"
- **Description**: "Token for tracking customer orders"
- **Domain**: "orders"

### Generated Files

**token_prefix.proto**:
```protobuf
enum TokenPrefix {
  // ... existing tokens
  ORDER_TRACKING = 42;
}
```

**orders/OrderTrackingToken.kt**:
```kotlin
package com.glossgenius.core.libs.tokens.domains.orders

class OrderTrackingToken : BaseToken {
  // Implementation
}
```

**TokenResource.kt**:
```kotlin
// Updated with OrderTrackingToken registration
```

## Integration with Other Plugins

This plugin works well with:
- `protobuf-new` plugin (which can suggest running `/new-token`)
- `improve-documentation` plugin for documentation review

## Troubleshooting

### Tests Fail After Creation
- Check for naming conflicts with existing tokens
- Verify domain structure matches expectations
- Review generated Kotlin class for syntax errors

### Token Not Registered
- Ensure `TokenResource.kt` was properly updated
- Check that the domain directory exists
- Verify protobuf compilation succeeds

## License

MIT License