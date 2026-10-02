"""Explorer — 페치한 문서를 읽고 요약해 위로 올린다. 필요하면 재귀한다.

`max_depth == 1` 이면 Search-o1 의 Reason-in-Documents 그대로다. 받은 문서를 읽고
요약만 돌려준다.

`max_depth > 1` 이면 explorer 가 **자기가 읽은 페이지의 링크를 직접 연다**.
URL 이 요약을 거쳐 위로 올라갔다가 다시 내려오지 않으므로 손상되지 않고, 각
explorer 의 컨텍스트에는 자기 페이지와 자식 요약만 남으므로 어디서도 컨텍스트가
폭발하지 않는다.

    depthsearch  gate 가 검색 결과를 보고 고른 페이지 하나
                   └→ explorer(depth 1)
                        ├→ web_fetch → explorer(depth 2)
                        │                └→ explorer(depth 3)
                        └→ 요약만 gate 로

    search-o1    검색당 상위 k개를 자동 페치해 페이지마다 explorer가 읽는다

현재 DS는 부모 노트의 첫 실행 가능한 Next link를 중복 선택 호출 없이 실행한다.
자식 반환 후에는 부모가 다시 판단한다. 링크별 목적 또는 직전 선택 이유를 탐색에 전달한다.
추출에는 원 질문·현재 원문만 전달한다. 이전 모드는 부모 reasoning을 사용한다.
tool call 인자는 url 하나이며 별도 자유 텍스트 인자를 추가하지 않는다.

제약은 **프롬프트가 아니라 구조**로 건다.
    깊이 상한 도달   →  fetch 도구를 아예 주지 않는다
    예산 소진        →  fetch 도구를 아예 주지 않는다
    이미 읽은 URL    →  완료된 노트 재사용, 진행 중인 조상의 재진입은 차단
explorer 는 매번 새 세션이라 "쓰던 도구를 뺏기는" 혼란이 없다. 그래서 메인
에이전트(대화 도중이라 안내를 돌려주는 쪽이 안전하다)와 처방이 다르다.
"""

from __future__ import annotations

import json
import hashlib
import re
import time
from types import SimpleNamespace
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse, urlsplit, urlunsplit

from .llm import LLM, Usage, recover_tool_calls, normalize_tool_names, history_tool_call
from .trace import Trace
from .urls import normalize_fetch_url

__all__ = [
    "Budget",
    "Document",
    "Explorer",
    "ExplorerConfig",
    "ExplorerResult",
    "FETCH_TOOL",
]

STATUSES = ("answered", "partial", "not_found")

# 인자는 url 하나뿐이다. 자유 텍스트 인자(goal 등)를 붙이면 모델이 형식을 흘려
# 툴콜 파싱이 깨지는 일이 잦고, 그 정보는 어차피 이 턴의 reasoning 에 다 들어 있다.
# 현재 DS는 부모 노트에서 URL별 목적을 찾아 탐색 문맥으로 전달한다(_open 참고).
FETCH_TOOL: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "web_fetch",
        "description": (
            "Open one more page and have it read for you.\n"
            "\n"
            "You can reach two kinds of address: a link printed on the page in front "
            "of you, and any page on a site you are already reading. Working out a "
            "sister page from the pattern of the ones you have seen is fine — if "
            "/archive/1660/12/ and /archive/1661/12/ exist, /archive/1666/12/ is a "
            "reasonable thing to try.\n"
            "\n"
            "This is not a search engine. A query URL for a search site, or a page on "
            "some site you have not been reading, is rejected without opening "
            "anything, and retrying a variant of it will fail the same way.\n"
            "\n"
            "Worth doing when this page says where the answer is without saying the "
            "answer — a footnote, a reference, an index entry, a linked record — or "
            "when the same answer has to be checked across a series of pages. If "
            "there is nothing like that here, report what you found instead."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": (
                        "Absolute URL. Either copy a link from the page text above "
                        "character for character, or give another address on a site "
                        "you are already reading. An address on any other site is "
                        "rejected."
                    ),
                },
            },
            "required": ["url"],
        },
    },
}


@dataclass(slots=True)
class ExplorerConfig:
    # 1 = 재귀 없음 (= Search-o1). N = depth N 까지 판다.
    max_depth: int = 1
    # 문항 하나가 쓸 수 있는 **depth 2 이상** 노드의 총량. depth 1 페치는 두 조건에
    # 똑같이 있으므로 세지 않는다 — 세면 두 조건의 행동 자체가 달라진다.
    max_expansion_nodes: int = 0
    # explorer 하나가 열 수 있는 자식 수. 한 서브트리가 예산을 독식하는 것을 막는다.
    max_subtree_children: int = 0
    # explorer 하나의 턴 상한. 없으면 링크를 계속 씹는다.
    max_turns: int = 1
    max_tokens: int = 32768
    # 이 explorer 에게 넘길 문서 묶음 **전체**의 토큰 상한.
    max_document_tokens: int = 50000
    # explorer 세션 하나의 컨텍스트 상한(자기 페이지 + 자식 요약 누적).
    context_limit: int = 100_000
    # 열 만한 링크를 몇 개까지 목록으로 보여 줄 것인가. 0 이면 목록을 안 붙인다.
    # 본문에 링크가 250~921개씩 흩어져 있어 모델이 훑지 못하는 것이 확장 실패의
    # 원인이라, 질의와 겹치는 순으로 추려서 눈앞에 놓는다(`_link_menu`).
    max_link_menu: int = 30
    # 재귀 탐색 전에 현재 페이지의 근거를 별도 저장한다.
    extract_before_expand: bool = True
    # DepthSearch separates source extraction from navigation context.
    isolate_extraction_context: bool = False
    prune_unhelpful_branches: bool = False
    max_root_nodes: int = 0

    @property
    def recursive(self) -> bool:
        return self.max_depth > 1 and self.max_expansion_nodes > 0


