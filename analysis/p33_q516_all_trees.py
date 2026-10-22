"""Offline trace tables and real output-selection replay; no API requests."""
import asyncio,csv,json,sys
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from searchgym.rawtree import RawTree,quota_select
from searchgym.trace import NullTrace
from tokenizers import Tokenizer

RUN=ROOT/'runs/test/20261022-1705_jevtree_gpt-oss-20b_browsecomp_raw_browser_p33_fetch_all10_10/q00516'
OUT=ROOT/'analysis/p33_diagnosis/q516_all_trees';OUT.mkdir(exist_ok=True)
EV=[json.loads(x) for x in (RUN/'trace.jsonl').read_text(encoding='utf-8').splitlines()]
STARTS=[e for e in EV if e['event']=='rawtree.start']
encoder=Tokenizer.from_file(str(next((Path.home()/'.cache/huggingface/hub/models--vllm-sr--d3-mini/snapshots').glob('*/tokenizer.json'))))
encoder.no_truncation();encoder.no_padding()
class Counter:
    def count(self,text):return len(encoder.encode(text,add_special_tokens=False).ids)
def dump_csv(name,rows):
    if not rows:return
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)

async def main():
    allnodes=[];allbundles=[];alllinks=[];allreplays=[];lines=['# 516번 전체 검색 트리 점수','',
        '저장된 p33 점수다. 통합 question의 새 점수와 섞지 않았다. 검색 결과 depth=1. —는 미평가이며 0점이 아니다.','']
    global_ids={r['source']:r.get('source_id','') for e in EV if e['event']=='rawtree.return' for r in e['returned']}
    for sn,start in enumerate(STARTS,1):
        sid=start['search_id'];ev=[e for e in EV if e.get('search_id')==sid]
        nodes={};preview={};bundles={};chunks={};returned={};read=set();parents={};titles={}
        def node(nid):return nodes.setdefault(nid,{'search':sn,'search_id':sid,'query':start['query'],'node_id':nid,'depth':1,'parent':'root','url':'','title':'','inspect':None,'direct':None,'query_score':None,'inspected':False,'returned':False,'fetch_failed':False})
        entries=next(e for e in ev if e['event']=='rawtree.entries')
        leadmap={x['lead']['url']:x['lead'] for x in entries['candidates']}
        for i,url in enumerate(entries['selected']):
            n=node(f'n{i}');n.update(url=url,title=leadmap.get(url,{}).get('title',''))
        for e in ev:
            kind=e['event']
            if kind in ('rawtree.preview','rawtree.fetch_failed','rawtree.fetch_reused'):
                n=node(e['node_id']);n['url']=e['url']
                if kind=='rawtree.preview':n.update(depth=e['depth'],inspect=e['scores'].get('inspect_value'))
                if kind=='rawtree.fetch_failed':n['fetch_failed']=True;n['error']=e['error']
            if kind=='rawtree.frontier':
                admitted={c['url']:c for c in e['candidates']}
                # Resolve selected IDs from preview/failure events, which retain URLs.
                for nid in e['selected']:
                    target=next((x for x in ev if x.get('node_id')==nid and x['event'] in ('rawtree.preview','rawtree.fetch_failed','rawtree.fetch_reused')),None)
                    if target:
                        n=node(nid);c=admitted.get(target['url'],{})
                        n.update(url=target['url'],depth=e['depth']+1,parent=c.get('parent','?'),incoming_score=c.get('score'))
            if kind=='rawtree.inspection_selection':
                for nid in e['selected']:node(nid)['inspected']=True;read.add(nid)
            if kind=='rawtree.chunks':chunks[e['node_id']]=e['chunks']
            if kind=='rawtree.bundles':bundles[e['node_id']]=e
            if kind=='rawtree.return':
                ret=e
                for r in e['returned']:node(r['node_id'])['returned']=True;returned[r['node_id']]=r
        for e in EV:
            if e['event']=='jev.request' and e.get('context',{}).get('search_id')==sid:
                state=e['body']['state'];nid=e['context'].get('node_id')
                if nid and isinstance(state,dict):titles[nid]=state.get('page_title','')
        cache={}
        for nid,b in bundles.items():
            n=node(nid);n['direct']=max(x['direct_answer'] for x in b['bundles']);n['query_score']=max(x['query_answer'] for x in b['bundles'])
            cs=[SimpleNamespace(**c) for c in chunks[nid]]
            doc_title=titles.get(nid,n['title']);doc_content=''
            # Reader title is available in successful fetch.raw headers. Use last successful matching URL.
            for raw in EV:
                if raw['event']=='fetch.raw' and raw.get('url')==n['url'] and not raw.get('is_error'):
                    text=raw.get('content','');doc_content=text
                    if text.startswith('Title: '):doc_title=text.splitlines()[0][7:]
            ns=SimpleNamespace(node_id=nid,url=n['url'],depth=n['depth'],document=SimpleNamespace(title=doc_title,content=doc_content),notes='')
            units=[]
            for x in b['bundles']:
                selected=x['id'] in b['selected_bundle_ids']
                unit={**x,'id':f'{nid}:bundle:{x["id"]}','bundle_id':x['id'],'node':ns,'chunk_id':x['chunk_ids'][0],'evaluation_unit':'bundle'}
                if selected:units.append(unit)
                text='\n\n'.join(cs[i].text for i in x['chunk_ids'])
                allbundles.append({'search':sn,'node_id':nid,'depth':n['depth'],'url':n['url'],'bundle_id':x['id'],'tokens':x['tokens'],
                    'direct':x['direct_answer'],'query':x['query_answer'],'kept':selected,
                    'returned':x['id'] in returned.get(nid,{}).get('bundle_ids',[]),'contains_nzioki':'Peter Nzioki' in text})
            cache[nid]=(cs,units)
        linkmap={}
        for e in ev:
            if e['event']=='rawtree.links':
                for link in e['links']:
                    if link.get('score') is not None:
                        key=(e['node_id'],link['url'])
                        if key not in linkmap or linkmap[key]['score']<link['score']:linkmap[key]=link
        admitted={(n['parent'],n['url']) for n in nodes.values() if n['depth']>1}
        for (nid,url),link in linkmap.items():alllinks.append({'search':sn,'parent':nid,'depth':nodes[nid]['depth'],'url':url,'anchor':link.get('anchor',''),'score':link['score'],'visited':(nid,url) in admitted})
        page_rows=[{'id':nid,'node':cache[nid][1][0]['node'],'direct_answer':n['direct'],'query_answer':n['query_score']}
                   for nid,n in nodes.items() if nid in cache]
        config=SimpleNamespace(**start['config']);tree=RawTree(SimpleNamespace(chunker=Counter()),config,None);tree.source_ids=global_ids
        class Trace(NullTrace):
            def __init__(self):self.skips=[]
            def event(self,kind,**kwargs):
                if kind=='rawtree.output_budget':self.skips.append(kwargs.get('chunk'))
        baseline_ids=[r['node_id'] for r in ret['returned']]
        policies=[('baseline',1,1,2,14000,False),('pages3_d2_q1',2,1,3,14000,False),('pages3_d1_q2',1,2,3,14000,False),
                  ('pages4_d2_q2',2,2,4,14000,False),('reserve_deepest_2pages',1,1,2,14000,True),
                  ('pages3_output18k',2,1,3,18000,False),('pages3_output22k',2,1,3,22000,False),
                  ('reserve_deepest_output18k',1,1,2,18000,True),
                  ('reserve_deepest_ancestor1_leaf3',1,1,2,14000,True),
                  ('reserve_deepest_ancestor1_leaf3_16k',1,1,2,16000,True),
                  ('all_inspected',0,0,0,14000,False)]
        for name,d,q,cap,budget,reserve in policies:
            picked=quota_select(page_rows,d,q,floor=config.jev_floor)[:cap]
            if name=='all_inspected':picked=page_rows
            if reserve and page_rows:
                first=quota_select(page_rows,1,0,floor=config.jev_floor)
                remaining=[r for r in page_rows if not first or r['id']!=first[0]['id']]
                deepest=max((r['node'].depth for r in remaining),default=0)
                tail=quota_select([r for r in remaining if r['node'].depth==deepest],1,1,floor=config.jev_floor)[:1]
                picked=(first+tail)[:cap]
            trace=Trace();stats=defaultdict(int,{'fetch_failed':ret['stats']['fetch_failed']})
            output_cache=cache
            if name.startswith('reserve_deepest_ancestor1_leaf3') and picked:
                maxdepth=max(r['node'].depth for r in picked)
                output_cache={}
                for r in picked:
                    nid=r['id'];cs,us=cache[nid]
                    limit=3 if r['node'].depth==maxdepth else 1
                    us=sorted(us,key=lambda u:-max(u['direct_answer'],u['query_answer']))[:limit]
                    output_cache[nid]=(cs,us)
            text,units,outs,seen=await tree._read_rows(picked,question='',query=start['query'],search_id=sid,trace=trace,meter=None,
                    stats=stats,failures=[],scores=None,evaluate=None,output_budget=budget,scored_pages=output_cache,record_notes=False,visited=set())
            result={'search':sn,'policy':name,'selected_pages':[r['id'] for r in picked],'returned_pages':[r['node_id'] for r in outs],
                    'returned_bundle_ids':{r['node_id']:r['bundle_ids'] for r in outs},'output_tokens':tree.jev.chunker.count(text),
                    'output_budget':budget,'skipped':trace.skips,'nzioki_returned':'Peter Nzioki' in text}
            if name=='baseline':
                assert set(result['returned_pages'])==set(baseline_ids),(sn,result['returned_pages'],baseline_ids)
                assert result['returned_bundle_ids']=={r['node_id']:r['bundle_ids'] for r in ret['returned']},(sn,'bundle replay mismatch')
            allreplays.append(result)
        lines+= [f'## 검색 {sn}: {start["query"]}','',f'방문 {ret["stats"]["page_visits"]}, 실패 {ret["stats"]["fetch_failed"]}, 본문 검사 {len(cache)}, 반환 {len(ret["returned"])}.','',
            '|노드|depth|부모|문서|미리보기|direct 최대|query 최대|상태|','|---|---:|---|---|---:|---:|---:|---|']
        fmt=lambda x:'—' if x is None else f'{x:.3f}'
        for nid,n in sorted(nodes.items(),key=lambda x:int(x[0][1:])):
            n['title']=n['title'] or titles.get(nid,'') or n['url'].split('/')[-1]
            label=n['title'].replace('|','/').replace('\n',' ')
            status='접근 실패' if n['fetch_failed'] else ('본문 반환' if n['returned'] else '본문 검사 후 미반환' if n['inspected'] else '미리보기만')
            lines.append(f'|{nid}|{n["depth"]}|{n["parent"]}|[{label}]({n["url"]})|{fmt(n["inspect"])}|{fmt(n["direct"])}|{fmt(n["query_score"])}|{status}|')
        lines+=['','### 검사 문서의 모든 묶음','', '|노드|묶음|direct|query|반환|출연진 단서|','|---|---:|---:|---:|---|---|']
        for b in allbundles:
            if b['search']==sn:lines.append(f'|{b["node_id"]}|{b["bundle_id"]}|{b["direct"]:.3f}|{b["query"]:.3f}|{"O" if b["returned"] else "—"}|{"Peter Nzioki" if b["contains_nzioki"] else ""}|')
        lines+=[''];allnodes.extend(nodes.values())
    dump_csv('nodes.csv',allnodes);dump_csv('bundles.csv',allbundles);dump_csv('links.csv',alllinks)
    (OUT/'selection_replay.json').write_text(json.dumps(allreplays,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'all_trees.md').write_text('\n'.join(lines),encoding='utf-8')
    print('COUNTS',len(allnodes),'nodes',len(allbundles),'bundles',len(alllinks),'links')
    for n in allnodes:
        if n['inspected']:print('PAGE',n['search'],n['node_id'],n['depth'],n['title'][:65],round(n['inspect'],3),round(n['direct'],3),round(n['query_score'],3),n['returned'])
    for r in allreplays:
        if r['search']==5:print('REPLAY',json.dumps(r))

if __name__=='__main__':asyncio.run(main())
