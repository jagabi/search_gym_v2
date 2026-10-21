"""Rejudge a saved real page state with current production prompts, d3 only."""
import asyncio
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import yaml
from searchgym.agent import AgentConfig
from searchgym.jevtree import JevUsage
from searchgym.rawtree import LocalDecision, node_action_questions, node_read_question, reading_action_scores
from pilot_depth_routes import Trace

async def main():
    src, node, dest = sys.argv[1:]
    rows = [json.loads(s) for s in (ROOT/src).read_text(encoding='utf-8').splitlines()]
    request = next(r for r in rows if r['event']=='jev.request'
                   and r['context'].get('phase')=='preview' and r['context'].get('node_id')==node)
    state = request['body']['state']
    original = request['body']['questions']['direct_answer']['instructions']
    target = original.split('Target: ',1)[1].split('\n',1)[0]
    questions = node_action_questions(target,target,can_read=True,
                                     can_expand='expand_now' in request['body']['questions'])
    questions.pop('read_now',None)
    questions.update(direct_answer=node_read_question(target,query=False),query_answer=node_read_question(target,query=True))
    cfg = AgentConfig(**yaml.safe_load((ROOT/'configs/jevtree.yaml').read_text(encoding='utf-8'))['agent'])
    decision=LocalDecision(cfg)
    trace=Trace(ROOT/dest)
    try:
        result=reading_action_scores(await decision.noul(state,questions,trace,usage=JevUsage(),context={'phase':'pilot_replay'}))
        print(json.dumps(result),flush=True)
    finally:
        trace.file.close()
        await decision.aclose()
asyncio.run(main())
