"""Caller identity resolution from JWT token."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from shared.errors.exceptions import AuthError


@dataclass(frozen=True)
# noinspection PyClassHasNoInitInspection
class CallerIdentity:
    """Represents a resolved caller identity."""

    identity: str
    token_jti: str
    permissions: tuple[str, ...]

    def has_permission(self, permission: str) -> bool:
        """Check if the caller has a specific permission."""
        return permission in self.permissions


def resolve_caller(payload: dict[str, Any]) -> CallerIdentity:
    """Resolve a CallerIdentity from decoded JWT claims.

    Expected claims:
        - sub: caller identity string
        - jti: unique token identifier
        - permissions: list of permission strings

    Raises AuthError if required claims are missing.
    """
    identity = payload.get("sub")
    if not identity:
        raise AuthError("Token missing 'sub' claim")

    jti = payload.get("jti", "")
    permissions = tuple(payload.get("permissions", []))

    return CallerIdentity(
        identity=identity,
        token_jti=jti,
        permissions=permissions,
    )
