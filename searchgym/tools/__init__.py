"""MCP 도구 계층.

`WebTools` 가 서버에 붙어 도구 목록과 실행을 제공한다. 에이전트 루프는 이것만
알면 되고, 서버가 stdio 서브프로세스인지 원격 HTTP인지는 신경 쓰지 않는다.

세 방법이 이 계층을 다르게 쓴다.

    ragent       모델에게 web_search + web_fetch 를 그대로 노출한다
    search-o1    모델에게 web_search 만 노출하고, 상위 k개 페치는 우리가 한다
    depthsearch  같되, explorer 가 fetch 를 재귀적으로 더 부른다

자동 페치를 서버가 아니라 여기서 하는 이유는 두 가지다 — 서버는 어떤 모델이 떠
있는지 모르고, 검색 결과에서 벤치마크 유출을 걷어낸 **뒤에** 열 URL 을 골라야
한다.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import sys
import time
import httpx
from contextlib import AsyncExitStack
from dataclasses import dataclass
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import get_default_environment, stdio_client

try:  # mcp>=1.20에서 이름이 바뀌었다
    from mcp.client.streamable_http import streamable_http_client
except ImportError:  # pragma: no cover - 구버전 SDK
    from mcp.client.streamable_http import streamablehttp_client as streamable_http_client

from ..explorer import Document
from ..paths import PROJECT_ROOT, load_env
from ..urls import normalize_fetch_url, reader_failure
from ..local_reader import local_reader_url

__all__ = ["ToolResult", "ToolSpec", "WebTools"]

_EMPTY: dict[str, Any] = {"type": "object", "properties": {}}


def _field(obj: Any, *names: str) -> Any:
    """SDK 버전마다 필드 이름이 camelCase / snake_case 로 갈린다.

    mcp 2.x 에서 `Tool.inputSchema` -> `input_schema`,
    `CallToolResult.isError` -> `is_error` 로 바뀌었다. 어느 쪽이든 읽는다.
    """
    for name in names:
        value = getattr(obj, name, None)
        if value is not None:
            return value
    return None


@dataclass(slots=True)
class ToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]

    def as_openai(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.input_schema,
            },
        }


@dataclass(slots=True)
class ToolResult:
    text: str
    is_error: bool = False
    duration_ms: float = 0.0


class WebTools:
    """MCP 웹 도구 세션. `async with` 로 쓴다."""

    def __init__(self, url: str | None = None, search_results: int = 0) -> None:
        load_env()
        self._url = url or os.getenv("MCP_SERVER_URL")
        # serper 가 돌려줄 결과 수. 서버는 별도 프로세스라 환경변수로만 전달된다.
        # 이걸 안 넘기면 yaml 의 agent.search_results 가 조용히 무시된다.
        if search_results:
            os.environ["SEARCH_RESULTS"] = str(search_results)
        self._stack = AsyncExitStack()
        self._session: ClientSession | None = None
        self._specs: list[ToolSpec] = []
        self.reader_status: dict[str, Any] = {}
        self._reader_http = None
        # Shared by all concurrent questions in this Runner/MCP session.
        self._fetch_slots = asyncio.Semaphore(max(1, int(os.getenv("JINA_MAX_CONCURRENT", "50"))))

    async def __aenter__(self) -> WebTools:
        await self._stack.__aenter__()
        self._reader_http = await self._stack.enter_async_context(httpx.AsyncClient(
            timeout=float(os.getenv("JINA_TIMEOUT_S", "60")), trust_env=False))
        try:
            if self._url:
                headers = {}
                if token := os.getenv("MCP_AUTH_TOKEN"):
                    headers["Authorization"] = f"Bearer {token}"
                # SDK 버전에 따라 2-튜플이거나 (get_session_id를 포함한) 3-튜플이다.
                transport = await self._stack.enter_async_context(
                    streamable_http_client(self._url, headers=headers or None)
                )
                read, write = transport[0], transport[1]
            else:
                # Do not start a subprocess with an implicit hosted fallback.
                local_reader_url(os.getenv("JINA_BASE_URL", ""))
                # env를 지정하면 SDK가 기본 환경을 통째로 대체하므로 위에 덮어쓴다.
                keys = {
                    name: os.environ[name]
                    for name in (
                        "SERPER_API_KEY", "JINA_API_KEY",
                        "SEARCH_REGION", "SEARCH_LANGUAGE", "SEARCH_RESULTS",
                        "FETCH_MAX_CHARS", "BLOCKED_TERMS",
                        "JINA_RETURN_FORMAT", "JINA_WITH_LINKS",
                        "JINA_WITH_IMAGES", "JINA_ENGINE",
                        "JINA_BASE_URL", "JINA_RPM", "JINA_MAX_CONCURRENT", "JINA_TIMEOUT_S", "JINA_RETRIES",
                    )
                    if os.getenv(name)
                }
                params = StdioServerParameters(
                    command=sys.executable,
                    args=["-m", "searchgym.tools.server"],
                    env={**get_default_environment(), **keys},
                    cwd=str(PROJECT_ROOT),
                )
                read, write = await self._stack.enter_async_context(stdio_client(params))

            session = await self._stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
            self._session = session

            listing = await session.list_tools()
            if "local_reader_status" not in {tool.name for tool in listing.tools}:
                raise RuntimeError("Run blocked: fetch server lacks the local Jina preflight. Update/restart the MCP server.")
            await self._check_local_reader()
            self._specs = [
                ToolSpec(
                    name=tool.name,
                    description=(tool.description or "").strip(),
                    input_schema=dict(_field(tool, "inputSchema", "input_schema") or _EMPTY),
                )
                for tool in listing.tools
                if tool.name != "local_reader_status"
            ]
        except BaseException:
            await self._stack.aclose()
            raise
        return self

    async def _check_local_reader(self) -> None:
        try:
            result = await asyncio.wait_for(self.call("local_reader_status", {}), timeout=15)
            if result.is_error:
                raise ValueError(result.text)
            status = json.loads(result.text)
            if not isinstance(status, dict) or status.get("ready") is not True:
                raise ValueError("fetch server did not confirm readiness")
            status["jina_base_url"] = local_reader_url(status.get("jina_base_url", ""))
            if status.get("verified_by") != "fetch_server":
                raise ValueError("missing fetch-server verification")
        except (RuntimeError, ValueError, TypeError, asyncio.TimeoutError) as exc:
            raise RuntimeError(f"Local Jina preflight failed; benchmark blocked: {exc}") from exc
        self.reader_status = status
        print(f"Local Jina ready: {status['jina_base_url']} "
              f"(RPM={status.get('jina_rpm')}, concurrency={status.get('jina_max_concurrent')}; fetch-server verified)",
              file=sys.stderr)

    async def __aexit__(self, *exc_info: Any) -> Any:
        self._session = None
        return await self._stack.__aexit__(*exc_info)

    # --- 도구 목록 ----------------------------------------------------------

    @property
    def specs(self) -> list[ToolSpec]:
        return list(self._specs)

    def specs_for(self, names: list[str]) -> list[ToolSpec]:
        """이름으로 걸러 낸 도구 목록. 방법마다 모델에게 주는 도구가 다르다."""
        wanted = {n.lower() for n in names}
        return [spec for spec in self._specs if spec.name.lower() in wanted]

    # --- 실행 ---------------------------------------------------------------

    async def call(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        """도구를 실행한다. 실패는 예외로 터뜨리지 않고 돌려줘 복구하게 한다."""
        if self._session is None:
            raise RuntimeError("WebTools를 async with 없이 사용했습니다.")

        started = time.perf_counter()
        try:
            if name == "web_fetch":
                async with self._fetch_slots:
                    raw = await self._session.call_tool(name, arguments)
            else:
                raw = await self._session.call_tool(name, arguments)
        except Exception as exc:
            result = ToolResult(f"tool call failed: {exc!r}", is_error=True)
        else:
            parts = [getattr(b, "text", None) or repr(b) for b in raw.content or []]
            result = ToolResult(
                "\n".join(parts), is_error=bool(_field(raw, "isError", "is_error"))
            )
        result.duration_ms = (time.perf_counter() - started) * 1000
        return result

    async def search(self, query: str) -> tuple[dict[str, Any], ToolResult]:
        """검색해서 파싱된 결과와 원본을 함께 돌려준다."""
        result = await self.call("web_search", {"query": query})
        if result.is_error:
            return {}, result
        try:
            parsed = json.loads(result.text)
        except (json.JSONDecodeError, TypeError):
            return {}, result
        return (parsed if isinstance(parsed, dict) else {}), result

    async def fetch(self, url: str, *, engine: str | None = None) -> Document:
        """URL 하나를 열어 `Document` 로 돌려준다. explorer 가 이걸 쓴다."""
        try:
            url = normalize_fetch_url(url)
        except ValueError as exc:
            return Document(url=str(url), content=f"Invalid page URL: {exc}", is_error=True)
        blocked_terms = os.getenv("BLOCKED_TERMS", "deepsearchqa,browsecomp,evobrowsecomp,kbrowsecomp,dsqa-full").split(",")
        if any(t.strip().lower() in url.lower() for t in blocked_terms if t.strip()) or "/fb-answers/" in url.lower():
            return Document(url=url, content="BLOCKED: evaluation material or answer-reposting page; find primary facts.", is_error=True)
        if engine is not None:
            return await self._fetch_engine(url, engine)
        from .native import file_kind, fetch_native
        native_error = ""
        if file_kind(url):
            try:
                content = await fetch_native(url)
                return Document(url=url, content=content, retrieval="native")
            except Exception as exc:
                native_error = f"Native document read failed: {type(exc).__name__}: {exc}"
        result = await self.call("web_fetch", {"url": url})
        failure = reader_failure(result.text)
        title = re.search(r"^Title:\s*(.*?)$", result.text, re.MULTILINE)
        return Document(url=url, content=(f"Could not read {url}: {failure}" if failure else result.text),
                        title=title.group(1).strip() if title else "",
                        is_error=result.is_error or bool(failure),
                        retrieval="jina_fallback" if native_error else "jina",
                        retrieval_note=native_error)

    async def _fetch_engine(self, url: str, engine: str) -> Document:
        """Explicit local transport for RawTree; never switch curl to browser silently."""
        if engine not in ("curl", "browser"):
            raise ValueError(f"Unsupported Reader engine: {engine}")
        base = local_reader_url(self.reader_status.get("jina_base_url", ""))
        if self._reader_http is None:
            raise RuntimeError("Reader client is not open")
        headers = {"Accept": "application/json", "X-Engine": engine,
                   "X-Return-Format": "content", "X-Respond-With": "content",
                    "X-With-Links-Summary": "false", "X-No-Cache": "true",
                    "X-Assert-Status-Code": "200"}
        try:
            async with self._fetch_slots:
                response = await self._reader_http.get(f"{base}/{url}", headers=headers)
            response.raise_for_status()
            payload = response.json()
            if payload.get("code") != 200 or not isinstance(payload.get("data"), dict):
                raise ValueError(f"Reader error: {payload}")
            data = payload["data"]
            content = data.get("content")
            if not isinstance(content, str):
                raise ValueError("Reader did not return data.content")
            failure = reader_failure(content)
            return Document(url=url, content=content, title=str(data.get("title") or ""),
                            is_error=bool(failure), retrieval=f"jina_{engine}",
                            retrieval_note=failure or "",
                            reader_metadata={k: data[k] for k in
                                ("url", "title", "status", "statusCode", "httpStatus", "publishedTime") if k in data})
        except (httpx.HTTPError, ValueError, TypeError) as exc:
            return Document(url=url, content=f"Could not read {url}: {exc}",
                            is_error=True, retrieval=f"jina_{engine}")

    async def fetch_many(self, entries: list[dict[str, str]]) -> list[Document]:
        """여러 URL 을 동시에 연다. 실패한 것도 자리를 지킨다.

        `entries` 는 serper 의 organic 항목(`link`/`title`)이다. 순서를 보존해야
        "상위 k개" 라는 말이 의미를 갖는다.
        """
        urls = [str(e.get("link") or "") for e in entries]
        titles = [str(e.get("title") or "") for e in entries]
        gathered = await asyncio.gather(
            *(self.fetch(url) for url in urls if url), return_exceptions=True
        )

        documents: list[Document] = []
        index = 0
        for url, title in zip(urls, titles):
            if not url:
                continue
            outcome = gathered[index]
            index += 1
            if isinstance(outcome, BaseException):
                documents.append(
                    Document(url=url, title=title, content=repr(outcome), is_error=True)
                )
            else:
                outcome.title = title
                documents.append(outcome)
        return documents
