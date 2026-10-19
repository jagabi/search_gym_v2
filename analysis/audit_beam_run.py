"""Bounded trace audit for the p11 automatic beam run, entirely offline."""
import collections
import json
from pathlib import Path
from urllib.parse import urlsplit
from inspect_run import events, read

RUN=Path('runs/test/20261019-1506_jevtree_gpt-oss-20b_browsecomp_raw_browser_p11_beam10')
OUT=Path('analysis/audit_20261019-1506')
TERMS={57:['PMC7227421','Vanderbilt','career development','31652074'],326:['Manushkin'],
       516:['Peter King','Nzioki','Fifth Estate'],598:['RRS_10_2013_a1en','Elisabeta Jaba','HDS'],
       746:['Rockefeller','Hamlin'],1230:['Regal Cinema','Colombo','209']}

def main():
    OUT.mkdir(exist_ok=True); summary=[]
    for record in events(RUN/'records.jsonl'):
        q=record['index']; folder=RUN/record['dir']; response=read(folder/'response.json')
        nodes={}; searches={}; req={}; fetches=[]; matches=[]; seen=set(); refused=[]; allcounts=collections.Counter()
        phases=collections.defaultdict(list); starts={}; final=[]; returns=[]
        def node(sid,nid):
            return nodes.setdefault((sid,nid),{'search_id':sid,'node_id':nid,'phase_requests':collections.Counter(),'phase_service_s':collections.Counter()})
        for e in events(folder/'trace.jsonl'):
            name=e['event']; t=e['elapsed_ms']/1000; allcounts[name]+=1
            if name=='rawtree.start': searches[e['search_id']]={'search_id':e['search_id'],'query':e['query'],'start_s':t}
            elif name=='jev.request':
                c=e['context']; key=next(iter(e['body']['questions']),''); phase=c['phase']
                if phase=='preview': phase='link' if key.startswith('link_') else 'page'
                req[e['request_id']]={'phase':phase,'ctx':c}
                n=node(c['search_id'],c['node_id']); n['phase_requests'][phase]+=1
                if 'link_count' in c: n['link_count']=c['link_count']
            elif name=='jev.attempt': req[e['request_id']]['start']=t
            elif name=='jev.response':
                r=req[e['request_id']]; seconds=t-r['start']; c=r['ctx']
                node(c['search_id'],c['node_id'])['phase_service_s'][r['phase']]+=seconds
            elif name in ['jev.result','jev.cancelled']: req.pop(e['request_id'],None)
            elif name=='rawtree.preview':
                node(e['search_id'],e['node_id']).update({k:e[k] for k in ['url','depth','scores','full_chars','prefix_tokens'] if k in e})
            elif name=='rawtree.chunk_timing': node(e['search_id'],e['node_id']).update({k:e[k] for k in ['source_chars','chunk_count','bundle_count','chunking_ms']})
            elif name=='rawtree.bundles':
                n=node(e['search_id'],e['node_id']); n['selected_bundles']=len(e['selected_bundle_ids']); n['candidate_chunks']=len(e['candidate_chunk_ids'])
            elif name=='rawtree.pages_selected':
                for p in e['pages']: node(e['search_id'],p['id']).update(read=True,objective=p.get('objective'))
            elif name=='rawtree.return':
                searches[e['search_id']].update(seconds=e['duration_s'],stats=e['stats'])
                returns.append({'search_id':e['search_id'],'minute':round(t/60,2),'source_count':len(e['returned']),
                    'sources':[{'url':r['source'],'chunks':r['chunk_ids']} for r in e['returned']]})
            elif name=='fetch.raw':
                fetches.append({'url':e['url'],'is_error':e['is_error'],'seconds':round(e['duration_ms']/1000,2),
                    'reason':e.get('content','')[:260] if e['is_error'] else ''})
            elif name in ['tool.unavailable','tool.refused','tool.invalid_arguments','run.truncated','run.finalizing','run.final_response']:
                refused.append({k:v for k,v in e.items() if k not in ['raw_text','reasoning','text','messages','body']})
            pieces=[]
            if name=='fetch.raw': pieces=[('fetch',e['url'],e.get('content',''))]
            elif name=='rawtree.return': pieces=[('returned',r['source'],'\n'.join(r.get('texts',{}).values())) for r in e['returned']]
            for kind,url,text in pieces:
                for term in TERMS.get(q,[]):
                    pos=text.casefold().find(term.casefold())
                    if pos<0: continue
                    allcounts[kind+':'+term]+=1; key=(kind,url,term)
                    if key in seen: continue
                    seen.add(key); matches.append({'kind':kind,'url':url,'term':term,'minute':round(t/60,2),
                        'excerpt':text[max(0,pos-120):pos+400]})
        data={'id':q,'question':response['question'],'answer':response['answer'],'score':record['score'],
            'minutes':round(record['latency_s']/60,2),'queries':[{'turn':s['turn'],'arguments':c['arguments']}
                for s in response['steps'] for c in s.get('tool_calls',[]) if c['name']=='web_search'],
            'nodes':list(nodes.values()),'searches':list(searches.values()),'fetches':fetches,
            'matches':matches,'counts':dict(allcounts),'control_events':refused,'returns':returns}
        (OUT/f'q{q:05d}_audit.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
        summary.append({'id':q,'minutes':data['minutes'],'score':record['score'],
            'depths':dict(collections.Counter(n.get('depth') for n in nodes.values() if 'depth' in n)),
            'read_depths':dict(collections.Counter(n.get('depth') for n in nodes.values() if n.get('read'))),
            'fetch_errors':sum(f['is_error'] for f in fetches),
            'largest_bundle_pages':sorted([{'url':n.get('url'),'bundles':n['bundle_count'],'chunks':n['chunk_count'],
                'chosen_bundles':n.get('selected_bundles'),'candidate_chunks':n.get('candidate_chunks'),
                'bundle_service_s':round(n['phase_service_s']['bundle'],1)} for n in nodes.values() if 'bundle_count' in n],key=lambda n:-n['bundles'])[:3]})
    (OUT/'beam_audit_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__': main()
