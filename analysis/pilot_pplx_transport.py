"""Small live test of integrated transport only; no main model or benchmark."""
import asyncio
import argparse
import json
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from searchgym.config import load_test
from searchgym.jevtree import JevUsage
from searchgym.paths import load_env
from searchgym.pplx_decision import PerplexityDecision
from searchgym.trace import NullTrace


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, default=ROOT / 'analysis/d3_latency_pilots/20261022-133822/requests.json')
    args = parser.parse_args()
    load_env()
    cfg = load_test(method='jevtree', decision_provider='pplx').agent
    client = PerplexityDecision(cfg)
    output = ROOT / 'analysis' / 'pplx_latency_pilots' / (datetime.now().strftime('%Y%m%d-%H%M%S') + '_transport')
    output.mkdir(parents=True)
    class Trace(NullTrace):
        def event(self, kind, **fields):
            with (output / 'trace.jsonl').open('a', encoding='utf-8') as handle:
                handle.write(json.dumps({'event': kind, 'time': time.monotonic(), **fields}, ensure_ascii=False) + '\n')
    trace, usage = Trace(), JevUsage()
    jobs = json.loads(args.inputs.read_text(encoding='utf-8'))
    try:
        await client.prepare()
        async def send(i, job):
            started = time.perf_counter()
            try:
                scores = await client.noul(job['body']['state'], job['body']['questions'], trace,
                    usage=usage, context={'search_id': 'transport_pilot', 'phase': 'bundle', 'node_id': str(i)})
                row = {'index': i, 'keys': job['key_count'], 'ok': len(scores) == job['key_count']}
            except Exception as exc:
                row = {'index': i, 'keys': job['key_count'], 'ok': False, 'error': repr(exc)}
            row['elapsed_s'] = time.perf_counter() - started
            print(json.dumps(row), flush=True)
            return row
        started = time.perf_counter()
        rows = await asyncio.gather(*(send(i, job) for i, job in enumerate(jobs)))
        summary = {'requests': len(rows), 'successes': sum(r['ok'] for r in rows),
                   'wall_s': time.perf_counter() - started, 'reported_input_tokens': usage.input_tokens,
                   'cost_usd': usage.input_tokens / 1e6 * .02, 'rows': rows}
        (output / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
        print(json.dumps({k: v for k, v in summary.items() if k != 'rows'}), flush=True)
        print(str(output), flush=True)
    finally:
        await client.aclose()


asyncio.run(main())