class Budget:
    """문항 하나의 확장 노드 예산. 깎아 쓰고, 0 이 되면 도구를 주지 않는다.

    이미 읽은 URL 도 여기서 같이 기억한다. 중복은 **세 겹**으로 막는다.

        1. 소스에서 제거  읽은 페이지를 가리키는 링크는 문서에서 앵커 텍스트만
                          남기고 지운 뒤 explorer 에게 준다. 고를 수가 없다.
        2. 사후 차단      그래도 URL 을 뱉으면 예산을 쓰지 않고 막는다.
        3. 예산           애초에 열 수 있는 노드 수가 유한하다.

    1번이 핵심이다. 2번만 있을 때는 explorer 가 이미 읽은 링크를 계속 골라
    턴을 태웠다(실측: 5문항에서 중복 시도 22회 > 실제 확장 19회). 모델에게
    "중복하지 마라"고 부탁하는 것보다 선택지에서 없애는 쪽이 확실하다.
    """

    __slots__ = (
        "total", "used", "refused", "visited", "_seen", "hosts",
        "refused_urls", "repeats",
        "duplicates", "links_stripped", "off_page", "same_site", "nodes_by_depth",
        "readings", "reused",
        "content_seen",
        "branch_ceiling",
        "extractions",
    )

    def __init__(self, total: int) -> None:
        self.total = max(0, total)
        self.used = 0
        self.refused = 0
        self.visited: list[str] = []
        self._seen: set[str] = set()
        # 이 문항에서 실제로 읽은 사이트들. 같은 사이트 안의 이동을 허용하는 근거다.
        self.hosts: set[str] = set()
        # 이미 한 번 거절된 URL. explorer 는 매번 새 세션이라 앞 세션이 거절당한
        # 것을 모르고 같은 주소를 다시 집는다(실측: 한 문항에서 같은 위키 문서를
        # 서로 다른 7개 세션이 각각 시도). 거절은 문항 단위로 기억해야 한다.
        self.refused_urls: set[str] = set()
        self.repeats = 0
        self.duplicates = 0
        # 1번 겹이 실제로 몇 개를 걷어냈는가. 메커니즘이 도는 증거라 기록한다.
        self.links_stripped = 0
        # 페이지에 없고 읽던 사이트도 아닌 URL 을 열려다 막힌 횟수.
        self.off_page = 0
        # 페이지의 링크는 아니지만 읽던 사이트 안이라 허용된 이동(= URL 구조 추론).
        self.same_site = 0
        # depth 별로 연 노드 수. 깊이 축의 그림이 여기서 나온다.
        self.nodes_by_depth: dict[int, int] = {}
        self.readings: dict[str, list[dict[str, Any]]] = {}
        self.reused = 0
        self.content_seen: set[str] = set()
        self.branch_ceiling: int | None = None
        # Complete own-page extraction only; never reuse another branch's conclusion.
        self.extractions: dict[str, dict[str, Any]] = {}

    def seen(self, url: str) -> bool:
        return _norm(url) in self._seen

    def visit(self, url: str) -> None:
        self._seen.add(_norm(url))
        if host := _host(url):
            self.hosts.add(host)
        if url not in self.visited:
            self.visited.append(url)

    def refuse(self, url: str) -> bool:
        """URL 하나를 거절로 기록한다. **이 문항에서 이미 거절된 것이면 True.**

        True 가 돌아오면 호출자는 그 세션의 도구를 곧바로 회수한다 — 앞 세션이
        거절당한 주소를 다시 집는 것은 고쳐 잡을 여지가 있는 실수가 아니다.
        """
        key = _norm(url)
        if key in self.refused_urls:
            self.repeats += 1
            return True
        self.refused_urls.add(key)
        return False

    def opened_at(self, depth: int) -> None:
        """노드 하나를 그 깊이에 기록한다. `take()` 가 성공한 뒤에 부른다."""
        self.nodes_by_depth[depth] = self.nodes_by_depth.get(depth, 0) + 1

    @property
    def remaining(self) -> int:
        ceiling = self.total if self.branch_ceiling is None else min(self.total, self.branch_ceiling)
        return max(0, ceiling - self.used)

    @property
    def exhausted(self) -> bool:
        return self.remaining <= 0

    def take(self) -> bool:
        """한 노드를 차감한다. **실제로 페치를 실행하는 시점에** 부른다.

        spawn 시점에 차감하면 실패한 페치까지 예산을 먹는다.
        """
        if self.exhausted:
            self.refused += 1
            return False
        self.used += 1
        return True

    def give_back(self) -> None:
        """페치가 실패했으면 노드를 돌려준다. 불안정한 사이트 하나가 문항을
        망치는 것을 막는다. 턴은 이미 소비됐으므로 무한 재시도는 안 된다."""
        self.used = max(0, self.used - 1)

    def as_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "used": self.used,
            "refused": self.refused,
            "duplicates": self.duplicates,
            "links_stripped": self.links_stripped,
            "off_page": self.off_page,
            "repeats": self.repeats,
            "same_site": self.same_site,
            "visited": len(self.visited),
            "nodes_by_depth": dict(sorted(self.nodes_by_depth.items())),
            "reused": self.reused,
        }


@dataclass(slots=True)
class Document:
    url: str
    content: str
    title: str = ""
    is_error: bool = False
    retrieval: str = ""
    retrieval_note: str = ""

    def render(self, index: int) -> str:
        head = f"[{index}] {self.title or '(untitled)'} — {self.url}"
        return f"{head}\n{self.content}"


@dataclass(slots=True)
class ExplorerResult:
    """explorer 하나가 부모(또는 gate)에게 돌려주는 것.

    `status` 가 핵심이다. 부모는 이걸 보고 다른 링크를 더 팔지 결정한다. 텍스트만
    돌려주면 12B 급 모델이 만족 여부를 안정적으로 추론하지 못해 적응 루프가
    무작정 확장으로 무너진다.
    """

    information: str = ""
    status: str = "not_found"
    sources: list[str] = field(default_factory=list)
    # 이 서브트리가 소비한 depth>=2 노드 수
    nodes: int = 0
    # 이 서브트리에서 실제로 도달한 최대 depth
    depth_reached: int = 1
    # 이 서브트리의 explorer 호출(세션) 수
    calls: int = 1
    # not_found 를 돌려준 자식 수. "헛다이브" 의 대용 지표다.
    dead_dives: int = 0
    turns: int = 0
    error: str | None = None
    log: dict[str, Any] = field(default_factory=dict)
    # Model-produced page notes, retained independently of every ancestor's output.
    notes: list[dict[str, Any]] = field(default_factory=list)
    extraction_state: str = "complete"
    reused: bool = False

    def render_for_parent(self) -> str:
        """부모의 도구 결과. 추출 실패를 페이지에 근거가 없다는 뜻으로 바꾸지 않는다."""
        body = self.information.strip() or (
            "No relevant evidence was extracted from this page."
            if self.extraction_state == "complete" else
            f"Reader output unavailable ({self.extraction_state}). "
            "This does not mean the page is inaccessible or contains no evidence."
        )
        lines = [body, "", f"**Status:** {self.status}",
                 f"**Extraction:** {self.extraction_state}"]
        if self.log.get("relational_reading"):
            overview = _relation_overview(self.notes)
            if overview:
                lines.insert(0, overview + "\n")
        if self.sources:
            lines.append("**Sources:** " + ", ".join(self.sources))
        if reason := self.log.get("expansion_stop_reason"):
            lines.append(f"**Further expansion stopped:** {reason}. Saved evidence is retained.")
        return "\n".join(lines)

    def render_for_gate(self) -> str:
        """gate 의 web_search 결과로 들어가는 문자열."""
        return self.render_for_parent()


