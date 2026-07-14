# Architecture

## C4 Context Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      AI Agent (Caller)                       │
└────────────────────────────┬────────────────────────────────┘
                             │ MCP Protocol (JSON-RPC over stdio/SSE)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    jol-mcp-servers                           │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌───────────┐  │
│  │  Git      │  │  Jira    │  │ Compliance│  │  Docs     │  │
│  │  Server   │  │  Server  │  │  Server   │  │  Server   │  │
│  └────┬─────┘  └────┬─────┘  └─────┬─────┘  └─────┬─────┘  │
│       │             │               │               │        │
│  ┌────┴─────────────┴───────────────┴───────────────┴─────┐  │
│  │                   Shared Security Layer                  │  │
│  │  Auth │ Input Sanitisation │ Audit Logging │ Config     │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │              │                │
         ▼              ▼                ▼
   ┌──────────┐  ┌──────────┐   ┌──────────────┐
   │  Git     │  │  Jira    │   │  Compliance  │
   │  Repos   │  │  Cloud   │   │  Repo (docs) │
   └──────────┘  └──────────┘   └──────────────┘
```

## Architecture Decision Records

| ADR | Title | Status |
|-----|-------|--------|
| [ADR-001](adr/ADR-001-sandboxed-execution.md) | Sandboxed Execution | Accepted |
| [ADR-002](adr/ADR-002-auth-model.md) | Authentication Model | Accepted |
| [ADR-003](adr/ADR-003-input-sanitisation.md) | Input Sanitisation | Accepted |
| [ADR-004](adr/ADR-004-audit-logging.md) | Audit Logging | Accepted |

## Key Design Principles

1. **Zero Trust**: Every tool call is authenticated and authorised
2. **Least Privilege**: Each server has the minimum permissions required
3. **Defence in Depth**: Multiple security layers (auth, sanitisation, audit)
4. **Immutability**: No server can modify the systems it reads from (except Jira create)
5. **Observability**: Every invocation is logged with structured OCSF events
