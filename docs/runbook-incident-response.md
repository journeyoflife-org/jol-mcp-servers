# Incident Response Runbook

**Scope**: All MCP servers and associated infrastructure
**Regulatory**: GDPR Article 33 — 72-hour breach notification

## Priority Definitions

| Priority | Description | Response Time |
|----------|------------|--------------|
| P1 | Active breach, data exfiltration, auth bypass | ACK 4h, triage 24h, fix 72h |
| P2 | Privilege escalation, PII exposure risk | ACK 24h, triage 3d, fix 14d |
| P3 | Information disclosure, service degradation | ACK 48h, triage 7d, fix 30d |
| P4 | Cosmetic, defence-in-depth gap | ACK 1w, triage 14d, next release |

## P1 Incident Procedure

### Phase 1: Detection & Acknowledgement (0–4 hours)

1. **Detect**: Alert from monitoring, audit log anomaly, or external report
2. **Acknowledge**: Incident Commander acknowledges within 4 hours
3. **Classify**: Confirm P1 severity; if uncertain, treat as P1 until confirmed
4. **Assemble**: Notify incident response team via PagerDuty

### Phase 2: Containment (4–24 hours)

1. **Isolate**: Disable affected MCP server(s) immediately
2. **Preserve**: Snapshot audit logs, container state, and network traffic
3. **Assess**: Determine scope of compromise (what data was accessed?)
4. **Communicate**: Internal status page update

### Phase 3: Eradication & Recovery (24–72 hours)

1. **Root Cause**: Identify and fix the vulnerability
2. **Rotate**: All tokens, keys, and credentials in scope
3. **Restore**: Redeploy from known-good image
4. **Verify**: Confirm fix with security scan + manual verification

### Phase 4: GDPR Article 33 Notification (within 72 hours)

1. **Notify Supervisory Authority**: Submit breach notification within 72 hours
2. **Document**: Record all actions taken, timeline, and impact assessment
3. **Notify Data Subjects**: If high risk to rights and freedoms (Art. 34)

### Phase 5: Post-Incident (within 2 weeks)

1. **Post-Mortem**: Blameless retrospective within 5 business days
2. **Update**: Threat model, runbook, and security controls as needed
3. **Evidence**: Archive all incident evidence for SOC 2 audit trail
