"""Extra cases; apply the candidate prompt to every link key in each saved packet."""
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
BASE=ROOT/'analysis/p31_diagnosis'
RUN=ROOT/'runs/test/20261022-1504_jevtree_gpt-oss-20b_browsecomp_raw_browser_p31_pplx_no_early_return_10'
PREFIX=('Would this URL open a specific record or candidate list that advances the missing relation? '
        'An intermediate record counts. A page defining or describing an organization/service '
        'does not count. Evaluate the destination itself, not the record linked beside it.\n')
CASES=[(40,'81b7b11ca384455b87c335798d7650be',['link_9']),
       (40,'4acb3aadd0a848ec926b105353f5efc2',['link_17']),
       (326,'1a5103c784ca4441b9ee677758ece079',['link_2']),
       (326,'6adb2971fc4a4accb70a7435557afc02',['link_0']),
       (516,'b62872519d39486a86eaf7ce6865ee3c',['link_14','link_15'])]


async def main():
    load_dotenv(ROOT/'.env')
    inventory=json.loads((BASE/'all_scored_links.json').read_text(encoding='utf-8'))
    mapping={(r['request_id'],r['key']):r for r in inventory}
    output=BASE/('extra_link_pilot_'+datetime.now().strftime('%Y%m%d-%H%M%S'));output.mkdir()
    jobs=[]
    for q,rid,targets in CASES:
        request=None
        for line in (RUN/f'q{q:05}'/'trace.jsonl').open(encoding='utf-8'):
            e=json.loads(line)
            if e.get('request_id')==rid and e['event']=='jev.request':request=e;break
        assert request
        body=copy.deepcopy(request['body']);changed=0
        for k,question in list(body['questions'].items()):
            if not k.startswith('link_'):continue
            link=mapping[(rid,k)]
            text=question['instructions']
            original=text.split('Original question:',1)[1].split('Current search target:',1)[0].strip()
            query=text.split('Current search target:',1)[1].split('Keep the subject,',1)[0].strip()
            body['questions'][k]={'type':'noul','instructions':PREFIX+
                f'Destination: {link["url"]}\nOriginal question: {original}\nCurrent search target: {query}'}
            changed+=1
        assert body['state']==request['body']['state']
        assert all(body['questions'][k]==request['body']['questions'][k]
                   for k in body['questions'] if not k.startswith('link_'))
        contexts={}
        for target in targets:
            text=body['state']['page_text']
            contexts[target]=[text[max(0,m.start()-160):m.end()+220] for m in
                list(re.finditer(r'(?<!\w)'+re.escape(target)+r'(?!\w)',text))[:2]]
        jobs.append({'q':q,'rid':rid,'targets':targets,'body':body,'changed_link_keys':changed,
                     'contexts':contexts})
    (output/'requests.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
    async with httpx.AsyncClient(headers={'Authorization':f'Bearer {os.environ["PERPLEXITY_API_KEY"]}'},
                                 timeout=httpx.Timeout(30,connect=5),trust_env=False) as client:
        slots=asyncio.Semaphore(4);lock=asyncio.Lock();next_send=0.0
        async def send(job):
            nonlocal next_send
            async with slots:
                async with lock:
                    await asyncio.sleep(max(0,next_send-time.monotonic()));next_send=time.monotonic()+1/6
                started=time.perf_counter();response=await client.post('https://api.perplexity.ai/v1/decisions',json=job['body'])
                response.raise_for_status();payload=response.json();elapsed=time.perf_counter()-started
            (output/f'{job["rid"]}_response.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
            rows=[]
            for target in job['targets']:
                link=mapping[(job['rid'],target)]
                row={'q':job['q'],'target':target,'url':link['url'],'anchor':link['anchor'],
                     'before':link['score'],'after':payload['answers'][target]['noul'],
                     'changed_link_keys':job['changed_link_keys'],'elapsed_s':elapsed,
                     'contexts':job['contexts'][target]}
                rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
            return rows
        groups=await asyncio.gather(*(send(job) for job in jobs))
    (output/'summary.json').write_text(json.dumps([r for rows in groups for r in rows],ensure_ascii=False,indent=2),encoding='utf-8')
    print(str(output),flush=True)


asyncio.run(main())
