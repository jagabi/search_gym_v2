"""MCP 도구 계층.

`WebTools`가 서버에 붙어 도구 목록과 실행을 제공한다. 에이전트 루프는 이것만
알면 되고, 서버가 stdio 서브프로세스인지 원격 HTTP인지는 신경 쓰지 않는다.
"""

from __future__ import annotations

import os
import sys
import time
from contextlib import AsyncExitStack
from dataclasses import dataclass
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import get_default_environment, stdio_client

try:  # mcp>=1.20에서 이름이 바뀌었다
    from mcp.client.streamable_http import streamable_http_client
except ImportError:  # pragma: no cover - 구버전 SDK
    from mcp.client.streamable_http import streamablehttp_client as streamable_http_client

from ..paths import PROJECT_ROOT, load_env

__all__ = ["ToolResult", "ToolSpec", "WebTools"]


@dataclass(slots=True)
class ToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]

    def as_openai(self) -> dict[str, Any]:
        """OpenAI 호환 chat.completions의 tools 항목 형태."""
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
    """MCP 웹 도구 세션. `async with`로 쓴다.

    MCP_SERVER_URL이 있으면 그 원격 서버에, 없으면 이 프로세스가 띄우는 stdio
    서버에 붙는다. 어느 쪽이든 도구를 실행하는 주체는 우리 쪽이다.
    """

    def __init__(self, url: str | None = None) -> None:
        load_env()
        self._url = url or os.getenv("MCP_SERVER_URL")
        self._stack = AsyncExitStack()
        self._session: ClientSession | None = None
        self._specs: list[ToolSpec] = []

    async def __aenter__(self) -> WebTools:
        await self._stack.__aenter__()
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
                # env를 지정하면 SDK가 기본 환경을 통째로 대체하므로 위에 덮어쓴다.
                keys = {
                    name: os.environ[name]
                    for name in ("SERPER_API_KEY", "JINA_API_KEY", "SEARCH_REGION", "SEARCH_LANGUAGE")
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
            self._specs = [
                ToolSpec(
                    name=tool.name,
                    description=(tool.description or "").strip(),
                    input_schema=dict(tool.inputSchema or {"type": "object", "properties": {}}),
                )
                for tool in listing.tools
            ]
        except BaseException:
            await self._stack.aclose()
            raise
        return self

    async def __aexit__(self, *exc_info: Any) -> Any:
        self._session = None
        return await self._stack.__aexit__(*exc_info)

    @property
    def specs(self) -> list[ToolSpec]:
        return list(self._specs)

    async def call(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        """도구를 실행한다. 실패는 예외로 터뜨리지 않고 모델에게 돌려줘 복구하게 한다."""
        if self._session is None:
            raise RuntimeError("WebTools를 async with 없이 사용했습니다.")

        started = time.perf_counter()
        try:
            raw = await self._session.call_tool(name, arguments)
        except Exception as exc:
            result = ToolResult(f"tool call failed: {exc!r}", is_error=True)
        else:
            parts = [getattr(b, "text", None) or repr(b) for b in raw.content or []]
            result = ToolResult("\n".join(parts), is_error=bool(raw.isError))
        result.duration_ms = (time.perf_counter() - started) * 1000
        return result
