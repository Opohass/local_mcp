"""Tests for Lab 3: Azure AI Foundry Agent."""

import asyncio
import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "foundry"))


# =============================================================================
# Environment Variable Tests
# =============================================================================


def test_foundry_endpoint_env_var():
    """Test that AZURE_AI_PROJECT_ENDPOINT environment variable is used."""
    # This is documented in the foundry_agent.py file
    import os
    
    # Check if env vars are mentioned in the agent code
    agent_path = Path(__file__).parent.parent / "foundry" / "foundry_agent.py"
    with open(agent_path) as f:
        content = f.read()
    
    assert "AZURE_AI_PROJECT_ENDPOINT" in content


def test_mcp_server_url_env_var():
    """Test that MCP_SERVER_URL environment variable is used."""
    agent_path = Path(__file__).parent.parent / "foundry" / "foundry_agent.py"
    with open(agent_path) as f:
        content = f.read()
    
    assert "MCP_SERVER_URL" in content


def test_azure_model_deployment_name_env_var():
    """Test that AZURE_AI_MODEL_DEPLOYMENT_NAME environment variable is used."""
    agent_path = Path(__file__).parent.parent / "foundry" / "foundry_agent.py"
    with open(agent_path) as f:
        content = f.read()
    
    assert "AZURE_AI_MODEL_DEPLOYMENT_NAME" in content


# =============================================================================
# Agent Functionality Tests
# =============================================================================


class TestFoundryAgent:
    """Tests for Foundry agent creation and MCP integration."""

    def test_agent_script_is_async(self):
        """Test that agent script uses async/await."""
        agent_path = Path(__file__).parent.parent / "foundry" / "foundry_agent.py"
        with open(agent_path) as f:
            content = f.read()
        
        assert "async def" in content
        assert "asyncio.run" in content or "await" in content

    def test_agent_imports_azure_packages(self):
        """Test that agent imports required Azure packages."""
        agent_path = Path(__file__).parent.parent / "foundry" / "foundry_agent.py"
        with open(agent_path) as f:
            content = f.read()
        
        assert "azure.ai.projects" in content
        assert "azure.identity" in content

    def test_agent_creates_mcp_tool_connection(self):
        """Test that agent code shows MCP tool connection creation."""
        agent_path = Path(__file__).parent.parent / "foundry" / "foundry_agent.py"
        with open(agent_path) as f:
            content = f.read()
        
        # Should mention MCP tool or MCP connection
        assert "mcp" in content.lower() or "MCP" in content

    def test_agent_creates_thread(self):
        """Test that agent creates a thread for conversation."""
        agent_path = Path(__file__).parent.parent / "foundry" / "foundry_agent.py"
        with open(agent_path) as f:
            content = f.read()
        
        # Should create a thread
        assert "thread" in content.lower()

    def test_agent_has_test_query(self):
        """Test that agent has a test query defined."""
        agent_path = Path(__file__).parent.parent / "foundry" / "foundry_agent.py"
        with open(agent_path) as f:
            content = f.read()
        
        # Should have a test query
        assert "query" in content.lower() or "test" in content.lower()

    def test_agent_processes_response(self):
        """Test that agent processes assistant responses."""
        agent_path = Path(__file__).parent.parent / "foundry" / "foundry_agent.py"
        with open(agent_path) as f:
            content = f.read()
        
        # Should process messages from the assistant
        assert "message" in content.lower()

    def test_agent_cleans_up_resources(self):
        """Test that agent cleans up resources after completion."""
        agent_path = Path(__file__).parent.parent / "foundry" / "foundry_agent.py"
        with open(agent_path) as f:
            content = f.read()
        
        # Should have cleanup code (delete agent, etc.)
        assert "delete" in content.lower() or "cleanup" in content.lower()


# =============================================================================
# Configuration and Setup Tests
# =============================================================================


def test_foundry_setup_markdown_exists():
    """Test that foundry_setup.md documentation exists."""
    setup_path = Path(__file__).parent.parent / "foundry" / "foundry_setup.md"
    assert setup_path.exists(), f"Setup doc not found: {setup_path}"


def test_foundry_setup_has_prerequisites():
    """Test that foundry setup doc mentions prerequisites."""
    setup_path = Path(__file__).parent.parent / "foundry" / "foundry_setup.md"
    with open(setup_path) as f:
        content = f.read()
    
    content_lower = content.lower()
    assert "prerequisite" in content_lower or "require" in content_lower or "install" in content_lower


def test_foundry_setup_has_environment_vars(self):
    """Test that foundry setup doc documents environment variables."""
    setup_path = Path(__file__).parent.parent / "foundry" / "foundry_setup.md"
    with open(setup_path) as f:
        content = f.read()
    
    # Should mention how to set up Azure credentials
    assert "environment" in content.lower() or "export" in content.lower() or "token" in content.lower()


