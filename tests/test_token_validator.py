"""Tests for TokenValidator."""

from __future__ import annotations

import time

import jwt
import pytest

from shared.auth.token_validator import TokenValidator
from shared.errors.exceptions import AuthError

# Use HS256 with a shared secret for testing (no RSA key needed)
_TEST_SECRET = "test-secret-key-for-unit-tests"


def _make_token(sub: str = "user-1", jti: str | None = None, exp_delta: int = 300) -> str:
    payload: dict = {"sub": sub}
    if jti:
        payload["jti"] = jti
    payload["exp"] = int(time.time()) + exp_delta
    return jwt.encode(payload, _TEST_SECRET, algorithm="HS256")


@pytest.fixture
def validator() -> TokenValidator:
    return TokenValidator(public_key=_TEST_SECRET, algorithm="HS256")


def test_validate_valid_token(validator):
    token = _make_token()
    claims = validator.validate(token)
    assert claims["sub"] == "user-1"


def test_validate_expired_token(validator):
    token = _make_token(exp_delta=-100)
    with pytest.raises(AuthError, match="expired"):
        validator.validate(token)


def test_validate_invalid_token(validator):
    with pytest.raises(AuthError, match="Invalid token"):
        validator.validate("not.a.valid.jwt")


def test_revoke_and_check(validator):
    token = _make_token(jti="revoke-me")
    validator.revoke("revoke-me")
    with pytest.raises(AuthError, match="revoked"):
        validator.validate(token)


def test_is_revoked(validator):
    assert not validator.is_revoked("jti-1")
    validator.revoke("jti-1")
    assert validator.is_revoked("jti-1")


def test_non_revoked_token_still_works(validator):
    token = _make_token(jti="keep-me")
    validator.revoke("other-jti")
    claims = validator.validate(token)
    assert claims["jti"] == "keep-me"
