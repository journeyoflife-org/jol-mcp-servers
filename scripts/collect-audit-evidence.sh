#!/usr/bin/env bash
# collect-audit-evidence.sh — SOC 2 quarterly: export audit logs + scan results
set -euo pipefail

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="audit-exports/soc2_quarterly_${TIMESTAMP}"

echo "=== SOC 2 Audit Evidence Collection ==="
echo "Output directory: $OUTPUT_DIR"

mkdir -p "$OUTPUT_DIR"

# Collect audit logs
if [[ -d "/var/log/jol-mcp" ]]; then
    echo "Collecting audit logs..."
    cp /var/log/jol-mcp/*.jsonl "$OUTPUT_DIR/" 2>/dev/null || echo "  No audit logs found"
fi

# Collect scan results
echo "Collecting security scan results..."

# Bandit
uv run bandit -r shared/ servers/ -ll -f json > "$OUTPUT_DIR/bandit_results.json" 2>/dev/null || true

# pip-audit
uv run pip-audit --format json > "$OUTPUT_DIR/pip_audit_results.json" 2>/dev/null || true

# Ruff
uv run ruff check . --output-format json > "$OUTPUT_DIR/ruff_results.json" 2>/dev/null || true

# Collect git log for change evidence
echo "Collecting git change log..."
git log --oneline --since="3 months ago" > "$OUTPUT_DIR/git_changelog.txt" 2>/dev/null || true

# Collect dependency versions
echo "Collecting dependency versions..."
uv pip freeze > "$OUTPUT_DIR/pip_freeze.txt" 2>/dev/null || true

echo ""
echo "=== Evidence collection complete ==="
echo "Output: $OUTPUT_DIR"
ls -la "$OUTPUT_DIR"
