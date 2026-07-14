# ADR-002: Authentication Model

## Status
Accepted

## Context

AI agents call MCP tools on behalf of users. We need to authenticate the caller,
enforce permissions, and prevent token reuse or replay attacks.

## Decision

- **JWT tokens** with asymmetric signing (RS256)
- **Short-lived tokens**: Maximum TTL of 5 minutes per token
- **Per-tool-call tokens**: Each tool invocation receives a fresh token
- **Revocation check**: Token JTI checked against revocation list before execution
- **Caller identity**: Resolved from token claims; logged in audit trail

## Consequences

- Minimises token replay window (5-minute TTL)
- Clear caller attribution in audit logs
- Requires token minting service or inline token generation
- Adds latency for token validation on each call
