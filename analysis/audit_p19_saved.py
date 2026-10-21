"""Saved-log audit only. Standard library; no project imports or network calls."""
import collections
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = {}
TERMS = ['nzioki', 'peter king', 'vanderbilt clinical', 'career development',
         'regional differences', 'fleet concentration', 'romanian statistical',
         'elisabeta', 'minnesota', 'japan', 'rockefeller', 'mumbai', 'regal',
         'thiruvananthapuram', '3.25', '209']
for label, pattern in [('p18', '20261021-1340*'), ('p19', '20261021-1739*')]:
    folder = next((ROOT/'runs/test').glob(pattern))
    items = []
    for rec in map(json.loads, (folder/'records.jsonl').read_text(encoding='utf-8').splitlines()):
        qpath = folder/rec['dir']
        response = json.loads((qpath/'response.json').read_text(encoding='utf-8'))
        item = {k: rec.get(k) for k in ['index', 'score', 'latency_s', 'searches', 'stop_reason']}
        item.update(answer=response['answer'], gold=response['gold_answer'])
        searches, requests, depths = {}, {}, collections.defaultdict(collections.Counter)
        actions, stops, phases = collections.Counter(), collections.Counter(), collections.Counter()
        http, queues, finals, failures = [], [], [], []
        hits = collections.defaultdict(list)
        for line in (qpath/'trace.jsonl').open(encoding='utf-8'):
            e = json.loads(line); kind = e['event']; sid = e.get('search_id'); nid = e.get('node_id')
            if kind == 'rawtree.start':
                searches[sid] = dict(query=e['query'], version=e.get('version'), nodes={}, returned=[])
            elif kind == 'rawtree.preview':
                searches[sid]['nodes'][nid] = dict(url=e['url'], depth=e['depth'], read=False)
                depths[e['depth']]['preview'] += 1
            elif kind == 'rawtree.chunks':
                node = searches[sid]['nodes'][nid]; node['read'] = True
                depths[node['depth']]['read'] += 1
            elif kind == 'rawtree.node_action': actions[e['action']] += 1
            elif kind == 'rawtree.traversal_end': stops[e['reason']] += 1
            elif kind == 'rawtree.fetch_failed': failures.append(e)
            elif kind == 'rawtree.return':
                searches[sid].update(stats=e['stats'], seconds=e['duration_s'])
                for source in e['returned']:
                    text = '\n'.join(source['texts'].values())
                    searches[sid]['returned'].append(dict(url=source['source'], text=text))
                    for term in TERMS:
                        if term in text.lower():
                            hits[term].append(dict(search_id=sid, url=source['source']))
            elif kind == 'jev.request':
                requests[e['request_id']] = e['context']; phases[e['context'].get('phase')] += e['question_count']
            elif kind == 'jev.response': http.append(e['duration_ms'])
            elif kind == 'jev.attempt': queues.append(e['queue_ms'])
            elif kind in ('run.final_response', 'run.finalizing'):
                finals.append({k: e.get(k) for k in ['event','text','raw_text','finish_reason','attempt','reason']})
        def dist(values):
            return dict(n=len(values), mean=statistics.mean(values), median=statistics.median(values),
                        max=max(values)) if values else {}
        item.update(search_runs=searches, depths=dict(depths), actions=dict(actions), stops=dict(stops),
                    phases=dict(phases), http_ms=dist(http), queue_ms=dist(queues),
                    finals=finals, failures=failures, hits=dict(hits))
        items.append(item)
    OUTPUT[label] = items
(ROOT/'analysis/p19_saved_audit.json').write_text(json.dumps(OUTPUT,ensure_ascii=False,indent=2),encoding='utf-8')
for label, items in OUTPUT.items():
    depth = collections.defaultdict(collections.Counter)
    for item in items:
        for d, counts in item['depths'].items(): depth[d].update(counts)
    print(label, 'depths', dict(depth))
    for item in items:
        print(json.dumps({k:item[k] for k in ['index','score','latency_s','searches','depths','http_ms','phases','stops']},ensure_ascii=True))
