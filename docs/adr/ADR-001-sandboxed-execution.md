# ADR-001: Sandboxed Execution

## Status
Accepted

## Context

MCP servers execute code that interacts with external systems (Git repos, Jira,
documentation stores). A compromised or malicious tool could attempt to escalate
privileges, access host resources, or pivot to other systems.

## Decision

All MCP servers run as non-root containers with a dedicated restricted user:

- **User**: `jol-mcp` (UID 10001)
- **No root access**: Containers run with `USER jol-mcp`
- **Read-only filesystem**: Where possible, mount filesystem as read-only
- **Resource limits**: CPU and memory constraints per container
- **Network isolation**: Each server only connects to its designated backend

## Consequences

- Limits blast radius of any single compromised server
- Prevents host-level privilege escalation
- Simplifies security audit (known user, known permissions)
- Adds operational overhead (user management in Dockerfiles)
