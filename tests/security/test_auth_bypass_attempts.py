"""Tests for auth bypass attempts — token forgery, replay, scope escalation."""

from __future__ import annotations

import pytest

from shared.auth.caller_identity import resolve_caller
from shared.auth.permissions import DEFAULT_REGISTRY
from shared.errors.exceptions import AuthError, ScopeError


class TestTokenForgery:
    """Test that forged/invalid tokens are rejected."""

    def test_empty_payload_rejected(self):
        """Empty payload should fail caller resolution."""
        with pytest.raises(AuthError):
            resolve_caller({})

    def test_none_sub_rejected(self):
        """Token with None 'sub' should fail."""
        with pytest.raises(AuthError):
            resolve_caller({"sub": None, "jti": "abc", "permissions": []})

    def test_empty_sub_rejected(self):
        """Token with empty 'sub' should fail."""
        with pytest.raises(AuthError):
            resolve_caller({"sub": "", "jti": "abc", "permissions": []})


class TestReplay:
    """Test token replay detection."""

    def test_revoked_token_rejected(self):
        """Revoked tokens should be rejected."""
        from shared.auth.token_validator import TokenValidator

        validator = TokenValidator(public_key="test-key")
        validator.revoke("token-jti-replay")
        assert validator.is_revoked("token-jti-replay")


class TestScopeEscalation:
    """Test that scope escalation is prevented."""

    def test_readonly_caller_cannot_write(self, mock_auth_payload_readonly):
        """Read-only caller should not have write permissions."""
        caller = resolve_caller(mock_auth_payload_readonly)
        assert not caller.has_permission("jira:write:create")
        assert not caller.has_permission("git:write:delete")

    def test_unknown_permission_raises(self):
        """Requesting unregistered permissions should raise ScopeError."""
        with pytest.raises(ScopeError):
            DEFAULT_REGISTRY.get("jol-git-server:admin:all")

    def test_cross_server_permission_denied(self):
        """Permission for different server should not grant access."""
        payload = {
            "sub": "git-only-agent",
            "jti": "token-git",
            "permissions": ["git:read:log"],
        }
        caller = resolve_caller(payload)
        assert not caller.has_permission("jira:read:search")
        assert not caller.has_permission("compliance:read:policy")
