"""Six saved inputs: compact prompt plus one generic-overview exclusion sentence."""
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
BASE=ROOT/'analysis/p31_diagnosis/compact_link_pilot_20261022-163324'
PREFIX=('Would this URL open a specific record or candidate list that advances the missing relation? '
        'An intermediate record counts. A page defining or describing an organization/service '
        'does not count. Evaluate the destination itself, not the record linked beside it.\n')


async def main():
    load_dotenv(ROOT/'.env')
    previous={(r['q'],r['target']):r for r in json.loads((BASE/'summary.json').read_text(encoding='utf-8'))}
    jobs=json.loads((BASE/'requests.json').read_text(encoding='utf-8'))
    output=BASE.parent/('compact_suppression_pilot_'+datetime.now().strftime('%Y%m%d-%H%M%S'))
    output.mkdir()
    modified=copy.deepcopy(jobs)
    for old,job in zip(jobs,modified):
        question=job['body']['questions'][job['target']]
        question['instructions']=PREFIX+'Destination:'+question['instructions'].split('Destination:',1)[1]
        assert question['instructions']!=old['body']['questions'][job['target']]['instructions']
        assert job['body']['state']==old['body']['state']
        assert all(job['body']['questions'][k]==old['body']['questions'][k]
                   for k in job['body']['questions'] if k!=job['target'])
    (output/'requests.json').write_text(json.dumps(modified,ensure_ascii=False,indent=2),encoding='utf-8')
    async with httpx.AsyncClient(headers={'Authorization':f'Bearer {os.environ["PERPLEXITY_API_KEY"]}'},
                                 timeout=httpx.Timeout(30,connect=5),trust_env=False) as client:
        slots=asyncio.Semaphore(4);lock=asyncio.Lock();next_send=0.0
        async def send(job):
            nonlocal next_send
            async with slots:
                async with lock:
                    await asyncio.sleep(max(0,next_send-time.monotonic()));next_send=time.monotonic()+1/6
                started=time.perf_counter()
                response=await client.post('https://api.perplexity.ai/v1/decisions',json=job['body'])
                response.raise_for_status();payload=response.json();elapsed=time.perf_counter()-started
            (output/f'q{job["q"]}_{job["target"]}_response.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
            before=previous[(job['q'],job['target'])]
            row={'q':job['q'],'target':job['target'],'destination':before['destination'],
                 'compact_score':before['compact_url_score'],
                 'suppressed_score':payload['answers'][job['target']]['noul'],
                 'elapsed_s':elapsed,'usage':payload.get('usage')}
            print(json.dumps(row,ensure_ascii=False),flush=True)
            return row
        results=await asyncio.gather(*(send(job) for job in modified))
    (output/'summary.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(str(output),flush=True)


asyncio.run(main())
