"""Offline integration tests for RawTree scheduling and partial evidence recovery."""
import asyncio
import json
import re
import sys
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx
from searchgym.agent import AgentConfig
from searchgym.config import load_test, _validate
from searchgym.explorer import Document
from searchgym.rawtree import LocalDecision, LocalDecisionError, RawTree
from searchgym.runner import _agent_fingerprint
from test_rawtree import Capture, chunker

BASE = 'https://example.org/'


class GraphDecision:
    def __init__(self, graph, *, delays=None, fail=None, page_scores=None):
        self.graph, self.delays, self.fail = graph, delays or {}, fail
        self.page_scores = page_scores or {}
        self.chunker = chunker(64)
        self.contexts = []

    async def prepare(self):
        pass

    async def noul(self, state, questions, trace, *, usage, context):
        self.contexts.append((state, questions, context))
        usage.attempts += 1
        name = state.get('page_url', state.get('page_title', '')).removeprefix(BASE)
        await asyncio.sleep(self.delays.get(name, 0))
        if self.fail and self.fail(state, context):
            usage.failures += 1
            raise LocalDecisionError('simulated evaluation failure')
        scores = {}
        edges = dict(self.graph.get(name, []))
        for key, question in questions.items():
            if key == 'inspect_value':
                values = self.page_scores.get(name, {})
                scores[key] = values.get('inspect_value', max(values.get('direct_answer', .8),
                                                            values.get('query_answer', .8)))
            elif key in ('return_now', 'read_now', 'expand_now'):
                defaults = {'return_now': .000001, 'read_now': .0000001 if edges else .9,
                            'expand_now': max(edges.values(), default=0)}
                scores[key] = self.page_scores.get(name, {}).get(key, defaults[key])
            elif (key in ('direct_answer', 'query_answer') and 'selected_sources' in state):
                default = .0000001 if edges else .9
                scores[key] = self.page_scores.get(name, {}).get(key, default)
            elif key.startswith('link_'):
                if 'Destination: ' in question['instructions']:
                    target = question['instructions'].split('Destination: ', 1)[1].split('\n', 1)[0].removeprefix(BASE)
                else:
                    target = re.search(r'\[([^]]+)\]\(' + re.escape(key) + r'\)', state['page_text']).group(1)
                scores[key] = edges[target]
            else:
                scores[key] = self.page_scores.get(name, {}).get(key, .8)
        usage.calls += 1
        return scores


def config(**kwargs):
    values = dict(jev_strategy='raw', jev_traversal='best_first', jev_entries=2,
                  jev_branch=1, jev_frontier_width=1, jev_expand_batch=2,
                  jev_depth=3, jev_fetch_budget=6, jev_direct_reads=0, jev_query_reads=0,
                  jev_bundle_tokens=160, jev_output_tokens=3000)
    values.update(kwargs)
    return AgentConfig(**values)


