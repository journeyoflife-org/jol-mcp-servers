"""Audit integration for the MCP tool-execution flow.

Wires ``AuditLogger`` into every tool invocation (ADR-004: "every invocation
logged — no exceptions"). Each server registers its tools through
``audit_tool`` / ``register_audited_tools`` so outcome, duration, and output
size are captured centrally instead of duplicating logging in each tool.
"""

from __future__ import annotations

import functools
import inspect
import logging
import math
import os
import re
import sys
import time
from collections.abc import Callable
from logging import FileHandler, Formatter
from typing import Any, ParamSpec, TypeVar

from shared.audit.audit_logger import AuditLogger
from shared.audit.schemas import OutcomeStatus, Severity
from shared.config.settings import Settings
from shared.sanitisation.output_sanitiser import OutputSanitiser

logger = logging.getLogger("jol.audit.integration")

P = ParamSpec("P")
R = TypeVar("R")

# Parameter names that must never appear in audit logs unredacted
_SECRET_KEY_PATTERN = re.compile(r"(token|secret|password|credential|auth|key)", re.IGNORECASE)

#: Caller attribution placeholder until JWT transport auth is wired in
#: (ADR-002); every event is still attributable by server + tool + timestamp.
_UNRESOLVED_CALLER = ("unresolved", "", ())


def redact_parameters(parameters: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of parameters with secret-looking values redacted."""
    return {
        name: "[REDACTED]" if _SECRET_KEY_PATTERN.search(name) else value
        for name, value in parameters.items()
    }


def create_audit_logger(server_name: str) -> AuditLogger:
    """Create the server's audit logger writing JSON Lines to the audit log path.

    The path comes from ``JOL_MCP_AUDIT_LOG_PATH`` (default
    ``/var/log/jol-mcp/audit.jsonl``). If the file cannot be opened, events
    fall back to stderr so audit records are never silently lost.
    """
    path = Settings().audit_log_path
    try:
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        handler: logging.Handler = FileHandler(path, encoding="utf-8")
    except OSError as exc:
        logger.error("Audit log %s is not writable (%s); falling back to stderr", path, exc)
        handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(Formatter("%(message)s"))  # raw JSON lines, no prefix
    return AuditLogger(server_name, log_handler=handler)


def audit_tool(
    audit: AuditLogger,
    caller_resolver: Callable[[], tuple[str, str, tuple[str, ...]]] | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorate a tool function so every invocation emits an audit event.

    The wrapper preserves the tool's signature (required for FastMCP
    registration), maps exceptions and ``Error:`` results onto outcome
    statuses, and re-raises tool exceptions after logging. Audit emission is
    best-effort: a logging failure must never break the tool invocation.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        resolve_caller = caller_resolver or (lambda: _UNRESOLVED_CALLER)

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = time.perf_counter()
            result: R | None = None
            exc: BaseException | None = None
            try:
                result = func(*args, **kwargs)
            except TimeoutError as timeout_exc:
                exc = timeout_exc
            except Exception as tool_exc:  # noqa: BLE001 — every failure must be audited
                exc = tool_exc

            duration_ms = math.ceil((time.perf_counter() - start) * 1000)
            output = result if exc is None else str(exc)
            status = _outcome_status(exc, result)
            severity = _severity(exc, result)

            try:
                bound = inspect.signature(func).bind_partial(*args, **kwargs)
                parameters = redact_parameters(dict(bound.arguments))
            except TypeError:
                parameters = {}

            identity, token_jti, permissions = resolve_caller()
            try:
                audit.log_invocation(
                    caller_identity=identity,
                    token_jti=token_jti,
                    permissions=list(permissions),
                    tool_name=func.__name__,
                    parameters=parameters,
                    outcome_status=status,
                    output_size=len(str(output).encode("utf-8")),
                    duration_ms=duration_ms,
                    pii_detected=isinstance(output, str) and OutputSanitiser.contains_pii(output),
                    severity=severity,
                )
            except Exception:  # noqa: BLE001 — never let audit emission break the call
                logger.exception("Failed to emit audit event for %s", func.__name__)

            if exc is not None:
                raise exc
            return result  # type: ignore[return-value]

        return wrapper

    return decorator


def register_audited_tools(mcp: Any, audit: AuditLogger, tools: list[Callable[..., Any]]) -> None:
    """Register tools on a FastMCP server wrapped with audit logging."""
    for tool in tools:
        mcp.tool()(audit_tool(audit)(tool))


def _outcome_status(exc: BaseException | None, result: Any) -> OutcomeStatus:
    if isinstance(exc, TimeoutError):
        return OutcomeStatus.TIMEOUT
    if exc is not None:
        return OutcomeStatus.FAILURE
    if isinstance(result, str) and result.startswith("Error:"):
        return OutcomeStatus.FAILURE
    return OutcomeStatus.SUCCESS


def _severity(exc: BaseException | None, result: Any) -> Severity:
    # Unhandled exceptions and timeouts are Errors; handled tool errors are Warnings
    if exc is not None:
        return Severity.ERROR
    if isinstance(result, str) and result.startswith("Error:"):
        return Severity.WARNING
    return Severity.INFORMATIONAL
