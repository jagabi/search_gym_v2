"""Jev-selected reading behind the main model's web_search (method `jevtree`).

    main web_search(query)                    the main model only writes queries
      → Jev: result_i per search result       entry score; top-e results (>= floor)
      → each entry page: candidate identification + condition verification + link_i
      → top-b links by link score are fetched (depth 2, then depth 3)
      → up to r pages alternating identification/verification ranks (>= floor)
        are read independently and their source quotations validated
      → results + structured notes and persistent candidates return to the main

Terms: entry width e (results opened per search, by entry score), branching
width b (links expanded per page, by link score), depth d, read budget r
(pages read per search, from both ranks), floor τ. Jev only ranks; it never
writes evidence. Each note passes through one reader call, never re-summarized.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import time
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable
from uuid import uuid4

import httpx

from urllib.parse import urlsplit

from .explorer import Document, _JUNK, _balanced_markdown_links, _content_fingerprint, _norm, _page_links
from .llm import LLM, Usage
from .jevtree_state import (CandidateMemory, CONDITION_PROMPT, READER_CONTRACT,
                            parse_conditions, parse_reading)
from .research_state import is_search_endpoint
from .trace import Trace

JEV_URL = "https://api.typesafe.ai/v1/systemone"
# Questions per Jev request. All share one state; larger pages are split.
LINKS_PER_REQUEST = 100
MAX_LINKS = 300

ENTRY_NOTE = (
    "`question` is the original research question. "
    "`search_results` are the results of `search_query` (titles, URLs, snippets only)."
)
STATE_NOTE = (
    "`question` is the original research question. "
    "`page_text` is the fetched page (possibly truncated)."
)
IDENTIFICATION_QUESTION = {
    "type": "noul",
    "instructions": (
        STATE_NOTE + " Does this page identify a concrete candidate through a distinctive "
        "condition or relation in `question_conditions`, narrowing the original question?"
    ),
    "criteria": {
        "true": "Names a plausible candidate and explicitly connects it to a distinguishing "
                "clue, or gives a concrete relation that substantially narrows the candidate set. "
                "A partial but distinctive identifying clue is useful; all conditions need not match.",
        "false": "Only shares a broad topic, common birthplace, generic date range or isolated "
                 "keyword without narrowing the target; or is unrelated, blocked or empty.",
    },
}
VERIFICATION_QUESTION = {
    "type": "noul",
    "instructions": STATE_NOTE + " Does this page explicitly confirm or refute a condition "
                    "in `question_conditions` for a concrete, plausible candidate for `question`?",
    "criteria": {
        "true": "A source statement links a plausible candidate to a requested date, entity, "
                "attribute or relation, letting that condition be checked. Explicit contradictory "
                "facts are useful too; merely not mentioning a condition is not a contradiction.",
        "false": "Only topical similarity or unrelated facts; no explicit candidate-condition "
                 "relation that can be checked. An error, blocked page or navigation only.",
    },
}
LINK_CRITERIA = {
    "true": "The anchor and nearby source text connect this link to a specific condition "
            "in question_conditions: identifying a candidate, connecting entities, or checking "
            "a candidate's missing fact or contradiction. A useful intermediate page counts "
            "even when it cannot answer the whole question by itself.",
    "false": "The link is navigation or site chrome, or leads to a topic unrelated to the "
             "facts the question asks for.",
}

ENTRY_CRITERIA = {
    "true": "Opening this result would likely give facts needed to answer the question or "
            "verify a candidate, either on the page itself or through pages it links to.",
    "false": "The result is unrelated, spam that only repeats query words, a search or "
             "listing page with no route to the needed facts, or otherwise not worth opening.",
}


@dataclass(slots=True)
class TreeNode:
    url: str
    depth: int
    parent: str = ""
    anchor: str = ""
    link_score: float | None = None
    evidence: float | None = None
    identification: float | None = None
    verification: float | None = None
    document: Document | None = None
    error: str = ""
    notes: str = ""
    read: bool = False
    reading: dict[str, Any] | None = None
    children: list["TreeNode"] = field(default_factory=list)
    # (link score, url, anchor) for links visible in this page's Jev view
    link_scores: list[tuple[float, str, str]] = field(default_factory=list)

    def log(self) -> dict[str, Any]:
        """Same shape as explorer logs so explorer.json/tree.svg keep working."""
        return {
            "depth": self.depth,
            "urls": [self.url],
            "anchor": self.anchor,
            "link_score": self.link_score,
            "evidence_score": self.evidence,
            "identification_score": self.identification,
            "verification_score": self.verification,
            "read": self.read,
            "status": ("not_found" if self.error else "partial" if self.read else "unread"),
            "error": self.error or None,
            "information": self.notes,
            "structured_reading": self.reading,
            "information_chars": len(self.notes),
            "turns": int(self.read),
            "opened": [c.log() for c in self.children],
        }


@dataclass(slots=True)
class JevUsage:
    """One search's usage; never shared between concurrent questions."""

    calls: int = 0
    attempts: int = 0
    input_tokens: int = 0
    failures: int = 0


