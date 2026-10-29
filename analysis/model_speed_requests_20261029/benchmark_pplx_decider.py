"""Reviewable request code from the 2026-10-29 model speed tests.
See README.md beside this file before comparing models.
"""
import argparse
from datetime import datetime, timezone

RUN_STAMP = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')

def run_concurrent():
    import concurrent.futures
    import hashlib
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
    OUT = Path(__file__).with_name(f'{Path(__file__).stem}_concurrent_{RUN_STAMP}.json')
    TARGET = 4096
    rng = random.SystemRandom()
    seen = set()
    audit_states = []
    question = {'type': 'choice', 'instructions': 'Which retrieval strategy best satisfies the stated requirements?',
                'criteria': {'A': 'Always retrieve ten documents without additional searches',
                             'B': 'Use iterative retrieval when evidence is insufficient',
                             'C': 'Retrieve twenty documents and select the top three'}}
    report = {'endpoint': BASE, 'model': 'pplx decider (user-provided identity; model-list endpoint unavailable)',
              'target_input_tokens_per_request': TARGET,
              'method': 'Independent root POST requests, concurrency 1..32. Cryptographically sourced random uppercase-letter contexts, disjoint from prior digit-only contexts. All contexts newly generated, SHA256 and common-prefix audits saved, unique cache_salt per request. Fixed question and server template. Server input-token usage validated at 4096. Bodies prepared before timing. Server-side KV cache disabling cannot be verified through this API.',
              'started_at_utc': datetime.now(timezone.utc).isoformat(), 'calibration': [], 'results': []}


    def save():
        OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')


    def payload(n, suffix=''):
        while True:
            digits = rng.choices('ABCDEFGHJKLMNPQRSTUVWXYZ', k=n)
            prefix = ''.join(digits[:16])
            if prefix not in seen:
                seen.add(prefix)
                break
        state = ' '.join(digits) + suffix
        audit_states.append(state)
        return json.dumps({'state': state,
                           'questions': {'strategy': question}, 'cache_salt': uuid.uuid4().hex}).encode()


    def send(body, gate=None, index=None):
        client = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        request = urllib.request.Request(BASE, data=body, headers={'Content-Type': 'application/json'})
        if gate:
            gate.wait()
        start = time.perf_counter()
        source = json.loads(body)
        row = {'request': index, 'start_perf': start,
               'state_sha256': hashlib.sha256(source['state'].encode()).hexdigest(),
               'state_prefix': source['state'][:64], 'cache_salt': source['cache_salt']}
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
    for suffix in ['', '.', ' .']:
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
    hashes = [hashlib.sha256(state.encode()).hexdigest() for state in audit_states]
    max_prefix = 0
    for i, first in enumerate(audit_states):
        for second in audit_states[i + 1:]:
            shared = 0
            for a, b in zip(first, second):
                if a != b:
                    break
                shared += 1
            max_prefix = max(max_prefix, shared)
    report['input_audit'] = {'total_generated_states': len(audit_states),
                             'unique_state_sha256_count': len(set(hashes)),
                             'duplicate_states': len(hashes) - len(set(hashes)),
                             'maximum_shared_state_prefix_characters': max_prefix,
                             'previous_input_family': 'space-separated digits',
                             'new_input_family': 'space-separated uppercase letters',
                             'all_state_sha256': hashes}
    assert len(hashes) == len(set(hashes)), 'Duplicate state detected'
    print('AUDIT ' + json.dumps(report['input_audit']), flush=True)
    save()
    print('Saved: ' + str(OUT), flush=True)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--test', choices=['concurrent'], default='concurrent',
                        help='1, 2, 4, 8, 16, 32 independent simultaneous root POST requests')
    parser.parse_args()
    run_concurrent()
