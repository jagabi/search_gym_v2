exec((__import__('pathlib').Path(__file__).parent/'diagnose_p31.py').read_text(encoding='utf-8').split('summaries=[]')[0])
import statistics
def union(intervals):
    end=total=0
    for a,b in sorted(intervals):total+=max(0,b-max(end,a));end=max(end,b)
    return total/1000
alltimes=[];allqueues=[];statuses=Counter();rows=[]
for r in records:
    ev=[json.loads(s) for s in (RUN/r['dir']/'trace.jsonl').read_text(encoding='utf-8').splitlines()]
    attempts={e['request_id']:e for e in ev if e['event']=='jev.attempt'}
    intervals=[];phases={};starts={};fetches=[];main=[];llmstart=None
    for e in ev:
        if e['event']=='jev.response':
            alltimes.append(e['duration_ms']/1000);statuses[e['status_code']]+=1
            intervals.append((attempts[e['request_id']]['elapsed_ms'],e['elapsed_ms']))
        if e['event']=='jev.attempt':allqueues.append(e.get('queue_ms',0)/1000)
        if e['event']=='llm.request':llmstart=e['elapsed_ms']
        if e['event']=='llm.response' and llmstart is not None:
            main.append((llmstart,e['elapsed_ms']));llmstart=None
        if e['event']=='fetch.raw':
            # Only use an explicit fetch duration if logged in milliseconds.
            if 'duration_ms' in e:fetches.append((e['elapsed_ms']-e['duration_ms'],e['elapsed_ms']))
    row={'index':r['index'],'seconds':r['latency_s'],'pplx_active_wall_s':round(union(intervals),2),
         'main_model_wall_s':round(union(main),2),'fetch_active_wall_s':round(union(fetches),2)}
    rows.append(row);print(json.dumps(row))
print('PPLX_LATENCY',{'mean':statistics.mean(alltimes),'median':statistics.median(alltimes),
      'p95':sorted(alltimes)[int(.95*(len(alltimes)-1))],'max':max(alltimes),'statuses':dict(statuses),
      'queue_mean':statistics.mean(allqueues),'queue_max':max(allqueues)})
(out/'performance.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
