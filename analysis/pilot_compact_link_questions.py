"""Repeat the six saved cases with compact, URL-visible target questions."""
import asyncio
import copy
import json
import os
import time
from datetime import datetime
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis/p31_diagnosis'


async def main():
    load_dotenv(ROOT/'.env')
    negative=BASE/'visible_destination_pilot_20261022-161845'
    positive=BASE/'positive_link_pilot_20261022-162257'
    old={}
    jobs=[]
    for path in (negative,positive):
        summaries=json.loads((path/'summary.json').read_text(encoding='utf-8'))
        for row in summaries:
            q=row.get('q',row.get('question'))
            old[(q,row['target'])]=row.get('after',row.get('strict_visible_score'))
        for job in json.loads((path/'requests.json').read_text(encoding='utf-8')):
            item=copy.deepcopy(job)
            target=item['target'];destination=item.get('url',item.get('destination'))
            text=item['body']['questions'][target]['instructions']
            original=text.split('Original question:',1)[1].split('Current search target:',1)[0].strip()
            query=text.split('Current search target:',1)[1].split('Keep the subject,',1)[0].strip()
            item['body']['questions'][target]={'type':'noul','instructions':(
                f'Would following {target} at the destination below likely reveal a missing fact '
                'or a useful next step toward the original question?\n'
                'Judge this link, not adjacent links. Candidate lists, intermediate records '
                'and refutations count; topic similarity alone does not.\n'
                f'Destination: {destination}\nOriginal question: {original}\nCurrent search target: {query}')}
            assert item['body']['state']==job['body']['state']
            assert list(item['body']['questions'])==list(job['body']['questions'])
            assert all(item['body']['questions'][k]==job['body']['questions'][k]
                       for k in item['body']['questions'] if k!=target)
            item['prior_long_score']=old[(item['q'],target)]
            jobs.append(item)
    output=BASE/('compact_link_pilot_'+datetime.now().strftime('%Y%m%d-%H%M%S'))
    output.mkdir()
    (output/'requests.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
    async with httpx.AsyncClient(headers={'Authorization':f'Bearer {os.environ["PERPLEXITY_API_KEY"]}'},
                                 timeout=httpx.Timeout(30,connect=5),trust_env=False) as client:
        slots=asyncio.Semaphore(4)
        pacing=asyncio.Lock();next_send=0.0
        async def send(job):
            nonlocal next_send
            async with slots:
                async with pacing:
                    await asyncio.sleep(max(0,next_send-time.monotonic()))
                    next_send=time.monotonic()+1/6
                started=time.perf_counter()
                response=await client.post('https://api.perplexity.ai/v1/decisions',json=job['body'])
                response.raise_for_status();payload=response.json()
                elapsed=time.perf_counter()-started
            (output/f'q{job["q"]}_{job["target"]}_response.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
            row={'q':job['q'],'target':job['target'],'destination':job.get('url',job.get('destination')),
                 'original_score':job.get('before',job.get('old_scores',{}).get(job['target'])),
                 'long_url_score':job['prior_long_score'],
                 'compact_url_score':payload['answers'][job['target']]['noul'],
                 'elapsed_s':elapsed,'usage':payload.get('usage'),
                 'key_count':len(job['body']['questions']),'state_unchanged':True}
            print(json.dumps(row,ensure_ascii=False),flush=True)
            return row
        rows=await asyncio.gather(*(send(job) for job in jobs))
    (output/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    print(str(output),flush=True)


asyncio.run(main())
