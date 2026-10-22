"""Whole-bundle evidence selection, with fake scoring and real local chunking."""
import unittest
import json
from collections import defaultdict
from unittest.mock import AsyncMock

from searchgym.explorer import Document
from searchgym.jevtree import JevUsage, TreeNode
from searchgym.rawtree import RawTree
from searchgym.raw_chunks import Chunk
from test_rawtree import Capture
from test_rawtree_navigation import Decision
from test_rawtree_policy import config


class BundleReadingTests(unittest.IsolatedAsyncioTestCase):
    async def test_64_bundles_use_three_routing_cards_then_four_full_sources(self):
        def score(state, key, ctx):
            marker = 'DIRECT_GOLD' if key == 'direct_answer' else 'QUERY_GOLD'
            return .95 if marker in state['page_text'] else .01
        decision, trace, stats = Decision(score), Capture(), defaultdict(int)
        cfg = config(jev_document_tree=True, jev_bundle_tokens=4096)
        chunks = [Chunk(i, (('DIRECT_GOLD' if i == 0 else 'QUERY_GOLD' if i == 63 else 'ordinary')
                            + f' original passage {i}. ')*50, 200, []) for i in range(64)]
        bundles = [{'id': i, 'chunk_ids': [i], 'text': c.text} for i, c in enumerate(chunks)]
        tree = RawTree(decision, cfg, None)
        tree._chunks = AsyncMock(return_value=(chunks, bundles, False))
        node = TreeNode(url='https://example.org/source', depth=1, node_id='n',
                        document=Document('https://example.org/source', 'source'))
        async def scores(state, preview, **ctx):
            return await decision.noul(state, {k: {'type': 'noul', 'instructions': 'Useful?'}
                for k in ('direct_answer', 'query_answer')}, trace, usage=JevUsage(), context=ctx)
        async def evaluate(coro, *args, **kwargs):
            return await coro
        text, _, _, _ = await tree._read_rows([
            {'id': 'n', 'node': node, 'objective': 'direct_answer'}], question='Q', query='q',
            search_id='s', trace=trace, meter=JevUsage(), stats=stats, failures=[],
            scores=scores, evaluate=evaluate)
        cards = [(s, q, c) for s, q, c in decision.calls if c['phase'] == 'region']
        full = [(s, q, c) for s, q, c in decision.calls if c['phase'] == 'bundle']
        self.assertEqual([len(q) for _, q, _ in cards], [16, 8, 8])
        self.assertEqual([c['bundle_id'] for _, _, c in full], [0, 1, 62, 63])
        self.assertEqual(len(decision.calls), 7)
        self.assertEqual(stats['region_cards'], 3)
        self.assertTrue(all(decision.chunker.count(json.dumps(s, ensure_ascii=False)) <= 4096
                            for s, _, _ in cards))
        self.assertTrue(all(s['page_text'] == bundles[c['bundle_id']]['text'] for s, _, c in full))
        self.assertIn('DIRECT_GOLD', text)
        self.assertIn('QUERY_GOLD', text)

    async def read(self, *, budget=3000, neighbors=1):
        def score(state, key, ctx):
            self.assertEqual(ctx['phase'], 'bundle')
            self.assertNotIn('previous_chunk', state)
            self.assertNotIn('target_chunk', state)
            self.assertNotIn('next_chunk', state)
            return .95 if 'GOLD_RELATION' in state['page_text'] else .01
        decision, trace, stats = Decision(score), Capture(), defaultdict(int)
        cfg = config(jev_bundle_tokens=160, jev_document_tree=False,
                     jev_neighbor_chunks=neighbors)
        tree = RawTree(decision, cfg, None)
        text = '\n\n'.join(('GOLD_RELATION candidate has the requested attribute. ' if i==7 else '')
                           + ' '.join(f'original_{i}_{j}' for j in range(25)) for i in range(18))
        node = TreeNode(url='https://example.org/source', depth=1, node_id='n',
                        document=Document('https://example.org/source', text))

        async def scores(state, preview, **ctx):
            return await decision.noul(state, {k: {'type':'noul','instructions':'Useful?'}
                for k in ('direct_answer','query_answer')}, trace, usage=JevUsage(), context=ctx)
        async def evaluate(coro, *args, **kwargs):
            return await coro
        rendered, picked, returned, seen = await tree._read_rows([
            {'id':'n','node':node,'objective':'direct_answer'}], question='Q', query='q',
            search_id='s', trace=trace, meter=JevUsage(), stats=stats, failures=[],
            scores=scores, evaluate=evaluate, output_budget=budget)
        return decision, stats, rendered, picked, returned

    async def test_bundle_is_final_unit_no_atomic_or_neighbor_scoring(self):
        decision, stats, text, picked, returned = await self.read(neighbors=99)
        self.assertIn('GOLD_RELATION', text)
        self.assertEqual(stats['chunks_scored'], 0)
        self.assertGreater(stats['bundles_scored'], 0)
        self.assertTrue(all(r['evaluation_unit']=='bundle' for r in picked))
        self.assertEqual(set(returned[0]['chunk_ids']), {i for r in picked for i in r['chunk_ids']})
        self.assertEqual(returned[0]['bundle_ids'], [r['bundle_id'] for r in picked])
        self.assertTrue(all(decision.chunker.count(s['page_text']) <= 160
                            for s, _, _ in decision.calls))

    async def test_budget_never_returns_only_a_fragment_of_scored_bundle(self):
        _, _, _, picked, returned = await self.read(budget=30)
        self.assertEqual(picked, [])
        self.assertEqual(returned, [])

    async def test_terminal_regions_use_full_bundle_once_even_with_score_cache_disabled(self):
        def score(state, key, ctx):
            self.assertEqual(ctx['phase'], 'bundle')
            self.assertTrue(ctx['region_leaf'])
            return .95 if 'GOLD_RELATION' in state['page_text'] else .01
        decision, trace, stats = Decision(score), Capture(), defaultdict(int)
        cfg = config(jev_document_tree=True, jev_tree_min_bundles=1, jev_leaf_bundles=2,
                     jev_bundle_tokens=160, jev_read_dedup=False)
        chunks = [Chunk(i, 'ordinary '*110 + ('GOLD_RELATION' if i==1 else 'other'), 111, [])
                  for i in range(4)]
        bundles = [{'id':i, 'chunk_ids':[i], 'text':c.text, 'tokens':decision.chunker.count(c.text)}
                   for i,c in enumerate(chunks)]
        tree = RawTree(decision, cfg, None)
        tree._chunks = AsyncMock(return_value=(chunks, bundles, False))
        node = TreeNode(url='https://example.org/source', depth=1, node_id='n',
                        document=Document('https://example.org/source', 'original document'))
        async def unexpected_scores(*args, **kwargs):
            self.fail('Terminal full-bundle decisions must be reused, not rescored')
        async def evaluate(coro, *args, **kwargs):
            return await coro
        text, _, _, _ = await tree._read_rows([
            {'id':'n','node':node,'objective':'direct_answer'}], question='Q', query='q',
            search_id='s', trace=trace, meter=JevUsage(), stats=stats, failures=[],
            scores=unexpected_scores, evaluate=evaluate)
        self.assertIn('GOLD_RELATION', text)
        self.assertEqual(len(decision.calls), 4)
        self.assertEqual({c['bundle_id'] for _,_,c in decision.calls}, set(range(4)))
        self.assertEqual(stats['bundles_scored'], 4)
        self.assertEqual(stats['chunks_scored'], 0)

