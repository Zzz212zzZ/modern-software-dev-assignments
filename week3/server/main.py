"""
Local STDIO entrypoint for the TMDB MCP server.
"""
from __future__ import annotations

from week3.server.app import mcp


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()