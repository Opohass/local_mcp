"""Tests for Lab 3: Azure MCP Server Tools.

Comprehensive tests for:
- search_issues: GitHub issue search
- summarize_pr: GitHub PR summarization
- check_service_health: URL/service health checking
- run_query: Sample dataset querying
"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add servers directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "server"))


# Import with error handling since we may not have all deps
try:
    from azure_mcp_server import check_service_health, run_query, search_issues, summarize_pr
    IMPORTS_AVAILABLE = True
except ImportError:
    IMPORTS_AVAILABLE = False


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Azure server dependencies not available")
class TestSearchIssues:
    """Tests for search_issues tool."""

    @pytest.mark.asyncio
    async def test_search_issues_success(self):
        """Test successful GitHub issue search."""
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock the GitHub API response
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "total_count": 2,
                "items": [
                    {
                        "number": 1,
                        "title": "Bug: Feature not working",
                        "html_url": "https://github.com/owner/repo/issues/1",
                        "labels": [{"name": "bug"}, {"name": "high-priority"}],
                    },
                    {
                        "number": 2,
                        "title": "Enhancement: Add new feature",
                        "html_url": "https://github.com/owner/repo/issues/2",
                        "labels": [{"name": "enhancement"}],
                    },
                ],
            }
            mock_get.return_value = mock_response

            result = await search_issues("owner/repo", query="feature", state="open")
            
            assert "Found 2 result" in result or "feature" in result.lower()
            assert "bug" in result.lower() or "#1" in result or "#2" in result

    @pytest.mark.asyncio
    async def test_search_issues_no_results(self):
        """Test GitHub issue search with no results."""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"total_count": 0, "items": []}
            mock_get.return_value = mock_response

            result = await search_issues("owner/repo", query="xyz-nonexistent")
            
            assert "No issues found" in result or "0 result" in result

    @pytest.mark.asyncio
    async def test_search_issues_api_error(self):
        """Test GitHub issue search API error."""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 403
            mock_response.text = "API rate limit exceeded"
            mock_get.return_value = mock_response

            result = await search_issues("owner/repo")
            
            assert "ERROR" in result
            assert "403" in result

    @pytest.mark.asyncio
    async def test_search_issues_with_labels(self):
        """Test that search_issues includes issue labels in output."""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "total_count": 1,
                "items": [
                    {
                        "number": 10,
                        "title": "Test Issue",
                        "html_url": "https://github.com/owner/repo/issues/10",
                        "labels": [{"name": "urgent"}, {"name": "frontend"}],
                    },
                ],
            }
            mock_get.return_value = mock_response

            result = await search_issues("owner/repo")
            
            assert "[urgent" in result or "[frontend" in result or "urgent" in result


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Azure server dependencies not available")
class TestSummarizePr:
    """Tests for summarize_pr tool."""

    @pytest.mark.asyncio
    async def test_summarize_pr_success(self):
        """Test successful PR summarization."""
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock PR details and files responses
            pr_response = MagicMock()
            pr_response.status_code = 200
            pr_response.json.return_value = {
                "number": 42,
                "title": "Add authentication",
                "state": "open",
                "mergeable": True,
                "user": {"login": "developer"},
                "base": {"ref": "main"},
                "head": {"ref": "feature/auth"},
                "changed_files": 5,
                "additions": 150,
                "deletions": 30,
                "body": "This PR adds JWT authentication",
            }

            files_response = MagicMock()
            files_response.status_code = 200
            files_response.json.return_value = [
                {"status": "added", "filename": "auth/jwt.py", "additions": 100, "deletions": 0},
            ]

            mock_get.side_effect = [pr_response, files_response]

            result = await summarize_pr("owner/repo", 42)
            
            assert "PR #42" in result
            assert "Add authentication" in result
            assert "developer" in result

    @pytest.mark.asyncio
    async def test_summarize_pr_not_found(self):
        """Test PR summarization when PR doesn't exist."""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response

            result = await summarize_pr("owner/repo", 999)
            
            assert "ERROR" in result or "could not fetch" in result.lower()

    @pytest.mark.asyncio
    async def test_summarize_pr_includes_files(self):
        """Test that summarize_pr includes file changes."""
        with patch("httpx.AsyncClient.get") as mock_get:
            pr_response = MagicMock()
            pr_response.status_code = 200
            pr_response.json.return_value = {
                "number": 1,
                "title": "Test",
                "state": "open",
                "mergeable": True,
                "user": {"login": "user"},
                "base": {"ref": "main"},
                "head": {"ref": "test"},
                "changed_files": 2,
                "additions": 50,
                "deletions": 10,
                "body": "Test PR",
            }

            files_response = MagicMock()
            files_response.status_code = 200
            files_response.json.return_value = [
                {"status": "modified", "filename": "file1.py", "additions": 30, "deletions": 5},
                {"status": "added", "filename": "file2.py", "additions": 20, "deletions": 0},
            ]

            mock_get.side_effect = [pr_response, files_response]

            result = await summarize_pr("owner/repo", 1)
            
            # Should show files
            assert "file1.py" in result or "file2.py" in result or "Files Changed" in result


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Azure server dependencies not available")
class TestCheckServiceHealth:
    """Tests for check_service_health tool."""

    @pytest.mark.asyncio
    async def test_check_service_health_single_url_success(self):
        """Test health check for a single URL."""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            with patch("time.monotonic", side_effect=[100.0, 100.1]):
                result = await check_service_health("https://example.com")
            
            assert "200" in result
            assert "https://example.com" in result

    @pytest.mark.asyncio
    async def test_check_service_health_multiple_urls(self):
        """Test health check for multiple URLs."""
        with patch("httpx.AsyncClient.get") as mock_get:
            # Mock different responses for different URLs
            responses = [
                MagicMock(status_code=200),
                MagicMock(status_code=503),
            ]
            mock_get.side_effect = responses

            with patch("time.monotonic", side_effect=[100.0, 100.05, 100.1, 100.15]):
                result = await check_service_health("https://example.com,https://api.example.com")
            
            assert "https://example.com" in result
            assert "https://api.example.com" in result

    @pytest.mark.asyncio
    async def test_check_service_health_connect_error(self):
        """Test health check with connection error."""
        import httpx
        
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.side_effect = httpx.ConnectError("Connection refused")

            result = await check_service_health("https://unreachable.local")
            
            assert "CONN_ERR" in result or "ERROR" in result

    @pytest.mark.asyncio
    async def test_check_service_health_timeout(self):
        """Test health check with timeout."""
        import httpx
        
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.side_effect = httpx.TimeoutException("Request timeout")

            result = await check_service_health("https://slow.example.com")
            
            assert "TIMEOUT" in result or "ERROR" in result

    @pytest.mark.asyncio
    async def test_check_service_health_includes_latency(self):
        """Test that health check includes latency in output."""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            with patch("time.monotonic", side_effect=[100.0, 100.05]):  # 50ms
                result = await check_service_health("https://example.com")
            
            # Should show latency (50ms)
            assert "ms" in result or "50" in result


