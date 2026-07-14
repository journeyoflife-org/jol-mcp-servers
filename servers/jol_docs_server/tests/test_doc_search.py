"""Tests for doc_search tool."""

from __future__ import annotations

from servers.jol_docs_server.tools.doc_search import doc_search


def test_doc_search_no_docs_dir(monkeypatch):
    """doc_search should return error when docs dir is missing."""
    monkeypatch.setenv("JOL_MCP_DOCS_ROOT", "/nonexistent/path")
    result = doc_search("security")
    assert "Error" in result


def test_doc_search_finds_matching_docs(tmp_path, monkeypatch):
    """doc_search should find documents containing search terms."""
    doc = tmp_path / "security.md"
    doc.write_text("# Security\nThis document covers security policies and authentication.")
    monkeypatch.setenv("JOL_MCP_DOCS_ROOT", str(tmp_path))

    result = doc_search("security")
    assert "security" in result.lower()
    assert "security.md" in result.lower()


def test_doc_search_no_results(tmp_path, monkeypatch):
    """doc_search should handle no matches gracefully."""
    doc = tmp_path / "readme.md"
    doc.write_text("# Hello World\nThis is a test document.")
    monkeypatch.setenv("JOL_MCP_DOCS_ROOT", str(tmp_path))

    result = doc_search("nonexistent term")
    assert "No documentation found" in result
