"""Jira issue creation tool — create only, no delete."""

from __future__ import annotations

import os

import httpx

from shared.sanitisation.input_sanitiser import InputSanitiser
from shared.sanitisation.output_sanitiser import OutputSanitiser

_sanitiser = InputSanitiser()
_output_sanitiser = OutputSanitiser()


def issue_create(
    project_key: str,
    summary: str,
    description: str = "",
    issue_type: str = "Task",
) -> str:
    """Create a new Jira issue.

    Args:
        project_key: Jira project key (e.g., 'PROJ').
        summary: Issue summary/title.
        description: Issue description (optional).
        issue_type: Issue type (default: 'Task').

    Returns:
        Created issue key or error message.
    """
    safe_project = _sanitiser.validate(project_key, "project_key")
    safe_summary = _sanitiser.validate(summary, "summary")
    safe_type = _sanitiser.validate(issue_type, "issue_type")
    safe_description = _sanitiser.validate(description, "description") if description else ""

    jira_url = os.environ.get("JOL_MCP_JIRA_URL", "")
    jira_token = os.environ.get("JOL_MCP_JIRA_TOKEN", "")

    if not jira_url:
        return "Error: Jira integration is not configured."

    payload = {
        "fields": {
            "project": {"key": safe_project},
            "summary": safe_summary,
            "description": safe_description,
            "issuetype": {"name": safe_type},
        }
    }

    try:
        with httpx.Client(timeout=30) as client:
            response = client.post(
                f"{jira_url}/rest/api/2/issue",
                json=payload,
                headers={
                    "Authorization": f"Bearer {jira_token}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
    except httpx.HTTPError as exc:
        return f"Error: Failed to create issue: {exc}"

    data = response.json()
    issue_key = data.get("key", "UNKNOWN")
    return _output_sanitiser.sanitise(f"Created issue: {issue_key}")
