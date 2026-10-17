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
            self.assertEqual(peak_keys, 12)
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
        client = LocalDecision(AgentConfig(jev_inflight_questions=8))
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
