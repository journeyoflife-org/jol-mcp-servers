"""Structured OCSF audit logger — every invocation logged."""

from __future__ import annotations

import logging
from logging import Handler
from typing import Any

from shared.audit.schemas import (
    AuditEvent,
    CallerInfo,
    Outcome,
    OutcomeStatus,
    SecurityMetadata,
    Severity,
    ToolInfo,
)

logger = logging.getLogger("jol.audit")


class AuditLogger:
    """Structured audit logger for MCP tool invocations.

    Emits JSON Lines to a configurable output (stdout, file, or logging handler).
    """

    def __init__(self, server_name: str, log_handler: Handler | None = None) -> None:
        self._server_name = server_name
        self._logger = logging.getLogger(f"jol.audit.{server_name}")
        if log_handler:
            self._logger.addHandler(log_handler)
        else:
            # Fallback: ensure audit events are never silently lost
            self._logger.addHandler(logging.StreamHandler())
        self._logger.setLevel(logging.INFO)

    def log_invocation(
        self,
        caller_identity: str,
        token_jti: str,
        permissions: list[str],
        tool_name: str,
        parameters: dict[str, Any],
        outcome_status: OutcomeStatus,
        output_size: int,
        duration_ms: int,
        input_sanitised: bool = True,
        output_sanitised: bool = True,
        pii_detected: bool = False,
        severity: Severity = Severity.INFORMATIONAL,
    ) -> AuditEvent:
        """Log a tool invocation audit event.

        Returns the constructed AuditEvent for inspection.
        """
        event = AuditEvent(
            severity=severity,
            caller=CallerInfo(
                identity=caller_identity,
                token_jti=token_jti,
                permissions=permissions,
            ),
            tool=ToolInfo(
                server=self._server_name,
                name=tool_name,
                parameters=parameters,
            ),
            outcome=Outcome(
                status=outcome_status,
                output_size_bytes=output_size,
                duration_ms=duration_ms,
            ),
            security=SecurityMetadata(
                input_sanitised=input_sanitised,
                output_sanitised=output_sanitised,
                pii_detected_in_output=pii_detected,
            ),
        )

        self._logger.info(event.model_dump_json())
        return event
