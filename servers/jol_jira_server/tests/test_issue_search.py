"""Tests for issue_search tool."""

from __future__ import annotations

import pytest

from shared.errors.exceptions import SanitisationError
from shared.sanitisation.input_sanitiser import InputSanitiser


def test_jql_validation_allows_valid_queries():
    """Valid JQL queries should pass validation."""
    sanitiser = InputSanitiser()
    assert sanitiser.validate_jql('project = "PROJ"') == 'project = "PROJ"'
    assert sanitiser.validate_jql("status = Open") == "status = Open"
    assert sanitiser.validate_jql("assignee = currentUser()") == "assignee = currentUser()"


def test_jql_validation_rejects_injection():
    """JQL with injection attempts should be rejected."""
    sanitiser = InputSanitiser()
    with pytest.raises(SanitisationError):
        sanitiser.validate_jql("project = PROJ; DROP TABLE issues;")


def test_issue_search_no_config():
    """issue_search should return error when JIRA_URL is not set."""
    import os

    from servers.jol_jira_server.tools.issue_search import issue_search

    os.environ.pop("JOL_MCP_JIRA_URL", None)
    result = issue_search("project = TEST")
    assert "Error" in result
