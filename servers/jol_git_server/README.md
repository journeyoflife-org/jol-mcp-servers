# jol-git-server

MCP server providing read-only Git repository inspection tools.

## Capabilities

| Tool | Description | Permission |
|------|-------------|-----------|
| `git_log` | View commit history (read-only) | `git:read:log` |
| `git_diff` | View diffs between commits/branches | `git:read:diff` |
| `git_blame` | Line-by-line attribution | `git:read:blame` |
| `git_status` | Working tree status | `git:read:status` |

## Security

- **Read-only**: No write operations permitted
- **Input sanitisation**: Repository paths validated against allowlist
- **No shell passthrough**: All Git operations use parameterised execution
- **Audit logging**: Every invocation logged in OCSF format

## Running

```bash
python server.py
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `JOL_MCP_GIT_REPO_ROOT` | Base path for allowed repositories | `/repos` |
| `JOL_MCP_JWT_PUBLIC_KEY` | JWT public key for auth | Required |
