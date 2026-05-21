# Lab 2 Prerequisites

## Required

- Node.js 18+ and npm (`npx` must be available)
- Claude Code CLI or VS Code with Copilot

## For GitHub MCP Server

- A GitHub Personal Access Token with `repo` scope
- Create one at: https://github.com/settings/tokens
- Set it as an environment variable:

**Linux / macOS**
```bash
export GITHUB_TOKEN=ghp_...
```

**Windows (PowerShell)**
```powershell
$env:GITHUB_TOKEN = "ghp_..."
```

## Verify

**Linux / macOS**
```bash
node --version      # Should be 18+
npx --version       # Should work
echo $GITHUB_TOKEN  # Should show your token (if using GitHub MCP)
```

**Windows (PowerShell)**
```powershell
node --version       # Should be 18+
npx --version        # Should work
$env:GITHUB_TOKEN    # Should show your token (if using GitHub MCP)
```
