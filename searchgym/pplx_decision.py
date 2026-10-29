"""Self-hosted pplx decider: same decision API as local d3, different identity check.

The decider server answers the systemone decision API (state + questions ->
answers[key].noul) but exposes no model list, ignores the request's `model`
field and returns no identifying header. Its identity therefore cannot be
proven over HTTP. Startup instead rejects a server that reports a d3 model and
requires one well-formed decision answer before any question runs.
"""
import asyncio
from contextlib import asynccontextmanager

from .raw_chunks import SourceChunker
from .rawtree import LocalDecision

PROBE_STATE = {'page_title': 'Decision probe', 'page_text': 'The treaty was signed in 1842.'}
PROBE_QUESTION = {'probe': {'type': 'noul', 'instructions': 'Does the text state when the treaty was signed?'}}


class DeciderDecision(LocalDecision):
    async def prepare(self):
        async with self.prepare_lock:
            if self.chunker is not None:
                return
            base = self.endpoint.removesuffix('/v1/systemone')
            try:
                listed = await self.http.get(base + '/v1/models')
            except Exception:
                listed = None
            if listed is not None and listed.status_code == 200:
                names = {r.get('id') for r in listed.json().get('data', [])}
                if any(str(n).startswith('vllm-sr/d3') for n in names):
                    raise RuntimeError(f'--decision pplx but the decision server reports d3 models: {sorted(names)}')
            probe = await self.http.post(self.endpoint, json=self._request_body(PROBE_STATE, PROBE_QUESTION, 'probe'),
                                         timeout=30.0)
            probe.raise_for_status()
            score = probe.json()['answers']['probe']['noul']
            if not 0 <= float(score) <= 1:
                raise RuntimeError(f'Decision server returned an invalid probe probability: {score}')
            self.chunker = await asyncio.to_thread(SourceChunker, self.cfg.jev_tokenizer, self.cfg.jev_chunk_tokens)

    @asynccontextmanager
    async def _question_slots(self, count):
        # Rolling admission: each request releases its slot on completion,
        # without waiting for the rest of a wave (decider batches per request).
        self.batch_id += 1
        batch_id = self.batch_id
        self.inflight_questions += count
        try:
            yield batch_id
        finally:
            self.inflight_questions -= count


def decision_client(config):
    """The decision client for --decision: pplx uses the decider check, d3 the model list."""
    from . import rawtree  # looked up at call time so tests can substitute the d3 client
    return DeciderDecision(config) if config.decision_provider == 'pplx' else rawtree.LocalDecision(config)


async def verify_decision_server(config):
    """Fail before any question runs if the server is not serving the requested model."""
    client = decision_client(config)
    try:
        await client.prepare()
    finally:
        await client.aclose()
