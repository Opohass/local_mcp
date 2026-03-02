# Global Prerequisites

## Required for All Labs

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.11+ | [python.org](https://www.python.org/downloads/) or `brew install python@3.11` |
| pip | Latest | Included with Python |
| Git | Any | `sudo apt install git` / `brew install git` |
| VS Code | Latest | [code.visualstudio.com](https://code.visualstudio.com/) |
| Claude Code CLI | Latest | `npm install -g @anthropic-ai/claude-code` |

## Recommended

| Tool | Purpose | Install |
|------|---------|---------|
| uv | Fast Python package manager | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Node.js + npm | Required for Lab 2 external servers | [nodejs.org](https://nodejs.org/) |

## Setup

```bash
# Clone the repository
git clone <repo-url>
cd local_mcp

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install base dependencies
pip install -e .

# Install with notebook support
pip install -e ".[notebooks]"

# Install all optional dependencies
pip install -e ".[notebooks,dev]"
```

## Lab-Specific Prerequisites

- **Lab 1**: No additional requirements beyond the base setup.
- **Lab 2**: Node.js + npm (for running external MCP servers via `npx`).
- **Lab 3**: Azure subscription, Azure CLI (`az`), Docker. See [lab3 prerequisites](../lab3-azure-deployment/prerequisites.md).

## Verify Your Setup

```bash
python --version          # Should be 3.11+
pip show fastmcp          # Should show fastmcp package info
claude --version          # Claude Code CLI
code --version            # VS Code
```
