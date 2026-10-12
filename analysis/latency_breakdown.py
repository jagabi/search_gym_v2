"""Read-only replay of saved timing logs; no API calls."""
import json
import re
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / 'runs/test'
PATHS = {
    'ragent': '20260920-2130_ragent_gpt-oss-20b_browsecomp_paper_frozen_v1',
    'search_o1': '20260919-1621_search-o1_gpt-oss-20b_browsecomp_paper_frozen_v1',
    'jev': '20261004-1329_jevtree_gpt-oss-20b_browsecomp_jevtree_v66_diagnostic10',
}


def union(intervals):
    total = 0
    end = -1
    for a, b in sorted(intervals):
        total += max(0, b - max(a, end))
        end = max(end, b)
    return total


def describe(v):
    if not v:
        return {'n': 0}
    s = sorted(v)
    return {'n': len(v), 'sum': sum(v), 'mean': statistics.mean(v),
            'median': statistics.median(v), 'p90': s[int((len(s)-1)*.9)]}


def scan(path):
    counts = Counter()
    calls = {}
    search_api = {}
    batches = {}
    fetch_samples = []
    jev_requests = {}
    jev_http = []
    jev_logical = []
    jev_intervals = []
    selections = {}
    endings = {}
    reader_intervals = []
    main_intervals = []
    main_start = None
    selected_events = {'run.start', 'fetch.source', 'tool.call', 'tool.result', 'search.fetched',
        'jev.request', 'jev.response', 'jev.result', 'jevtree.selection', 'jevtree.search_end',
        'llm.request', 'llm.response', 'run.final_request', 'run.final_response'}
    with path.open(encoding='utf-8') as f:
        for line in f:
            head = line[:1200]
            match = re.search(r'"event": "([^"]+)"', head)
            if not match or match[1] not in selected_events:
                continue
            kind = match[1]
            t = float(re.search(r'"elapsed_ms": ([\d.]+)', head)[1]) / 1000
            if kind == 'run.start':
                counts.clear()
                calls.clear()
                search_api.clear()
                batches.clear()
                fetch_samples.clear()
                jev_requests.clear()
                jev_http.clear()
                jev_logical.clear()
                jev_intervals.clear()
                selections.clear()
                endings.clear()
                reader_intervals.clear()
                main_intervals.clear()
                main_start = None
                continue
            if kind in ('llm.request', 'run.final_request'):
                main_start = t
                continue
            if kind in ('llm.response', 'run.final_response'):
                if main_start is not None:
                    main_intervals.append((main_start, t))
                    main_start = None
                continue
            if kind == 'jev.request':
                rid = re.search(r'"request_id": "([^"]+)"', head)[1]
                jev_requests[rid] = t
                continue
            d = json.loads(line)
            if kind == 'fetch.source':
                counts[d.get('retrieval', 'unknown')] += 1
                counts['all_fetch'] += 1
                counts['fetch_errors'] += bool(d.get('is_error'))
            elif kind == 'tool.call':
                calls[(d['turn'], d['tool'])] = t
            elif kind == 'tool.result':
                if d['tool'] == 'web_fetch' and d.get('duration_ms', 0) > 0:
                    fetch_samples.append({'seconds':d['duration_ms']/1000, 'failed':bool(d.get('is_error'))})
                elif d['tool'] == 'web_search':
                    search_api[d['turn']] = d['duration_ms'] / 1000
            elif kind == 'search.fetched':
                batches[d['turn']] = t
            elif kind == 'jev.response':
                jev_http.append(d['duration_ms']/1000)
            elif kind == 'jev.result':
                jev_logical.append(d['duration_ms']/1000)
                if d['request_id'] in jev_requests:
                    jev_intervals.append((jev_requests[d['request_id']], t))
                counts['jev_failed'] += bool(d.get('failed'))
            elif kind == 'jevtree.selection':
                # There is one web_search in flight in this main-agent loop.
                turn = max(k[0] for k in calls if k[1] == 'web_search')
                selections[d['search_id']] = (t, turn)
            elif kind == 'jevtree.search_end':
                sid = d['search_id']
                endings[sid] = t
                if sid in selections:
                    reader_intervals.append((selections[sid][0], t))
    batch_seconds = [max(0, end-calls[(turn,'web_search')]-search_api[turn])
        for turn,end in batches.items() if (turn,'web_search') in calls and turn in search_api]
    tree_intervals = [(calls[(turn,'web_search')]+search_api[turn], end)
        for end,turn in selections.values() if turn in search_api]
    return {'counts':dict(counts), 'fetch_samples':fetch_samples,
        'search_api_seconds':sum(search_api.values()), 'batch_seconds':batch_seconds,
        'jev_http_seconds':jev_http, 'jev_logical_seconds':jev_logical,
        'jev_union_seconds':union(jev_intervals), 'tree_seconds':union(tree_intervals),
        'tree_minus_jev_seconds':union(tree_intervals)-union(jev_intervals),
        'reader_phase_seconds':union(reader_intervals), 'main_llm_seconds':union(main_intervals)}


