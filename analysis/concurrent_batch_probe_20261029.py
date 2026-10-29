import concurrent.futures
import json
import random
import statistics
import threading
import time
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

BASE = 'http://172.16.3.192:8101'
MODEL = 'vllm-sr/d3-mini'
OUT = Path(__file__).with_suffix('.json')
COUNT, BATCH, LENGTH = 10, 32, 4096


def opener():
    return urllib.request.build_opener(urllib.request.ProxyHandler({}))


token_request = urllib.request.Request(
    BASE + '/tokenize',
    data=json.dumps({'model': MODEL, 'prompt': 'The quick brown fox jumps over the lazy dog. 가나다라 데이터 검색 테스트 0123456789', 'add_special_tokens': False}).encode(),
    headers={'Content-Type': 'application/json'})
with opener().open(token_request, timeout=30) as response:
    pool = list(set(json.load(response)['tokens']))

rng = random.Random(uuid.uuid4().int)
prefixes = set()
payloads = []
for _ in range(COUNT):
    inputs = []
    for _ in range(BATCH):
        while True:
            tokens = rng.choices(pool, k=LENGTH)
            prefix = tuple(tokens[:16])
            if prefix not in prefixes:
                prefixes.add(prefix)
                inputs.append(tokens)
                break
    payloads.append(json.dumps({'model': MODEL, 'input': inputs, 'task': 'classify',
                               'add_special_tokens': False, 'cache_salt': uuid.uuid4().hex}).encode())

barrier = threading.Barrier(COUNT + 1)
report = {'base_url': BASE, 'model': MODEL, 'endpoint': '/pooling', 'task': 'classify',
          'concurrent_requests': COUNT, 'batch_size': BATCH, 'input_tokens_per_prompt': LENGTH,
          'total_inputs': COUNT * BATCH, 'total_input_tokens': COUNT * BATCH * LENGTH,
          'method': '10 simultaneous HTTP requests, pre-encoded bodies, 32 distinct random 4096-token inputs per request, unique cache_salt per request; timing includes HTTP and server queueing; no generation.',
          'results': []}


def run(index):
    client = opener()
    request = urllib.request.Request(BASE + '/pooling', data=payloads[index],
                                     headers={'Content-Type': 'application/json'})
    barrier.wait()
    started = time.perf_counter()
    row = {'request': index + 1, 'start_perf': started}
    try:
        with client.open(request, timeout=600) as response:
            result = json.load(response)
        row.update(usage=result.get('usage', {}), result_count=len(result.get('data', [])))
        row['valid'] = row['result_count'] == BATCH and row['usage'].get('prompt_tokens') == BATCH * LENGTH
    except Exception as error:
        row.update(error=str(error), valid=False)
        if hasattr(error, 'read'):
            row['error_body'] = error.read().decode(errors='replace')
    row['end_perf'] = time.perf_counter()
    row['elapsed_seconds'] = row['end_perf'] - started
    return row


with concurrent.futures.ThreadPoolExecutor(max_workers=COUNT) as executor:
    futures = [executor.submit(run, i) for i in range(COUNT)]
    report['started_at_utc'] = datetime.now(timezone.utc).isoformat()
    wall_start = time.perf_counter()
    barrier.wait()
    print(f'Dispatched {COUNT} simultaneous requests x {BATCH} inputs x {LENGTH} tokens', flush=True)
    for future in concurrent.futures.as_completed(futures):
        row = future.result()
        row['start_offset_seconds'] = row.pop('start_perf') - wall_start
        row['completion_offset_seconds'] = row.pop('end_perf') - wall_start
        report['results'].append(row)
        OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
        print(json.dumps(row), flush=True)

elapsed = max(r['completion_offset_seconds'] for r in report['results'])
latencies = [r['elapsed_seconds'] for r in report['results']]
successful = [r for r in report['results'] if r['valid']]
report['summary'] = {
    'total_elapsed_seconds': elapsed, 'successful_requests': len(successful),
    'failed_requests': COUNT - len(successful),
    'mean_request_seconds': statistics.mean(latencies),
    'p50_request_seconds': statistics.median(latencies),
    'min_request_seconds': min(latencies), 'max_request_seconds': max(latencies),
    'requests_per_second': len(successful) / elapsed,
    'inputs_per_second': len(successful) * BATCH / elapsed,
    'input_tokens_per_second': sum(r['usage']['prompt_tokens'] for r in successful) / elapsed,
    'dispatch_spread_seconds': max(r['start_offset_seconds'] for r in report['results']) - min(r['start_offset_seconds'] for r in report['results']),
}
report['results'].sort(key=lambda r: r['request'])
report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
print('SUMMARY ' + json.dumps(report['summary']), flush=True)
print('Saved: ' + str(OUT), flush=True)
