"""Decision packet splitting and shared client backpressure, without a server."""
import asyncio
import json
import unittest

import httpx

from searchgym.agent import AgentConfig
from searchgym.jevtree import JevUsage
from searchgym.rawtree import LocalDecision, LocalDecisionError, decision_question
from test_rawtree import Capture


class BackpressureTests(unittest.IsolatedAsyncioTestCase):
    async def test_four_single_judgments_wait_for_entire_wave_across_sources(self):
        client = LocalDecision(AgentConfig())
        await client.http.aclose()
        four_started, three_finished, release_slow = asyncio.Event(), asyncio.Event(), asyncio.Event()
        posted, finished = [], []

        async def respond(request):
            body = json.loads(request.content)
            self.assertEqual(len(body['questions']), 1)
            key = next(iter(body['questions']))
            posted.append(key)
            if len(posted) == 4:
                four_started.set()
            if key == 'a0':
                await release_slow.wait()
            elif key in ('a1', 'a2', 'a3'):
                await four_started.wait()
            finished.append(key)
            if set(('a1', 'a2', 'a3')).issubset(finished):
                three_finished.set()
            if key not in ('a0', 'a1', 'a2', 'a3'):
                self.assertTrue(set(('a0', 'a1', 'a2', 'a3')).issubset(finished))
            await asyncio.sleep(0)
            return httpx.Response(200, json={'answers': {key: {'noul': .5}}})

        client.http = httpx.AsyncClient(transport=httpx.MockTransport(respond))
        trace = Capture()
        def call(prefix, size):
            return client.noul({'page_text': prefix},
                {f'{prefix}{i}': decision_question('target', query=True) for i in range(size)},
                trace, usage=JevUsage(), context={'source': prefix})

        tasks = [asyncio.create_task(call('a', 8)), asyncio.create_task(call('b', 5))]
        try:
            await asyncio.wait_for(three_finished.wait(), timeout=3)
            await asyncio.sleep(.02)
            self.assertEqual(posted, ['a0', 'a1', 'a2', 'a3'])
            release_slow.set()
            results = await asyncio.wait_for(asyncio.gather(*tasks), timeout=3)
            self.assertEqual([len(result) for result in results], [8, 5])
            self.assertEqual(len(set(posted)), 13)
            # A batch ID cannot advance while an HTTP request in it is active.
            active = set()
            batch_id = None
            for event in trace.events:
                if event['event'] == 'jev.attempt':
                    if event['batch_id'] != batch_id:
                        self.assertFalse(active)
                        batch_id = event['batch_id']
                    active.add(event['request_id'])
                    self.assertLessEqual(len(active), 4)
                elif event['event'] in ('jev.result', 'jev.error', 'jev.cancelled'):
                    active.remove(event['request_id'])
            self.assertFalse(active)
            self.assertEqual(client.batch_active, 0)
        finally:
            release_slow.set()
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            await client.aclose()

    async def test_failed_key_keeps_successful_siblings_and_stops_after_wave(self):
        client = LocalDecision(AgentConfig())
        await client.http.aclose()
        posted = []

        async def respond(request):
            key = next(iter(json.loads(request.content)['questions']))
            posted.append(key)
            await asyncio.sleep(.01)
            if key == 'key_0':
                return httpx.Response(500, text='unavailable')
            return httpx.Response(200, json={'answers': {key: {'noul': .5}}})

        client.http = httpx.AsyncClient(transport=httpx.MockTransport(respond))
        try:
            with self.assertRaises(LocalDecisionError) as caught:
                await client.noul('source', {f'key_{i}': decision_question('target', query=True)
                    for i in range(9)}, Capture(), usage=JevUsage(), context={})
            self.assertEqual(posted, ['key_0', 'key_1', 'key_2', 'key_3'])
            self.assertEqual(caught.exception.partial_scores, {f'key_{i}': .5 for i in range(1, 4)})
            self.assertEqual(client.inflight_questions, 0)
            self.assertEqual(client.batch_active, 0)
        finally:
            await client.aclose()

    async def test_small_packets_preserve_every_key_under_shared_weighted_limit(self):
        client = LocalDecision(AgentConfig(jev_packet_questions=8, jev_inflight_questions=12))
        await client.http.aclose()
        active_keys = active_http = peak_keys = peak_http = 0
        bodies = []

        async def respond(request):
            nonlocal active_keys, active_http, peak_keys, peak_http
            body = json.loads(request.content)
            bodies.append(body)
            size = len(body['questions'])
            active_keys += size
            active_http += 1
            peak_keys = max(peak_keys, active_keys)
            peak_http = max(peak_http, active_http)
            try:
                await asyncio.sleep(.01)
                return httpx.Response(200, json={'answers': {
                    k: {'noul': int(k.removeprefix('key_')) / 100}
                    for k in reversed(body['questions'])}})
            finally:
                active_keys -= size
                active_http -= 1

        client.http = httpx.AsyncClient(transport=httpx.MockTransport(respond))
        trace = Capture()
        sizes = [25, 2, 2, 33]
        try:
            results = await asyncio.wait_for(asyncio.gather(*(client.noul(
                {'page_text': f'source_{i}'},
                {f'key_{k}': decision_question('target', query=True) for k in range(size)},
                trace, usage=JevUsage(), context={'source': i})
                for i, size in enumerate(sizes))), timeout=3)
            self.assertLessEqual(peak_keys, 12)
            self.assertLessEqual(peak_http, 4)
            self.assertTrue(all(len(b['questions']) <= 8 for b in bodies))
            for i, size in enumerate(sizes):
                self.assertEqual(results[i], {f'key_{k}': k / 100 for k in range(size)})
                source_packets = [b for b in bodies if b['state']['page_text'] == f'source_{i}']
                self.assertEqual([k for b in source_packets for k in b['questions']],
                                 [f'key_{k}' for k in range(size)])
                self.assertEqual(len(source_packets), (size + 7) // 8)
            self.assertTrue(all(e['inflight_questions'] <= 12 for e in trace.events
                                if e['event'] == 'jev.attempt'))
            self.assertEqual(client.inflight_questions, 0)
            self.assertFalse(client.question_waiters)
        finally:
            await client.aclose()

    async def test_cancelling_weight_waiter_and_http_releases_both_limits(self):
        client = LocalDecision(AgentConfig(jev_packet_questions=8, jev_inflight_questions=8))
        await client.http.aclose()
        posted = asyncio.Event()

        async def respond(request):
            posted.set()
            await asyncio.Event().wait()

        client.http = httpx.AsyncClient(transport=httpx.MockTransport(respond))
        questions = {f'key_{i}': decision_question('target', query=True) for i in range(8)}

        def call():
            return client.noul('source', questions, Capture(), usage=JevUsage(), context={})

        tasks = []
        try:
            tasks.append(asyncio.create_task(call()))
            await asyncio.wait_for(posted.wait(), timeout=3)
            tasks.append(asyncio.create_task(call()))
            for _ in range(100):
                if client.question_waiters:
                    break
                await asyncio.sleep(0)
            self.assertEqual(len(client.question_waiters), 1)
            tasks[1].cancel()
            with self.assertRaises(asyncio.CancelledError):
                await tasks[1]
            self.assertEqual(client.inflight_questions, 8)
            self.assertFalse(client.question_waiters)
            tasks[0].cancel()
            with self.assertRaises(asyncio.CancelledError):
                await tasks[0]
            self.assertEqual(client.inflight_questions, 0)
            await client.http.aclose()
            client.http = httpx.AsyncClient(transport=httpx.MockTransport(lambda request:
                httpx.Response(200, json={'answers': {k: {'noul': .5} for k in questions}})))
            self.assertEqual(len(await asyncio.wait_for(call(), timeout=3)), 8)
        finally:
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            await client.aclose()

    async def test_transport_failure_releases_weight_before_next_request(self):
        client = LocalDecision(AgentConfig(jev_packet_questions=8, jev_inflight_questions=8))
        await client.http.aclose()
        attempts = 0

        async def respond(request):
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise httpx.ReadTimeout('simulated', request=request)
            body = json.loads(request.content)
            return httpx.Response(200, json={'answers': {k: {'noul': .5} for k in body['questions']}})

        client.http = httpx.AsyncClient(transport=httpx.MockTransport(respond))
        questions = {f'key_{i}': decision_question('target', query=True) for i in range(8)}
        try:
            with self.assertRaises(LocalDecisionError):
                await client.noul('source', questions, Capture(), usage=JevUsage(), context={})
            result = await asyncio.wait_for(client.noul(
                'source', questions, Capture(), usage=JevUsage(), context={}), timeout=3)
            self.assertEqual(len(result), 8)
            self.assertEqual(client.inflight_questions, 0)
            self.assertFalse(client.question_waiters)
        finally:
            await client.aclose()
