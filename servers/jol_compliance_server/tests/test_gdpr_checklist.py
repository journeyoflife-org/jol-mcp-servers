"""Tests for gdpr_checklist tool."""

from __future__ import annotations

from servers.jol_compliance_server.tools.gdpr_checklist import gdpr_checklist


def test_gdpr_checklist_returns_checklist():
    result = gdpr_checklist("user-profile")
    assert "GDPR Checklist" in result
    assert "Data Collection" in result
    assert "Data Storage" in result
    assert "Breach Response" in result


def test_gdpr_checklist_contains_checkboxes():
    result = gdpr_checklist("analytics")
    assert "- [ ]" in result


def test_gdpr_checklist_strips_injection():
    """Shell metacharacters are stripped, not raised — remaining text is safe."""
    result = gdpr_checklist("feature; rm -rf /")
    # Semicolons are stripped by the sanitiser
    assert ";" not in result
    assert "GDPR Checklist" in result
