# Lab 2: External MCP Sources

## Objectives

By the end of this lab you will be able to:

1. Find and evaluate MCP servers from community registries
2. Configure external MCP servers in Claude Code and VS Code
3. Combine multiple MCP servers in a single configuration
4. Understand security implications of connecting external tools

## What You'll Connect

| Server | Provider | What It Does |
|--------|----------|-------------|
| Filesystem MCP | Official (Anthropic) | Read, write, and search files through MCP |
| GitHub MCP | GitHub | Search repos, read files, manage issues/PRs |
| Fetch MCP | Official (Anthropic) | Fetch and parse web pages |

## Files

| File | Description |
|------|-------------|
| `configs/mcp_external.json` | Claude Code config with all external servers |
| `configs/vscode_mcp_external.json` | VS Code config with all external servers |
| `external_servers.md` | Catalog of useful external MCP servers |
| `lab2_notebook.ipynb` | Step-by-step Jupyter walkthrough |

## Quick Start (without notebook)

```bash
# Copy the external config to your project root
cp labs/lab2-external-mcp-sources/configs/mcp_external.json .mcp.json

# Make sure npm/npx is available (for JS-based servers)
npx --version

# Start Claude Code
claude
```

## Prerequisites

Before you begin, ensure you have the following installed and configured:

- Node.js 18+ and npm (so that `npx` is available)
- If you plan to use the GitHub MCP server, create a GitHub Personal Access Token with `repo` scope and set it in your environment:

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

See `prerequisites.md` for full details.

## Estimated Time

30-45 minutes
