#!/usr/bin/env bash
# Quick test runner script for MCP HOL

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Ensure venv is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source .venv/bin/activate
fi

# Show menu
show_menu() {
    echo -e "\n${BLUE}MCP Hands-on Lab - Test Runner${NC}"
    echo "================================"
    echo "1. Run all tests"
    echo "2. Run Lab 1 tests only"
    echo "3. Run Lab 2 tests only"
    echo "4. Run Lab 3 tests only"
    echo "5. Run integration tests only"
    echo "6. Run all tests with coverage"
    echo "7. Run specific test by pattern"
    echo "8. Exit"
    echo ""
}

# Run tests
run_tests() {
    case $1 in
        1)
            echo -e "${GREEN}Running all tests...${NC}"
            pytest -v
            ;;
        2)
            echo -e "${GREEN}Running Lab 1 tests...${NC}"
            pytest labs/lab1-local-mcp-servers/tests/ -v
            ;;
        3)
            echo -e "${GREEN}Running Lab 2 tests...${NC}"
            pytest labs/lab2-external-mcp-sources/tests/ -v
            ;;
        4)
            echo -e "${GREEN}Running Lab 3 tests...${NC}"
            pytest labs/lab3-azure-deployment/tests/ -v
            ;;
        5)
            echo -e "${GREEN}Running integration tests...${NC}"
            pytest tests/test_integration.py -v
            ;;
        6)
            echo -e "${GREEN}Running all tests with coverage...${NC}"
            pytest -v --cov=labs --cov=meta_server --cov-report=html --cov-report=term-missing
            echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"
            ;;
        7)
            read -p "Enter test pattern (e.g., 'port_checker'): " pattern
            echo -e "${GREEN}Running tests matching pattern: $pattern${NC}"
            pytest -k "$pattern" -v
            ;;
        8)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option"
            ;;
    esac
}

# Main loop
if [[ $# -eq 0 ]]; then
    # Interactive mode
    while true; do
        show_menu
        read -p "Select option (1-8): " choice
        run_tests "$choice"
    done
else
    # Script mode with argument
    run_tests "$1"
fi
