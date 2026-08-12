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

# FastMCP는 SDK 버전마다 위치가 다르다. 이름이 옮겨 다녀도 서버가 뜨게 둔다.
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:  # pragma: no cover
    try:
        from mcp.server import FastMCP
    except ImportError:
        from fastmcp import FastMCP  # 별도 패키지로 분리된 버전

from ..paths import load_env, require_env

load_env()

SERPER_HOST = "google.serper.dev"
JINA_HOST = "r.jina.ai"
TIMEOUT_S = 30.0

SEARCH_RESULTS = 10

# 페치는 **자르지 않고 날것 그대로** 돌려준다(0 = 무제한).
#
# 이 서버는 독립 서브프로세스라 어떤 모델이 떠 있는지 모른다 — 토크나이저가 없으니
# 자 단위로밖에 못 자르고, 그건 부정확할 뿐 아니라 에이전트가 판단하기 전에 정보를
# 버린다. 절단은 모델을 아는 쪽에서 한 번만 한다:
#   agent.refine_max_document_tokens  정제기에 넣을 원문의 토큰 상한
#   agent.context_limit               대화에 들어갈 도구 결과의 토큰 상한
# 덕분에 search_o1.json에는 손대지 않은 원문이 통째로 남는다.
#
# 병적으로 큰 페이지를 막아야 하면 .env의 FETCH_MAX_CHARS로 비상 밸브를 건다.
FETCH_MAX_CHARS = int(os.getenv("FETCH_MAX_CHARS", "0"))

# --- 오염 차단 --------------------------------------------------------------
#
# 실측: gemma-4-12B가 첫 문항에서 huggingface.co/datasets/google/deepsearchqa 를
# 열려고 했다. 벤치마크 자체를 검색해 정답을 긁어오면 점수가 실력이 아니라 유출을
# 측정한다(Search-Time Contamination, arXiv 2606.05241).
#
# 벤치마크 이름만 막는다. 도메인을 통째로 막으면(huggingface.co 등) 정당한 자료
# 조회까지 죽는다 — 실제로 OWID 데이터가 HF datasets에 미러돼 있는 경우가 있다.
BLOCKED_TERMS = tuple(
    t.strip().lower()
    for t in os.getenv(
        "BLOCKED_TERMS", "deepsearchqa,browsecomp,evobrowsecomp,kbrowsecomp,dsqa-full"
    ).split(",")
    if t.strip()
)
BLOCK_NOTICE = (
    "BLOCKED: this points at the evaluation benchmark itself, not at a source for the "
    "question. Find the underlying facts from a primary source instead."
)

mcp = FastMCP("web")


def _blocked(text: str) -> str | None:
    """차단 대상이면 걸린 표현을 돌려준다."""
    lowered = (text or "").lower()
    return next((term for term in BLOCKED_TERMS if term in lowered), None)


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

    # 벤치마크 자체를 가리키는 결과는 목록에서 지운다. 링크를 보여주면 다음 턴에
    # 그걸 fetch하려 들고, 그 시도가 궤적을 오염시킨다.
    organic, blocked = [], 0
    for item in data.get("organic", []):
        picked = _pick(item, "title", "link", "snippet", "date")
        if _blocked(f"{picked.get('title', '')} {picked.get('link', '')}"):
            blocked += 1
            continue
        organic.append(picked)
    result["organic"] = organic
    if blocked:
        result["filtered_results"] = f"{blocked} result(s) removed: {BLOCK_NOTICE}"

    if related := data.get("relatedSearches"):
        result["related_searches"] = [r["query"] for r in related if r.get("query")]
    return json.dumps(result, ensure_ascii=False)


def fetch(url: str) -> str:
    """Jina Reader로 본문만 마크다운으로 받는다."""
    if term := _blocked(url):
        raise RuntimeError(f"{BLOCK_NOTICE} (matched: {term})")
    headers = {"X-Return-Format": "markdown"}
    if key := os.getenv("JINA_API_KEY"):
        headers["Authorization"] = f"Bearer {key}"
    # Jina Reader는 읽을 주소를 경로에 그대로 이어 붙인다.
    text = _request(JINA_HOST, "GET", f"/{url}", headers)
    if FETCH_MAX_CHARS and len(text) > FETCH_MAX_CHARS:
        return text[:FETCH_MAX_CHARS] + f"\n\n... (비상 밸브: {FETCH_MAX_CHARS:,}자에서 잘림)"
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
