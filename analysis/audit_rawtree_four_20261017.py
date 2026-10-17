"""Streaming audit of the four completed v8 questions; no network/model calls."""
import collections
import json
from pathlib import Path
import statistics

RUN = Path('runs/test/20261017-1836_jevtree_gpt-oss-20b_browsecomp_raw_browser_p8_10')
OUT = Path('analysis/rawtree_four_20261017')
OUT.mkdir(exist_ok=True)


def coverage(spans, duration):
    points = [(0, '', 0), (duration, '', 0)]
    for kind, start, end in spans:
        start, end = max(0, start), min(duration, end)
        if end > start:
            points.extend([(start, kind, 1), (end, kind, -1)])
    active, result = collections.Counter(), collections.Counter()
    last = 0
    for t, kind, delta in sorted(points):
        key = '+'.join(sorted(k for k, count in active.items() if count > 0)) or 'other'
        result[key] += t-last
        active[kind] += delta
        last = t
    return dict(result)


def describe(values):
    return dict(n=len(values), sum=sum(values), mean=statistics.mean(values),
                median=statistics.median(values), max=max(values)) if values else {}


output = {}
for record in map(json.loads, (RUN/'records.jsonl').open(encoding='utf-8')):
    name = record['dir']
    response = json.loads((RUN/name/'response.json').read_text(encoding='utf-8'))
    duration = response['latency_ms']/1000
    requests, attempts, llms, searches, nodes, batches = {}, {}, {}, {}, {}, {}
    phases, spans, fetches, hits = collections.defaultdict(list), [], [], []
    seen_hits = set()
    needles = {40: ['26 august 1999', '26 aug 1999'],
               57: ['vanderbilt clinical oncology', 'pmc7227421'],
               117: ['october 22, 2019', '22 october 2019', 'in october 2019'],
               326: ['manushkin', 'baby, come out', 'bird watching', 'cat watching']}[record['index']]
    pending, active, peak_http, wave_violations = set(), set(), 0, []
    active_batch = None
    for line in (RUN/name/'trace.jsonl').open(encoding='utf-8'):
        e = json.loads(line)
        t, event = e['elapsed_ms']/1000, e['event']
        if event == 'jev.request':
            ctx = e['context']; body = e['body']; key = next(iter(body['questions']))
            phase = ('link' if key.startswith('link_') else 'page') if ctx['phase']=='preview' else ctx['phase']
            requests[e['request_id']] = dict(start=t, context=ctx, phase=phase, keys=e['question_count'])
            pending.add(e['request_id'])
            state_text = json.dumps(body['state'], ensure_ascii=False)
            lower = state_text.lower()
            for needle in needles:
                if needle in lower:
                    identity = (ctx['search_id'], ctx['node_id'], ctx['phase'], ctx.get('bundle_id'), ctx.get('chunk_id'), needle)
                    if identity not in seen_hits:
                        seen_hits.add(identity);pos=lower.index(needle)
                        hits.append(dict(event=event, t=t, context=ctx, needle=needle,
                                         url=body['state'].get('page_url'), excerpt=state_text[max(0,pos-250):pos+650]))
        elif event == 'jev.attempt':
            rid=e['request_id'];r=requests[rid];attempts[rid]=t
            spans.append(('queue',r['start'],t));active.add(rid);peak_http=max(peak_http,len(active))
            bid=e.get('batch_id')
            if bid != active_batch:
                if len(active)>1:wave_violations.append(dict(t=t,batch=bid))
                active_batch=bid
            batch=batches.setdefault(bid,dict(start=t,end=t,size=0,service_sum=0))
            batch['size']+=1
            r['batch_id']=bid
        elif event == 'jev.response':
            rid=e['request_id'];r=requests[rid];start=attempts[rid]
            spans.append((r['phase'],start,t))
            phases[r['phase']].append(dict(service=t-start,queue=start-r['start'],search_id=r['context']['search_id']))
            batch=batches[r['batch_id']];batch['end']=max(batch['end'],t);batch['service_sum']+=t-start
        elif event in ('jev.result','jev.error','jev.cancelled'):
            rid=e['request_id'];active.discard(rid);pending.discard(rid)
        elif event == 'fetch.raw':
            dt=e['duration_ms']/1000;spans.append(('fetch',t-dt,t))
            fetches.append(dict(url=e['url'],duration=dt,error=e['is_error']))
        elif event == 'llm.request':llms[e['turn']]=t
        elif event == 'llm.response' and e['turn'] in llms:spans.append(('main',llms[e['turn']],t))
        elif event == 'rawtree.start':
            searches[e['search_id']]=dict(query=e['query'],start=t,version=e['version'])
        elif event == 'rawtree.preview':
            nodes[(e['search_id'],e['node_id'])]=dict(url=e['url'],depth=e['depth'],scores=e['scores'])
        elif event == 'rawtree.pages_selected':searches[e['search_id']]['pages']=e['pages']
        elif event == 'rawtree.traversal_end':searches[e['search_id']]['traversal_s']=t-searches[e['search_id']]['start']
        elif event == 'rawtree.return':
            searches[e['search_id']].update(duration=e['duration_s'],stats=e['stats'],returned=e['returned'])
            text=e['text'];lower=text.lower()
            for needle in needles:
                if needle in lower:
                    pos=lower.index(needle);hits.append(dict(event=event,t=t,search_id=e['search_id'],needle=needle,excerpt=text[max(0,pos-250):pos+650]))
    parts=coverage(spans,duration)
    unions={kind:sum(v for k,v in parts.items() if kind in k.split('+')) for kind in ['link','page','bundle','chunk','queue','fetch','main']}
    unions['decision_any']=sum(v for k,v in parts.items() if any(x in k.split('+') for x in ['link','page','bundle','chunk']))
    unions['queue_only']=parts.get('queue',0)
    tree_rows=[]
    for step in response['steps']:
        for tool in step.get('tool_calls',[]):
            for tree in tool.get('explorations',[]):
                sid=tree.get('search_id');selected_sources={r['source'] for r in tree.get('returned_chunks',[])}
                def walk(node):
                    if node.get('depth',0):
                        node_urls = node.get('urls', [])
                        tree_rows.append(dict(search_id=sid,node_id=node.get('node_id'),url=node_urls[0] if node_urls else None,
                                              depth=node['depth'],link_score=node.get('link_score'),
                                              read=node.get('read'),contributed=any(u in selected_sources for u in node_urls)))
                    for child in node.get('opened',[]):walk(child)
                walk(tree)
    summary=dict(record=record,question=response['question'],gold=response['gold_answer'],answer=response['answer'],
                 duration_s=duration,phase_stats={k:dict(service=describe([x['service'] for x in v]),queue=describe([x['queue'] for x in v])) for k,v in phases.items()},
                 interval_partitions_s=parts,interval_unions_s=unions,searches=searches,fetches=fetches,
                 evidence_hits=hits,nodes=tree_rows,preview_nodes=[dict(search_id=k[0],node_id=k[1],**v) for k,v in nodes.items()],
                 peak_http=peak_http,wave_violations=wave_violations,batch_sizes=dict(collections.Counter(b['size'] for b in batches.values())),
                 batch_slot_utilization=sum(b['service_sum'] for b in batches.values())/sum(4*(b['end']-b['start']) for b in batches.values()))
    output[name]=summary
    (OUT/(name+'.json')).write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(name,'min',round(duration/60,2),'eval active min',round(unions['decision_any']/60,2),'queue only',round(unions['queue_only']/60,2),'violations',len(wave_violations),flush=True)
    for phase,values in summary['phase_stats'].items():print(phase,values['service'],flush=True)
    for i,(sid,s) in enumerate(searches.items(),1):print('search',i,round(s.get('duration',0)),s['query'],flush=True)
    print('hits',len(hits),flush=True)
(OUT/'summary.json').write_text(json.dumps({k:{a:b for a,b in v.items() if a not in ['nodes','preview_nodes','fetches','evidence_hits']} for k,v in output.items()},ensure_ascii=False,indent=2),encoding='utf-8')
