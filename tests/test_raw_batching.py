"""Single-state multi-key d3 transport: real request assembly, fake HTTP, no model services."""
import asyncio
import json
import unittest

import httpx

from searchgym.agent import AgentConfig
from searchgym.jevtree import JevUsage
from searchgym.rawtree import LocalDecision, LocalDecisionError
from test_rawtree import Capture, chunker


def original(body, key):
    if '__' not in key:
        return body['state'], key
    item, key = key.split('__', 1)
    return {**body['state']['shared'], **body['state']['items'][item]}, key


class BatchingTests(unittest.IsolatedAsyncioTestCase):
    async def test_timeout_uses_actual_packet_key_count(self):
        self.assertEqual([LocalDecision._packet_timeout(n) for n in (1, 3, 16, 64)],
                         [10, 11, 37, 133])
        posted = []
        async def respond(request):
            body = json.loads(request.content)
            posted.append((len(body['questions']), request.extensions['timeout']))
            return httpx.Response(200, json={'answers': {
                k: {'noul': .6} for k in body['questions']}})
        client = await self.client(respond, jev_concurrency=4)
        await client.noul({'page_text': 'source'}, {
            f'k{i}': {'type': 'noul', 'instructions': 'Useful?'} for i in range(65)},
            Capture(), usage=JevUsage(), context={})
        self.assertEqual(sorted((n, t['read']) for n, t in posted), [(1, 10), (64, 133)])
        self.assertTrue(all(t['connect'] == 5 and t['pool'] == 5 for _, t in posted))

    async def test_overall_timeout_releases_wave_for_next_request(self):
        async def respond(request):
            body = json.loads(request.content)
            if body['state']['page_text'] == 'stalled':
                await asyncio.Event().wait()
            return httpx.Response(200, json={'answers': {'gain': {'noul': .6}}})
        client = await self.client(respond, jev_concurrency=4)
        client._packet_timeout = lambda count: .02
        trace, usage = Capture(), JevUsage()
        questions = {'gain': {'type': 'noul', 'instructions': 'Useful?'}}
        with self.assertRaises(LocalDecisionError) as caught:
            await client.noul({'page_text': 'stalled'}, questions, trace, usage=usage, context={})
        self.assertIn('TimeoutError', str(caught.exception))
        self.assertEqual(usage.failures, 1)
        self.assertEqual(client.inflight_questions, 0)
        self.assertEqual(client.batch_active, 0)
        result = await client.noul({'page_text': 'ready'}, questions, trace, usage=usage, context={})
        self.assertEqual(result, {'gain': .6})

    async def client(self, respond, **kwargs):
        client = LocalDecision(AgentConfig(**kwargs))
        await client.http.aclose()
        client.chunker = chunker()
        client.http = httpx.AsyncClient(transport=httpx.MockTransport(respond))
        self.addAsyncCleanup(client.aclose)
        return client

    async def test_two_objectives_share_one_unchanged_state(self):
        posted = []
        async def respond(request):
            body = json.loads(request.content); posted.append(body)
            return httpx.Response(200, json={'answers': {
                'query_answer': {'noul': .3}, 'direct_answer': {'noul': .8}}})
        client = await self.client(respond)
        state = {'page_text': 'original passage'}
        result = await client.noul(state, {k: {'type': 'noul', 'instructions': k}
            for k in ('direct_answer', 'query_answer')}, Capture(), usage=JevUsage(), context={})
        self.assertEqual(result, {'direct_answer': .8, 'query_answer': .3})
        self.assertEqual(len(posted), 1)
        self.assertEqual(posted[0]['state'], state)

    async def test_33_distinct_states_remain_33_requests_without_swapping_scores(self):
        posted = []
        async def respond(request):
            body = json.loads(request.content); posted.append(body)
            answers = {}
            for key in reversed(body['questions']):
                state, objective = original(body, key)
                answers[key] = {'noul': state['ordinal']/100 + (.001 if objective == 'query_answer' else 0)}
                self.assertEqual(state['previous_chunk'], f'previous_{state["ordinal"]}')
                self.assertIn('Evaluate ONLY', body['questions'][key]['instructions']
                              if '__' in key else 'Evaluate ONLY')
            return httpx.Response(200, json={'answers': answers})
        client = await self.client(respond)
        trace, usage = Capture(), JevUsage()
        states = [{'page_url': 'https://example.org/source', 'ordinal': i,
                   'target_chunk': f'original_{i}', 'previous_chunk': f'previous_{i}'} for i in range(33)]
        results = await asyncio.gather(*(client.noul(state, {
            k: {'type': 'noul', 'instructions': 'Read the target_chunk only.'}
            for k in ('direct_answer', 'query_answer')}, trace, usage=usage,
            context={'search_id': 'search', 'phase': 'chunk', 'chunk_id': i})
            for i, state in enumerate(states)))
        self.assertEqual([len(b['questions']) for b in posted], [2]*33)
        self.assertTrue(all('items' not in b['state'] for b in posted))
        self.assertEqual(usage.calls, 33)
        for i, result in enumerate(results):
            self.assertEqual(result, {'direct_answer': i/100, 'query_answer': i/100+.001})
        self.assertTrue(all(s['target_chunk'] == f'original_{i}' for i, s in enumerate(states)))

    async def test_same_state_unique_link_keys_need_no_scoped_wrapper(self):
        posted = []
        async def respond(request):
            body = json.loads(request.content); posted.append(body)
            return httpx.Response(200, json={'answers': {k: {'noul': .6} for k in body['questions']}})
        client = await self.client(respond)
        trace, usage = Capture(), JevUsage()
        state = {'page_text': 'Original paragraph with two source links.'}
        await asyncio.gather(*(client.noul(state, {f'link_{i}': {'type': 'noul', 'instructions': 'Route?'}},
            trace, usage=usage, context={'search_id': 's', 'phase': 'links'}) for i in range(2)))
        self.assertEqual(len(posted), 1)
        self.assertEqual(posted[0]['state'], state)
        self.assertEqual(set(posted[0]['questions']), {'link_0', 'link_1'})

    async def test_source_budget_splits_inputs_without_truncating_them(self):
        posted = []
        async def respond(request):
            body = json.loads(request.content); posted.append(body)
            return httpx.Response(200, json={'answers': {k: {'noul': .5} for k in body['questions']}})
        client = await self.client(respond, jev_bundle_tokens=50)
        trace, usage = Capture(), JevUsage()
        states = [{'page_text': ' '.join(f'word_{i}_{j}' for j in range(80))} for i in range(2)]
        await asyncio.gather(*(client.noul(state, {'gain': {'type': 'noul', 'instructions': 'Useful?'}},
            trace, usage=usage, context={'phase': 'bundle'}) for state in states))
        self.assertEqual(len(posted), 2)
        self.assertEqual([b['state'] for b in posted], states)

    async def test_missing_key_preserves_other_items_and_partial_objectives(self):
        async def respond(request):
            body = json.loads(request.content)
            return httpx.Response(200, json={'answers': {
                k: {'noul': .7} for k in body['questions'] if not (body['state']['target_chunk'] == '1' and k == 'query_answer')}})
        client = await self.client(respond)
        trace, usage = Capture(), JevUsage()
        results = await asyncio.gather(*(client.noul({'target_chunk': str(i)}, {
            k: {'type': 'noul', 'instructions': 'Useful?'} for k in ('direct_answer', 'query_answer')},
            trace, usage=usage, context={'phase': 'chunk'}) for i in range(2)), return_exceptions=True)
        self.assertEqual(results[0], {'direct_answer': .7, 'query_answer': .7})
        self.assertIsInstance(results[1], LocalDecisionError)
        self.assertEqual(results[1].partial_scores, {'direct_answer': .7})

    async def test_different_searches_and_phases_never_coalesce(self):
        posted = []
        async def respond(request):
            body = json.loads(request.content); posted.append(body)
            return httpx.Response(200, json={'answers': {k: {'noul': .5} for k in body['questions']}})
        client = await self.client(respond)
        trace, usage = Capture(), JevUsage()
        await asyncio.gather(*(client.noul({'page_text': 'same'}, {'gain': {'type': 'noul', 'instructions': 'Useful?'}},
            trace, usage=usage, context={'search_id': search, 'phase': phase})
            for search, phase in [('a', 'chunk'), ('b', 'chunk'), ('a', 'links')]))
        self.assertEqual(len(posted), 3)

    async def test_cancelling_one_item_keeps_its_shared_request_for_other_item(self):
        posted, release = asyncio.Event(), asyncio.Event()
        async def respond(request):
            body = json.loads(request.content); posted.set(); await release.wait()
            return httpx.Response(200, json={'answers': {k: {'noul': .5} for k in body['questions']}})
        client = await self.client(respond)
        trace, usage = Capture(), JevUsage()
        jobs = [asyncio.create_task(client.noul({'page_text': 'same source'},
            {f'gain_{i}': {'type': 'noul', 'instructions': 'Useful?'}}, trace, usage=usage,
            context={'phase': 'chunk'})) for i in range(2)]
        await asyncio.wait_for(posted.wait(), 3)
        jobs[0].cancel()
        with self.assertRaises(asyncio.CancelledError):
            await jobs[0]
        release.set()
        self.assertEqual(await asyncio.wait_for(jobs[1], 3), {'gain_1': .5})
        self.assertEqual(usage.attempts, 1)

    async def test_different_links_keep_their_own_exact_context_and_destination(self):
        posted = []
        async def respond(request):
            body = json.loads(request.content); posted.append(body)
            answers = {}
            for key in reversed(body['questions']):
                state, original_key = original(body, key)
                i = int(original_key.removeprefix('link_'))
                self.assertEqual(state['page_text'], f'Original paragraph {i} [{original_key}]')
                self.assertEqual(state['outgoing_links'], {original_key: f'https://example.org/{i}'})
                answers[key] = {'noul': i/10}
            return httpx.Response(200, json={'answers': answers})
        client = await self.client(respond)
        trace, usage = Capture(), JevUsage()
        results = await asyncio.gather(*(client.noul({
            'page_url': 'https://example.org/parent',
            'page_text': f'Original paragraph {i} [link_{i}]',
            'outgoing_links': {f'link_{i}': f'https://example.org/{i}'}},
            {f'link_{i}': {'type': 'noul', 'instructions': f'Evaluate link_{i}.'}},
            trace, usage=usage, context={'search_id': 's', 'phase': 'links'}) for i in range(3)))
        self.assertEqual(len(posted), 3)
        self.assertTrue(all('items' not in b['state'] for b in posted))
        self.assertEqual(results, [{f'link_{i}': i/10} for i in range(3)])

    async def test_four_64_key_requests_share_wave_without_early_fifth(self):
        four_started, three_finished, release = asyncio.Event(), asyncio.Event(), asyncio.Event()
        posted, finished = [], []
        async def respond(request):
            body = json.loads(request.content)
            name = body['state']['name']; posted.append(name)
            self.assertEqual(len(body['questions']), 64)
            if len(posted) == 4:
                four_started.set()
            if name == 0:
                await release.wait()
            elif name < 4:
                await four_started.wait()
            else:
                self.assertIn(0, finished)
            finished.append(name)
            if all(i in finished for i in (1, 2, 3)):
                three_finished.set()
            return httpx.Response(200, json={'answers': {k: {'noul': .5} for k in body['questions']}})
        client = await self.client(respond)
        trace, usage = Capture(), JevUsage()
        jobs = [asyncio.create_task(client.noul({'name': i}, {
            f'gain_{j}': {'type': 'noul', 'instructions': 'Useful?'} for j in range(64)},
            trace, usage=usage, context={'search_id': str(i), 'phase': 'chunk'})) for i in range(5)]
        try:
            await asyncio.wait_for(three_finished.wait(), 3)
            self.assertEqual(posted, [0, 1, 2, 3])
            release.set()
            results = await asyncio.wait_for(asyncio.gather(*jobs), 3)
            self.assertEqual([len(r) for r in results], [64]*5)
            self.assertTrue(all(e['inflight_questions'] <= 256 for e in trace.events
                                if e['event'] == 'jev.attempt'))
        finally:
            release.set()
            for job in jobs:
                job.cancel()
            await asyncio.gather(*jobs, return_exceptions=True)

    async def test_close_cancels_entire_combined_request_and_releases_limits(self):
        posted, cancelled = asyncio.Event(), asyncio.Event()
        async def respond(request):
            posted.set()
            try:
                await asyncio.Event().wait()
            except asyncio.CancelledError:
                cancelled.set()
                raise
        client = await self.client(respond)
        trace, usage = Capture(), JevUsage()
        jobs = [asyncio.create_task(client.noul({'page_text': 'same source'},
            {f'gain_{i}': {'type': 'noul', 'instructions': 'Useful?'}}, trace, usage=usage,
            context={'phase': 'chunk'})) for i in range(2)]
        await asyncio.wait_for(posted.wait(), 3)
        await client.aclose()
        results = await asyncio.wait_for(asyncio.gather(*jobs, return_exceptions=True), 3)
        self.assertTrue(all(isinstance(r, asyncio.CancelledError) for r in results))
        self.assertTrue(cancelled.is_set())
        self.assertEqual(client.inflight_questions, 0)
        self.assertFalse(client.question_waiters)

    async def test_packing_failure_resolves_all_waiters_without_hanging(self):
        async def respond(request):
            self.fail('Invalid packing must fail before HTTP')
        client = await self.client(respond)
        class BrokenCounter:
            def count(self, text):
                raise ValueError('fake tokenizer failure')
        client.chunker = BrokenCounter()
        trace, usage = Capture(), JevUsage()
        results = await asyncio.wait_for(asyncio.gather(*(client.noul({'page_text': 'same source'},
            {f'gain_{i}': {'type': 'noul', 'instructions': 'Useful?'}}, trace, usage=usage,
            context={'phase': 'chunk'}) for i in range(2)), return_exceptions=True), 3)
        self.assertTrue(all(isinstance(r, LocalDecisionError) for r in results))
        self.assertEqual(usage.attempts, 0)

