"""Git log tool — read-only commit history inspection."""

from __future__ import annotations

import os
import subprocess

from shared.sanitisation.input_sanitiser import InputSanitiser
from shared.sanitisation.output_sanitiser import OutputSanitiser

_sanitiser = InputSanitiser()
_output_sanitiser = OutputSanitiser()


def git_log(repo: str, max_count: int = 10) -> str:
    """View commit history for a repository.

    Args:
        repo: Repository name (must be within allowed repo root).
        max_count: Maximum number of commits to return (default: 10).

    Returns:
        Formatted git log output.
    """
    # Validate inputs
    safe_repo = _sanitiser.validate_repo_path(repo)
    repo_root = os.environ.get("JOL_MCP_GIT_REPO_ROOT", "/repos")
    repo_path = os.path.join(repo_root, safe_repo)

    if not os.path.isdir(repo_path):
        return f"Error: Repository '{safe_repo}' not found."

    # Parameterised git log (no shell passthrough)
    result = subprocess.run(  # noqa: S603
        ["git", "log", f"--max-count={max_count}", "--format=%H %s (%an, %ar)"],  # noqa: S607
        cwd=repo_path,
        capture_output=True,
        text=True,
        timeout=30,
    )

    if result.returncode != 0:
        return f"Error: {result.stderr.strip()}"

    return _output_sanitiser.sanitise(result.stdout)
