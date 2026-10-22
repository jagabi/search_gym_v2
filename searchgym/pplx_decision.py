"""Perplexity transport for the same raw search decisions and source states."""
import asyncio
import json
import os
import time
import weakref
from collections import deque
from contextlib import asynccontextmanager

from .raw_chunks import SourceChunker
from .rawtree import LocalDecision


class DecisionRateLimit:
    """Shared per event loop across question clients; pace requests and reserve tokens."""
    def __init__(self):
        self.lock = asyncio.Lock()
        self.slots = asyncio.Semaphore(16)
        self.next_request = 0.0
        self.tokens = deque()

    async def acquire(self, tokens):
        if tokens > 12_000_000:
            raise ValueError('Decision request exceeds the local minute token budget')
        while True:
            async with self.lock:
                now = time.monotonic()
                while self.tokens and self.tokens[0][0] <= now - 60:
                    self.tokens.popleft()
                delay = max(0, self.next_request - now)
                if sum(n for _, n in self.tokens) + tokens > 12_000_000:
                    delay = max(delay, self.tokens[0][0] + 60 - now)
                if delay <= 0:
                    self.next_request = now + 1 / 6
                    self.tokens.append((now, tokens))
                    return
            await asyncio.sleep(min(delay, 1.0))


_LIMITERS = weakref.WeakKeyDictionary()


class PerplexityDecision(LocalDecision):
    def __init__(self, config):
        key = os.environ.get('PERPLEXITY_API_KEY')
        if not key:
            raise RuntimeError('PERPLEXITY_API_KEY is required for decision-provider=pplx')
        super().__init__(config)
        self.endpoint = 'https://api.perplexity.ai/v1/decisions'
        self.http.headers['Authorization'] = f'Bearer {key}'
        loop = asyncio.get_running_loop()
        if loop not in _LIMITERS:
            _LIMITERS[loop] = DecisionRateLimit()
        self.limiter = _LIMITERS[loop]
        self.slots = self.limiter.slots

    async def prepare(self):
        async with self.prepare_lock:
            if self.chunker is None:
                # Preserve the source units used by local d3; no local HTTP probe.
                self.chunker = await asyncio.to_thread(SourceChunker, self.cfg.jev_model,
                                                       self.cfg.jev_chunk_tokens)

    def _request_body(self, state, questions, request_id):
        # Decisions rejects unknown top-level fields, including request_id.
        return {'model': 'pplx-decider-v1.2', 'state': state, 'questions': questions}

    @staticmethod
    def _packet_timeout(question_count):
        return 30.0

    async def _admit_request(self, state, questions):
        # UTF-8 bytes conservatively reserve text tokens despite different tokenizers.
        # Includes question text, output tokens and generous protocol overhead.
        reservation = len(json.dumps({'state': state, 'questions': questions},
                                    ensure_ascii=False).encode('utf-8')) + 4096
        await self.limiter.acquire(reservation)

    def _observe_response(self, response):
        if response.status_code == 429:
            try:
                delay = max(1.0, float(response.headers.get('retry-after', '1')))
            except ValueError:
                delay = 1.0
            self.limiter.next_request = max(self.limiter.next_request, time.monotonic() + delay)

    @asynccontextmanager
    async def _question_slots(self, count):
        # Rolling admission: release each completed request without a wave barrier.
        self.batch_id += 1
        batch_id = self.batch_id
        self.inflight_questions += count
        try:
            yield batch_id
        finally:
            self.inflight_questions -= count
