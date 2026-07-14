"""MCP Inspector smoke test via subprocess."""

from __future__ import annotations

import subprocess
import sys

import pytest


@pytest.mark.skip(reason="Requires MCP Inspector CLI and running server instances")
class TestMCPInspector:
    """Smoke tests using MCP Inspector to verify server compliance."""

    SERVERS = [
        "jol-git-server",
        "jol-jira-server",
        "jol-compliance-server",
        "jol-docs-server",
    ]

    @pytest.mark.parametrize("server", SERVERS)
    def test_server_starts_and_responds(self, server):
        """Each server should start and respond to MCP initialize."""
        server_path = f"servers/{server}/server.py"
        proc = subprocess.Popen(
            [sys.executable, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        try:
            # Send MCP initialize request (JSON-RPC)
            init_request = (
                '{"jsonrpc": "2.0", "id": 1, "method": "initialize", '
                '"params": {"protocolVersion": "2024-11-05", "capabilities": {}, '
                '"clientInfo": {"name": "test", "version": "0.1.0"}}}\n'
            )
            proc.stdin.write(init_request)
            proc.stdin.flush()

            # Read response with timeout
            response = proc.stdout.readline()
            assert '"jsonrpc": "2.0"' in response or '"jsonrpc":"2.0"' in response
        finally:
            proc.terminate()
            proc.wait(timeout=5)

    @pytest.mark.parametrize("server", SERVERS)
    def test_server_lists_tools(self, server):
        """Each server should list its tools via tools/list."""
        server_path = f"servers/{server}/server.py"
        proc = subprocess.Popen(
            [sys.executable, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        try:
            # Initialize first
            init_request = (
                '{"jsonrpc": "2.0", "id": 1, "method": "initialize", '
                '"params": {"protocolVersion": "2024-11-05", "capabilities": {}, '
                '"clientInfo": {"name": "test", "version": "0.1.0"}}}\n'
            )
            proc.stdin.write(init_request)
            proc.stdin.flush()
            proc.stdout.readline()  # Consume init response

            # List tools
            list_request = '{"jsonrpc": "2.0", "id": 2, "method": "tools/list"}\n'
            proc.stdin.write(list_request)
            proc.stdin.flush()

            response = proc.stdout.readline()
            assert "tools" in response
        finally:
            proc.terminate()
            proc.wait(timeout=5)
