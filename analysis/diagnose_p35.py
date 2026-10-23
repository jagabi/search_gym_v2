"""Read-only, physical-line JSONL diagnosis for the unified-score run."""
import json,statistics
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'runs/test/20261022-2010_jevtree_gpt-oss-20b_browsecomp_raw_browser_p35_unified_score_10'
OLD=ROOT/'runs/test/20261022-1829_jevtree_gpt-oss-20b_browsecomp_raw_browser_p34_chunk_return_10'
OUT=ROOT/'analysis/p35_diagnosis';OUT.mkdir(exist_ok=True)
def read(path):return [json.loads(l) for l in path.read_text(encoding='utf-8').split('\n') if l.strip()]
old={r['index']:r for r in read(OLD/'records.jsonl')}
summaries=[];allhttp=[];audit=Counter();budgets=[]
for r in read(RUN/'records.jsonl'):
    q=r['index'];folder=RUN/r['dir'];ev=read(folder/'trace.jsonl');response=json.loads((folder/'response.json').read_text(encoding='utf-8'))
    starts=[e for e in ev if e['event']=='rawtree.start'];queries={e['search_id']:e['query'] for e in starts};sidnumber={e['search_id']:i+1 for i,e in enumerate(starts)}
    depth=Counter();returns=[];hits=[];errors=[];requests={};results={}
    terms={326:['Fran Manushkin'],516:['Peter Nzioki','Peter King','Nzioki'],57:['career development award'],598:['Elisabeta','Jemna','Romanian Statistical Review'],746:['Japan'],1196:['Raja Ravi Varma','Thiruvananthapuram'],1230:['Regal Cinema','Colombo']}.get(q,[])
    for e in ev:
        if e['event']=='rawtree.inspection_selection':depth[e['depth']]+=len(e['selected'])
        if e['event']=='jev.request':requests[e['request_id']]=e
        if e['event']=='jev.result':results[e['request_id']]=e
        if e['event']=='jev.response':allhttp.append(e['duration_ms']/1000);audit[f'http_{e["status_code"]}']+=1
        if e['event']=='rawtree.return':
            stats=e['stats'];budgets.append((q,sidnumber[e['search_id']],stats.get('body_output_tokens'),stats.get('notice_output_tokens'),stats['raw_output_tokens'],stats.get('output_tokenizer')))
            returns.append({'search':sidnumber[e['search_id']],'query':queries[e['search_id']],'stats':stats,
                            'sources':[x['source'] for x in e['returned']],
                            'selected':[{k:v for k,v in x.items() if k in ('id','evidence_value','objective','bundle_id')} for x in e['selected']]})
            for term in terms:
                # Only returned source excerpts count, not navigation notices.
                for source in e['returned']:
                    text='\n'.join(source['texts'].values());pos=text.casefold().find(term.casefold())
                    if pos>=0:hits.append({'event':'returned_evidence','search':sidnumber[e['search_id']],'url':source['source'],'term':term,'excerpt':text[max(0,pos-120):pos+400]})
        if e['event'] in ('jev.error','rawtree.evaluation_failed','tool.invalid','tool.invalid_call'):errors.append(e)
        if e['event']=='fetch.raw' and not e.get('is_error'):
            for term in terms:
                text=e.get('content','');pos=text.casefold().find(term.casefold())
                if pos>=0:hits.append({'event':'fetched','url':e['url'],'term':term,'excerpt':text[max(0,pos-120):pos+400]})
    for e in requests.values():
        if e.get('context',{}).get('phase')=='bundle':
            keys=set(e['body']['questions']);audit['bundle_packets']+=1
            audit['bundle_legacy_key_packets']+=bool(keys&{'direct_answer','query_answer'})
            for term in terms:
                state=e['body']['state'];text=state.get('page_text','');pos=text.casefold().find(term.casefold())
                if pos>=0:hits.append({'event':'bundle_input','term':term,'context':e['context'],'title':state.get('page_title'),
                                      'scores':{k:v for k,v in results.get(e['request_id'],{}).get('scores',{}).items() if k=='evidence_value'},
                                      'excerpt':text[max(0,pos-100):pos+350]})
    row={'index':q,'old_score':old[q]['score'],'score':r['score'],'seconds':r['latency_s'],'old_seconds':old[q]['latency_s'],
         'searches':r['searches'],'depth':dict(depth),'empty_searches':sum(not x['sources'] for x in returns),
         'question':response['question'],'gold':response['gold_answer'],'answer':response['answer'],'queries':list(queries.values()),
         'returns':returns,'hits':hits,'errors':errors,
         'fetch_failures':sum(e['event']=='rawtree.fetch_failed' for e in ev),
         'output_budget_skips':sum(e['event']=='rawtree.output_budget' for e in ev)}
    summaries.append(row)
    (OUT/f'q{q}.json').write_text(json.dumps(row,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in row.items() if k in ('index','old_score','score','seconds','old_seconds','searches','depth','empty_searches','fetch_failures','output_budget_skips')},ensure_ascii=False))
(OUT/'summary.json').write_text(json.dumps(summaries,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'budget_audit.json').write_text(json.dumps(budgets,indent=2),encoding='utf-8')
print('TOTAL_SECONDS',sum(r['seconds'] for r in summaries))
print('AUDIT',dict(audit),'HTTP_MEAN',statistics.mean(allhttp),'MAX',max(allhttp))
print('BUDGET_EXCESS',[b for b in budgets if b[2]>14336 or b[3]>2048 or b[4]>16384 or b[5]!='main_model'])
