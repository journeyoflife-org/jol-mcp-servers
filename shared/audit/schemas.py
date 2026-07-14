"""Pydantic models for OCSF-based audit events."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class OutcomeStatus(StrEnum):
    """Valid outcome statuses for audit events."""

    SUCCESS = "Success"
    FAILURE = "Failure"
    TIMEOUT = "Timeout"


class Severity(StrEnum):
    """Audit event severity levels."""

    INFORMATIONAL = "Informational"
    WARNING = "Warning"
    ERROR = "Error"


class CallerInfo(BaseModel):
    """Caller identity information."""

    identity: str
    token_jti: str
    permissions: list[str]


class ToolInfo(BaseModel):
    """Tool invocation details."""

    server: str
    name: str
    parameters: dict[str, Any]


class Outcome(BaseModel):
    """Invocation outcome."""

    status: OutcomeStatus
    output_size_bytes: int
    duration_ms: int


class SecurityMetadata(BaseModel):
    """Security-related metadata for the invocation."""

    input_sanitised: bool = True
    output_sanitised: bool = True
    pii_detected_in_output: bool = False


class AuditEvent(BaseModel):
    """OCSF-based audit event for a tool invocation."""

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    event_class: str = "Tool Invocation"
    severity: Severity = Severity.INFORMATIONAL
    caller: CallerInfo
    tool: ToolInfo
    outcome: Outcome
    security: SecurityMetadata = Field(default_factory=SecurityMetadata)
