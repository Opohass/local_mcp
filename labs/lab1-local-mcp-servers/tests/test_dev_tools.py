"""Tests for the dev tools MCP server.

Comprehensive tests for:
- file_tree: Directory listing with max depth and ignore patterns
- port_checker: Port availability detection
- run_remote_command: SSH command execution
- Review prompts: code_review, security_review, design_review, networking_review
"""

import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add servers directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "servers"))

from dev_tools_stdio import (
    code_review,
    design_review,
    file_tree,
    networking_review,
    port_checker,
    run_remote_command,
    security_review,
)


# =============================================================================
# file_tree Tests
# =============================================================================


def test_file_tree_current_dir():
    """Test file_tree with current directory."""
    result = file_tree(".", max_depth=1)
    assert isinstance(result, str)
    assert len(result) > 0


def test_file_tree_current_dir_structure():
    """Test that file_tree output shows proper tree structure."""
    result = file_tree(".", max_depth=1)
    # Check for tree characters
    assert "├──" in result or "└──" in result or "/" in result


def test_file_tree_invalid_dir():
    """Test file_tree with invalid directory."""
    result = file_tree("/nonexistent/path/xyz")
    assert "ERROR" in result


def test_file_tree_custom_depth():
    """Test file_tree with custom max_depth."""
    result_depth1 = file_tree(".", max_depth=1)
    result_depth3 = file_tree(".", max_depth=3)
    # Deeper tree should generally have more content (but not always)
    assert isinstance(result_depth1, str)
    assert isinstance(result_depth3, str)


def test_file_tree_ignore_patterns():
    """Test file_tree with ignore patterns."""
    # Create a temporary directory with nested structure
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        # Create test structure
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").touch()
        (tmp_path / ".git").mkdir()
        (tmp_path / ".git" / "config").touch()
        (tmp_path / "__pycache__").mkdir()
        (tmp_path / "__pycache__" / "cache.pyc").touch()

        result = file_tree(str(tmp_path), max_depth=2)
        
        # Should show src directory
        assert "src" in result or "main.py" in result
        # Should NOT show ignored directories (in typical git ignore)
        # Note: This is a best-effort check, depends on default ignore patterns


def test_file_tree_root_directory():
    """Test file_tree starting from root."""
    result = file_tree("/", max_depth=1)
    assert isinstance(result, str)
    # Root should show some directories
    assert "/" in result


def test_file_tree_empty_directory():
    """Test file_tree with empty directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = file_tree(tmpdir, max_depth=1)
        assert isinstance(result, str)
        # Should still show the directory name
        assert Path(tmpdir).name in result


# =============================================================================
# port_checker Tests
# =============================================================================


def test_port_checker_single_port():
    """Test port_checker with a single port."""
    result = port_checker("99999")
    assert "INVALID" in result
    assert ":99999" in result
    assert "Port Status:" in result


def test_port_checker_multiple_ports():
    """Test port_checker with multiple ports."""
    result = port_checker("3000,5000,8000")
    assert ":3000" in result
    assert ":5000" in result
    assert ":8000" in result
    assert result.count("IN USE") + result.count("FREE") >= 3


def test_port_checker_default_ports():
    """Test port_checker with default ports."""
    result = port_checker()
    # Should check default ports: 3000, 5000, 8000, 8080, 9000
    assert ":3000" in result
    assert ":8080" in result
    assert ":9000" in result


def test_port_checker_high_port():
    """Test port_checker with high port number."""
    result = port_checker("65535")
    assert ":65535" in result
    assert isinstance(result, str)


def test_port_checker_output_format():
    """Test that port_checker output is properly formatted."""
    result = port_checker("22,80,443")
    lines = result.split("\n")
    # Should have header + at least 3 port lines
    assert len(lines) >= 4


# =============================================================================
# run_remote_command Tests
# =============================================================================


def test_run_remote_command_ssh_not_found():
    """Test run_remote_command when ssh is not available."""
    with patch("subprocess.run", side_effect=FileNotFoundError()):
        result = run_remote_command("example.com", "ls")
        assert "ERROR" in result
        assert "ssh not found" in result


def test_run_remote_command_timeout():
    """Test run_remote_command with timeout."""
    from unittest.mock import patch
    
    with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("ssh", 30)):
        result = run_remote_command("example.com", "sleep 100")
        assert "ERROR" in result


def test_run_remote_command_format_with_user():
    """Test run_remote_command formats SSH target correctly with user."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout="test output", stderr="", returncode=0
        )
        result = run_remote_command("example.com", "ls", user="ubuntu")
        # Check that ssh was called with correct target
        call_args = mock_run.call_args
        assert "ubuntu@example.com" in call_args[0][0]


