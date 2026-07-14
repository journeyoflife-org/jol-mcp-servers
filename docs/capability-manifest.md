# Capability Manifest

**Purpose**: Complete inventory of every MCP tool, its permissions, data access, and authorised callers.
**Maintenance**: Must be updated for every new tool or permission change.

## jol-git-server

| Tool | Read | Write | PII Access | Permissions | Authorised Callers |
|------|------|-------|------------|-------------|-------------------|
| `git_log` | Yes | No | Author names, emails (git metadata) | `git:read:log` | All authenticated |
| `git_diff` | Yes | No | May appear in diff content | `git:read:diff` | All authenticated |
| `git_blame` | Yes | No | Author names, emails | `git:read:blame` | All authenticated |
| `git_status` | Yes | No | None | `git:read:status` | All authenticated |

## jol-jira-server

| Tool | Read | Write | PII Access | Permissions | Authorised Callers |
|------|------|-------|------------|-------------|-------------------|
| `issue_search` | Yes | No | Assignee names, reporter info | `jira:read:search` | All authenticated |
| `issue_create` | No | Yes (create) | Reporter field (auto) | `jira:write:create` | Approved callers only |

## jol-compliance-server

| Tool | Read | Write | PII Access | Permissions | Authorised Callers |
|------|------|-------|------------|-------------|-------------------|
| `policy_lookup` | Yes | No | None | `compliance:read:policy` | All authenticated |
| `gdpr_checklist` | Yes | No | None | `compliance:read:gdpr` | All authenticated |

## jol-docs-server

| Tool | Read | Write | PII Access | Permissions | Authorised Callers |
|------|------|-------|------------|-------------|-------------------|
| `doc_search` | Yes | No | Indirect (doc content) | `docs:read:search` | All authenticated |
