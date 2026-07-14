"""Tests for the AuditLogger."""

from __future__ import annotations

import logging
import logging.handlers

from shared.audit.audit_logger import AuditLogger
from shared.audit.schemas import OutcomeStatus, Severity


def _make_logger(handler: logging.Handler | None = None) -> AuditLogger:
    return AuditLogger("test-server", log_handler=handler)


def test_audit_logger_with_handler():
    handler = logging.handlers.MemoryHandler(capacity=100)
    audit = _make_logger(handler)
    event = audit.log_invocation(
        caller_identity="user-1",
        token_jti="jti-1",
        permissions=["git:read"],
        tool_name="git_log",
        parameters={"repo": "test"},
        outcome_status=OutcomeStatus.SUCCESS,
        output_size=256,
        duration_ms=50,
    )
    assert event.tool.name == "git_log"
    assert event.outcome.status == OutcomeStatus.SUCCESS


def test_audit_logger_fallback_handler():
    """Without a handler, StreamHandler fallback is used."""
    audit = AuditLogger("fallback-server")
    event = audit.log_invocation(
        caller_identity="u",
        token_jti="j",
        permissions=[],
        tool_name="t",
        parameters={},
        outcome_status=OutcomeStatus.FAILURE,
        output_size=0,
        duration_ms=0,
        severity=Severity.WARNING,
    )
    assert event.severity == Severity.WARNING


def test_audit_logger_pii_flags():
    handler = logging.handlers.MemoryHandler(capacity=10)
    audit = _make_logger(handler)
    event = audit.log_invocation(
        caller_identity="u",
        token_jti="j",
        permissions=[],
        tool_name="t",
        parameters={},
        outcome_status=OutcomeStatus.SUCCESS,
        output_size=0,
        duration_ms=0,
        input_sanitised=False,
        output_sanitised=False,
        pii_detected=True,
    )
    assert event.security.input_sanitised is False
    assert event.security.pii_detected_in_output is True
