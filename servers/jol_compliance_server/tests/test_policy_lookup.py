"""Tests for policy_lookup tool."""

from __future__ import annotations

from servers.jol_compliance_server.tools.policy_lookup import policy_lookup


def test_policy_lookup_no_docs_dir(monkeypatch):
    """policy_lookup should return error when docs dir is missing."""
    monkeypatch.setenv("JOL_MCP_COMPLIANCE_DOCS_ROOT", "/nonexistent/path")
    result = policy_lookup("data-retention")
    assert "Error" in result


def test_policy_lookup_with_test_docs(tmp_path, monkeypatch):
    """policy_lookup should find matching documents."""
    # Create test doc
    doc = tmp_path / "data-retention-policy.md"
    doc.write_text("# Data Retention Policy\nRetain for 7 years.")
    monkeypatch.setenv("JOL_MCP_COMPLIANCE_DOCS_ROOT", str(tmp_path))

    result = policy_lookup("data-retention")
    assert "Data Retention" in result


def test_policy_lookup_no_match(tmp_path, monkeypatch):
    """policy_lookup should handle no matches gracefully."""
    doc = tmp_path / "other-policy.md"
    doc.write_text("# Other Policy")
    monkeypatch.setenv("JOL_MCP_COMPLIANCE_DOCS_ROOT", str(tmp_path))

    result = policy_lookup("nonexistent-topic")
    assert "No policy documents found" in result
