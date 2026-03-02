#!/usr/bin/env bash
# Clean up all Azure resources created by deploy.sh
# Usage: ./cleanup.sh [resource-group-name]

set -euo pipefail

RG_NAME="${1:-rg-mcp-hol}"

echo "=== Cleaning up Azure resources ==="
echo "This will delete resource group: $RG_NAME"
echo "All resources inside will be permanently deleted."
echo ""
read -p "Are you sure? (y/N): " confirm

if [[ "$confirm" =~ ^[Yy]$ ]]; then
    echo "Deleting resource group $RG_NAME..."
    az group delete --name "$RG_NAME" --yes --no-wait
    echo "Deletion initiated (running in background)."
    echo "Check status: az group show --name $RG_NAME"
else
    echo "Cancelled."
fi