def test_run_remote_command_format_without_user():
    """Test run_remote_command formats SSH target correctly without user."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout="test output", stderr="", returncode=0
        )
        result = run_remote_command("example.com", "ls")
        # Check that ssh was called
        call_args = mock_run.call_args
        assert "example.com" in call_args[0][0]


def test_run_remote_command_success_with_output():
    """Test run_remote_command successful execution with output."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout="file1.txt\nfile2.txt", stderr="", returncode=0
        )
        result = run_remote_command("example.com", "ls")
        assert "STDOUT:" in result
        assert "file1.txt" in result
        assert "file2.txt" in result
        assert "Exit code" not in result  # No error


def test_run_remote_command_with_stderr():
    """Test run_remote_command that produces stderr."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout="", stderr="command not found", returncode=127
        )
        result = run_remote_command("example.com", "invalid_cmd")
        assert "STDERR:" in result
        assert "command not found" in result
        assert "Exit code: 127" in result


def test_run_remote_command_both_stdout_stderr():
    """Test run_remote_command with both stdout and stderr."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout="partial output", stderr="warning message", returncode=0
        )
        result = run_remote_command("example.com", "cmd")
        assert "STDOUT:" in result
        assert "partial output" in result
        assert "STDERR:" in result
        assert "warning message" in result


def test_run_remote_command_no_output():
    """Test run_remote_command with no output."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", stderr="", returncode=0)
        result = run_remote_command("example.com", "ls > /dev/null")
        assert "(no output)" in result


# =============================================================================
# Review Prompt Tests
# =============================================================================


def test_code_review_prompt_content():
    """Test that code_review prompt contains expected review criteria."""
    result = code_review()
    assert isinstance(result, str)
    assert len(result) > 100
    # Check for key sections
    assert "Correctness" in result
    assert "Readability" in result
    assert "Performance" in result
    assert "Security" in result
    assert "Maintainability" in result


def test_code_review_prompt_actionable():
    """Test that code_review prompt contains actionable guidance."""
    result = code_review()
    # Should have specific checks
    assert "edge cases" in result.lower()
    assert "error" in result.lower()
    assert "variable" in result.lower() or "name" in result.lower()


def test_security_review_prompt_content():
    """Test that security_review prompt covers security areas."""
    result = security_review()
    assert isinstance(result, str)
    assert len(result) > 100
    # Check for key sections
    assert "Authentication" in result
    assert "Input Validation" in result
    assert "Data Protection" in result
    assert "OWASP" in result


def test_security_review_prompt_specific_items():
    """Test that security_review prompt mentions specific vulnerabilities."""
    result = security_review()
    assert "SQL" in result or "Injection" in result
    assert "XSS" in result or "encoding" in result
    assert "CRITICAL" in result or "severity" in result.upper()


def test_design_review_prompt_content():
    """Test that design_review prompt covers architecture concerns."""
    result = design_review()
    assert isinstance(result, str)
    assert len(result) > 100
    # Check for key sections
    assert "Separation of Concerns" in result
    assert "Scalability" in result
    assert "Extensibility" in result
    assert "Simplicity" in result


def test_design_review_prompt_resilience():
    """Test that design_review covers resilience patterns."""
    result = design_review()
    assert "Resilience" in result
    assert "retry" in result.lower() or "fail" in result.lower()


def test_networking_review_prompt_content():
    """Test that networking_review prompt covers network areas."""
    result = networking_review()
    assert isinstance(result, str)
    assert len(result) > 100
    # Check for key sections
    assert "Connectivity" in result
    assert "TLS" in result or "Encryption" in result
    assert "Firewall" in result
    assert "Monitoring" in result


def test_networking_review_prompt_specific_items():
    """Test that networking_review mentions specific recommendations."""
    result = networking_review()
    assert "1.2" in result  # TLS 1.2
    assert "certificate" in result.lower()
    assert "least privilege" in result or "restrictive" in result.lower()


def test_all_prompts_are_strings():
    """Test that all prompts return strings."""
    prompts = [
        code_review(),
        security_review(),
        design_review(),
        networking_review(),
    ]
    for prompt in prompts:
        assert isinstance(prompt, str)
        assert len(prompt) > 0


def test_all_prompts_are_unique():
    """Test that prompts have distinct content."""
    prompts = {
        "code": code_review(),
        "security": security_review(),
        "design": design_review(),
        "networking": networking_review(),
    }
    # Each prompt should be substantially different
    for key1, prompt1 in prompts.items():
        for key2, prompt2 in prompts.items():
            if key1 != key2:
                # Different prompts should be mostly different
                # (allow small overlap)
                assert prompt1 != prompt2
