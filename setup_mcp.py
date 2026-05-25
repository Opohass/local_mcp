"""Generate .vscode/mcp.json so GitHub Copilot Chat auto-detects the meta MCP server.

Run:
    python setup_mcp.py

Writes a config matching the official VS Code MCP schema:
    https://code.visualstudio.com/docs/copilot/reference/mcp-configuration
"""

import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.resolve()
SERVER_SCRIPT = REPO_ROOT / "meta_server" / "lab_content_server.py"
VENV_DIR = REPO_ROOT / ".venv"
VSCODE_DIR = REPO_ROOT / ".vscode"
MCP_JSON = VSCODE_DIR / "mcp.json"
SERVER_NAME = "mcp-hol-assistant"


def pick_python_command() -> str:
    """Pick the Python interpreter VS Code should launch.

    Prefers a project-local `.venv` (which is where fastmcp is installed).
    The venv layout differs by OS: Windows uses `Scripts/python.exe`,
    Linux/macOS use `bin/python`. We emit the path using ${workspaceFolder}
    so the resulting JSON is workspace-relative.
    """
    is_windows = sys.platform == "win32"
    venv_python = VENV_DIR / ("Scripts/python.exe" if is_windows else "bin/python")
    if venv_python.exists():
        return "${workspaceFolder}/.venv/" + ("Scripts/python.exe" if is_windows else "bin/python")

    candidates = ["python", "python3"] if is_windows else ["python3", "python"]
    for cmd in candidates:
        if shutil.which(cmd):
            return cmd
    return candidates[0]


def main() -> None:
    if not SERVER_SCRIPT.exists():
        sys.exit(f"Server script not found: {SERVER_SCRIPT}")

    VSCODE_DIR.mkdir(exist_ok=True)

    config = {
        "servers": {
            SERVER_NAME: {
                "type": "stdio",
                "command": pick_python_command(),
                "args": ["${workspaceFolder}/meta_server/lab_content_server.py"],
            }
        }
    }

    MCP_JSON.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {MCP_JSON.relative_to(REPO_ROOT)} (command: {config['servers'][SERVER_NAME]['command']})")


if __name__ == "__main__":
    main()
