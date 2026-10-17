"""Offline policy review: actual RawTree/LDS plus a candidate scheduler prototype.

No network, tokenizer download, benchmark, or production configuration changes.
The best-first prototype tests scheduling only, not integration or answer quality.
"""
import asyncio
import heapq
import json
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from searchgym.agent import AgentConfig
from searchgym.explorer import Document
from searchgym.jevtree import JevUsage, TreeNode
from searchgym.lds import grow_lds
from searchgym.rawtree import RawTree
from searchgym.trace import NullTrace


BASE = 'https://example.org/'


class Capture(NullTrace):
    def __init__(self):
        super().__init__()
        self.events = []

    def event(self, kind, **fields):
        self.events.append({'event': kind, **fields})


class FakeDecision:
    chunker = SimpleNamespace(count=len, prefix=lambda text, limit: text[:limit])

    def __init__(self, graph):
        self.graph = graph

    async def prepare(self):
        pass

    async def noul(self, state, questions, trace, *, usage, context):
        usage.calls += 1
        edges = self.graph.get(state['page_url'].removeprefix(BASE), [])
        by_url = {BASE + name: score for name, score in edges}
        scores = {}
        for key, q in questions.items():
            if key.startswith('link_'):
                url = q['instructions'].split('Destination: ', 1)[1].split('\n', 1)[0]
                scores[key] = by_url[url]
            else:
                scores[key] = .5
        return scores


async def actual_raw(graph, roots, *, branch=2, depth=2, width=4, budget=6, repeat=False):
    cfg = AgentConfig(jev_strategy='raw', jev_entries=len(roots), jev_branch=branch,
                      jev_depth=depth, jev_frontier_width=width, jev_fetch_budget=budget,
                      jev_direct_reads=0, jev_query_reads=0)
    calls = []

    async def fetch(url, *, engine):
        calls.append(url.removeprefix(BASE))
        edges = graph.get(url.removeprefix(BASE), [])
        return Document(url, 'Source facts.\n' + '\n'.join(
            f'[{name}]({BASE}{name})' for name, _ in edges))

    tree = RawTree(FakeDecision(graph), cfg, fetch)
    result = []
    for query in (['first query', 'different query'] if repeat else ['first query']):
        start = len(calls)
        _, _, stats = await tree.run_search(query, [{'link': BASE + name} for name in roots],
                                            question='Original question', trace=Capture(), usage=None)
        result.append({'query': query, 'visited': calls[start:],
                       'entries': stats['entries'], 'nodes': stats['nodes'],
                       'max_depth': stats['max_depth']})
    return result


def best_first_prototype(graph, roots, *, depth=2, budget=6, floor=0):
    """Serial heap prototype: candidates are revealed only when their parent is visited."""
    visited = set(roots)
    order = list(roots)
    pending = []

    def reveal(name, parent_depth):
        if parent_depth >= depth:
            return
        for child, score in graph.get(name, []):
            if score >= floor:
                heapq.heappush(pending, (-score, child, parent_depth + 1))

    for root in roots:
        reveal(root, 1)
    while pending and len(order) < budget:
        _, name, node_depth = heapq.heappop(pending)
        if name in visited:
            continue
        visited.add(name)
        order.append(name)
        reveal(name, node_depth)
    return order


async def actual_lds():
    fetched = []

    async def fetch(url):
        fetched.append(url)
        return Document(url, 'Unique source ' + url)

    async def score(node, *args, **kwargs):
        node.link_scores = ([(.9, node.url + '/first', 'first'),
                             (.8, node.url + '/second', 'second')]
                            if node.depth < 5 else [])

    tree = SimpleNamespace(entries=10, branch=2, depth=5, fetch_budget=50,
                           visited=set(), contents={}, reader_status={},
                           reader_budgets={'direct_answer': 2, 'query_answer': 4},
                           fetch=fetch, _score=score)
    root = TreeNode('search: query', depth=0,
                    link_scores=[(.9, BASE + f'r{i}', f'r{i}') for i in range(10)])
    stats = {'fetched': 0, 'fetch_failed': 0}
    _, record = await grow_lds(tree, root, 'question', Capture(), stats, JevUsage(), 'offline')
    return {'fetches': len(fetched), 'second_choice_fetches': sum('/second' in u for u in fetched),
            'pending_alternatives': sum(s['status'] == 'pending' for s in record.states.values()),
            'discrepancy_limit_reached': record.limit}


async def main():
    ranked = {'a': [('a1', .9), ('a2', .8), ('a3', .7)],
              'b': [('b1', .003), ('b2', .002)]}
    duplicate = {'a': [('shared1', .9), ('shared2', .8), ('a3', .7)],
                 'b': [('shared1', .99), ('shared2', .98), ('b3', .97)]}
    binary = {}
    def populate(name, depth):
        if depth >= 5:
            return
        binary[name] = [(name + 'a', .9), (name + 'b', .8)]
        for child, _ in binary[name]:
            populate(child, depth + 1)
    roots = [f'r{i}' for i in range(10)]
    for root in roots:
        populate(root, 1)
    report = {
        'scope': 'Synthetic scheduling checks only; no answer-quality claims.',
        'current_top2': await actual_raw(ranked, ['a', 'b']),
        'current_top3': await actual_raw(ranked, ['a', 'b'], branch=3),
        'best_first_prototype': best_first_prototype(ranked, ['a', 'b']),
        'best_first_floor_001': best_first_prototype(ranked, ['a', 'b'], floor=.01),
        'duplicate_top2': await actual_raw(duplicate, ['a', 'b']),
        'duplicate_top3': await actual_raw(duplicate, ['a', 'b'], branch=3),
        'repeat_query': await actual_raw(ranked, ['a', 'b'], repeat=True),
        'widths': {str(w): await actual_raw(binary, roots, depth=5, width=w, budget=50)
                   for w in (4, 10, 20)},
        'legacy_lds': await actual_lds(),
    }
    checks = {
        'top2_discards_higher_third': 'a3' not in report['current_top2'][0]['visited']
                                     and 'b2' in report['current_top2'][0]['visited'],
        'top3_recovers_third': 'a3' in report['current_top3'][0]['visited'],
        'duplicate_top2_underfills': report['duplicate_top2'][0]['nodes'] == 4,
        'repeat_query_skips_roots': report['repeat_query'][1]['entries'] == 0,
        'width4_uses26': report['widths']['4'][0]['nodes'] == 26,
        'width10_reaches5': report['widths']['10'][0]['max_depth'] == 5,
        'width20_only_reaches3': report['widths']['20'][0]['max_depth'] == 3,
        'lds_budget_leaves_no_deviations': report['legacy_lds']['second_choice_fetches'] == 0
                                          and report['legacy_lds']['fetches'] == 50,
        'prototype_keeps_third_and_stops_at_floor': report['best_first_floor_001']
                                                   == ['a', 'b', 'a1', 'a2', 'a3'],
    }
    assert all(checks.values()), checks
    report['checks'] = checks
    target = Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    import faulthandler
    faulthandler.dump_traceback_later(45, exit=True)
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