class Explorer:
    def __init__(
        self,
        llm: LLM,
        config: ExplorerConfig,
        system_prompt: str,
        fetch: Any,
        *,
        enforce_tool_availability: bool = False,
        preserve_source_evidence: bool = False,
        relational_reading: bool = False,
    ) -> None:
        """`fetch` 는 `async (url) -> Document` 콜러블이다(도구 계층이 준다)."""
        self.llm = llm
        self.config = config
        self.system_prompt = system_prompt.strip()
        self._fetch = fetch
        self.enforce_tool_availability = enforce_tool_availability
        self.preserve_source_evidence = preserve_source_evidence
        self.relational_reading = relational_reading

    async def explore(self, **kwargs) -> ExplorerResult:
        budget = kwargs["budget"]
        old_ceiling = budget.branch_ceiling
        if kwargs.get("depth", 1) == 1 and self.config.max_root_nodes:
            budget.branch_ceiling = min(budget.total, budget.used + self.config.max_root_nodes)
        try:
            return await self._explore(**kwargs)
        finally:
            budget.branch_ceiling = old_ceiling

    async def _explore(
        self,
        *,
        question: str,
        reasoning: str,
        query: str,
        documents: list[Document],
        budget: Budget,
        trace: Trace,
        usage: Usage,
        depth: int = 1,
        parent_reasoning: str = "",
        turn: int = 0,
        reading_goal: str = "",
    ) -> ExplorerResult:
        cfg = self.config
        started = time.perf_counter()
        result = ExplorerResult(depth_reached=depth)

        for doc in documents:
            budget.visit(doc.url)

        cache_key = _extraction_key(documents[0].content) if len(documents) == 1 else ""
        if self.relational_reading and cache_key and cache_key in budget.extractions:
            saved = dict(budget.extractions[cache_key])
            # Keep the original source URL: a mirror is not independent evidence.
            saved["source_notice"] = (saved.get("source_notice", "") +
                "\nIdentical supplied content; reused the original page extraction, not independent corroboration.")
            saved["navigation_goal"] = reading_goal
            result.notes = [saved]
            result.information = _render_notes(result.notes)
            result.sources = list(saved["urls"])
            result.status, result.extraction_state = saved["status"], saved["extraction_state"]
            result.calls, result.reused = 0, True
            result.log = {"depth": depth, "urls": [d.url for d in documents], "opened": [],
                          "reused": True, "relational_reading": True, "reading_goal": reading_goal,
                          "status": result.status, "extraction_state": result.extraction_state,
                          "expansion_stop_reason": "repeated_content", "information": result.information,
                          "information_chars": len(result.information)}
            for doc in documents:
                budget.readings[_norm(doc.url)] = result.notes
            budget.reused += 1
            trace.event("explorer.reused_content", depth=depth, urls=[d.url for d in documents],
                        original_sources=result.sources, reading_goal=reading_goal)
            return result

        child_limit = cfg.max_subtree_children

        fingerprints = {_content_fingerprint(doc.content) for doc in documents if doc.content.strip()}
        repeated_content = bool(fingerprints) and fingerprints <= budget.content_seen
        budget.content_seen.update(fingerprints)

        can_expand = (
            depth < cfg.max_depth
            and child_limit > 0
            and not budget.exhausted
        )
        children_left = min(child_limit, budget.remaining) if can_expand else 0

        rendered, doc_truncated = await self._render_documents(documents, budget)
        # **페이지에 실제로 있는 링크만 열 수 있다.** 절단·링크 제거를 거친 뒤의
        # 문자열에서 뽑으므로, 모델이 눈으로 본 것과 정확히 일치한다.
        openable = _page_links(rendered)
        menu = (
            _link_menu(rendered, budget, query, question, cfg.max_link_menu)
            if children_left > 0
            else []
        )
        user = _user_message(
            question=question,
            reasoning=reasoning,
            parent_reasoning=parent_reasoning,
            query=query,
            documents=rendered,
            depth=depth,
            max_depth=cfg.max_depth,
            budget=budget,
            children_left=children_left,
            menu=menu,
        )
        if self.relational_reading:
            user += ("\n\nLocal navigation task (parent hypothesis, not source evidence):\n"
                     + (reading_goal or "Use this page to establish relevant relations in the original question.")
                     + "\nReturn when this relation is established, contradicted, or has no useful route here. "
                     "Other unresolved parts of the whole question belong to the parent. "
                     "Keep unexpected facts useful to the original question.")
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": self._system()},
            {"role": "user", "content": user},
        ]
        extraction_messages = (
            [{"role": "system", "content": self._system()},
             {"role": "user", "content": _extraction_message(question, rendered, "" if self.relational_reading else reading_goal)}]
            if cfg.isolate_extraction_context or self.relational_reading else messages[:2]
        )
        trace.event(
            "explorer.start",
            depth=depth,
            turn=turn,
            query=query,
            reading_goal=reading_goal,
            documents=[d.url for d in documents],
            document_chars=len(rendered),
            document_truncated=doc_truncated,
            can_expand=can_expand,
            # 이 explorer 가 실제로 고를 수 있었던 링크 수. 0 인데 확장이 없으면
            # 모델 탓이 아니라 페이지에 갈 곳이 없었던 것이다 — 둘을 구분해야 한다.
            openable_links=len(openable),
            menu_links=len(menu),
            budget=budget.as_dict(),
        )

        urls = [d.url for d in documents]
        # 원문과 파싱 전 응답은 trace에 한 번만 저장한다. 트리/캐시에 복제하지 않는다.
        trace.event("explorer.input", depth=depth, urls=urls, messages=messages)
        opened: list[dict[str, Any]] = []
        own_information, own_status = "", "not_found"
        own_state = "empty_output"
        child_notes: list[dict[str, Any]] = []
        recovery_attempts = 0
        expansion_decision = ""
        expansion_stop_reason = ""
        access_only = self.relational_reading and _access_only_documents(documents)

        async def chat(history: list[dict[str, Any]], phase: str, tools: Any = None):
            result.turns += 1
            # 문서+추론+누적 자식 결과 전체를 확인한다. 근거를 조용히 자르지 않는다.
            size = await self.llm.count_tokens(json.dumps(history, ensure_ascii=False))
            if size + 512 > cfg.context_limit:
                raise ValueError("explorer context limit reached; retained page notes are preserved")
            choice = {"tool_choice": "none"} if self.enforce_tool_availability and not tools else {}
            if self.relational_reading:
                trace.event("explorer.request", depth=depth, urls=urls, phase=phase,
                            turn=result.turns, context_tokens=size,
                            available_tools=[t["function"]["name"] for t in tools or []])
            reply = await self.llm.chat(
                history, max_tokens=cfg.max_tokens, tools=tools, usage=usage, **choice
            )
            raw_text = reply.text
            recovered_call = recover_tool_calls(reply, tools)
            normalized = normalize_tool_names(reply, tools)
            if recovered_call:
                reply.text = ""
            trace.event(
                "explorer.response", depth=depth, urls=urls, phase=phase,
                turn=result.turns, reasoning=reply.reasoning, text=raw_text,
                recovered_tool_call=recovered_call,
                normalized_tool_names=normalized,
                finish_reason=reply.finish_reason,
                prompt_tokens=reply.prompt_tokens, completion_tokens=reply.completion_tokens,
                tool_calls=[{"name": c.function.name, "arguments": c.function.arguments}
                            for c in reply.tool_calls],
            )
            return reply

        async def extract() -> tuple[str, str, str]:
            nonlocal recovery_attempts, expansion_decision
            if access_only:
                expansion_decision = "no"
                trace.event("explorer.access_only", depth=depth, urls=urls)
                return ("Access screen only; no document evidence was available. "
                        "Retain the search title/author as a lead to another copy.", "not_found", "complete")
            # 실패한 사고/툴콜 이력 없이 같은 원문에서 최대 한 번 복구한다.
            best, status, state = "", "not_found", "empty_output"
            for attempt in range(2):
                instruction = _EXTRACT_NOW
                if self.relational_reading:
                    instruction += (" Include **Connections:** with brief source-supported entity relations "
                                    "and **Next links:** with one URL and its missing relation per line. "
                                    "Connections are your interpretation; label deductions and preserve quotes. "
                                    "If Expand is yes, the first eligible Next link will be opened directly; "
                                    "put the most useful specific route first. For an irrelevant/access page, "
                                    "return one short explanation, Expand no and Status not_found; omit empty sections.")
                history = extraction_messages + [{"role": "user", "content": instruction}]
                if attempt:
                    recovery_attempts += 1
                    history.append({"role": "user", "content": _EXTRACT_RETRY})
                trace.event("explorer.extract_input", depth=depth, urls=urls,
                            attempt=attempt, messages=history)
                try:
                    reply = await chat(history, "extract" if not attempt else "recover")
                except Exception as exc:
                    state = "context_limit" if "context limit" in str(exc) else "reader_error"
                    trace.event("explorer.error", depth=depth, urls=urls, phase="extract",
                                error=repr(exc))
                    if state == "context_limit":
                        break
                    continue
                body, parsed_status = _parse_final(reply.text, allow_explanation=self.enforce_tool_availability)
                body, decision = _parse_expansion_decision(body)
                if body and reply.truncated and not reply.tool_calls:
                    best, status = body, parsed_status
                if reply.truncated:
                    state = "truncated"
                elif reply.tool_calls:
                    state = "invalid_output"
                elif not _SPECIAL.sub("", reply.text or "").strip():
                    state = "empty_output"
                elif body.strip().upper() in {"DONE", "DONE.", "FINISHED"}:
                    state = "invalid_output"
                else:
                    expansion_decision = decision
                    return body, parsed_status, "complete"
            return best, status, "truncated" if best else state

        try:
            # 먼저 현재 페이지의 사실을 고정한다. 이후 탐색의 실패가 이 기록을 지우지 못한다.
            if cfg.extract_before_expand or not can_expand:
                own_information, own_status, own_state = await extract()
                if cfg.prune_unhelpful_branches and can_expand:
                    if repeated_content:
                        expansion_stop_reason = "repeated_content"
                    elif own_state != "complete":
                        expansion_stop_reason = "extraction_unavailable"
                    elif expansion_decision == "no":
                        expansion_stop_reason = "no_useful_next_link"
                    elif own_status == "not_found" and expansion_decision != "yes":
                        expansion_stop_reason = "no_evidence_or_route"
                    if expansion_stop_reason:
                        can_expand = False
                        trace.event("expand.pruned", depth=depth, urls=urls,
                                    reason=expansion_stop_reason, budget=budget.as_dict())
                if can_expand:
                    if self.relational_reading:
                        # Extraction has already read the full source. Navigation needs
                        # saved facts and observed link context, not another full reading.
                        messages = [messages[0], {"role": "user", "content": (
                            "Original question:\n" + question
                            + "\n\nLocal navigation task (hypothesis, not evidence):\n"
                            + (reading_goal or reasoning or question)
                            + "\n\nCurrent source URLs:\n" + "\n".join(urls)
                            + "\n\nObserved source links and their surrounding text:\n"
                            + _navigation_links(rendered)
                        )}]
                    messages.append({"role": "user", "content": (
                        "Your page note has been saved separately:\n"
                        + (own_information or f"Reader state: {own_state}; no evidence saved yet.")
                        + "\n\nNow follow a page link if it can fill a specific missing fact. "
                        + ("Use the supplied source links. " if self.relational_reading
                           else "Read the links in the original page above. ")
                        + "Your note and all child notes "
                        "will be returned automatically; do not rewrite or discard them. "
                        "Before opening a link, identify the missing field and explain why its "
                        "label, surrounding text, or observed URL pattern can supply that field. "
                        "Check the required entity, year and scope. A general navigation link "
                        "on an unrelated page is not sufficient. Stop branches that repeat "
                        "content or cannot supply the missing field; preserve budget for other pages. "
                        "If no useful expansion remains, reply DONE."
                    )})

            wasted = 0
            first_route = (_first_note_route(own_information, openable, budget)
                           if self.relational_reading and expansion_decision == "yes"
                           and own_state == "complete" and can_expand else None)
            for step in range(1, max(1, cfg.max_turns) + 1) if can_expand else ():
                if children_left <= 0 or budget.exhausted or wasted >= _MAX_WASTED_CALLS:
                    if self.enforce_tool_availability:
                        trace.event("expand.tool_withdrawn", depth=depth, turn=step,
                                    reason="local_expansion_finished", children_left=children_left,
                                    remaining=budget.remaining)
                    break
                navigation_messages = messages
                if self.enforce_tool_availability:
                    navigation_messages = messages + [{"role": "user", "content": (
                        f"Current local expansion allowance: {min(children_left, budget.remaining)} direct children, "
                        f"{budget.remaining} nodes remaining within the active branch/global limit. "
                        "Only web_fetch is available here. If no useful link remains, return DONE. "
                        "When this allowance ends, saved evidence returns to the parent automatically; "
                        "this does not end the main research task."
                    )}]
                from_note = step == 1 and first_route is not None
                if from_note:
                    route_url, navigation_reason = first_route
                    calls = [SimpleNamespace(id=f"note_route_{depth}", function=SimpleNamespace(
                        name="web_fetch", arguments=json.dumps({"url": route_url})))]
                    trace.event("expand.from_note", depth=depth, url=route_url, goal=navigation_reason)
                else:
                    reply = await chat(navigation_messages, "expand", [FETCH_TOOL])
                    if not reply.tool_calls:
                        if not cfg.extract_before_expand:
                            own_information, own_status = _parse_final(reply.text, allow_explanation=self.enforce_tool_availability)
                            own_state = "truncated" if reply.truncated else (
                                "complete" if reply.text.strip() else "empty_output"
                            )
                            if own_information.strip().upper() in {"DONE", "DONE.", "FINISHED"}:
                                own_information, own_state = "", "invalid_output"
                        break
                    navigation_reason = ("\n".join(p for p in (reply.reasoning, reply.text) if p)
                                         if self.relational_reading else reply.reasoning or reply.text)
                    calls = reply.tool_calls
                    messages.append(_assistant_message(reply))
                for call in calls:
                    if self.enforce_tool_availability and (children_left <= 0 or budget.exhausted):
                        messages.append({"role": "tool", "tool_call_id": call.id, "content":
                            "Local expansion has finished; this call was not executed. Saved evidence will return to the parent."})
                        continue
                    seen_repeats = budget.repeats
                    output, child = await self._open(
                        call=call, question=question, reasoning=reasoning,
                        reasoning_now=(
                            "Saved facts from the parent page (not the page you are about to read):\n"
                            + (own_information or "(none)") + "\n\nPurpose of following this link:\n"
                            + navigation_reason
                        ),
                        query=query, budget=budget, trace=trace, usage=usage,
                        depth=depth, turn=step, allowed=children_left, openable=openable,
                        reading_goal=reading_goal,
                        link_goals=_link_goals(own_information) if self.relational_reading else None,
                        navigation_reason=navigation_reason if self.relational_reading else "",
                    )
                    if child is not None:
                        child_notes.extend(child.notes)
                        opened.append(child.log)
                        if not child.reused:
                            children_left -= 1
                            result.nodes += child.nodes + 1
                            result.calls += child.calls
                            result.depth_reached = max(result.depth_reached, child.depth_reached)
                            result.dead_dives += child.dead_dives + int(
                                child.status == "not_found" and child.extraction_state == "complete"
                            )
                        else:
                            wasted += 1
                        if cfg.prune_unhelpful_branches and not child.reused and (
                            child.status == "not_found" or
                            child.log.get("expansion_stop_reason") == "repeated_content"
                        ):
                            wasted += 1
                            output += ("\nThis branch supplied no new relevant evidence. "
                                       "Use a different promising link or finish; do not try URL "
                                       "variants of this branch.")
                    else:
                        if output.startswith("Could not open "):
                            # The failed request costs no expansion node, but its outcome
                            # must reach the main model rather than disappearing here.
                            failed_url = _parse_arguments(call.function.arguments).get("url", "")
                            child_notes.append({"urls": [str(failed_url)], "text": output,
                                                "status": "not_found", "extraction_state": "fetch_error"})
                        wasted += _MAX_WASTED_CALLS if budget.repeats > seen_repeats else 1
                    if from_note:
                        # This action came from the recorded page note, not a fabricated
                        # native tool-call response. Keep that provenance in the dialogue.
                        messages.append({"role": "user", "content": (
                            "Result of opening the first route selected in your saved page note:\n"
                            + route_url + "\nPurpose (hypothesis): " + navigation_reason
                            + "\n" + output
                        )})
                    else:
                        messages.append({"role": "tool", "tool_call_id": call.id, "content": output})
                if wasted >= _MAX_WASTED_CALLS:
                    trace.event("expand.tool_withdrawn", depth=depth, turn=step, wasted=wasted)

            # 한 단계 모드에서도 마지막 턴이 툴콜이면 현재 페이지의 추출을 마무리한다.
            if not cfg.extract_before_expand and can_expand and own_state != "complete":
                own_information, own_status, own_state = await extract()
        except Exception as exc:
            result.error = repr(exc)
            trace.event("explorer.error", depth=depth, urls=urls, phase="expand", error=result.error)

        own_note = {"urls": urls, "text": own_information, "status": own_status,
                    "extraction_state": own_state}
        if self.relational_reading:
            own_note["navigation_goal"] = reading_goal
        if self.preserve_source_evidence:
            # Carry already-seen structured sources separately from model prose.
            # Never fetch again or bypass document truncation/contamination checks.
            if repeated_content:
                own_note["source_notice"] = (
                    "This page repeats previously read content; it adds no new source rows. "
                    "Use a linked detail page or another missing condition instead of URL variants."
                )
            elif not any(d.is_error for d in documents) and _structured_source(rendered):
                if await self.llm.count_tokens(rendered) <= cfg.max_tokens:
                    own_note["source_evidence"] = rendered
                    own_note["source_notice"] = (
                        "Verbatim supplied source follows, separate from the reader's interpretation. "
                        "Its scope and missing conditions still apply; it is not a verified answer set."
                    )
                else:
                    own_note["source_notice"] = (
                        "The structured source exceeds the verbatim supplement limit; only the "
                        "reader note is returned. Summary omissions do not establish absence or "
                        "complete list coverage."
                    )
            if doc_truncated or any("(page truncated)" in d.content for d in documents):
                own_note["source_notice"] = own_note.get("source_notice", "") + (
                    " The supplied source was truncated; unseen rows remain unknown."
                )
        result.notes = _merge_notes([own_note, *child_notes])
        if (self.relational_reading and cache_key and own_state == "complete"
                and own_information.strip() and not doc_truncated
                and not any(d.is_error for d in documents)):
            budget.extractions[cache_key] = dict(own_note)
        result.information = _render_notes(result.notes)
        result.status = "partial" if any(
            n["text"] and n["status"] != "not_found" for n in result.notes
        ) else "not_found"
        # 한 페이지의 answered를 전체 서브트리/원 질문의 완료로 승격하지 않는다.
        if not opened and own_information and own_status == "answered":
            result.status = "answered"
        result.extraction_state = own_state
        if own_state == "complete" and any(n["extraction_state"] != "complete" for n in child_notes):
            result.extraction_state = "partial_failure"
        result.sources = _dedupe([u for n in result.notes if n["text"]
                                 and n["extraction_state"] != "fetch_error" for u in n["urls"]])
        # 현재 페이지가 어느 경로에서 다시 요청되어도 이미 얻은 근거를 돌려준다.
        for url in urls:
            budget.readings[_norm(url)] = result.notes

        result.log = {
            "depth": depth,
            "parent_reasoning": parent_reasoning,
            "query": query,
            "urls": [d.url for d in documents],
            "turns": result.turns,
            "status": result.status,
            "information": result.information,
            "information_chars": len(result.information),
            "own_information": own_information,
            "own_status": own_status,
            "own_information_chars": len(own_information),
            "source_evidence_chars": len(own_note.get("source_evidence", "")),
            "extraction_state": result.extraction_state,
            "own_extraction_state": own_state,
            "note_count": len(result.notes),
            "recovery_attempts": recovery_attempts,
            "expansion_decision": expansion_decision,
            "expansion_stop_reason": expansion_stop_reason,
            "nodes": result.nodes,
            "error": result.error,
            "latency_ms": round((time.perf_counter() - started) * 1000, 1),
            "opened": opened,
        }
        if self.relational_reading:
            result.log.update(relational_reading=True, reading_goal=reading_goal)
        trace.event(
            "explorer.end",
            depth=depth,
            status=result.status,
            turns=result.turns,
            nodes=result.nodes,
            information_chars=len(result.information),
            own_information_chars=len(own_information),
            extraction_state=result.extraction_state,
            budget=budget.as_dict(),
        )
        return result

    # --- 내부 ---------------------------------------------------------------

    def _system(self) -> str:
        effort = self.llm.profile.reasoning_effort
        if effort:
            return f"Reasoning: {effort}\n{self.system_prompt}".strip()
        return self.system_prompt

    async def _render_documents(
        self, documents: list[Document], budget: Budget
    ) -> tuple[str, bool]:
        """문서 예산을 **문서 수로 나눠** 각자에게 준다.

        묶음 전체에 한 번만 걸면 앞 문서가 예산을 다 먹고 뒤 문서는 모델에 도달조차
        하지 않는다(실측: 위키 페이지 하나가 232K자 ≈ 77.6K 토큰으로 이미 묶음
        예산 50K 의 1.5배다). "상위 k개를 읽었다"가 성립하려면 k개가 다 와야 한다.

        절단은 앞에서부터 남기는 단순 절단이다. 그래서 문서의 꼬리(위키의 각주·참고
        문헌 등)는 잘려 나간다 — 확장 대상이 거기 있는 경우가 있어 한계로 남는다.

        **절단 전에 이미 읽은 페이지로 가는 링크를 걷어낸다.** 순서가 중요하다 —
        뒤에 하면 지워질 링크가 문서 예산을 먼저 먹는다.
        """
        if not documents:
            return "", False

        prepared: list[str] = []
        for i, doc in enumerate(documents, 1):
            text, stripped = _strip_visited_links(doc.render(i), budget)
            budget.links_stripped += stripped
            prepared.append(text)

        shares = await self._shares(prepared)
        parts, truncated = [], False
        for text, share in zip(prepared, shares):
            body, cut = await self.llm.cap(text, share)
            truncated = truncated or cut
            parts.append(body + ("\n... (document truncated)" if cut else ""))
        return "\n\n".join(parts), truncated

    async def _shares(self, texts: list[str]) -> list[int]:
        """문서별 토큰 상한. **남는 몫을 큰 문서에 돌려준다.**

        예산을 문서 수로 똑같이 나누기만 하면, 작은 문서가 제 몫을 안 쓰고 버리는
        동안 큰 문서는 잘린다. 실측(search-o1, top-5): 묶음 총량이 38K 토큰으로
        예산 90K 의 절반도 안 되는데 절단이 41% 에서 일어났다. 예산이 모자란 게
        아니라 배분이 굳어 있었던 것이다.

        그래서 균등 몫보다 작은 문서들을 먼저 확정하고, 남은 예산을 아직 넘치는
        문서들에게 다시 균등 배분한다(더 나눌 것이 없을 때까지 반복). 총량은 그대로
        지키면서 절단만 줄어든다.

        문서가 하나면 몫이 곧 예산이라 depthsearch 의 동작은 달라지지 않는다.
        """
        total = max(1, self.config.max_document_tokens)
        if len(texts) == 1:
            return [total]

        sizes = [await self.llm.count_tokens(t) for t in texts]
        shares = [0] * len(sizes)
        pending = set(range(len(sizes)))
        left = total
        while pending:
            even = max(1, left // len(pending))
            fits = {i for i in pending if sizes[i] <= even}
            if not fits:  # 남은 문서가 전부 넘친다 — 균등하게 나눠 준다
                for i in pending:
                    shares[i] = even
                break
            for i in fits:
                shares[i] = sizes[i]
                left -= sizes[i]
            pending -= fits
        return shares

    async def _open(
        self,
        *,
        call: Any,
        question: str,
        reasoning: str,
        reasoning_now: str,
        query: str,
        budget: Budget,
        trace: Trace,
        usage: Usage,
        depth: int,
        turn: int,
        allowed: int,
        openable: dict[str, str],
        reading_goal: str = "",
        link_goals: dict[str, str] | None = None,
        navigation_reason: str = "",
    ) -> tuple[str, ExplorerResult | None]:
        """자식 하나를 연다. 돌려주는 문자열이 부모의 도구 결과가 된다."""
        arguments = _parse_arguments(getattr(call.function, "arguments", None))
        try:
            url = normalize_fetch_url(arguments.get("url"))
        except ValueError as exc:
            return f"Invalid web_fetch arguments: {exc}. Supply a JSON object with a url.", None

        if call.function.name != "web_fetch":
            return f"unknown tool '{call.function.name}'.", None
        if not url:
            return "web_fetch needs a url.", None
        if allowed <= 0:
            return _BUDGET_NOTICE.format(remaining=budget.remaining), None

        # **페이지에 없는 URL 은 열지 않는다.** 실측상 explorer 는 링크를 따라가는
        # 대신 그럴듯한 주소를 지어낸다 — 한 문항에서 위키 문서 제목을 추측한 URL
        # 하나로 10번, 같은 주소의 슬래시·접미사 변형으로 다시 여러 번. 전부 존재하지
        # 않거나 이미 읽은 페이지였다. 도구 설명이 "이 페이지의 링크"라고 말해도
        # 강제되지 않으면 지어낸다. 예산도 턴도 쓰지 않고 막는다.
        # **순서가 중요하다.** 이미 읽은 페이지를 먼저 본다. 이 검사를 뒤에 두면
        # 읽은 페이지의 링크는 문서에서 걷어낸 뒤라 `openable` 에 없고, 따라서
        # 전부 off_page 로 잘못 기록된다(실측: 12건 중 7건이 그렇게 뒤집혔다).
        # 두 숫자는 서로 다른 것을 말한다 — duplicates 는 "갔던 곳을 또 가려 했다",
        # off_page 는 "없는 주소를 지어냈다". 섞이면 진단이 불가능하다.
        if budget.seen(url):
            budget.duplicates += 1
            if notes := budget.readings.get(_norm(url)):
                budget.reused += 1
                cached = ExplorerResult(
                    notes=notes, information=_render_notes(notes), calls=0,
                    status="partial" if any(n["text"] and n["status"] != "not_found" for n in notes)
                           else "not_found",
                    extraction_state=("complete" if all(n["extraction_state"] == "complete" for n in notes)
                                      else "partial_failure"),
                    sources=_dedupe([u for n in notes if n["text"]
                                     and n["extraction_state"] != "fetch_error" for u in n["urls"]]),
                    reused=True,
                )
                cached.log = {"depth": depth + 1, "urls": [url], "reused": True,
                              "status": cached.status, "extraction_state": cached.extraction_state,
                              "information_chars": len(cached.information), "opened": []}
                trace.event("expand.reused", depth=depth + 1, url=url)
                return "Previously saved page notes (no new fetch):\n" + cached.render_for_parent(), cached
            repeat = budget.refuse(url)
            trace.event("expand.duplicate", depth=depth + 1, url=url, repeat=repeat)
            return (
                f"{url} is currently being read by an ancestor or another reader. "
                "Its note is not complete yet. Use the parent facts you were given, "
                "follow a different link, or finish with this page's evidence.",
                None,
            )

        # 열 수 있는 곳은 둘이다 — **이 페이지의 링크**, 또는 **이미 읽고 있는
        # 사이트 안**.
        #
        # 처음에는 페이지의 링크만 허용했는데, 그게 모델의 정상 행동을 막았다.
        # `/diary/1660/12/` 와 `/diary/1661/12/` 를 본 모델은 `/diary/1666/12/` 를
        # 추론해서 연다 — 실존하는 페이지고, "12월마다 등장하는 인물"을 묻는 문항
        # 에서는 그게 정답 전략이다. 링크만 따라가게 하면 그 문항은 풀 수가 없다.
        #
        # 반대로 막아야 할 것은 분명하다 — 검색엔진 쿼리, 우리 페치 서비스 주소,
        # 읽던 것과 무관한 사이트. 같은 사이트 안이라는 조건이 그 셋을 다 걸러낸다.
        # 추론이 빗나가 404 가 나면 예산은 돌려받으므로(`give_back`) 턴 하나로 끝난다.
        on_page = openable.get(_norm(url))
        if on_page is not None:
            url = on_page  # 모델의 변형이 아니라 페이지에 적힌 형태로 연다
        elif _host(url) in budget.hosts:
            budget.same_site += 1
            trace.event("expand.same_site", depth=depth + 1, url=url)
        else:
            budget.off_page += 1
            repeat = budget.refuse(url)
            trace.event("expand.off_page", depth=depth + 1, url=url, repeat=repeat)
            return (
                f"{url} is neither a link on the page you are reading nor a page on a "
                "site you are already reading, so it cannot be opened. This tool "
                "follows links and moves within a site; it is not a search engine. "
                "Retrying a variant of it will fail the same way. If there is nothing "
                "here worth opening, finish and report what you found.",
                None,
            )

        # 예산은 **페치를 실제로 실행하는 시점에** 차감한다.
        if not budget.take():
            trace.event("budget.nodes_exhausted", depth=depth, turn=turn, url=url)
            return _BUDGET_NOTICE.format(remaining=0), None

        trace.event(
            "expand.node", depth=depth + 1, url=url, parent_depth=depth,
            budget=budget.as_dict(),
        )
        document = await self._fetch(url)
        if document.is_error:
            # 실패한 페치는 노드를 돌려준다. 턴은 이미 소비됐다.
            budget.give_back()
            trace.event("expand.failed", depth=depth + 1, url=url, error=document.content[:300])
            return f"Could not open {url}: {document.content[:300]}", None

        local_goal = (link_goals or {}).get(_norm(url), "") if self.relational_reading else reading_goal
        if self.relational_reading:
            fallback = ("matched_next_link" if local_goal else "parent_decision" if navigation_reason
                        else "inherited_task" if reading_goal else "original_question")
            local_goal, _ = await self.llm.cap(local_goal or navigation_reason or reading_goal or question, self.config.max_tokens)
            trace.event("expand.relation_task", url=url, parent_depth=depth, goal=local_goal,
                        fallback=fallback)

        child = await self.explore(
            question=question,
            reasoning="" if self.relational_reading else reasoning,
            query="" if self.relational_reading else query,
            documents=[document],
            budget=budget,
            trace=trace,
            usage=usage,
            depth=depth + 1,
            parent_reasoning="" if self.relational_reading else reasoning_now,
            turn=turn,
            reading_goal=local_goal,
        )
        if child.reused:
            budget.give_back()
        else:
            budget.opened_at(depth + 1)
        trace.event(
            "expand.return",
            depth=depth + 1,
            url=url,
            status=child.status,
            information_chars=len(child.information),
        )
        return child.render_for_parent(), child


# --- 렌더 · 파싱 -------------------------------------------------------------

_BUDGET_NOTICE = (
    "Expansion budget exhausted — no further page can be opened ({remaining} node(s) "
    "left). Write your **Final Information** from what you already have."
)

# 한 explorer 세션에서 허용하는 '아무것도 못 연' 호출 수. 넘으면 도구를 회수한다.
# 2 로 둔 것은, 한 번 빗나가고 고쳐 잡을 여지는 주되 같은 주소를 열 번씩 두드리는
# 것은 막기 위해서다.
_MAX_WASTED_CALLS = 2

_EXTRACT_NOW = (
    "Read only the page(s) supplied above. First save the facts available HERE, without "
    "opening links or solving the entire multi-page question. Follow the output format: "
    "**Final Information**, then **Page**, **Evidence**, **Coverage**, **Missing**, **Next links**, "
    "and a final **Status:** line. In Evidence copy exact relevant names, numbers, dates, "
    "units, table rows and short supporting quotations, keeping each entity attached to "
    "its own values. Return the COMPLETE relevant list or table, not a few examples. "
    "State which entities, years and conditions are covered and whether the list is "
    "complete, a subset, or truncated. Unseen rows are unknown, not absent. "
    "A missing fact on another page does not invalidate facts on this page. "
    "Distinguish source text from the supplied reasoning, which may be mistaken. "
    "If the page contains no relevant evidence, explain briefly what it actually is "
    "and what is missing. Do not claim the page could not be accessed unless its content "
    "actually shows an access error. Do not invent facts or URLs."
    " If the system requests an Expand field, put **Expand:** yes or no before Status. "
    "Say yes only for a concrete route to a missing field. A relevant index may have "
    "such a route without answer facts; unrelated years/topics or generic footer links "
    "alone do not justify continuing. This is a navigation decision, not source evidence."
)
_EXTRACT_RETRY = (
    "The previous reader response was empty, incomplete, or not a page note. "
    "Return your extracted evidence now in the final answer channel. No tool calls. "
    "Keep it compact enough to finish; prioritize exact facts and full relevant lists."
)


def _content_fingerprint(text: str) -> str:
    # Ignore Reader URL metadata so query-string variants returning the same body
    # cannot create another recursive branch. Do not use fuzzy semantic matching.
    body = text.split("Markdown Content:", 1)[-1]
    body = re.sub(r"^URL Source:.*$", "", body, flags=re.MULTILINE)
    return hashlib.sha256(" ".join(body.split()).encode("utf-8")).hexdigest()


def _extraction_key(text: str) -> str:
    # Preserve row boundaries/spacing, unlike the legacy branch-pruning fingerprint.
    # Reader wrapper metadata is not page content. Notes retain the original URL.
    body = text.split("Markdown Content:", 1)[-1]
    body = re.sub(r"^URL Source:.*(?:\n|$)", "", body, flags=re.MULTILINE)
    return hashlib.sha256(body.encode("utf-8")).hexdigest() if body.strip() else ""


def _access_only_documents(documents: list[Document]) -> bool:
    """Recognize a complete, known access screen, never keywords in an article."""
    allowed = {
        "loading", "18+ only", "18+ access", "private 18+ access", "premium access portal",
        "continue to access", "please confirm you are over 18 years old.",
        "continue 18+ verified", "continue to unlock exclusive content.", "age-restricted content",
        "[leave](https://google.com/)",
    }
    for doc in documents:
        if not re.search(r"^Title:\s*18\+ Access\s*$", doc.content, re.MULTILINE | re.IGNORECASE):
            return False
        if "Markdown Content:" not in doc.content:
            return False
        body = doc.content.split("Markdown Content:", 1)[1]
        lines = [" ".join(line.strip(" #*_").lower().split()) for line in body.splitlines() if line.strip()]
        if not lines or any(line not in allowed for line in lines):
            return False
    return bool(documents)


def _navigation_links(rendered: str) -> str:
    """Keep every observed URL with local source context; no menu-rank pruning."""
    lines = rendered.splitlines()
    keep = set()
    for i, line in enumerate(lines):
        if _page_links(line):
            keep.update(range(max(0, i - 1), min(len(lines), i + 2)))
    return "\n".join(lines[i] for i in sorted(keep)) or "(No source links supplied.)"


def _first_note_route(note: str, openable: dict[str, str], budget: Budget) -> tuple[str, str] | None:
    """Execute only the reader's first eligible, described route; never rank in code."""
    goals = _link_goals(note)
    for line in _note_section(note, "Next links").splitlines():
        links = _page_links(line)
        if len(links) > 1:
            return None  # Ambiguous format: let the ordinary navigation turn decide.
        for key, url in links.items():
            if not goals.get(key) or budget.seen(url):
                continue
            if key not in openable and _host(url) not in budget.hosts:
                return None
            return openable.get(key, url), goals[key]
    return None


def _note_section(text: str, heading: str) -> str:
    start = re.search(r"(?im)^\s*(?:\*\*|#{1,4}\s*)" + re.escape(heading)
                      + r"\s*(?::\s*)?(?:\*\*)?\s*:?[^\S\n]*", text)
    if not start:
        return ""
    rest = text[start.end():]
    end = re.search(r"(?im)^\s*(?:\*\*|#{1,4}\s*)(?:Page|Evidence|Connections|Coverage|Missing|Next links|Expand|Status)\b", rest)
    return (rest[:end.start()] if end else rest).strip()


def _link_goals(note: str) -> dict[str, str]:
    """Bind existing one-line Next links explanations to URLs, never tool arguments."""
    goals = {}
    for line in _note_section(note, "Next links").splitlines():
        for key, url in _page_links(line).items():
            explanation = line.replace(url, "").strip(" |-*[]():\t")
            if explanation:
                goals[key] = explanation
    return goals


def _relation_overview(notes: list[dict[str, Any]]) -> str:
    rows = []
    for note in notes:
        connections = _note_section(note["text"], "Connections")
        if connections:
            row = "Source: " + ", ".join(note["urls"])
            if connections:
                row += "\nConnections: " + connections
            rows.append(row)
    return ("Reader's source-linked interpretations (verify against the page evidence below):\n"
            + "\n\n".join(rows)) if rows else ""


def _extraction_message(question: str, documents: str, reading_goal: str = "") -> str:
    return (
        f"**Original Question:**\n{question.strip()}\n\n"
        "**Local reading task:**\nExtract the fields this page can establish for the "
        "question: entities, conditions, measurements, dates and units. The question "
        "specifies what to look for; it is not evidence that any fact is true. "
        "Use only the supplied page content. Report absent fields as unknown. "
        "For a table, preserve its headers and the relevant rows. For a list, preserve "
        "all relevant members and its scope. A link may be useful even when this page "
        "contains no answer facts.\n\n"
        + ("**Relation to verify (a task, not evidence; its assumptions may be wrong):**\n"
           + reading_goal + "\nExtract support, explicit contradiction, or missing evidence for this relation. "
           "Retain other useful original-question findings; do not solve the whole question from memory.\n\n"
           if reading_goal else "")
        + "**Pages you were given:**\n" + documents
    )


def _parse_expansion_decision(text: str) -> tuple[str, str]:
    # Optional control line, separate from source evidence. Older/custom prompts
    # without this field retain their usual navigation behavior.
    pattern = r"^[ \t]*\*\*Expand:\*\*[ \t]*(?:\*\*)?(yes|no)\b[^\n]*$"
    matches = list(re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE))
    decision = matches[-1].group(1).lower() if matches else ""
    return re.sub(pattern, "", text, flags=re.MULTILINE | re.IGNORECASE).strip(), decision


