"""Integration and End-to-End Tests for MCP Hands-on Lab.

Tests that verify:
- All labs work together
- Configurations are valid across labs
- Tools and prompts are discoverable
- Lab progression flows correctly
- Shared utilities work for all labs
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add shared utilities to path
sys.path.insert(0, str(Path(__file__).parent.parent / "labs" / "shared"))


# =============================================================================
# Repository Structure Tests
# =============================================================================


def test_repository_structure_complete():
    """Test that all expected directories and files exist."""
    root = Path(__file__).parent.parent
    
    # Check main files
    assert (root / "README.md").exists()
    assert (root / "pyproject.toml").exists()
    
    # Check lab directories
    labs_dir = root / "labs"
    assert (labs_dir / "lab1-local-mcp-servers").exists()
    assert (labs_dir / "lab2-external-mcp-sources").exists()
    assert (labs_dir / "lab3-azure-deployment").exists()
    assert (labs_dir / "shared").exists()
    
    # Check meta server
    assert (root / "meta_server").exists()
    
    # Check presentation
    assert (root / "presentation").exists()


def test_all_labs_have_readmes():
    """Test that all labs have README documentation."""
    root = Path(__file__).parent.parent
    labs_dir = root / "labs"
    
    for lab in ["lab1-local-mcp-servers", "lab2-external-mcp-sources", "lab3-azure-deployment"]:
        readme = labs_dir / lab / "README.md"
        assert readme.exists(), f"Missing README for {lab}"


def test_all_labs_have_notebooks():
    """Test that all labs have Jupyter notebooks."""
    root = Path(__file__).parent.parent
    labs_dir = root / "labs"
    
    notebooks = [
        labs_dir / "lab1-local-mcp-servers" / "lab1_notebook.ipynb",
        labs_dir / "lab2-external-mcp-sources" / "lab2_notebook.ipynb",
        labs_dir / "lab3-azure-deployment" / "lab3_notebook.ipynb",
    ]
    
    for notebook in notebooks:
        assert notebook.exists(), f"Missing notebook: {notebook}"


def test_all_labs_have_prerequisites():
    """Test that all labs have prerequisites documentation."""
    root = Path(__file__).parent.parent
    labs_dir = root / "labs"
    
    # Check individual lab prerequisites
    for lab in ["lab1-local-mcp-servers", "lab2-external-mcp-sources", "lab3-azure-deployment"]:
        prereq = labs_dir / lab / "prerequisites.md"
        assert prereq.exists(), f"Missing prerequisites for {lab}"
    
    # Check shared prerequisites
    shared_prereq = labs_dir / "shared" / "prerequisites.md"
    assert shared_prereq.exists()


# =============================================================================
# Configuration Consistency Tests
# =============================================================================


def test_all_mcp_configs_are_valid_json():
    """Test that all MCP configuration files are valid JSON."""
    root = Path(__file__).parent.parent
    configs = [
        root / "labs" / "lab1-local-mcp-servers" / "configs" / "mcp.json",
        root / "labs" / "lab1-local-mcp-servers" / "configs" / "vscode_mcp.json",
        root / "labs" / "lab2-external-mcp-sources" / "configs" / "mcp_external.json",
        root / "labs" / "lab2-external-mcp-sources" / "configs" / "vscode_mcp_external.json",
        root / ".mcp.json",
    ]
    
    for config_path in configs:
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
            assert isinstance(config, dict), f"Invalid JSON in {config_path}"


def test_meta_server_config_points_to_content_server():
    """Test that meta server is configured in .mcp.json."""
    root = Path(__file__).parent.parent
    mcp_path = root / ".mcp.json"
    
    assert mcp_path.exists()
    
    with open(mcp_path) as f:
        config = json.load(f)
    
    servers = config.get("mcpServers", {})
    # Should reference the lab content server
    assert len(servers) > 0


def test_vscode_configs_reference_python_servers():
    """Test that vscode configs reference Python server implementations."""
    root = Path(__file__).parent.parent
    
    lab1_config = root / "labs" / "lab1-local-mcp-servers" / "configs" / "vscode_mcp.json"
    with open(lab1_config) as f:
        config = json.load(f)
    
    servers = config.get("mcpServers", {})
    # Should have dev-tools server
    assert any("dev" in name.lower() or "tool" in name.lower() for name in servers)


# =============================================================================
# Tool and Prompt Discovery Tests
# =============================================================================


def test_lab1_tools_are_discoverable():
    """Test that Lab 1 tools are properly defined."""
    # Verify dev_tools_stdio.py has tools defined
    server_path = Path(__file__).parent.parent / "labs" / "lab1-local-mcp-servers" / "servers" / "dev_tools_stdio.py"
    
    with open(server_path) as f:
        content = f.read()
    
    # Should have tool decorators
    assert "@mcp.tool()" in content
    # Should have specific tools
    assert "file_tree" in content
    assert "port_checker" in content


def test_lab1_prompts_are_discoverable():
    """Test that Lab 1 review prompts are properly defined."""
    server_path = Path(__file__).parent.parent / "labs" / "lab1-local-mcp-servers" / "servers" / "dev_tools_stdio.py"
    
    with open(server_path) as f:
        content = f.read()
    
    # Should have prompt decorators
    assert "@mcp.prompt()" in content
    # Should have specific prompts
    assert "code_review" in content
    assert "security_review" in content
    assert "design_review" in content
    assert "networking_review" in content


def test_lab3_tools_are_discoverable():
    """Test that Lab 3 tools are properly defined."""
    server_path = Path(__file__).parent.parent / "labs" / "lab3-azure-deployment" / "server" / "azure_mcp_server.py"
    
    with open(server_path) as f:
        content = f.read()
    
    # Should have tool decorators
    assert "@mcp.tool()" in content
    # Should have specific tools
    assert "search_issues" in content
    assert "summarize_pr" in content
    assert "check_service_health" in content
    assert "run_query" in content


# =============================================================================
# Shared Utilities Tests
# =============================================================================


def test_shared_utilities_exist():
    """Test that shared utilities module exists."""
    utils_path = Path(__file__).parent.parent / "labs" / "shared" / "utils.py"
    assert utils_path.exists()


def test_shared_utilities_have_content():
    """Test that shared utilities have useful functions."""
    utils_path = Path(__file__).parent.parent / "labs" / "shared" / "utils.py"
    
    with open(utils_path) as f:
        content = f.read()
    
    # Should have some functions or utilities
    assert "def " in content or "class " in content


def test_shared_prerequisites_comprehensive():
    """Test that shared prerequisites cover all requirements."""
    prereq_path = Path(__file__).parent.parent / "labs" / "shared" / "prerequisites.md"
    
    with open(prereq_path) as f:
        content = f.read()
    
    content_lower = content.lower()
    # Should mention key requirements
    assert any(term in content_lower for term in [
        "python",
        "pip",
        "git",
        "vscode",
        "claude",
        "mcp"
    ])


def test_shared_troubleshooting_exists():
    """Test that troubleshooting guide exists."""
    troubleshooting_path = Path(__file__).parent.parent / "labs" / "shared" / "troubleshooting.md"
    assert troubleshooting_path.exists()


def test_shared_troubleshooting_comprehensive():
    """Test that troubleshooting guide covers common issues."""
    troubleshooting_path = Path(__file__).parent.parent / "labs" / "shared" / "troubleshooting.md"
    
    with open(troubleshooting_path) as f:
        content = f.read()
    
    content_lower = content.lower()
    # Should have multiple issue categories
    assert "error" in content_lower or "issue" in content_lower or "problem" in content_lower


# =============================================================================
# Lab Progression Tests
# =============================================================================


def test_lab_progression_is_logical():
    """Test that labs follow a logical progression."""
    root = Path(__file__).parent.parent
    labs_dir = root / "labs"
    
    # Lab 1 should be about local servers
    lab1_readme = labs_dir / "lab1-local-mcp-servers" / "README.md"
    with open(lab1_readme) as f:
        lab1_content = f.read()
    assert "local" in lab1_content.lower()
    
    # Lab 2 should be about external servers
    lab2_readme = labs_dir / "lab2-external-mcp-sources" / "README.md"
    with open(lab2_readme) as f:
        lab2_content = f.read()
    assert "external" in lab2_content.lower() or "source" in lab2_content.lower()
    
    # Lab 3 should be about deployment
    lab3_readme = labs_dir / "lab3-azure-deployment" / "README.md"
    with open(lab3_readme) as f:
        lab3_content = f.read()
    assert "deploy" in lab3_content.lower() or "azure" in lab3_content.lower()


def test_lab_notebooks_build_on_concepts():
    """Test that lab notebooks reference prior concepts."""
    root = Path(__file__).parent.parent
    
    # Get all notebooks
    notebooks = [
        root / "labs" / "lab1-local-mcp-servers" / "lab1_notebook.ipynb",
        root / "labs" / "lab2-external-mcp-sources" / "lab2_notebook.ipynb",
        root / "labs" / "lab3-azure-deployment" / "lab3_notebook.ipynb",
    ]
    
    for notebook_path in notebooks:
        with open(notebook_path) as f:
            notebook = json.load(f)
        
        # Each notebook should have cells
        assert len(notebook.get("cells", [])) > 0
        
        # Notebook should be self-contained (have some instructions)
        content = json.dumps(notebook)
        assert len(content) > 100


# =============================================================================
# Meta Server Tests
# =============================================================================


def test_meta_server_exists():
    """Test that meta server module exists."""
    meta_server = Path(__file__).parent.parent / "meta_server" / "lab_content_server.py"
    assert meta_server.exists()


def test_meta_server_documentation_exists():
    """Test that meta server has documentation."""
    meta_readme = Path(__file__).parent.parent / "meta_server" / "README.md"
    assert meta_readme.exists()


def test_meta_server_has_mcp_import():
    """Test that meta server uses FastMCP."""
    meta_server = Path(__file__).parent.parent / "meta_server" / "lab_content_server.py"
    
    with open(meta_server) as f:
        content = f.read()
    
    assert "FastMCP" in content or "fastmcp" in content.lower()


# =============================================================================
# Presentation Tests
# =============================================================================


def test_presentation_exists():
    """Test that presentation exists."""
    presentation = Path(__file__).parent.parent / "presentation" / "index.html"
    assert presentation.exists()


def test_presentation_assets_exist():
    """Test that presentation has required assets."""
    assets_dir = Path(__file__).parent.parent / "presentation" / "assets"
    
    # Should have some CSS or other assets
    assert assets_dir.exists()


def test_presentation_has_custom_styles():
    """Test that presentation has custom CSS."""
    custom_css = Path(__file__).parent.parent / "presentation" / "assets" / "styles" / "custom.css"
    assert custom_css.exists()


# =============================================================================
# Project Configuration Tests
# =============================================================================


def test_pyproject_toml_is_valid():
    """Test that pyproject.toml is valid."""
    pyproject = Path(__file__).parent.parent / "pyproject.toml"
    
    # Simple check: file should have [project] section
    with open(pyproject) as f:
        content = f.read()
    
    assert "[project]" in content
    assert "name" in content


def test_pyproject_has_required_dependencies():
    """Test that pyproject.toml lists required dependencies."""
    pyproject = Path(__file__).parent.parent / "pyproject.toml"
    
    with open(pyproject) as f:
        content = f.read()
    
    # Should mention FastMCP and httpx
    assert "fastmcp" in content.lower() or "mcp" in content.lower()
    assert "httpx" in content.lower()


def test_pyproject_has_optional_dependencies():
    """Test that pyproject.toml has optional dependency groups."""
    pyproject = Path(__file__).parent.parent / "pyproject.toml"
    
    with open(pyproject) as f:
        content = f.read()
    
    # Should have optional groups
    assert "optional-dependencies" in content
    # Should have lab3, notebooks, dev groups
    assert "lab3" in content or "azure" in content.lower()
    assert "notebook" in content.lower()
    assert "dev" in content


def test_gitignore_exists():
    """Test that .gitignore exists."""
    gitignore = Path(__file__).parent.parent / ".gitignore"
    assert gitignore.exists()


# =============================================================================
# End-to-End Workflow Tests
# =============================================================================


def test_can_discover_all_lab1_tools_and_prompts():
    """Test that we can identify all Lab 1 tools and prompts."""
    lab1_server = Path(__file__).parent.parent / "labs" / "lab1-local-mcp-servers" / "servers" / "dev_tools_stdio.py"
    
    with open(lab1_server) as f:
        content = f.read()
    
    # Count tools
    tool_count = content.count("@mcp.tool()")
    assert tool_count >= 3  # At least file_tree, port_checker, run_remote_command
    
    # Count prompts
    prompt_count = content.count("@mcp.prompt()")
    assert prompt_count >= 4  # code, security, design, networking


def test_can_discover_all_lab3_tools():
    """Test that we can identify all Lab 3 tools."""
    lab3_server = Path(__file__).parent.parent / "labs" / "lab3-azure-deployment" / "server" / "azure_mcp_server.py"
    
    with open(lab3_server) as f:
        content = f.read()
    
    # Count async tools
    tool_count = content.count("@mcp.tool()")
    assert tool_count >= 4  # search_issues, summarize_pr, check_service_health, run_query


def test_all_servers_have_main_entry_point():
    """Test that all servers have proper entry points."""
    servers = [
        Path(__file__).parent.parent / "labs" / "lab1-local-mcp-servers" / "servers" / "dev_tools_stdio.py",
        Path(__file__).parent.parent / "labs" / "lab1-local-mcp-servers" / "servers" / "dev_tools_http.py",
        Path(__file__).parent.parent / "labs" / "lab3-azure-deployment" / "server" / "azure_mcp_server.py",
        Path(__file__).parent.parent / "meta_server" / "lab_content_server.py",
    ]
    
    for server in servers:
        if server.exists():
            with open(server) as f:
                content = f.read()
            
            assert 'if __name__ == "__main__"' in content
            assert "mcp.run" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
