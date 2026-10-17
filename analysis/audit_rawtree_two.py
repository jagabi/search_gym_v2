"""Read-only trace audit of the first two finished rawtree questions."""
import collections
import json
from pathlib import Path
import statistics

RUN = Path('runs/test/20261016-2310_jevtree_gpt-oss-20b_browsecomp_raw_d3_c4_d5_10')


def coverage(spans, duration):
    points = [(0, '', 0), (duration, '', 0)]
    for kind, start, end in spans:
        start, end = max(0, start), min(duration, end)
        if end > start:
            points.extend([(start, kind, 1), (end, kind, -1)])
    active, result = collections.Counter(), collections.Counter()
    last = 0
    for t, kind, delta in sorted(points):
        key = '+'.join(sorted(k for k, count in active.items() if count > 0)) or 'other'
        result[key] += t-last
        active[kind] += delta
        last = t
    return dict(result)


output = {}
for q in ['q00326', 'q00117']:
    response = json.loads((RUN/q/'response.json').read_text(encoding='utf-8'))
    duration = response['latency_ms']/1000
    requests, attempts, phases = {}, {}, collections.defaultdict(list)
    spans, searches, errors, fetches, returns, llms = [], [], [], [], [], {}
    after_end = collections.Counter()
    for line in (RUN/q/'trace.jsonl').open(encoding='utf-8'):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        t, event = e['elapsed_ms']/1000, e['event']
        if t > duration + .01:
            after_end[event] += 1
        if event == 'jev.request':
            requests[e['request_id']] = {'start': t, 'context': e['context'],
                                         'state': e['body']['state']}
        elif event == 'jev.attempt':
            attempts[e['request_id']] = t
            spans.append(('decision_queue', requests[e['request_id']]['start'], t))
        elif event in ['jev.response', 'jev.error']:
            rid = e['request_id']; r = requests[rid]; started = attempts[rid]
            spans.append(('decision_active', started, t))
            row = {'elapsed_s': t, 'service_s': t-started, 'queue_s': started-r['start'],
                   'search_id': r['context']['search_id'], 'node_id': r['context']['node_id']}
            if event == 'jev.error':
                errors.append({**row, 'error': e['error'], 'context': r['context'], 'state': r['state']})
            else:
                body = json.loads(e['response_text'])
                row['tokens'] = body.get('usage', {}).get('input_tokens', 0)
                phases[r['context']['phase']].append(row)
        elif event == 'fetch.raw':
            dt = e['duration_ms']/1000
            spans.append((e['retrieval'], t-dt, t))
            fetches.append({'url': e['url'], 'retrieval': e['retrieval'], 'duration_s': dt, 'error': e['is_error']})
        elif event == 'llm.request':
            llms[e['turn']] = t
        elif event == 'llm.response' and e['turn'] in llms:
            spans.append(('main_llm', llms[e['turn']], t))
        elif event == 'rawtree.start':
            searches.append({'search_id': e['search_id'], 'query': e['query'], 'start_s': t})
        elif event == 'rawtree.return':
            returns.append({k:e[k] for k in ['search_id', 'duration_s', 'stats', 'returned']})
    by_phase = {}
    for phase, rows in phases.items():
        by_phase[phase] = {'count': len(rows), 'tokens': sum(r['tokens'] for r in rows)}
        for key in ['service_s', 'queue_s']:
            vals = [r[key] for r in rows]
            by_phase[phase][key] = {'sum':sum(vals), 'mean':statistics.mean(vals),
                                  'median':statistics.median(vals), 'max':max(vals)}
    parts = coverage(spans, duration)
    unions = {kind:sum(v for k,v in parts.items() if kind in k.split('+'))
              for kind in ['decision_queue', 'decision_active', 'jina_curl', 'jina_browser', 'main_llm']}
    # Fetch-or-decision durations are unions, not sums across parallel requests.
    unions['any_decision_pending'] = sum(v for k,v in parts.items() if 'decision_' in k)
    unions['any_fetch'] = sum(v for k,v in parts.items() if 'jina_' in k)
    depth_counts = collections.Counter()
    returned_depths = []
    for step in response['steps']:
        for tool in step.get('tool_calls', []):
            for tree in tool.get('explorations', []):
                node_depth = {}
                def walk(node):
                    node_depth[node['node_id']] = node['depth']
                    if node['depth']:
                        depth_counts[node['depth']] += 1
                    for child in node['opened']:
                        walk(child)
                walk(tree)
                for ret in tree.get('returned_chunks', []):
                    returned_depths.append({**ret, 'depth':node_depth[ret['node_id']], 'search_id':tree['search_id']})
    output[q] = {'latency_s':duration, 'question':response['question'], 'gold':response['gold_answer'],
                 'answer':response['answer'], 'phase_stats':by_phase, 'interval_partitions_s':parts,
                 'interval_unions_s':unions, 'searches':searches, 'returns':returns, 'errors':errors,
                 'fetches':fetches, 'node_counts_by_depth':dict(depth_counts),
                 'returned_chunk_groups':returned_depths, 'events_after_run_end':dict(after_end)}
    print(q, json.dumps({'duration':duration, 'unions':unions, 'partitions':parts,
                         'nodes_by_depth':dict(depth_counts),
                         'returned_groups_by_depth':dict(collections.Counter(r['depth'] for r in returned_depths))}, indent=2))
Path('analysis/rawtree_first_two_audit.json').write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
