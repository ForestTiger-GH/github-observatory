from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


DEFAULT_API_VERSION = "2026-03-10"
REST_ROOT = "https://api.github.com"
GRAPHQL_URL = "https://api.github.com/graphql"


class GitHubAPIError(RuntimeError):
    def __init__(self, status: int | None, message: str, url: str, headers: dict[str, str] | None = None):
        super().__init__(f"GitHub API error {status or 'unknown'} for {url}: {message}")
        self.status = status
        self.message = message
        self.url = url
        self.headers = headers or {}


@dataclass
class GitHubResponse:
    data: Any
    headers: dict[str, str]
    status: int


class GitHubClient:
    """Small stdlib-only GitHub REST/GraphQL client for Observatory."""

    def __init__(self, token: str, api_version: str = DEFAULT_API_VERSION, user_agent: str = "github-observatory"):
        if not token:
            raise ValueError("A GitHub token is required")
        self.token = token
        self.api_version = api_version
        self.user_agent = user_agent

    def _headers(self, graphql: bool = False) -> dict[str, str]:
        return {
            "Accept": "application/vnd.github+json" if not graphql else "application/json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": self.api_version,
            "User-Agent": self.user_agent,
        }

    def _request(self, request: urllib.request.Request, retries: int = 3) -> GitHubResponse:
        for attempt in range(retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    raw = response.read()
                    data = json.loads(raw) if raw else None
                    return GitHubResponse(
                        data=data,
                        headers={k.lower(): v for k, v in response.headers.items()},
                        status=response.status,
                    )
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                try:
                    parsed = json.loads(body)
                    message = parsed.get("message", body)
                except json.JSONDecodeError:
                    message = body or str(exc)
                headers = {k.lower(): v for k, v in exc.headers.items()} if exc.headers else {}
                if exc.code in {502, 503, 504} and attempt < retries:
                    time.sleep(2 ** attempt)
                    continue
                raise GitHubAPIError(exc.code, message, request.full_url, headers) from exc
            except urllib.error.URLError as exc:
                if attempt < retries:
                    time.sleep(2 ** attempt)
                    continue
                raise GitHubAPIError(None, str(exc.reason), request.full_url) from exc
        raise AssertionError("unreachable")

    def get(self, path: str, params: dict[str, Any] | None = None) -> GitHubResponse:
        if path.startswith("http://") or path.startswith("https://"):
            url = path
        else:
            url = f"{REST_ROOT}{path}"
        if params:
            query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
            url = f"{url}{'&' if '?' in url else '?'}{query}"
        request = urllib.request.Request(url, headers=self._headers(), method="GET")
        return self._request(request)

    def get_paginated(self, path: str, params: dict[str, Any] | None = None) -> list[Any]:
        params = dict(params or {})
        params.setdefault("per_page", 100)
        page = 1
        items: list[Any] = []
        while True:
            params["page"] = page
            response = self.get(path, params)
            chunk = response.data
            if not isinstance(chunk, list):
                raise GitHubAPIError(response.status, "Expected a list response", path, response.headers)
            items.extend(chunk)
            if len(chunk) < int(params["per_page"]):
                break
            page += 1
        return items

    def graphql(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
        request = urllib.request.Request(
            GRAPHQL_URL,
            data=payload,
            headers={**self._headers(graphql=True), "Content-Type": "application/json"},
            method="POST",
        )
        response = self._request(request)
        if not isinstance(response.data, dict):
            raise GitHubAPIError(response.status, "Unexpected GraphQL response", GRAPHQL_URL, response.headers)
        if response.data.get("errors"):
            message = "; ".join(str(error.get("message", error)) for error in response.data["errors"])
            raise GitHubAPIError(response.status, message, GRAPHQL_URL, response.headers)
        return response.data["data"]