def main():
    # Snapshot completion IDs once; include earlier completed diagnostic questions.
    jp = RUNS/PATHS['jev']
    existing_file = ROOT/'analysis/latency_breakdown.json'
    existing = json.loads(existing_file.read_text(encoding='utf-8')) if existing_file.exists() else None
    ids = existing['ids'] if existing else sorted(int(p.parent.name[1:]) for p in jp.glob('q*/response.json'))
    summaries = {}
    rows = {}
    for name, dirname in PATHS.items():
        p = RUNS/dirname
        rows[name] = []
        for pos, i in enumerate(ids):
            q = p/f'q{i:05}'
            d = json.loads((q/'response.json').read_text(encoding='utf-8'))
            if existing:
                old = next(r for r in existing['questions'][name] if r['index'] == i)
                if old['counts'].get('all_fetch',0) == d['fetch_attempts']:
                    rows[name].append(old)
                    continue
            s = scan(q/'trace.jsonl')
            rows[name].append({'index':i, 'latency_s':d['latency_ms']/1000,
                'searches':d['searches'], 'fetch_attempts':d['fetch_attempts'],
                'llm_calls':d['usage']['calls'], **s})
            if (pos+1)%50 == 0:
                print(f'{name}: {pos+1}/{len(ids)}', flush=True)
        rr = rows[name]
        fields = ['latency_s','searches','fetch_attempts','llm_calls','search_api_seconds',
            'jev_union_seconds','tree_seconds','tree_minus_jev_seconds','reader_phase_seconds','main_llm_seconds']
        result = {k:describe([r[k] for r in rr]) for k in fields}
        result['jina_fetches'] = describe([r['counts'].get('jina',0)+r['counts'].get('jina_fallback',0) for r in rr])
        for k in ['batch_seconds','jev_http_seconds','jev_logical_seconds']:
            result[k] = describe([v for r in rr for v in r[k]])
        result['fetch_call_observed_seconds'] = describe([s['seconds'] for r in rr for s in r['fetch_samples']])
        result['fetch_call_success_seconds'] = describe([s['seconds'] for r in rr for s in r['fetch_samples'] if not s['failed']])
        result['jina_per_search'] = result['jina_fetches']['sum']/result['searches']['sum']
        summaries[name] = result
        print(json.dumps({'method':name, 'summary':result}), flush=True)
        (ROOT/'analysis/latency_breakdown_partial.json').write_text(json.dumps({'ids':ids,'summary':summaries},indent=2),encoding='utf-8')
    output = {'ids':ids, 'n':len(ids), 'runs':PATHS, 'summary':summaries, 'questions':rows,
        'limitations':'No per-Jina HTTP start/duration or pacing wait is logged. RAgent fetch-call duration includes pacing/retries/local work. JEV tree-minus-evaluation includes fetch/pacing/retries/native reads/tokenization/logging, not pure Jina service time. Interval unions account for within-question overlap. Questions ordered by ID; historical run concurrency/server conditions differ.'}
    (ROOT/'analysis/latency_breakdown.json').write_text(json.dumps(output,indent=2),encoding='utf-8')


if __name__ == '__main__':
    main()
