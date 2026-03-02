"""
MCP Server: Dev Tools (STDIO Transport)

A local MCP server providing developer utility tools and review prompts.
Connects to Claude Code and VS Code via stdio transport.

Usage:
    python dev_tools_stdio.py
"""

import os
import socket
import subprocess
from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP("dev-tools")

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def run_remote_command(host: str, command: str, user: str = "") -> str:
    """Run a shell command on a remote machine via SSH.

    Args:
        host: Hostname or IP address of the remote machine.
        command: The shell command to execute remotely.
        user: SSH username. If empty, uses the current user.
    """
    ssh_target = f"{user}@{host}" if user else host
    try:
        result = subprocess.run(
            ["ssh", "-o", "StrictHostKeyChecking=accept-new", "-o", "ConnectTimeout=10",
             ssh_target, command],
            capture_output=True, text=True, timeout=30,
        )
        output = result.stdout.strip()
        errors = result.stderr.strip()
        parts = []
        if output:
            parts.append(f"STDOUT:\n{output}")
        if errors:
            parts.append(f"STDERR:\n{errors}")
        if result.returncode != 0:
            parts.append(f"Exit code: {result.returncode}")
        return "\n\n".join(parts) if parts else "(no output)"
    except subprocess.TimeoutExpired:
        return f"ERROR: Command timed out after 30 seconds on {host}"
    except FileNotFoundError:
        return "ERROR: ssh not found on PATH. Install OpenSSH client."


