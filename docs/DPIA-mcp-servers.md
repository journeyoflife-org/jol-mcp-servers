# Data Protection Impact Assessment (DPIA) — MCP Servers

**Document Owner**: Platform Core Team
**Last Updated**: 2024-01-15
**Classification**: Internal

## Article 35 Screening

### Processing Description

The MCP server suite enables AI agents to access organisational data through
controlled tool interfaces. The following data categories are processed:

| Server | Data Category | PII? | Sensitivity |
|--------|-------------|------|-------------|
| jol-git-server | Source code, commit metadata | Indirect (author names, emails in git log) | Medium |
| jol-jira-server | Issue data, assignee info, descriptions | Yes (names, emails) | High |
| jol-compliance-server | Policy documents | No | Low |
| jol-docs-server | Documentation content | Indirect | Low |

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| PII leakage via tool output | Medium | High | Output sanitiser with PII redaction |
| Unauthorised access | Low | Critical | JWT auth with short-lived tokens |
| Data exfiltration via large responses | Low | Medium | Output size limits (100KB default) |
| Prompt injection leading to data access | Medium | High | Input allowlist + scope enforcement |

### Mitigations Applied

1. **Output Sanitisation**: All tool outputs pass through PII redaction filters
2. **Access Control**: JWT-based auth with tool-scoped permissions
3. **Audit Trail**: Every invocation logged for 7 years (ISO 27001 A.12.4)
4. **Data Minimisation**: Field allowlists on all data-returning tools

## DPIA Trigger Checklist

For each new tool or server, verify:

- [ ] Does the tool process personal data? → If yes, full DPIA required
- [ ] Does the tool access systems containing PII?
- [ ] Could the tool output contain personal data?
- [ ] Is there a legitimate basis for processing?
- [ ] Has the data subject been informed?
