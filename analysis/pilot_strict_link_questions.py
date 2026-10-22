"""Two exact logged source states; only the target link question is changed."""
import asyncio
import copy
import hashlib
import json
import os
import time
from datetime import datetime
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'runs/test/20261022-1504_jevtree_gpt-oss-20b_browsecomp_raw_browser_p31_pplx_no_early_return_10'
CASES=[(516,'b62872519d39486a86eaf7ce6865ee3c','link_32',
        'https://en.wikipedia.org/wiki/IMDb_(identifier)'),
       (40,'cd498968c424480b9a72f48487c43e43','link_48',
        'https://en.wikipedia.org/wiki/World_Athletics')]


async def main():
    load_dotenv(ROOT/'.env')
    key=os.environ['PERPLEXITY_API_KEY']
    output=ROOT/'analysis/p31_diagnosis'/('strict_link_pilot_'+datetime.now().strftime('%Y%m%d-%H%M%S'))
    output.mkdir()
    jobs=[]
    for q,request_id,target,destination in CASES:
        request=result=None
        for line in (RUN/f'q{q:05}'/'trace.jsonl').open(encoding='utf-8'):
            e=json.loads(line)
            if e.get('request_id')==request_id:
                if e['event']=='jev.request':request=e
                if e['event']=='jev.result':result=e
        assert request and result
        original=request['body'];body=copy.deepcopy(original)
        instructions=original['questions'][target]['instructions']
        targets=instructions[instructions.index('Original question:'):]
        body['questions'][target]={
            'type':'noul',
            'instructions':(
                f'Evaluate ONLY the destination represented by {target} in page_text. '
                'Would opening that exact destination likely establish a missing identifying '
                'relation or provide a specific record needed by the original question? '
                'Bind the judgment to this marker, its own anchor and its local grammatical role. '
                'Adjacent links are different destinations: do not transfer their record, profile, '
                'cast list, statistics or evidence to this marker. A source or service name beside '
                'a linked record does not itself establish that this marker opens that record. '
                'Definitions, organization descriptions, generic navigation and another work '
                'sharing an entity are not useful routes unless the observed context establishes '
                'a concrete connection to the missing relation. Candidate lists, intermediate '
                'records and refutations remain useful when that connection is explicit. '
                'Do not invent destination contents or assume the target is resolved because '
                'the surrounding page is relevant.\n'+targets),
            'criteria':{
                'true':'The observed context binds this exact marker to a specific record or route advancing the missing relation.',
                'false':'Usefulness belongs to another link, or relies only on a topic/service name or an unsupported destination assumption.'}}
        assert body['state']==original['state']
        assert list(body['questions'])==list(original['questions'])
        assert all(body['questions'][k]==original['questions'][k] for k in body['questions'] if k!=target)
        jobs.append({'q':q,'target':target,'destination':destination,'old_scores':result['scores'],
            'state_sha256':hashlib.sha256(json.dumps(body['state'],sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
            'body':body})
    (output/'requests.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
    async with httpx.AsyncClient(headers={'Authorization':f'Bearer {key}'},
                                 timeout=httpx.Timeout(30,connect=5),trust_env=False) as client:
        async def send(job):
            started=time.perf_counter()
            response=await client.post('https://api.perplexity.ai/v1/decisions',json=job['body'])
            response.raise_for_status();payload=response.json()
            (output/f"q{job['q']}_response.json").write_text(json.dumps(payload,indent=2),encoding='utf-8')
            scores={k:v['noul'] for k,v in payload['answers'].items()}
            row={'question':job['q'],'target':job['target'],'destination':job['destination'],
                 'before':job['old_scores'][job['target']],'after':scores[job['target']],
                 'elapsed_s':time.perf_counter()-started,'key_count':len(job['body']['questions']),
                 'state_unchanged':True,'changed_question_count':1,'request_id':response.headers.get('x-request-id'),
                 'usage':payload.get('usage'), 'other_score_changes':{k:{'before':job['old_scores'].get(k),'after':v}
                     for k,v in scores.items() if k!=job['target'] and abs(v-job['old_scores'].get(k,v))>.05}}
            print(json.dumps(row,ensure_ascii=False),flush=True)
            return row
        rows=await asyncio.gather(*(send(job) for job in jobs))
    (output/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    print(str(output),flush=True)


asyncio.run(main())
