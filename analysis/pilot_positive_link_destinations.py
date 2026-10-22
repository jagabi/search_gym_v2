"""Positive/bridge controls: exact logged states, strict target question plus URL."""
import asyncio
import copy
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'runs/test/20261022-1504_jevtree_gpt-oss-20b_browsecomp_raw_browser_p31_pplx_no_early_return_10'
CASES=[
    (40,'cd498968c424480b9a72f48487c43e43','link_47',
     'https://worldathletics.org/athletes/-/14289238','Direct official athlete-profile control'),
    (40,'9e64ee1f92cf4439ba19c1ef50ecb975','link_13',
     'https://en.wikipedia.org/wiki/1999_World_Championships_in_Athletics','Event-to-results bridge; not guaranteed to contain the exact date'),
    (516,'b62872519d39486a86eaf7ce6865ee3c','link_27',
     'https://www.metacritic.com/movie/the-constant-gardener','Film-record bridge; gold cast passage previously fetched from its credits subpage'),
    (1196,'013728d341ef4aebad2d16f26635a514','link_56',
     'https://worldpopulationreview.com/cities/india/thiruvananthapuram','Alternative-city population check; context may not identify it as the needed candidate')]


async def main():
    load_dotenv(ROOT/'.env')
    prior=ROOT/'analysis/p31_diagnosis/strict_link_pilot_20261022-161716/requests.json'
    template=json.loads(prior.read_text(encoding='utf-8'))[0]['body']['questions']['link_32']
    strict_prefix=template['instructions'].split('Original question:',1)[0]
    output=prior.parent.parent/('positive_link_pilot_'+datetime.now().strftime('%Y%m%d-%H%M%S'))
    output.mkdir()
    jobs=[]
    for q,rid,target,url,label in CASES:
        request=result=None
        for line in (RUN/f'q{q:05}'/'trace.jsonl').open(encoding='utf-8'):
            e=json.loads(line)
            if e.get('request_id')==rid:
                if e['event']=='jev.request':request=e
                elif e['event']=='jev.result':result=e
        assert request and result
        original=request['body'];body=copy.deepcopy(original)
        original_question=body['questions'][target]['instructions']
        suffix=original_question[original_question.index('Original question:'):]
        body['questions'][target]={'type':'noul','criteria':copy.deepcopy(template['criteria']),
            'instructions':strict_prefix.replace('link_32',target)+'Original question:'+suffix.split('Original question:',1)[1]+
                f'\nActual destination URL for {target}: {url}'}
        assert body['state']==original['state']
        assert list(body['questions'])==list(original['questions'])
        assert all(body['questions'][k]==original['questions'][k] for k in body['questions'] if k!=target)
        text=body['state']['page_text']
        contexts=[text[max(0,m.start()-220):m.end()+260]
                  for m in list(re.finditer(r'(?<!\w)'+re.escape(target)+r'(?!\w)',text))[:3]]
        jobs.append({'q':q,'target':target,'url':url,'label':label,'before':result['scores'][target],
                     'source_contexts':contexts,'body':body})
    (output/'requests.json').write_text(json.dumps(jobs,indent=2,ensure_ascii=False),encoding='utf-8')
    async with httpx.AsyncClient(headers={'Authorization':f'Bearer {os.environ["PERPLEXITY_API_KEY"]}'},
                                 timeout=httpx.Timeout(30,connect=5),trust_env=False) as client:
        async def send(job):
            started=time.perf_counter()
            response=await client.post('https://api.perplexity.ai/v1/decisions',json=job['body'])
            response.raise_for_status();payload=response.json()
            elapsed=time.perf_counter()-started
            (output/f'q{job["q"]}_{job["target"]}_response.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
            row={k:job[k] for k in ('q','target','url','label','before','source_contexts')}
            row.update(after=payload['answers'][job['target']]['noul'],elapsed_s=elapsed,
                key_count=len(job['body']['questions']),state_unchanged=True,
                usage=payload.get('usage'),request_id=response.headers.get('x-request-id'))
            print(json.dumps(row,ensure_ascii=False),flush=True)
            return row
        rows=await asyncio.gather(*(send(job) for job in jobs))
    (output/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    print(str(output),flush=True)


asyncio.run(main())
