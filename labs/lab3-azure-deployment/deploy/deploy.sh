#!/usr/bin/env bash
# Deploy MCP Server to Azure Container Apps
# Usage: ./deploy.sh [resource-group-name] [location]

set -euo pipefail

# Configuration
RG_NAME="${1:-rg-mcp-hol}"
LOCATION="${2:-eastus}"
ACR_NAME="mcpholregistry${RANDOM}"
ENV_NAME="mcp-env"
APP_NAME="mcp-server-app"
IMAGE_NAME="mcp-server"

echo "=== MCP Server Azure Deployment ==="
echo "Resource Group: $RG_NAME"
echo "Location:       $LOCATION"
echo "ACR Name:       $ACR_NAME"
echo ""

# Step 1: Create Resource Group
echo "[1/6] Creating resource group..."
az group create --name "$RG_NAME" --location "$LOCATION" --output none

# Step 2: Create Azure Container Registry
echo "[2/6] Creating container registry..."
az acr create --resource-group "$RG_NAME" --name "$ACR_NAME" --sku Basic --output none
az acr login --name "$ACR_NAME"

# Step 3: Build and push image
echo "[3/6] Building and pushing Docker image..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
docker build -t "$IMAGE_NAME:latest" "$SCRIPT_DIR/../server/"
docker tag "$IMAGE_NAME:latest" "$ACR_NAME.azurecr.io/$IMAGE_NAME:latest"
docker push "$ACR_NAME.azurecr.io/$IMAGE_NAME:latest"

# Step 4: Create Container Apps Environment
echo "[4/6] Creating Container Apps environment..."
az containerapp env create \
    --name "$ENV_NAME" \
    --resource-group "$RG_NAME" \
    --location "$LOCATION" \
    --output none

# Step 5: Deploy Container App
echo "[5/6] Deploying container app..."
az containerapp create \
    --name "$APP_NAME" \
    --resource-group "$RG_NAME" \
    --environment "$ENV_NAME" \
    --image "$ACR_NAME.azurecr.io/$IMAGE_NAME:latest" \
    --target-port 9000 \
    --ingress external \
    --registry-server "$ACR_NAME.azurecr.io" \
    --min-replicas 1 \
    --max-replicas 1 \
    --output none

# Step 6: Get the URL
echo "[6/6] Getting deployment URL..."
FQDN=$(az containerapp show \
    --name "$APP_NAME" \
    --resource-group "$RG_NAME" \
    --query "properties.configuration.ingress.fqdn" \
    --output tsv)

echo ""
echo "=== Deployment Complete ==="
echo "Server URL: https://$FQDN"
echo "MCP Endpoint: https://$FQDN/mcp"
echo ""
echo "Test with:"
echo "  curl https://$FQDN/health"
echo ""
echo "Clean up with:"
echo "  az group delete --name $RG_NAME --yes --no-wait"
