"""Directly replay the slowest 2-key and 8-key packets; record server metrics."""
import concurrent.futures
import json
from pathlib import Path
import threading
import time
import urllib.request
import uuid

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'runs/test/20261017-1754_jevtree_gpt-oss-20b_browsecomp_raw_browser_p8_10/q00040/trace.jsonl'
BASE = 'http://100.89.209.104:8101'


def request(path, body=None):
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    data = json.dumps(body, ensure_ascii=False).encode() if body else None
    req = urllib.request.Request(BASE + path, data=data, headers={'Content-Type': 'application/json'})
    with opener.open(req, timeout=180 if body else 8) as response:
        return response.read().decode()


def metrics():
    raw = request('/metrics')
    values = {}
    for line in raw.splitlines():
        if line and not line.startswith('#'):
            key, value = line.rsplit(' ', 1)
            if key.startswith('vllm:'):
                values[key] = float(value)
    return values


def total(values, name):
    return sum(v for k, v in values.items() if k.startswith('vllm:' + name + '{'))


def main():
    events = [json.loads(line) for line in SOURCE.read_text(encoding='utf-8').splitlines()]
    requests = {e['request_id']: e for e in events if e['event'] == 'jev.request'}
    attempts = {e['request_id']: e for e in events if e['event'] == 'jev.attempt'}
    completed = [e for e in events if e['event'] == 'jev.result']
    out = ROOT / 'analysis' / ('d3_direct_probe_' + time.strftime('%Y%m%d-%H%M%S'))
    out.mkdir()
    summaries = []
    for count in (2, 8):
        original = max((e for e in completed if requests[e['request_id']]['question_count'] == count),
                       key=lambda e: e['elapsed_ms'] - attempts[e['request_id']]['elapsed_ms'])
        job = requests[original['request_id']]
        before = metrics()
        if total(before, 'num_requests_running') or total(before, 'num_requests_waiting'):
            print('Server is busy; no inference submitted.', flush=True)
            break
        folder = out / f'keys{count}'
        folder.mkdir()
        body = {**job['body'], 'request_id': 'direct-' + uuid.uuid4().hex, 'cache_salt': uuid.uuid4().hex}
        (folder / 'request.json').write_text(json.dumps(body, ensure_ascii=False, indent=2), encoding='utf-8')
        samples, stop = [], threading.Event()
        started = time.perf_counter()

        def monitor():
            while not stop.wait(2):
                try:
                    sample = metrics()
                    samples.append({'elapsed_s': time.perf_counter() - started, 'values': sample})
                except Exception as exc:
                    samples.append({'elapsed_s': time.perf_counter() - started, 'error': repr(exc)})

        worker = threading.Thread(target=monitor, daemon=True)
        worker.start()
        print('Sending directly:', count, 'keys;', body['state']['page_url'], flush=True)
        try:
            response = json.loads(request('/v1/systemone', body))
            error = None
        except Exception as exc:
            response, error = {}, repr(exc)
        elapsed = time.perf_counter() - started
        stop.set()
        worker.join(timeout=10)
        after = metrics()
        summary = dict(question_count=count, source_request_id=original['request_id'],
                       url=body['state']['page_url'],
                       original_http_s=(original['elapsed_ms'] - attempts[original['request_id']]['elapsed_ms']) / 1000,
                       direct_http_s=elapsed, usage=response.get('usage'), error=error,
                       returned_keys=len(response.get('answers', {})),
                       metrics_delta={name: total(after, name)-total(before, name) for name in (
                           'request_queue_time_seconds_sum', 'request_queue_time_seconds_count',
                           'request_inference_time_seconds_sum', 'request_inference_time_seconds_count',
                           'request_success_total', 'prompt_tokens_total', 'num_preemptions_total')},
                       peak_internal_waiting=max((total(s.get('values', {}), 'num_requests_waiting')
                                                  for s in samples), default=0),
                       note='Direct urllib POST; no RawTree, LocalDecision semaphore, or proxy. '
                            'One trial on an initially idle server; fresh request_id/cache_salt.')
        for name, value in [('response', response), ('metrics_before', before), ('metrics_after', after),
                            ('metrics_samples', samples), ('summary', summary)]:
            (folder / (name + '.json')).write_text(json.dumps(value, indent=2), encoding='utf-8')
        summaries.append(summary)
        (out / 'summary.json').write_text(json.dumps(summaries, indent=2), encoding='utf-8')
        print(json.dumps(summary), flush=True)
        if error:
            break
    print('Saved:', out, flush=True)


if __name__ == '__main__':
    main()
