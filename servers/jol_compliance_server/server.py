"""jol-compliance-server — FastMCP entrypoint for compliance tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from servers.jol_compliance_server.tools.gdpr_checklist import gdpr_checklist
from servers.jol_compliance_server.tools.policy_lookup import policy_lookup

mcp = FastMCP("jol-compliance-server")

mcp.tool()(policy_lookup)
mcp.tool()(gdpr_checklist)


if __name__ == "__main__":
    mcp.run()
