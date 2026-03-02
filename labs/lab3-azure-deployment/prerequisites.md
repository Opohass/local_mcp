# Lab 3 Prerequisites

## Required

| Tool | Version | Install |
|------|---------|---------|
| Azure CLI | Latest | [Install guide](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) |
| Docker | Latest | [docs.docker.com/get-docker](https://docs.docker.com/get-docker/) |
| Azure subscription | Active | [Free tier](https://azure.microsoft.com/free/) works for this lab |

## Required Python packages

```bash
pip install -e ".[lab3]"
# Installs: azure-identity, azure-ai-projects
```

## Optional

- GitHub Personal Access Token (for `search_issues` and `summarize_pr` tools to have higher rate limits)

## Verify

```bash
az version           # Azure CLI installed
az account show      # Logged in to Azure
docker info          # Docker running
```

## For observers (no Azure subscription)

You can follow along with the step-by-step guide. Each step includes **Expected output** sections showing what you would see. The Foundry setup guide also includes expected agent responses.
