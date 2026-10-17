"""Bounded live-model wiring probe with a saved source; no live web search.

Not a benchmark/accuracy comparison: the relevant paper is deliberately supplied.
"""
import asyncio
import json
from dataclasses import replace
from datetime import datetime
from pathlib import Path
import sys
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from searchgym.agent import SearchAgent
from searchgym.config import load_test
from searchgym.explorer import Document
from searchgym.serving import profile_for
from searchgym.trace import Trace


async def main():
    prior = Path('runs/test/20261017-1836_jevtree_gpt-oss-20b_browsecomp_raw_browser_p8_10/q00057')
    question = json.loads((prior/'response.json').read_text(encoding='utf-8'))['question']
    url = 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7227421/'
    content = ''
    for line in (prior/'trace.jsonl').open(encoding='utf-8'):
        e = json.loads(line)
        if e['event'] == 'fetch.raw' and e['url'] == url and not e['is_error']:
            if len(e['content']) > len(content):
                content = e['content']
    assert content
    cfg = load_test(method='jevtree', model='gpt-oss', benchmark='browsecomp')
    agent_cfg = replace(cfg.agent, max_searches=1, max_turns=4, timeout_s=45,
                        max_tokens=3072, jev_entries=1, jev_direct_reads=1, jev_query_reads=0)
    title = '177Lu-DOTATATE for the treatment of gastroenteropancreatic neuroendocrine tumors'
    class SavedTools:
        def specs_for(self, names):
            return [SimpleNamespace(as_openai=lambda: {'type': 'function', 'function': {
                'name': 'web_search', 'description': 'Search and return original source excerpts.',
                'parameters': {'type': 'object', 'properties': {'query': {'type': 'string'}},
                               'required': ['query']}}})]
        async def search(self, query):
            payload = {'organic': [{'link': url, 'title': title}]}
            return payload, SimpleNamespace(is_error=False, duration_ms=0, text=json.dumps(payload))
        async def fetch(self, target, *, engine):
            return Document(target, content if target == url else 'Unavailable in saved-source replay.',
                            title=title if target == url else '', is_error=target != url)
    out = Path('analysis/rawtree_four_20261017') / ('live_replay_' + datetime.now().strftime('%H%M%S'))
    out.mkdir(parents=True)
    trace = Trace(out/'trace.jsonl', 'saved-q57-progressive')
    agent = SearchAgent(profile_for(cfg.model), agent_cfg, 'jevtree', cfg.explorer, cfg.explorer_prompt)
    print('Replay started:', out, 'source_chars:', len(content), flush=True)
    try:
        result = await asyncio.wait_for(agent.run(question, cfg.system_prompt, SavedTools(), trace), 180)
        payload = dict(answer=result.answer, error=result.error, latency_s=result.latency_ms/1000,
                       stop_reason=result.stop_reason, stats=result.reader_stats,
                       actions=[dict(name=t.name, arguments=t.arguments, refused=t.refused) for t in result.tool_calls],
                       state=result.research_state.snapshot())
        (out/'result.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({k:v for k,v in payload.items() if k!='state'}, ensure_ascii=False), flush=True)
    finally:
        await agent.aclose()


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
