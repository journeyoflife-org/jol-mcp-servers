"""jol-jira-server — FastMCP entrypoint for Jira tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from servers.jol_jira_server.tools.issue_create import issue_create
from servers.jol_jira_server.tools.issue_search import issue_search
from shared.audit.integration import create_audit_logger, register_audited_tools

mcp = FastMCP("jol-jira-server")

# Register tools — every invocation audited (ADR-004)
_audit = create_audit_logger("jol-jira-server")
register_audited_tools(mcp, _audit, [issue_search, issue_create])


if __name__ == "__main__":
    mcp.run()
