"""Offline provider wiring, request shape, rolling admission and rate limiting."""
import asyncio
import json
import os
import time
import unittest
from unittest.mock import patch

import httpx

from searchgym.agent import AgentConfig
from searchgym.config import load_test
from searchgym.jevtree import JevUsage
from searchgym.pplx_decision import DecisionRateLimit, PerplexityDecision
from searchgym.raw_policy import raw_policy
from test_rawtree import Capture, chunker


class PerplexityTests(unittest.IsolatedAsyncioTestCase):
    async def test_provider_payload_and_no_local_model_probe(self):
        posted = []
        async def respond(request):
            self.assertEqual(request.url.path, '/v1/decisions')
            self.assertEqual(request.headers['authorization'], 'Bearer offline-key')
            body = json.loads(request.content)
            posted.append(body)
            self.assertEqual(set(body), {'model', 'state', 'questions'})
            return httpx.Response(200, json={'answers': {k: {'noul': .7} for k in body['questions']}})
        cfg = load_test(method='jevtree', decision_provider='pplx').agent
        with patch.dict(os.environ, PERPLEXITY_API_KEY='offline-key'):
            client = PerplexityDecision(cfg)
        await client.http.aclose()
        client.http = httpx.AsyncClient(transport=httpx.MockTransport(respond),
                                       headers={'Authorization': 'Bearer offline-key'})
        self.addAsyncCleanup(client.aclose)
        with patch('searchgym.pplx_decision.SourceChunker', return_value=chunker()):
            await client.prepare()
        result = await client.noul({'page_text': 'source'}, {'gain': {'type': 'noul',
            'instructions': 'Useful?'}}, Capture(), usage=JevUsage(), context={})
        self.assertEqual(result, {'gain': .7})
        self.assertEqual(posted[0]['model'], 'pplx-decider-v1.2')
        self.assertEqual(cfg.jev_concurrency, 16)
        self.assertFalse(raw_policy(cfg, 'jevtree')['http_wave']['wait_for_all'])

    async def test_rolling_admission_does_not_wait_for_other_requests(self):
        with patch.dict(os.environ, PERPLEXITY_API_KEY='offline-key'):
            client = PerplexityDecision(AgentConfig())
        self.addAsyncCleanup(client.aclose)
        async with client._question_slots(3):
            async with client._question_slots(16):
                self.assertEqual(client.inflight_questions, 19)
            async with client._question_slots(64):
                self.assertEqual(client.inflight_questions, 67)
        self.assertEqual(client.inflight_questions, 0)

    async def test_request_pacing_and_expired_token_reservations(self):
        limiter = DecisionRateLimit()
        limiter.tokens.append((time.monotonic() - 61, 12_000_000))
        await limiter.acquire(100)
        self.assertEqual(sum(n for _, n in limiter.tokens), 100)
        before = time.monotonic()
        await limiter.acquire(100)
        self.assertGreaterEqual(time.monotonic() - before, .09)
        self.assertEqual(sum(n for _, n in limiter.tokens), 200)

    async def test_token_budget_wait_can_be_cancelled_without_reserving(self):
        limiter = DecisionRateLimit()
        limiter.tokens.append((time.monotonic(), 12_000_000))
        with self.assertRaises(TimeoutError):
            async with asyncio.timeout(.02):
                await limiter.acquire(1)
        self.assertEqual(len(limiter.tokens), 1)

    async def test_rate_limit_response_sets_shared_cooldown(self):
        with patch.dict(os.environ, PERPLEXITY_API_KEY='offline-key'):
            client = PerplexityDecision(AgentConfig())
        self.addAsyncCleanup(client.aclose)
        client._observe_response(httpx.Response(429, headers={'Retry-After': '3'}))
        self.assertGreater(client.limiter.next_request - time.monotonic(), 2.9)

    async def test_local_provider_keeps_four_request_wave(self):
        cfg = load_test(method='jevtree', decision_provider='d3').agent
        self.assertEqual(cfg.jev_concurrency, 4)
        self.assertTrue(raw_policy(cfg, 'jevtree')['http_wave']['wait_for_all'])
