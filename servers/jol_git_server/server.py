"""jol-git-server — FastMCP entrypoint for read-only Git tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from servers.jol_git_server.tools.git_log import git_log
from servers.jol_git_server.tools.git_status import git_status
from shared.audit.integration import create_audit_logger, register_audited_tools

mcp = FastMCP("jol-git-server")

# Register tools — every invocation audited (ADR-004)
_audit = create_audit_logger("jol-git-server")
register_audited_tools(mcp, _audit, [git_log, git_status])


if __name__ == "__main__":
    mcp.run()
