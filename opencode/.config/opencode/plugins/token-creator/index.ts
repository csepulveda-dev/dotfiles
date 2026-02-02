import type { Plugin } from "@opencode-ai/plugin"

export const TokenCreatorPlugin: Plugin = async ({ project, client, $, directory, worktree }) => {
  const pluginName = "token-creator"
  
  await client.app.log({
    body: {
      service: pluginName,
      level: "info",
      message: "TokenCreatorPlugin initialized",
      extra: { directory, worktree }
    }
  })

  return {
    "tui.command.execute": async (input, output) => {
      if (input.command === "/new-token" || input.command === "/create-token" || input.command === "/token-new") {
        await client.app.log({
          body: {
            service: pluginName,
            level: "info",
            message: "Starting token creation process"
          }
        })

        // Send the token creation task to the AI
        await client.message.create({
          body: {
            text: `I'll help you create a new resource token prefix with all the necessary registrations and tests.

## Context
- Versioning is managed through \`git\`.
- Token prefixes are registered in \`src/com.glossgenius/tokens/token_prefix.proto\`.
- Kotlin Token classes are in \`packages/kotlin/src/main/kotlin/com/glossgenius/core/libs/tokens/domains\` under their corresponding domain.
- Token classes are recorded in \`packages/kotlin/src/main/kotlin/com/glossgenius/core/libs/tokens/TokenResource.kt\`.
- Domains are directories under \`packages/kotlin/src/main/kotlin/com/glossgenius/core/libs/tokens/domains/\`.
- Running tests can be done by \`cd packages/kotlin && ./gradlew test\`.

## Process I'll follow:

1. **Ask for token name**: What's the name of the token you're trying to create?

2. **Get description**: Based on the name, I'll suggest a short description or ask you for one.

3. **Determine domain**: I'll propose a domain or ask you for the domain name.

4. **Create token prefix**: Register the token in \`token_prefix.proto\`.

5. **Generate Kotlin class**: Create the Kotlin class in the corresponding domain.

6. **Register token**: Add the token to \`TokenResource.kt\`.

7. **Run tests**: Execute the test suite to ensure everything works.

What's the name of the token you want to create? Please provide a descriptive name for the new token type.`,
            role: "user"
          }
        })

        output.handled = true
      }
    },

    "tool.execute.before": async (input, output) => {
      // Restrict operations to safe commands and allow gradle test execution
      if (input.tool === "bash" && output.args.command) {
        const command = output.args.command.toLowerCase()
        
        // Allow specific git commands and gradle test
        const allowedCommands = [
          "git add",
          "git status", 
          "git commit",
          "cd packages/kotlin && ./gradlew test",
          "./gradlew test"
        ]
        
        // Check for gradle test commands (more flexible matching)
        const isGradleTest = command.includes("gradlew test") || command.includes("gradle test")
        const isGitCommand = command.startsWith("git ")
        
        if (isGitCommand) {
          const allowedGitCommands = ["git add", "git status", "git commit"]
          const isAllowedGitCommand = allowedGitCommands.some(allowed => 
            command.startsWith(allowed.toLowerCase())
          )
          
          if (!isAllowedGitCommand) {
            throw new Error(`Git command not allowed for token creation: ${command}. Allowed commands: ${allowedGitCommands.join(", ")}`)
          }
        } else if (isGradleTest) {
          // Allow gradle test commands
          await client.app.log({
            body: {
              service: pluginName,
              level: "info",
              message: "Allowing gradle test execution",
              extra: { command }
            }
          })
        } else {
          // Check if command is in allowed list
          const isAllowedCommand = allowedCommands.some(allowed => 
            command.includes(allowed.toLowerCase())
          )
          
          if (!isAllowedCommand && (command.includes("gradle") || command.includes("gradlew"))) {
            throw new Error(`Gradle command not allowed for token creation: ${command}. Only 'gradlew test' is allowed.`)
          }
        }
      }
    },

    "tool.execute.after": async (input, output) => {
      // Log completion of test runs
      if (input.tool === "bash" && input.args.command?.includes("gradlew test")) {
        await client.app.log({
          body: {
            service: pluginName,
            level: "info",
            message: "Gradle test execution completed",
            extra: { 
              success: !output.error,
              exitCode: output.exitCode 
            }
          }
        })
      }
    },

    "file.edited": async (input) => {
      // Log when token-related files are edited
      const tokenRelatedPaths = [
        "token_prefix.proto",
        "TokenResource.kt",
        "/tokens/domains/"
      ]
      
      if (tokenRelatedPaths.some(path => input.filePath.includes(path))) {
        await client.app.log({
          body: {
            service: pluginName,
            level: "info",
            message: "Token-related file edited",
            extra: { filePath: input.filePath }
          }
        })
      }
    },

    "session.created": async (input) => {
      // Log when a new session starts
      await client.app.log({
        body: {
          service: pluginName,
          level: "debug", 
          message: "New session created, token creation plugin ready"
        }
      })
    }
  }
}

export default TokenCreatorPlugin