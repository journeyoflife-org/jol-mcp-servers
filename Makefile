.PHONY: scan lint test audit-log sync clean

sync:
	uv sync --all-extras

lint:
	uv run ruff check .
	uv run mypy shared/ servers/

test:
	uv run pytest --tb=short -q

scan:
	uv run bandit -r shared/ servers/ -ll
	uv run pip-audit

audit-log:
	@echo "Collecting audit evidence for SOC 2 quarterly review..."
	./scripts/collect-audit-evidence.sh

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage htmlcov/
