"""Sixteen extra calls isolating question coupling and known-context effects."""
import asyncio,json,os,sys,time
from pathlib import Path
import httpx
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from searchgym.paths import load_env
OUT=ROOT/'analysis/pplx_scoring_pilots/20261022-175715_fifth_estate'

async def main():
    load_env();jobs=json.loads((OUT/'requests.json').read_text(encoding='utf-8'))
    originals={j['bundle_id']:j for j in jobs if j['variant']=='original' and j['repeat']==0}
    novelty={j['bundle_id']:j for j in jobs if j['variant']=='known_progress' and j['repeat']==0}
    known='The relevant director is Bill Condon and the 2013 film is The Fifth Estate.'
    tests=[]
    for repeat in range(2):
        for bid in (0,1):
            for variant in ('original_plus_memory','novelty_without_memory','direct_alone','query_alone'):
                job=json.loads(json.dumps(novelty[bid] if variant=='novelty_without_memory' else originals[bid]))
                job.update(variant=variant,repeat=repeat)
                qs=job['body']['questions']
                if variant=='original_plus_memory':
                    for q in qs.values():q['instructions']+='\nEstablished facts: '+known
                if variant=='novelty_without_memory':
                    for q in qs.values():q['instructions']=q['instructions'].replace('\nEstablished facts: '+known,'')
                if variant=='direct_alone':job['body']['questions']={'direct_answer':qs['direct_answer']}
                if variant=='query_alone':job['body']['questions']={'query_answer':qs['query_answer']}
                tests.append(job)
    (OUT/'controls_requests.json').write_text(json.dumps(tests,indent=2),encoding='utf-8')
    rows=[]
    async with httpx.AsyncClient(headers={'Authorization':'Bearer '+os.environ['PERPLEXITY_API_KEY']},timeout=30,trust_env=False) as client:
        async def send(job):
            row={k:v for k,v in job.items() if k!='body'}
            try:
                response=await client.post('https://api.perplexity.ai/v1/decisions',json=job['body'])
                row.update(status=response.status_code,response=response.json());response.raise_for_status()
                row['scores']={k:row['response']['answers'][k]['noul'] for k in job['body']['questions']}
            except Exception as exc:row['error']=repr(exc)
            with (OUT/'controls_results.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(row)+'\n')
            return row
        for i in range(0,len(tests),4):
            # Sequential admission at 5/s, with at most four active jobs per wave.
            tasks=[]
            for job in tests[i:i+4]:
                tasks.append(asyncio.create_task(send(job)));await asyncio.sleep(.2)
            rows.extend(await asyncio.gather(*tasks))
    for r in rows:print(r['variant'],r['repeat'],r['bundle_id'],r.get('scores',r.get('error')))

if __name__=='__main__':asyncio.run(main())
