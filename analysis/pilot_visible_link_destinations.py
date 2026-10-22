"""Repeat two strict-link pilot requests with only the target URL disclosed."""
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
BASE=ROOT/'analysis/p31_diagnosis/strict_link_pilot_20261022-161716'


async def main():
    load_dotenv(ROOT/'.env')
    jobs=json.loads((BASE/'requests.json').read_text(encoding='utf-8'))
    previous={r['question']:r for r in json.loads((BASE/'summary.json').read_text(encoding='utf-8'))}
    output=BASE.parent/('visible_destination_pilot_'+datetime.now().strftime('%Y%m%d-%H%M%S'))
    output.mkdir()
    modified=[]
    for job in jobs:
        item=copy.deepcopy(job)
        target=item['target']
        item['body']['questions'][target]['instructions']+=(
            f'\nActual destination URL for {target}: {item["destination"]}')
        assert item['body']['state']==job['body']['state']
        assert list(item['body']['questions'])==list(job['body']['questions'])
        assert all(item['body']['questions'][k]==job['body']['questions'][k]
                   for k in item['body']['questions'] if k!=target)
        modified.append(item)
    (output/'requests.json').write_text(json.dumps(modified,ensure_ascii=False,indent=2),encoding='utf-8')
    async with httpx.AsyncClient(headers={'Authorization':f'Bearer {os.environ["PERPLEXITY_API_KEY"]}'},
                                 timeout=httpx.Timeout(30,connect=5),trust_env=False) as client:
        async def send(job):
            started=time.perf_counter()
            response=await client.post('https://api.perplexity.ai/v1/decisions',json=job['body'])
            response.raise_for_status();payload=response.json()
            elapsed=time.perf_counter()-started
            (output/f'q{job["q"]}_response.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
            row={'question':job['q'],'target':job['target'],'destination':job['destination'],
                 'original_score':job['old_scores'][job['target']],
                 'strict_hidden_score':previous[job['q']]['after'],
                 'strict_visible_score':payload['answers'][job['target']]['noul'],
                 'elapsed_s':elapsed,'state_unchanged':True,'key_count':len(job['body']['questions']),
                 'usage':payload.get('usage'),'request_id':response.headers.get('x-request-id')}
            print(json.dumps(row,ensure_ascii=False),flush=True)
            return row
        rows=await asyncio.gather(*(send(job) for job in modified))
    (output/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    print(str(output),flush=True)


asyncio.run(main())
