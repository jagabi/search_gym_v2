"""Offline p33/p34 comparison and fixed-trajectory source-gate counterfactuals."""
import asyncio,csv,json,statistics,sys
from collections import Counter,defaultdict
from pathlib import Path
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from searchgym.rawtree import RawTree,quota_select
from searchgym.trace import NullTrace
from tokenizers import Tokenizer
P33=ROOT/'runs/test/20261022-1705_jevtree_gpt-oss-20b_browsecomp_raw_browser_p33_fetch_all10_10'
P34=ROOT/'runs/test/20261022-1829_jevtree_gpt-oss-20b_browsecomp_raw_browser_p34_chunk_return_10'
OUT=ROOT/'analysis/p34_diagnosis';OUT.mkdir(exist_ok=True)
def read_events(path):
    # JSON strings may contain U+2028/U+0085. They are not JSONL delimiters.
    return [json.loads(line) for line in path.read_text(encoding='utf-8').split('\n') if line.strip()]
def records(run):return read_events(run/'records.jsonl')
encoder=Tokenizer.from_file(str(next((Path.home()/'.cache/huggingface/hub/models--vllm-sr--d3-mini/snapshots').glob('*/tokenizer.json'))))
encoder.no_truncation();encoder.no_padding()
class Tokens:
    def count(self,text):return len(encoder.encode(text,add_special_tokens=False).ids)
class Trace(NullTrace):
    def __init__(self):self.skips=[]
    def event(self,kind,**fields):
        if kind=='rawtree.output_budget':self.skips.append(fields['chunk'])

async def replay(q,ev):
    allout=[]
    source_ids={r['source']:r.get('source_id','') for e in ev if e['event']=='rawtree.return' for r in e['returned']}
    raw={e['url']:e.get('content','') for e in ev if e['event']=='fetch.raw' and not e.get('is_error')}
    for sn,start in enumerate((e for e in ev if e['event']=='rawtree.start'),1):
        sid=start['search_id'];se=[e for e in ev if e.get('search_id')==sid]
        ret=next(e for e in se if e['event']=='rawtree.return')
        selection=next(e for e in se if e['event']=='rawtree.pages_selected')['pages']
        previews={e['node_id']:e for e in se if e['event']=='rawtree.preview'}
        ch={e['node_id']:e['chunks'] for e in se if e['event']=='rawtree.chunks'}
        bs={e['node_id']:e for e in se if e['event']=='rawtree.bundles'}
        titles={e['context']['node_id']:e['body']['state'].get('page_title','') for e in ev
                if e['event']=='jev.request' and e.get('context',{}).get('search_id')==sid
                and e['context'].get('node_id') and isinstance(e['body']['state'],dict)}
        pages=[];cache={}
        for row in selection:
            nid=row['id'];p=previews[nid];content=raw.get(p['url'],'');title=titles.get(nid,'')
            if content.startswith('Title: '):title=content.split('\n',1)[0][7:]
            n=SimpleNamespace(node_id=nid,url=p['url'],depth=p['depth'],notes='',document=SimpleNamespace(title=title,content=content))
            pages.append({**row,'node':n})
            cs=[SimpleNamespace(**c) for c in ch[nid]]
            us=[{**b,'id':f'{nid}:bundle:{b["id"]}','bundle_id':b['id'],'node':n,
                 'chunk_id':b['chunk_ids'][0],'evaluation_unit':'bundle'}
                for b in bs[nid]['bundles'] if b['id'] in bs[nid]['selected_bundle_ids']]
            cache[nid]=(cs,us)
        cfg=SimpleNamespace(**start['config']);tree=RawTree(SimpleNamespace(chunker=Tokens()),cfg,None);tree.source_ids=source_ids
        rowout={'index':q,'search':sn,'query':start['query'],'search_id':sid,'inspected_pages':len(pages),'policies':{}}
        for policy in ('all_inspected','old_source_gate'):
            selected=pages if policy=='all_inspected' else quota_select(pages,cfg.jev_direct_reads,cfg.jev_query_reads,floor=cfg.jev_floor)[:cfg.jev_reads]
            trace=Trace()
            text,picked,returned,_=await tree._read_rows(selected,question='',query=start['query'],search_id=sid,trace=trace,meter=None,
                stats=defaultdict(int,{'fetch_failed':ret['stats']['fetch_failed']}),failures=[],scores=None,evaluate=None,
                output_budget=cfg.jev_output_tokens-cfg.jev_notice_tokens,scored_pages=cache,record_notes=False,visited=set())
            ids=[u['id'] for u in picked]
            if policy=='all_inspected':assert ids==[u['id'] for u in ret['selected']],(q,sn,'replay mismatch',ids,[u['id'] for u in ret['selected']])
            rowout['policies'][policy]={'page_ids':[r['id'] for r in selected],'bundle_ids':ids,'sources':[r['source'] for r in returned],
                'body_tokens':tree.jev.chunker.count(text),'skipped':trace.skips,
                'hits':{term:term.casefold() in text.casefold() for term in ['Peter Nzioki','Peter King','Fran Manushkin','Thiruvananthapuram','Raja Ravi Varma']}}
            (OUT/f'q{q}_s{sn}_{policy}.txt').write_text(text,encoding='utf-8')
        rowout['added_bundles']=sorted(set(rowout['policies']['all_inspected']['bundle_ids'])-set(rowout['policies']['old_source_gate']['bundle_ids']))
        rowout['removed_bundles']=sorted(set(rowout['policies']['old_source_gate']['bundle_ids'])-set(rowout['policies']['all_inspected']['bundle_ids']))
        allout.append(rowout)
    return allout

