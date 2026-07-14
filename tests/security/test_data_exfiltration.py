"""Tests for data exfiltration prevention — output size limits and PII detection."""

from __future__ import annotations

import pytest

from shared.errors.exceptions import SanitisationError
from shared.sanitisation.output_sanitiser import OutputSanitiser


class TestOutputSizeLimits:
    """Verify output size limits prevent data exfiltration."""

    def test_default_limit(self):
        """Default limit is 100KB."""
        sanitiser = OutputSanitiser()
        # 100KB of text should pass
        small_output = "A" * (100 * 1024 - 100)
        result = sanitiser.sanitise(small_output)
        assert len(result) > 0

    def test_exceeds_limit_rejected(self):
        """Output exceeding limit should raise SanitisationError."""
        sanitiser = OutputSanitiser(max_size=100)
        with pytest.raises(SanitisationError, match="exceeds maximum size"):
            sanitiser.sanitise("X" * 200)

    def test_custom_limit(self):
        """Custom size limit should be enforced."""
        sanitiser = OutputSanitiser(max_size=50)
        with pytest.raises(SanitisationError):
            sanitiser.sanitise("B" * 100)


class TestPIIDetection:
    """Verify PII is detected and redacted in output."""

    @pytest.fixture
    def sanitiser(self):
        return OutputSanitiser()

    def test_email_detected(self, sanitiser):
        """Email addresses should be detected as PII."""
        assert sanitiser.contains_pii("user@example.com")
        assert sanitiser.contains_pii("admin@company.org")

    def test_phone_detected(self, sanitiser):
        """Phone numbers should be detected as PII."""
        assert sanitiser.contains_pii("Call 555-123-4567")
        assert sanitiser.contains_pii("Phone: 123.456.7890")

    def test_ssn_detected(self, sanitiser):
        """SSNs should be detected as PII."""
        assert sanitiser.contains_pii("SSN: 123-45-6789")

    def test_no_pii_clean(self, sanitiser):
        """Clean text should not trigger PII detection."""
        assert not sanitiser.contains_pii("Hello, this is a test message.")
        assert not sanitiser.contains_pii("Repository: jol-platform, branch: main")

    def test_pii_redacted_in_output(self, sanitiser):
        """PII should be redacted in sanitised output."""
        text = "Contact john@test.com or call 555-999-8888. SSN: 999-88-7777"
        result = sanitiser.sanitise(text)
        assert "john@test.com" not in result
        assert "555-999-8888" not in result
        assert "999-88-7777" not in result
        assert "[REDACTED_EMAIL]" in result
        assert "[REDACTED_PHONE]" in result
        assert "[REDACTED_SSN]" in result
