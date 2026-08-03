"""jol-compliance-server — FastMCP entrypoint for compliance tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from servers.jol_compliance_server.tools.gdpr_checklist import gdpr_checklist
from servers.jol_compliance_server.tools.policy_lookup import policy_lookup
from shared.audit.integration import create_audit_logger, register_audited_tools

mcp = FastMCP("jol-compliance-server")

# Register tools — every invocation audited (ADR-004)
_audit = create_audit_logger("jol-compliance-server")
register_audited_tools(mcp, _audit, [policy_lookup, gdpr_checklist])


if __name__ == "__main__":
    mcp.run()
