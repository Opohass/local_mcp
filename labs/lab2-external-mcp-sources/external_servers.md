# Catalog of Useful External MCP Servers

## Official Reference Servers

Maintained by the MCP team at [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers).

| Server | Package | Description |
|--------|---------|-------------|
| **Filesystem** | `@modelcontextprotocol/server-filesystem` | Read, write, search files with access controls |
| **Fetch** | `@modelcontextprotocol/server-fetch` | Fetch web pages and convert to markdown |
| **Git** | `@modelcontextprotocol/server-git` | Read, search, and manipulate Git repositories |
| **Memory** | `@modelcontextprotocol/server-memory` | Knowledge graph-based persistent memory |
| **SQLite** | `@modelcontextprotocol/server-sqlite` | Database interaction and querying |
| **Sequential Thinking** | `@modelcontextprotocol/server-sequential-thinking` | Dynamic problem-solving through thought chains |

## Third-Party Servers

| Server | Source | Description |
|--------|--------|-------------|
| **GitHub** | `@github/github-mcp-server` | Full GitHub API: repos, issues, PRs, search |
| **Sentry** | `https://mcp.sentry.dev/mcp` | Error tracking, issue management (remote) |
| **Slack** | Community | Send/read Slack messages |
| **Docker** | Community | Manage Docker containers |
| **PostgreSQL** | Community | Query PostgreSQL databases |

## Finding More Servers

- **Official Registry**: [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)
- **Community List**: [github.com/wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers)
- **Search**: [mcpservers.org](https://mcpservers.org)

## Security Notes

Before connecting any external MCP server:

1. **Review the source code** — Know what the server can access
2. **Minimize permissions** — Only grant file access to directories you need
3. **Use environment variables** for secrets — Never hardcode tokens in config files
4. **Pin versions** where possible — Use specific npm package versions
5. **Audit network access** — Some servers may make external HTTP requests
