import type { Plugin } from "@opencode-ai/plugin"

export const ProtobufNewPlugin: Plugin = async ({ project, client, $, directory, worktree }) => {
  const pluginName = "protobuf-new"
  
  await client.app.log({
    body: {
      service: pluginName,
      level: "info",
      message: "ProtobufNewPlugin initialized",
      extra: { directory, worktree }
    }
  })

  return {
    "tui.command.execute": async (input, output) => {
      if (input.command === "/proto-new" || input.command === "/protobuf-new" || input.command === "/new-proto") {
        await client.app.log({
          body: {
            service: pluginName,
            level: "info",
            message: "Starting new protobuf creation process"
          }
        })

        // Send the creation task to the AI
        await client.message.create({
          body: {
            text: `I'll help you create new protobuf methods, messages, or services following best practices.

## Context
- Best practices and guidelines are in \`docs/CONTRIBUTING.md\`.
- Services are stored in \`src/com/glossgenius/services/\`.

## Process I'll follow:

1. **Ask for details**: I need to understand what you want to create. Please provide an example like: "I want to create a new method on core-users that searches for users by email."

2. **Validate against guidelines**: I'll check if your request follows the contribution guidelines and ask clarifying questions if needed.

3. **Check for duplicates**: I'll search through existing protobuf definitions to verify your request isn't already handled. If it exists, I'll provide the links and code samples.

4. **Gather additional details**: If I need more information as we work through the task, I'll ask proactive questions with suggestions.

5. **Token type suggestion**: If you're creating a new message type with a field named exactly \`token\` (e.g., \`string token\`), I'll ask if you want to create a new token type for this resource. If you confirm, I'll suggest running the \`/new-token\` command to create the token prefix, Kotlin class, and registration.

What would you like me to create? Please describe the protobuf method, message, or service you need.`,
            role: "user"
          }
        })

        output.handled = true
      }
    },

    "tool.execute.before": async (input, output) => {
      // Restrict git operations to safe commands as per original skill
      if (input.tool === "bash" && output.args.command) {
        const command = output.args.command.toLowerCase()
        
        // Allow only specific git commands for protobuf creation
        const allowedGitCommands = [
          "git add",
          "git status", 
          "git commit"
        ]
        
        const isGitCommand = command.startsWith("git ")
        if (isGitCommand) {
          const isAllowedGitCommand = allowedGitCommands.some(allowed => 
            command.startsWith(allowed.toLowerCase())
          )
          
          if (!isAllowedGitCommand) {
            throw new Error(`Git command not allowed for protobuf creation: ${command}. Allowed commands: ${allowedGitCommands.join(", ")}`)
          }
        }
      }
    },

    "file.edited": async (input) => {
      // Log when protobuf files are edited
      if (input.filePath.endsWith('.proto')) {
        await client.app.log({
          body: {
            service: pluginName,
            level: "info",
            message: "Protobuf file edited",
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
          message: "New session created, protobuf creation plugin ready"
        }
      })
    }
  }
}

export default ProtobufNewPlugin