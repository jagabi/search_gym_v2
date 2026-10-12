"""Offline counts of actual fetch.source events; no model/network requests."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / 'runs/test'


def measure(events):
    counts = Counter(e['url'] for e in events)
    successes = set()
    first_question = {}
    saved = same = cross = 0
    for e in events:
        url, question = e['url'], (e['run'], e['question'])
        if url in successes:
            saved += 1
            if first_question[url] == question:
                same += 1
            else:
                cross += 1
        if not e['is_error']:
            successes.add(url)
            first_question.setdefault(url, question)
    n = len(events)
    return {
        'requests': n, 'unique_urls': len(counts),
        'duplicate_requests': n - len(counts),
        'duplicate_pct': round(100 * (n - len(counts)) / n, 2) if n else 0,
        'successful_cache_hits': saved,
        'successful_cache_hit_pct': round(100 * saved / n, 2) if n else 0,
        'cache_hits_same_question': same, 'cache_hits_other_question_or_run': cross,
        'errors': sum(e['is_error'] for e in events),
        'top_repeated_urls': counts.most_common(8),
    }


def main():
    report, all_events = {}, {}
    for p in sorted(RUNS.glob('*browsecomp*')):
        if not any('_' + m + '_' in p.name for m in ('search-o1', 'ragent', 'depthsearch')):
            continue
        sf = p / 'summary.json'
        if not sf.exists():
            continue
        summary = json.loads(sf.read_text(encoding='utf-8'))
        if summary.get('n') != 300:
            continue
        records = {r['index']: r for line in (p / 'records.jsonl').read_text(encoding='utf-8').splitlines() if line.strip() for r in [json.loads(line)]}
        if any(not (p / f'q{i:05}' / 'trace.jsonl').exists() for i in records):
            print(json.dumps({'skipped_incomplete_trace_run': p.name}), flush=True)
            continue
        events, retrievals = [], Counter()
        for i in sorted(records):
            f = p / f'q{i:05}' / 'trace.jsonl'
            with f.open(encoding='utf-8') as handle:
                for line in handle:
                    if '"event": "fetch.source"' not in line:
                        continue
                    e = json.loads(line)
                    retrievals[e.get('retrieval', '')] += 1
                    events.append({'url': e['url'], 'is_error': bool(e.get('is_error')), 'question': i, 'run': p.name, 'retrieval': e.get('retrieval', '')})
        jina = [e for e in events if e['retrieval'] in ('jina', 'jina_fallback')]
        all_events[p.name] = jina
        report[p.name] = {'n': len(records), 'expected_fetch_attempts': sum(r['fetch_attempts'] for r in records.values()), 'observed_fetch_events': len(events), 'retrievals': dict(retrievals), **measure(jina)}
        print(json.dumps({'run': p.name, **{k:v for k,v in report[p.name].items() if k != 'top_repeated_urls'}}), flush=True)
    names = list(all_events)
    groups = {
        'three_frozen_baselines': [n for n in names if 'paper_frozen_v1' in n],
        'ragent_search_o1_depthsearch_v8': [n for n in names if '_ragent_' in n or '_search-o1_' in n or 'ds_directed_v8' in n],
        'all_complete_trace_runs': names,
    }
    combined = {}
    for label, members in groups.items():
        merged = [e for n in members for e in all_events[n]]
        combined[label] = {'runs': members, **measure(merged)}
        print(json.dumps({'group': label, **{k:v for k,v in combined[label].items() if k not in ('runs', 'top_repeated_urls')}}), flush=True)
    output = {'methodology': 'Exact URL strings; only jina/jina_fallback fetch.source events. Duplicate ratio=(requests-unique)/requests. Success-cache estimate replays each run in question-ID order and runs in directory order, caching only successful fetches; ignores TTL, content changes, concurrency and HTTP-internal retries. Existing fetch.reused events are excluded.', 'runs': report, 'combined': combined}
    (ROOT / 'analysis/fetch_url_duplicates.json').write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf-8')


if __name__ == '__main__':
    main()
