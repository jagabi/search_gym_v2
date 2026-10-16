"""Offline tests: real Docling, synthetic tokenizer, fake fetch/model endpoints."""
import asyncio
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx
from tokenizers import Tokenizer, models, pre_tokenizers
from searchgym.agent import AgentConfig
from searchgym.explorer import Document
from searchgym.jevtree import JevUsage
from searchgym.raw_chunks import SourceChunker
from searchgym.rawtree import LocalDecision, RawTree, decision_question, quota_select
from searchgym.trace import NullTrace


def chunker(limit=32):
    tokenizer = Tokenizer(models.WordLevel({'[UNK]': 0}, unk_token='[UNK]'))
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
    with patch('tokenizers.Tokenizer.from_pretrained', return_value=tokenizer):
        return SourceChunker('offline', limit)


class Capture(NullTrace):
    def __init__(self):
        super().__init__()
        self.events = []

    def event(self, kind, **fields):
        self.events.append({'event': kind, **fields})


class ChunkTests(unittest.TestCase):
    def test_full_document_bundles_cover_tail_and_overlap(self):
        c = chunker()
        text = '# Heading\n\n' + '\n\n'.join(' '.join(f'fact{i}_{j}' for j in range(20)) for i in range(30))
        text += '\n\nTHE_FINAL_ANSWER_IS_AT_THE_END'
        chunks = c.chunks(text)
        bundles = c.bundles(chunks, 120, 2)
        self.assertIn('THE_FINAL_ANSWER_IS_AT_THE_END', chunks[-1].text)
        self.assertEqual(set(range(len(chunks))), {i for b in bundles for i in b['chunk_ids']})
        self.assertTrue(all(b['tokens'] <= 120 for b in bundles))
        self.assertEqual(bundles[0]['chunk_ids'][-2:], bundles[1]['chunk_ids'][:2])
        self.assertLessEqual(c.count(c.prefix(text, 50)), 50)

    def test_source_table_and_url_survive(self):
        c = chunker(128)
        text = '# Awards\n\n| Name | Year |\n|---|---|\n| Ada | 2021 |\n\n[Record](https://example.org/record)\n'
        joined = '\n'.join(x.text for x in c.chunks(text))
        for value in ['Ada', '2021', 'https://example.org/record']:
            self.assertIn(value, joined)

    def test_quota_overlap_does_not_consume_query_slot(self):
        rows = [{'id': 'a', 'direct_answer': .9, 'query_answer': .9},
                {'id': 'b', 'direct_answer': .1, 'query_answer': .8}]
        self.assertEqual([r['id'] for r in quota_select(rows, 1, 1)], ['a', 'b'])


