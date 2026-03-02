# MCP Hands-on Lab (HOL)

A hands-on workshop for learning **Model Context Protocol (MCP)** — the open standard that connects AI assistants to your tools, data, and services.

## What You'll Learn

| Lab | Topic | What You Build |
|-----|-------|---------------|
| **Presentation** | MCP concepts, architecture, transports | — |
| **Lab 1** | Local MCP Servers | Python STDIO + HTTP servers with dev tools & review prompts |
| **Lab 2** | External MCP Sources | Connect GitHub, Filesystem, and Fetch servers |
| **Lab 3** | Azure Deployment | Deploy to Azure Container Apps + connect to AI Foundry agents |

## Quick Start

```bash
# Clone and install
git clone <repo-url> && cd local_mcp
python -m venv .venv && source .venv/bin/activate
pip install -e ".[notebooks]"

# Run the presentation
cd presentation && python -m http.server 8080

# Start Lab 1
jupyter notebook labs/lab1-local-mcp-servers/lab1_notebook.ipynb
```

## Prerequisites

See [labs/shared/prerequisites.md](labs/shared/prerequisites.md) for full requirements.

**Minimum**: Python 3.11+, pip, a code editor (VS Code recommended), Claude Code CLI.

## Repository Structure

```
local_mcp/
├── presentation/          # Reveal.js interactive slide deck
├── labs/
│   ├── shared/            # Prerequisites, troubleshooting, utilities
│   ├── lab1-local-mcp-servers/    # Build local STDIO + HTTP MCP servers
│   ├── lab2-external-mcp-sources/ # Connect to community MCP servers
│   └── lab3-azure-deployment/     # Deploy to Azure + AI Foundry
└── meta_server/           # This repo as an MCP server (ask questions about the labs!)
```

## Meta Server

This repo includes an MCP server that lets you ask AI assistants questions about the lab content itself. If you open this repo in Claude Code, the meta server is auto-configured in `.mcp.json`.

```bash
# Or run it manually
python meta_server/lab_content_server.py
```
