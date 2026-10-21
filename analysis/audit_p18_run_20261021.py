"""Read saved p17/p18 traces only; no project imports or network/model calls."""
import collections
import json
from pathlib import Path
import statistics

ROOT=Path(__file__).resolve().parents[1]
RUNS={
 'p17':ROOT/'runs/test/20261021-1012_jevtree_gpt-oss-20b_browsecomp_raw_browser_p17_readpool10',
 'p18':ROOT/'runs/test/20261021-1340_jevtree_gpt-oss-20b_browsecomp_raw_browser_p18_pilot',
}
def distribution(values):
    values=sorted(values)
    return dict(n=len(values),mean=statistics.mean(values),median=statistics.median(values),
                p95=values[int((len(values)-1)*.95)],max=max(values)) if values else {}

output={}
for label,folder in RUNS.items():
    result=[]
    for rec in map(json.loads,(folder/'records.jsonl').read_text(encoding='utf-8').splitlines()):
        qfolder=folder/rec['dir']
        response=json.loads((qfolder/'response.json').read_text(encoding='utf-8'))
        item={k:rec.get(k) for k in ('index','score','searches','latency_s','stop_reason','answer_chars','reader_stats','cached')}
        item.update(question=response['question'],gold=response['gold_answer'],answer=response['answer'])
        depths=collections.defaultdict(collections.Counter)
        searches={}; requests={}; durations=[]; queues=[]; failures=[]; finals=[]; queries=[]
        actions=collections.Counter(); stops=collections.Counter(); phases=collections.Counter()
        fetch_times=[]; seen=collections.Counter(); hits=collections.defaultdict(list)
        terms=['manushkin','baby, come out','peter king','nzioki','rockefeller','tampa','padmanabha','prolactin','goodall','174']
        for line in (qfolder/'trace.jsonl').open(encoding='utf-8'):
            r=json.loads(line); event=r['event']; seen[event]+=1
            sid=r.get('search_id'); nid=r.get('node_id')
            if event=='rawtree.start': searches[sid]={'query':r['query'],'version':r.get('version'),'depths':{},'actions':[]}
            elif event=='rawtree.preview':
                depth=r['depth']; depths[depth]['previews']+=1
                searches[sid]['depths'][nid]=depth
            elif event=='rawtree.fetch_failed': failures.append({k:r.get(k) for k in ('search_id','url','reader_metadata','error')})
            elif event=='jev.request':
                requests[r['request_id']]=r.get('context',{})
                phases[r.get('context',{}).get('phase')]+=r.get('question_count',len(r['body']['questions']))
            elif event=='jev.response': durations.append(r['duration_ms'])
            elif event=='jev.attempt': queues.append(r['queue_ms'])
            elif event=='rawtree.node_action':
                actions[r['action']]+=1
                searches[sid]['actions'].append({k:r.get(k) for k in ('node_id','depth','action','reason','terminal','scores')})
            elif event=='rawtree.read_deferred': searches[sid].setdefault('read_deferred',[]).append(r)
            elif event=='rawtree.chunks':
                depth=searches[sid]['depths'].get(nid)
                depths[depth]['reads']+=1
                body='\n'.join(c['text'] for c in r['chunks']).lower()
                for term in terms:
                    if term in body: hits[term].append(dict(stage='chunked_body',search_id=sid,url=r['url']))
            elif event=='rawtree.traversal_end': stops[r['reason']]+=1
            elif event=='rawtree.return':
                searches[sid].update(stats=r['stats'],seconds=r['duration_s'],returned=[dict(url=x['source'],texts=x['texts']) for x in r['returned']])
                for x in r['returned']:
                    body='\n'.join(x['texts'].values()).lower()
                    for term in terms:
                        if term in body: hits[term].append(dict(stage='returned',search_id=sid,url=x['source']))
            elif event in ('run.final_response','run.finalizing'):
                finals.append({k:r.get(k) for k in ('event','elapsed_ms','text','raw_text','finish_reason','attempt','reason')})
            elif event=='fetch.raw':
                fetch_times.append({k:r.get(k) for k in ('url','duration_ms','reader_metadata')})
            if event in ('tool.call','tool.result','rawtree.preview'):
                if event=='tool.call': queries.append(r)
                lower=json.dumps(r,ensure_ascii=False).lower()
                for term in terms:
                    if term in lower: hits[term].append(dict(stage=event,search_id=sid,url=r.get('url')))
        tree=json.loads((qfolder/'explorer.json').read_text(encoding='utf-8'))
        def walk(node):
            if isinstance(node,list):
                for n in node:walk(n)
            elif isinstance(node,dict):
                if node.get('node_id') and node.get('depth',0)>0: depths[node['depth']]['visits']+=1
                for n in node.get('opened',[]):walk(n)
        walk(tree)
        # Actual traversal node logs may omit node_id; count depth from tree separately below if needed.
        item.update(depths=dict(depths),search_runs=searches,actions=dict(actions),stops=dict(stops),
                    d3_http_ms=distribution(durations),d3_queue_ms=distribution(queues),
                    phases=dict(phases),fetch_failures=failures,finals=finals,queries=queries,
                    hits=dict(hits),event_counts=dict(seen))
        result.append(item)
    output[label]=result
(ROOT/'analysis/p18_run_audit_20261021.json').write_text(json.dumps(output,indent=2,ensure_ascii=False),encoding='utf-8')
for label,items in output.items():
    print(label,'seconds',round(sum(r['latency_s'] for r in items),1),'searches',sum(r['searches'] for r in items))
    for r in items:
        print(json.dumps(dict(id=r['index'],score=r['score'],seconds=r['latency_s'],depths=r['depths'],
            http=r['d3_http_ms'],search_seconds=round(sum(s.get('seconds',0) for s in r['search_runs'].values()),1),
            stops=r['stops'],actions=r['actions']),ensure_ascii=True))
