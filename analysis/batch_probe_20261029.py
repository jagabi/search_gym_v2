import json
import random
import time
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

BASE = 'http://172.16.3.192:8101'
MODEL = 'vllm-sr/d3-mini'
OUT = Path(__file__).with_suffix('.json')
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def post(path, body):
    request = urllib.request.Request(
        BASE + path, data=json.dumps(body).encode(),
        headers={'Content-Type': 'application/json'}, method='POST')
    with opener.open(request, timeout=600) as response:
        return json.load(response)


pool = post('/tokenize', {
    'model': MODEL,
    'prompt': 'The quick brown fox jumps over the lazy dog. 가나다라 데이터 검색 테스트 0123456789',
    'add_special_tokens': False,
})['tokens']
pool = list(set(pool))
rng = random.SystemRandom()
prefixes = set()
report = {
    'started_at_utc': datetime.now(timezone.utc).isoformat(),
    'base_url': BASE, 'model': MODEL, 'input_tokens_per_prompt': 4096,
    'endpoint': '/pooling', 'task': 'classify',
    'method': 'One /pooling request containing a batch of 4096-token ID inputs per size; all inputs randomized from their first token; unique cache_salt per batch; one run per size after a 32-token warmup. No generation.',
    'results': [],
}


def save():
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')


warmup = post('/pooling', {
    'model': MODEL, 'input': [rng.choice(pool) for _ in range(32)],
    'task': 'classify', 'add_special_tokens': False, 'cache_salt': uuid.uuid4().hex,
})
report['warmup_usage'] = warmup.get('usage')
print('Warmup complete: ' + json.dumps(report['warmup_usage']), flush=True)
save()

for size in [1, 2, 4, 8, 16, 32, 64]:
    prompts = []
    for _ in range(size):
        while True:
            prompt = [rng.choice(pool) for _ in range(4096)]
            prefix = tuple(prompt[:16])
            if prefix not in prefixes:
                prefixes.add(prefix)
                prompts.append(prompt)
                break
    payload = {'model': MODEL, 'input': prompts, 'task': 'classify',
               'add_special_tokens': False, 'cache_salt': uuid.uuid4().hex}
    print(f'Starting batch={size}, input_tokens={size * 4096}', flush=True)
    start = time.perf_counter()
    try:
        response = post('/pooling', payload)
        elapsed = time.perf_counter() - start
        usage = response.get('usage', {})
        row = {
            'batch_size': size, 'elapsed_seconds': elapsed,
            'amortized_seconds_per_prompt': elapsed / size,
            'prompts_per_second': size / elapsed,
            'input_tokens_per_second': usage.get('prompt_tokens', size * 4096) / elapsed,
            'usage': usage, 'result_count': len(response.get('data', [])),
            'output_dimensions': [len(c.get('data', [])) for c in response.get('data', [])],
        }
        row['valid'] = (usage.get('prompt_tokens') == size * 4096
                        and row['result_count'] == size)
    except Exception as error:
        row = {'batch_size': size, 'elapsed_seconds': time.perf_counter() - start,
               'error': str(error)}
        if hasattr(error, 'read'):
            row['error_body'] = error.read().decode(errors='replace')
    report['results'].append(row)
    save()
    print(json.dumps(row, ensure_ascii=False), flush=True)

report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
save()
print('Saved: ' + str(OUT), flush=True)
