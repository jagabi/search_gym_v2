"""Read-only targeted comparison of five historical wins lost by p35."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CURRENT=ROOT/'runs/test/20261022-2100_jevtree_gpt-oss-20b_browsecomp_raw_browser_p35_unified_score_50'
DIRECTED=ROOT/'runs/test/20260924-0737_depthsearch_gpt-oss-20b_browsecomp_ds_directed_v8'
RAGENT=ROOT/'runs/test/20260920-2130_ragent_gpt-oss-20b_browsecomp_paper_frozen_v1'
OUT=ROOT/'analysis/p35_lost_five';OUT.mkdir(exist_ok=True)
def read(path):return [json.loads(l) for l in path.read_text(encoding='utf-8').split('\n') if l.strip()]
def queries(response):
    out=[]
    for step in response['steps']:
        for call in step.get('tool_calls',[]):
            args=call.get('arguments',{})
            if isinstance(args,str):
                try:args=json.loads(args)
                except ValueError:continue
            if call.get('name') in ('web_search','search'):out.append(args.get('query',args))
    return out
for q in (8,26,74,128,157):
    oldrun=RAGENT if q==128 else DIRECTED
    nr=next(r for r in read(CURRENT/'records.jsonl') if r['index']==q)
    pr=next(r for r in read(oldrun/'records.jsonl') if r['index']==q)
    new=json.loads((CURRENT/nr['dir']/'response.json').read_text(encoding='utf-8'))
    old=json.loads((oldrun/pr['dir']/'response.json').read_text(encoding='utf-8'))
    ev=read(CURRENT/nr['dir']/'trace.jsonl')
    oldtrace=oldrun/pr['dir']/'trace.jsonl';oe=read(oldtrace) if oldtrace.exists() else []
    starts=[e for e in ev if e['event']=='rawtree.start'];num={e['search_id']:i+1 for i,e in enumerate(starts)}
    returns=[];depth=Counter()
    for e in ev:
        if e['event']=='rawtree.inspection_selection':depth[e['depth']]+=len(e['selected'])
        if e['event']=='rawtree.return':
            returns.append({'search':num[e['search_id']],'query':next(s['query'] for s in starts if s['search_id']==e['search_id']),
                'sources':[r['source'] for r in e['returned']],
                'bundles':[{k:v for k,v in b.items() if k in ('id','evidence_value','bundle_id')} for b in e['selected']],
                'stats':e['stats']})
            (OUT/f'q{q}_s{num[e["search_id"]]}_return.txt').write_text(e['text'],encoding='utf-8')
    row={'index':q,'question':new['question'],'gold':new['gold_answer'],'p35_answer':new['answer'],
         'old_answer':old['answer'],'old_run':str(oldrun),'old_queries':queries(old),'p35_queries':[s['query'] for s in starts],
         'p35_depth':dict(depth),'p35_record':nr,'old_record':pr,'returns':returns,
         'old_event_kinds':dict(Counter(e['event'] for e in oe))}
    (OUT/f'q{q}.json').write_text(json.dumps(row,ensure_ascii=False,indent=2),encoding='utf-8')
    print('\nQUESTION',q,new['question']);print('GOLD',new['gold_answer']);print('P35_ANSWER',new['answer'][:1100]);print('OLD_ANSWER',old['answer'][:1100]);print('P35_QUERIES',row['p35_queries']);print('OLD_QUERIES',row['old_queries']);print('DEPTH',row['p35_depth']);print('OLD_EVENTS',row['old_event_kinds'])
