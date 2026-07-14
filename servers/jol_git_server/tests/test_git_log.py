"""Tests for git_log tool."""

from __future__ import annotations

import subprocess

import pytest

from servers.jol_git_server.tools.git_log import git_log


@pytest.fixture
def git_repo(tmp_path):
    """Create a temporary git repository for testing."""
    subprocess.run(["git", "init", str(tmp_path / "test-repo")], check=True, capture_output=True)
    repo_path = tmp_path / "test-repo"
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=str(repo_path),
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=str(repo_path),
        check=True,
        capture_output=True,
    )
    # Create an initial commit
    readme = repo_path / "README.md"
    readme.write_text("# Test")
    subprocess.run(["git", "add", "."], cwd=str(repo_path), check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=str(repo_path),
        check=True,
        capture_output=True,
    )
    return repo_path


def test_git_log_returns_commits(git_repo, monkeypatch):
    """git_log should return commit history."""
    monkeypatch.setenv("JOL_MCP_GIT_REPO_ROOT", str(git_repo.parent))
    result = git_log(git_repo.name)
    assert "Initial commit" in result


def test_git_log_nonexistent_repo(monkeypatch):
    """git_log should handle missing repos gracefully."""
    monkeypatch.setenv("JOL_MCP_GIT_REPO_ROOT", "/nonexistent")
    result = git_log("missing-repo")
    assert "Error" in result or "not found" in result


def test_git_log_max_count(git_repo, monkeypatch):
    """git_log should respect max_count parameter."""
    monkeypatch.setenv("JOL_MCP_GIT_REPO_ROOT", str(git_repo.parent))
    result = git_log(git_repo.name, max_count=1)
    assert "Initial commit" in result