class AsyncTests(unittest.IsolatedAsyncioTestCase):
    async def test_fetch_engine_headers_and_no_summary(self):
        from searchgym.tools import WebTools
        seen = []

        async def respond(request):
            seen.append(request)
            return httpx.Response(200, json={'code': 200, 'data': {'title': 'Source', 'content': 'Exact source text'}})

        tools = WebTools()
        tools.reader_status = {'jina_base_url': 'http://127.0.0.1:3001'}
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            tools._reader_http = client
            for engine in ['curl', 'browser']:
                doc = await tools.fetch('https://example.org/page', engine=engine)
                self.assertFalse(doc.is_error)
                self.assertEqual(doc.content, 'Exact source text')
        self.assertEqual([r.headers['X-Engine'] for r in seen], ['curl', 'browser'])
        self.assertTrue(all(r.headers['X-No-Cache'] == 'true' for r in seen))
        self.assertTrue(all(r.url.host == '127.0.0.1' for r in seen))

    async def test_bad_probability_fails_instead_of_scoring_zero(self):
        client = LocalDecision(AgentConfig(jev_model='vllm-sr/d3-mini'))
        await client.http.aclose()
        client.http = httpx.AsyncClient(transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json={'answers': {'x': {'noul': 'nan'}}})))
        meter = JevUsage()
        try:
            with self.assertRaises(RuntimeError):
                await client.noul('source', {'x': decision_question('target', query=True)},
                                  NullTrace(), usage=meter, context={})
            self.assertEqual(meter.failures, 1)
            self.assertEqual(meter.calls, 0)
        finally:
            await client.aclose()

    async def test_global_four_slots_and_atomic_questions(self):
        cfg = AgentConfig(jev_model='vllm-sr/d3-mini', jev_concurrency=4)
        client = LocalDecision(cfg)
        await client.http.aclose()
        active = peak = 0
        bodies = []

        async def respond(request):
            nonlocal active, peak
            body = json.loads(request.content)
            bodies.append(body)
            active += 1
            peak = max(peak, active)
            await asyncio.sleep(.01)
            active -= 1
            key = next(iter(body['questions']))
            return httpx.Response(200, json={'answers': {key: {'noul': .7}}, 'usage': {'input_tokens': 10}})

        client.http = httpx.AsyncClient(transport=httpx.MockTransport(respond))
        meter = JevUsage()
        try:
            q = decision_question('original target', query=False)
            await asyncio.gather(*(client.noul({'page_text': 'source'}, {'direct': q, 'query': q},
                                               NullTrace(), usage=meter, context={}) for _ in range(7)))
            self.assertEqual(peak, 4)
            self.assertEqual(meter.calls, 14)
            self.assertTrue(all(len(b['questions']) == 1 for b in bodies))
            self.assertTrue(all(set(b['state']) == {'page_text'} for b in bodies))
        finally:
            await client.aclose()

    async def test_depth_budget_and_browser_then_raw_tail(self):
        cfg = AgentConfig(jev_strategy='raw', jev_entries=10, jev_branch=2, jev_depth=5,
                          jev_fetch_budget=50, jev_frontier_width=10, jev_direct_reads=2, jev_query_reads=4,
                          jev_chunk_tokens=32, jev_bundle_tokens=120, jev_direct_chunks=4, jev_query_chunks=8)

        class FakeDecision:
            chunker = chunker()

            async def prepare(self):
                pass

            async def noul(self, state, questions, trace, *, usage, context):
                self_test.assertNotIn('question', state)
                self_test.assertNotIn('search_query', state)
                usage.calls += len(questions)
                usage.attempts += len(questions)
                return {key: .9 if context['phase'] != 'chunk' or 'FINAL_FACT' in state['target_chunk'] else .01
                        for key in questions}

        self_test = self
        fetched = []

        async def fetch(url, *, engine):
            fetched.append((url, engine))
            if engine == 'curl':
                return Document(url, f'Useful facts. [First]({url}/a) [Second]({url}/b)')
            return Document(url, '# Source\n\n' + ('ordinary evidence ' * 200) + '\n\nFINAL_FACT 42.')

        trace = Capture()
        tree = RawTree(FakeDecision(), cfg, fetch)
        log, text, stats = await tree.run_search('current query',
                    [{'link': f'https://example.org/{i}'} for i in range(10)],
                    question='original target', trace=trace, usage=None)
        self.assertEqual(stats['max_depth'], 5)
        self.assertEqual(stats['fast_fetches'], 50)
        self.assertEqual(stats['browser_fetches'], 6)
        self.assertEqual(stats['summary_calls'], 0)
        self.assertIn('FINAL_FACT', text)
        self.assertLessEqual(tree.jev.chunker.count(text), cfg.jev_output_tokens)
        self.assertTrue(all(engine == 'curl' for _, engine in fetched[:50]))
        selected = next(e for e in trace.events if e['event'] == 'rawtree.return')
        ids = [(r['node_id'], i) for r in selected['returned'] for i in r['chunk_ids']]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == '__main__':
    # Selector avoids Proactor pipe issues in restricted Windows test runners.
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    unittest.main()
