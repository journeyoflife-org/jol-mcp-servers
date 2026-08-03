"""jol-docs-server — FastMCP entrypoint for documentation tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from servers.jol_docs_server.tools.doc_search import doc_search
from shared.audit.integration import create_audit_logger, register_audited_tools

mcp = FastMCP("jol-docs-server")

# Register tools — every invocation audited (ADR-004)
_audit = create_audit_logger("jol-docs-server")
register_audited_tools(mcp, _audit, [doc_search])


if __name__ == "__main__":
    mcp.run()
