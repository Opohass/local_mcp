# Azure AI Foundry Setup Guide

This guide covers creating and configuring Azure AI Foundry to work with your deployed MCP server.

## What is Azure AI Foundry?

Azure AI Foundry (formerly Azure AI Studio) is Microsoft's platform for building AI applications. It provides:

- **Hubs**: Organizational containers for AI projects
- **Projects**: Workspaces where you build and test AI agents
- **Agents**: AI assistants that can use tools (including MCP servers)
- **Model Deployments**: Access to LLMs (GPT-4o, GPT-4o-mini, etc.)

## Architecture

```
┌────────────────────────────────────────────────────┐
│  Azure AI Foundry                                  │
│                                                    │
│  ┌──────────┐    ┌──────────┐    ┌──────────────┐  │
│  │   Hub    │───►│ Project  │───►│    Agent     │  │
│  │          │    │          │    │  (GPT-4o)    │  │
│  └──────────┘    └──────────┘    └──────┬───────┘  │
│                                         │          │
└─────────────────────────────────────────┼──────────┘
                                          │ HTTPS
                                          ▼
                               ┌──────────────────┐
                               │  MCP Server      │
                               │  (Container App) │
                               │  :9000/mcp       │
                               └──────────────────┘
```

## Step 1: Create an AI Foundry Hub

### Via Portal (Recommended)

1. Go to [ai.azure.com](https://ai.azure.com)
2. Sign in with your Azure account
3. Click **"Create a hub"** (or "Manage" → "Hubs" → "New hub")
4. Fill in:
   - **Hub name**: `mcp-hol-hub`
   - **Subscription**: Select your subscription
   - **Resource group**: `rg-mcp-hol` (same as the MCP server)
   - **Region**: `East US` (must match or be close to your Container App)
5. Click **"Create"** and wait ~2 minutes

### Via CLI

```bash
# Install the ML extension if needed
az extension add --name ml

az ml workspace create \
    --kind hub \
    --name mcp-hol-hub \
    --resource-group rg-mcp-hol \
    --location eastus
```

## Step 2: Create a Project

### Via Portal

1. Inside your hub at [ai.azure.com](https://ai.azure.com), click **"New project"**
2. Project name: `mcp-hol-project`
3. Click **"Create"**

### Via CLI

**Linux / macOS**
```bash
HUB_ID=$(az ml workspace show --name mcp-hol-hub --resource-group rg-mcp-hol --query id -o tsv)

az ml workspace create \
    --kind project \
    --name mcp-hol-project \
    --resource-group rg-mcp-hol \
    --hub-id "$HUB_ID"
```

**Windows (PowerShell)**
```powershell
$HUB_ID = az ml workspace show --name mcp-hol-hub --resource-group rg-mcp-hol --query id -o tsv

az ml workspace create `
    --kind project `
    --name mcp-hol-project `
    --resource-group rg-mcp-hol `
    --hub-id $HUB_ID
```

## Step 3: Deploy a Model

### Via Portal

1. In your project, go to **"Model catalog"** (left sidebar)
2. Search for **`gpt-4o-mini`** (cheapest option for testing)
3. Click the model → **"Deploy"** → **"Deploy to serverless API"**
4. Deployment name: `gpt-4o-mini`
5. Click **"Deploy"**
6. Note the **endpoint URL** shown after deployment

### Important Notes

- `gpt-4o-mini` is the most cost-effective choice for lab purposes
- You can also use `gpt-4o` for better quality (higher cost)
- Deployment takes 1-2 minutes

## Step 4: Get Your Project Endpoint

### Via Portal

1. In your project, go to **"Settings"** (left sidebar, bottom)
2. Look for **"Project endpoint"** or **"Discovery URL"**
3. It looks like: `https://<hub-name>.services.ai.azure.com/api/projects/<project-id>`

### Via CLI

```bash
az ml workspace show \
    --name mcp-hol-project \
    --resource-group rg-mcp-hol \
    --query discovery_url -o tsv
```

## Step 5: Set Environment Variables

**Linux / macOS**
```bash
export AZURE_AI_PROJECT_ENDPOINT="https://<hub-name>.services.ai.azure.com/api/projects/<project-id>"
export MCP_SERVER_URL="https://<container-app-fqdn>/mcp"
export AZURE_AI_MODEL_DEPLOYMENT_NAME="gpt-4o-mini"
```

**Windows (PowerShell)**
```powershell
$env:AZURE_AI_PROJECT_ENDPOINT = "https://<hub-name>.services.ai.azure.com/api/projects/<project-id>"
$env:MCP_SERVER_URL = "https://<container-app-fqdn>/mcp"
$env:AZURE_AI_MODEL_DEPLOYMENT_NAME = "gpt-4o-mini"
```

## Step 6: Run the Foundry Agent

```bash
# Install Foundry dependencies
pip install azure-identity azure-ai-projects
```

**Linux / macOS**
```bash
python labs/lab3-azure-deployment/foundry/foundry_agent.py
```

**Windows (PowerShell)**
```powershell
py labs/lab3-azure-deployment/foundry/foundry_agent.py
```

### Expected Output

```
Creating Foundry agent with MCP tools...
Agent created: agent-abc123def456
Running test query: "Check the health of https://httpbin.org/get and search for 'degraded' in the sample dataset"

Agent response:
  I performed two checks:

  1. **Health Check** for https://httpbin.org/get:
     - Status: 200, Latency: 145ms — the service is healthy.

  2. **Dataset Search** for "degraded":
     - Found 1 result: [service] user-service — degraded (westus)

Cleaning up agent...
Done.
```

## Troubleshooting

### "DefaultAzureCredential failed"

Make sure you're logged in:
```bash
az login
```

### "Model deployment not found"

Verify the deployment name matches:

**Linux / macOS**
```bash
echo $AZURE_AI_MODEL_DEPLOYMENT_NAME
```

**Windows (PowerShell)**
```powershell
$env:AZURE_AI_MODEL_DEPLOYMENT_NAME
```

### "MCP server connection refused"

1. Verify the Container App is running:
   ```bash
   az containerapp show --name mcp-server-app --resource-group rg-mcp-hol --query "properties.runningStatus"
   ```
2. Test the URL directly:

   **Linux / macOS**
   ```bash
   curl $MCP_SERVER_URL
   ```

   **Windows (PowerShell)**
   ```powershell
   Invoke-WebRequest $env:MCP_SERVER_URL
   ```

### Agent returns empty response

- The model may need more explicit instructions. Try modifying the `instructions` parameter in `foundry_agent.py`.
- Ensure the MCP server tools are being discovered. Check the agent's tool definitions.
