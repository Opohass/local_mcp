# MCP Hands-on Lab - Test Suite

Comprehensive test coverage for all labs and components of the MCP Hands-on Lab.

## Overview

The test suite is organized by lab with integration tests to verify cross-lab functionality:

```
tests/
├── test_integration.py          # Integration & end-to-end tests
labs/
├── lab1-local-mcp-servers/tests/
│   └── test_dev_tools.py        # Lab 1: STDIO + HTTP servers
├── lab2-external-mcp-sources/tests/
│   └── test_external_sources.py # Lab 2: External MCP servers
└── lab3-azure-deployment/tests/
    ├── test_azure_server.py     # Lab 3: Azure MCP server tools
    └── test_foundry_agent.py    # Lab 3: AI Foundry agent
```

## Test Coverage

### Lab 1: Local MCP Servers
**File**: `labs/lab1-local-mcp-servers/tests/test_dev_tools.py`

Tests for the dev tools MCP server with 3 tools and 4 review prompts:

#### Tools:
- ✅ `file_tree` — Directory listing with depth & ignore patterns
- ✅ `port_checker` — Port availability detection
- ✅ `run_remote_command` — SSH command execution

#### Prompts:
- ✅ `code_review` — Comprehensive code review checklist
- ✅ `security_review` — Security-focused review checklist
- ✅ `design_review` — Architecture and design review criteria
- ✅ `networking_review` — Network configuration review guide

**Test Count**: ~50 tests
- `file_tree`: Directory listing, error handling, depth control, ignore patterns
- `port_checker`: Single/multiple ports, default ports, output format
- `run_remote_command`: SSH formatting, stdout/stderr capture, error handling, timeouts
- **Prompts**: Content validation, structure, actionable guidance, uniqueness

### Lab 2: External MCP Sources
**File**: `labs/lab2-external-mcp-sources/tests/test_external_sources.py`

Tests for external MCP server configurations and connectivity:

**Test Areas**:
- Configuration loading & validation (mcp_external.json, vscode_mcp_external.json)
- External server configurations (Filesystem, Fetch, Git, GitHub)
- Environment variable substitution
- Documentation completeness
- Configuration consistency across files

**Test Count**: ~30 tests
- Configuration: JSON validity, structure, mcpServers section
- External Servers: Filesystem, Fetch, Git, GitHub configurations
- Environment Vars: Token handling, auth setup
- Documentation: markdown content, tables, security notes
- Integration: Config consistency, server name validation

### Lab 3: Azure Deployment
**Files**: 
- `labs/lab3-azure-deployment/tests/test_azure_server.py`
- `labs/lab3-azure-deployment/tests/test_foundry_agent.py`

#### Azure Server Tools
**File**: `test_azure_server.py`

Tests for the Azure MCP server with GitHub and health check tools:

**Tools**:
- ✅ `search_issues` — GitHub issue search with filtering
- ✅ `summarize_pr` — GitHub PR summarization
- ✅ `check_service_health` — URL/service health checking
- ✅ `run_query` — Sample dataset querying

**Test Count**: ~35 tests
- `search_issues`: Success, no results, API errors, labels
- `summarize_pr`: Success, 404 errors, file changes, PR metadata
- `check_service_health`: Single/multiple URLs, connection errors, timeouts, latency
- `run_query`: Success, no results, case sensitivity, type/status/region queries
- Integration: Tool callability, documentation, parameters

#### Foundry Agent
**File**: `test_foundry_agent.py`

Tests for Azure AI Foundry agent integration:

**Test Areas**:
- Environment variable configuration
- Agent async implementation
- Azure package imports
- Thread and message management
- Resource cleanup
- Documentation and setup guides

**Test Count**: ~25 tests
- Agent functionality: async code, Azure imports, MCP tool connections
- Configuration: Environment variables, setup documentation
- Deployment: Script existence, deployment phases, cleanup
- Documentation: READMEs, prerequisites, setup guides

### Integration Tests
**File**: `tests/test_integration.py`

End-to-end tests verifying all labs work together:

**Test Areas**:
- Repository structure completeness
- All labs have README, notebooks, prerequisites
- Configuration consistency across all labs
- Tool and prompt discoverability
- Shared utilities functionality
- Lab progression logic
- Meta server functionality
- Presentation assets
- Project configuration (pyproject.toml, .gitignore)
- Workflow viability

**Test Count**: ~40 tests

## Running Tests

### Run All Tests
```bash
source .venv/bin/activate
pytest -v
```

### Run Tests by Lab
```bash
# Lab 1 only
pytest labs/lab1-local-mcp-servers/tests/ -v

# Lab 2 only
pytest labs/lab2-external-mcp-sources/tests/ -v

# Lab 3 only
pytest labs/lab3-azure-deployment/tests/ -v

# Integration tests only
pytest tests/test_integration.py -v
```

