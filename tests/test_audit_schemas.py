"""Tests for shared audit schemas."""

from __future__ import annotations

from datetime import datetime

from shared.audit.schemas import (
    AuditEvent,
    CallerInfo,
    Outcome,
    OutcomeStatus,
    SecurityMetadata,
    Severity,
    ToolInfo,
)


def test_outcome_status_enum_values():
    assert OutcomeStatus.SUCCESS == "Success"
    assert OutcomeStatus.FAILURE == "Failure"
    assert OutcomeStatus.TIMEOUT == "Timeout"


def test_severity_enum_values():
    assert Severity.INFORMATIONAL == "Informational"
    assert Severity.WARNING == "Warning"
    assert Severity.ERROR == "Error"


def test_caller_info_model():
    caller = CallerInfo(identity="user-123", token_jti="jti-abc", permissions=["git:read"])
    assert caller.identity == "user-123"
    assert caller.token_jti == "jti-abc"
    assert caller.permissions == ["git:read"]


def test_tool_info_model():
    tool = ToolInfo(server="jol-git-server", name="git_log", parameters={"repo": "my-repo"})
    assert tool.server == "jol-git-server"
    assert tool.name == "git_log"
    assert tool.parameters == {"repo": "my-repo"}


def test_outcome_model():
    outcome = Outcome(status=OutcomeStatus.SUCCESS, output_size_bytes=1024, duration_ms=150)
    assert outcome.status == OutcomeStatus.SUCCESS
    assert outcome.output_size_bytes == 1024
    assert outcome.duration_ms == 150


def test_security_metadata_defaults():
    sec = SecurityMetadata()
    assert sec.input_sanitised is True
    assert sec.output_sanitised is True
    assert sec.pii_detected_in_output is False


def test_audit_event_construction():
    event = AuditEvent(
        caller=CallerInfo(identity="u1", token_jti="j1", permissions=["p1"]),
        tool=ToolInfo(server="s", name="t", parameters={}),
        outcome=Outcome(status=OutcomeStatus.SUCCESS, output_size_bytes=0, duration_ms=0),
    )
    assert event.event_class == "Tool Invocation"
    assert event.severity == Severity.INFORMATIONAL
    assert isinstance(event.timestamp, datetime)
    assert event.security.input_sanitised is True


def test_audit_event_custom_severity():
    event = AuditEvent(
        severity=Severity.ERROR,
        caller=CallerInfo(identity="u", token_jti="j", permissions=[]),
        tool=ToolInfo(server="s", name="t", parameters={}),
        outcome=Outcome(status=OutcomeStatus.FAILURE, output_size_bytes=0, duration_ms=0),
    )
    assert event.severity == Severity.ERROR


def test_audit_event_serialisation():
    event = AuditEvent(
        caller=CallerInfo(identity="u", token_jti="j", permissions=[]),
        tool=ToolInfo(server="s", name="t", parameters={}),
        outcome=Outcome(status=OutcomeStatus.SUCCESS, output_size_bytes=10, duration_ms=5),
    )
    json_str = event.model_dump_json()
    assert "Tool Invocation" in json_str
    assert "Success" in json_str
