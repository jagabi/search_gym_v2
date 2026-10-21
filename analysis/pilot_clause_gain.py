"""Evaluate exact question sentences separately; no generated plan or gold facts."""
import asyncio
import json
import re
import httpx
from pilot_marginal_actions import extract
from pilot_marginal_routes import OUT, Trace, config
from searchgym.rawtree import LocalDecision, node_read_question
from searchgym.jevtree import JevUsage

async def main():
    client=LocalDecision(config());await client.http.aclose()
    client.http=httpx.AsyncClient(timeout=httpx.Timeout(40,connect=5),trust_env=False)
    trace=Trace(OUT/'clause_replay.jsonl');usage=JevUsage();rows=[]
    cases=[('film','bill_focused_current.jsonl','n3'),('other_person','bill_focused_current.jsonl','n4'),
           ('bridge','bill_focused_current.jsonl','n1'),
           ('birth_facts','chemistry_focused_current.jsonl','n1'),('metadata','direct_focused_current.jsonl','n0')]
    try:
        for name,file,node in cases:
            state,base=extract(OUT/file,node)
            original=base['direct_answer']['instructions'].split('Target: ',1)[1].split('\n',1)[0]
            clauses=re.split(r'(?<=[.!?。！？])\s+',original)
            questions={f'clause_{i}':node_read_question(c,query=False) for i,c in enumerate(clauses)}
            scores=await client.noul({**state,'original_question':original},questions,trace,usage=usage,
                context={'phase':'clause_pilot','case':name})
            row=dict(case=name,clauses=clauses,scores=scores,maximum=max(scores.values()))
            rows.append(row);print(json.dumps(row,ensure_ascii=True),flush=True)
            (OUT/'clause_summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    finally:trace.f.close();await client.aclose()
if __name__=='__main__':asyncio.run(main())