@mcp.tool()
def file_tree(
    directory: str = ".",
    max_depth: int = 3,
    ignore_patterns: str = ".git,node_modules,__pycache__,.venv,venv,.ipynb_checkpoints",
) -> str:
    """Generate a clean directory tree listing.

    Args:
        directory: Root directory to scan. Defaults to current directory.
        max_depth: Maximum depth to recurse. Defaults to 3.
        ignore_patterns: Comma-separated directory/file names to skip.
    """
    root = Path(directory).resolve()
    if not root.is_dir():
        return f"ERROR: {directory} is not a valid directory."

    ignores = set(p.strip() for p in ignore_patterns.split(","))
    lines = [f"{root.name}/"]

    def _walk(path: Path, prefix: str, depth: int):
        if depth > max_depth:
            return
        try:
            entries = sorted(path.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
        except PermissionError:
            return
        dirs = [e for e in entries if e.is_dir() and e.name not in ignores]
        files = [e for e in entries if e.is_file() and e.name not in ignores]
        items = dirs + files
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{item.name}{'/' if item.is_dir() else ''}")
            if item.is_dir():
                extension = "    " if is_last else "│   "
                _walk(item, prefix + extension, depth + 1)

    _walk(root, "", 1)
    return "\n".join(lines)


@mcp.tool()
def port_checker(ports: str = "3000,5000,8000,8080,9000") -> str:
    """Check which common development ports are in use.

    Args:
        ports: Comma-separated list of port numbers to check.
    """
    results = []
    for port_str in ports.split(","):
        port = int(port_str.strip())
        if port < 0 or port > 65535:
            results.append(f"  :{port}  INVALID (must be 0-65535)")
            continue
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            in_use = s.connect_ex(("127.0.0.1", port)) == 0

        status = "IN USE" if in_use else "FREE"
        line = f"  :{port}  {status}"

        # Try to find the owning process on Linux/macOS
        if in_use:
            try:
                out = subprocess.run(
                    ["lsof", "-i", f":{port}", "-t"], capture_output=True, text=True, timeout=5
                )
                if out.stdout.strip():
                    pid = out.stdout.strip().splitlines()[0]
                    ps = subprocess.run(
                        ["ps", "-p", pid, "-o", "comm="], capture_output=True, text=True, timeout=5
                    )
                    proc_name = ps.stdout.strip()
                    line += f"  (pid {pid}, {proc_name})"
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass

        results.append(line)

    return "Port Status:\n" + "\n".join(results)


# ---------------------------------------------------------------------------
# Prompts (Review Context)
# ---------------------------------------------------------------------------


@mcp.prompt()
def code_review() -> str:
    """Comprehensive code review checklist and instructions for AI-assisted reviews."""
    return """You are performing a code review. Evaluate the code against these criteria:

## Correctness
- Does the code do what it's supposed to do?
- Are edge cases handled (null, empty, boundary values)?
- Are error conditions handled gracefully?

## Readability
- Are variable/function names descriptive and consistent?
- Is the code self-documenting or properly commented where complex?
- Is the structure logical and easy to follow?

## Performance
- Are there unnecessary loops, allocations, or API calls?
- Could any operations be batched or cached?
- Are data structures appropriate for the operations?

## Security
- Is user input validated and sanitized?
- Are secrets hardcoded or properly managed?
- Are there injection risks (SQL, command, XSS)?

## Maintainability
- Is the code DRY without being over-abstracted?
- Are functions small and single-purpose?
- Would a new developer understand this easily?

Provide specific, actionable feedback with line references where possible."""


@mcp.prompt()
def security_review() -> str:
    """Security-focused review checklist for code and infrastructure."""
    return """You are performing a security review. Focus on these areas:

## Authentication & Authorization
- Are auth checks present on all protected endpoints?
- Is session management secure (token expiry, rotation)?
- Are permissions checked at the right granularity?

## Input Validation
- Is all external input validated (type, range, format)?
- Are file uploads restricted by type and size?
- Is output encoding applied to prevent XSS?

## Data Protection
- Are secrets stored in environment variables, not code?
- Is sensitive data encrypted at rest and in transit?
- Are logs free of sensitive information (passwords, tokens, PII)?

## Infrastructure
- Are dependencies up to date and free of known CVEs?
- Are network ports minimized and firewalled?
- Are containers running as non-root users?

## OWASP Top 10 Check
- Injection, Broken Auth, Sensitive Data Exposure, XXE
- Broken Access Control, Misconfiguration, XSS
- Insecure Deserialization, Vulnerable Components, Insufficient Logging

Flag issues by severity: CRITICAL / HIGH / MEDIUM / LOW."""


@mcp.prompt()
def design_review() -> str:
    """Architecture and design review criteria."""
    return """You are performing an architecture/design review. Evaluate against:

## Separation of Concerns
- Are responsibilities clearly divided between components?
- Is business logic separated from transport/presentation?
- Are interfaces/contracts well-defined between layers?

## Scalability
- Can the system handle 10x the current load?
- Are there single points of failure?
- Is state managed appropriately (stateless services, shared state)?

## Extensibility
- Can new features be added without modifying existing code?
- Are extension points clearly defined?
- Is the dependency graph clean (no circular deps)?

## Simplicity
- Is this the simplest design that meets requirements?
- Are there unnecessary abstractions or indirections?
- Could a new team member understand this in a day?

## Resilience
- How does the system behave when dependencies fail?
- Are retries, timeouts, and circuit breakers in place?
- Is there graceful degradation?

Provide a summary assessment and specific recommendations."""


@mcp.prompt()
def networking_review() -> str:
    """Network configuration and firewall review guide."""
    return """You are performing a network configuration review. Check these areas:

## Connectivity
- Are only required ports exposed (principle of least privilege)?
- Is internal traffic separated from external traffic?
- Are DNS records correct and TTLs appropriate?

## TLS / Encryption
- Is TLS 1.2+ enforced on all public endpoints?
- Are certificates valid and auto-renewed?
- Is certificate pinning used where appropriate?

## Firewall Rules
- Are inbound rules as restrictive as possible?
- Are outbound rules defined (not just allow-all)?
- Are rules documented with purpose and owner?

## Load Balancing & DNS
- Are health checks configured on load balancers?
- Is there failover for DNS (multiple records, low TTL)?
- Are sticky sessions avoided where possible?

## Monitoring
- Are network metrics collected (latency, packet loss, throughput)?
- Are alerts set for anomalies (traffic spikes, connection failures)?
- Are access logs retained for audit?

Provide findings with network-specific remediation steps."""


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
