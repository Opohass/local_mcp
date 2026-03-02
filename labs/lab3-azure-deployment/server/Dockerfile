FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY azure_mcp_server.py .

EXPOSE 9000

# Health check for Azure Container Apps
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:9000/health')" || exit 1

CMD ["python", "azure_mcp_server.py"]
