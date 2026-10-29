import concurrent.futures
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = 'http://172.16.3.192:8101'
OUT = Path(__file__).with_suffix('.json')
cases = [(p, None) for p in ['/health', '/v1/models', '/openapi.json', '/does-not-exist']]
cases += [
    ('/tokenize', {'prompt': 'A short test.', 'add_special_tokens': False}),
    ('/pooling', {'input': [[760, 13], [3841, 13]], 'task': 'classify', 'add_special_tokens': False}),
    ('/classify', {'input': ['A short test.', 'Another short test.']}),
    ('/v1/decisions', {'model': 'pplx-decider', 'input': 'The sky is blue.', 'questions': [{'type': 'predicate', 'id': 'q1', 'question': 'Is the sky blue?'}]}),
    ('/v1/systemone', {'state': 'The sky is blue.', 'questions': {'q1': {'type': 'predicate', 'question': 'Is the sky blue?'}}}),
    ('/v1/completions', {'model': 'pplx-decider', 'prompt': 'Hello', 'max_tokens': 1}),
    ('/v1/chat/completions', {'model': 'pplx-decider', 'messages': [{'role': 'user', 'content': 'Hello'}], 'max_tokens': 1}),
    ('/pooling', {'model': 'perplexity-ai/pplx-decider', 'input': 'A short test.'}),
    ('/pooling', {'model': 'pplx-decider-v1.2', 'input': [[760, 13]], 'task': 'classify'}),
]


def probe(case):
    path, body = case
    client = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    request = urllib.request.Request(BASE + path, data=None if body is None else json.dumps(body).encode(),
                                     headers={'Content-Type': 'application/json'})
    start = time.perf_counter()
    row = {'path': path, 'method': request.get_method(), 'request': body}
    try:
        with client.open(request, timeout=20) as response:
            row.update(status=response.status, body=response.read().decode(errors='replace'))
    except urllib.error.HTTPError as error:
        row.update(status=error.code, body=error.read().decode(errors='replace'), request_id=error.headers.get('x-request-id'))
    except Exception as error:
        row['error'] = str(error)
    row['seconds'] = time.perf_counter() - start
    print(json.dumps(row, ensure_ascii=False), flush=True)
    return row


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    rows = list(executor.map(probe, cases))
OUT.write_text(json.dumps({'tested_at_utc': datetime.now(timezone.utc).isoformat(), 'base_url': BASE,
                           'proxy': 'disabled', 'results': rows}, ensure_ascii=False, indent=2), encoding='utf-8')
print('Saved: ' + str(OUT), flush=True)
