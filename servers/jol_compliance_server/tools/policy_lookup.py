"""Policy lookup tool — read-only query over compliance documents."""

from __future__ import annotations

import os
from pathlib import Path

from shared.sanitisation.input_sanitiser import InputSanitiser
from shared.sanitisation.output_sanitiser import OutputSanitiser

_sanitiser = InputSanitiser()
_output_sanitiser = OutputSanitiser()


def policy_lookup(topic: str) -> str:
    """Look up a compliance policy document by topic.

    Args:
        topic: Policy topic to search for (e.g., 'data-retention', 'access-control').

    Returns:
        Matching policy document content or 'not found' message.
    """
    safe_topic = _sanitiser.validate(topic, "topic")

    docs_root = os.environ.get(
        "JOL_MCP_COMPLIANCE_DOCS_ROOT",
        "/compliance-docs",
    )

    docs_path = Path(docs_root)
    if not docs_path.is_dir():
        return "Error: Compliance document store is not configured."

    # Search for matching policy file
    matches = list(docs_path.glob(f"*{safe_topic}*"))
    if not matches:
        return f"No policy documents found for topic: {safe_topic}"

    results = []
    for match in matches[:5]:  # Limit to 5 results
        if match.is_file():
            content = match.read_text(encoding="utf-8", errors="replace")
            results.append(f"--- {match.name} ---\n{content}")

    output = "\n\n".join(results)
    return _output_sanitiser.sanitise(output)
