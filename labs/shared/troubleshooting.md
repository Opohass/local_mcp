# Troubleshooting

## Common Issues

### FastMCP not found / import errors

```
ModuleNotFoundError: No module named 'fastmcp'
```

**Fix**: Make sure you installed in the active virtual environment:

**Linux / macOS**
```bash
source .venv/bin/activate
pip install -e .
```

**Windows (PowerShell)**
```powershell
.venv\Scripts\Activate.ps1
pip install -e .
```

### Port already in use (Lab 1 HTTP server)

```
OSError: [Errno 98] Address already in use
```

**Fix**: Find and kill the process using the port:

**Linux / macOS**
```bash
lsof -i :9000
kill <PID>
```

**Windows (PowerShell)**
```powershell
netstat -ano | findstr :9000
taskkill /PID <PID> /F
```
Or change the port in `dev_tools_http.py`.

### Claude Code doesn't see MCP tools

**Possible causes**:
1. **Config path wrong** — Claude Code reads `.mcp.json` from the project root. Make sure you're running `claude` from the repo directory.
2. **Server not starting** — Test the server manually first: `python labs/lab1-local-mcp-servers/servers/dev_tools_stdio.py`
3. **Python path** — The config uses `python` but your venv might need the full path. Try:
   - Linux / macOS: `"command": ".venv/bin/python"`
   - Windows: `"command": ".venv\\Scripts\\python"`

### VS Code Copilot doesn't show MCP tools

1. Make sure `.vscode/mcp.json` exists in the workspace root.
2. Restart VS Code after editing the config.
3. Open Copilot Chat and check the tools icon — MCP tools should appear there.
4. VS Code MCP support requires a recent version (1.99+).

### Jupyter kernel not found

```bash
# Install the kernel in your venv
pip install ipykernel
python -m ipykernel install --user --name=mcp-hol --display-name="MCP HOL"
```

### SSH connection refused (run_remote_command tool)

1. Ensure the target machine has SSH enabled.
2. Check that your SSH key is loaded: `ssh-add -l`
3. Test manually: `ssh user@host echo "test"`
4. The tool uses `subprocess` with `ssh` — make sure `ssh` is on your PATH.

### Azure CLI not logged in (Lab 3)

```bash
az login
az account show  # Verify correct subscription
```

### Docker not running (Lab 3)

```bash
sudo systemctl start docker  # Linux
# Or open Docker Desktop on macOS/Windows
docker info  # Verify
```
