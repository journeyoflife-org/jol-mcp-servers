# jol-mcp-servers

Model Context Protocol (MCP) server suite for Journey of Life platform.

## Security & Capability Reference

All servers operate under a zero-trust security model with:

- **Authentication**: JWT-based with short-lived tokens per tool call ([ADR-002](docs/adr/ADR-002-auth-model.md))
- **Input Sanitisation**: Allowlist + regex validation; no shell passthrough ([ADR-003](docs/adr/ADR-003-input-sanitisation.md))
- **Audit Logging**: Every invocation logged in OCSF format with 7-year retention ([ADR-004](docs/adr/ADR-004-audit-logging.md))
- **Sandboxed Execution**: Non-root containers with restricted user per server ([ADR-001](docs/adr/ADR-001-sandboxed-execution.md))

## Servers

| Server | Purpose | Access Level |
|--------|---------|-------------|
| `jol-git-server` | Git repository inspection | Read-only (log, diff, blame, status) |
| `jol-jira-server` | Jira issue management | Read + Create only |
| `jol-compliance-server` | Policy & GDPR compliance lookup | Read-only |
| `jol-docs-server` | Documentation search | Read-only (vector search) |

## Quick Start

```bash
# Set up development environment
./scripts/setup-dev.sh

# Run a server locally
./scripts/run-server-local.sh jol-git-server
```

## Development

```bash
make lint       # Run linters across all servers
make test       # Run test suite
make scan       # Run security scans
```

## Documentation

- [Architecture](docs/architecture.md)
- [Threat Model](docs/threat-model.md)
- [Capability Manifest](docs/capability-manifest.md)
- [DPIA](docs/DPIA-mcp-servers.md)
- [Audit Log Specification](docs/audit-log-specification.md)
- [Incident Response Runbook](docs/runbook-incident-response.md)
- [Production Server: mcp-prod-lt01](docs/servers/mcp-prod-lt01.md)
- [Deployment Runbook: mcp-prod-lt01](docs/runbooks/mcp-prod-lt01-deployment.md)

## Security

See [SECURITY.md](SECURITY.md) for vulnerability disclosure policy.

## License

Proprietary — All Rights Reserved. See [LICENSE](LICENSE).
