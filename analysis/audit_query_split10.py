"""Read-only audit of the completed 2026-10-12 diagnostic run."""
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
import statistics

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

RUN = Path('runs/test/20261012-2235_jevtree_gpt-oss-20b_browsecomp_lds_query_split10')


def rows(path):
    with path.open(encoding='utf-8') as f:
        for line in f:
            yield json.loads(line)


def union(intervals):
    total = 0
    end = float('-inf')
    for a, b in sorted(intervals):
        if b > end:
            total += b - max(a, end)
            end = b
    return total


def stats(xs):
    return dict(n=len(xs), mean=round(statistics.mean(xs), 2), median=round(statistics.median(xs), 2),
                p95=round(sorted(xs)[min(len(xs)-1, int(len(xs)*.95))], 2)) if xs else {}


result = {'run': str(RUN), 'questions': [], 'comparisons': {}}
records = list(rows(RUN/'records.jsonl'))
ids = {r['index'] for r in records}
for label, folder in [('current', RUN.name), ('previous_jev', '20261004-1329_jevtree_gpt-oss-20b_browsecomp_jevtree_v66_diagnostic10'),
                      ('search_o1', '20260919-1621_search-o1_gpt-oss-20b_browsecomp_paper_frozen_v1')]:
    rs = [r for r in rows(RUN.parent/folder/'records.jsonl') if r['index'] in ids]
    result['comparisons'][label] = dict(n=len(rs), correct=sum(r['score'] for r in rs),
        **{k: sum(r[k] for r in rs) for k in ('fetch_attempts','fetch_failures','searches','input_tokens','llm_calls')},
        latency_seconds=stats([r['latency_s'] for r in rs]),
        jev_input_tokens=sum(r.get('reader_stats',{}).get('jev_input_tokens',0) for r in rs),
        reader_calls=sum(r['explorer_calls'] for r in rs))
for row in sorted(records, key=lambda r:r['index']):
    qdir = RUN/row['dir']
    q = dict(index=row['index'], score=row['score'], searches=[], depth_fetched=Counter(), depth_read=Counter())
    all_actions=[]
    for path in qdir.glob('lds/*/structure.json'):
        s=json.loads(path.read_text(encoding='utf-8')); ns=s['nodes']; acts=s['actions']; all_actions.extend(acts)
        fetched=[n for n in ns if n.get('fetch_order')]; read=[n for n in ns if n['read']]
        q['depth_fetched'].update(n['depth'] for n in fetched);q['depth_read'].update(n['depth'] for n in read)
        eligible=[n for n in ns if not n['read'] and (n.get('query_answer') or 0)>=.15 and not n.get('error')]
        q['searches'].append(dict(query=s['query'], stats=s['stats'], start=acts[0]['timestamp'],
            quota_blocked_query_pages=min(len(eligible),2-s['stats'].get('direct_reads',0)),
            best_direct=max((n.get('direct_answer') or 0 for n in ns),default=0),
            best_query=max((n.get('query_answer') or 0 for n in ns),default=0),
            best_unread=[{k:n.get(k) for k in ('id','url','depth','direct_answer','query_answer','read','reader_objective')}
                         for n in sorted((n for n in fetched if not n['read']),key=lambda n:max(n.get('direct_answer') or 0,n.get('query_answer') or 0),reverse=True)[:3]],
            structure=str(path)))
    q['searches'].sort(key=lambda s:s['start'])
    q['fetch_service_seconds']=stats([n['fetch_duration_ms']/1000 for a in all_actions if a['kind']=='fetch_end' for n in a['updates']])
    starts={};stages={'fetch':[],'jev':[]}
    for a in sorted(all_actions,key=lambda a:a['timestamp']):
        stage='fetch' if a['kind'].startswith('fetch_') else 'jev' if a['kind'].startswith('jev_') else None
        if stage and a['kind'] in (stage+'_start',stage+'_end',stage+'_failed'):
            for n in a['updates']:
                key=(stage,n['url']);t=datetime.fromisoformat(a['timestamp']).timestamp()
                if a['kind'].endswith('_start'):starts[key]=t
                elif key in starts:stages[stage].append((starts.pop(key),t))
    q['fetch_active_wall_s']=round(union(stages['fetch']),2);q['jev_page_active_wall_s']=round(union(stages['jev']),2)
    q['latency_s']=row['latency_s'];q['fetch_active_fraction']=round(q['fetch_active_wall_s']/q['latency_s'],3)
    result['questions'].append(q)
result['total_depth_fetched']=dict(sum((q['depth_fetched'] for q in result['questions']),Counter()))
result['total_depth_read']=dict(sum((q['depth_read'] for q in result['questions']),Counter()))
ss=[s for q in result['questions'] for s in q['searches']]
result['searches_with_fetch_no_reader']=[dict(index=q['index'],query=s['query'],fetched=s['stats']['fetched'],best_direct=s['best_direct'],best_query=s['best_query'])
    for q in result['questions'] for s in q['searches'] if s['stats']['fetched'] and not s['stats']['reads']]
result['quota_blocked_query_slots']=sum(s['quota_blocked_query_pages'] for s in ss)
result['full_budget_searches']=sum(s['stats']['fetched']==40 for s in ss)
out=Path('analysis/lds_query_split10_audit_20261013.json');out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='questions'},ensure_ascii=False))
for q in result['questions']:print(json.dumps({k:v for k,v in q.items() if k!='searches'},ensure_ascii=False))
