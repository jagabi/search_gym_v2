"""Single-question scoring of the same seven saved source states. No production edits."""
import asyncio
import copy
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import httpx

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from searchgym.paths import load_env

SOURCE=ROOT/'analysis/pplx_scoring_pilots/20261022-175715_fifth_estate'
PROMPT=(
    'Does this excerpt provide explicit evidence that advances answering the original '
    'question, with the search query as context? Direct answers, candidate identities '
    'and connecting facts count, even if incomplete. A keyword mention alone does not. '
    'Judge only source facts; do not assume the search query is true.\n'
    'Original question: {question}\nSearch query: {query}'
)

async def main():
    load_env()
    manifest=json.loads((SOURCE/'manifest.json').read_text(encoding='utf-8'))
    originals=[j for j in json.loads((SOURCE/'requests.json').read_text(encoding='utf-8'))
               if j['variant']=='original' and j['repeat']==0]
    out=ROOT/'analysis/pplx_scoring_pilots'/datetime.now().strftime('%Y%m%d-%H%M%S_unified_question')
    out.mkdir(parents=True)
    instructions=PROMPT.format(question=manifest['original_question'],query=manifest['query'])
    jobs=[]
    for original in sorted(originals,key=lambda j:j['bundle_id']):
        body=copy.deepcopy(original['body'])
        body['questions']={'evidence_value':{'type':'noul','instructions':instructions}}
        jobs.append({'bundle_id':original['bundle_id'],'state_hash':original['state_hash'],'body':body})
    assert len(jobs)==7
    (out/'requests.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'prompt.txt').write_text(instructions,encoding='utf-8')
    rows=[]
    async with httpx.AsyncClient(headers={'Authorization':'Bearer '+os.environ['PERPLEXITY_API_KEY']},
                                 timeout=30,trust_env=False) as client:
        async def send(job):
            row={'bundle_id':job['bundle_id'],'state_hash':job['state_hash']}
            try:
                response=await client.post('https://api.perplexity.ai/v1/decisions',json=job['body'])
                row.update(status=response.status_code,response=response.json());response.raise_for_status()
                row['score']=row['response']['answers']['evidence_value']['noul']
            except Exception as exc:row['error']=repr(exc)
            with (out/'results.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(row)+'\n')
            return row
        for i in range(0,len(jobs),4):
            tasks=[]
            for job in jobs[i:i+4]:
                tasks.append(asyncio.create_task(send(job)));await asyncio.sleep(.2)
            rows.extend(await asyncio.gather(*tasks))
            if any('error' in r for r in rows):raise RuntimeError('API error; inspect saved results')
    ranked=sorted(rows,key=lambda r:-r['score'])
    summary={'source_manifest':str(SOURCE/'manifest.json'),'prompt_template':PROMPT,
             'request_count':len(rows),'ranks':[{k:r[k] for k in ('bundle_id','score')} for r in ranked],
             'evidence_bundle_id':1,'evidence_rank':next(i+1 for i,r in enumerate(ranked) if r['bundle_id']==1),
             'input_tokens':sum(r['response'].get('usage',{}).get('input_tokens',0) for r in rows)}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2));print('OUTPUT',out)

if __name__=='__main__':asyncio.run(main())
