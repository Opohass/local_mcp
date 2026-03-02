"""Shared utilities for MCP HOL servers."""

import logging
import sys


def setup_logging(name: str, level: int = logging.INFO) -> logging.Logger:
    """Configure logging for an MCP server. Logs to stderr to avoid polluting stdio transport."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s"))
    logger.addHandler(handler)
    return logger
