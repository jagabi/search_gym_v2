"""Exactly 20 unauthenticated, sequential Reader requests. No retries."""
import json
import random
import statistics
import time
import urllib.error
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
RUNS = [
    '20260920-2130_ragent_gpt-oss-20b_browsecomp_paper_frozen_v1',
    '20260919-1621_search-o1_gpt-oss-20b_browsecomp_paper_frozen_v1',
    '20261004-1329_jevtree_gpt-oss-20b_browsecomp_jevtree_v66_diagnostic10',
]


def main():
    rng = random.Random(20261006)
    pools = []
    for name in RUNS:
        files = sorted((ROOT/'runs/test'/name).glob('q*/trace.jsonl'))
        rng.shuffle(files)
        pool = []
        for f in files:
            candidates = []
            with f.open(encoding='utf-8') as h:
                for line in h:
                    if '"event": "fetch.source"' not in line:
                        continue
                    d = json.loads(line)
                    if d.get('retrieval') == 'jina' and not d.get('is_error'):
                        candidates.append(d['url'])
            if candidates:
                pool.append({'url':rng.choice(candidates),'source_run':name,'question':f.parent.name})
            if len(pool) >= 20:
                break
        pools.append(pool)
    selected, seen = [], set()
    for i in range(20):
        pool = pools[i % 3]
        while pool:
            entry = pool.pop(0)
            if entry['url'] not in seen:
                selected.append(entry)
                seen.add(entry['url'])
                break
    assert len(selected) == 20
    output = {'started_utc':datetime.now(timezone.utc).isoformat(),
        'method':'20 unique URLs sampled from historically successful Jina fetches; 7 RAgent, 7 search-o1, 6 JEV. No API key, no retry, sequential starts spaced at least 3.4s. HTTP duration excludes deliberate spacing, includes DNS/TLS/transfer/server delay. Default Jina server cache behavior.',
        'samples':[]}
    dest = ROOT/'analysis/jina_probe20.json'
    last_start = 0.0
    for i, entry in enumerate(selected, 1):
        time.sleep(max(0, last_start+3.4-time.perf_counter()))
        request = urllib.request.Request('https://r.jina.ai/'+entry['url'],headers={'X-Return-Format':'markdown'})
        started = last_start = time.perf_counter()
        status, size, error, retry_after = None, 0, '', ''
        try:
            with urllib.request.urlopen(request,timeout=60) as response:
                body = response.read()
                status, size = response.status, len(body)
                excerpt = body.decode('utf-8',errors='replace')
                warnings = [line for line in excerpt.splitlines() if line.startswith('Warning:')]
        except urllib.error.HTTPError as exc:
            status = exc.code
            retry_after = exc.headers.get('Retry-After','')
            error = exc.read(500).decode('utf-8',errors='replace')
            warnings = []
        except Exception as exc:
            error = repr(exc)
            warnings = []
        elapsed = time.perf_counter()-started
        row = {**entry,'seconds':round(elapsed,4),'status':status,'bytes':size,'error':error,'warnings':warnings,'retry_after':retry_after}
        output['samples'].append(row)
        dest.write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps({'i':i,'seconds':row['seconds'],'status':status,'bytes':size,'warning':bool(warnings)}),flush=True)
    for label, values in [('all',[r['seconds'] for r in output['samples']]),('http200',[r['seconds'] for r in output['samples'] if r['status']==200]),('http200_without_warning',[r['seconds'] for r in output['samples'] if r['status']==200 and not r['warnings']])]:
        output[label] = {'n':len(values),'mean':statistics.mean(values) if values else None,'median':statistics.median(values) if values else None,'min':min(values) if values else None,'max':max(values) if values else None}
    dest.write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:output[k] for k in ['all','http200','http200_without_warning']}),flush=True)


if __name__ == '__main__':
    main()
