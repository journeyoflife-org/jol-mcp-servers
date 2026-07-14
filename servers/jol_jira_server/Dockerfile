FROM python:3.12-slim AS builder

WORKDIR /app
COPY pyproject.toml ./
COPY servers/jol_jira_server/pyproject.toml ./server-pyproject.toml
RUN pip install --no-cache-dir uv && \
    uv venv .venv && \
    uv pip install --python .venv/bin/python -r server-pyproject.toml

FROM python:3.12-slim

RUN groupadd -g 10001 jol-mcp && \
    useradd -u 10001 -g jol-mcp -m -s /bin/false jol-mcp

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY servers/jol_jira_server/ ./
COPY shared/ ./shared/

ENV PATH="/app/.venv/bin:$PATH"

USER jol-mcp

CMD ["python", "server.py"]