def _merge_notes(notes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Retain each source note once; never ask an ancestor to reproduce child facts."""
    seen: set[tuple[Any, ...]] = set()
    merged = []
    for note in notes:
        key = (tuple(note["urls"]), note["text"], note["extraction_state"])
        if key not in seen:
            seen.add(key)
            merged.append(note)
    return merged


def _render_notes(notes: list[dict[str, Any]]) -> str:
    blocks = []
    for n in notes:
        if not (n["text"].strip() or n.get("source_evidence") or n.get("source_notice")):
            continue
        block = (f"### Page note: {', '.join(n['urls'])}\n"
                 f"Reader state: {n['extraction_state']}; relevance: {n['status']}\n{n['text']}")
        if n.get("source_notice"):
            block += "\n\nSource coverage notice: " + n["source_notice"]
        if n.get("source_evidence"):
            block += "\n\n#### Verbatim source (not model-generated)\n" + n["source_evidence"]
        blocks.append(block)
    return "\n\n".join(blocks)


def _structured_source(text: str) -> bool:
    """Compact native files or Markdown tables benefit from lossless handoff."""
    return bool(re.search(r"^Title: (?:PDF|CSV) document\s*$|^\[PDF page \d+\]",
                          text, re.MULTILINE)
                or re.search(r"^\s*\|?\s*:?-{3,}:?\s*\|\s*:?-{3,}", text, re.MULTILINE))


def _user_message(
    *,
    question: str,
    reasoning: str,
    parent_reasoning: str,
    query: str,
    documents: str,
    depth: int,
    max_depth: int,
    budget: Budget,
    children_left: int,
    menu: list[tuple[str, str]] | None = None,
) -> str:
    """Search-o1 의 RiD 입력 구성. 원 질문과 **누적** 추론을 함께 넘긴다.

    논문 식 (4) 의 R(<i) 는 i번째 검색 직전까지 누적된 추론 체인 전체이고,
    Alg.1 line 2 의 `S <- {I (+) q}` · line 11 의 `ID <- Idocs (+) qsearch (+) Seq`
    에서 Seq 가 `I (+) q` 로 시작하므로 **원 질문도 포함된다**.

    depth 2 이상에서는 여기에 하나가 더 붙는다 — 부모가 이 링크를 열기 직전에 한
    사고다. 그게 "왜 여기 왔는가" 이고, 도구 인자로 받는 것보다 안전하다(자유 텍스트
    인자는 모델이 형식을 흘리면 툴콜이 통째로 깨진다).
    """
    parts = [
        "**Original Question:**",
        question.strip() or "(unknown)",
        "",
        "**Previous Reasoning Steps:**",
        reasoning.strip() or "(none yet — this is the first search)",
        "",
        "**Current Search Query:**",
        query.strip() or "(no search query)",
    ]
    if parent_reasoning.strip():
        parts += [
            "",
            "**Why this page was opened** (the reasoning of the reader that opened it, "
            "immediately before it did):",
            parent_reasoning.strip(),
        ]
    if max_depth > 1:
        parts += ["", f"**Reading level:** {depth} of {max_depth}"]
    # 이미 읽은 페이지 목록. 문서에서 링크를 걷어내는 것만으로는 부족하다 —
    # explorer 는 같은 사이트 안이면 주소를 **조립해서** 갈 수 있으므로, 걷어낸
    # 링크를 그대로 다시 만들어낸다(실측: 중복 시도 47회 > 실제 확장 37회).
    # 갈 수 없게 만드는 것과 갔다 왔다고 알려 주는 것은 서로 다른 일이다.
    if budget.visited and children_left > 0:
        parts += [
            "",
            "**Already visited — completed notes can be reused; active ancestors cannot be reopened:**",
            "\n".join(f"- {u}" for u in budget.visited[-20:]),
        ]
    if menu:
        # **본문 앞에 놓는다.** 프롬프트 맨 끝(본문 뒤)으로 옮겨 봤더니 f1 이
        # 0.396 -> 0.271 로 무너졌다. 주의가 가장 큰 자리에 링크를 늘어놓으면
        # explorer 의 본업인 추출에서 링크 사냥 쪽으로 주의가 밀린다
        # (중복 197->219, 반복거절 90->107). 목록은 안내이지 강제가 아니다 —
        # 본문의 다른 링크도 열린다.
        parts += [
            "",
            f"**Links on this page, ranked for this query** ({len(menu)} shown). "
            "Open one of these if the page points at it; you may also follow any "
            "other link printed in the page below. The menu is not a whitelist.",
            "\n".join(f"- [{label}]({url})" for label, url in menu),
        ]
    if children_left > 0:
        parts += [
            "",
            f"**Expansion budget:** {budget.remaining} node(s) remain for the whole "
            f"question; you may open at most {children_left} more page(s) from here. "
            "Opening a page that does not change your answer costs the rest of the run.",
        ]
    parts += [
        "",
        "**Pages you were given:**",
        documents or "(no page content was retrieved)",
    ]
    return "\n".join(parts)


def _norm(url: str) -> str:
    """Host case/fragment normalization; preserve case-sensitive paths and query values."""
    cleaned = (url or "").strip()
    try:
        parsed = urlsplit(cleaned)
    except ValueError:
        return cleaned
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(),
                       parsed.path.rstrip("/"), parsed.query, ""))


def _host(url: str) -> str:
    """같은 사이트 판정을 위한 호스트. `www.` 는 떼서 같은 곳으로 본다."""
    try:
        host = urlparse((url or "").strip()).hostname or ""
    except ValueError:
        return ""
    return host.lower().removeprefix("www.")


# jina 가 돌려주는 마크다운의 인라인 링크. explorer 는 이걸 보고 확장할 곳을 고른다.
_MD_LINK = re.compile(r"\[([^\]]*)\]\(\s*(<?)([^)\s]+)\2\s*(?:\"[^\"]*\")?\s*\)")


# 본문에 그냥 박혀 있는 URL. 마크다운 링크가 아니어도 모델 눈에는 보이므로
# 열 수 있는 것으로 친다.
_BARE_URL = re.compile(r"https?://[^\s)\]<>\"']+")


def _page_links(text: str) -> dict[str, str]:
    """이 페이지에서 **실제로 열 수 있는** 링크. `정규화된 URL -> 페이지의 원문 URL`.

    마크다운 링크의 목적지와 본문에 그대로 박힌 URL 을 모은다. `_open` 이 이 표에
    없는 URL 을 거절하므로, explorer 는 눈으로 본 링크만 따라갈 수 있다.

    키를 정규화해 두는 이유는, 모델이 링크를 제대로 베끼고도 끝슬래시나 조각(#…)
    한 글자 때문에 튕기는 것을 막기 위해서다. 열 때는 값(페이지에 적힌 형태)을
    쓴다 — 모델의 변형이 아니라 페이지가 말한 주소를 연다.

    절단·링크 제거를 **거친 뒤의** 문자열에서 뽑아야 한다. 그래야 모델이 본 것과
    표가 정확히 일치한다 — 잘려 나간 꼬리의 링크를 허용하면 보이지도 않는 것을
    열 수 있게 된다.
    """
    if not text:
        return {}
    urls = {m.group(3) for m in _MD_LINK.finditer(text)}
    urls |= set(_BARE_URL.findall(text))
    out: dict[str, str] = {}
    for raw in sorted(urls):
        url = raw.rstrip(".,;")
        if url.startswith(("http://", "https://")):
            out.setdefault(_norm(url), url)
    return out


# 메뉴에서 빼는 링크. 본문 어디에나 깔려 있지만 절대 답이 없는 것들이다.
_JUNK = (
    "file:", "special:", "category:", "template:", "help:", "portal:", "talk:",
    "wikipedia:", "#cite", "action=edit", "action=raw", "oldid=", "index.php",
    "facebook.com/sharer", "twitter.com/intent", "linkedin.com/share",
    "reddit.com/submit", "pinterest.com/pin", "/login", "/signin", "/register",
    "/subscribe", "/privacy", "/terms", "/cookie", "/rss", "/feed",
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".woff",
)
_STOP = frozenset(
    "the a an of and or in on at to for from by with about into over after is are was "
    "were be been being that this these those it its as which who whom what when where "
    "how why all any both each more most other some such no nor not only own same so "
    "than too very can will just".split()
)


def _terms(*texts: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", " ".join(texts).lower())
    return {w for w in words if len(w) > 2 and w not in _STOP}


def _link_menu(
    text: str, budget: Budget, query: str, question: str, limit: int
) -> list[tuple[str, str]]:
    """이 페이지에서 열 만한 링크를 **추려서 순위대로** 돌려준다.

    explorer 가 링크를 못 따라가고 URL 을 지어내는 이유는 고를 줄 몰라서가 아니라
    **볼 수가 없어서**다. 실측으로 페이지 하나에 링크가 250~921개씩 있고 본문은
    6~47만 자라, 그 안에 흩어진 링크를 모델이 훑지 못한다. 그래서 아는 것으로
    주소를 만들어내고(확장의 93%가 URL 구조 추론), 열어 보면 엉뚱한 페이지라
    94%가 not_found 로 끝난다.

    걷어내는 것만으로는 모자란다 — 위키 한 장에서 보일러플레이트를 다 빼도 403개가
    남는다. 그래서 지금 쫓고 있는 **검색어와 앵커 텍스트가 겹치는 순**으로 줄
    세우고 상위 몇 개만 보여 준다. 목록은 강제가 아니라 안내다. 본문에 있는 링크는
    목록에 없어도 열리므로(`_page_links`), 추리기가 틀려도 막다른 길이 되지 않는다.
    """
    if not text or limit <= 0:
        return []
    wanted = _terms(query, question)
    seen: set[str] = set()
    scored: list[tuple[int, int, str, str]] = []
    for order, m in enumerate(_MD_LINK.finditer(text)):
        label, url = " ".join(m.group(1).split()), m.group(3)
        if not url.startswith(("http://", "https://")) or len(label) < 3:
            continue
        low = url.lower()
        if any(j in low for j in _JUNK) or budget.seen(url):
            continue
        key = _norm(url)
        if key in seen:
            continue
        seen.add(key)
        overlap = len(_terms(label) & wanted)
        scored.append((-overlap, order, label, url))
    scored.sort()
    return [(label, url) for _, _, label, url in scored[:limit]]


def _strip_visited_links(text: str, budget: Budget) -> tuple[str, int]:
    """이미 읽은 페이지로 가는 링크를 **앵커 텍스트만 남기고** 지운다.

    explorer 가 확장할 곳을 고르는 근거는 본문의 인라인 링크다. 이미 읽은 URL 이
    거기 그대로 남아 있으면 계속 고른다 — 사후에 막아도 턴은 이미 나갔다. 그래서
    선택지 자체에서 없앤다.

    앵커 텍스트는 남긴다. 링크를 통째로 지우면 문장이 깨지고, 그 단어가 본문의
    사실을 가리키는 경우가 많아 추출에 손해다. 지우는 것은 **갈 수 있다는 사실**
    뿐이다.
    """
    if not text or not budget.visited:
        return text, 0

    removed = 0

    def repl(m: "re.Match[str]") -> str:
        nonlocal removed
        anchor, url = m.group(1), m.group(3)
        if url.startswith(("http://", "https://")) and budget.seen(url):
            removed += 1
            return anchor
        return m.group(0)

    return _MD_LINK.sub(repl, text), removed


# harmony 채널 토큰. 대화 이력에 되넣으면 다음 요청에서 서버가 500 으로 죽는다.
# 메인 에이전트와 같은 이유·같은 처방이다(agent.py `_strip_special` 참고).
_SPECIAL = re.compile(r"<\|[^|>]{0,64}\|>")


def _assistant_message(reply: Any) -> dict[str, Any]:
    return {
        "role": "assistant",
        "content": _SPECIAL.sub("", reply.text or ""),
        "tool_calls": [history_tool_call(c) for c in reply.tool_calls],
    }


def _parse_arguments(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {"_raw": raw}
    return parsed if isinstance(parsed, dict) else {"_value": parsed}


# 굵은 표시는 선택이다. Search-o1 논문 Appendix A.1 의 RiD 지시는 마커를 굵게
# 쓰지 않으므로(`Final Information`), 그 형식도 받아야 베이스라인이 논문 그대로
# 돌아간다. 받아들이는 형태만 넓히며 기존 굵은 형식의 동작은 그대로다.
_FINAL = re.compile(r"(?:\*\*)?\s*Final Information\s*(?:\*\*)?", re.IGNORECASE)
_STATUS = re.compile(r"^[ \t]*\*\*\s*Status\s*:?\s*\*\*\s*:?\s*([a-z_]+)[ \t]*$",
                     re.IGNORECASE | re.MULTILINE)
_NOTHING = re.compile(r"no\s+helpful\s+information\s+found", re.IGNORECASE)


def _parse_final(text: str, *, allow_explanation: bool = False) -> tuple[str, str]:
    """`**Final Information**` 이후를 본문으로, `**Status:**` 를 상태로 읽는다.

    마커가 없으면 전체를 본문으로 본다 — 형식을 못 지켰다고 내용까지 버리면
    한 번의 형식 실수가 문항 하나를 통째로 날린다.
    """
    body = _SPECIAL.sub("", text or "").strip()
    if match := _FINAL.match(body):
        body = body[match.end() :].strip()

    status = ""
    pattern = (_STATUS if not allow_explanation else re.compile(
        r"^[ \t]*\*\*\s*Status\s*:?\s*\*\*\s*:?\s*"
        r"(answered|partial|not_found)(?:[ \t]*[\u2013\u2014:-][ \t]*[^\n]*)?[ \t]*$",
        re.IGNORECASE | re.MULTILINE))
    if found := list(pattern.finditer(body)):
        # Only the reader's trailing status is metadata; quoted child lines remain content.
        last = found[-1]
        if not body[last.end():].strip():
            status = last.group(1).lower()
            body = body[:last.start()].strip()
    if status not in STATUSES:
        status = ""

    # A child may be quoted as returning this phrase inside a useful parent note.
    # Only the standalone sentinel means an empty extraction.
    if not body or _NOTHING.fullmatch(body.strip(" \n\r\t.*_")):
        return ("", status or "not_found")
    return (body, status or "partial")


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out
