# Security Policy

## Supported Versions

Only the latest release on `main` receives security patches.

## Reporting a Vulnerability

1. **Do NOT open a public GitHub issue.**
2. Email `security@journeyoflife.io` with:
   - A clear description of the vulnerability
   - Steps to reproduce
   - Impact assessment (CIA triad)
   - Suggested remediation (if any)
3. PGP key available on request.

## Response SLA

| Priority | Acknowledgement | Triage | Fix |
|----------|----------------|--------|-----|
| P1 — Critical (RCE, auth bypass, data breach) | 4 hours | 24 hours | 72 hours |
| P2 — High (privilege escalation, PII exposure) | 24 hours | 3 days | 14 days |
| P3 — Medium (information disclosure, DoS) | 48 hours | 7 days | 30 days |
| P4 — Low (cosmetic, defence-in-depth) | 1 week | 14 days | Next release |

## GDPR Article 33 — Breach Notification

In the event of a personal data breach, Journey of Life will notify the
relevant supervisory authority within **72 hours** of becoming aware of the
breach, in accordance with GDPR Article 33.

See [Incident Response Runbook](docs/runbook-incident-response.md) for full
procedure.

## Scope

This policy covers all code in this repository, the MCP server endpoints, and
any associated infrastructure configurations.
