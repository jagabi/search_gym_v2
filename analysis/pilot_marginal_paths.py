"""Fixed-seed full-tree pilot of current RawTree; Jina+d3 only.

The current variant uses production routing unchanged. Other variants temporarily
replace the link criterion/input for comparison inside this process only.
"""
import argparse
import asyncio
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import httpx
from searchgym.explorer import Document
from searchgym.tools import WebTools
import searchgym.rawtree as raw
from pilot_marginal_routes import config, marginal_question, edge_question, focused_scores
from probe_pilot_services import settings

BASE_LINK=raw.link_question
CASES={
 'bill': (json.loads((ROOT/'runs/test/20261021-1340_jevtree_gpt-oss-20b_browsecomp_raw_browser_p18_pilot/q00516/response.json').read_text(encoding='utf-8'))['question'],
          '"Kinsey" film director 2004', ['https://en.wikipedia.org/wiki/Kinsey_(film)']),
 'chemistry': ('What is the full birth date and birthplace of the person awarded the 1911 Nobel Prize in Chemistry?',
              '1911 Nobel Prize in Chemistry', ['https://www.nobelprize.org/prizes/chemistry/1911/summary/']),
 'pep615': ('Who authored the PEP that introduced zoneinfo in Python 3.9, and on what date was that PEP created?',
            'zoneinfo Python 3.9 PEP', ['https://docs.python.org/3.9/whatsnew/3.9.html']),
 'direct': ('What is the status and creation date of PEP 615?', 'PEP 615 status creation date',
            ['https://peps.python.org/pep-0615/']),
}

class Trace:
 def __init__(self,path):
  self.f=path.open('w',encoding='utf-8');self.nodes={}
 def event(self,event,**kw):
  self.f.write(json.dumps(dict(event=event,**kw),ensure_ascii=False,default=str)+'\n');self.f.flush()
  if event=='rawtree.preview':self.nodes[kw['node_id']]={k:kw.get(k) for k in ['url','depth']}

async def main(args):
 folder=ROOT/args.output_dir;folder.mkdir(parents=True,exist_ok=True)
 cache=ROOT/'analysis/pilots/bodies';cache.mkdir(exist_ok=True)
 cfg=config();cfg.jev_rank_entries=False
 if args.depth is not None:cfg.jev_depth=args.depth
 decision=raw.LocalDecision(cfg)
 base_noul=decision.noul
 await decision.http.aclose();decision.http=httpx.AsyncClient(timeout=httpx.Timeout(40,connect=5),trust_env=False)
 _,_,reader=settings();web=WebTools();web.reader_status={'jina_base_url':reader}
 web._reader_http=httpx.AsyncClient(timeout=40,trust_env=False)
 try:
  await decision.prepare()
  for name in args.cases:
   question,query,urls=CASES[name]
   for variant in args.variants:
    label=variant+(f'_d{args.depth}' if args.depth is not None else '')
    criterion=variant.removeprefix('focused_')
    if criterion=='current':raw.link_question=BASE_LINK
    elif criterion=='original':
     def original(q,query,marker,url,anchor):
      v=BASE_LINK(q,query,marker,url,anchor)
      v['instructions']=v['instructions'].replace('facts answering the current search target?','facts answering the original question?')
      return v
     raw.link_question=original
    elif criterion=='edge':raw.link_question=edge_question
    else:raw.link_question=marginal_question
    async def routed_noul(state,questions,trace,*,usage,context):
     if variant.startswith('focused_') and context.get('phase')=='links':
      return await focused_scores(decision,state,questions,trace,usage,context)
     return await base_noul(state,questions,trace,usage=usage,context=context)
    decision.noul=routed_noul
    trace=Trace(folder/f'{name}_{label}.jsonl');fetches=[]
    async def fetch(url,*,engine):
     dest=cache/(hashlib.sha256(url.encode()).hexdigest()+'.json')
     reused=dest.exists();start=time.perf_counter()
     if reused:doc=Document(**json.loads(dest.read_text(encoding='utf-8')))
     else:
      doc=await web.fetch(url,engine=engine)
      if not doc.is_error:dest.write_text(json.dumps(asdict(doc),ensure_ascii=False),encoding='utf-8')
     fetches.append({'url':url,'cached':reused,'failed':doc.is_error,'seconds':round(time.perf_counter()-start,3)})
     return doc
    start=time.perf_counter()
    try:
     tree,text,stats=await asyncio.wait_for(raw.RawTree(decision,cfg,fetch).run_search(query,
       [{'link':u} for u in urls],question=question,trace=trace,usage=None),args.timeout)
     report=dict(case=name,variant=label,seconds=round(time.perf_counter()-start,3),stats=stats,
                 nodes=trace.nodes,fetches=fetches,tree=tree)
     (folder/f'{name}_{label}.evidence.txt').write_text(text,encoding='utf-8')
    except Exception as exc:report=dict(case=name,variant=label,error=repr(exc),fetches=fetches,seconds=round(time.perf_counter()-start,3))
    finally:trace.f.close()
    (folder/f'{name}_{label}.summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='tree'},ensure_ascii=True),flush=True)
 finally:
  raw.link_question=BASE_LINK
  await decision.aclose();await web._reader_http.aclose()

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--cases',nargs='+',choices=CASES,default=['chemistry','pep615','direct'])
 p.add_argument('--variants',nargs='+',default=['current','marginal']);p.add_argument('--timeout',type=float,default=180)
 p.add_argument('--depth',type=int)
 p.add_argument('--output-dir',default='analysis/pilots/p19_marginal')
 asyncio.run(main(p.parse_args()))
