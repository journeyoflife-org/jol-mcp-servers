"""Custom exceptions for jol-mcp-servers."""


class AuthError(Exception):
    """Raised when authentication or authorisation fails."""


class SanitisationError(Exception):
    """Raised when input/output sanitisation fails."""


class ScopeError(Exception):
    """Raised when a tool access is outside the caller's authorised scope."""
