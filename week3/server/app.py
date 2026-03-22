"""
Shared FastMCP application for local STDIO and remote HTTP deployment.
"""
from __future__ import annotations

import atexit
import json
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from starlette.responses import JSONResponse

from week3.server.tmdb import TMDBClient, TMDBError

_WEEK3_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_WEEK3_ROOT / ".env")

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format="%(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

mcp = FastMCP(
    "tmdb-discovery",
    host="0.0.0.0",
    stateless_http=True,
)
_client: TMDBClient | None = None


def _get_client() -> TMDBClient:
    global _client
    if _client is None:
        _client = TMDBClient()
    return _client


def _shutdown_client() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


atexit.register(_shutdown_client)


def _json_ok(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False)


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "ok", "service": "tmdb-discovery"})


@mcp.tool()
def search_media(query: str, limit: int = 15) -> str:
    """Search movies and TV by keyword via TMDB /search/multi. Returns JSON with key "results" (may be empty)."""
    try:
        lim = max(1, min(int(limit), 50))
        rows = _get_client().search_media(query, limit=lim)
        return _json_ok({"results": rows})
    except TMDBError as e:
        logger.warning("search_media: %s", e)
        return _json_ok({"error": str(e)})
    except (TypeError, ValueError):
        return _json_ok({"error": "Invalid limit; use an integer between 1 and 50."})


@mcp.tool()
def get_recommendations(media_type: str, tmdb_id: int, limit: int = 15) -> str:
    """Given TMDB id and media_type "movie" or "tv", return similar titles (JSON "results")."""
    mt = (media_type or "").strip().lower()
    if mt not in ("movie", "tv"):
        return _json_ok({"error": 'media_type must be "movie" or "tv".'})
    try:
        lim = max(1, min(int(limit), 50))
        rows = _get_client().get_recommendations(mt, int(tmdb_id), limit=lim)  # type: ignore[arg-type]
        return _json_ok({"results": rows})
    except TMDBError as e:
        logger.warning("get_recommendations: %s", e)
        return _json_ok({"error": str(e)})
    except (TypeError, ValueError):
        return _json_ok({"error": "Invalid tmdb_id or limit."})


@mcp.tool()
def trending_media(media_type: str = "movie", window: str = "day", limit: int = 15) -> str:
    """Trending movies or TV (TMDB /trending/{movie|tv}/{day|week}). Returns JSON "results"."""
    mt = (media_type or "").strip().lower()
    w = (window or "").strip().lower()
    if mt not in ("movie", "tv"):
        return _json_ok({"error": 'media_type must be "movie" or "tv".'})
    if w not in ("day", "week"):
        return _json_ok({"error": 'window must be "day" or "week".'})
    try:
        lim = max(1, min(int(limit), 50))
        rows = _get_client().trending_media(mt, window=w, limit=lim)  # type: ignore[arg-type]
        return _json_ok({"results": rows})
    except TMDBError as e:
        logger.warning("trending_media: %s", e)
        return _json_ok({"error": str(e)})
    except (TypeError, ValueError):
        return _json_ok({"error": "Invalid limit; use an integer between 1 and 50."})
