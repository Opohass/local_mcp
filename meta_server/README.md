# Meta Server: Labs as MCP

This MCP server exposes all lab content as tools and resources, so you can ask your AI assistant questions about the labs themselves.

## How It Works

The server scans the `labs/` directory and provides:

**Resources** (read-only data):
- `labs://overview` — Main README
- `labs://prerequisites` — Global prerequisites
- `labs://troubleshooting` — Troubleshooting guide

**Tools** (searchable/queryable):
- `list_labs()` — List all available labs
- `get_lab_content(lab_id, file_type)` — Read lab README, prerequisites, notebook, or any file
- `search_lab_content(query, lab_id)` — Search across lab docs
- `get_lab_prerequisites(lab_id)` — Get prerequisites for a specific lab

## Usage

### Automatic (Claude Code)

If you opened this repo in Claude Code, the meta server is already configured via `.mcp.json`. Just ask:

- *"What labs are available?"*
- *"What are the prerequisites for lab 3?"*
- *"Search for 'Docker' across all labs"*
- *"Show me the code for the STDIO server in lab 1"*

### Manual

```bash
python meta_server/lab_content_server.py
```
