"""
Meta MCP Server: Labs as MCP

Exposes all lab content as MCP resources and tools so students can
ask AI assistants questions about the labs themselves.

Usage:
    python meta_server/lab_content_server.py

Auto-configured in the repo root .mcp.json for Claude Code.
"""

import json
from pathlib import Path

from fastmcp import FastMCP

REPO_ROOT = Path(__file__).parent.parent.resolve()
LABS_DIR = REPO_ROOT / "labs"

mcp = FastMCP("mcp-hol-assistant")

# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------


@mcp.resource("labs://overview")
def get_overview() -> str:
    """Returns the main repository README."""
    readme = REPO_ROOT / "README.md"
    return readme.read_text() if readme.exists() else "README.md not found."


@mcp.resource("labs://prerequisites")
def get_global_prerequisites() -> str:
    """Returns the global prerequisites document."""
    prereqs = LABS_DIR / "shared" / "prerequisites.md"
    return prereqs.read_text() if prereqs.exists() else "Prerequisites not found."


@mcp.resource("labs://troubleshooting")
def get_troubleshooting() -> str:
    """Returns the troubleshooting guide."""
    guide = LABS_DIR / "shared" / "troubleshooting.md"
    return guide.read_text() if guide.exists() else "Troubleshooting guide not found."


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def list_labs() -> str:
    """List all available labs with their titles and descriptions."""
    labs = []
    for lab_dir in sorted(LABS_DIR.iterdir()):
        if not lab_dir.is_dir() or lab_dir.name.startswith(".") or lab_dir.name == "shared":
            continue
        readme = lab_dir / "README.md"
        title = lab_dir.name
        description = ""
        if readme.exists():
            lines = readme.read_text().splitlines()
            if lines:
                title = lines[0].lstrip("# ").strip()
            for line in lines[1:]:
                if line.strip() and not line.startswith("#"):
                    description = line.strip()
                    break
        labs.append(f"- **{lab_dir.name}**: {title}\n  {description}")
    return "\n\n".join(labs) if labs else "No labs found."


@mcp.tool()
def get_lab_content(lab_id: str, file_type: str = "readme") -> str:
    """Get content from a specific lab.

    Args:
        lab_id: Lab directory name (e.g., 'lab1-local-mcp-servers').
        file_type: Type of content to retrieve: 'readme', 'prerequisites', 'notebook', or a filename.
    """
    lab_dir = LABS_DIR / lab_id
    if not lab_dir.is_dir():
        available = [d.name for d in LABS_DIR.iterdir() if d.is_dir() and d.name != "shared"]
        return f"Lab '{lab_id}' not found. Available labs: {', '.join(available)}"

    file_map = {
        "readme": lab_dir / "README.md",
        "prerequisites": lab_dir / "prerequisites.md",
    }

    # Check for notebook
    if file_type == "notebook":
        notebooks = list(lab_dir.glob("*.ipynb"))
        if notebooks:
            nb = json.loads(notebooks[0].read_text())
            cells_text = []
            for cell in nb.get("cells", []):
                source = "".join(cell.get("source", []))
                if cell.get("cell_type") == "markdown":
                    cells_text.append(source)
                elif cell.get("cell_type") == "code":
                    cells_text.append(f"```python\n{source}\n```")
            return "\n\n---\n\n".join(cells_text)
        return f"No notebook found in {lab_id}."

    # Check file map
    if file_type in file_map:
        path = file_map[file_type]
        return path.read_text() if path.exists() else f"{file_type} not found in {lab_id}."

    # Try as filename — search in subdirectories
    for path in lab_dir.rglob(file_type):
        if path.is_file():
            return path.read_text()
    return f"File '{file_type}' not found in {lab_id}."


@mcp.tool()
def search_lab_content(query: str, lab_id: str = "") -> str:
    """Search across all lab documentation for a keyword or phrase.

    Args:
        query: Search term (case-insensitive).
        lab_id: Optional lab directory name to limit search scope.
    """
    search_dir = LABS_DIR / lab_id if lab_id else LABS_DIR
    if not search_dir.is_dir():
        return f"Directory '{lab_id}' not found."

    results = []
    for path in search_dir.rglob("*"):
        if path.suffix not in (".md", ".py", ".json", ".toml") or not path.is_file():
            continue
        try:
            content = path.read_text(errors="ignore")
        except Exception:
            continue
        for i, line in enumerate(content.splitlines(), 1):
            if query.lower() in line.lower():
                rel = path.relative_to(REPO_ROOT)
                results.append(f"{rel}:{i}: {line.strip()}")

    if not results:
        return f"No results for '{query}'."
    if len(results) > 30:
        return "\n".join(results[:30]) + f"\n\n... and {len(results) - 30} more matches."
    return "\n".join(results)


@mcp.tool()
def get_lab_prerequisites(lab_id: str) -> str:
    """Get prerequisites for a specific lab.

    Args:
        lab_id: Lab directory name (e.g., 'lab1-local-mcp-servers').
    """
    lab_dir = LABS_DIR / lab_id
    prereqs = lab_dir / "prerequisites.md"
    if prereqs.exists():
        return prereqs.read_text()
    shared = LABS_DIR / "shared" / "prerequisites.md"
    return shared.read_text() if shared.exists() else "Prerequisites not found."


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
