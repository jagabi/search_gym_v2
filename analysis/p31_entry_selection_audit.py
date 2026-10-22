"""Audit saved 10-to-6 entry selection, diversity changes and lead truncation."""
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'runs/test/20261022-1504_jevtree_gpt-oss-20b_browsecomp_raw_browser_p31_pplx_no_early_return_10'
records=[json.loads(s) for s in (RUN/'records.jsonl').read_text(encoding='utf-8').splitlines()]
out=ROOT/'analysis/p31_diagnosis';allrows=[];counts=Counter();cuts=[]
def quota(rows,a,b):
    chosen=[];seen=set()
    for objective,budget in (('direct_answer',a),('query_answer',b)):
        for row in sorted(rows,key=lambda r:(-r[objective],str(r['id']))):
            if budget<=0:break
            if row['id'] in seen:continue
            chosen.append(row['id']);seen.add(row['id']);budget-=1
    return chosen
for record in records:
    f=RUN/record['dir'];events=[json.loads(s) for s in (f/'trace.jsonl').read_text(encoding='utf-8').splitlines()]
    response=json.loads((f/'response.json').read_text(encoding='utf-8'))
    queries={e['search_id']:e['query'] for e in events if e['event']=='rawtree.start'}
    diversity={e['search_id']:e for e in events if e['event']=='rawtree.entry_diversity'}
    originals={}
    for step in response['steps']:
        for call in step.get('tool_calls',[]):
            result=call.get('result','')
            if isinstance(result,dict):result=result.get('text',json.dumps(result,ensure_ascii=False))
            if not isinstance(result,str):continue
            marker='Unverified search results for further navigation:\n'
            if marker not in result:continue
            try:search,_=json.JSONDecoder().raw_decode(result.split(marker,1)[1])
            except (ValueError,TypeError):continue
            query=call.get('arguments',{}).get('query','')
            originals[query]={row.get('link'):row for row in search.get('organic',[])}
    for e in events:
        if e['event']!='rawtree.entries':continue
        sid=e['search_id'];query=queries[sid];d=diversity.get(sid,{})
        candidates=e['candidates'];chosen=set(e['selected']);seeds=set(d.get('seed',[]))
        gains={r['id']:r['score'] for r in d.get('candidates',[])}
        baseline=quota(candidates,3,3);actual=[r['id'] for r in candidates if r['lead']['url'] in chosen]
        for c in candidates:
            lead=c['lead'];orig=originals.get(query,{}).get(lead['url'],{})
            counts['matched_original_leads']+=bool(orig)
            for field in ('title','snippet'):
                if field in orig and orig[field]!=lead[field]:
                    cuts.append({'q':record['index'],'query':query,'url':lead['url'],'field':field,
                                 'original':orig[field],'sent':lead[field]})
        rows=[{**c['lead'],'id':c['id'],'direct':c['direct_answer'],'query':c['query_answer'],
               'gain':gains.get(c['id']),'selected':c['lead']['url'] in chosen,'seed':c['id'] in seeds,
               'baseline_selected':c['id'] in baseline} for c in candidates]
        row={'q':record['index'],'correct':record['score'],'search_id':sid,'query':query,'candidates':rows,
             'selected_count':len(chosen),'diversity_changed':set(actual)!=set(baseline),
             'added':[r for r in rows if r['selected'] and not r['baseline_selected']],
             'removed':[r for r in rows if not r['selected'] and r['baseline_selected']]}
        allrows.append(row);counts['searches']+=1;counts['candidates']+=len(rows);counts['selected']+=len(chosen)
        counts['diversity_rounds']+=bool(d);counts['diversity_changed']+=row['diversity_changed']
        if not record['score']:
            print('SEARCH',record['index'],query)
            for r in rows:
                print(json.dumps({k:r[k] for k in ('id','url','title','snippet','direct','query','gain','selected','seed','baseline_selected')},ensure_ascii=False))
    counts['searches_with_original_results']+=len(originals)
(out/'entry_selection.json').write_text(json.dumps(allrows,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'entry_truncations.json').write_text(json.dumps(cuts,ensure_ascii=False,indent=2),encoding='utf-8')
print('COUNTS',dict(counts),'TRUNCATIONS',len(cuts),Counter(c['field'] for c in cuts))