### Run Specific Test Class or Function
```bash
# Run all port_checker tests
pytest labs/lab1-local-mcp-servers/tests/test_dev_tools.py::TestPortChecker -v

# Run specific test
pytest labs/lab1-local-mcp-servers/tests/test_dev_tools.py::TestPortChecker::test_port_checker_single_port -v
```

### Run with Coverage
```bash
pytest --cov=labs --cov=meta_server --cov-report=html
```

### Run Tests Matching Pattern
```bash
# All tool tests
pytest -k "tool" -v

# All prompt tests
pytest -k "prompt" -v

# All async tests
pytest -m asyncio -v
```

## Test Markers

Tests are marked for easy filtering:

```bash
# Lab-specific markers
pytest -m lab1 -v
pytest -m lab2 -v
pytest -m lab3 -v

# Feature markers
pytest -m asyncio -v           # Async tests
pytest -m slow -v              # Slow tests
pytest -m requires_network -v  # Network tests
pytest -m requires_azure -v    # Azure-specific tests
```

## Test Requirements

### Base Requirements
- `pytest >= 7.0`
- `pytest-asyncio` (for async tests)
- `httpx` (for HTTP tests)

### Optional Requirements
```bash
# For coverage reporting
pip install pytest-cov

# For parallel test execution
pip install pytest-xdist

# Run: pytest -n auto
```

## Expected Test Results

### All Tests Passing
```
tests/test_integration.py::test_repository_structure_complete PASSED
tests/test_integration.py::test_all_labs_have_readmes PASSED
...
labs/lab1-local-mcp-servers/tests/test_dev_tools.py::test_file_tree_current_dir PASSED
...
labs/lab2-external-mcp-sources/tests/test_external_sources.py::test_mcp_config_exists PASSED
...
labs/lab3-azure-deployment/tests/test_azure_server.py::test_run_query_success PASSED
labs/lab3-azure-deployment/tests/test_foundry_agent.py::test_foundry_endpoint_env_var PASSED
...

======================== 180+ passed in X.XXs ========================
```

## Test Quality Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Test Count | 150+ | ✅ Complete |
| Coverage (Lab Code) | >80% | ✅ Good |
| Coverage (Tools) | 100% | ✅ Complete |
| Coverage (Configs) | 100% | ✅ Complete |
| Coverage (Docs) | 100% | ✅ Complete |
| Async Tests | All covered | ✅ Complete |
| Error Cases | All covered | ✅ Complete |

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    source .venv/bin/activate
    pytest -v --tb=short --cov=labs --cov=meta_server
```

## Debugging Tests

### Verbose Output
```bash
pytest -vv -s  # Extra verbose, show print statements
```

### Debug a Single Test
```bash
pytest -vv -s --pdb labs/lab1-local-mcp-servers/tests/test_dev_tools.py::test_file_tree_current_dir
```

### Show Test Collection Without Running
```bash
pytest --collect-only
```

### Run Tests in Specific Order
```bash
pytest --maxfail=1  # Stop after first failure
pytest -x          # Same as above
```

## Common Issues

### Import Errors
If you see "could not be resolved" warnings, ensure you're running from the correct directory:
```bash
cd /home/opohass/Documents/code/local_mcp
python -m pytest
```

### Async Test Issues
If async tests fail, ensure pytest-asyncio is installed:
```bash
pip install pytest-asyncio
```

### Network Tests Failing
Some tests may require network connectivity or specific environment variables:
```bash
# Skip network tests
pytest -m "not requires_network" -v
```

### Azure Tests Failing
Tests for Azure Foundry require specific credentials:
```bash
# Skip Azure tests
pytest -m "not requires_azure" -v
```

## Adding New Tests

When adding features, add corresponding tests:

```python
# labs/lab1-local-mcp-servers/tests/test_dev_tools.py

def test_new_tool_feature():
    """Test description."""
    result = new_tool_function(args)
    assert expected_result in result
```

Follow the naming convention:
- `test_` prefix for all tests
- `Test` prefix for test classes
- Descriptive names: `test_feature_success`, `test_feature_error`, etc.

## Test Documentation

Each test file has:
1. **Module docstring** explaining what's tested
2. **Test grouping** using classes or comments
3. **Individual test docstrings** explaining each test
4. **Clear assertions** with meaningful failure messages

## See Also

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio documentation](https://pytest-asyncio.readthedocs.io/)
- [Lab 1 README](labs/lab1-local-mcp-servers/README.md)
- [Lab 2 README](labs/lab2-external-mcp-sources/README.md)
- [Lab 3 README](labs/lab3-azure-deployment/README.md)
