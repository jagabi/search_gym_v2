"""Live d3 latency only: distinct 4096-token states, strict four-request waves."""
import asyncio
import hashlib
import json
import random
import re
import statistics
import sys
import time
from pathlib import Path
from uuid import uuid4

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from searchgym.config import load_test
from searchgym.paths import load_env
from searchgym.explorer import Document
from searchgym.jevtree import TreeNode
from searchgym.rawtree import LocalDecision, RawTree


def source_pool():
    run=ROOT/'runs/test/20261022-1233_jevtree_gpt-oss-20b_browsecomp_raw_browser_p29_return_now_10'
    pool=[];seen=set()
    for q in ('q00040','q00057'):
        question=query=''
        for line in (run/q/'trace.jsonl').open(encoding='utf-8'):
            e=json.loads(line)
            if e['event']=='run.start':question=e.get('question','Identify the source facts requested by the search target.')
            elif e['event']=='rawtree.start':query=e['query']
            elif e['event']=='fetch.raw' and not e.get('is_error'):
                text=e.get('content','');url=e['url']
                if len(text)<25000 or url in seen:continue
                seen.add(url)
                title=e.get('reader_metadata',{}).get('source_reported',{}).get('title') or 'Original source document'
                pool.append(dict(question=question,query=query,text=text,url=url,title=title))
    return pool


def exact_state(chunker,title,text):
    def count(n):return chunker.count(json.dumps({'page_title':title,'page_text':text[:n]},ensure_ascii=False))
    if count(len(text))<4096:return None
    lo,hi=0,len(text)
    while lo<hi:
        mid=(lo+hi+1)//2
        if count(mid)<=4096:lo=mid
        else:hi=mid-1
    for n in range(max(0,lo-64),min(len(text),lo+64)+1):
        if count(n)==4096:
            return {'page_title':title,'page_text':text[:n]}
    return None


async def main():
    load_env();cfg=load_test(method='jevtree').agent
    output=ROOT/'analysis'/'d3_latency_pilots'/time.strftime('%Y%m%d-%H%M%S')
    output.mkdir(parents=True,exist_ok=False)
    decision=LocalDecision(cfg)
    try:
        await decision.prepare()
        tree=RawTree(decision,cfg,None);pool=source_pool()
        rng=random.Random();hashes=set();jobs=[]
        # Counterbalance small/large key waves to reduce a simple time-order effect.
        for wave,key_count in enumerate((3,16,16,3)):
            for slot in range(4):
                for attempt in range(500):
                    source=pool[(wave*4+slot+attempt)%len(pool)]
                    # Different source offsets, not nonce-only changes to a repeated prefix.
                    limit=max(1,len(source['text'])-22000)
                    offset=rng.randrange(limit)
                    boundary=source['text'].find('\n\n',offset)
                    if boundary>=0 and boundary<limit:offset=boundary+2
                    raw=source['text'][offset:]
                    node=TreeNode(url=source['url'],depth=1,anchor=source['title'],
                                  document=Document(source['url'],raw,title=source['title']))
                    state,questions,links=tree._joint_input(node,raw,source['question'],source['query'],{source['url']})
                    state=exact_state(decision.chunker,state['page_title'],state['page_text'])
                    if state is None:continue
                    visible=list(dict.fromkeys(re.findall(r'\blink_\d+\b',state['page_text'])))
                    if len(visible)<key_count-3:continue
                    selected=['direct_answer','query_answer','return_now']+visible[:key_count-3]
                    questions={k:questions[k] for k in selected}
                    digest=hashlib.sha256(json.dumps(state,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
                    if digest in hashes:continue
                    hashes.add(digest)
                    body={'model':cfg.jev_model,'state':state,'questions':questions,'request_id':uuid4().hex}
                    job=dict(wave=wave+1,slot=slot+1,key_count=key_count,state_tokens=4096,
                             state_hash=digest,source=source['url'],source_offset=offset,body=body)
                    jobs.append(job);break
                else:raise RuntimeError('Could not construct a distinct, source-only 4096-token state')
        assert len(hashes)==16
        (output/'requests.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps({'ready':True,'endpoint':decision.endpoint,'model':cfg.jev_model,
                          'requests':len(jobs),'unique_states':len(hashes),'state_tokens':4096,
                          'concurrency':4,'output':str(output)},ensure_ascii=False),flush=True)
        results=[];waves=[];active=peak=0
        async def send(job):
            nonlocal active,peak
            active+=1;peak=max(peak,active)
            assert active<=4
            started=time.perf_counter()
            result={k:v for k,v in job.items() if k!='body'}
            try:
                response=await decision.http.post(decision.endpoint,json=job['body'])
                result['http_status']=response.status_code
                response.raise_for_status();payload=response.json()
                result['usage']=payload.get('usage',{})
                answers=payload.get('answers',{})
                result['valid_keys']=sum(k in answers and isinstance(answers[k].get('noul'),(int,float))
                                         for k in job['body']['questions'])
                result['ok']=result['valid_keys']==job['key_count']
                (output/f"response_w{job['wave']}_s{job['slot']}.json").write_text(
                    json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
            except Exception as exc:result.update(ok=False,error=repr(exc))
            finally:
                active-=1
                result['elapsed_s']=time.perf_counter()-started
            with (output/'results.jsonl').open('a',encoding='utf-8') as f:
                f.write(json.dumps(result,ensure_ascii=False)+'\n')
            print(json.dumps({k:result.get(k) for k in ('wave','slot','key_count','ok','elapsed_s','error')},ensure_ascii=False),flush=True)
            return result
        for wave in range(1,5):
            group=[j for j in jobs if j['wave']==wave]
            print(f'WAVE {wave} START: 4 requests, {group[0]["key_count"]} keys each',flush=True)
            started=time.perf_counter()
            # Do not refill an early-freed slot. Finish all four before starting the next four.
            batch=await asyncio.gather(*(send(job) for job in group))
            results.extend(batch)
            waves.append(dict(wave=wave,key_count=group[0]['key_count'],wall_s=time.perf_counter()-started))
            print(json.dumps({'wave_complete':waves[-1]},ensure_ascii=False),flush=True)
        summary={'endpoint':decision.endpoint,'model':cfg.jev_model,'tokenizer':cfg.jev_model,
                 'state_tokens':4096,'peak_http':peak,'distinct_states':len(hashes),'waves':waves,'groups':{}}
        for keys in (3,16):
            rows=[r for r in results if r['key_count']==keys];good=[r for r in rows if r['ok']]
            times=[r['elapsed_s'] for r in good]
            summary['groups'][str(keys)]={'attempts':len(rows),'successes':len(good),'failures':len(rows)-len(good),
                'mean_s':statistics.mean(times) if times else None,'median_s':statistics.median(times) if times else None,
                'min_s':min(times) if times else None,'max_s':max(times) if times else None,
                'mean_wave_wall_s':statistics.mean(w['wall_s'] for w in waves if w['key_count']==keys),
                'mean_reported_input_tokens':statistics.mean(r.get('usage',{}).get('input_tokens',0) for r in good) if good else None}
        (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
        print('SUMMARY '+json.dumps(summary,ensure_ascii=False),flush=True)
    finally:await decision.aclose()


if __name__=='__main__':asyncio.run(main())
