"""Offline timing and query-transition audit of the matched 300-question runs."""
import json
import re
import statistics as st
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "analysis/comparison_300_audit.json"
STOP = set("the a an of in on for to and or by with from what which who how is are was were at as according me tell please all between had have has its that this their it".split())


def words(s):
    return set(re.findall(r"[a-z0-9]+", s.lower())) - STOP


def sim(a, b):
    x, y = words(a), words(b)
    return len(x & y) / len(x | y) if x | y else 0


def normurl(s):
    try:
        u = urlsplit(s)
        return urlunsplit((u.scheme, u.netloc.lower(), u.path.rstrip('/'), u.query, ''))
    except ValueError:
        return s


def group_summary(rows):
    if not rows:
        return {"n": 0}
    d = {"n": len(rows), "ids": [r['id'] for r in rows]}
    for m in ('ragent', 'search-o1', 'depthsearch'):
        d[m] = st.mean(r['scores'][m] for r in rows)
    d.update(zero=sum(r['scores']['depthsearch'] == 0 for r in rows),
             full=sum(r['scores']['depthsearch'] == 1 for r in rows),
             delta_o1=d['depthsearch'] - d['search-o1'],
             delta_ragent=d['depthsearch'] - d['ragent'],
             single=sum(r['answer_type'] == 'single' for r in rows),
             categories=dict(Counter(r['category'] for r in rows)))
    for key in ('searches', 'fetch_attempts', 'expansion_nodes'):
        d[key] = st.mean(r[key] for r in rows)
    return d


def main():
    a = json.loads(AUDIT.read_text(encoding='utf-8'))
    rows = []
    for q in a['questions']:
        p = ROOT / 'runs/test' / a['runs']['depthsearch'] / q['behavior']['depthsearch']['dir']
        response = json.loads((p/'response.json').read_text(encoding='utf-8'))
        calls = []
        searches = 0
        for s in response['steps']:
            for c in s.get('tool_calls', []):
                if c.get('refused'):
                    continue
                calls.append({'order': len(calls), 'turn': s['turn'], 'searches_before': searches,
                              'name': c['name'], 'arguments': c['arguments'],
                              'is_error': c.get('is_error', False),
                              'readers': len(c.get('explorations', [])),
                              'nodes': sum(e.get('nodes', 0) for e in c.get('explorations', []))})
                if c['name'] == 'web_search':
                    searches += 1
        r = {k: q[k] for k in ('id', 'category', 'question', 'gold', 'answer_type', 'answer_count', 'scores')}
        r.update({k: q['behavior']['depthsearch'][k] for k in ('searches', 'fetch_attempts', 'expansion_nodes')})
        r['calls'] = calls
        r['first'] = {}
        for kind, condition in [
            ('fetch', lambda c: c['name'] == 'web_fetch'),
            ('reader', lambda c: c['name'] == 'web_fetch' and c['readers'] > 0),
            ('recursive', lambda c: c['name'] == 'web_fetch' and c['nodes'] > 0),
        ]:
            c = next((c for c in calls if condition(c)), None)
            r['first'][kind] = c
            if c is None:
                continue
            before = [v for v in calls[:c['order']] if v['name'] == 'web_search']
            after = [v for v in calls[c['order']+1:] if v['name'] == 'web_search']
            qs_before = [v['arguments'].get('query', '') for v in before]
            qs_after = [v['arguments'].get('query', '') for v in after]
            # Query overlap is only an observable repetition proxy, not a semantic diagnosis.
            pre_pairs = [sim(x, y) for x, y in zip(qs_before, qs_before[1:])]
            post_pairs = [sim(x, y) for x, y in zip(qs_after, qs_after[1:])]
            r[kind+'_transition'] = {
                'before_queries': qs_before, 'after_queries': qs_after,
                'boundary_overlap': sim(qs_before[-1], qs_after[0]) if qs_before and qs_after else None,
                'before_adjacent': pre_pairs, 'after_adjacent': post_pairs,
                'after_near_repeat': sum(v >= .7 for v in post_pairs),
                'after_exact_repeat': len(qs_after) - len(set(' '.join(x.lower().split()) for x in qs_after)),
            }
        rows.append(r)
    groups = {}
    for kind in ('fetch', 'reader', 'recursive'):
        groups[kind] = {}
        bins = [('0',0,0), ('1',1,1), ('2',2,2), ('3',3,3), ('4-5',4,5), ('6-10',6,10)]
        for name, lo, hi in bins:
            selected = [r for r in rows if r['first'][kind] is not None and lo <= r['first'][kind]['searches_before'] <= hi]
            groups[kind][name] = group_summary(selected)
        groups[kind]['never'] = group_summary([r for r in rows if r['first'][kind] is None])
        for name, lo, hi in [('early0-1',0,1), ('middle2-3',2,3), ('late4-10',4,10)]:
            selected = [r for r in rows if r['first'][kind] is not None and lo <= r['first'][kind]['searches_before'] <= hi]
            groups[kind][name] = group_summary(selected)
            for typ in ('single', 'set'):
                groups[kind][name+'_'+typ] = group_summary([r for r in selected if r['answer_type'] == typ])
    output = {'definitions': {
        'fetch': 'First non-refused main web_fetch, including failed attempts.',
        'reader': 'First main web_fetch producing a fresh Explorer session.',
        'recursive': 'First main web_fetch returning at least one successfully expanded child node.',
        'searches_before': 'Executed (non-refused) main web_search calls before that fetch, including failed searches.',
        'warning': 'Observational timing, not randomized intervention; query overlap does not establish fixation.'},
        'runs': a['runs'], 'groups': groups, 'questions': rows}
    target = ROOT/'analysis/fetch_timing_300_audit.json'
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    for kind, gs in groups.items():
        print('\n',kind)
        for name in ('0','1','2','3','4-5','6-10','never','early0-1_single','late4-10_single','early0-1_set','late4-10_set'):
            v = gs[name]
            print(name, {k: round(x,4) if isinstance(x,float) else x for k,x in v.items() if k not in ('ids','categories')})


if __name__ == '__main__':
    main()
