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
import random
import threading
import time
from typing import Any

from anyio import to_thread
from ..urls import normalize_fetch_url

# 서버 클래스는 SDK 버전마다 위치와 **이름**이 다르다. 어느 쪽이든 뜨게 둔다.
#   mcp 1.x        mcp.server.fastmcp.FastMCP
#   mcp 2.x        mcp.server.mcpserver.MCPServer   (FastMCP 에서 개명)
#   fastmcp        별도 패키지로 분리된 버전
# 셋 다 tool() 데코레이터 · run(transport=...) · settings · streamable_http_app() 가
# 같은 모양이라 아래 코드는 그대로 돈다.
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:  # pragma: no cover
    try:
        from mcp.server.mcpserver import MCPServer as FastMCP
    except ImportError:
        try:
            from mcp.server import FastMCP
        except ImportError:
            from fastmcp import FastMCP

from ..paths import load_env, require_env

load_env()

SERPER_HOST = "google.serper.dev"
JINA_HOST = "r.jina.ai"
TIMEOUT_S = 30.0

SEARCH_RESULTS = int(os.getenv("SEARCH_RESULTS", "10"))

# 페치는 **자르지 않고 날것 그대로** 돌려준다(0 = 무제한).
#
# 이 서버는 독립 서브프로세스라 어떤 모델이 떠 있는지 모른다 — 토크나이저가 없으니
# 자 단위로밖에 못 자르고, 그건 부정확할 뿐 아니라 에이전트가 판단하기 전에 정보를
# 버린다. 절단은 모델을 아는 쪽에서 한 번만 한다:
#   explorer.max_document_tokens  explorer 에 넣을 문서 묶음의 토큰 상한
#   agent.context_limit           대화에 들어갈 도구 결과의 토큰 상한
# 덕분에 explorer.json 에는 손대지 않은 원문이 통째로 남는다.
#
# 병적으로 큰 페이지를 막아야 하면 .env의 FETCH_MAX_CHARS로 비상 밸브를 건다.
FETCH_MAX_CHARS = int(os.getenv("FETCH_MAX_CHARS", "0"))

# 페치 재시도 횟수. 429(속도 초과)와 5xx 는 기다렸다 다시 보내면 대개 지나간다.
# 실패를 모델에게 돌려주면 모델이 같은 페이지를 다른 주소로 바꿔가며 재시도하다
# 턴과 검색 예산을 태운다 — 재시도는 여기서 조용히 처리하는 쪽이 훨씬 싸다.
JINA_RETRIES = int(os.getenv("JINA_RETRIES", "4"))
# Serper 도 같은 처방. 여기는 아직 한도에 닿은 적이 없어 재시도만 둔다.
SERPER_RETRIES = int(os.getenv("SERPER_RETRIES", "3"))

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


# 다시 보내면 지나갈 수 있는 응답. 429 는 속도 초과, 5xx 는 상대 서버 사정이다.
_RETRY_STATUS = frozenset({429, 500, 502, 503, 504})
# 다시 보내도 절대 지나가지 않는 것. 조용히 재시도하면 원인이 가려진다.
_FATAL_STATUS = {
    401: "the Jina API key was rejected.",
    402: (
        "the Jina account has no balance left."
    ),
    403: "access was refused.",
    # Serper 크레딧 소진이 400 으로 온다. 재시도해도 소용없고, 조용히 실패로 넘기면
    # 모델에게는 "Error executing tool" 만 가서 원인이 완전히 가려진다(실측: 검색의
    # 47% 가 이렇게 죽는 동안 지표에는 아무것도 안 나타났다).
    400: "the request was refused — check the API key's remaining credits.",
}


class _Pacer:
    """요청을 분당 N회로 **고르게 벌려** 보낸다. 스레드 안전.

    평균만 맞춰도 부족하다 — 실측에서 평균 분당 11회인데도 429 가 41건 났다.
    `workers` 개의 문항이 동시에 페치를 던지고 search-o1 은 검색 한 번에 5개를
    한꺼번에 던지므로, 평균은 한도 아래인데 순간 burst 가 한도를 넘는다. 그래서
    개수를 세는 대신 **다음 요청 시각을 예약**해 간격 자체를 만든다.

    이렇게 하면 workers 를 낮추지 않고도 한도를 지킬 수 있다. 병렬은 GPU 쪽에서
    필요한 것이고, 페치 속도와는 별개로 두어야 한다.
    """

    def __init__(self, per_minute: int) -> None:
        self.interval = 60.0 / max(1, per_minute)
        self._lock = threading.Lock()
        self._next = 0.0

    def acquire(self) -> None:
        with self._lock:
            now = time.monotonic()
            start = self._next if self._next > now else now
            self._next = start + self.interval
        if (delay := start - now) > 0:
            time.sleep(delay)

    def penalise(self, seconds: float) -> None:
        """429 를 받았으면 그만큼 전체를 뒤로 민다. 다른 스레드도 같이 쉰다."""
        with self._lock:
            self._next = max(self._next, time.monotonic() + max(0.0, seconds))


_pacer_lock = threading.Lock()
_pacer: _Pacer | None = None