async def main():
    comparison=[];replays=[];details=[]
    for old,new in zip(records(P33),records(P34)):
        assert old['index']==new['index'];q=new['index']
        a=read_events(P33/old['dir']/'trace.jsonl');b=read_events(P34/new['dir']/'trace.jsonl')
        qa=[e['query'] for e in a if e['event']=='rawtree.start'];qb=[e['query'] for e in b if e['event']=='rawtree.start']
        def stat(ev,r):
            returns=[e for e in ev if e['event']=='rawtree.return'];depth=Counter()
            for e in ev:
                if e['event']=='rawtree.inspection_selection':depth[e['depth']]+=len(e['selected'])
            http=[e['duration_ms']/1000 for e in ev if e['event']=='jev.response']
            return {'score':r['score'],'seconds':r['latency_s'],'searches':r['searches'],'depth':dict(depth),
                    'empty':sum(not e['returned'] for e in returns),'output_tokens':sum(e['stats']['raw_output_tokens'] for e in returns),
                    'returned_bundles':sum(len(e['selected']) for e in returns),'returned_sources':sum(len(e['returned']) for e in returns),
                    'http_n':len(http),'http_mean':statistics.mean(http) if http else None,'http_max':max(http,default=None)}
        row={'index':q,'p33':stat(a,old),'p34':stat(b,new),'same_first_query':qa[0]==qb[0],'first_p33':qa[0],'first_p34':qb[0]}
        comparison.append(row);print('COMPARISON',json.dumps(row,ensure_ascii=False),flush=True)
        response=json.loads((P34/new['dir']/'response.json').read_text(encoding='utf-8'))
        d={'index':q,'question':response['question'],'gold':response['gold_answer'],'answer':response['answer'],'queries':qb,'returns':[],'targets':[]}
        for sn,e in enumerate((e for e in b if e['event']=='rawtree.return'),1):
            d['returns'].append({'search':sn,'query':qb[sn-1],'tokens':e['stats']['raw_output_tokens'],'sources':[r['source'] for r in e['returned']],
                                 'bundles':[{k:u[k] for k in ['id','direct_answer','query_answer','objective']} for u in e['selected']]})
        needles={326:['Fran Manushkin','Manushkin'],516:['Peter Nzioki','Peter King','Nzioki'],1196:['Thiruvananthapuram','Raja Ravi Varma','3.25','Indreshwar'],598:['Elisabeta','Jemna','Romanian Statistical Review']}.get(q,[])
        results={e['request_id']:e for e in b if e['event']=='jev.result'}
        for e in b:
            if e['event']=='fetch.raw' and not e.get('is_error'):
                for term in needles:
                    content=e.get('content','');pos=content.casefold().find(term.casefold())
                    if pos>=0:d['targets'].append({'event':'fetch.raw','term':term,'url':e['url'],'excerpt':content[max(0,pos-100):pos+400]})
            if e['event']=='jev.request' and e.get('context',{}).get('phase')=='bundle':
                state=e['body']['state'];text=state.get('page_text','')
                for term in needles:
                    pos=text.casefold().find(term.casefold())
                    if pos>=0:d['targets'].append({'event':'bundle_input','term':term,'context':e['context'],
                        'title':state.get('page_title'),'excerpt':text[max(0,pos-100):pos+350],
                        'scores':{k:v for k,v in results[e['request_id']]['scores'].items() if k in ['direct_answer','query_answer']}})
        details.append(d)
        if q in (326,516,1196):
            replays.extend(await replay(q,b));print('REPLAY_DONE',q,flush=True)
    for name,data in [('comparison.json',comparison),('details.json',details),('counterfactuals.json',replays)]:
        (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print('DONE',len(replays),'search counterfactuals',flush=True)

if __name__=='__main__':asyncio.run(main())
