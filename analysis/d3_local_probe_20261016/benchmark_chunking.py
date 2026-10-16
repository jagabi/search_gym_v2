"""CPU-only saved-document benchmark. No fetch or model inference requests."""
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from searchgym.raw_chunks import SourceChunker

here = Path(__file__).resolve().parent
start = time.perf_counter()
chunker = SourceChunker('vllm-sr/d3-mini', 512)
init_s = time.perf_counter()-start
texts = []
for i in range(5):
    body = json.loads((here / 'single_question_5k' / f'request_{i:02}.json').read_text(encoding='utf-8'))
    texts.append(body['state']['page_text'])
cases = [(f'saved_{i}', t) for i, t in enumerate(texts)]
cases.append(('synthetic_long_10x', '\n\n'.join(texts * 2)))
rows = []
for name, text in cases:
    times = []
    for repeat in range(3):
        start = time.perf_counter()
        chunks = chunker.chunks(text)
        chunk_s = time.perf_counter()-start
        start = time.perf_counter()
        bundles = chunker.bundles(chunks, 5000, 2)
        bundle_s = time.perf_counter()-start
        times.append({'chunk_s': chunk_s, 'bundle_s': bundle_s})
    row = {'case': name, 'source_tokens': chunker.count(text), 'chars': len(text),
           'chunks': len(chunks), 'bundles': len(bundles), 'trials': times}
    rows.append(row)
    print(json.dumps(row), flush=True)
(here / 'chunking_latency.json').write_text(json.dumps({'initialization_s': init_s, 'rows': rows,
    'note': 'CPU only, no model/fetch calls. Initial tokenizer download/import excluded from per-document latency. Five saved page prefixes and one synthetic concatenation; three trials in fixed order.'}, indent=2), encoding='utf-8')
