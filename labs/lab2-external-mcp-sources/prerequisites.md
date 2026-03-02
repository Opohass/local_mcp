# Lab 2 Prerequisites

## Required

- Node.js 18+ and npm (`npx` must be available)
- Claude Code CLI or VS Code with Copilot

## For GitHub MCP Server

- A GitHub Personal Access Token with `repo` scope
- Set it as an environment variable: `export GITHUB_TOKEN=ghp_...`
- Create one at: https://github.com/settings/tokens

## Verify

```bash
node --version    # Should be 18+
npx --version     # Should work
echo $GITHUB_TOKEN  # Should show your token (if using GitHub MCP)
```
