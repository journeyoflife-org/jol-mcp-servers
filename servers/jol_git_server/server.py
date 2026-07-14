"""jol-git-server — FastMCP entrypoint for read-only Git tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from servers.jol_git_server.tools.git_log import git_log
from servers.jol_git_server.tools.git_status import git_status

mcp = FastMCP("jol-git-server")

# Register tools
mcp.tool()(git_log)
mcp.tool()(git_status)


if __name__ == "__main__":
    mcp.run()
