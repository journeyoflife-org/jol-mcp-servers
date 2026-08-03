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

## Change Control & Break-Glass Procedure

**Policy (SOC 2 CC6.1, CC8.1 · ISO 27001 A.8.15)** — All changes to `main`
must be made through a pull request with passing status checks. Direct
pushes to `main` are prohibited for day-to-day work, and branch-protection
bypass allowances are removed for routine development. This preserves
segregation of duties: the author of a change is not the sole approver, and
every merge carries review and CI evidence.

**Break-glass (emergency bypass)** is permitted only during a declared
**P1 incident** (see [Incident Response Runbook](docs/runbook-incident-response.md),
Phases 2–3) when the standard PR path would materially delay containment or
recovery — for example, an urgent revert or hotfix while CI is unavailable.

Break-glass steps:

1. **Declare**: record the incident ID and the justification for bypass in
   the incident log before bypassing.
2. **Scope**: grant the minimum temporary permission needed (e.g., enable
   admin enforcement bypass or a time-boxed ruleset bypass), never a
   standing exemption.
3. **Act**: push GPG-signed commits only; every bypassed push is visible in
   the GitHub audit log and must reference the incident ID in the commit
   message.
4. **Revoke**: remove the bypass allowance within **24 hours** and no later
   than incident closure.
5. **Review**: during Phase 5 (Post-Incident), review all bypassed changes,
   confirm the protection rule is reinstated, and record the outcome in the
   post-incident report.

Break-glass usage is an auditable exception: zero uses is the expected
baseline, and any invocation without a declared P1 incident is itself a
security finding.

## Scope

This policy covers all code in this repository, the MCP server endpoints, and
any associated infrastructure configurations.
