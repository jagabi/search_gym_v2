"""Jev-selected reading behind the main model's web_search (method `jevtree`).

    main web_search(query)                    the main model only writes queries
      → Jev: result_i per search result       entry score; top-e results (>= floor)
      → 5k-token prefix: original answer + current query answer + link_i
      → top-b links are candidates for level or budgeted LDS expansion
      → separate original-answer/query-answer reader quotas (>= floor)
        are read independently in free-form prose
      → results + reader notes return verbatim to the main

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
from .jevtree_input import LINK_CRITERIA, complete_prefix, page_requests
from .research_state import is_search_endpoint
from .trace import Trace

JEV_URL = "https://api.typesafe.ai/v1/systemone"
# Questions per Jev request. All share one state; larger pages are split.
LINKS_PER_REQUEST = 100
MAX_LINKS = 300

SEARCH_FOLLOWUP = """Next action:
The results above were obtained using the query {query}.

Use these results together with all evidence collected so far. If they support
an answer to the original question, return the final answer instead of searching again.

If you cannot answer yet and another search is available:
- If you found a promising candidate or a new connection, use it to search for
  a specific fact that is still unverified.
- If you gained no new lead, abandon the current approach. Start from a different
  clue, relationship, or type of source in the original question.
- Do not repeat the previous query with only a number, a few keywords, or synonyms
  changed. The next query must seek different information, not rephrase the same search."""

ENTRY_NOTE = "Prioritize answering search_query; direct evidence for question also counts."
IDENTIFICATION_QUESTION = {
    "type": "noul",
    "instructions": "Does page_text explicitly answer question?",
    "criteria": {"true": "Answer directly supported.", "false": "No explicit answer."},
}
QUERY_ANSWER_QUESTION = {
    "type": "noul",
    "instructions": "Does page_text provide evidence that answers search_query, even if question remains unresolved?",
    "criteria": {"true": "Query answer supported by source facts.", "false": "Mere mention or no query answer."},
}

ENTRY_CRITERIA = {
    "true": "Helps answer the query or directly answers the original question.",
    "false": "Unrelated or spam.",
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
    query_answer: float | None = None
    reader_objective: str = ""
    document: Document | None = None
    error: str = ""
    notes: str = ""
    read: bool = False
    children: list["TreeNode"] = field(default_factory=list)
    # (link score, url, anchor) for links visible in this page's Jev view
    link_scores: list[tuple[float, str, str]] = field(default_factory=list)
    node_id: str = ""
    root_id: str = ""
    rank: int = 0
    discrepancy: int = 0

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
            "direct_answer": self.identification,
            "query_answer": self.query_answer,
            "reader_objective": self.reader_objective,
            "read": self.read,
            "status": ("not_found" if self.error else "partial" if self.read else "unread"),
            "error": self.error or None,
            "information": self.notes,
            "information_chars": len(self.notes),
            "turns": int(self.read),
            "opened": [c.log() for c in self.children],
            "node_id": self.node_id, "root_id": self.root_id,
            "sibling_rank": self.rank, "discrepancy": self.discrepancy,
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


def candidate_links(text: str, page_url: str, skip: set[str], *,
                    trace: Trace | None = None) -> list[tuple[str, str]]:
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
        if norm == here or norm in skip:
            continue
        try:
            search_endpoint = is_search_endpoint(raw)
        except ValueError as exc:
            if trace is not None:
                trace.event("jevtree.invalid_link", url=raw, parent=page_url,
                            phase="page", error=str(exc))
            continue
        if search_endpoint:
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
        strategy: str = "level",
        fetch_budget: int = 40,
        direct_reads: int | None = None,
        query_reads: int | None = None,
        reader_status: dict | None = None,
    ) -> None:
        self.jev, self.llm, self.fetch = jev, llm, fetch
        self.reader_status = dict(reader_status or {})
        self.reader_prompt = reader_prompt
        self.reader_max_tokens = reader_max_tokens
        self.entries = entries
        self.branch, self.depth, self.reads, self.floor = branch, depth, reads, floor
        self.jev_page_tokens = jev_page_tokens
        self.visited = visited  # per question, across main fetches
        if strategy not in ("level", "lds"):
            raise ValueError(f"Unknown JEV strategy: {strategy}")
        if min(entries, branch, depth, fetch_budget) < 1 or (strategy == "lds" and fetch_budget < entries):
            raise ValueError("JEV limits must be positive; LDS fetch budget must cover starting roots")
        self.strategy, self.fetch_budget = strategy, fetch_budget
        if direct_reads is None:
            direct_reads = reads - query_reads if query_reads is not None else reads // 3
        if query_reads is None:
            query_reads = reads - direct_reads
        if min(direct_reads, query_reads) < 0 or direct_reads + query_reads != reads:
            raise ValueError("JEV direct/query reader budgets must be nonnegative and sum to reads")
        self.reader_budgets = {"direct_answer": direct_reads, "query_answer": query_reads}
        self.contents: dict[str, str] = {}  # body fingerprint -> first URL (redirect copies)

    def _select_readers(self, nodes: list[TreeNode]) -> list[TreeNode]:
        """Reserve original-answer slots first, then query slots; read each URL once.

        An overlap consumes only the direct slot, allowing another query page.
        Insufficient eligible pages leave slots unused; budgets do not transfer.
        """
        selected: list[TreeNode] = []
        seen: set[str] = set()
        for objective, score in (("direct_answer", "identification"), ("query_answer", "query_answer")):
            queue = sorted((n for n in nodes if (getattr(n, score) or 0) >= self.floor),
                           key=lambda n: getattr(n, score) or 0, reverse=True)
            used = 0
            for node in queue:
                if used >= self.reader_budgets[objective]:
                    break
                if node.url in seen:
                    continue
                node.reader_objective = objective
                selected.append(node)
                seen.add(node.url)
                used += 1
        return selected

    async def run_search(self, query: str, results: list[dict[str, Any]], *, question: str,
                         main_reasoning: str = "", trace: Trace, usage: Usage) -> tuple[dict[str, Any], str, dict[str, int]]:
        """Grow trees and read both ranks; main_reasoning is a legacy unused argument."""
        stats = {"fetched": 0, "fetch_failed": 0, "jev_requests": 0, "links_scored": 0, "entries": 0}
        jev_usage = JevUsage()
        search_id = uuid4().hex
        search = TreeNode(url=f"search: {query}", depth=0)
        candidates = []
        for row in results:
            url = str(row.get("link") or "")
            if not url.startswith(("http://", "https://")):
                continue
            try:
                search_endpoint = is_search_endpoint(url)
            except ValueError as exc:
                trace.event("jevtree.invalid_link", url=url, phase="entry",
                            search_id=search_id, error=str(exc))
                continue
            if search_endpoint:
                continue
            if _norm(url) in self.visited:
                continue
            candidates.append((url, str(row.get("title") or ""), str(row.get("snippet") or "")))
        if candidates:
            state = {"question": question, "search_query": query,
                     "search_results": [{"id": f"result_{i}", "title": t, "url": u, "snippet": sn}
                                        for i, (u, t, sn) in enumerate(candidates)]}
            questions = {f"result_{i}": {
                "type": "noul",
                "instructions": f"Would result_{i} help find an answer? " + ENTRY_NOTE,
                "criteria": ENTRY_CRITERIA,
            } for i, (u, _t, _sn) in enumerate(candidates)}
            scores = await self.jev.noul(
                state, questions, trace, usage=jev_usage,
                context={"search_id": search_id, "query": query, "phase": "entry"})
            search.link_scores = [(scores.get(f"result_{i}", 0.0), u, t)
                                  for i, (u, t, _sn) in enumerate(candidates)
                                  if (f"result_{i}" in scores if self.strategy == "lds"
                                      else scores.get(f"result_{i}", 0.0) >= self.floor)]
            trace.event("jevtree.entry_scores", search_id=search_id, query=query,
                        scores=sorted(((round(scores.get(f"result_{i}", 0.0), 3), u)
                                       for i, (u, _t, _sn) in enumerate(candidates)), reverse=True))
        lds = None
        if self.strategy == "lds":
            from .lds import grow_lds
            nodes, lds = await grow_lds(self, search, question, trace, stats, jev_usage, search_id)
        else:
            level = await self._expand(search, trace, stats, width=self.entries)
            stats["entries"] = len(level)
            nodes = list(level)
            while level:
                await asyncio.gather(*(self._score(n, question, trace, stats,
                                                   jev_usage, search_id, query=query) for n in level))
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
        if lds:
            lds.emit("reader_selection", "Select pages for free-form reading", to_read,
                     selected_ids=[n.node_id for n in to_read], budgets=self.reader_budgets)
        trace.event("jevtree.selection", search_id=search_id, query=query, nodes=len(nodes),
                    budgets=self.reader_budgets,
                    objectives=[{"url": n.url, "objective": n.reader_objective} for n in to_read],
                    read=[(n.url, n.evidence) for n in to_read],
                    unread=[(n.url, n.evidence) for n in nodes if not n.read])
        await asyncio.gather(*(self._read(n, question, trace, usage, query=query) for n in to_read))
        stats["nodes"] = len(nodes)
        stats["reads"] = len(to_read)
        stats["direct_reads"] = sum(n.reader_objective == "direct_answer" for n in to_read)
        stats["query_reads"] = sum(n.reader_objective == "query_answer" for n in to_read)
        stats["max_depth"] = max((n.depth for n in nodes), default=0)
        stats.update(jev_requests=jev_usage.calls, jev_attempts=jev_usage.attempts,
                     jev_input_tokens=jev_usage.input_tokens, jev_failures=jev_usage.failures)
        trace.event("jevtree.search_end", search_id=search_id, query=query, stats=stats)
        log = {**search.log(), "search_id": search_id, "query": query, "entry": "search", "jevtree": stats}
        if lds:
            lds.emit("search_end", "Search finished; reader notes saved", nodes, stats=dict(stats))
            log["lds"] = lds.export(stats)
            lds.save(stats)
        return log, self._render(search, nodes, to_read), stats

    async def _score(self, node: TreeNode, question: str, trace: Trace,
                     stats: dict[str, int], jev_usage: JevUsage, search_id: str, *, query: str) -> None:
        source = node.document.content
        page, excerpt_cut = await self.llm.cap(source, self.jev_page_tokens)
        page = complete_prefix(source, page)
        links = (candidate_links(page, node.url, self.visited, trace=trace)
                 if node.depth < self.depth else [])
        packets = page_requests(
            question=question, search_query=query, page_url=node.url, page=page, links=links,
            page_questions={"direct_answer": IDENTIFICATION_QUESTION,
                            "query_answer": QUERY_ANSWER_QUESTION},
            links_per_request=LINKS_PER_REQUEST)
        trace.event("jevtree.input_compacted", search_id=search_id, url=node.url,
                    source_chars=len(source), excerpt_chars=len(page), excerpt_truncated=excerpt_cut,
                    links=len(links), chunks=len(packets),
                    request_chars=sum(len(json.dumps({"state": s, "questions": q}, ensure_ascii=False))
                                      for s, q in packets))
        scores: dict[str, float] = {}
        results = await asyncio.gather(*(self.jev.noul(
            state, q, trace, usage=jev_usage,
            context={"search_id": search_id, "phase": "page", "page_url": node.url,
                     "parent_url": node.parent, "depth": node.depth,
                     "chunk_index": i, "chunks": len(packets)},
        ) for i, (state, q) in enumerate(packets)))
        for part in results:
            scores.update(part)
        stats["links_scored"] += len(links)
        # Preserve historical report fields while exposing the new meanings explicitly.
        node.identification = scores.get("direct_answer")
        node.query_answer = scores.get("query_answer")
        # Legacy reports use evidence; selection uses the two separate ranks.
        node.evidence = max(node.identification or 0, node.query_answer or 0)
        node.link_scores = [(scores.get(f"link_{i}", 0.0), url, anchor)
                            for i, (url, anchor) in enumerate(links)
                            if self.strategy != "lds" or f"link_{i}" in scores]
        trace.event("jevtree.scored", search_id=search_id, url=node.url, depth=node.depth, evidence=node.evidence,
                    identification=node.identification, verification=node.verification,
                    direct_answer=node.identification, query_answer=node.query_answer,
                    links=len(links), page_truncated=len(page) < len(source),
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
                    trace: Trace, usage: Usage, *, query: str) -> None:
        state = {"question": question, "search_query": query,
                 "page_url": node.url, "page_text": node.document.content}
        messages = [{"role": "system", "content": self.reader_prompt},
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
            if text:
                # Pass useful prose through even when incomplete. No format or
                # quotation validator may discard the reader's findings.
                node.notes = text + ("\n[Reader output truncated.]" if reply.truncated else "")
                return
            messages.append({"role": "user", "content":
                "Return your page notes as free-form prose now. No tool calls."})
        node.notes = "(Reader returned no notes. This does not mean the page lacks evidence.)"

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
                head += (f", direct_answer {node.identification or 0:.2f}, "
                         f"query_answer {node.query_answer or 0:.2f}")
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


