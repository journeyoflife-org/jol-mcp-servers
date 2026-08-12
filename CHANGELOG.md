# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

This changelog serves as SOC 2 CC8.1 versioned change evidence.

## [Unreleased]

### Added
- Production deployment documentation for `mcp-prod-lt01` (Issue #29, 2026-08-12):
  server doc (`docs/servers/mcp-prod-lt01.md`), operator deployment runbook
  (`docs/runbooks/mcp-prod-lt01-deployment.md`), and fleet host variables
  (`inventory/prod/host_vars/mcp-prod-lt01.yml`)
- Deployment change evidence: all four stdio MCP servers verified operational on
  `mcp-prod-lt01` (10.40.40.11) with OCSF audit records; pre-change Proxmox
  snapshot `pre-mcp-fix-20260812-2213` retained for rollback
- Initial repository structure with shared security primitives
- `jol-git-server`: Read-only Git inspection tools (log, diff, blame, status)
- `jol-jira-server`: Jira issue search and create tools
- `jol-compliance-server`: Policy lookup and GDPR checklist tools
- `jol-docs-server`: Vector-based documentation search
- Shared auth module with JWT validation and short-lived tokens
- Shared input/output sanitisation layer
- Shared structured audit logging (OCSF format)
- CI/CD pipeline with security scanning
- Qodana static analysis configuration
