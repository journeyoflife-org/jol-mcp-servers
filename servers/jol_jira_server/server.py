"""jol-jira-server — FastMCP entrypoint for Jira tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from servers.jol_jira_server.tools.issue_create import issue_create
from servers.jol_jira_server.tools.issue_search import issue_search

mcp = FastMCP("jol-jira-server")

mcp.tool()(issue_search)
mcp.tool()(issue_create)


if __name__ == "__main__":
    mcp.run()
