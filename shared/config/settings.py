"""Application settings loaded from environment variables only."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration for all MCP servers, loaded from environment variables.

    No config files — env-var only for containerised deployment.
    """

    # Server identity
    server_name: str = "jol-mcp-server"
    log_level: str = "INFO"

    # Auth
    jwt_public_key: str = ""
    jwt_algorithm: str = "RS256"
    token_max_ttl_seconds: int = 300  # 5 minutes

    # Sanitisation
    max_output_size_bytes: int = 100 * 1024  # 100KB

    # Audit
    audit_log_path: str = "/var/log/jol-mcp/audit.jsonl"

    # Rate limiting
    max_requests_per_minute: int = 60

    # Tool timeouts
    tool_timeout_seconds: int = 30

    model_config = {"env_prefix": "JOL_MCP_", "env_file": None}
