"""Tests for the audit integration with the tool-execution flow (ADR-004)."""

from __future__ import annotations

import inspect
import json
import logging
import logging.handlers

import pytest

from shared.audit.audit_logger import AuditLogger
from shared.audit.integration import (
    audit_tool,
    create_audit_logger,
    redact_parameters,
)
from shared.audit.schemas import OutcomeStatus, Severity


def _memory_audit() -> AuditLogger:
    return AuditLogger("test-server", log_handler=logging.handlers.MemoryHandler(capacity=100))


def _events(audit: AuditLogger) -> list[dict]:
    handler = audit._logger.handlers[0]
    handler.flush()
    return [json.loads(record.getMessage()) for record in handler.buffer]


def test_success_invocation_logs_event():
    audit = _memory_audit()

    @audit_tool(audit)
    def add(a: int, b: int) -> int:
        return a + b

    assert add(2, 3) == 5
    (event,) = _events(audit)
    assert event["tool"]["name"] == "add"
    assert event["tool"]["server"] == "test-server"
    assert event["tool"]["parameters"] == {"a": 2, "b": 3}
    assert event["outcome"]["status"] == OutcomeStatus.SUCCESS
    assert event["severity"] == Severity.INFORMATIONAL


def test_error_string_result_logs_failure():
    audit = _memory_audit()

    @audit_tool(audit)
    def failing() -> str:
        return "Error: something went wrong"

    assert failing().startswith("Error:")
    (event,) = _events(audit)
    assert event["outcome"]["status"] == OutcomeStatus.FAILURE
    assert event["severity"] == Severity.WARNING


def test_exception_logged_and_reraised():
    audit = _memory_audit()

    @audit_tool(audit)
    def broken() -> str:
        raise ValueError("boom")

    with pytest.raises(ValueError, match="boom"):
        broken()
    (event,) = _events(audit)
    assert event["outcome"]["status"] == OutcomeStatus.FAILURE
    assert event["severity"] == Severity.ERROR
    assert event["outcome"]["output_size_bytes"] > 0


def test_timeout_logged_with_timeout_status():
    audit = _memory_audit()

    @audit_tool(audit)
    def slow() -> str:
        raise TimeoutError("deadline exceeded")

    with pytest.raises(TimeoutError):
        slow()
    (event,) = _events(audit)
    assert event["outcome"]["status"] == OutcomeStatus.TIMEOUT
    assert event["severity"] == Severity.ERROR


def test_secret_parameters_redacted():
    audit = _memory_audit()

    @audit_tool(audit)
    def connect(host: str, api_token: str) -> str:
        return "ok"

    connect("example.com", "super-secret")
    (event,) = _events(audit)
    assert event["tool"]["parameters"] == {"host": "example.com", "api_token": "[REDACTED]"}
    assert "super-secret" not in json.dumps(event)


def test_redact_parameters_helper():
    redacted = redact_parameters({"repo": "x", "password": "p", "JiraKey": "k"})
    assert redacted == {"repo": "x", "password": "[REDACTED]", "JiraKey": "[REDACTED]"}


def test_pii_detected_flag():
    audit = _memory_audit()

    @audit_tool(audit)
    def leaky() -> str:
        return "contact someone@example.com"

    leaky()
    (event,) = _events(audit)
    assert event["security"]["pii_detected_in_output"] is True


def test_caller_resolver_hook():
    audit = _memory_audit()
    caller = ("agent-xyz", "jti-123", ("git:read:log",))

    @audit_tool(audit, caller_resolver=lambda: caller)
    def tool() -> str:
        return "ok"

    tool()
    (event,) = _events(audit)
    assert event["caller"]["identity"] == "agent-xyz"
    assert event["caller"]["token_jti"] == "jti-123"
    assert event["caller"]["permissions"] == ["git:read:log"]


def test_default_caller_unresolved_until_auth_wired():
    audit = _memory_audit()

    @audit_tool(audit)
    def tool() -> str:
        return "ok"

    tool()
    (event,) = _events(audit)
    assert event["caller"]["identity"] == "unresolved"


def test_signature_preserved_for_fastmcp():
    audit = _memory_audit()

    def original(repo: str, max_count: int = 10) -> str:
        """Docstring kept for FastMCP tool descriptions."""
        return repo

    wrapped = audit_tool(audit)(original)
    assert wrapped.__name__ == "original"
    assert wrapped.__doc__ == original.__doc__
    assert inspect.signature(wrapped) == inspect.signature(original)


def test_create_audit_logger_writes_jsonl(tmp_path, monkeypatch):
    log_path = tmp_path / "audit.jsonl"
    monkeypatch.setenv("JOL_MCP_AUDIT_LOG_PATH", str(log_path))
    audit = create_audit_logger("file-server")

    @audit_tool(audit)
    def tool() -> str:
        return "ok"

    tool()
    for handler in audit._logger.handlers:
        handler.flush()

    lines = log_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    event = json.loads(lines[0])
    assert event["tool"]["server"] == "file-server"
    assert event["outcome"]["status"] == OutcomeStatus.SUCCESS


def test_create_audit_logger_falls_back_when_not_writable(tmp_path, monkeypatch):
    # Parent is a file, so the audit path can never be opened
    blocker = tmp_path / "blocker"
    blocker.write_text("x", encoding="utf-8")
    monkeypatch.setenv("JOL_MCP_AUDIT_LOG_PATH", str(blocker / "audit.jsonl"))
    audit = create_audit_logger("fallback-server")
    assert any(
        isinstance(handler, logging.StreamHandler) for handler in audit._logger.handlers
    )
