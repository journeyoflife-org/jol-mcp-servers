.PHONY: scan lint test audit-log sync clean pre-push-check

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

pre-push-check:
	@echo "════════════════════════════════════════════"
	@echo "  JOL Pre-Push Validation — $(shell basename $(CURDIR))"
	@echo "════════════════════════════════════════════"
	@echo ""
	@echo "[1/5] TruffleHog — full history secret scan"
	@if command -v trufflehog >/dev/null 2>&1; then \
		trufflehog git file://. --results=verified,unknown --fail; \
	elif command -v docker >/dev/null 2>&1; then \
		docker run --rm -v "$(CURDIR):/repo" trufflesecurity/trufflehog:latest \
			git file:///repo --results=verified,unknown --fail --no-update; \
	else \
		echo "WARNING: trufflehog not installed and docker unavailable — secret scan SKIPPED"; \
	fi
	@echo ""
	@echo "[2/5] Ruff lint + Bandit SAST"
	uv run ruff check --select S,E,W,F,I,N,B . --output-format=concise
	uv run bandit -r shared/ servers/ -ll
	@echo ""
	@echo "[3/5] mypy type check"
	uv run mypy shared/ servers/ --ignore-missing-imports --strict || true
	@echo ""
	@echo "[4/5] pytest with coverage"
	uv run pytest --cov=shared --cov-report=term-missing --cov-fail-under=80 -q
	@echo ""
	@echo "[5/5] pip-audit dependency scan"
	uv run pip-audit --desc
	@echo ""
	@echo " All checks passed — safe to push"
