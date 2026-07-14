"""Input sanitisation with allowlist validation and shell metacharacter stripping."""

from __future__ import annotations

import re
from typing import Pattern  # noqa: UP035 — required by Qodana type checker

from shared.errors.exceptions import SanitisationError

# Shell metacharacters that must never appear in tool inputs
_SHELL_META = re.compile(r"[;&|`$(){}<>!#\\]")

# Default allowlist: alphanumeric, hyphens, underscores, dots, slashes, colons, @
_DEFAULT_ALLOWLIST = re.compile(r"^[a-zA-Z0-9_\-./:@ ]+$")

# Repo path: alphanumeric, hyphens, underscores, forward slashes
# (no dots — path traversal prevention)
_REPO_PATH_PATTERN = re.compile(r"^[a-zA-Z0-9_\-/]+$")

# JQL: allows parentheses, equals, quotes, etc.
_JQL_PATTERN = re.compile(r'^[a-zA-Z0-9_\-./: =()<>"\'!~,\s*|&]+$')


class InputSanitiser:
    """Validates and sanitises tool input parameters."""

    def __init__(self, allowlist_pattern: Pattern[str] | None = None) -> None:
        self._allowlist = allowlist_pattern or _DEFAULT_ALLOWLIST

    def validate(self, value: str, field_name: str = "input") -> str:
        """Validate input against allowlist and strip shell metacharacters.

        Returns the sanitised value.
        Raises SanitisationError if validation fails.
        """
        if not isinstance(value, str):
            raise SanitisationError(f"{field_name}: expected string, got {type(value).__name__}")

        # Strip shell metacharacters
        cleaned = _SHELL_META.sub("", value)

        # Validate against allowlist
        if not self._allowlist.match(cleaned):
            raise SanitisationError(f"{field_name}: input contains disallowed characters")

        return cleaned

    @staticmethod
    def validate_repo_path(value: str) -> str:
        """Validate a repository path (stricter allowlist)."""
        if not _REPO_PATH_PATTERN.match(value):
            raise SanitisationError(f"Invalid repository path: {value}")
        if ".." in value:
            raise SanitisationError(f"Path traversal detected: {value}")
        return value

    @staticmethod
    def validate_jql(value: str) -> str:
        """Validate a JQL query (allows JQL-specific characters)."""
        if not _JQL_PATTERN.match(value):
            raise SanitisationError("Invalid JQL query: contains disallowed characters")
        return value
