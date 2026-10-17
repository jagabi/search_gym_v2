"""Replay four saved source requests through the production bounded client."""
import asyncio
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from searchgym.config import load_test
from searchgym.jevtree import JevUsage
from searchgym.rawtree import LocalDecision
from searchgym.trace import Trace


async def main():
    source = ROOT / 'runs/test/20261017-1720_jevtree_gpt-oss-20b_browsecomp_raw_browser_rolling10/q00040/trace.jsonl'
    events = [json.loads(line) for line in source.read_text(encoding='utf-8').splitlines()]
    jobs = [next(e for e in events if e['event'] == 'jev.request'
                 and e['context']['node_id'] == node and e['context']['packet_index'] == 0)
            for node in ('n0', 'n1', 'n2', 'n3')]
    cfg = load_test(method='jevtree').agent
    client = LocalDecision(cfg)
    out = Path(__file__).resolve().parent / ('backpressure_' + time.strftime('%Y%m%d-%H%M%S'))
    out.mkdir()
    trace = Trace(out / 'trace.jsonl', 'backpressure-probe')
    try:
        before = await client.http.get(cfg.jev_base_url.rstrip('/') + '/metrics')
        before.raise_for_status()
        (out / 'metrics_before.txt').write_text(before.text, encoding='utf-8')
        for line in before.text.splitlines():
            if line.startswith(('vllm:num_requests_running{', 'vllm:num_requests_waiting{')):
                if float(line.rsplit(' ', 1)[1]) != 0:
                    print('Server busy; no inference submitted.', flush=True)
                    return
        meter = JevUsage()
        started = time.perf_counter()

        async def replay(job):
            body = job['body']
            result = await client.noul(body['state'], body['questions'], trace,
                                       usage=meter, context=job['context'])
            assert set(result) == set(body['questions'])
            print('completed', job['context']['node_id'], len(result), flush=True)
            return len(result)

        results = await asyncio.gather(*(replay(job) for job in jobs), return_exceptions=True)
        wall = time.perf_counter() - started
        after = await client.http.get(cfg.jev_base_url.rstrip('/') + '/metrics')
        (out / 'metrics_after.txt').write_text(after.text, encoding='utf-8')
        records = [json.loads(line) for line in trace.path.read_text(encoding='utf-8').splitlines()]
        requests = {e['request_id']: e for e in records if e['event'] == 'jev.request'}
        active, peak_http, batch_id = set(), 0, None
        batch_sizes, boundaries_valid = {}, True
        for event in records:
            if event['event'] == 'jev.attempt':
                if event['batch_id'] != batch_id:
                    boundaries_valid = boundaries_valid and not active
                    batch_id = event['batch_id']
                batch_sizes[batch_id] = batch_sizes.get(batch_id, 0) + 1
                active.add(event['request_id'])
                peak_http = max(peak_http, len(active))
            elif event['event'] in ('jev.result', 'jev.error', 'jev.cancelled'):
                active.discard(event['request_id'])
        durations = [e['duration_ms'] / 1000 for e in records if e['event'] == 'jev.response']
        summary = dict(source=str(source), original_request_sizes=[j['question_count'] for j in jobs],
                       expected_keys=sum(j['question_count'] for j in jobs),
                       returned_keys=sum(r for r in results if isinstance(r, int)),
                       errors=[repr(r) for r in results if isinstance(r, BaseException)],
                       packet_limit=cfg.jev_packet_questions, question_limit=cfg.jev_inflight_questions,
                       peak_http=peak_http,
                       peak_questions=max(e['inflight_questions'] for e in records if e['event'] == 'jev.attempt'),
                       largest_packet=max(e['question_count'] for e in requests.values()),
                       batch_sizes=list(batch_sizes.values()), batch_boundaries_valid=boundaries_valid,
                       http_calls=meter.calls, failures=meter.failures, input_tokens=meter.input_tokens,
                       wall_s=wall, max_http_s=max(durations, default=0),
                       note='One small replay, not a whole-question runtime or controlled speed comparison. '
                            'All keys in the four saved packets preserved; no server settings changed.')
        (out / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
        print(json.dumps(summary), flush=True)
    finally:
        await client.aclose()


if __name__ == '__main__':
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
