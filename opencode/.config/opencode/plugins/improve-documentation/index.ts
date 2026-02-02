import type { Plugin } from "@opencode-ai/plugin"

export const ImproveDocumentationPlugin: Plugin = async ({ project, client, $, directory, worktree }) => {
  const pluginName = "improve-documentation"
  
  await client.app.log({
    body: {
      service: pluginName,
      level: "info",
      message: "ImproveDocumentationPlugin initialized",
      extra: { directory, worktree }
    }
  })

  return {
    "tui.command.execute": async (input, output) => {
      if (input.command === "/improve-docs" || input.command === "/improve-documentation") {
        await client.app.log({
          body: {
            service: pluginName,
            level: "info",
            message: "Starting documentation improvement process"
          }
        })

        // Send the improvement task to the AI
        await client.message.create({
          body: {
            text: `Please help improve the documentation for protobuf changes in this project.

## Context
- Versioning is managed through \`git\`.
- Best practices and guidelines are in \`docs/CONTRIBUTING.md\`.
- Linter rules are in \`linter/linter.py\`.
- Protobuf files are in \`src/\`.

## Your task
1. Identify the changes made on the local branch by comparing them from \`main\`.
2. If needed, write or improve the documentation of the identified changes.
3. If context is required, ask the user for clarifications before making the changes.
4. If a field name does not match the documentation or seems incorrect:
   a. If you can't reason about the change, ask the user for clarification.
   b. If the change seems straightforward, make a suggestion.

Please start by examining the current git status and recent changes.`,
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
        
        // Allow only specific git commands for documentation improvement
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
            throw new Error(`Git command not allowed for documentation improvement: ${command}. Allowed commands: ${allowedGitCommands.join(", ")}`)
          }
        }
      }
    },

    "session.created": async (input) => {
      // Log when a new session starts that might use this plugin
      await client.app.log({
        body: {
          service: pluginName,
          level: "debug", 
          message: "New session created, documentation improvement plugin ready"
        }
      })
    }
  }
}

export default ImproveDocumentationPlugin