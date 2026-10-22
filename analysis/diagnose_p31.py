"""Read-only trace diagnosis of the completed PPLX/no-early-return ten questions."""
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'runs/test/20261022-1504_jevtree_gpt-oss-20b_browsecomp_raw_browser_p31_pplx_no_early_return_10'
records=[json.loads(s) for s in (RUN/'records.jsonl').read_text(encoding='utf-8').splitlines()]
out=ROOT/'analysis/p31_diagnosis';out.mkdir(exist_ok=True)
summaries=[]
for r in records:
    f=RUN/r['dir'];response=json.loads((f/'response.json').read_text(encoding='utf-8'))
    events=[json.loads(s) for s in (f/'trace.jsonl').read_text(encoding='utf-8').splitlines()]
    queries={e['search_id']:e['query'] for e in events if e['event']=='rawtree.start'}
    previews={(e['search_id'],e['node_id']):e for e in events if e['event']=='rawtree.preview'}
    requests={e['request_id']:e for e in events if e['event']=='jev.request'}
    results={e['request_id']:e for e in events if e['event']=='jev.result'}
    depth=Counter();ret=[];empty=0;goldhits=[];links=[]
    terms={516:['Peter King','Peter King Nzioki'],746:[],1196:[],1230:[],57:['career development award','PMC7227421','1685381']} .get(r['index'],[])
    terms += [response['gold_answer']]
    for e in events:
        if e['event']=='rawtree.inspection_selection':depth[e['depth']]+=len(e['selected'])
        if e['event']=='rawtree.return':
            empty+=not bool(e['returned'])
            ret.append({'query':queries[e['search_id']], 'sources':[x['source'] for x in e['returned']],
                'selected':[{k:v for k,v in x.items() if k in ('id','direct_answer','query_answer','objective')} for x in e['selected']],
                'stats':e['stats']})
        if e['event'] in ('fetch.raw','rawtree.return'):
            text=e.get('content','') if e['event']=='fetch.raw' else e.get('text','')
            for term in terms:
                pos=text.lower().find(term.lower())
                if pos>=0:goldhits.append({'event':e['event'],'url':e.get('url'),'search_id':e.get('search_id'),
                    'term':term,'excerpt':text[max(0,pos-130):pos+350]})
        if e['event']=='rawtree.frontier':
            selected=set(x['node_id'] if 'node_id' in x else x.get('id') for x in [])
            links.append(e)
    row={'index':r['index'],'score':r['score'],'seconds':r['latency_s'],'searches':r['searches'],
         'inspections_by_depth':dict(depth),'empty_searches':empty,'answer':response['answer'],
         'gold':response['gold_answer'],'question':response['question'],'queries':list(queries.values()),
         'returns':ret,'gold_hits':goldhits}
    summaries.append(row)
    lines=[json.dumps({k:v for k,v in row.items() if k not in ('returns','gold_hits')},ensure_ascii=False,indent=2)]
    for item in ret:lines.append('RETURN '+json.dumps({k:v for k,v in item.items() if k!='stats'},ensure_ascii=False))
    for hit in goldhits:lines.append('GOLD_HIT '+json.dumps(hit,ensure_ascii=False))
    if r['score']==0:
        for request in requests.values():
            state=request['body']['state'];text=state.get('page_text','') if isinstance(state,dict) else ''
            for term in terms:
                if term.lower() in text.lower():
                    lines.append('GOLD_D3 '+json.dumps({'context':request['context'],'title':state.get('page_title'),
                        'term':term,'scores':results.get(request['request_id'],{}).get('scores')},ensure_ascii=False))
        for e in events:
            if e['event']=='rawtree.fetch_failed':lines.append('FETCH_FAIL '+json.dumps({k:e.get(k) for k in ('url','error')},ensure_ascii=False))
            if e['event']=='rawtree.inspection_selection':lines.append('INSPECT '+json.dumps(e,ensure_ascii=False))
    (out/f"q{r['index']}.txt").write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({k:v for k,v in row.items() if k not in ('returns','gold_hits','answer','gold','question','queries')},ensure_ascii=False))
(out/'summary.json').write_text(json.dumps(summaries,ensure_ascii=False,indent=2),encoding='utf-8')
print('TOTAL',sum(r['latency_s'] for r in records),'FIRST7',sum(r['latency_s'] for r in records[:7]))
