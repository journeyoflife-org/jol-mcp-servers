# mcp-prod-lt01 — MCP Production Server

Change record: GitHub Issue #29 (2026-08-12). Proxmox rollback snapshot:
`pre-mcp-fix-20260812-2213`.

## Overview

Dedicated production host for the `jol-mcp-servers` suite. All four MCP servers
run as stdio-transport FastMCP processes under systemd — there are no HTTP/SSE
listeners anywhere on this host (port 3000 disabled by design).

- **Host**: `mcp-prod-lt01` (Proxmox guest)
- **OS**: Ubuntu 24.04 LTS
- **Management IP**: `10.40.40.11` (VLAN 40)

## Services

| Unit | Server | Tools | Notes |
|------|--------|-------|-------|
| `jol-git-server.service` | jol-git-server | `git_log`, `git_status` | Read-only Git inspection |
| `jol-jira-server.service` | jol-jira-server | `issue_search`, `issue_create` | Returns `Failure` until credentials provisioned |
| `jol-compliance-server.service` | jol-compliance-server | `policy_lookup`, `gdpr_checklist` | Read-only |
| `jol-docs-server.service` | jol-docs-server | `doc_search` | Returns `Failure` until credentials provisioned |
| `node_exporter.service` | node_exporter v1.8.2 | — | Metrics on `10.40.40.11:9100` (interface bind only) |

Every tool invocation emits one OCSF-compliant JSONL audit record via
`register_audited_tools()` (ADR-004). Parameters matching secret patterns
(`token|secret|password|credential|auth|key`) are redacted automatically.

## Filesystem layout

| Path | Purpose | Owner / Mode |
|------|---------|--------------|
| `/opt/jol-mcp-servers` | Runtime checkout (`.venv` included) | `mcp-svc` |
| `/opt/jol/git/jol-mcp-servers.git` | Bare repo + post-receive deploy hook | `jol-admin` |
| `/etc/jol-mcp/mcp.env` | Environment file for all units | `root` / `0600` |
| `/var/log/jol-mcp/audit.jsonl` | OCSF audit log (logrotate, 14-day compressed retention) | `mcp-svc` |

## Environment

All settings use the `JOL_MCP_` prefix and are loaded from `/etc/jol-mcp/mcp.env`
(see `shared/config/settings.py`). Never store values here or in code — this table
lists names only.

| Variable | Purpose |
|----------|---------|
| `JOL_MCP_SERVER_NAME` | Server identity for audit records |
| `JOL_MCP_LOG_LEVEL` | Application log level |
| `JOL_MCP_JWT_PUBLIC_KEY` | JWT verification key (ADR-002) |
| `JOL_MCP_JWT_ALGORITHM` | JWT algorithm (default `RS256`) |
| `JOL_MCP_TOKEN_MAX_TTL_SECONDS` | Max token lifetime (default 300) |
| `JOL_MCP_MAX_OUTPUT_SIZE_BYTES` | Output sanitisation cap |
| `JOL_MCP_AUDIT_LOG_PATH` | Audit JSONL destination |
| `JOL_MCP_MAX_REQUESTS_PER_MINUTE` | Rate limit |
| `JOL_MCP_TOOL_TIMEOUT_SECONDS` | Per-tool timeout |
| `JIRA_API_TOKEN` | **Not configured** — no Vaultwarden secret available yet |
| `BITRIX_API_TOKEN` | **Not configured** — no Vaultwarden secret available yet |

## Security hardening

- **systemd**: `mcp-svc` nologin user, `Type=simple` with stdin keep-alive,
  `NoNewPrivileges`, `ProtectSystem=strict`, `ProtectHome`, `ReadWritePaths=/var/log/jol-mcp`,
  `PrivateTmp`, `PrivateDevices`, `ProtectKernelTunables/Modules/Logs`,
  `ProtectControlGroups`, `RestrictSUIDSGID`, `LockPersonality`,
  `SystemCallArchitectures=native`, `UMask=0027`
- **UFW**: default-deny inbound; allow 22 from management VLAN, 9100 from
  `10.40.40.0/24` only (source-filtered scrape)
- **Integrity**: AIDE baseline rebuilt post-change (nightly check clean, rc=0);
  auditd rules immutable (`-e 2`); auditd watch on `/etc/jol-mcp/mcp.env`
- **Compliance mapping**: SOC 2 CC6.1 / CC6.6 / CC6.7 / CC7.2, ISO 27001 A.8.9,
  GDPR Art. 5(1)(f)

## Known out-of-scope items

| Item | Status | Reason |
|------|--------|--------|
| Jira API credentials | Not configured | No Vaultwarden secret available |
| Bitrix API credentials | Not configured | No Vaultwarden secret available |
| SSE/HTTP transport (port 3000) | Not enabled | stdio-only architecture by design |
| Promtail → Loki shipping | Not enabled | Loki endpoint not provisioned |

## Related

- Deployment runbook: [`../runbooks/mcp-prod-lt01-deployment.md`](../runbooks/mcp-prod-lt01-deployment.md)
- Inventory: `inventory/prod/host_vars/mcp-prod-lt01.yml`
- Audit log specification: [`../audit-log-specification.md`](../audit-log-specification.md)
