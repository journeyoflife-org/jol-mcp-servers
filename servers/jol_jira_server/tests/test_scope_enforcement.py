"""Tests for scope enforcement — permission checks."""

from __future__ import annotations

import pytest

from shared.auth.permissions import DEFAULT_REGISTRY
from shared.errors.exceptions import ScopeError


def test_default_registry_has_git_permissions():
    """Default registry should contain git server permissions."""
    assert DEFAULT_REGISTRY.is_valid("jol-git-server:read:log")
    assert DEFAULT_REGISTRY.is_valid("jol-git-server:read:status")


def test_default_registry_has_jira_permissions():
    """Default registry should contain jira server permissions."""
    assert DEFAULT_REGISTRY.is_valid("jol-jira-server:read:search")
    assert DEFAULT_REGISTRY.is_valid("jol-jira-server:write:create")


def test_unknown_permission_raises_scope_error():
    """Requesting an unregistered permission should raise ScopeError."""
    with pytest.raises(ScopeError, match="Unknown permission"):
        DEFAULT_REGISTRY.get("jol-git-server:write:delete")


def test_server_permissions_filter():
    """server_permissions should return only permissions for that server."""
    git_perms = DEFAULT_REGISTRY.server_permissions("jol-git-server")
    assert all(p.server == "jol-git-server" for p in git_perms)
    assert len(git_perms) == 4  # log, diff, blame, status
