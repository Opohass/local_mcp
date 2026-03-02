# Lab 3: Azure Deployment

## Objectives

By the end of this lab you will be able to:

1. Containerize an MCP server with Docker
2. Deploy to Azure Container Apps with a public HTTPS endpoint
3. Create an Azure AI Foundry Hub, Project, and Agent
4. Connect a deployed MCP server to a Foundry Agent

## What You'll Build

An HTTP MCP server deployed to Azure with 4 tools:

| Tool | Purpose |
|------|---------|
| `search_issues` | Search GitHub issues via API |
| `summarize_pr` | Fetch and summarize a Pull Request |
| `check_service_health` | Ping URLs and report status/latency |
| `run_query` | Query a sample dataset |

## Architecture

```
Local Dev → Docker Image → Azure Container Registry → Container App (HTTPS)
                                                           ↓
Azure AI Foundry Hub → Project → Agent ───── MCP Tools ───┘
```

## Files

| File | Description |
|------|-------------|
| `server/azure_mcp_server.py` | The MCP server (HTTP transport) |
| `server/Dockerfile` | Container image definition |
| `server/requirements.txt` | Pinned Python dependencies |
| `deploy/deploy.sh` | Automated deployment script |
| `deploy/deploy_steps.md` | Manual step-by-step guide (CLI + Portal) |
| `deploy/cleanup.sh` | Resource cleanup script |
| `foundry/foundry_agent.py` | Create and test a Foundry agent |
| `foundry/foundry_setup.md` | Foundry Hub/Project/Model setup guide |

## Quick Start

### Automated deployment

```bash
./labs/lab3-azure-deployment/deploy/deploy.sh
```

### Manual (follow the guide)

See [deploy/deploy_steps.md](deploy/deploy_steps.md) for step-by-step instructions.

### Cleanup

```bash
./labs/lab3-azure-deployment/deploy/cleanup.sh
# Or: az group delete --name rg-mcp-hol --yes --no-wait
```

## Estimated Time

60-90 minutes (including Azure resource creation)

## Estimated Cost

~$2-5 for a 2-hour lab session. See [deploy_steps.md](deploy/deploy_steps.md#resource-summary) for breakdown.
