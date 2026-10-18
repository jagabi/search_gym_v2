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
from searchgym.rawtree import LocalDecision, RawTree, decision_question, quota_select, _gather_owned
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

    def test_headings_without_body_survive(self):
        c = chunker(128)
        text = ('# Awards\n\nIntroductory context.\n\n'
                '## Finalist: Grace Hopper\n\n'
                '## Award details\n\nThe award is presented annually.\n\n'
                '## Winner: Ada Lovelace, 2021\n')
        chunks = c.chunks(text)
        joined = '\n'.join(chunk.text for chunk in chunks)
        for fact in ['Finalist: Grace Hopper', 'Winner: Ada Lovelace, 2021',
                     'Introductory context.', 'The award is presented annually.']:
            self.assertIn(fact, joined)

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
        self.assertTrue(all(r.headers['X-Assert-Status-Code'] == '200' for r in seen))
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

    async def test_global_four_slots_and_shared_question_packets(self):
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
            return httpx.Response(200, json={
                'answers': {key: {'noul': .7} for key in reversed(body['questions'])},
                'usage': {'input_tokens': 10}})

        client.http = httpx.AsyncClient(transport=httpx.MockTransport(respond))
        meter = JevUsage()
        try:
            q = decision_question('original target', query=False)
            results = await asyncio.gather(*(client.noul({'page_text': 'source'}, {'direct': q, 'query': q},
                                               NullTrace(), usage=meter, context={}) for _ in range(7)))
            self.assertEqual(peak, 4)
            self.assertEqual(meter.calls, 14)
            self.assertEqual(meter.attempts, 14)
            self.assertEqual(meter.input_tokens, 140)
            self.assertEqual(len(bodies), 14)
            self.assertTrue(all(r == {'direct': .7, 'query': .7} for r in results))
            self.assertTrue(all(len(b['questions']) == 1 for b in bodies))
            self.assertTrue(all(set(b['state']) == {'page_text'} for b in bodies))
        finally:
            await client.aclose()

    async def test_page_and_link_requests_preserve_shared_source_cutoff_and_score_mapping(self):
        cfg = AgentConfig(jev_strategy='raw', jev_entries=1, jev_branch=1, jev_depth=2,
                          jev_fetch_budget=2, jev_direct_reads=0, jev_query_reads=0)
        client = LocalDecision(cfg)
        await client.http.aclose()
        client.chunker = chunker()
        full = ('First context [First](https://example.org/first)\n'
                'Second context [Second](https://example.org/second)\n'
                'Cut context [Cut](https://example.org/cutoff)\n'
                'UNSEEN [Tail](https://example.org/tail)')
        cut = full.index('/cutoff') + 3
        bodies, fetched = [], []

        async def respond(request):
            body = json.loads(request.content)
            bodies.append(body)
            values = {'direct_answer': .3, 'query_answer': .8, 'link_0': .1, 'link_1': .9}
            return httpx.Response(200, json={
                'answers': {k: {'noul': values[k]} for k in reversed(body['questions'])},
                'usage': {'input_tokens': 20}})

        async def fetch(url, *, engine):
            fetched.append(url)
            self.assertEqual(engine, 'browser')
            return Document(url, full if url.endswith('/root') else
                            'Terminal [No expansion](https://example.org/deeper)')

        client.http = httpx.AsyncClient(transport=httpx.MockTransport(respond))
        trace = Capture()
        try:
            with patch.object(client.chunker, 'prefix', side_effect=lambda text, limit:
                              text[:cut] if text == full else text):
                _, _, stats = await RawTree(client, cfg, fetch).run_search(
                    'current target', [{'link': 'https://example.org/root'}],
                    question='original target', trace=trace, usage=None)
            self.assertEqual(fetched, ['https://example.org/root', 'https://example.org/second'])
            self.assertEqual(len(bodies), 6)
            self.assertEqual([k for b in bodies[:4] for k in b['questions']],
                             ['direct_answer', 'query_answer', 'link_0', 'link_1'])
            self.assertEqual([k for b in bodies[4:] for k in b['questions']], ['direct_answer', 'query_answer'])
            self.assertTrue(all(b['state'] == bodies[0]['state'] for b in bodies[:4]))
            page = bodies[0]['state']['page_text']
            self.assertIn('First context [First](link_0)', page)
            self.assertIn('Second context [Second](link_1)', page)
            self.assertNotIn('UNSEEN', page)
            self.assertNotIn('cutoff', json.dumps(bodies[0]))
            self.assertNotIn('current target', json.dumps(bodies[0]['state']))
            self.assertNotIn('original target', json.dumps(bodies[0]['state']))
            self.assertEqual(stats['jev_requests'], 6)
            self.assertEqual(stats['links_scored'], 2)
            links = next(e['links'] for e in trace.events if e['event'] == 'rawtree.links')
            self.assertEqual([(r['url'], r['score']) for r in links],
                             [('https://example.org/first', .1), ('https://example.org/second', .9)])
        finally:
            await client.aclose()

    async def test_missing_score_does_not_silently_drop_a_link(self):
        client = LocalDecision(AgentConfig())
        await client.http.aclose()
        client.http = httpx.AsyncClient(transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json={'answers': {'direct_answer': {'noul': .8}}})))
        meter = JevUsage()
        try:
            q = decision_question('target', query=True)
            with self.assertRaises(RuntimeError):
                await client.noul('source', {'direct_answer': q, 'link_0': q},
                                  NullTrace(), usage=meter, context={})
            self.assertEqual(meter.attempts, 2)
            self.assertEqual(meter.calls, 1)
            self.assertEqual(meter.failures, 1)
        finally:
            await client.aclose()

    async def test_server_64_key_limit_preserves_all_scores_and_minimal_packets(self):
        client = LocalDecision(AgentConfig(jev_packet_questions=64, jev_inflight_questions=256))
        await client.http.aclose()
        bodies = []
        values = {}

        async def respond(request):
            body = json.loads(request.content)
            bodies.append(body)
            if len(body['questions']) > 64:
                return httpx.Response(400, json={'error': {'message': 'questions: at most 64 for this model'}})
            return httpx.Response(200, json={
                'answers': {k: {'noul': values[k]} for k in reversed(body['questions'])},
                'usage': {'input_tokens': 100}})

        client.http = httpx.AsyncClient(transport=httpx.MockTransport(respond))
        try:
            # Includes all three observed failures and both sides of packet boundaries.
            for size in [2, 64, 65, 72, 120, 114, 128, 129, 302]:
                with self.subTest(size=size):
                    bodies.clear()
                    keys = ['direct_answer', 'query_answer'] + [f'link_{i}' for i in range(size-2)]
                    values = {k: i/(size-1) for i, k in enumerate(keys)}
                    questions = {k: decision_question(k, query=True) for k in keys}
                    state = {'page_text': 'Shared prefix with numbered source links'}
                    meter, trace = JevUsage(), Capture()
                    result = await client.noul(state, questions, trace, usage=meter, context={'phase': 'preview'})
                    self.assertEqual(result, values)
                    self.assertEqual([k for b in bodies for k in b['questions']], keys)
                    self.assertEqual(len(bodies), (size+63)//64)
                    self.assertTrue(all(len(b['questions']) <= 64 and b['state'] == state for b in bodies))
                    self.assertEqual(list(bodies[0]['questions'])[:2], ['direct_answer', 'query_answer'])
                    self.assertEqual(meter.calls, len(bodies))
                    self.assertEqual(meter.failures, 0)
                    self.assertEqual(meter.input_tokens, 100*len(bodies))
                    contexts = [e['context'] for e in trace.events if e['event'] == 'jev.request']
                    self.assertEqual([c['packet_index'] for c in contexts], list(range(len(bodies))))
                    self.assertTrue(all(c['total_question_count'] == size for c in contexts))
        finally:
            await client.aclose()

    async def test_failed_owned_group_cancels_active_and_queued_sibling_requests(self):
        cfg = AgentConfig(jev_strategy='raw', jev_entries=6, jev_depth=1,
                          jev_concurrency=2, jev_direct_reads=0, jev_query_reads=0)
        client = LocalDecision(cfg)
        await client.http.aclose()
        client.chunker = chunker()
        started, cancelled = asyncio.Event(), asyncio.Event()
        posted = []

        async def respond(request):
            url = json.loads(request.content)['state']['page_url']
            posted.append(url)
            if url.endswith('/0'):
                await started.wait()
                return httpx.Response(500, json={'error': {'message': 'specific server failure'}})
            started.set()
            try:
                await asyncio.Event().wait()
            finally:
                cancelled.set()

        client.http = httpx.AsyncClient(transport=httpx.MockTransport(respond))
        try:
            with self.assertRaisesRegex(RuntimeError, 'specific server failure'):
                await asyncio.wait_for(_gather_owned(*(client.noul(
                    {'page_url': f'https://example.org/{i}'},
                    {'query_answer': decision_question('target', query=True)},
                    Capture(), usage=JevUsage(), context={}) for i in range(6))), timeout=3)
            self.assertTrue(cancelled.is_set())
            count_at_exit = len(posted)
            await asyncio.sleep(.01)
            self.assertEqual(len(posted), count_at_exit)
            # All active HTTP tasks and slot waiters have been cleaned up.
            for _ in range(2):
                await asyncio.wait_for(client.slots.acquire(), timeout=.1)
            for _ in range(2):
                client.slots.release()
            self.assertEqual(client.inflight_questions, 0)
            self.assertFalse(client.question_waiters)
        finally:
            await client.aclose()

    async def test_nested_workers_are_joined_on_parent_cancellation(self):
        started, cleaned = asyncio.Event(), asyncio.Event()

        async def leaf():
            started.set()
            try:
                await asyncio.Event().wait()
            finally:
                # Cleanup must finish before the parent returns to the caller.
                await asyncio.sleep(.01)
                cleaned.set()

        task = asyncio.create_task(_gather_owned(_gather_owned(leaf())))
        await started.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertTrue(cleaned.is_set())

    async def test_depth_budget_and_browser_body_reuse_including_tail(self):
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
                usage.calls += 1
                usage.attempts += 1
                return {key: .9 if context['phase'] != 'chunk' or 'FINAL_FACT' in state['target_chunk'] else .01
                        for key in questions}

        self_test = self
        fetched = []

        async def fetch(url, *, engine):
            fetched.append((url, engine))
            return Document(url, f'# Source\n\nUseful facts. [First]({url}/a) [Second]({url}/b)\n\n'
                            + ('ordinary evidence ' * 200) + '\n\nFINAL_FACT 42.')

        trace = Capture()
        tree = RawTree(FakeDecision(), cfg, fetch)
        log, text, stats = await tree.run_search('current query',
                    [{'link': f'https://example.org/{i}'} for i in range(10)],
                    question='original target', trace=trace, usage=None)
        self.assertEqual(stats['max_depth'], 5)
        self.assertEqual(stats['fast_fetches'], 0)
        self.assertEqual(stats['browser_fetches'], 50)
        self.assertEqual(stats['reads'], 6)
        self.assertEqual(len(fetched), 50)
        self.assertEqual(len({url for url, _ in fetched}), 50)
        self.assertEqual(stats['summary_calls'], 0)
        self.assertIn('FINAL_FACT', text)
        self.assertLessEqual(tree.jev.chunker.count(text), cfg.jev_output_tokens)
        self.assertTrue(all(engine == 'browser' for _, engine in fetched))
        selected = next(e for e in trace.events if e['event'] == 'rawtree.return')
        ids = [(r['node_id'], i) for r in selected['returned'] for i in r['chunk_ids']]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == '__main__':
    # Selector avoids Proactor pipe issues in restricted Windows test runners.
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    unittest.main()