class Jev:
    """TypeSafe System One client. Failures degrade to no ranking, never to a crash."""

    def __init__(self, model: str, timeout_s: float = 60.0) -> None:
        self.model = model
        self.key = os.environ.get("TYPESAFE_API_KEY", "")
        self._http = httpx.AsyncClient(timeout=timeout_s)

    async def noul(self, state: dict[str, Any], questions: dict[str, Any], trace: Trace,
                   *, usage: JevUsage | None = None,
                   context: dict[str, Any] | None = None) -> dict[str, float]:
        usage = usage if usage is not None else JevUsage()
        request_id = uuid4().hex
        body = {"model": self.model, "state": state, "questions": questions}
        # Exact request body, without authentication headers. Repeated attempts
        # refer to this event instead of duplicating a potentially large page.
        trace.event("jev.request", request_id=request_id, endpoint=JEV_URL,
                    context=context or {}, body=body)
        if not self.key:
            usage.failures += 1
            trace.event("jev.error", request_id=request_id, attempt=None,
                        error="TYPESAFE_API_KEY is not set", retryable=False)
            raise RuntimeError("TYPESAFE_API_KEY is not set")
        started = time.perf_counter()
        for attempt in range(3):
            attempt_started = time.perf_counter()
            usage.attempts += 1
            trace.event("jev.attempt", request_id=request_id, attempt=attempt)
            try:
                response = await self._http.post(
                    JEV_URL, json=body, headers={"Authorization": f"Bearer {self.key}"})
                # Save the complete body even for HTTP errors or invalid JSON.
                trace.event("jev.response", request_id=request_id, attempt=attempt,
                            duration_ms=round((time.perf_counter() - attempt_started) * 1000, 1),
                            status_code=response.status_code, response_text=response.text)
                if response.status_code >= 500 or response.status_code == 429:
                    raise httpx.HTTPStatusError("retryable", request=response.request, response=response)
                response.raise_for_status()
                payload = response.json()
                scores = {k: float(v.get("noul", 0.0))
                          for k, v in (payload.get("answers") or {}).items()}
                tokens = int((payload.get("usage") or {}).get("input_tokens") or 0)
                usage.calls += 1
                usage.input_tokens += tokens
                trace.event("jev.result", request_id=request_id, attempt=attempt,
                            duration_ms=round((time.perf_counter() - started) * 1000, 1),
                            scores=scores, usage=payload.get("usage") or {}, failed=False)
                return scores
            except (httpx.HTTPError, ValueError, TypeError, AttributeError) as exc:
                detail = getattr(getattr(exc, "response", None), "text", "")
                retryable = not (isinstance(exc, httpx.HTTPStatusError)
                                and 400 <= exc.response.status_code < 500
                                and exc.response.status_code != 429)
                trace.event("jev.error", request_id=request_id, attempt=attempt,
                            duration_ms=round((time.perf_counter() - attempt_started) * 1000, 1),
                            error=repr(exc), detail=detail,
                            retryable=retryable, will_retry=retryable and attempt < 2)
                if attempt == 2 or not retryable:
                    break
                await asyncio.sleep(1.5 * (attempt + 1))
        usage.failures += 1
        trace.event("jev.result", request_id=request_id, attempt=attempt,
                    duration_ms=round((time.perf_counter() - started) * 1000, 1),
                    scores={}, usage={}, failed=True)
        return {}

    async def aclose(self) -> None:
        await self._http.aclose()


_MD_ESCAPE = re.compile(r"\\([\\`*_{}\[\]()#+\-.!~])")


def _unescape(url: str) -> str:
    """Jina markdown escapes URL characters (e.g. Countryman\\_(album)); servers need the raw URL."""
    return _MD_ESCAPE.sub(r"\1", url)


