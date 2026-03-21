from __future__ import annotations

import logging
import os
import time
from typing import Any, Literal

import httpx

logger = logging.getLogger(__name__)

BASE_URL = "https://api.themoviedb.org/3"
DEFAULT_TIMEOUT = 15.0
OVERVIEW_MAX_LEN = 200
MAX_ITEMS_DEFAULT = 15


class TMDBError(Exception):
    """Raised when TMDB returns an error or the response cannot be used."""


class TMDBClient:
    def __init__(
        self,
        api_key: str | None = None,
        *,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        key = api_key or os.environ.get("TMDB_API_KEY")
        if not key or not str(key).strip():
            raise TMDBError(
                "Missing TMDB_API_KEY. Set it in week3/.env (loaded by main) or in the environment."
            )
        self._api_key = str(key).strip()
        self._client = httpx.Client(base_url=BASE_URL, timeout=timeout)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> TMDBClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _request(self, method: str, path: str, *, params: dict[str, Any] | None = None) -> Any:
        merged: dict[str, Any] = {"api_key": self._api_key}
        if params:
            merged.update(params)

        def do_request() -> httpx.Response:
            return self._client.request(method, path, params=merged)

        try:
            response = do_request()
        except httpx.TimeoutException as e:
            logger.warning("TMDB timeout: %s %s", method, path)
            raise TMDBError("TMDB request timed out. Try again later.") from e
        except httpx.RequestError as e:
            logger.warning("TMDB connection error: %s", e)
            raise TMDBError("Could not reach TMDB. Check your network connection.") from e

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            wait = float(retry_after) if retry_after and retry_after.isdigit() else 1.0
            wait = min(max(wait, 0.5), 5.0)
            logger.warning("TMDB rate limited (429), retrying after %.1fs", wait)
            time.sleep(wait)
            try:
                response = do_request()
            except (httpx.TimeoutException, httpx.RequestError) as e:
                raise TMDBError("TMDB rate limited and retry failed.") from e

        if response.status_code >= 400:
            logger.warning(
                "TMDB HTTP %s for %s %s: %s",
                response.status_code,
                method,
                path,
                response.text[:500],
            )
            raise TMDBError(f"TMDB error (HTTP {response.status_code}).")

        try:
            return response.json()
        except ValueError as e:
            raise TMDBError("TMDB returned invalid JSON.") from e

    @staticmethod
    def _trim_overview(text: str | None) -> str | None:
        if not text:
            return None
        text = text.strip()
        if len(text) <= OVERVIEW_MAX_LEN:
            return text
        return text[: OVERVIEW_MAX_LEN - 3].rstrip() + "..."

    def _normalize_multi_item(self, raw: dict[str, Any]) -> dict[str, Any] | None:
        mtype = raw.get("media_type")
        if mtype not in ("movie", "tv"):
            return None
        title = raw.get("title") if mtype == "movie" else raw.get("name")
        date = raw.get("release_date") if mtype == "movie" else raw.get("first_air_date")
        return {
            "id": raw.get("id"),
            "media_type": mtype,
            "title": title,
            "release_or_first_air_date": date,
            "vote_average": raw.get("vote_average"),
            "overview": self._trim_overview(raw.get("overview")),
        }

    def search_media(self, query: str, *, limit: int = MAX_ITEMS_DEFAULT) -> list[dict[str, Any]]:
        q = (query or "").strip()
        if not q:
            return []

        data = self._request("GET", "/search/multi", params={"query": q})
        results = data.get("results") or []
        out: list[dict[str, Any]] = []
        for item in results:
            if not isinstance(item, dict):
                continue
            norm = self._normalize_multi_item(item)
            if norm and norm.get("id") is not None:
                out.append(norm)
            if len(out) >= limit:
                break
        return out

    def get_recommendations(
        self,
        media_type: Literal["movie", "tv"],
        tmdb_id: int,
        *,
        limit: int = MAX_ITEMS_DEFAULT,
    ) -> list[dict[str, Any]]:
        if tmdb_id <= 0:
            raise TMDBError("tmdb_id must be a positive integer.")

        path = f"/{media_type}/{tmdb_id}/recommendations"
        data = self._request("GET", path)
        results = data.get("results") or []
        out: list[dict[str, Any]] = []
        for raw in results:
            if not isinstance(raw, dict):
                continue
            title = raw.get("title") if media_type == "movie" else raw.get("name")
            date = raw.get("release_date") if media_type == "movie" else raw.get("first_air_date")
            out.append(
                {
                    "id": raw.get("id"),
                    "media_type": media_type,
                    "title": title,
                    "release_or_first_air_date": date,
                    "vote_average": raw.get("vote_average"),
                    "overview": self._trim_overview(raw.get("overview")),
                }
            )
            if len(out) >= limit:
                break
        return out

    def trending_media(
        self,
        media_type: Literal["movie", "tv"] = "movie",
        *,
        window: Literal["day", "week"] = "day",
        limit: int = MAX_ITEMS_DEFAULT,
    ) -> list[dict[str, Any]]:
        path = f"/trending/{media_type}/{window}"
        data = self._request("GET", path)
        results = data.get("results") or []
        out: list[dict[str, Any]] = []
        for raw in results:
            if not isinstance(raw, dict):
                continue
            title = raw.get("title") if media_type == "movie" else raw.get("name")
            date = raw.get("release_date") if media_type == "movie" else raw.get("first_air_date")
            out.append(
                {
                    "id": raw.get("id"),
                    "media_type": media_type,
                    "title": title,
                    "release_or_first_air_date": date,
                    "vote_average": raw.get("vote_average"),
                    "overview": self._trim_overview(raw.get("overview")),
                }
            )
            if len(out) >= limit:
                break
        return out