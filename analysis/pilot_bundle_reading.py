"""Live d3-only reading pilot over original source documents in saved traces.

No search, fetch, main inference model or judge calls. Gold checks are used only
after scoring and are never sent to d3.
"""
import argparse
import asyncio
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from searchgym.config import load_test
from searchgym.explorer import Document
from searchgym.jevtree import JevUsage, TreeNode
from searchgym.paths import load_env
from searchgym.rawtree import RawTree, LocalDecision, LocalDecisionError, decision_question, VERSION


SPECS = [
    ('40', '20261021-1739*', 'sporting-heroes.net/athletics/kenya/tegla-loroupe',
     ['10,000 Metres 30:32.03 Sevilla 26 AUG 1999']),
    ('57', '20261021-2232*', '82nlqV-nihms-1586521.pdf',
     ['Vanderbilt clinical oncology research career development award']),
    ('366', '20261021-1948*', 'https://and1.com/pages/and1-history-1',
     ['making the Mixtape one of the most successful promotions in US retail history']),
    ('1196', '20261021-1948*', '1752225934_Chapter13',
     ['Thiruvananthapuram was 3.3 million', '3.25% growth rate']),
]


def norm(text):
    return re.sub(r'[^\w]', '', text.casefold())


def has_evidence(text, checks):
    text = norm(text)
    return all(norm(check) in text for check in checks)


def sources():
    cases = []
    for qid, pattern, url_part, checks in SPECS:
        run = next((ROOT/'runs/test').glob(pattern))
        qpath = run/f'q{int(qid):05d}'
        response = json.loads((qpath/'response.json').read_text(encoding='utf-8'))
        query = None
        for line in (qpath/'trace.jsonl').open(encoding='utf-8'):
            if '"event": "rawtree.start"' in line:
                query = json.loads(line)['query']
            elif '"event": "fetch.raw"' in line:
                e = json.loads(line)
                if url_part in e.get('url', '') and not e.get('is_error'):
                    assert query and has_evidence(e['content'], checks), (qid, 'missing source evidence')
                    cases.append(dict(id=qid, question=response['question'], query=query,
                        source=e['url'], text=e['content'], checks=checks,
                        saved_trace=str((qpath/'trace.jsonl').relative_to(ROOT))))
                    break
        else:
            raise ValueError(f'Original source not found: {qid}')
    return cases


class Trace:
    def __init__(self, path):
        self.events = []
        self.file = path.open('w', encoding='utf-8')
        self.started = time.perf_counter()

    def event(self, name, **kwargs):
        e = dict(event=name, elapsed_ms=round(1000*(time.perf_counter()-self.started), 1), **kwargs)
        self.events.append(e)
        self.file.write(json.dumps(e, ensure_ascii=False)+'\n')
        self.file.flush()


