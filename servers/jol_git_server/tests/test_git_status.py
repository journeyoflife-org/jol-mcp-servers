"""Tests for git_status tool."""

from __future__ import annotations

import subprocess

import pytest

from servers.jol_git_server.tools.git_status import git_status
from shared.errors.exceptions import SanitisationError


def test_git_status_nonexistent_repo():
    """Should return error for non-existent repo."""
    result = git_status("nonexistent-repo")
    assert "not found" in result.lower() or "error" in result.lower()


def test_git_status_with_real_repo(tmp_path, monkeypatch):
    """Should return git status output for a valid repo."""
    repo_dir = tmp_path / "test-repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, capture_output=True)
    monkeypatch.setenv("JOL_MCP_GIT_REPO_ROOT", str(tmp_path))
    result = git_status("test-repo")
    # Should contain something (either status output or "Working tree clean")
    assert isinstance(result, str)
    assert len(result) > 0


def test_git_status_rejects_injection():
    """Path traversal should be rejected."""
    with pytest.raises(SanitisationError):
        git_status("../../../etc/passwd")
