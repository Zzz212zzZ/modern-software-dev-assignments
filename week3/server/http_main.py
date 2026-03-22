"""
Remote HTTP entrypoint for local ASGI testing and cloud deployment.
"""
from __future__ import annotations

import uvicorn

from week3.server.app import mcp

app = mcp.streamable_http_app()


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
