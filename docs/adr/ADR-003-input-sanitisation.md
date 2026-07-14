# ADR-003: Input Sanitisation

## Status
Accepted

## Context

MCP tool parameters originate from AI agent outputs, which may be influenced by
prompt injection or adversarial inputs. Parameters must be validated before use.

## Decision

- **Allowlist validation**: Each tool parameter has a defined allowlist of valid patterns
- **Regex enforcement**: Inputs matched against strict regex patterns
- **Shell metacharacter stripping**: All shell metacharacters removed from inputs
- **No shell passthrough**: Tool implementations use parameterised execution only
- **Reject unknown**: Any input not matching the allowlist is rejected with an error

## Consequences

- Prevents shell injection attacks (no `;`, `|`, `$()`, etc.)
- Limits tool parameters to known-safe values
- May require updating allowlists when legitimate inputs are rejected
- Zero shell passthrough eliminates entire class of injection vulnerabilities
