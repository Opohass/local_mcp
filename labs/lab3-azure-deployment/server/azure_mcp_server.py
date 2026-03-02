"""
MCP Server: Azure Deployment (HTTP Transport)

A remote-capable MCP server designed for Azure Container Apps deployment.
Includes a health endpoint for container health probes.

Usage (local):
    python azure_mcp_server.py
    # Server starts at http://0.0.0.0:9000

Usage (Docker):
    docker build -t mcp-server .
    docker run -p 9000:9000 mcp-server
"""

import os
import time

import httpx
from fastmcp import FastMCP

mcp = FastMCP("azure-dev-tools")


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
async def search_issues(repo: str, query: str = "", state: str = "open") -> str:
    """Search GitHub issues for a repository.

    Args:
        repo: GitHub repo in 'owner/name' format (e.g., 'microsoft/vscode').
        query: Search keywords to filter issues.
        state: Issue state: 'open', 'closed', or 'all'.
    """
    url = f"https://api.github.com/search/issues"
    q = f"repo:{repo} is:issue state:{state}"
    if query:
        q += f" {query}"

    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params={"q": q, "per_page": 10}, headers=headers)
        if resp.status_code != 200:
            return f"ERROR: GitHub API returned {resp.status_code}: {resp.text[:200]}"
        data = resp.json()

    issues = data.get("items", [])
    if not issues:
        return f"No issues found for '{query}' in {repo} (state: {state})."

    lines = [f"Found {data['total_count']} issues (showing top {len(issues)}):\n"]
    for issue in issues:
        labels = ", ".join(l["name"] for l in issue.get("labels", []))
        labels_str = f" [{labels}]" if labels else ""
        lines.append(f"  #{issue['number']}: {issue['title']}{labels_str}")
        lines.append(f"    {issue['html_url']}")
    return "\n".join(lines)


@mcp.tool()
async def summarize_pr(repo: str, pr_number: int) -> str:
    """Fetch and summarize a GitHub Pull Request.

    Args:
        repo: GitHub repo in 'owner/name' format.
        pr_number: The PR number to summarize.
    """
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    async with httpx.AsyncClient() as client:
        pr_resp = await client.get(
            f"https://api.github.com/repos/{repo}/pulls/{pr_number}", headers=headers
        )
        if pr_resp.status_code != 200:
            return f"ERROR: Could not fetch PR #{pr_number}: {pr_resp.status_code}"
        pr = pr_resp.json()

        files_resp = await client.get(
            f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files",
            headers=headers, params={"per_page": 30},
        )
        files = files_resp.json() if files_resp.status_code == 200 else []

    lines = [
        f"# PR #{pr_number}: {pr['title']}",
        f"**Author**: {pr['user']['login']}",
        f"**State**: {pr['state']}  |  **Mergeable**: {pr.get('mergeable', 'unknown')}",
        f"**Base**: {pr['base']['ref']} ← {pr['head']['ref']}",
        f"**Changed files**: {pr.get('changed_files', len(files))}  |  "
        f"+{pr.get('additions', '?')} / -{pr.get('deletions', '?')} lines",
        "",
        "## Description",
        pr.get("body", "(no description)") or "(no description)",
        "",
        "## Files Changed",
    ]
    for f in files[:20]:
        lines.append(f"  {f.get('status', '?'):10s}  +{f.get('additions', 0):-4d} "
                      f"-{f.get('deletions', 0):-4d}  {f['filename']}")

    return "\n".join(lines)


@mcp.tool()
async def check_service_health(urls: str) -> str:
    """Check health/availability of one or more URLs.

    Args:
        urls: Comma-separated list of URLs to check (e.g., 'https://example.com,https://api.github.com').
    """
    results = []
    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        for url in urls.split(","):
            url = url.strip()
            if not url:
                continue
            try:
                start = time.monotonic()
                resp = await client.get(url)
                elapsed = (time.monotonic() - start) * 1000
                results.append(f"  {resp.status_code}  {elapsed:6.0f}ms  {url}")
            except httpx.ConnectError:
                results.append(f"  CONN_ERR       -  {url}")
            except httpx.TimeoutException:
                results.append(f"  TIMEOUT        -  {url}")
            except Exception as e:
                results.append(f"  ERROR          -  {url}  ({type(e).__name__})")

    header = "  Status  Latency  URL"
    return f"{header}\n" + "\n".join(results)


@mcp.tool()
def run_query(query: str, data_source: str = "sample") -> str:
    """Run a simple keyword query against a sample dataset.

    This is a demonstration tool — in production, this could connect
    to a real database or data warehouse.

    Args:
        query: Search keywords.
        data_source: Dataset to search. Currently only 'sample' is available.
    """
    # Sample dataset for demonstration
    sample_data = [
        {"id": 1, "type": "service", "name": "api-gateway", "status": "healthy", "region": "eastus"},
        {"id": 2, "type": "service", "name": "auth-service", "status": "healthy", "region": "eastus"},
        {"id": 3, "type": "service", "name": "user-service", "status": "degraded", "region": "westus"},
        {"id": 4, "type": "database", "name": "main-db", "status": "healthy", "region": "eastus"},
        {"id": 5, "type": "database", "name": "analytics-db", "status": "healthy", "region": "westeurope"},
        {"id": 6, "type": "cache", "name": "redis-primary", "status": "healthy", "region": "eastus"},
        {"id": 7, "type": "queue", "name": "task-queue", "status": "healthy", "region": "eastus"},
        {"id": 8, "type": "service", "name": "notification-svc", "status": "stopped", "region": "westus"},
    ]

    query_lower = query.lower()
    matches = [
        item for item in sample_data
        if any(query_lower in str(v).lower() for v in item.values())
    ]

    if not matches:
        return f"No results for '{query}' in {data_source} dataset."

    lines = [f"Found {len(matches)} result(s) for '{query}':\n"]
    for item in matches:
        lines.append(f"  [{item['type']}] {item['name']} — {item['status']} ({item['region']})")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    print("Starting Azure Dev Tools MCP server on http://0.0.0.0:9000", file=sys.stderr)
    mcp.run(transport="streamable-http", host="0.0.0.0", port=9000)