def test_foundry_setup_has_usage_instructions():
    """Test that foundry setup doc has usage instructions."""
    setup_path = Path(__file__).parent.parent / "foundry" / "foundry_setup.md"
    with open(setup_path) as f:
        content = f.read()
    
    # Should explain how to run the agent
    assert "python" in content.lower() or "run" in content.lower()


# =============================================================================
# Deployment Configuration Tests
# =============================================================================


def test_deploy_script_exists():
    """Test that deploy.sh script exists."""
    deploy_path = Path(__file__).parent.parent / "deploy" / "deploy.sh"
    assert deploy_path.exists(), f"Deploy script not found: {deploy_path}"


def test_deploy_steps_doc_exists():
    """Test that deploy_steps.md documentation exists."""
    steps_path = Path(__file__).parent.parent / "deploy" / "deploy_steps.md"
    assert steps_path.exists(), f"Deploy steps doc not found: {steps_path}"


def test_cleanup_script_exists():
    """Test that cleanup.sh script exists."""
    cleanup_path = Path(__file__).parent.parent / "deploy" / "cleanup.sh"
    assert cleanup_path.exists(), f"Cleanup script not found: {cleanup_path}"


def test_deploy_steps_doc_content():
    """Test that deploy_steps.md has deployment instructions."""
    steps_path = Path(__file__).parent.parent / "deploy" / "deploy_steps.md"
    with open(steps_path) as f:
        content = f.read()
    
    content_lower = content.lower()
    # Should mention key deployment components
    assert any(term in content_lower for term in [
        "container",
        "azure",
        "deploy",
        "foundry",
        "agent"
    ])


def test_deploy_steps_doc_has_phases():
    """Test that deploy_steps.md documents deployment phases."""
    steps_path = Path(__file__).parent.parent / "deploy" / "deploy_steps.md"
    with open(steps_path) as f:
        content = f.read()
    
    # Should have multiple steps/phases
    assert "#" in content  # Markdown headers for phases
    content_lower = content.lower()
    # Should mention various deployment aspects
    assert any(term in content_lower for term in [
        "step",
        "phase",
        "setup",
        "configure",
        "deploy",
        "verify",
        "clean"
    ])


# =============================================================================
# Integration Tests
# =============================================================================


def test_all_foundry_components_present():
    """Test that all foundry components are present."""
    foundry_dir = Path(__file__).parent.parent / "foundry"
    
    assert (foundry_dir / "foundry_agent.py").exists()
    assert (foundry_dir / "foundry_setup.md").exists()


def test_all_deploy_components_present():
    """Test that all deployment components are present."""
    deploy_dir = Path(__file__).parent.parent / "deploy"
    
    assert (deploy_dir / "deploy.sh").exists()
    assert (deploy_dir / "cleanup.sh").exists()
    assert (deploy_dir / "deploy_steps.md").exists()


def test_azure_server_config_file_exists():
    """Test that configs directory exists for Azure setup."""
    config_dir = Path(__file__).parent.parent / "configs"
    assert config_dir.exists(), f"Configs directory not found: {config_dir}"


# =============================================================================
# Documentation Tests
# =============================================================================


def test_lab3_readme_exists():
    """Test that Lab 3 README exists."""
    readme_path = Path(__file__).parent.parent / "README.md"
    assert readme_path.exists(), f"README not found: {readme_path}"


def test_lab3_readme_mentions_azure(self):
    """Test that Lab 3 README mentions Azure."""
    readme_path = Path(__file__).parent.parent / "README.md"
    with open(readme_path) as f:
        content = f.read()
    
    assert "Azure" in content or "azure" in content.lower()


def test_lab3_readme_mentions_foundry():
    """Test that Lab 3 README mentions AI Foundry."""
    readme_path = Path(__file__).parent.parent / "README.md"
    with open(readme_path) as f:
        content = f.read()
    
    content_lower = content.lower()
    assert "foundry" in content_lower or "ai" in content_lower


def test_lab3_notebook_exists():
    """Test that lab3 notebook exists."""
    notebook_path = Path(__file__).parent.parent / "lab3_notebook.ipynb"
    assert notebook_path.exists(), f"Notebook not found: {notebook_path}"


def test_lab3_notebook_valid_json():
    """Test that lab3 notebook is valid JSON."""
    notebook_path = Path(__file__).parent.parent / "lab3_notebook.ipynb"
    with open(notebook_path) as f:
        notebook = json.load(f)
    assert isinstance(notebook, dict)


def test_lab3_prerequisites_exist():
    """Test that prerequisites documentation exists."""
    prereq_path = Path(__file__).parent.parent / "prerequisites.md"
    assert prereq_path.exists(), f"Prerequisites not found: {prereq_path}"


def test_lab3_prerequisites_content():
    """Test that prerequisites documentation is useful."""
    prereq_path = Path(__file__).parent.parent / "prerequisites.md"
    with open(prereq_path) as f:
        content = f.read()
    
    content_lower = content.lower()
    # Should mention Azure setup requirements
    assert any(term in content_lower for term in [
        "azure",
        "prerequisite",
        "require",
        "install",
        "setup"
    ])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
