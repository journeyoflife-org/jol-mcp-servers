"""Tests for authentication in git server."""

from __future__ import annotations

import pytest

from shared.auth.caller_identity import resolve_caller
from shared.errors.exceptions import AuthError


def test_resolve_caller_valid_token():
    """Valid token payload should resolve to a CallerIdentity."""
    payload = {
        "sub": "agent-test",
        "jti": "token-123",
        "permissions": ["git:read:log", "git:read:status"],
    }
    caller = resolve_caller(payload)
    assert caller.identity == "agent-test"
    assert caller.token_jti == "token-123"
    assert caller.has_permission("git:read:log")
    assert not caller.has_permission("jira:write:create")


def test_resolve_caller_missing_sub():
    """Token without 'sub' claim should raise AuthError."""
    with pytest.raises(AuthError, match="missing 'sub' claim"):
        resolve_caller({"jti": "token-123", "permissions": []})


def test_resolve_caller_empty_permissions():
    """Token with no permissions should resolve but have no access."""
    payload = {"sub": "agent-no-perms", "jti": "token-456", "permissions": []}
    caller = resolve_caller(payload)
    assert caller.identity == "agent-no-perms"
    assert not caller.has_permission("git:read:log")
