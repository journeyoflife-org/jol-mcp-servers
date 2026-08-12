# Runbook: Deploying to mcp-prod-lt01

Audience: platform operators. Change control: every deployment requires a GitHub
issue with rollback plan (see Issue #29 as template) and a Proxmox snapshot
taken before changes.

Related: [server documentation](../servers/mcp-prod-lt01.md) |
[incident response](../runbook-incident-response.md) |
[change control / break-glass](../../SECURITY.md)

## Architecture recap

- Deploy trigger: `git push mcp-prod main` from an authorized workstation
- Remote: `ssh://jol-admin@mcp-prod-lt01/opt/jol/git/jol-mcp-servers.git` (bare)
- The `post-receive` hook checks out `main` into `/opt/jol-mcp-servers` and
  restarts the four MCP systemd units
- Transport is stdio only — there is nothing to expose or port-forward

## Prerequisites

1. Branch merged to `main` via signed-commit PR (status checks + review passed)
2. `git log origin/main..HEAD` is clean locally; `main` is what you push
3. Proxmox snapshot of the guest taken and recorded in the change issue
4. All modified host files backed up with timestamped `.bak` suffixes
5. If new env vars are introduced: add them to `/etc/jol-mcp/mcp.env` (root:0600)
   BEFORE pushing, then update `docs/servers/mcp-prod-lt01.md` § Environment and
   `inventory/prod/host_vars/mcp-prod-lt01.yml` `jol_audit_secret_files`

## Deploy

```bash
# From the repository checkout (mcp-prod remote already configured)
git checkout main
git pull origin main
git push mcp-prod main
```

The post-receive hook performs checkout + unit restarts. Watch it live:

```bash
ssh jol-admin@mcp-prod-lt01 'sudo journalctl -fu jol-git-server'  # or any unit
```

## Verify

1. **Units active** (all four, plus node_exporter):

   ```bash
   systemctl status jol-git-server jol-jira-server jol-compliance-server jol-docs-server node_exporter
   ```

2. **MCP protocol smoke test** per server — the JSON-RPC sequence
   `initialize` → `initialized` → `tools/list` → `tools/call` must succeed:

   ```bash
   sudo -u mcp-svc sh -c 'cd /opt/jol-mcp-servers && .venv/bin/python -m servers.jol_git_server.server'
   # drive the stdio session with an MCP client (e.g. MCP Inspector in stdio mode)
   ```

3. **Audit trail**: each executed tool call must produce exactly one OCSF record:

   ```bash
   sudo tail -n 5 /var/log/jol-mcp/audit.jsonl | jq .
   ```

4. **Metrics reachable from VLAN 40 only**:

   ```bash
   curl -s http://10.40.40.11:9100/metrics | head   # from a 10.40.40.0/24 peer
   ```

   A timeout from any other subnet is correct behaviour (UFW source filtering).

5. **Integrity**: after host-level changes, rebuild the AIDE baseline
   (`aideinit` / `aide --update`), then confirm the nightly check passes (rc=0).

## Rollback

In order of preference:

1. **Git revert**: revert the offending commit on `main`, re-push
   (`git push mcp-prod main`). Fastest for code-level regressions.
2. **File restore**: restore affected files from their timestamped `.bak` copies
   and restart the relevant units:

   ```bash
   sudo systemctl restart jol-git-server jol-jira-server jol-compliance-server jol-docs-server
   ```

3. **Proxmox snapshot**: instant full-VM rollback to the pre-change snapshot
   recorded in the change issue (current reference snapshot:
   `pre-mcp-fix-20260812-2213`). Use for host-level regressions (systemd,
   firewall, AIDE/auditd config).

After any rollback: re-run the Verify steps above and append evidence to the
change issue.

## Escalation

If rollback does not restore service, follow the break-glass procedure in
[SECURITY.md](../../SECURITY.md) and the [incident response runbook](../runbook-incident-response.md).