async def run_case(case, decision, cfg, output):
    trace = Trace(output/f'q{case["id"]}_trace.jsonl')
    meter, stats, failures = JevUsage(), defaultdict(int), []
    tree = RawTree(decision, cfg, None)
    n = TreeNode(url=case['source'], node_id='source', depth=1,
                 document=Document(case['source'], case['text']))
    chunks, bundles, _ = await tree._chunks(case['text'])
    assert all(b['tokens'] <= 4096 for b in bundles)

    async def scores(state, preview, **context):
        return await tree._noul(state, {
            'direct_answer': decision_question(case['question'], query=False),
            'query_answer': decision_question(case['query'], query=True, original_question=case['question'])},
            trace, usage=meter, context={'search_id': case['id'], **context})

    async def evaluate(coro, phase, node, **context):
        try:
            return await coro
        except LocalDecisionError as exc:
            stats[f'{phase}_eval_failures'] += 1
            failures.append(dict(phase=phase, error=str(exc)))
            return exc.partial_scores

    started = time.perf_counter()
    try:
        text, picked, returned, _ = await tree._read_rows([
            {'id': n.node_id, 'node': n, 'objective': 'direct_answer'}],
            question=case['question'], query=case['query'], search_id=case['id'],
            trace=trace, meter=meter, stats=stats, failures=failures,
            scores=scores, evaluate=evaluate, output_budget=cfg.jev_output_tokens-cfg.jev_notice_tokens)
        if VERSION.endswith('/25'):
            assert stats['chunks_scored'] == 0
            assert all(r['evaluation_unit'] == 'bundle' for r in picked)
            delivered = {i for source in returned for i in source['chunk_ids']}
            assert all(set(r['chunk_ids']) <= delivered for r in picked)
            assert not any(e['event']=='jev.request' and e['context'].get('phase')=='chunk'
                           for e in trace.events)
        gold_bundles = [b['id'] for b in bundles if has_evidence(b['text'], case['checks'])]
        routing = [e for e in trace.events if e['event']=='rawtree.document_candidates']
        candidates = routing[-1]['selected_bundle_ids'] if routing else [b['id'] for b in bundles]
        judged = [e for e in trace.events if e['event']=='rawtree.bundles']
        row = dict(id=case['id'], version=VERSION, source=case['source'],
            question=case['question'], query=case['query'], chunks=len(chunks), bundles=len(bundles),
            max_bundle_tokens=max(b['tokens'] for b in bundles), gold_bundles=gold_bundles,
            region_candidates=candidates,
            gold_scores=[b for e in judged for b in e['bundles'] if b['id'] in gold_bundles],
            evidence_returned=has_evidence(text, case['checks']),
            http_requests=meter.calls, attempts=meter.attempts, failures=failures,
            questions=sum(e['question_count'] for e in trace.events if e['event']=='jev.request'),
            input_tokens=meter.input_tokens, elapsed_s=round(time.perf_counter()-started, 2),
            phases=dict(Counter(e['context']['phase'] for e in trace.events if e['event']=='jev.request')),
            stats=dict(stats), returned_tokens=decision.chunker.count(text),
            selected=[{k:v for k,v in r.items() if k!='node'} for r in picked])
        (output/f'q{case["id"]}_returned.txt').write_text(text, encoding='utf-8')
        (output/f'q{case["id"]}_result.json').write_text(json.dumps(row, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({k:row[k] for k in ['id','bundles','gold_bundles','evidence_returned',
            'http_requests','questions','elapsed_s','failures']}, ensure_ascii=False), flush=True)
        return row
    finally:
        trace.file.close()


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', required=True)
    parser.add_argument('--case', action='append')
    parser.add_argument('--force-regions', action='store_true')
    args = parser.parse_args()
    load_env()
    cfg = load_test(method='jevtree').agent
    cfg.jev_bundle_tokens = 4096
    if args.force_regions:
        cfg.jev_tree_min_bundles = 1
        cfg.jev_leaf_bundles = 2
    cases = [c for c in sources() if not args.case or c['id'] in args.case]
    output = ROOT/'analysis'/'bundle_pilots'/args.tag
    output.mkdir(parents=True, exist_ok=False)
    (output/'cases.json').write_text(json.dumps(cases, ensure_ascii=False, indent=2), encoding='utf-8')
    (output/'settings.json').write_text(json.dumps(dict(version=VERSION, tokenizer=cfg.jev_model,
        bundle_tokens=cfg.jev_bundle_tokens, internal_chunk_tokens=cfg.jev_chunk_tokens,
        region_threshold=cfg.jev_tree_min_bundles, region_leaf_bundles=cfg.jev_leaf_bundles,
        concurrency=cfg.jev_concurrency, packet_keys=cfg.jev_packet_questions,
        evidence_output_budget=cfg.jev_output_tokens-cfg.jev_notice_tokens), indent=2), encoding='utf-8')
    decision = LocalDecision(cfg)
    try:
        await decision.prepare()
        print(json.dumps(dict(ready=True, tokenizer=cfg.jev_model, bundle_tokens=4096,
            region_threshold=cfg.jev_tree_min_bundles, output=str(output)), ensure_ascii=False), flush=True)
        rows = [await run_case(c, decision, cfg, output) for c in cases]
        (output/'summary.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
    finally:
        await decision.aclose()


if __name__ == '__main__':
    asyncio.run(main())
