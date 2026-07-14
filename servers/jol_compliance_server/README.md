# jol-compliance-server

MCP server providing read-only access to compliance policies and GDPR checklists.

## Capabilities

| Tool | Description | Permission |
|------|-------------|-----------|
| `policy_lookup` | Query compliance repo documents | `compliance:read:policy` |
| `gdpr_checklist` | Return GDPR checklist for a feature | `compliance:read:gdpr` |

## Security

- **Read-only**: No write operations
- **No PII**: Policy documents contain no personal data
- **Audit logging**: Every invocation logged
