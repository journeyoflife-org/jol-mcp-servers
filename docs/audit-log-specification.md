# Audit Log Specification

**Standard**: Based on OCSF (Open Cybersecurity Schema Framework)
**Format**: JSON Lines (one event per line)
**Retention**: 7 years (ISO 27001 A.12.4, SOC 2 CC7.3)

## Event Schema

Every tool invocation produces an audit event:

```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "event_class": "Tool Invocation",
  "severity": "Informational",
  "caller": {
    "identity": "agent-xyz",
    "token_jti": "abc123...",
    "permissions": ["git:read:log"]
  },
  "tool": {
    "server": "jol-git-server",
    "name": "git_log",
    "parameters": {
      "repo": "jol-platform",
      "max_count": 10
    }
  },
  "outcome": {
    "status": "Success",
    "output_size_bytes": 4521,
    "duration_ms": 142
  },
  "security": {
    "input_sanitised": true,
    "output_sanitised": true,
    "pii_detected_in_output": false
  }
}
```

## Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `timestamp` | ISO 8601 | Yes | UTC timestamp of invocation |
| `event_class` | string | Yes | Always "Tool Invocation" |
| `severity` | enum | Yes | Informational / Warning / Error |
| `caller.identity` | string | Yes | Resolved caller identity |
| `caller.token_jti` | string | Yes | JWT token ID for traceability |
| `caller.permissions` | string[] | Yes | Permissions used in this call |
| `tool.server` | string | Yes | MCP server name |
| `tool.name` | string | Yes | Tool function name |
| `tool.parameters` | object | Yes | Sanitised parameters (secrets redacted) |
| `outcome.status` | enum | Yes | Success / Failure / Timeout |
| `outcome.output_size_bytes` | int | Yes | Size of tool output |
| `outcome.duration_ms` | int | Yes | Execution time |
| `security.input_sanitised` | bool | Yes | Whether input passed sanitisation |
| `security.output_sanitised` | bool | Yes | Whether output was sanitised |
| `security.pii_detected_in_output` | bool | Yes | PII detected before redaction |
