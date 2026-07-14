"""jol-docs-server — FastMCP entrypoint for documentation tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from servers.jol_docs_server.tools.doc_search import doc_search

mcp = FastMCP("jol-docs-server")

mcp.tool()(doc_search)


if __name__ == "__main__":
    mcp.run()
