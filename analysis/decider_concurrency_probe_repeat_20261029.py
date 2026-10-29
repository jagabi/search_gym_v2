import concurrent.futures
import json
import random
import statistics
import threading
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

BASE = 'http://172.16.3.192:8101/'
OUT = Path(__file__).with_suffix('.json')
TARGET = 4096
rng = random.Random(uuid.uuid4().int)
seen = set()
question = {'type': 'choice', 'instructions': 'Which retrieval strategy best satisfies the stated requirements?',
            'criteria': {'A': 'Always retrieve ten documents without additional searches',
                         'B': 'Use iterative retrieval when evidence is insufficient',
                         'C': 'Retrieve twenty documents and select the top three'}}
report = {'endpoint': BASE, 'model': 'pplx decider (user-provided identity; model-list endpoint unavailable)',
          'target_input_tokens_per_request': TARGET,
          'method': 'Independent root POST requests released simultaneously per concurrency level, not a server batch API. Random digit context differs from the first token for all requests. One choice question per request. All input token counts include template/question overhead and are checked against response usage. Bodies prepared before timing. No generation.',
          'started_at_utc': datetime.now(timezone.utc).isoformat(), 'calibration': [], 'results': []}


def save():
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')


def payload(n, suffix=''):
    while True:
        digits = rng.choices('0123456789', k=n)
        prefix = ''.join(digits[:16])
        if prefix not in seen:
            seen.add(prefix)
            break
    return json.dumps({'state': ' '.join(digits) + suffix,
                       'questions': {'strategy': question}, 'cache_salt': uuid.uuid4().hex}).encode()


def send(body, gate=None, index=None):
    client = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    request = urllib.request.Request(BASE, data=body, headers={'Content-Type': 'application/json'})
    if gate:
        gate.wait()
    start = time.perf_counter()
    row = {'request': index, 'start_perf': start}
    try:
        with client.open(request, timeout=600) as response:
            data = json.load(response)
            row['status'] = response.status
        row.update(usage=data.get('usage', {}), answer_count=len(data.get('answers', {})))
        row['valid'] = (row['status'] == 200 and row['usage'].get('input_tokens') == TARGET
                        and row['usage'].get('sequences') == 1 and row['answer_count'] == 1)
    except urllib.error.HTTPError as error:
        row.update(status=error.code, error=error.read().decode(errors='replace'), valid=False)
    except Exception as error:
        row.update(error=str(error), valid=False)
    row['end_perf'] = time.perf_counter()
    row['elapsed_seconds'] = row['end_perf'] - start
    return row


calibrated = None
for suffix in ['', '.']:
    probes = []
    for n in [16, 32]:
        row = send(payload(n, suffix))
        row.update(digits=n, suffix=suffix)
        report['calibration'].append(row)
        probes.append(row)
        print('CALIBRATION ' + json.dumps(row), flush=True)
        save()
        if 'usage' not in row:
            raise RuntimeError('Calibration failed; see saved response')
    first, second = (r['usage']['input_tokens'] for r in probes)
    slope = (second - first) / 16
    estimated = 16 + (TARGET - first) / slope
    if estimated.is_integer():
        calibrated = (int(estimated), suffix)
        break
if calibrated is None:
    raise RuntimeError('Could not calibrate exact input token count')

n, suffix = calibrated
warmup = send(payload(n, suffix))
report['warmup'] = warmup
report['digits_per_context'] = n
report['suffix'] = suffix
save()
print('WARMUP ' + json.dumps(warmup), flush=True)
if not warmup['valid']:
    raise RuntimeError('4096-token warmup validation failed')

for concurrency in [1, 2, 4, 8, 16, 32]:
    bodies = [payload(n, suffix) for _ in range(concurrency)]
    gate = threading.Barrier(concurrency + 1)
    print(f'START concurrency={concurrency}', flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(send, body, gate, index + 1) for index, body in enumerate(bodies)]
        start = time.perf_counter()
        gate.wait()
        rows = [future.result() for future in concurrent.futures.as_completed(futures)]
    elapsed = max(row['end_perf'] for row in rows) - start
    for row in rows:
        row['start_offset_seconds'] = row.pop('start_perf') - start
        row['completion_offset_seconds'] = row.pop('end_perf') - start
    valid = [row for row in rows if row['valid']]
    latencies = [row['elapsed_seconds'] for row in rows]
    tokens = sum(row['usage']['input_tokens'] for row in valid)
    summary = {'concurrency': concurrency, 'total_elapsed_seconds': elapsed,
               'success': len(valid), 'failed': concurrency - len(valid),
               'mean_request_seconds': statistics.mean(latencies),
               'p50_request_seconds': statistics.median(latencies),
               'min_request_seconds': min(latencies), 'max_request_seconds': max(latencies),
               'requests_per_second': len(valid) / elapsed,
               'input_tokens_per_second': tokens / elapsed, 'total_valid_input_tokens': tokens,
               'dispatch_spread_seconds': max(row['start_offset_seconds'] for row in rows) - min(row['start_offset_seconds'] for row in rows)}
    report['results'].append({**summary, 'requests': sorted(rows, key=lambda row: row['request'])})
    save()
    print('RESULT ' + json.dumps(summary), flush=True)

report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
save()
print('Saved: ' + str(OUT), flush=True)
