# Lab 1 Prerequisites

## Required

- Python 3.11+ with virtual environment activated
- `fastmcp` package installed (`pip install -e .` from repo root)
- Claude Code CLI or VS Code with Copilot (at least one)

## Optional

- SSH access to a remote machine (for testing `run_remote_command`)
- `lsof` command available (for `port_checker` process identification — Linux/macOS only)

## Verify

```bash
python -c "import fastmcp; print(f'FastMCP {fastmcp.__version__}')"
```
