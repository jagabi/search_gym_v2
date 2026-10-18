"""Live model/d3 check of q746's contradictory vice-president hypothesis.

Supplies two saved source excerpts. This checks evidence use, not full q746 accuracy.
"""
import asyncio
from dataclasses import replace
from datetime import datetime
import json
from pathlib import Path
import sys
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from searchgym.agent import SearchAgent
from searchgym.config import load_test
from searchgym.explorer import Document
from searchgym.serving import profile_for
from probe_progressive_replay import CompactProbeTrace


async def main():
    prior = Path('runs/test/20261017-2332_jevtree_gpt-oss-20b_browsecomp_raw_browser_p9_10/q00746/trace.jsonl')
    urls = ['https://en.wikipedia.org/wiki/Hannibal_Hamlin',
            'https://cv.libguides.com/US_Vice_Presidents/nrockefeller']
    bodies = {}
    with prior.open(encoding='utf8') as stream:
        for line in stream:
            e = json.loads(line)
            if e['event'] == 'fetch.raw' and e.get('url') in urls and not e['is_error']:
                bodies.setdefault(e['url'], e['content'][:7000])
            if len(bodies) == 2:
                break
    assert len(bodies) == 2
    question = ('Which US vice president born in Maine is chronologically plausible as the '
                'employer of an aide who later employed a person born in the 1930s? '
                'Identify the vice president using the supplied sources and discuss the chronology '
                'of alternative candidates. Do not identify the younger person or their travels.')
    config = load_test(method='jevtree', model='gpt-oss', expected_raw_traversal='progressive')
    cfg = replace(config.agent, max_searches=1, max_turns=5, max_tokens=3072, timeout_s=45,
                  jev_entries=2, jev_reads=2, jev_direct_reads=1, jev_query_reads=1)
    class SavedTools:
        def specs_for(self, names):
            return [SimpleNamespace(as_openai=lambda: {'type': 'function', 'function': {
                'name': 'web_search', 'description': 'Search source records.',
                'parameters': {'type': 'object', 'properties': {'query': {'type': 'string'}}, 'required': ['query']}}})]
        async def search(self, query):
            payload = {'organic': [{'link': u, 'title': u.rsplit('/', 1)[-1]} for u in urls]}
            return payload, SimpleNamespace(is_error=False, duration_ms=0, text=json.dumps(payload))
        async def fetch(self, url, *, engine):
            return Document(url, bodies.get(url, 'Unavailable in replay'), is_error=url not in bodies)
    out = Path('analysis/audit_20261017-2332') / ('chronology_' + datetime.now().strftime('%H%M%S'))
    out.mkdir()
    trace = CompactProbeTrace(out/'trace.jsonl', 'saved-chronology')
    agent = SearchAgent(profile_for(config.model), cfg, 'jevtree', config.explorer, config.explorer_prompt)
    print('Replay started:', out, flush=True)
    try:
        result = await asyncio.wait_for(agent.run(question, config.system_prompt, SavedTools(), trace), 180)
        payload = {'answer': result.answer, 'error': result.error, 'latency_s': result.latency_ms/1000,
            'd3_requests': result.reader_stats.get('jev_requests'), 'invalid_tool_calls': result.invalid_tool_calls,
            'actions': [t.name for t in result.tool_calls], 'state': result.research_state.snapshot()}
        (out/'result.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf8')
        print(json.dumps({k: v for k, v in payload.items() if k != 'state'}, ensure_ascii=False), flush=True)
    finally:
        await agent.aclose()


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf8')
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
