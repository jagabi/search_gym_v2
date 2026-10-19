from audit_progressive10 import RUN, OUT, events, read
import collections
import json

empty=[]; stopped=[]; contam=[]; final=[]; failed_reads=[]; search_returns=[]
for record in events(RUN/'records.jsonl'):
    n=record['index']; parent=RUN/record['dir']
    for e in events(parent/'trace.jsonl'):
        name=e['event']
        if name=='contamination.filtered': contam.append({'q':n,**e})
        elif name=='run.truncated': stopped.append({'q':n,'reason':e.get('reason'),'turns':e.get('turns')})
        elif name=='run.final_request' and n==516:
            final.append({t:sum(t.casefold() in str(m.get('content','')).casefold() for m in e['messages'])
                for t in ['M. Sharath','Peter King','Fifth Estate','Jeethu Joseph']})
        elif name=='rawtree.return':
            if not e['returned']:
                empty.append({'q':n,'action':e['action'],'min':round(e['elapsed_ms']/60000,2),
                    'stats':{k:e['stats'].get(k) for k in ['page_visits','fetch_failed','jev_requests']}})
            if n==326 and 'manushkin' in e['text'].lower():
                manifest=json.loads(e['text'].split('Research session (navigation metadata, not evidence):')[-1])
                search_returns.append({'q':n,'min':round(e['elapsed_ms']/60000,2),'sources':
                    [{k:s.get(k) for k in ['source_id','title','fetched','failed']} for s in manifest['sources']]})
result={'empty':empty,'max_turns':stopped,'contamination':contam,'final516_terms':final,'q326_manifest':search_returns}
(OUT/'extra.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False))