def _anchors(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for _start, _end, label, url in _balanced_markdown_links(text):
        out.setdefault(_norm(_unescape(url)), _unescape(re.sub(r"\s+", " ", label).strip())[:120])
    return out


_SEARCH_HOSTS = ("scholar.google.", "www.jstor.org/action/dobasicsearch", "/search?", "/search/?")
_WIKI = re.compile(r"^([a-z\-]+)\.(?:m\.)?(wikipedia|wikiquote|wikisource|wiktionary)\.org$")


def _other_language_wiki(url: str, page_url: str) -> bool:
    """Interlanguage copies of the same article repeat content in another language."""
    try:
        here, there = urlsplit(page_url).hostname or "", urlsplit(url).hostname or ""
    except ValueError:
        return False
    a, b = _WIKI.match(here.lower()), _WIKI.match(there.lower())
    return bool(a and b and a.group(2) == b.group(2) and a.group(1) != b.group(1))


def candidate_links(text: str, page_url: str, skip: set[str]) -> list[tuple[str, str]]:
    """Links visible in the (truncated) page Jev sees, minus self/visited/junk."""
    anchors = _anchors(text)
    here = _norm(page_url)
    out, seen = [], set()
    for raw in _page_links(text, balanced=True).values():
        position = text.find(raw)
        raw = _unescape(raw)
        norm = _norm(raw)
        lower = raw.lower()
        if norm in seen:
            continue
        seen.add(norm)
        if norm == here or norm in skip or is_search_endpoint(raw):
            continue
        if any(j in lower for j in _JUNK + _SEARCH_HOSTS) or "r.jina.ai" in lower:
            continue
        if _other_language_wiki(raw, page_url):
            continue
        out.append((position, raw, anchors.get(norm, "")))
    out.sort()  # page order
    return [(raw, anchor) for _, raw, anchor in out[:MAX_LINKS]]


class JevTree:
    def __init__(
        self,
        *,
        jev: Jev,
        llm: LLM,
        fetch: Callable[[str], Awaitable[Document]],
        reader_prompt: str,
        reader_max_tokens: int,
        entries: int,
        branch: int,
        depth: int,
        reads: int,
        floor: float,
        jev_page_tokens: int,
        visited: set[str],
    ) -> None:
        self.jev, self.llm, self.fetch = jev, llm, fetch
        self.reader_prompt = reader_prompt
        self.reader_max_tokens = reader_max_tokens
        self.entries = entries
        self.branch, self.depth, self.reads, self.floor = branch, depth, reads, floor
        self.jev_page_tokens = jev_page_tokens
        self.visited = visited  # per question, across main fetches
        self.contents: dict[str, str] = {}  # body fingerprint -> first URL (redirect copies)
        self.conditions: list[dict[str, str]] = []
        self.memory = CandidateMemory()

    async def prepare(self, question: str, trace: Trace, usage: Usage) -> None:
        """Extract verbatim question conditions once, without main hypotheses."""
        if self.conditions:
            return
        messages = [{"role": "system", "content": CONDITION_PROMPT},
                    {"role": "user", "content": question}]
        for attempt in range(2):
            trace.event("jevtree.conditions_request", attempt=attempt, messages=messages)
            try:
                reply = await self.llm.chat(messages, max_tokens=4096, usage=usage, tool_choice="none")
                trace.event("jevtree.conditions_response", attempt=attempt, text=reply.text,
                            reasoning=reply.reasoning, finish_reason=reply.finish_reason,
                            prompt_tokens=reply.prompt_tokens, completion_tokens=reply.completion_tokens)
                if reply.truncated or reply.tool_calls:
                    raise ValueError("Incomplete condition extraction")
                self.conditions = parse_conditions(reply.text, question)
                break
            except Exception as exc:
                trace.event("jevtree.conditions_error", attempt=attempt, error=repr(exc))
                messages.append({"role": "user", "content":
                    "Return complete JSON with a conditions array of exact excerpts copied from the question."})
        if not self.conditions:
            self.conditions = [{"id": "C1", "text": question}]
            trace.event("jevtree.conditions_fallback", reason="Use original question without inferred constraints")
        trace.event("jevtree.conditions", conditions=self.conditions)

    def checkpoint(self) -> str:
        return self.memory.render(self.conditions)

    def _select_readers(self, nodes: list[TreeNode]) -> list[TreeNode]:
        """Alternate identification/verification slots, deduplicating both ranks."""
        queues = [sorted((n for n in nodes if (getattr(n, score) or 0) >= self.floor),
                         key=lambda n: getattr(n, score) or 0, reverse=True)
                  for score in ("identification", "verification")]
        selected: list[TreeNode] = []
        seen: set[str] = set()
        while len(selected) < self.reads:
            added = False
            for queue in queues:
                while queue and queue[0].url in seen:
                    queue.pop(0)
                if queue and len(selected) < self.reads:
                    node = queue.pop(0)
                    selected.append(node)
                    seen.add(node.url)
                    added = True
            if not added:
                break
        return selected

    async def run_search(self, query: str, results: list[dict[str, Any]], *, question: str,
                         main_reasoning: str, trace: Trace, usage: Usage) -> tuple[dict[str, Any], str, dict[str, int]]:
        """Grow trees and read both ranks; main_reasoning is a legacy unused argument."""
        await self.prepare(question, trace, usage)
        stats = {"fetched": 0, "fetch_failed": 0, "jev_requests": 0, "links_scored": 0, "entries": 0}
        jev_usage = JevUsage()
        search_id = uuid4().hex
        search = TreeNode(url=f"search: {query}", depth=0)
        candidates = []
        for row in results:
            url = str(row.get("link") or "")
            if not url.startswith(("http://", "https://")) or is_search_endpoint(url):
                continue
            if _norm(url) in self.visited:
                continue
            candidates.append((url, str(row.get("title") or ""), str(row.get("snippet") or "")))
        if candidates:
            state = {"question": question, "question_conditions": self.conditions, "search_query": query,
                     "search_results": [{"id": f"result_{i}", "title": t, "url": u, "snippet": sn}
                                        for i, (u, t, sn) in enumerate(candidates)]}
            questions = {f"result_{i}": {
                "type": "noul",
                "instructions": (ENTRY_NOTE + f" Would opening `search_results` item result_{i} "
                                 f"({u}) help answer `question`?"),
                "criteria": ENTRY_CRITERIA,
            } for i, (u, _t, _sn) in enumerate(candidates)}
            scores = await self.jev.noul(
                state, questions, trace, usage=jev_usage,
                context={"search_id": search_id, "query": query, "phase": "entry"})
            search.link_scores = [(scores.get(f"result_{i}", 0.0), u, t)
                                  for i, (u, t, _sn) in enumerate(candidates)
                                  if scores.get(f"result_{i}", 0.0) >= self.floor]
            trace.event("jevtree.entry_scores", search_id=search_id, query=query,
                        scores=sorted(((round(scores.get(f"result_{i}", 0.0), 3), u)
                                       for i, (u, _t, _sn) in enumerate(candidates)), reverse=True))
        level = await self._expand(search, trace, stats, width=self.entries)
        stats["entries"] = len(level)
        nodes = list(level)
        while level:
            await asyncio.gather(*(self._score(n, question, trace, stats,
                                               jev_usage, search_id) for n in level))
            if level[0].depth >= self.depth:
                break
            nxt: list[TreeNode] = []
            for parent in level:
                nxt.extend(await self._expand(parent, trace, stats))
            nodes.extend(nxt)
            level = nxt

        to_read = self._select_readers(nodes)
        for node in to_read:
            node.read = True
        trace.event("jevtree.selection", search_id=search_id, query=query, nodes=len(nodes),
                    read=[(n.url, n.evidence) for n in to_read],
                    unread=[(n.url, n.evidence) for n in nodes if not n.read])
        await asyncio.gather(*(self._read(n, question, trace, usage) for n in to_read))
        # Stable candidate/evidence IDs independent of reader completion order.
        for node in to_read:
            if node.reading is not None:
                self.memory.ingest(node.reading, node.url)
        trace.event("jevtree.candidate_state", search_id=search_id,
                    candidates=self.memory.candidates, evidence=self.memory.evidence)
        stats["nodes"] = len(nodes)
        stats["reads"] = len(to_read)
        stats["max_depth"] = max((n.depth for n in nodes), default=0)
        stats.update(jev_requests=jev_usage.calls, jev_attempts=jev_usage.attempts,
                     jev_input_tokens=jev_usage.input_tokens, jev_failures=jev_usage.failures)
        trace.event("jevtree.search_end", search_id=search_id, query=query, stats=stats)
        log = {**search.log(), "search_id": search_id, "query": query, "entry": "search", "jevtree": stats}
        return log, self._render(search, nodes, to_read), stats

    async def _score(self, node: TreeNode, question: str, trace: Trace,
                     stats: dict[str, int], jev_usage: JevUsage, search_id: str) -> None:
        page, _ = await self.llm.cap(node.document.content, self.jev_page_tokens)
        state = {"question": question, "question_conditions": self.conditions,
                 "page_url": node.url, "page_text": page}
        links = (candidate_links(page, node.url, self.visited)
                 if node.depth < self.depth else [])
        questions: list[dict[str, Any]] = [{"candidate_identification": IDENTIFICATION_QUESTION,
                                         "condition_verification": VERIFICATION_QUESTION}]
        for start in range(0, len(links), LINKS_PER_REQUEST):
            chunk = {}
            for i, (url, anchor) in enumerate(links[start:start + LINKS_PER_REQUEST], start):
                position = page.find(url)
                if position < 0 and anchor:
                    position = page.find(anchor)
                # The full page is already in state; keep this locator short and
                # do not duplicate long URLs inside every surrounding excerpt.
                nearby = (page[max(0, position - 60):position] + " [link] "
                          + page[position + len(url):position + len(url) + 60]) if position >= 0 else ""
                chunk[f"link_{i}"] = {
                    "type": "noul",
                    "instructions": ("Would this link identify a candidate or check a question_condition? Source data: "
                                     + json.dumps({"url": url, "anchor": anchor, "nearby_text": nearby},
                                                  ensure_ascii=False)),
                    "criteria": LINK_CRITERIA,
                }
            if start == 0:
                questions[0].update(chunk)
            else:
                questions.append(chunk)
        scores: dict[str, float] = {}
        results = await asyncio.gather(*(self.jev.noul(
            state, q, trace, usage=jev_usage,
            context={"search_id": search_id, "phase": "page", "page_url": node.url,
                     "parent_url": node.parent, "depth": node.depth,
                     "chunk_index": i, "chunks": len(questions)},
        ) for i, q in enumerate(questions)))
        for part in results:
            scores.update(part)
        stats["links_scored"] += len(links)
        node.identification = scores.get("candidate_identification")
        node.verification = scores.get("condition_verification")
        # Legacy reports use evidence; selection uses the two separate ranks.
        node.evidence = max(node.identification or 0, node.verification or 0)
        node.link_scores = [(scores.get(f"link_{i}", 0.0), url, anchor)
                            for i, (url, anchor) in enumerate(links)]
        trace.event("jevtree.scored", search_id=search_id, url=node.url, depth=node.depth, evidence=node.evidence,
                    identification=node.identification, verification=node.verification,
                    links=len(links), page_truncated=len(page) < len(node.document.content),
                    link_scores=[{"id": f"link_{i}", "url": url, "anchor": anchor,
                                  "score": scores.get(f"link_{i}")}
                                 for i, (url, anchor) in enumerate(links)],
                    top_links=sorted(node.link_scores, reverse=True)[:8])

    async def _expand(self, parent: TreeNode, trace: Trace, stats: dict[str, int],
                      width: int | None = None) -> list[TreeNode]:
        """Fetch the top links by score; a failed or duplicate fetch yields to the next one."""
        width = self.branch if width is None else width
        ranked = sorted(parent.link_scores, key=lambda x: x[0], reverse=True)
        kids: list[TreeNode] = []
        cursor = 0
        while len(kids) < width and cursor < len(ranked) and cursor < 2 * width:
            batch = []
            while len(batch) + len(kids) < width and cursor < len(ranked) and cursor < 2 * width:
                score, url, anchor = ranked[cursor]
                cursor += 1
                if _norm(url) in self.visited:
                    continue
                self.visited.add(_norm(url))
                batch.append(TreeNode(url=url, depth=parent.depth + 1,
                                      parent=parent.url if parent.depth else "",
                                      anchor=anchor, link_score=score))
            if not batch:
                break
            docs = await asyncio.gather(*(self.fetch(n.url) for n in batch))
            for node, doc in zip(batch, docs):
                stats["fetched"] += 1
                same = None
                if not doc.is_error:
                    owners = [self.contents.setdefault(k, node.url) for k in _same_page_keys(doc)]
                    same = next((o for o in owners if o != node.url), None)
                if same and same != node.url:
                    stats["duplicates"] = stats.get("duplicates", 0) + 1
                    node.error = f"same content as {same}"
                    parent.children.append(node)
                    trace.event("jevtree.duplicate", url=node.url, same_as=same)
                    continue
                if doc.is_error:
                    stats["fetch_failed"] += 1
                    node.error = doc.content[:200]
                    parent.children.append(node)
                    trace.event("jevtree.fetch_failed", url=node.url, parent=parent.url)
                    continue
                node.document = doc
                parent.children.append(node)
                kids.append(node)
        return kids

    async def _read(self, node: TreeNode, question: str,
                    trace: Trace, usage: Usage) -> None:
        state = {"question": question, "question_conditions": self.conditions,
                 "page_url": node.url, "page_text": node.document.content}
        messages = [{"role": "system", "content": self.reader_prompt + "\n\n" + READER_CONTRACT},
                    {"role": "user", "content": json.dumps(state, ensure_ascii=False, indent=1)}]
        for attempt in range(2):
            trace.event("jevtree.reader_request", url=node.url, attempt=attempt, messages=messages)
            try:
                reply = await self.llm.chat(messages, max_tokens=self.reader_max_tokens, usage=usage,
                                            tool_choice="none")
            except Exception as exc:  # Keep the tree; report the unread page honestly.
                trace.event("jevtree.reader_error", url=node.url, error=repr(exc))
                node.notes = f"(Reader failed: {exc!r}. This does not mean the page lacks evidence.)"
                return
            text = _SPECIAL.sub("", reply.text or "").strip()
            trace.event("jevtree.read", url=node.url, attempt=attempt, chars=len(text),
                        prompt_tokens=reply.prompt_tokens, completion_tokens=reply.completion_tokens,
                        finish_reason=reply.finish_reason, reasoning=reply.reasoning, text=text)
            try:
                if not text or reply.truncated or reply.tool_calls:
                    raise ValueError("Incomplete reader output")
                node.reading = parse_reading(text, node.document.content, self.conditions)
                node.notes = json.dumps(node.reading, ensure_ascii=False, indent=1)
                trace.event("jevtree.reader_validated", url=node.url, reading=node.reading)
                return
            except (ValueError, TypeError) as exc:
                trace.event("jevtree.reader_invalid", url=node.url, attempt=attempt, error=str(exc))
                messages.append({"role": "user", "content":
                    f"Invalid output: {exc}. Return complete JSON following the schema. "
                    "Quotes must be verbatim page excerpts containing their candidate name; "
                    "use empty arrays where the source does not support an extraction."})
        node.notes = "(Reader output failed source/schema validation; raw output is retained in the trace.)"

    @staticmethod
    def _render(search: TreeNode, nodes: list[TreeNode], read: list[TreeNode]) -> str:
        entries = [n for n in search.children if not n.error]
        if not entries:
            return ("Reading: no search result was judged worth opening, or none could be "
                    "opened. Change the clue or the source type in the next query.")
        lines = [f"Reading: opened {len(entries)} result(s) and followed their links up to depth "
                 f"{max(n.depth for n in nodes)}; {len(nodes)} pages fetched, {len(read)} read. "
                 "Each block is one page's notes, written by a reader of that page alone."]
        by_url = {n.url: n for n in nodes}
        for i, node in enumerate(read):
            head = f"\n## [P{i}] {node.url} (depth {node.depth}"
            if node.parent:
                path, cur = [], node
                while cur is not None and cur.parent:
                    path.append(f'"{cur.anchor or cur.url}"')
                    cur = by_url.get(cur.parent)
                head += f", reached from {cur.url if cur else '?'} via " + " → ".join(reversed(path))
            else:
                head += ", search result"
            if node.evidence is not None:
                head += (f", identification {node.identification or 0:.2f}, "
                         f"verification {node.verification or 0:.2f}")
            lines.append(head + ")")
            lines.append(node.notes or "(no notes)")
        unread = [n for n in nodes if not n.read]
        if unread:
            lines.append("\nOther fetched pages, not selected within the two-rank reading budget:")
            for n in unread:
                tag = f"failed: {n.error[:80]}" if n.error else (
                    f"evidence {n.evidence:.2f}" if n.evidence is not None else "unscored")
                lines.append(f'- {n.url} — "{n.anchor}" ({tag})')
        return "\n".join(lines)


def _same_page_keys(doc: Document) -> list[str]:
    """Redirect aliases (e.g. Wikipedia) return the same article under another URL."""
    keys = [_content_fingerprint(doc.content)]
    title = re.search(r"^Title:\s*(.+?)\s*$", doc.content[:1000], re.MULTILINE)
    host = (urlsplit(doc.url).hostname or "").lower()
    if title and len(title.group(1)) > 8:
        keys.append(f"title:{host}:{title.group(1).lower()}")
    return keys


_SPECIAL = re.compile(r"<\|[^|>]{0,64}\|>")


