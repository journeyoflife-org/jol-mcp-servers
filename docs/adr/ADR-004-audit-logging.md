# ADR-004: Audit Logging

## Status
Accepted

## Context

SOC 2, ISO 27001, and GDPR require comprehensive audit trails of all data access.
MCP servers provide AI agents with access to organisational data, making logging
essential for compliance and incident response.

## Decision

- **Every invocation logged**: No exceptions; every tool call produces an audit event
- **Structured format**: OCSF-based JSON schema (see [audit-log-specification.md](../audit-log-specification.md))
- **ISO 8601 timestamps**: All timestamps in UTC
- **7-year retention**: Meets ISO 27001 A.12.4 and SOC 2 CC7.3 requirements
- **Tamper-evident**: Append-only storage with hash chaining
- **Caller attribution**: Every event includes caller identity, permissions, and tool details

## Consequences

- Complete audit trail for compliance evidence
- Enables incident investigation and forensics
- Storage cost for 7-year retention (mitigated by structured format for compression)
- Performance overhead per invocation (minimal; async logging)
