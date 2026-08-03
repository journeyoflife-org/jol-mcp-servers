"""Structured audit logging module."""

from shared.audit.audit_logger import AuditLogger
from shared.audit.integration import (
    audit_tool,
    create_audit_logger,
    redact_parameters,
    register_audited_tools,
)
from shared.audit.schemas import (
    AuditEvent,
    Outcome,
    OutcomeStatus,
    SecurityMetadata,
    Severity,
    ToolInfo,
)

__all__ = [
    "AuditLogger",
    "AuditEvent",
    "ToolInfo",
    "Outcome",
    "OutcomeStatus",
    "SecurityMetadata",
    "Severity",
    "audit_tool",
    "create_audit_logger",
    "redact_parameters",
    "register_audited_tools",
]
