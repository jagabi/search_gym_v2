"""Small paid PPLX scoring ablation on one saved document; no benchmark or production edits."""
import asyncio
import copy
import hashlib
import json
import os
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path

import httpx

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from searchgym.paths import load_env

RUN=ROOT/'runs/test/20261022-1705_jevtree_gpt-oss-20b_browsecomp_raw_browser_p33_fetch_all10_10/q00516'
SID='0fb414b68efe49aa8ba185c42d6a183f'

def question(text):return {'type':'noul','instructions':text}

async def main():
    load_env()
    key=os.environ.get('PERPLEXITY_API_KEY')
    if not key:raise RuntimeError('PERPLEXITY_API_KEY missing')
    ev=[json.loads(x) for x in (RUN/'trace.jsonl').read_text(encoding='utf-8').splitlines()]
    original=json.loads((RUN/'response.json').read_text(encoding='utf-8'))['question']
    target=next(e['query'] for e in ev if e['event']=='rawtree.start' and e['search_id']==SID)
    requests={e['context']['bundle_id']:e for e in ev if e['event']=='jev.request'
              and e.get('context',{}).get('search_id')==SID
              and e.get('context',{}).get('node_id')=='n12'
              and e.get('context',{}).get('phase')=='bundle'}
    assert set(requests)==set(range(7))
    assert all(set(e['body']['state'])=={'page_title','page_text'} for e in requests.values())
    assert all(set(e['body']['questions'])=={'direct_answer','query_answer'} for e in requests.values())
    out=ROOT/'analysis/pplx_scoring_pilots'/datetime.now().strftime('%Y%m%d-%H%M%S_fifth_estate')
    out.mkdir(parents=True)
    jobs=[]
    known='The relevant director is Bill Condon and the 2013 film is The Fifth Estate.'
    scope='Score only explicit source facts; do not infer an unstated match.'
    for variant in ('original','compact','person_focus','known_progress','retarget_cast'):
        for repeat in range(2):
            for bid,e in sorted(requests.items()):
                body=copy.deepcopy(e['body']);body={'model':'pplx-decider-v1.2','state':body['state'],'questions':body['questions']}
                if variant=='compact':
                    body['questions']={
                        'direct_answer':question(f'Does this excerpt give explicit candidate identities or connecting facts useful for answering the original question? {scope}\nOriginal question: {original}'),
                        'query_answer':question(f'Does this excerpt explicitly answer or refute the current search target? {scope}\nCurrent search target: {target}\nOriginal question: {original}')}
                elif variant=='person_focus':
                    body['questions']={
                        'direct_answer':question(f'Does this excerpt name candidate people with roles or biographical facts that narrow the person sought? A film or director alone is a bridge, not a candidate person meeting the clues. {scope}\nOriginal question: {original}'),
                        'query_answer':question(f'Does this excerpt establish the requested film/director or identify people in that film who could advance the original question? {scope}\nCurrent search target: {target}\nOriginal question: {original}')}
                elif variant=='known_progress':
                    body['questions']={
                        'direct_answer':question(f'Does this excerpt add a named candidate person or a verifiable connecting relation beyond the established facts? Repeating established facts alone has no added value. {scope}\nEstablished facts: {known}\nOriginal question: {original}'),
                        'query_answer':question(f'Does this excerpt add a concrete next lead beyond the established film and director, such as cast members paired with character roles? Repeating established facts alone has no added value. {scope}\nEstablished facts: {known}\nOriginal question: {original}')}
                elif variant=='retarget_cast':
                    body['questions']['query_answer']=question(f'Does this excerpt explicitly identify cast members and their character roles in The Fifth Estate (2013), providing candidates for the original question? {scope}\nOriginal question: {original}')
                state_hash=hashlib.sha256(json.dumps(body['state'],sort_keys=True).encode()).hexdigest()
                assert body['state']==e['body']['state']
                jobs.append({'variant':variant,'repeat':repeat,'bundle_id':bid,'state_hash':state_hash,'body':body})
    # Save exact test inputs with no credentials. Never add answer names to questions.
    (out/'requests.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
    manifest={'run':str(RUN),'search_id':SID,'query':target,'original_question':original,
              'document':'https://en.wikipedia.org/wiki/The_Fifth_Estate_(film)',
              'state_policy':'exact saved states, each already bounded by the production 4096-token limit',
              'request_count':len(jobs),'repeats':2,'concurrency':4,'variants':sorted({j['variant'] for j in jobs}),
              'caveat':'Only one document. No controlled cross-document ranking or accuracy estimate. Identical repeats may be cached.',
              'evidence_bundle_ids':[bid for bid,e in requests.items() if 'Peter Nzioki' in e['body']['state']['page_text']],
              'logged_scores':{e['context']['bundle_id']:next((r['scores'] for r in ev if r['event']=='jev.result' and r['request_id']==e['request_id']),{}) for e in requests.values()}}
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'output':str(out),'requests':len(jobs),'evidence_bundle_ids':manifest['evidence_bundle_ids']}),flush=True)
    rows=[];pace_lock=asyncio.Lock();next_start=0.
    async with httpx.AsyncClient(headers={'Authorization':f'Bearer {key}'},timeout=httpx.Timeout(30,connect=5),trust_env=False) as client:
        async def send(job):
            nonlocal next_start
            async with pace_lock:
                delay=max(0,next_start-time.monotonic())
                if delay:await asyncio.sleep(delay)
                next_start=time.monotonic()+.2
            row={k:v for k,v in job.items() if k!='body'};start=time.monotonic()
            try:
                resp=await client.post('https://api.perplexity.ai/v1/decisions',json=job['body'])
                row.update(status=resp.status_code,response=resp.json())
                resp.raise_for_status()
                row['scores']={k:row['response']['answers'][k]['noul'] for k in job['body']['questions']}
            except Exception as exc:row['error']=repr(exc)
            row['seconds']=time.monotonic()-start
            with (out/'results.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
            return row
        # Four at a time, with variants interleaved to avoid temporal confounding.
        jobs.sort(key=lambda j:(j['repeat'],j['bundle_id'],j['variant']))
        for start in range(0,len(jobs),4):
            rows.extend(await asyncio.gather(*(send(j) for j in jobs[start:start+4])))
            print('completed',len(rows),'/',len(jobs),flush=True)
            if sum('error' in r for r in rows)>=3:raise RuntimeError('Three API errors; stop pilot. Inspect saved results.')
    summary=[]
    for variant in manifest['variants']:
        for bid in sorted(requests):
            selected=[r for r in rows if r['variant']==variant and r['bundle_id']==bid and 'scores' in r]
            summary.append({'variant':variant,'bundle_id':bid,'evidence_candidate':bid in manifest['evidence_bundle_ids'],
                            'n':len(selected),**{k:round(statistics.mean(r['scores'][k] for r in selected),5) for k in ('direct_answer','query_answer')},
                            'scores':[r['scores'] for r in selected]})
    total={'rows':summary,'request_count':len(rows),'errors':sum('error' in r for r in rows),
           'reported_input_tokens':sum(r.get('response',{}).get('usage',{}).get('input_tokens',0) for r in rows)}
    (out/'summary.json').write_text(json.dumps(total,indent=2),encoding='utf-8')
    for variant in manifest['variants']:
        group=[r for r in summary if r['variant']==variant]
        print(variant,'direct',[(r['bundle_id'],r['direct_answer']) for r in sorted(group,key=lambda r:-r['direct_answer'])],
              'query',[(r['bundle_id'],r['query_answer']) for r in sorted(group,key=lambda r:-r['query_answer'])],flush=True)
    print('OUTPUT',out,flush=True)

if __name__=='__main__':asyncio.run(main())
