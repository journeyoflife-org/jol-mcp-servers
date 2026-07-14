#!/usr/bin/env bash
# setup-dev.sh — One-command dev environment setup
set -euo pipefail

echo "=== jol-mcp-servers dev setup ==="

# Check for uv
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Sync dependencies
echo "Syncing dependencies..."
uv sync --all-extras

# Install pre-commit hooks (if pre-commit is available)
if command -v pre-commit &> /dev/null; then
    echo "Installing pre-commit hooks..."
    pre-commit install
fi

# Verify Python version
python_version=$(python --version 2>&1)
echo "Python: $python_version"

# Run initial lint check
echo "Running initial lint check..."
uv run ruff check shared/ || true

echo ""
echo "=== Setup complete ==="
echo "Run 'make test' to verify the setup."
echo "Run './scripts/run-server-local.sh jol-git-server' to start a server."
