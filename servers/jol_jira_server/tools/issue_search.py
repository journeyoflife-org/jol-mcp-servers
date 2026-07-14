"""Jira issue search tool — JQL with field allowlist enforcement."""

from __future__ import annotations

import os

import httpx

from shared.sanitisation.input_sanitiser import InputSanitiser
from shared.sanitisation.output_sanitiser import OutputSanitiser

_sanitiser = InputSanitiser()
_output_sanitiser = OutputSanitiser()

# Only these fields are returned in search results
_FIELD_ALLOWLIST = {"key", "summary", "status", "assignee", "created", "priority", "issuetype"}


def issue_search(jql: str, max_results: int = 20) -> str:
    """Search Jira issues using JQL.

    Args:
        jql: JQL query string (validated against allowlist).
        max_results: Maximum number of results (default: 20).

    Returns:
        Formatted search results.
    """
    safe_jql = _sanitiser.validate_jql(jql)

    jira_url = os.environ.get("JOL_MCP_JIRA_URL", "")
    jira_token = os.environ.get("JOL_MCP_JIRA_TOKEN", "")

    if not jira_url:
        return "Error: Jira integration is not configured."

    # Build request with field allowlist
    params: dict[str, str | int] = {
        "jql": safe_jql,
        "maxResults": min(max_results, 50),
        "fields": ",".join(sorted(_FIELD_ALLOWLIST)),
    }

    try:
        with httpx.Client(timeout=30) as client:
            response = client.get(
                f"{jira_url}/rest/api/2/search",
                params=params,
                headers={
                    "Authorization": f"Bearer {jira_token}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
    except httpx.HTTPError as exc:
        return f"Error: Failed to query Jira: {exc}"

    data = response.json()
    issues = data.get("issues", [])

    if not issues:
        return "No issues found matching the query."

    lines = []
    for issue in issues:
        fields = issue.get("fields", {})
        line = (
            f"- {issue.get('key')}: {fields.get('summary', 'N/A')} "
            f"[{fields.get('status', {}).get('name', 'Unknown')}]"
        )
        lines.append(line)

    result = f"Found {len(issues)} issue(s):\n" + "\n".join(lines)
    return _output_sanitiser.sanitise(result)