def _jina_pacer() -> _Pacer:
    """Jina 전용 페이서. 키가 있으면 한도가 훨씬 높다.

    `JINA_RPM` 으로 직접 줄 수 있다. 비워 두면 키 유무로 정한다 — 무료 티어는
    분당 20회라 18로 여유를 두고, 키가 있으면 유료 한도에 맞춰 올린다.
    """
    global _pacer
    with _pacer_lock:
        if _pacer is None:
            raw = os.getenv("JINA_RPM", "").strip()
            rpm = int(raw) if raw.isdigit() and int(raw) > 0 else (
                180 if os.getenv("JINA_API_KEY") else 18
            )
            _pacer = _Pacer(rpm)
        return _pacer


def _request(
    host: str,
    method: str,
    path: str,
    headers: dict[str, str],
    body: str | None = None,
    *,
    pacer: _Pacer | None = None,
    retries: int = 0,
) -> str:
    """HTTP 한 번. `pacer` 가 있으면 속도를 맞추고, 재시도 가능한 응답은 다시 보낸다."""
    for attempt in range(retries + 1):
        if pacer is not None:
            pacer.acquire()
        conn = http.client.HTTPSConnection(host, timeout=TIMEOUT_S)
        try:
            conn.request(method, path, body, headers)
            response = conn.getresponse()
            payload = response.read().decode("utf-8", errors="replace")
            status = response.status
            retry_after = response.getheader("Retry-After") or ""
        finally:
            conn.close()

        if status == 200:
            return payload
        if note := _FATAL_STATUS.get(status):
            raise RuntimeError(f"{host} failed (HTTP {status}): {note}")
        if status in _RETRY_STATUS and attempt < retries:
            # Retry-After 를 주면 그대로 따르고, 없으면 지수 백오프 + 지터.
            try:
                wait = float(retry_after)
            except ValueError:
                wait = min(30.0, 2.0**attempt) + random.uniform(0, 0.5)
            if status == 429 and pacer is not None:
                pacer.penalise(wait)
            time.sleep(wait)
            continue
        raise RuntimeError(f"{host}{path} failed (HTTP {status}): {payload[:300]}")
    raise RuntimeError(f"{host}{path} failed after {retries} retries")


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
            retries=SERPER_RETRIES,
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
    for item in data.get("organic", [])[:SEARCH_RESULTS]:
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


# --- Jina Reader 옵션 --------------------------------------------------------
#
# 전부 .env 로 바꿀 수 있다. tests/fetch.py 가 이 값들을 바꿔 가며 부른다.
#
#   JINA_RETURN_FORMAT   markdown | text | html   (기본 markdown)
#   JINA_WITH_LINKS      1 이면 본문 끝에 페이지의 링크 목록을 붙인다.
#                        **depthsearch 는 이게 켜져 있어야 확장할 URL 을 볼 수 있다.**
#                        대신 링크가 많은 페이지에서는 정제기의 문서 예산을 크게 먹는다.
#   JINA_WITH_IMAGES     1 이면 이미지 목록도 붙인다. 보통 필요 없다.
#   JINA_ENGINE          browser | direct   (비우면 Jina 기본값)
JINA_RETURN_FORMAT = os.getenv("JINA_RETURN_FORMAT", "markdown")
JINA_WITH_LINKS = os.getenv("JINA_WITH_LINKS", "0") not in ("", "0", "false", "False")
JINA_WITH_IMAGES = os.getenv("JINA_WITH_IMAGES", "0") not in ("", "0", "false", "False")
JINA_ENGINE = os.getenv("JINA_ENGINE", "")


def fetch(url: str) -> str:
    """Jina Reader로 본문만 마크다운으로 받는다."""
    url = normalize_fetch_url(url)
    if term := _blocked(url):
        raise RuntimeError(f"{BLOCK_NOTICE} (matched: {term})")
    headers = {"X-Return-Format": JINA_RETURN_FORMAT}
    if JINA_WITH_LINKS:
        headers["X-With-Links-Summary"] = "true"
    if JINA_WITH_IMAGES:
        headers["X-With-Images-Summary"] = "true"
    if JINA_ENGINE:
        headers["X-Engine"] = JINA_ENGINE
    if key := os.getenv("JINA_API_KEY"):
        headers["Authorization"] = f"Bearer {key}"
    # Jina Reader는 읽을 주소를 경로에 그대로 이어 붙인다.
    # 페이서와 재시도를 여기서 건다 — 모든 페치가 지나가는 단일 관문이라, 속도
    # 제한을 지키는 자리도 여기 하나뿐이면 된다.
    #
    # **실패 메시지에 리더의 주소를 노출하지 않는다.** 에러는 도구 결과로 모델에게
    # 그대로 가는데, 거기에 "r.jina.ai/http://example.com/x failed" 가 찍히면 모델이
    # 그것을 열어야 할 주소로 읽고 다시 요청한다. 그러면 r.jina.ai/r.jina.ai/... 가
    # 되고 또 실패하며 오염이 커진다(실측: 한 판에서 프로토콜이 두 번 겹친 주소까지
    # 나왔다). 모델에게는 **자기가 요청한 주소**만 보여 준다.
    try:
        text = _request(
            JINA_HOST, "GET", f"/{url}", headers,
            pacer=_jina_pacer(), retries=JINA_RETRIES,
        )
    except RuntimeError as exc:
        detail = str(exc).split(": ", 1)[-1]
        raise RuntimeError(f"could not read {url}: {detail}") from None
    if FETCH_MAX_CHARS and len(text) > FETCH_MAX_CHARS:
        return text[:FETCH_MAX_CHARS] + f"\n\n... (truncated at {FETCH_MAX_CHARS:,} chars)"
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
