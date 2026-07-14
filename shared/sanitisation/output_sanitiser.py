"""Output sanitisation with PII redaction and size limiting."""

from __future__ import annotations

import re

from shared.errors.exceptions import SanitisationError

# PII patterns for redaction
_EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
_PHONE_PATTERN = re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b")
_SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

# Default maximum output size (100KB)
_DEFAULT_MAX_SIZE = 100 * 1024


class OutputSanitiser:
    """Sanitises tool output by redacting PII and enforcing size limits."""

    def __init__(self, max_size: int = _DEFAULT_MAX_SIZE) -> None:
        self._max_size = max_size

    def sanitise(self, output: str) -> str:
        """Sanitise output: redact PII and enforce size limit.

        Returns the sanitised output string.
        Raises SanitisationError if output exceeds size limit after redaction.
        """
        # Redact PII
        redacted = self.redact_pii(output)

        # Enforce size limit
        if len(redacted.encode("utf-8")) > self._max_size:
            raise SanitisationError(f"Output exceeds maximum size of {self._max_size} bytes")

        return redacted

    @staticmethod
    def redact_pii(text: str) -> str:
        """Redact personally identifiable information from text."""
        text = _EMAIL_PATTERN.sub("[REDACTED_EMAIL]", text)
        text = _PHONE_PATTERN.sub("[REDACTED_PHONE]", text)
        text = _SSN_PATTERN.sub("[REDACTED_SSN]", text)
        return text

    @staticmethod
    def contains_pii(text: str) -> bool:
        """Check if text contains PII patterns."""
        return bool(
            _EMAIL_PATTERN.search(text) or _PHONE_PATTERN.search(text) or _SSN_PATTERN.search(text)
        )
