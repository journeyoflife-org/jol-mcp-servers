# jol-jira-server

MCP server providing Jira issue search and creation tools.

## Capabilities

| Tool | Description | Permission |
|------|-------------|-----------|
| `issue_search` | JQL search with field allowlist | `jira:read:search` |
| `issue_create` | Create new issues (no delete) | `jira:write:create` |

## Security

- **Read + Create only**: No update or delete operations
- **Field allowlist**: Only permitted fields returned in search results
- **PII redaction**: Output sanitised for personal data
- **Audit logging**: Every invocation logged in OCSF format