class PolicyTests(unittest.IsolatedAsyncioTestCase):
    async def run_graph(self, graph, roots=('a', 'b'), *, cfg=None, delays=None,
                        fail=None, bodies=None, fetch_failures=(), page_scores=None):
        decision = GraphDecision(graph, delays=delays, fail=fail, page_scores=page_scores)
        fetched = []

        async def fetch(url, *, engine):
            self.assertEqual(engine, 'browser')
            name = url.removeprefix(BASE)
            fetched.append(name)
            if name in fetch_failures:
                return Document(url, 'fetch unavailable', is_error=True)
            content = ((bodies or {}).get(name) or f'# Source {name}\n\nVERIFIED_FACT_{name}.\n\n')
            content += '\n'.join(f'[{child}]({BASE}{child})' for child, _ in graph.get(name, []))
            return Document(url, content, title=name)

        tree = RawTree(decision, cfg or config(), fetch)
        trace = Capture()
        output = await tree.run_search('query', [{'link': BASE + name} for name in roots],
                                       question='original', trace=trace, usage=None)
        return tree, decision, fetched, trace, output

    async def test_best_first_keeps_third_link_and_backfills_duplicate_urls(self):
        graph = {'a': [('shared1', .9), ('shared2', .8), ('a3', .7)],
                 'b': [('shared1', .99), ('shared2', .98), ('b3', .97)]}
        _, _, fetched, _, (_, _, stats) = await self.run_graph(graph)
        self.assertEqual(fetched, ['a', 'b', 'shared1', 'shared2', 'b3', 'a3'])
        self.assertEqual(stats['page_visits'], 6)
        self.assertGreater(stats['duplicate_candidates'], 0)

    async def test_best_first_compares_candidates_across_depths(self):
        graph = {'a': [('a1', .9), ('a2', .8)], 'b': [('b1', .1)],
                 'a1': [('deep', .95)]}
        _, _, fetched, _, _ = await self.run_graph(graph, cfg=config(jev_expand_batch=1, jev_fetch_budget=5))
        self.assertEqual(fetched, ['a', 'b', 'a1', 'deep', 'a2'])

    async def test_cancellation_cleans_up_rolling_page_jobs(self):
        cfg = config(jev_expand_batch=2)
        decision = GraphDecision({})
        started = asyncio.Event()
        active = set()

        async def fetch(url, *, engine):
            active.add(url)
            if len(active) == 2:
                started.set()
            try:
                await asyncio.Event().wait()
            finally:
                active.remove(url)

        job = asyncio.create_task(RawTree(decision, cfg, fetch).run_search(
            'query', [{'link': BASE + name} for name in ('a', 'b')],
            question='original', trace=Capture(), usage=None))
        try:
            await asyncio.wait_for(started.wait(), timeout=3)
        finally:
            job.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await job
        self.assertFalse(active)

    async def test_floor_applies_to_links_only_and_depth_limits_children(self):
        graph = {'a': [('a1', .009), ('a2', .01)], 'b': [('b1', 0)],
                 'a2': [('too_deep', 1)]}
        _, _, fetched, _, (_, _, stats) = await self.run_graph(
            graph, cfg=config(jev_link_floor=.01, jev_depth=2))
        self.assertEqual(fetched, ['a', 'b', 'a2'])
        self.assertEqual(stats['links_pruned'], 2)
        self.assertEqual(stats['max_depth'], 2)

    async def test_beam_remains_a_separate_browser_comparison(self):
        graph = {'a': [('a1', .9), ('a2', .8), ('a3', .7)],
                 'b': [('b1', .003), ('b2', .002)]}
        _, _, fetched, _, _ = await self.run_graph(graph, cfg=config(
            jev_traversal='beam', jev_branch=2, jev_frontier_width=4, jev_depth=2))
        self.assertEqual(fetched, ['a', 'b', 'a1', 'a2', 'b1', 'b2'])

    async def test_default_beam_narrows_six_two_two_and_returns_two_evidence_sources(self):
        cfg = load_test(method='jevtree').agent
        graph = {'a': [('a1', .9), ('a2', .8), ('a3', .7)],
                 'b': [('b1', .85), ('b2', .11)],
                 'c': [('c1', .09)], 'd': [('d1', .05)],
                 'e': [('e1', .10)], 'f': [('f1', .08)],
                 'a1': [('a11', .95), ('a12', .3)],
                 'b1': [('b11', .94), ('b12', .2)],
                 'b11': [('too_deep', .99)]}
        _, decision, fetched, _, (tree, _, stats) = await self.run_graph(
            graph, roots=('a', 'b', 'c', 'd', 'e', 'f'), cfg=cfg,
            page_scores={'a': {'direct_answer': .99, 'query_answer': .2, 'read_now': .99},
                         'b11': {'direct_answer': .1, 'query_answer': .99, 'read_now': .99}})
        self.assertEqual(fetched[:6], ['a', 'b', 'c', 'd', 'e', 'f'])
        self.assertEqual(set(fetched[6:8]), {'a1', 'b1'})
        self.assertEqual(set(fetched[8:]), {'a11', 'b11'})
        self.assertEqual(stats['page_visits'], 10)
        self.assertEqual(stats['max_depth'], 3)
        self.assertEqual((stats['reads'], stats['direct_reads'], stats['query_reads']), (6, 1, 1))
        self.assertEqual(stats['evidence_pages'], 2)
        precise_pages = {s['page_title'] for s, _, c in decision.contexts
                         if c['phase'] in {'bundle', 'chunk'}}
        self.assertEqual(precise_pages, {'a','b','a1','b1','a11','b11'})

    async def test_default_beam_does_not_fill_slots_below_threshold(self):
        cfg = load_test(method='jevtree').agent
        for score, expected in ((.099, ['a']), (.1, ['a', 'child'])):
            with self.subTest(score=score):
                _, _, fetched, _, (_, _, stats) = await self.run_graph(
                    {'a': [('child', score)], 'child': [('too_low', .01)]}, roots=('a',), cfg=cfg)
                self.assertEqual(fetched, expected)
                self.assertLess(stats['page_visits'], cfg.jev_fetch_budget)

    async def test_new_query_reuses_browser_body_but_recomputes_scores(self):
        tree, decision, fetched, _, _ = await self.run_graph({}, cfg=config(
            jev_direct_reads=1, jev_query_reads=1, jev_fetch_budget=2))
        before = len(decision.contexts)
        _, text, stats = await tree.run_search('new target', [{'link': BASE + name} for name in ('a', 'b')],
                                              question='original', trace=Capture(), usage=None)
        self.assertEqual(fetched, ['a', 'b'])
        self.assertEqual(stats['document_reuses'], 2)
        self.assertEqual(stats['page_visits'], 2)
        self.assertEqual(stats['browser_fetches'], 0)
        self.assertIn('VERIFIED_FACT_a', text)
        new_calls = decision.contexts[before:]
        self.assertTrue(new_calls)
        self.assertTrue(all('new target' in questions['query_answer']['instructions']
                            for _, questions, _ in new_calls))

    async def test_bad_page_does_not_discard_other_pages_evidence(self):
        _, _, _, trace, (log, text, stats) = await self.run_graph(
            {}, cfg=config(jev_direct_reads=1, jev_query_reads=1),
            fail=lambda state, ctx: ctx['phase'] == 'preview' and state['page_url'].endswith('/a'))
        self.assertIn('VERIFIED_FACT_b', text)
        self.assertIn('Retrieval is incomplete', text)
        self.assertEqual(stats['page_eval_failures'], 1)
        self.assertEqual(stats['jev_failures'], 1)
        self.assertEqual(log['evaluation_failures'][0]['retained_keys'], [])
        self.assertTrue(any(e['event'] == 'rawtree.return' for e in trace.events))

    async def test_bundle_failures_preserve_other_units_without_atomic_rescoring(self):
        body = '# Source\n\n' + '\n\n'.join(' '.join(f'fact_{i}_{j}' for j in range(20)) for i in range(25))
        def fail(state, ctx):
            return ((ctx['phase'] == 'bundle' and ctx['bundle_id'] == 0) or
                    (ctx['phase'] == 'chunk' and ctx['chunk_id'] == 8))
        _, _, _, _, (_, text, stats) = await self.run_graph(
            {}, roots=('a',), cfg=config(jev_entries=1, jev_direct_reads=1, jev_query_reads=0),
            bodies={'a': body}, fail=fail)
        self.assertEqual(stats['bundle_eval_failures'], 1)
        self.assertEqual(stats['chunk_eval_failures'], 0)
        self.assertEqual(stats['chunks_scored'], 0)
        self.assertGreater(stats['chunks_returned'], 0)
        self.assertIn('Source: ' + BASE + 'a', text)
        self.assertIn('Retrieval is incomplete', text)

    async def test_failed_fetch_is_not_cached(self):
        tree, _, fetched, _, _ = await self.run_graph({}, roots=('a',), fetch_failures=('a',))
        _, _, stats = await tree.run_search('retry', [{'link': BASE + 'a'}], question='original',
                                           trace=Capture(), usage=None)
        self.assertEqual(fetched, ['a', 'a'])
        self.assertEqual(stats['document_reuses'], 0)
        self.assertEqual(stats['fetch_failed'], 1)

    async def test_partial_packet_keeps_valid_page_scores_and_marks_unknown_links(self):
        cfg = config(jev_entries=1, jev_depth=2, jev_fetch_budget=2,
                     jev_direct_reads=1, jev_query_reads=0, jev_page_tokens=10000,
                     jev_packet_questions=1, jev_inflight_questions=4)
        client = LocalDecision(cfg)
        await client.http.aclose()
        client.chunker = chunker(64)

        async def respond(request):
            body = json.loads(request.content)
            keys = body['questions']
            if 'link_6' in keys:
                return httpx.Response(500, text='overflow unavailable')
            return httpx.Response(200, json={'answers': {k: {'noul': .8} for k in keys},
                                            'usage': {'input_tokens': 10}})

        async def fetch(url, *, engine):
            return Document(url, 'VALID_FACT\n\n' + '\n'.join(
                f'[Link {i}]({BASE}target{i})' for i in range(70)))

        client.http = httpx.AsyncClient(transport=httpx.MockTransport(respond))
        trace = Capture()
        try:
            _, text, stats = await RawTree(client, cfg, fetch).run_search(
                'query', [{'link': BASE + 'root'}], question='original', trace=trace, usage=None)
            self.assertIn('VALID_FACT', text)
            self.assertEqual(stats['page_eval_failures'], 1)
            links = next(e['links'] for e in trace.events if e['event'] == 'rawtree.links')
            # One question per request, four requests per wave: failure at
            # index 6 retains 0..5 and 7, then prevents the next wave (8+).
            self.assertEqual(sum(link['evaluated'] for link in links), 7)
            self.assertIsNone(links[6]['score'])
            self.assertTrue(links[7]['evaluated'])
            self.assertTrue(all(link['score'] is None for link in links[8:]))
        finally:
            await client.aclose()


