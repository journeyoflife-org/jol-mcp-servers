"""Document search tool — vector search over documentation."""

from __future__ import annotations

import os
from pathlib import Path

from shared.sanitisation.input_sanitiser import InputSanitiser
from shared.sanitisation.output_sanitiser import OutputSanitiser

_sanitiser = InputSanitiser()
_output_sanitiser = OutputSanitiser()


def doc_search(query: str, max_results: int = 5) -> str:
    """Search documentation using keyword matching.

    Note: In production, this would use a vector embedding store.
    Currently implements basic keyword-based search over docs directory.

    Args:
        query: Search query string.
        max_results: Maximum number of results (default: 5).

    Returns:
        Matching documentation excerpts.
    """
    safe_query = _sanitiser.validate(query, "query")

    docs_root = os.environ.get("JOL_MCP_DOCS_ROOT", "/docs")
    docs_path = Path(docs_root)

    if not docs_path.is_dir():
        return "Error: Documentation store is not configured."

    # Simple keyword search over markdown files
    query_terms = safe_query.lower().split()
    results: list[tuple[str, float, str]] = []

    for md_file in docs_path.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8", errors="replace")
        content_lower = content.lower()

        # Score by term frequency
        score: float = float(sum(content_lower.count(term) for term in query_terms))
        if score > 0:
            # Extract first 500 chars as excerpt
            excerpt = content[:500]
            if len(content) > 500:
                excerpt += "..."
            results.append((md_file.name, score, excerpt))

    # Sort by relevance score
    results.sort(key=lambda x: x[1], reverse=True)
    results = results[:max_results]

    if not results:
        return f"No documentation found matching: {safe_query}"

    lines = [f"Found {len(results)} result(s) for: {safe_query}\n"]
    for filename, score, excerpt in results:
        lines.append(f"### {filename} (relevance: {score})")
        lines.append(excerpt)
        lines.append("")

    output = "\n".join(lines)
    return _output_sanitiser.sanitise(output)
