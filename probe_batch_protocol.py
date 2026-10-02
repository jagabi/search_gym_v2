"""Bounded model-only DS diagnostics; never executes tools or evaluates answers."""
from __future__ import annotations
import argparse
import asyncio
import copy
import json
from datetime import datetime
from pathlib import Path

from openai import AsyncOpenAI
from searchgym.config import load_test
from searchgym.serving import profile_for

ROOT = Path(__file__).resolve().parent
RUN = ROOT / 'runs/test/20260925-1231_depthsearch_gpt-oss-20b_browsecomp_ds_batch_v9-2'

def events(q):
    return [json.loads(l) for l in (RUN/q/'trace.jsonl').read_text(encoding='utf-8').split('\n') if l.strip()]

def native_cases():
    original = next(e for e in events('q00026') if e['event']=='control.request' and e['mode']=='select')
    spec = copy.deepcopy(original['tools'])
    spec[0]['function']['parameters']['properties']['url']['enum'] = ['https://example.org/alpha', 'https://example.org/beta']
    messages = [{'role':'system','content':'Reasoning: medium\nYou test native tool-call serialization. Only call the supplied tool.'},
        {'role':'user','content':'Read BOTH independent supplied records: https://example.org/alpha and https://example.org/beta. Emit two web_fetch calls in this single response, one url per call. Do not wait for a result between the two calls. This is a format diagnostic; no tool is actually executed.'}]
    cases=[]
    for explicit in [False, True]:
        for rep in range(2):
            cases.append(dict(name=f'format_parallel_{explicit}_{rep+1}', messages=messages, tools=spec,
                              tool_choice='auto', **({'parallel_tool_calls':True} if explicit else {})))
    for q in ['q00008','q00026']:
        e=next(e for e in events(q) if e['event']=='control.request' and e['mode']=='select')
        cases.append(dict(name=f'{q}_saved_select_parallel',messages=e['messages'],tools=e['tools'],
                          tool_choice='auto',parallel_tool_calls=True))
    return cases

async def run(args):
    cfg=load_test(ROOT/'conf.yaml',method='depthsearch');profile=profile_for(cfg.model)
    cases=native_cases() if args.phase=='native' else json.loads(Path(args.cases).read_text(encoding='utf-8'))
    if len(cases)>16: raise ValueError('At most 16 calls per diagnostic phase.')
    output=ROOT/'runs/batch_protocol_probe'/datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    output.mkdir(parents=True)
    (output/'cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(cases)} model calls; NO search/fetch/judge. Output: {output}',flush=True)
    sem=asyncio.Semaphore(2)
    async with AsyncOpenAI(base_url=cfg.agent.base_url,api_key=cfg.agent.api_key,timeout=120,max_retries=0) as client:
        async def one(case):
            async with sem:
                request={k:v for k,v in case.items() if k!='name'}
                request.update(model=cfg.agent.model_name or profile.repo,max_tokens=cfg.agent.max_tokens,**profile.sampling)
                extra=dict(profile.sampling_extra)
                if profile.thinking_kwarg: extra['chat_template_kwargs']={'enable_thinking':True}
                if extra: request['extra_body']=extra
                data={'name':case['name'],'request':request}
                try:
                    raw=await client.chat.completions.create(**request)
                    data['response']=raw.model_dump()
                    choice=raw.choices[0];m=choice.message
                    row={'name':case['name'],'calls':len(m.tool_calls or []),'text_chars':len(m.content or ''),
                         'finish_reason':choice.finish_reason,'usage':raw.usage.model_dump() if raw.usage else {},
                         'tool_calls':[c.model_dump() for c in m.tool_calls or []]}
                except Exception as exc:
                    data['error']=repr(exc);row={'name':case['name'],'error':repr(exc)}
                (output/(case['name']+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
                print(json.dumps(row,ensure_ascii=False),flush=True)
                return row
        rows=await asyncio.gather(*(one(c) for c in cases))
    (output/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--phase',choices=['native','replay'],default='native')
    parser.add_argument('--cases');args=parser.parse_args()
    if args.phase=='replay' and not args.cases:parser.error('--cases required for replay')
    asyncio.run(run(args))