class ConfigurationTests(unittest.TestCase):
    def test_experiment_overrides_keep_other_budgets_and_are_saved_in_config(self):
        cfg = load_test(method='jevtree', raw_traversal='beam', expected_raw_traversal='beam',
                        raw_link_floor=.01, raw_query_pages=6)
        self.assertEqual(cfg.agent.jev_traversal, 'beam')
        self.assertEqual(cfg.agent.jev_link_floor, .01)
        base = load_test(method='jevtree')
        self.assertEqual((cfg.agent.jev_reads, cfg.agent.jev_direct_reads, cfg.agent.jev_query_reads),
                         (base.agent.jev_direct_reads + 6, base.agent.jev_direct_reads, 6))
        self.assertEqual((cfg.agent.jev_depth, cfg.agent.jev_fetch_budget),
                         (base.agent.jev_depth, base.agent.jev_fetch_budget))
        with self.assertRaises(ValueError):
            load_test(method='ragent', raw_traversal='beam')
        with self.assertRaises(ValueError):
            load_test(method='jevtree', raw_query_pages=-1)

    def test_policy_parameters_are_validated_and_invalidate_cache(self):
        cfg = load_test(method='jevtree')
        for changes in ({'jev_traversal': 'unknown'}, {'jev_expand_batch': 0},
                        {'jev_link_floor': -1}, {'jev_link_floor': float('nan')},
                        {'jev_packet_questions': 0}, {'jev_packet_questions': 65},
                        {'jev_packet_questions': 8.5}, {'jev_inflight_questions': 0},
                        {'jev_inflight_questions': 32.5}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                _validate(replace(cfg, agent=replace(cfg.agent, **changes)))
        base = _agent_fingerprint(cfg.agent)
        for changes in ({'jev_traversal': 'best_first'}, {'jev_expand_batch': 1}, {'jev_link_floor': .01},
                        {'jev_packet_questions': 16}, {'jev_inflight_questions': 16}):
            self.assertNotEqual(base, _agent_fingerprint(replace(cfg.agent, **changes)))


if __name__ == '__main__':
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    unittest.main()
