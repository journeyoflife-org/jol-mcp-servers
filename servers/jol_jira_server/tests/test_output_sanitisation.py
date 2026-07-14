"""Tests for output sanitisation — PII leak prevention."""

from __future__ import annotations

import pytest

from shared.errors.exceptions import SanitisationError
from shared.sanitisation.output_sanitiser import OutputSanitiser


@pytest.fixture
def sanitiser():
    return OutputSanitiser()


def test_email_redaction(sanitiser):
    """Email addresses should be redacted from output."""
    text = "Assigned to john.doe@example.com for review"
    result = sanitiser.redact_pii(text)
    assert "john.doe@example.com" not in result
    assert "[REDACTED_EMAIL]" in result


def test_phone_redaction(sanitiser):
    """Phone numbers should be redacted from output."""
    text = "Contact: 555-123-4567 for support"
    result = sanitiser.redact_pii(text)
    assert "555-123-4567" not in result
    assert "[REDACTED_PHONE]" in result


def test_ssn_redaction(sanitiser):
    """SSNs should be redacted from output."""
    text = "Employee SSN: 123-45-6789"
    result = sanitiser.redact_pii(text)
    assert "123-45-6789" not in result
    assert "[REDACTED_SSN]" in result


def test_contains_pii_detection(sanitiser):
    """contains_pii should detect PII in text."""
    assert sanitiser.contains_pii("email: user@test.com") is True
    assert sanitiser.contains_pii("no pii here") is False


def test_output_size_limit():
    """Output exceeding size limit should raise error."""
    small_sanitiser = OutputSanitiser(max_size=10)
    with pytest.raises(SanitisationError, match="exceeds maximum size"):
        small_sanitiser.sanitise("A" * 100)
