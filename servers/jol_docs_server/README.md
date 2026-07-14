# jol-docs-server

MCP server providing read-only documentation search via vector embeddings.

## Capabilities

| Tool | Description | Permission |
|------|-------------|-----------|
| `doc_search` | Vector search over /docs | `docs:read:search` |

## Security

- **Read-only**: No write operations
- **No shell access**: Vector search only
- **Audit logging**: Every invocation logged
