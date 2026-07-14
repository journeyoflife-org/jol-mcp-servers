"""Shared pytest fixtures for jol-mcp-servers."""

from __future__ import annotations

import os
from typing import Any

import pytest


@pytest.fixture
def mock_auth_payload() -> dict[str, Any]:
    """Return a valid mock JWT payload for testing."""
    return {
        "sub": "test-agent",
        "jti": "test-token-jti-001",
        "permissions": [
            "git:read:log",
            "git:read:diff",
            "git:read:blame",
            "git:read:status",
            "jira:read:search",
            "jira:write:create",
            "compliance:read:policy",
            "compliance:read:gdpr",
            "docs:read:search",
        ],
    }


@pytest.fixture
def mock_auth_payload_readonly() -> dict[str, Any]:
    """Return a read-only mock JWT payload."""
    return {
        "sub": "readonly-agent",
        "jti": "test-token-jti-002",
        "permissions": [
            "git:read:log",
            "git:read:status",
            "docs:read:search",
        ],
    }


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """Ensure clean environment for each test."""
    for key in list(os.environ.keys()):
        if key.startswith("JOL_MCP_"):
            monkeypatch.delenv(key, raising=False)
