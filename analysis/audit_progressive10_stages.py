"""Stream saved evidence and summarize timing without dumping documents."""
import collections
import json
from urllib.parse import urlsplit
from audit_progressive10 import RUN, OUT, events, read

TERMS={326:['manushkin','bird-watching','cat-watching'],516:['peter king','peter king nzioki','M. Sharath','fifth estate'],598:['RRS_10_2013_a1en','HDS','Elisabeta Jaba'],746:['Rockefeller','Hamlin'],1230:['Regal','209','Mumbai']}

def main():
    overall=collections.Counter(); stages={}; timings=[]; errors=[]; failures=collections.Counter()
    for record in events(RUN/'records.jsonl'):
        n=record['index']; folder=RUN/record['dir']; r=read(folder/'response.json'); m=read(OUT/f'q{n:05d}.json')
        final_start=0; final_s=0; search_s=0; requests={}; unavailable_s=0; invalid_s=0
        counts=collections.Counter(); hits=[]; seen=set(); fetches=[]
        for e in events(folder/'trace.jsonl'):
            name=e['event']; sec=e['elapsed_ms']/1000; counts[name]+=1
            if name=='run.final_request': final_start=sec
            elif name=='run.final_response': final_s+=sec-final_start
            elif name=='tool.result' and e.get('tool')=='web_search': search_s+=e['duration_ms']/1000
            elif name=='llm.request': requests[e['turn']]=sec
            elif name=='tool.unavailable': unavailable_s+=sec-requests.get(e.get('turn'),sec)
            elif name=='tool.invalid_arguments':
                # Validation events sometimes omit turn; use the latest request.
                invalid_s+=sec-max(requests.values(),default=sec)
                errors.append({'q':n,**{k:v for k,v in e.items() if k in ['event','error','tool','arguments','elapsed_ms']}})
            if name=='fetch.raw':
                fetches.append({'url':e['url'],'s':round(e['duration_ms']/1000,2),'error':e.get('is_error'),
                    'reason':e.get('content','')[:280] if e.get('is_error') else ''})
                if e.get('is_error'): failures[urlsplit(e['url']).netloc]+=1
            fragments=[]
            if name=='fetch.raw': fragments=[('fetch',e.get('url'),e.get('content',''))]
            elif name=='rawtree.return':
                fragments=[('returned',x.get('source'),'\n'.join(x.get('texts',{}).values())) for x in e.get('returned',[])]
                # The content also contains the source manifest (snippets are leads).
                fragments.append(('manifest_or_content',None,e.get('text','')))
            elif name=='llm.response': fragments=[('thought',None,e.get('reasoning','')+'\n'+e.get('text',''))]
            for kind,url,content in fragments:
                for term in TERMS.get(n,[]):
                    pos=content.casefold().find(term.casefold())
                    if pos<0: continue
                    counts[kind+':'+term]+=1
                    key=(kind,term,url)
                    if key in seen: continue
                    seen.add(key); hits.append({'kind':kind,'term':term,'minute':round(sec/60,2),'url':url,'excerpt':content[max(0,pos-100):pos+280]})
        sourcehits=[]
        for s in r['research_state']['sources']:
            value=json.dumps({k:s.get(k) for k in ['url','title','snippets']},ensure_ascii=False)
            found=[t for t in TERMS.get(n,[]) if t.casefold() in value.casefold()]
            if found: sourcehits.append({'id':s['id'],'url':s['url'],'status':s.get('status'),'terms':found,'snippets':s.get('snippets')})
        row={'q':n,'wall_s':r['latency_ms']/1000,'d3_s':m['active_s'].get('d3',0),'fetch_s':m['active_s'].get('fetch',0),
             'main_s':m['active_s'].get('main',0),'final_s':round(final_s,2),'search_s':round(search_s,2),
             'invalid_calls':counts['tool.invalid_arguments'],'invalid_response_s':round(invalid_s,2),
             'unavailable_calls':counts['tool.unavailable'],'unavailable_response_s':round(unavailable_s,2),
             'd3_phases':m['service'],'max_fetch_s':max((v['s'] for v in fetches),default=0),
             'llm_main_max_s':m['service'].get('main',{}).get('max_s')}
        timings.append(row); overall.update(counts)
        stages[str(n)]={'counts':{k:v for k,v in counts.items() if ':' in k},'hits':hits,'sourcehits':sourcehits,'fetches':fetches}
    (OUT/'stage_evidence.json').write_text(json.dumps(stages,ensure_ascii=False,indent=2),encoding='utf8')
    (OUT/'timings.json').write_text(json.dumps(timings,ensure_ascii=False,indent=2),encoding='utf8')
    (OUT/'errors.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({'totals':{k:round(sum(r[k] for r in timings),2) for k in ['wall_s','d3_s','fetch_s','main_s','final_s','search_s','invalid_response_s','unavailable_response_s']},
        'events':{k:v for k,v in overall.items() if ':' not in k},'failure_domains':failures,
        'rows':[{k:v for k,v in r.items() if k!='d3_phases'} for r in timings]},ensure_ascii=False))

if __name__=='__main__': main()
