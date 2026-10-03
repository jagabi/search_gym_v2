"""Reconstruct per-question phase wall time; merge overlapping model calls."""
import collections
import json
from pathlib import Path


RUN = Path('runs/test/20261003-1643_jevtree_gpt-oss-20b_browsecomp_jevtree_v65_10')


def merged(intervals):
    out = []
    for start, end in sorted(intervals, key=lambda interval: (interval[0], interval[1])):
        assert end >= start, (start, end)
        if out and start <= out[-1][1]:
            out[-1][1] = max(end, out[-1][1])
        else:
            out.append([start, end])
    return out


def duration(intervals):
    return sum(b-a for a, b in merged(intervals)) / 1000


def audit(qdir):
    intervals = collections.defaultdict(list)
    pending = collections.defaultdict(dict)
    searches = []
    reader_batches = []
    retrievals = collections.Counter()
    token_calls = collections.Counter()
    jev_reported_ms = 0
    finalizing = None
    total_ms = 0
    for line in (qdir/'trace.jsonl').open(encoding='utf-8'):
        e = json.loads(line)
        kind, t = e['event'], e['elapsed_ms']
        if kind == 'run.end':
            total_ms = t
        if kind == 'fetch.source':
            retrievals[e.get('retrieval', '')] += 1
        if kind == 'tool.call' and e['tool'] == 'web_search':
            searches.append({'start': t, 'turn': e['turn']})
        if kind == 'jevtree.selection':
            searches[-1]['selection'] = t
            reader_batches.append([t, None])
        if kind == 'jevtree.search_end':
            reader_batches[-1][1] = t
        if kind == 'tool.result' and e['tool'] == 'web_search':
            search = searches[-1]
            assert search['turn'] == e['turn']
            search['search_ms'] = e['duration_ms']
        if kind == 'llm.request':
            pending['main'][e['turn']] = t
        if kind == 'llm.response':
            intervals['main'].append((pending['main'].pop(e['turn']), t))
        if kind == 'run.finalizing':
            finalizing = t
        if kind == 'run.final_response':
            assert finalizing is not None
            intervals['main'].append((finalizing, t))
            finalizing = t
        if kind == 'jevtree.conditions_request':
            pending['conditions'][e['attempt']] = t
        if kind in ('jevtree.conditions_response', 'jevtree.conditions_error'):
            start = pending['conditions'].pop(e['attempt'], None)
            if start is not None:
                intervals['conditions'].append((start, t))
        if kind == 'jev.request':
            pending['jev'][e['request_id']] = t
        if kind == 'jev.result':
            intervals['jev'].append((pending['jev'].pop(e['request_id']), t))
            jev_reported_ms += e['duration_ms']
        if kind == 'jevtree.reader_request':
            pending['reader'][(e['url'], e['attempt'])] = t
        if kind == 'jevtree.read':
            intervals['reader'].append((pending['reader'].pop((e['url'], e['attempt'])), t))
            token_calls['reader_input'] += e.get('prompt_tokens', 0)
            token_calls['reader_output'] += e.get('completion_tokens', 0)
    assert not any(pending.values()), pending
    assert all(b is not None for a, b in reader_batches)
    for s in searches:
        intervals['search'].append((s['start'], s['start'] + s['search_ms']))
        intervals['traversal'].append((s['start'] + s['search_ms'], s['selection']))
    jev_union = merged(intervals['jev'])
    # Every JEV call is in the traversal envelope, alongside fetch and preprocessing.
    assert all(any(start >= a and end <= b for a, b in intervals['traversal'])
               for start, end in jev_union)
    seconds = {key: duration(intervals[key]) for key in ('main', 'conditions', 'jev', 'search')}
    seconds['reader'] = duration(reader_batches)
    seconds['fetch_and_preprocessing'] = duration(intervals['traversal']) - seconds['jev']
    seconds['other'] = total_ms / 1000 - sum(seconds.values())
    # Phase envelopes do not overlap; parallel work is merged within each phase.
    envelopes = intervals['main'] + intervals['conditions'] + intervals['search'] + intervals['traversal'] + reader_batches
    assert abs(duration(envelopes) - (total_ms/1000 - seconds['other'])) < .01
    return {'index': int(qdir.name[1:]), 'total_s': total_ms/1000,
            'phase_s': seconds, 'phase_pct': {k: 100*v/(total_ms/1000) for k,v in seconds.items()},
            'reader_calls': len(intervals['reader']), 'reader_call_sum_s': sum(b-a for a,b in intervals['reader'])/1000,
            'reader_call_union_s': duration(intervals['reader']),
            'reader_call_durations_s': [(b-a)/1000 for a,b in intervals['reader']],
            'jev_call_sum_s': jev_reported_ms/1000, 'retrievals': dict(retrievals),
            'tokens': dict(token_calls)}


if __name__ == '__main__':
    rows = [audit(q) for q in sorted(RUN.glob('q*')) if q.is_dir()]
    total = sum(r['total_s'] for r in rows)
    seconds = {k: sum(r['phase_s'][k] for r in rows) for k in rows[0]['phase_s']}
    summary = {'run': str(RUN), 'denominator': 'Sum of per-question agent wall times, not batch elapsed time',
               'total_question_seconds': total, 'phase_s': seconds,
               'phase_pct': {k:100*v/total for k,v in seconds.items()},
               'reader_call_sum_s': sum(r['reader_call_sum_s'] for r in rows),
               'jev_call_sum_s': sum(r['jev_call_sum_s'] for r in rows),
               'caveat': 'Fetch residual includes Jina/native retrieval, pacing/retries, tokenizer, filtering and trace overhead. No fetch start/HTTP/pacer timing exists in this historical trace.',
               'questions': rows}
    Path('analysis/jevtree_v65_latency.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k != 'questions'}, indent=2))
    for row in rows:
        print(row['index'], {k:round(v,1) for k,v in row['phase_pct'].items()}, row['retrievals'])
