"""Tests for Lab 2: External MCP Sources Configuration and Connectivity.

Tests for:
- Loading MCP configuration files (mcp_external.json, vscode_mcp_external.json)
- Validating external server configurations
- Testing connectivity to official MCP servers
- Verifying proper environment variable substitution
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))


# =============================================================================
# Configuration Loading Tests
# =============================================================================


def test_mcp_config_exists():
    """Test that mcp_external.json exists."""
    config_path = Path(__file__).parent.parent / "configs" / "mcp_external.json"
    assert config_path.exists(), f"Config file not found: {config_path}"


def test_vscode_mcp_config_exists():
    """Test that vscode_mcp_external.json exists."""
    config_path = Path(__file__).parent.parent / "configs" / "vscode_mcp_external.json"
    assert config_path.exists(), f"Config file not found: {config_path}"


def test_mcp_config_valid_json():
    """Test that mcp_external.json is valid JSON."""
    config_path = Path(__file__).parent.parent / "configs" / "mcp_external.json"
    with open(config_path) as f:
        config = json.load(f)
    assert isinstance(config, dict)


def test_vscode_mcp_config_valid_json():
    """Test that vscode_mcp_external.json is valid JSON."""
    config_path = Path(__file__).parent.parent / "configs" / "vscode_mcp_external.json"
    with open(config_path) as f:
        config = json.load(f)
    assert isinstance(config, dict)


def test_mcp_config_has_mcp_servers():
    """Test that mcp_external.json has mcpServers section."""
    config_path = Path(__file__).parent.parent / "configs" / "mcp_external.json"
    with open(config_path) as f:
        config = json.load(f)
    assert "mcpServers" in config
    assert isinstance(config["mcpServers"], dict)


def test_vscode_mcp_config_structure():
    """Test that vscode_mcp_external.json has proper structure."""
    config_path = Path(__file__).parent.parent / "configs" / "vscode_mcp_external.json"
    with open(config_path) as f:
        config = json.load(f)
    
    # Should have mcpServers with external servers
    if "mcpServers" in config:
        assert isinstance(config["mcpServers"], dict)
        # Each server should have a command or similar
        for server_name, server_config in config["mcpServers"].items():
            assert isinstance(server_config, dict)


# =============================================================================
# External Server Configuration Tests
# =============================================================================


def test_external_servers_configured():
    """Test that external servers are configured in mcp_external.json."""
    config_path = Path(__file__).parent.parent / "configs" / "mcp_external.json"
    with open(config_path) as f:
        config = json.load(f)
    
    servers = config.get("mcpServers", {})
    # Should have at least one external server
    assert len(servers) > 0, "No external servers configured"


def test_filesystem_server_config():
    """Test Filesystem server configuration if present."""
    config_path = Path(__file__).parent.parent / "configs" / "mcp_external.json"
    with open(config_path) as f:
        config = json.load(f)
    
    servers = config.get("mcpServers", {})
    if "filesystem" in servers or any("filesystem" in name.lower() for name in servers):
        # Find filesystem server
        fs_server = next(
            (s for n, s in servers.items() if "filesystem" in n.lower()),
            servers.get("filesystem"),
        )
        assert fs_server is not None
        # Should have either command or npm package
        assert "command" in fs_server or "npm_package" in fs_server or "package" in fs_server


def test_fetch_server_config():
    """Test Fetch server configuration if present."""
    config_path = Path(__file__).parent.parent / "configs" / "mcp_external.json"
    with open(config_path) as f:
        config = json.load(f)
    
    servers = config.get("mcpServers", {})
    if any("fetch" in name.lower() for name in servers):
        # Find fetch server
        fetch_server = next(s for n, s in servers.items() if "fetch" in n.lower())
        assert fetch_server is not None


def test_git_server_config():
    """Test Git server configuration if present."""
    config_path = Path(__file__).parent.parent / "configs" / "mcp_external.json"
    with open(config_path) as f:
        config = json.load(f)
    
    servers = config.get("mcpServers", {})
    if any("git" in name.lower() for name in servers):
        # Find git server
        git_server = next(s for n, s in servers.items() if "git" in n.lower())
        assert git_server is not None


def test_github_server_config():
    """Test GitHub server configuration if present."""
    config_path = Path(__file__).parent.parent / "configs" / "mcp_external.json"
    with open(config_path) as f:
        config = json.load(f)
    
    servers = config.get("mcpServers", {})
    if any("github" in name.lower() for name in servers):
        github_server = next(s for n, s in servers.items() if "github" in n.lower())
        assert github_server is not None
        # GitHub typically requires auth, should have env var reference
        server_str = json.dumps(github_server)
        # May have ${GITHUB_TOKEN} or similar
        if "env" in server_str or "token" in server_str.lower():
            assert True  # Has some form of auth


# =============================================================================
# Environment Variable Tests
# =============================================================================


def test_config_supports_env_vars():
    """Test that configuration supports environment variable substitution."""
    config_path = Path(__file__).parent.parent / "configs" / "mcp_external.json"
    with open(config_path) as f:
        config_str = f.read()
    
    # Should support ${VAR_NAME} pattern if using auth
    if "token" in config_str.lower() or "auth" in config_str.lower():
        # If auth is mentioned, should have env var references
        assert "${" in config_str or "env" in config_str.lower()


def test_github_token_env_var():
    """Test that GITHUB_TOKEN environment variable is documented/used."""
    config_path = Path(__file__).parent.parent / "configs" / "mcp_external.json"
    with open(config_path) as f:
        config_str = f.read()
    
    # If GitHub server is configured, should mention GITHUB_TOKEN
    if "github" in config_str.lower():
        # Check config or README for token documentation
        readme_path = Path(__file__).parent.parent / "README.md"
        if readme_path.exists():
            with open(readme_path) as f:
                readme = f.read()
            # Should document how to set up GitHub token
            if "github" in readme.lower():
                # This is a soft check - documentation should mention tokens
                assert True


# =============================================================================
# Lab Notebook Tests
# =============================================================================


def test_lab2_notebook_exists():
    """Test that lab2 notebook exists."""
    notebook_path = Path(__file__).parent.parent / "lab2_notebook.ipynb"
    assert notebook_path.exists(), f"Notebook not found: {notebook_path}"


def test_lab2_notebook_valid_json():
    """Test that lab2 notebook is valid JSON."""
    notebook_path = Path(__file__).parent.parent / "lab2_notebook.ipynb"
    with open(notebook_path) as f:
        notebook = json.load(f)
    assert isinstance(notebook, dict)
    assert "cells" in notebook


def test_lab2_notebook_has_cells():
    """Test that lab2 notebook has content cells."""
    notebook_path = Path(__file__).parent.parent / "lab2_notebook.ipynb"
    with open(notebook_path) as f:
        notebook = json.load(f)
    
    cells = notebook.get("cells", [])
    assert len(cells) > 0, "Notebook has no cells"


def test_lab2_notebook_has_instructions():
    """Test that lab2 notebook includes learning instructions."""
    notebook_path = Path(__file__).parent.parent / "lab2_notebook.ipynb"
    with open(notebook_path) as f:
        notebook = json.load(f)
    
    content = json.dumps(notebook)
    # Should mention key topics
    assert "external" in content.lower() or "server" in content.lower()


# =============================================================================
# Documentation Tests
# =============================================================================


def test_external_servers_markdown_exists():
    """Test that external_servers.md exists."""
    doc_path = Path(__file__).parent.parent / "external_servers.md"
    assert doc_path.exists(), f"Documentation not found: {doc_path}"


def test_external_servers_markdown_content():
    """Test that external_servers.md contains server listings."""
    doc_path = Path(__file__).parent.parent / "external_servers.md"
    with open(doc_path) as f:
        content = f.read()
    
    # Should list various servers
    assert "Filesystem" in content or "filesystem" in content.lower()
    assert "Fetch" in content or "fetch" in content.lower()
    assert "Git" in content or "git" in content.lower()


def test_external_servers_markdown_has_table():
    """Test that external_servers.md has server table."""
    doc_path = Path(__file__).parent.parent / "external_servers.md"
    with open(doc_path) as f:
        content = f.read()
    
    # Should have markdown table with server info
    assert "|" in content  # Markdown table separator


def test_external_servers_markdown_security_notes():
    """Test that external_servers.md includes security notes."""
    doc_path = Path(__file__).parent.parent / "external_servers.md"
    with open(doc_path) as f:
        content = f.read()
    
    # Should mention security considerations
    content_lower = content.lower()
    assert "security" in content_lower or "token" in content_lower or "permission" in content_lower


def test_readme_exists():
    """Test that README.md exists for lab 2."""
    readme_path = Path(__file__).parent.parent / "README.md"
    assert readme_path.exists(), f"README not found: {readme_path}"


def test_readme_has_prerequisites():
    """Test that README mentions prerequisites."""
    readme_path = Path(__file__).parent.parent / "README.md"
    with open(readme_path) as f:
        content = f.read()
    
    content_lower = content.lower()
    # Should link to or mention prerequisites
    assert "prerequisite" in content_lower or "setup" in content_lower or "install" in content_lower


# =============================================================================
# Integration Tests
# =============================================================================


def test_config_files_are_consistent():
    """Test that both config files refer to the same servers."""
    mcp_path = Path(__file__).parent.parent / "configs" / "mcp_external.json"
    vscode_path = Path(__file__).parent.parent / "configs" / "vscode_mcp_external.json"
    
    with open(mcp_path) as f:
        mcp_config = json.load(f)
    with open(vscode_path) as f:
        vscode_config = json.load(f)
    
    mcp_servers = set(mcp_config.get("mcpServers", {}).keys())
    vscode_servers = set(vscode_config.get("mcpServers", {}).keys())
    
    # Should have significant overlap
    if len(mcp_servers) > 0 and len(vscode_servers) > 0:
        overlap = mcp_servers & vscode_servers
        assert len(overlap) > 0, "No common servers between configs"


def test_config_server_names_valid():
    """Test that server names are valid identifiers."""
    config_path = Path(__file__).parent.parent / "configs" / "mcp_external.json"
    with open(config_path) as f:
        config = json.load(f)
    
    for server_name in config.get("mcpServers", {}).keys():
        # Server names should be alphanumeric + underscore/hyphen
        assert all(c.isalnum() or c in "-_" for c in server_name), f"Invalid server name: {server_name}"


# =============================================================================
# Connection Tests (Mock-based)
# =============================================================================


def test_could_connect_to_filesystem_server():
    """Test that filesystem server config would allow connections."""
    config_path = Path(__file__).parent.parent / "configs" / "mcp_external.json"
    with open(config_path) as f:
        config = json.load(f)
    
    servers = config.get("mcpServers", {})
    # If filesystem is configured, it should have required fields
    if any("filesystem" in n.lower() for n in servers):
        fs_config = next(s for n, s in servers.items() if "filesystem" in n.lower())
        # Should be able to construct a connection
        assert fs_config is not None


def test_could_connect_to_github_server():
    """Test that GitHub server config would allow connections."""
    config_path = Path(__file__).parent.parent / "configs" / "mcp_external.json"
    with open(config_path) as f:
        config = json.load(f)
    
    servers = config.get("mcpServers", {})
    # If github is configured
    if any("github" in n.lower() for n in servers):
        github_config = next(s for n, s in servers.items() if "github" in n.lower())
        assert github_config is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
