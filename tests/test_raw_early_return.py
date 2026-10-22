"""Finish admitted evidence and navigation without decision-driven early return."""
import asyncio
import json
import unittest

import httpx
from searchgym.explorer import Document
from searchgym.rawtree import LocalDecision, RawTree
from test_rawtree import Capture, chunker
from test_rawtree_navigation import Decision
from test_rawtree_policy import BASE, config
import test_rawtree_actions as actions


class NoEarlyReturnTests(unittest.IsolatedAsyncioTestCase):
    run_graph = actions.JointInspectionTests.run_graph

    async def test_high_evidence_does_not_stop_child_navigation(self):
        decision = Decision(lambda *args: .9)
        _, _, trace, fetched, (_, text, _) = await self.run_graph(
            {'root': 'ROOT_FACT [Record]('+BASE+'leaf)', 'leaf': 'CHILD_FACT explicit answer.'},
            decision=decision)
        self.assertEqual(fetched, ['root', 'leaf'])
        self.assertIn('CHILD_FACT', text)
        self.assertTrue(all('return_now' not in questions for _, questions, _ in decision.calls))
        self.assertFalse(any(e['event'].startswith('rawtree.early_return') for e in trace.events))

    async def test_slow_sibling_fact_is_preserved_after_fast_page_completes(self):
        fast_done, slow_done = asyncio.Event(), asyncio.Event()
        class Parallel(Decision):
            async def noul(self, state, questions, trace, *, usage, context):
                if context['phase'] == 'bundle':
                    if state['page_title'] == 'Search b':
                        await fast_done.wait()
                        await asyncio.sleep(.03)
                        slow_done.set()
                    else:
                        fast_done.set()
                return await super().noul(state, questions, trace, usage=usage, context=context)
        _, _, _, _, (_, text, _) = await self.run_graph(
            {'a': 'FAST_GENERAL_FACT complete.', 'b': 'SLOW_CAST Peter King Nzioki — Policeman 1.'},
            roots=('a', 'b'), decision=Parallel(lambda *args: .9))
        self.assertTrue(slow_done.is_set())
        self.assertIn('FAST_GENERAL_FACT', text)
        self.assertIn('Peter King Nzioki', text)

    async def test_waits_for_all_link_packets_without_return_question(self):
        later_done = asyncio.Event()
        posted = []
        async def respond(request):
            body = json.loads(request.content)
            posted.append(body)
            questions = body['questions']
            self.assertNotIn('return_now', questions)
            if all(k.startswith('link_') for k in questions):
                await asyncio.sleep(.03)
                later_done.set()
            return httpx.Response(200, json={'answers': {
                k: {'noul': .01 if k.startswith('link_') else .9} for k in questions}})
        cfg = config(jev_traversal='beam', jev_entries=1, jev_frontier_width=2, jev_depth=3,
                     jev_fetch_budget=10, jev_reads=1, jev_direct_reads=1, jev_query_reads=0,
                     jev_bundle_tokens=4096, jev_page_tokens=4096, jev_output_tokens=16000,
                     jev_link_floor=.1)
        client = LocalDecision(cfg)
        await client.http.aclose()
        client.http = httpx.AsyncClient(transport=httpx.MockTransport(respond))
        client.chunker = chunker(64)
        self.addAsyncCleanup(client.aclose)
        body = 'SOURCE_FACT '+ ' '.join(f'[Record {i}]({BASE}r{i})' for i in range(120))
        async def fetch(url, *, engine):
            return Document(url, body, title='Original')
        _, text, _ = await RawTree(client, cfg, fetch).run_search('target',
            [{'link': BASE+'root', 'title': 'Search'}], question='original', trace=Capture(), usage=None)
        self.assertTrue(later_done.is_set())
        self.assertIn('SOURCE_FACT', text)
        self.assertEqual([len(b['questions']) for b in posted], [1, 64, 58])
        self.assertEqual(client.inflight_questions, 0)
