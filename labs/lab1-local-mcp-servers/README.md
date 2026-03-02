# Lab 1: Local MCP Servers

## Objectives

By the end of this lab you will be able to:

1. Create an MCP server in Python using FastMCP
2. Understand the difference between STDIO and HTTP transports
3. Connect your MCP server to Claude Code and VS Code
4. Use MCP tools (executable functions) and prompts (review contexts)

## What You'll Build

A dev tools MCP server with:

**Tools** (3):
- `run_remote_command` — Execute commands on remote machines via SSH
- `file_tree` — Generate clean directory tree listings
- `port_checker` — Check which dev ports are in use

**Prompts** (4):
- `code_review` — Code review checklist
- `security_review` — Security-focused review criteria
- `design_review` — Architecture review criteria
- `networking_review` — Network configuration review guide

## Files

| File | Description |
|------|-------------|
| `servers/dev_tools_stdio.py` | MCP server using STDIO transport (local) |
| `servers/dev_tools_http.py` | Same server using HTTP transport (network-accessible) |
| `configs/mcp.json` | Claude Code configuration template |
| `configs/vscode_mcp.json` | VS Code configuration template |
| `lab1_notebook.ipynb` | Step-by-step Jupyter walkthrough |

## Quick Start (without notebook)

```bash
# Activate your virtual environment
source .venv/bin/activate

# Test the STDIO server
python labs/lab1-local-mcp-servers/servers/dev_tools_stdio.py

# Test the HTTP server
python labs/lab1-local-mcp-servers/servers/dev_tools_http.py
# → Server at http://localhost:9000

# Connect to Claude Code
cp labs/lab1-local-mcp-servers/configs/mcp.json .mcp.json
claude  # Tools should appear automatically
```

## Estimated Time

45-60 minutes (following the notebook)
