"""Git status tool — read-only working tree status."""

from __future__ import annotations

import os
import subprocess

from shared.sanitisation.input_sanitiser import InputSanitiser
from shared.sanitisation.output_sanitiser import OutputSanitiser

_sanitiser = InputSanitiser()
_output_sanitiser = OutputSanitiser()


def git_status(repo: str) -> str:
    """Get the working tree status of a repository.

    Args:
        repo: Repository name (must be within allowed repo root).

    Returns:
        Git status output.
    """
    safe_repo = _sanitiser.validate_repo_path(repo)
    repo_root = os.environ.get("JOL_MCP_GIT_REPO_ROOT", "/repos")
    repo_path = os.path.join(repo_root, safe_repo)

    if not os.path.isdir(repo_path):
        return f"Error: Repository '{safe_repo}' not found."

    result = subprocess.run(  # noqa: S603
        ["git", "status", "--short"],  # noqa: S607
        cwd=repo_path,
        capture_output=True,
        text=True,
        timeout=30,
    )

    if result.returncode != 0:
        return f"Error: {result.stderr.strip()}"

    output = result.stdout if result.stdout.strip() else "Working tree clean."
    return _output_sanitiser.sanitise(output)
