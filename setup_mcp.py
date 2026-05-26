"""Generate MCP config files so VS Code Copilot Chat and Claude Code auto-detect the meta MCP server.

Run:
    python setup_mcp.py

Writes:
    .vscode/mcp.json - VS Code Copilot Chat schema (https://code.visualstudio.com/docs/copilot/reference/mcp-configuration)
    .mcp.json        - Claude Code project schema (https://code.claude.com/docs/en/mcp)

Each file contains a single server entry whose paths are fitted to the host OS
at generation time (Windows uses `.venv\\Scripts\\python.exe`; Linux/macOS use
`.venv/bin/python`).
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.resolve()
SERVER_SCRIPT_REL = "meta_server/lab_content_server.py"
VENV_DIR = REPO_ROOT / ".venv"
VSCODE_MCP_JSON = REPO_ROOT / ".vscode" / "mcp.json"
CLAUDE_MCP_JSON = REPO_ROOT / ".mcp.json"
SERVER_NAME = "mcp-hol-assistant"

IS_WINDOWS = sys.platform == "win32"
SEP = "\\" if IS_WINDOWS else "/"
VENV_PYTHON_REL = SEP.join([".venv", "Scripts", "python.exe"]) if IS_WINDOWS else ".venv/bin/python"
SERVER_SCRIPT_OS = SERVER_SCRIPT_REL.replace("/", SEP)


def relative_with_dot(path: str) -> str:
    """Prefix a relative path with the OS-appropriate `./` so it's unambiguous."""
    return f".{SEP}{path}"


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {path.relative_to(REPO_ROOT)}")


def main() -> None:
    if not (REPO_ROOT / SERVER_SCRIPT_REL).exists():
        sys.exit(f"Server script not found: {REPO_ROOT / SERVER_SCRIPT_REL}")
    if not (VENV_DIR / VENV_PYTHON_REL.replace("\\", "/").split("/", 1)[1]).exists():
        sys.exit(f"Project venv not found at {VENV_DIR}. Create it before running this script.")

    command = relative_with_dot(VENV_PYTHON_REL)
    args = [relative_with_dot(SERVER_SCRIPT_OS)]

    # VS Code Copilot Chat: top-level "servers", per-entry "type: stdio".
    vscode_config = {
        "servers": {
            SERVER_NAME: {
                "type": "stdio",
                "command": command,
                "args": args,
            }
        }
    }

    # Claude Code: top-level "mcpServers". Servers spawn with CWD = project root,
    # so the same relative paths work without variable expansion.
    claude_config = {
        "mcpServers": {
            SERVER_NAME: {
                "command": command,
                "args": args,
            }
        }
    }

    write_json(VSCODE_MCP_JSON, vscode_config)
    write_json(CLAUDE_MCP_JSON, claude_config)


if __name__ == "__main__":
    main()
