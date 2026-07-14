"""JWT token validation with short TTL and revocation check."""

from __future__ import annotations

from typing import Any

import jwt

from shared.errors.exceptions import AuthError


class TokenValidator:
    """Validates JWT tokens with expiration and revocation checks."""

    def __init__(self, public_key: str, algorithm: str = "RS256") -> None:
        self._public_key = public_key
        self._algorithm = algorithm
        self._revoked_jtis: set[str] = set()

    def validate(self, token: str) -> dict[str, Any]:
        """Validate a JWT token and return decoded claims.

        Raises AuthError if the token is invalid, expired, or revoked.
        """
        try:
            payload = jwt.decode(
                token,
                self._public_key,
                algorithms=[self._algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise AuthError("Token has expired") from None
        except jwt.InvalidTokenError as exc:
            raise AuthError(f"Invalid token: {exc}") from exc

        # Revocation check
        jti = payload.get("jti")
        if jti and jti in self._revoked_jtis:
            raise AuthError("Token has been revoked")

        return payload

    def revoke(self, jti: str) -> None:
        """Add a token JTI to the revocation list."""
        self._revoked_jtis.add(jti)

    def is_revoked(self, jti: str) -> bool:
        """Check if a token JTI has been revoked."""
        return jti in self._revoked_jtis
