"""Standalone paid Decisions API latency pilot; no benchmark integration.

Reuses distinct source states from the local d3 latency pilot. State lengths
are 4096 LOCAL D3 tokens; Perplexity's reported token counts may differ.
"""
import argparse
import asyncio
import json
import os
import statistics
import time
from datetime import datetime
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = 'https://api.perplexity.ai/v1/decisions'


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', default='pplx-decider-v1.2',
                        choices=['pplx-decider-v1.2', 'pplx-decider-flash-v1.2'])
    parser.add_argument('--inputs', type=Path, default=ROOT / 'analysis' /
        'd3_latency_pilots' / '20261022-133822' / 'requests.json')
    args = parser.parse_args()
    load_dotenv(ROOT / '.env')
    key = os.environ.get('PERPLEXITY_API_KEY')
    if not key:
        raise RuntimeError('PERPLEXITY_API_KEY is missing')
    jobs = [j for j in json.loads(args.inputs.read_text(encoding='utf-8')) if j['wave'] in (1, 2)]
    assert len(jobs) == 8 and len({j['state_hash'] for j in jobs}) == 8
    output = ROOT / 'analysis' / 'pplx_latency_pilots' / datetime.now().strftime('%Y%m%d-%H%M%S')
    output.mkdir(parents=True, exist_ok=False)
    results, waves = [], []
    price = .01 if 'flash' in args.model else .02
    print(json.dumps({'model': args.model, 'requests': len(jobs), 'concurrency': 4,
                      'local_d3_state_tokens': 4096, 'output': str(output)}), flush=True)
    async with httpx.AsyncClient(headers={'Authorization': f'Bearer {key}'},
                                 timeout=httpx.Timeout(60, connect=10), trust_env=False) as client:
        async def send(job):
            body = {'model': args.model, 'state': job['body']['state'],
                    'questions': job['body']['questions']}
            assert all(q['type'] == 'noul' for q in body['questions'].values())
            row = {k: job[k] for k in ('wave', 'slot', 'key_count', 'state_hash', 'source', 'source_offset')}
            started = time.perf_counter()
            try:
                async with asyncio.timeout(60):
                    response = await client.post(ENDPOINT, json=body)
                row.update(http_status=response.status_code, request_id=response.headers.get('x-request-id'))
                # Response bodies and request IDs aid diagnosis; never persist auth headers.
                (output / f"response_w{job['wave']}_s{job['slot']}.txt").write_text(response.text, encoding='utf-8')
                response.raise_for_status()
                payload = response.json()
                row['usage'] = payload.get('usage', {})
                row['ok'] = all(isinstance(payload.get('answers', {}).get(k, {}).get('noul'), (int, float))
                                for k in body['questions'])
                row['cost_usd'] = row['usage'].get('input_tokens', 0) / 1e6 * price
            except Exception as exc:
                row.update(ok=False, error=repr(exc))
            row['elapsed_s'] = time.perf_counter() - started
            with (output / 'results.jsonl').open('a', encoding='utf-8') as handle:
                handle.write(json.dumps(row, ensure_ascii=False) + '\n')
            print(json.dumps(row, ensure_ascii=False), flush=True)
            return row
        for wave in (1, 2):
            started = time.perf_counter()
            results.extend(await asyncio.gather(*(send(j) for j in jobs if j['wave'] == wave)))
            waves.append({'wave': wave, 'key_count': 3 if wave == 1 else 16,
                          'wall_s': time.perf_counter() - started})
    summary = {'model': args.model, 'waves': waves, 'groups': {},
               'total_reported_cost_usd': sum(r.get('cost_usd', 0) for r in results)}
    for keys in (3, 16):
        rows = [r for r in results if r['key_count'] == keys]
        good = [r for r in rows if r['ok']]
        summary['groups'][str(keys)] = {'attempts': len(rows), 'successes': len(good),
            'mean_s': statistics.mean(r['elapsed_s'] for r in good) if good else None,
            'min_s': min((r['elapsed_s'] for r in good), default=None),
            'max_s': max((r['elapsed_s'] for r in good), default=None),
            'mean_input_tokens': statistics.mean(r['usage'].get('input_tokens', 0) for r in good) if good else None}
    (output / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print('SUMMARY ' + json.dumps(summary), flush=True)


if __name__ == '__main__':
    asyncio.run(main())
