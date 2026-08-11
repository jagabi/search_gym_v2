"""웹 검색과 페이지 읽기를 MCP 도구로 노출하는 서버.

    web_search  Serper (google.serper.dev)
    web_fetch   Jina Reader (r.jina.ai)

    python -m searchgym.tools.server                                # stdio
    python -m searchgym.tools.server --transport streamable-http    # 원격

도구를 실행하는 주체가 벤더가 아니라 이 프로세스이므로, 어떤 모델을 쓰든 질의와
결과가 같은 형태로 남는다. 검색 예산 상한은 여기가 아니라 에이전트 루프에서 건다
(모델별로 다르게 주고 싶기 때문이다).
"""

from __future__ import annotations

import argparse
import http.client
import json
import os
from typing import Any

from anyio import to_thread
from mcp.server.fastmcp import FastMCP

from ..paths import load_env, require_env

load_env()

SERPER_HOST = "google.serper.dev"
JINA_HOST = "r.jina.ai"
TIMEOUT_S = 30.0

SEARCH_RESULTS = 10
FETCH_MAX_CHARS = 20_000

mcp = FastMCP("web")


def _request(host: str, method: str, path: str, headers: dict[str, str], body: str | None = None) -> str:
    conn = http.client.HTTPSConnection(host, timeout=TIMEOUT_S)
    try:
        conn.request(method, path, body, headers)
        response = conn.getresponse()
        payload = response.read().decode("utf-8", errors="replace")
    finally:
        conn.close()
    if response.status != 200:
        raise RuntimeError(f"{host}{path} 실패 (HTTP {response.status}): {payload[:300]}")
    return payload


def _pick(source: dict[str, Any], *keys: str) -> dict[str, Any]:
    return {key: source[key] for key in keys if source.get(key)}


def search(query: str, gl: str = "", hl: str = "") -> str:
    """Serper 호출. gl/hl은 지역·언어 코드로, 한국어 벤치마크에서 반드시 넘겨야 한다."""
    payload = json.dumps(
        {
            "q": query,
            "num": SEARCH_RESULTS,
            "gl": gl or os.getenv("SEARCH_REGION", "us"),
            "hl": hl or os.getenv("SEARCH_LANGUAGE", "en"),
        }
    )
    data = json.loads(
        _request(
            SERPER_HOST,
            "POST",
            "/search",
            {"X-API-KEY": require_env("SERPER_API_KEY"), "Content-Type": "application/json"},
            payload,
        )
    )

    result: dict[str, Any] = {}
    if box := data.get("answerBox"):
        result["answer_box"] = _pick(box, "title", "answer", "snippet", "link")
    if graph := data.get("knowledgeGraph"):
        result["knowledge_graph"] = _pick(graph, "title", "type", "description", "website")
    result["organic"] = [
        _pick(item, "title", "link", "snippet", "date") for item in data.get("organic", [])
    ]
    if related := data.get("relatedSearches"):
        result["related_searches"] = [r["query"] for r in related if r.get("query")]
    return json.dumps(result, ensure_ascii=False)


def fetch(url: str) -> str:
    """Jina Reader로 본문만 마크다운으로 받는다."""
    headers = {"X-Return-Format": "markdown"}
    if key := os.getenv("JINA_API_KEY"):
        headers["Authorization"] = f"Bearer {key}"
    # Jina Reader는 읽을 주소를 경로에 그대로 이어 붙인다.
    text = _request(JINA_HOST, "GET", f"/{url}", headers)
    if len(text) > FETCH_MAX_CHARS:
        return text[:FETCH_MAX_CHARS] + f"\n\n... (본문이 길어 {FETCH_MAX_CHARS}자에서 잘렸습니다)"
    return text


@mcp.tool()
async def web_search(query: str) -> str:
    """Search the web and return the top results as JSON.

    Returns an answer box and knowledge graph when available, plus organic results
    with title, link, snippet and date. Use this to find pages; use web_fetch
    afterwards to read one in full.

    Args:
        query: The search query. Short keyword queries work best.
    """
    return await to_thread.run_sync(lambda: search(query))


@mcp.tool()
async def web_fetch(url: str) -> str:
    """Fetch a web page and return its main content as markdown.

    Navigation and ads are stripped; very long pages are truncated. Use this to read
    a page found through web_search — snippets rarely contain the exact figure, date
    or title you need.

    Args:
        url: Absolute URL of the page to read, including the scheme.
    """
    return await to_thread.run_sync(lambda: fetch(url))


def main() -> None:
    parser = argparse.ArgumentParser(description="웹 검색/읽기 MCP 서버")
    parser.add_argument("--transport", choices=["stdio", "streamable-http"], default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=int(os.getenv("MCP_PORT", "8100")))
    args = parser.parse_args()

    if args.transport == "stdio":
        mcp.run(transport="stdio")
        return

    import uvicorn

    mcp.settings.host, mcp.settings.port = args.host, args.port
    uvicorn.run(mcp.streamable_http_app(), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
