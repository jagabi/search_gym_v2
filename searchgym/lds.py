"""Online rank-only LDS with deterministic root rounds and replayable events.

Fetch+evaluation may overlap across roots in a round. The next round waits for
that round, so response speed cannot change allocation or duplicate ownership.
Candidates only exist after their parent has been fetched and evaluated.
"""
from __future__ import annotations

import asyncio
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from .explorer import Document, _norm


class LDSRecord:
    def __init__(self, tree, search, trace, stats, search_id):
        self.tree, self.trace, self.stats = tree, trace, stats
        self.search_id, self.query = search_id, search.url.removeprefix("search: ")
        self.nodes, self.states, self.actions = {}, {}, []
        self.limit = 0
        self.origin = time.perf_counter()
        self.directory = (Path(trace.path).parent / "lds" / search_id
                          if getattr(trace, "path", None) else None)
        if self.directory:
            (self.directory / "pages").mkdir(parents=True, exist_ok=True)
        self.config = dict(strategy="lds", version=2, entries=tree.entries,
                           reader_budgets=tree.reader_budgets,
                           page_score_keys=["direct_answer", "query_answer"],
                           depth=tree.depth, candidates_per_parent=tree.branch,
                           fetch_budget=tree.fetch_budget, entry_floor=None,
                           discrepancy="non-first child costs 1; roots all start at 0",
                           tie_break="original sibling order", alternative_order="early",
                           allocation="one candidate per root per round; round barrier",
                           jina_base_url=os.getenv("JINA_BASE_URL", "https://r.jina.ai"),
                           jina_rpm=os.getenv("JINA_RPM", "auto"),
                           jina_max_concurrent=int(os.getenv("JINA_MAX_CONCURRENT", "50")))

    def add(self, node, parent_id=""):
        node.node_id = f"n{len(self.nodes)+1:04d}"
        node.root_id = self.nodes[parent_id].root_id if parent_id else node.node_id
        self.nodes[node.node_id] = node
        self.states[node.node_id] = dict(parent_id=parent_id, status="pending", children=[])

    def view(self, node):
        return dict(self.states[node.node_id], id=node.node_id, root_id=node.root_id,
                    url=node.url, anchor=node.anchor, depth=node.depth, rank=node.rank,
                    discrepancy=node.discrepancy, score=node.link_score,
                    direct_answer=node.identification, query_answer=node.query_answer,
                    reader_objective=node.reader_objective,
                    error=node.error, read=node.read, notes=node.notes)

    def emit(self, kind, reason, nodes=(), **extra):
        event = dict(action=len(self.actions)+1, kind=kind, reason=reason,
                     elapsed_ms=round((time.perf_counter()-self.origin)*1000, 1),
                     timestamp=datetime.now(timezone.utc).isoformat(),
                     discrepancy_limit=self.limit, fetch_attempts=self.stats["fetched"],
                     updates=[self.view(n) for n in nodes], **extra)
        self.actions.append(event)
        self.trace.event("jevtree.lds_action", search_id=self.search_id,
                         action_kind=kind, search_elapsed_ms=event["elapsed_ms"],
                         **{k:v for k,v in event.items() if k not in ("kind", "elapsed_ms")})
        if self.directory:
            with (self.directory / "actions.jsonl").open("a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False)+"\n")

    def export(self, stats):
        return dict(schema="searchgym.lds/1", search_id=self.search_id, query=self.query,
                    config=self.config, stats=dict(stats),
                    nodes=[self.view(n) for n in self.nodes.values()], actions=self.actions)

    def save(self, stats):
        if self.directory:
            tmp=self.directory / "structure.tmp"
            tmp.write_text(json.dumps(self.export(stats), ensure_ascii=False, indent=2), encoding="utf-8")
            tmp.replace(self.directory / "structure.json")


async def grow_lds(tree, search, question, trace, stats, jev_usage, search_id):
    from .jevtree import TreeNode, _same_page_keys

    record = LDSRecord(tree, search, trace, stats, search_id)
    children, successful = {}, []
    root_candidates = []
    seen = set()
    for rank, (score, url, anchor) in enumerate(sorted(search.link_scores, key=lambda x: -x[0]), 1):
        if _norm(url) in seen or _norm(url) in tree.visited:
            continue
        seen.add(_norm(url))
        node = TreeNode(url=url, depth=1, anchor=anchor, link_score=score, rank=rank)
        record.add(node)
        root_candidates.append(node)
    record.emit("entry_ranked", "Entry JEV results; root score floor disabled in LDS", root_candidates)

    async def process(batch):
        reserved=[]
        for node in batch:
            if stats["fetched"] >= tree.fetch_budget:
                break
            if _norm(node.url) in tree.visited:
                record.states[node.node_id]["status"] = "skipped_visited"
                record.emit("skip", "URL already reserved or fetched; no extra fetch charged", [node])
                continue
            tree.visited.add(_norm(node.url))
            stats["fetched"] += 1
            record.states[node.node_id].update(status="reserved", fetch_order=stats["fetched"])
            parent_id=record.states[node.node_id]["parent_id"]
            (record.nodes[parent_id] if parent_id else search).children.append(node)
            reserved.append(node)
            record.emit("select", "Rank-only LDS selection; one candidate per root in this round", [node])

        async def fetch_one(node):
            started=time.perf_counter()
            record.states[node.node_id]["status"]="fetching"
            record.emit("fetch_start", "Fetch requested; no children are known yet", [node])
            try:
                doc=await tree.fetch(node.url)
            except Exception as exc:
                doc=Document(url=node.url, content=repr(exc), is_error=True)
            record.states[node.node_id].update(status="fetch_returned",
                fetch_duration_ms=round((time.perf_counter()-started)*1000,1),
                content_chars=len(doc.content), retrieval=doc.retrieval)
            if record.directory:
                path=record.directory / "pages" / f"{node.node_id}.md"
                path.write_text(doc.content,encoding="utf-8")
                record.states[node.node_id]["document_path"]=f"pages/{node.node_id}.md"
            record.emit("fetch_end", "Fetch returned; evaluation still pending", [node])
            return doc

        docs=await asyncio.gather(*(fetch_one(n) for n in reserved))
        ready=[]
        # Commit in scheduled order, not network-completion order.
        for node,doc in zip(reserved,docs):
            if doc.is_error:
                stats["fetch_failed"]+=1
                node.error=doc.content[:400]
                record.states[node.node_id]["status"]="failed"
                record.emit("fetch_failed", "Failure consumes one logical fetch attempt", [node])
                continue
            owners=[tree.contents.setdefault(k,node.url) for k in _same_page_keys(doc)]
            same=next((o for o in owners if o!=node.url),None)
            if same:
                stats["duplicates"]=stats.get("duplicates",0)+1
                node.error=f"same content as {same}"
                record.states[node.node_id].update(status="duplicate",same_as=same)
                record.emit("duplicate", "Duplicate body; fetched once but not evaluated again", [node])
                continue
            node.document=doc
            ready.append(node)
            successful.append(node)

        async def score_one(node):
            started=time.perf_counter()
            record.states[node.node_id]["status"]="scoring"
            record.emit("jev_start", "Evaluate page; depth limit pages have no link questions", [node])
            try:
                await tree._score(node,question,trace,stats,jev_usage,search_id,query=record.query)
            except Exception as exc:
                record.states[node.node_id].update(status="score_failed",score_error=repr(exc))
                node.link_scores=[]
                record.emit("jev_failed", "Keep fetched document; no unscored links will be expanded", [node])
                return
            record.states[node.node_id].update(status="scored",
                jev_duration_ms=round((time.perf_counter()-started)*1000,1))
            record.emit("jev_end", "Page scores returned; candidates committed after this parallel round", [node])
        await asyncio.gather(*(score_one(n) for n in ready))
        for node in ready:
            ranked=sorted(node.link_scores,key=lambda x:-x[0])
            kids=[]; distinct=set()
            for rank,(score,url,anchor) in enumerate(ranked,1):
                if len(kids)>=tree.branch or node.depth>=tree.depth:
                    break
                if _norm(url) in distinct:
                    continue
                distinct.add(_norm(url))
                child=TreeNode(url=url,depth=node.depth+1,parent=node.url,anchor=anchor,
                               link_score=score,rank=rank,
                               discrepancy=node.discrepancy+int(rank>1))
                record.add(child,node.node_id)
                kids.append(child)
            children[node.node_id]=kids
            record.states[node.node_id]["children"]=[c.node_id for c in kids]
            status=record.states[node.node_id]["status"]
            if status!="score_failed":
                record.states[node.node_id]["status"]=("depth_limit" if node.depth>=tree.depth else "ready" if kids else "no_candidates")
            record.emit("candidates", "Reveal ranked top-K candidates; discovery costs no fetch", [node,*kids],
                        parent_id=node.node_id, ranked_links=[dict(rank=i+1,score=s,url=u,anchor=a)
                                                           for i,(s,u,a) in enumerate(ranked)])
        record.save(stats)
        return ready

    # Mandatory roots first, replacing failures/duplicate bodies from the remaining results.
    roots=[]; cursor=0
    while len(roots)<tree.entries and cursor<len(root_candidates) and stats["fetched"]<tree.fetch_budget:
        count=min(tree.entries-len(roots),tree.fetch_budget-stats["fetched"])
        roots.extend(await process(root_candidates[cursor:cursor+count]))
        cursor+=count
    stats["entries"]=len(roots)
    record.emit("roots_ready", "Mandatory root stage complete; all roots have discrepancy zero", roots)

    def walk(node):
        if record.states[node.node_id]["status"]=="pending":
            yield node
        kids=children.get(node.node_id,[])
        choices=kids[1:]+kids[:1] if node.discrepancy<record.limit else kids[:1]
        for child in choices:
            if child.discrepancy<=record.limit:
                yield from walk(child)

    for limit in range(tree.depth):
        if stats["fetched"]>=tree.fetch_budget:
            break
        record.limit=limit
        record.emit("phase", f"Allow up to {limit} deviations; cached nodes are not re-fetched")
        generators=[walk(root) for root in roots]
        while generators and stats["fetched"]<tree.fetch_budget:
            batch=[]; remaining=[]
            for g in generators:
                if len(batch)>=tree.fetch_budget-stats["fetched"]:
                    break
                node=next(g,None)
                if node is not None:
                    batch.append(node);remaining.append(g)
            if not batch:
                break
            await process(batch)
            generators=remaining
        if not any(s["status"]=="pending" and n.depth>1
                   for key,s in record.states.items() for n in [record.nodes[key]]):
            break
    record.emit("expansion_end", "Fetch budget reached" if stats["fetched"]>=tree.fetch_budget else "Eligible candidates exhausted")
    record.save(stats)
    return successful,record