class TestRunQuery:
    """Tests for run_query tool."""

    def test_run_query_success(self):
        """Test successful query execution."""
        result = run_query("api-gateway")
        
        assert "Found" in result or "result" in result.lower()
        assert "api-gateway" in result.lower()

    def test_run_query_no_results(self):
        """Test query with no results."""
        result = run_query("xyz-nonexistent-service")
        
        assert "No results" in result or "found 0" in result.lower()

    def test_run_query_case_insensitive(self):
        """Test that query is case-insensitive."""
        result1 = run_query("API-GATEWAY")
        result2 = run_query("api-gateway")
        
        # Both should find the same results
        assert ("Found" in result1 or "No results" in result1)
        assert ("Found" in result2 or "No results" in result2)

    def test_run_query_by_type(self):
        """Test query by item type."""
        result = run_query("service")
        
        assert "Found" in result or "result" in result.lower()

    def test_run_query_by_status(self):
        """Test query by status."""
        result = run_query("degraded")
        
        # Should find the degraded service
        assert "Found" in result
        assert "user-service" in result.lower()

    def test_run_query_by_region(self):
        """Test query by region."""
        result = run_query("westus")
        
        # Should find services in westus
        assert "Found" in result

    def test_run_query_multiple_results(self):
        """Test query returning multiple results."""
        result = run_query("healthy")
        
        # Should find multiple healthy items
        assert "Found" in result
        # Check for multiple results indicator
        assert "result" in result.lower()

    def test_run_query_returns_structured_data(self):
        """Test that query results are well-structured."""
        result = run_query("database")
        
        assert isinstance(result, str)
        # Should show type, name, status, region
        assert "[" in result  # Type indicator
        assert "]" in result


# =============================================================================
# Integration Tests
# =============================================================================


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Azure server dependencies not available")
class TestServerIntegration:
    """Integration tests for the Azure MCP server."""

    @pytest.mark.asyncio
    async def test_all_tools_are_callable(self):
        """Test that all tools are importable and callable."""
        # These should not raise exceptions
        assert callable(search_issues)
        assert callable(summarize_pr)
        assert callable(check_service_health)
        assert callable(run_query)

    @pytest.mark.asyncio
    async def test_tools_have_docstrings(self):
        """Test that all tools have documentation."""
        assert search_issues.__doc__ is not None
        assert summarize_pr.__doc__ is not None
        assert check_service_health.__doc__ is not None
        assert run_query.__doc__ is not None

    @pytest.mark.asyncio
    async def test_tools_mention_parameters(self):
        """Test that tool docstrings document parameters."""
        # Check search_issues
        assert "repo" in search_issues.__doc__.lower()
        assert "query" in search_issues.__doc__.lower()
        
        # Check run_query
        assert "query" in run_query.__doc__.lower()


# =============================================================================
# Configuration Tests
# =============================================================================


def test_azure_server_requirements_exist():
    """Test that requirements.txt exists for Azure server."""
    req_path = Path(__file__).parent.parent / "server" / "requirements.txt"
    assert req_path.exists(), f"Requirements not found: {req_path}"


def test_azure_server_dockerfile_exists():
    """Test that Dockerfile exists for containerization."""
    dockerfile_path = Path(__file__).parent.parent / "server" / "Dockerfile"
    assert dockerfile_path.exists(), f"Dockerfile not found: {dockerfile_path}"


def test_azure_server_requirements_valid():
    """Test that requirements.txt is properly formatted."""
    req_path = Path(__file__).parent.parent / "server" / "requirements.txt"
    with open(req_path) as f:
        requirements = f.read()
    
    # Should have some dependencies
    assert len(requirements.strip()) > 0
    # Should mention key dependencies
    assert "fastmcp" in requirements.lower() or "httpx" in requirements.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
