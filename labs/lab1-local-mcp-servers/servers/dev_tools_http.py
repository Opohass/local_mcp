"""
MCP Server: Dev Tools (HTTP Transport)

Same tools and prompts as the STDIO server, but served over HTTP.
This demonstrates how transport changes while tool logic stays identical.

Usage:
    python dev_tools_http.py
    # Server starts at http://localhost:9000
"""

# Re-use the same FastMCP instance from the STDIO server
# by importing and changing only the transport.
import sys
from pathlib import Path

# Add the servers directory to path so we can import the stdio module
sys.path.insert(0, str(Path(__file__).parent))

from dev_tools_stdio import mcp  # noqa: E402

if __name__ == "__main__":
    print("Starting Dev Tools MCP server on http://0.0.0.0:9000", file=sys.stderr)
    mcp.run(transport="streamable-http", host="0.0.0.0", port=9000)
