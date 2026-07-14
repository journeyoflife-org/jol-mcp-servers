#!/usr/bin/env bash
# run-server-local.sh — Run a named MCP server locally with restricted env
set -euo pipefail

SERVER_NAME="${1:?Usage: run-server-local.sh <server-name>}"

# Accept both hyphen and underscore forms
SAFE_NAME="${SERVER_NAME//-/_}"

VALID_SERVERS=("jol_git_server" "jol_jira_server" "jol_compliance_server" "jol_docs_server")
VALID=false
for s in "${VALID_SERVERS[@]}"; do
    if [[ "$SAFE_NAME" == "$s" ]]; then
        VALID=true
        break
    fi
done

if [[ "$VALID" != "true" ]]; then
    echo "Error: Unknown server '$SERVER_NAME'"
    echo "Valid servers: ${VALID_SERVERS[*]}"
    exit 1
fi

SERVER_DIR="servers/${SAFE_NAME}"
SERVER_PY="${SERVER_DIR}/server.py"

if [[ ! -f "$SERVER_PY" ]]; then
    echo "Error: Server file not found: $SERVER_PY"
    exit 1
fi

# Set restricted environment
export JOL_MCP_SERVER_NAME="$SERVER_NAME"
export JOL_MCP_LOG_LEVEL="${JOL_MCP_LOG_LEVEL:-DEBUG}"

# Use a temp directory for audit logs
export JOL_MCP_AUDIT_LOG_PATH="$(mktemp -d)/audit.jsonl"

echo "Starting $SERVER_NAME..."
echo "  Audit log: $JOL_MCP_AUDIT_LOG_PATH"
echo "  Log level: $JOL_MCP_LOG_LEVEL"
echo ""

exec uv run python "$SERVER_PY"
