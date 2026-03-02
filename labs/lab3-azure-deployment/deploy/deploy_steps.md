# Azure Deployment: Step-by-Step Guide

This guide walks through deploying the MCP server to Azure Container Apps and connecting it to Azure AI Foundry. Each step includes both CLI and Portal instructions.

**Estimated time**: 45-60 minutes (first time), 15-20 minutes (repeat)
**Estimated cost**: ~$2-5 for a lab session (Container Apps + ACR basic tier)

---

## Phase 1: Prerequisites

### 1.1 Install Azure CLI

```bash
# Linux
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# macOS
brew install azure-cli

# Windows
winget install Microsoft.AzureCLI

# Verify
az version
```

### 1.2 Install Docker

```bash
# Verify Docker is running
docker info
```

If not installed: [docs.docker.com/get-docker](https://docs.docker.com/get-docker/)

### 1.3 Login to Azure

```bash
az login
# A browser window will open for authentication

# Verify your subscription
az account show --query "{name:name, id:id}" -o table

# If you need to switch subscriptions:
az account list -o table
az account set --subscription "<subscription-id>"
```

---

## Phase 2: Test the Server Locally

### 2.1 Run the MCP server

```bash
cd labs/lab3-azure-deployment/server
python azure_mcp_server.py
# → Starting Azure Dev Tools MCP server on http://0.0.0.0:9000
```

### 2.2 Test with the MCP Inspector

In a separate terminal:
```bash
fastmcp dev labs/lab3-azure-deployment/server/azure_mcp_server.py
```

This opens a web UI where you can invoke each tool interactively.

### 2.3 Test the tools

Try calling each tool in the inspector:
- `check_service_health` with urls: `https://httpbin.org/status/200,https://httpbin.org/status/404`
- `search_issues` with repo: `microsoft/vscode`, query: `bug`
- `run_query` with query: `degraded`

**Expected output for observers** (if you don't have the server running):
```
check_service_health("https://httpbin.org/status/200"):
  Status  Latency  URL
  200     142ms    https://httpbin.org/status/200

run_query("degraded"):
  Found 1 result(s) for 'degraded':
    [service] user-service — degraded (westus)
```

---

## Phase 3: Containerize

### 3.1 Review the Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY azure_mcp_server.py .
EXPOSE 9000
CMD ["python", "azure_mcp_server.py"]
```

### 3.2 Build the Docker image

```bash
cd labs/lab3-azure-deployment/server
docker build -t mcp-server:latest .
```

**Expected output**:
```
[+] Building 15.2s (9/9) FINISHED
 => [1/4] FROM python:3.11-slim
 => [2/4] COPY requirements.txt .
 => [3/4] RUN pip install ...
 => [4/4] COPY azure_mcp_server.py .
 => exporting to image
```

### 3.3 Test locally with Docker

```bash
docker run -p 9000:9000 mcp-server:latest
```

Verify in another terminal:
```bash
curl http://localhost:9000/docs
# Should return the FastMCP docs page or a 200 response
```

---

## Phase 4: Deploy to Azure

### 4.1 Create a Resource Group

**CLI:**
```bash
az group create --name rg-mcp-hol --location eastus
```

**Portal:**
1. Go to [portal.azure.com](https://portal.azure.com)
2. Search for "Resource groups" → Click "Create"
3. Subscription: Select yours
4. Resource group name: `rg-mcp-hol`
5. Region: `East US`
6. Click "Review + Create" → "Create"

### 4.2 Create Azure Container Registry (ACR)

**CLI:**
```bash
az acr create \
    --resource-group rg-mcp-hol \
    --name mcpholregistry \
    --sku Basic

az acr login --name mcpholregistry
```

**Portal:**
1. Search for "Container registries" → "Create"
2. Resource group: `rg-mcp-hol`
3. Registry name: `mcpholregistry` (must be globally unique — append random numbers if taken)
4. SKU: Basic
5. Click "Review + Create" → "Create"

> **Note**: The registry name must be globally unique. If `mcpholregistry` is taken, try `mcpholregistry123`.

### 4.3 Push the Docker image to ACR

```bash
# Tag the image for ACR
docker tag mcp-server:latest mcpholregistry.azurecr.io/mcp-server:latest

# Push to ACR
docker push mcpholregistry.azurecr.io/mcp-server:latest
```

**Expected output**:
```
The push refers to repository [mcpholregistry.azurecr.io/mcp-server]
latest: digest: sha256:abc123... size: 1234
```

### 4.4 Create Container Apps Environment

**CLI:**
```bash
az containerapp env create \
    --name mcp-env \
    --resource-group rg-mcp-hol \
    --location eastus
```

**Portal:**
1. Search for "Container Apps Environments" → "Create"
2. Resource group: `rg-mcp-hol`
3. Environment name: `mcp-env`
4. Region: `East US`
5. Click "Review + Create" → "Create"

### 4.5 Deploy the Container App

**CLI:**
```bash
az containerapp create \
    --name mcp-server-app \
    --resource-group rg-mcp-hol \
    --environment mcp-env \
    --image mcpholregistry.azurecr.io/mcp-server:latest \
    --target-port 9000 \
    --ingress external \
    --registry-server mcpholregistry.azurecr.io \
    --min-replicas 1 \
    --max-replicas 1
```

**Portal:**
1. Search for "Container Apps" → "Create"
2. Resource group: `rg-mcp-hol`
3. Container App name: `mcp-server-app`
4. Environment: `mcp-env`
5. Under "Container":
   - Image source: Azure Container Registry
   - Registry: `mcpholregistry`
   - Image: `mcp-server`
   - Tag: `latest`
6. Under "Ingress":
   - Enabled: Yes
   - Traffic: Accept from anywhere
   - Target port: `9000`
7. Click "Review + Create" → "Create"

### 4.6 Get the deployment URL

```bash
FQDN=$(az containerapp show \
    --name mcp-server-app \
    --resource-group rg-mcp-hol \
    --query "properties.configuration.ingress.fqdn" \
    --output tsv)

echo "Your MCP server is at: https://$FQDN"
```

### 4.7 Verify the deployment

```bash
curl https://$FQDN/docs
# Should return the FastMCP documentation page
```

**Expected output for observers**:
```
Your MCP server is at: https://mcp-server-app.kindpond-abc123.eastus.azurecontainerapps.io
```

---

## Phase 5: Connect to Azure AI Foundry

### 5.1 Create an AI Foundry Hub

**Portal** (recommended for first time):
1. Go to [ai.azure.com](https://ai.azure.com)
2. Click "Create a hub"
3. Hub name: `mcp-hol-hub`
4. Subscription: Select yours
5. Resource group: `rg-mcp-hol`
6. Region: `East US`
7. Click "Create"

**CLI:**
```bash
az ml workspace create \
    --kind hub \
    --name mcp-hol-hub \
    --resource-group rg-mcp-hol \
    --location eastus
```

### 5.2 Create a Project

**Portal:**
1. Inside your Hub, click "Create project"
2. Project name: `mcp-hol-project`
3. Click "Create"

**CLI:**
```bash
az ml workspace create \
    --kind project \
    --name mcp-hol-project \
    --resource-group rg-mcp-hol \
    --hub-id /subscriptions/<sub-id>/resourceGroups/rg-mcp-hol/providers/Microsoft.MachineLearningServices/workspaces/mcp-hol-hub
```

### 5.3 Deploy a Model

**Portal:**
1. In your project, go to "Model catalog"
2. Search for `gpt-4o-mini`
3. Click "Deploy" → "Deploy to serverless API"
4. Deployment name: `gpt-4o-mini`
5. Click "Deploy"

Note the endpoint URL — you'll need it for the agent.

### 5.4 Connect MCP Server to Foundry Agent

Set environment variables:
```bash
export AZURE_AI_PROJECT_ENDPOINT="https://<your-hub>.services.ai.azure.com/api/projects/<project-id>"
export AZURE_AI_MODEL_DEPLOYMENT_NAME="gpt-4o-mini"
export MCP_SERVER_URL="https://<your-fqdn>/mcp"
```

Run the Foundry agent script:
```bash
python labs/lab3-azure-deployment/foundry/foundry_agent.py
```

See [foundry/foundry_setup.md](../foundry/foundry_setup.md) for detailed setup instructions.

### 5.5 Test the Agent

The script will create an agent and run a test query. You should see output like:

**Expected output**:
```
Creating Foundry agent with MCP tools...
Agent created: agent-abc123
Running test query: "Check the health of https://httpbin.org/get"

Agent response:
  I checked the health of https://httpbin.org/get and it returned:
  Status: 200, Latency: 142ms

Cleaning up agent...
Done.
```

---

## Phase 6: Cleanup

### Automated

```bash
./labs/lab3-azure-deployment/deploy/cleanup.sh rg-mcp-hol
```

### Manual

```bash
# Delete the entire resource group (removes everything inside)
az group delete --name rg-mcp-hol --yes --no-wait
```

**Portal:**
1. Go to Resource Groups
2. Select `rg-mcp-hol`
3. Click "Delete resource group"
4. Type the name to confirm

---

## Resource Summary

| Resource | Name | Purpose | Est. Cost |
|----------|------|---------|-----------|
| Resource Group | `rg-mcp-hol` | Container for all resources | Free |
| Container Registry | `mcpholregistry` | Store Docker images | ~$0.17/day (Basic) |
| Container Apps Environment | `mcp-env` | Hosting environment | Free (included) |
| Container App | `mcp-server-app` | Run the MCP server | ~$0.05/hour (1 vCPU) |
| AI Foundry Hub | `mcp-hol-hub` | AI project management | Free |
| AI Foundry Project | `mcp-hol-project` | Agent workspace | Free |
| Model Deployment | `gpt-4o-mini` | LLM for the agent | Pay per token |

**Total for a 2-hour lab session**: ~$2-5
