"""Capability-scoped permission registry."""

from __future__ import annotations

from dataclasses import dataclass

from shared.errors.exceptions import ScopeError


@dataclass(frozen=True)
# noinspection PyClassHasNoInitInspection
class Permission:
    """Represents a single permission."""

    server: str
    resource: str
    action: str

    @property
    def key(self) -> str:
        """Permission key in server:action:resource format."""
        return f"{self.server}:{self.action}:{self.resource}"


class PermissionRegistry:
    """Registry of all valid permissions across MCP servers."""

    def __init__(self) -> None:
        self._permissions: dict[str, Permission] = {}

    def register(self, permission: Permission) -> None:
        """Register a new permission."""
        self._permissions[permission.key] = permission

    def get(self, key: str) -> Permission:
        """Get a permission by key.

        Raises ScopeError if the permission is not registered.
        """
        perm = self._permissions.get(key)
        if perm is None:
            raise ScopeError(f"Unknown permission: {key}")
        return perm

    def is_valid(self, key: str) -> bool:
        """Check if a permission key is registered."""
        return key in self._permissions

    def all_permissions(self) -> list[Permission]:
        """Return all registered permissions."""
        return list(self._permissions.values())

    def server_permissions(self, server: str) -> list[Permission]:
        """Return all permissions for a specific server."""
        return [p for p in self._permissions.values() if p.server == server]


# Global registry initialised with default permissions
DEFAULT_REGISTRY = PermissionRegistry()
_DEFAULT_PERMISSIONS = [
    Permission("jol-git-server", "log", "read"),
    Permission("jol-git-server", "diff", "read"),
    Permission("jol-git-server", "blame", "read"),
    Permission("jol-git-server", "status", "read"),
    Permission("jol-jira-server", "search", "read"),
    Permission("jol-jira-server", "create", "write"),
    Permission("jol-compliance-server", "policy", "read"),
    Permission("jol-compliance-server", "gdpr", "read"),
    Permission("jol-docs-server", "search", "read"),
]
for _perm in _DEFAULT_PERMISSIONS:
    DEFAULT_REGISTRY.register(_perm)
