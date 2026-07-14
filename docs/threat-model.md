# Threat Model — MCP Server Layer

**Methodology**: STRIDE
**Scope**: All MCP servers, shared libraries, and MCP protocol endpoints

## System Boundaries

```
┌──────────────────────────────────────────┐
│           Trust Boundary                  │
│                                          │
│  AI Agent ──(MCP)──► MCP Server          │
│                        │                 │
│                    ┌───┴───┐             │
│                    │Shared │             │
│                    │Layer  │             │
│                    └───┬───┘             │
│                        │                 │
│                    Backend System         │
└──────────────────────────────────────────┘
```

## STRIDE Analysis

### Spoofing
- **Threat**: Forged JWT tokens accepted by auth layer
- **Mitigation**: Asymmetric JWT verification with key rotation
- **Threat**: Impersonation of legitimate caller
- **Mitigation**: Caller identity resolution with audit logging

### Tampering
- **Threat**: Tool input modified to bypass sanitisation
- **Mitigation**: Allowlist-based input validation; reject unknown patterns
- **Threat**: Audit log tampering
- **Mitigation**: Append-only log storage; tamper-evident hashing

### Repudiation
- **Threat**: Caller denies making a tool invocation
- **Mitigation**: Every invocation logged with caller identity + timestamp
- **Threat**: Tool output disputed
- **Mitigation**: Output hash recorded in audit log

### Information Disclosure
- **Threat**: PII leaked through tool output
- **Mitigation**: Output sanitiser with PII redaction; size limits
- **Threat**: Error messages expose internals
- **Mitigation**: Generic error responses; detailed errors only in audit log

### Denial of Service
- **Threat**: Excessive tool calls exhaust resources
- **Mitigation**: Rate limiting per caller; output size caps
- **Threat**: Slow backend responses cascade
- **Mitigation**: Per-tool timeouts; circuit breaker pattern

### Elevation of Privilege
- **Threat**: Tool scope escalation (accessing unauthorised tools)
- **Mitigation**: Capability-scoped permission registry; per-tool authorisation
- **Threat**: Shell injection via tool parameters
- **Mitigation**: No shell passthrough; parameterised execution only
