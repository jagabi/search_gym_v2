"""Inspect saved entry candidates for the 15 baseline-only correct cases."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT/'runs/test/20261004-1329_jevtree_gpt-oss-20b_browsecomp_jevtree_v66_diagnostic10'
ALIASES = {
    191: ['shin hae', 'kang se'], 313: ['spero'], 326: ['fran manushkin'],
    334: ['valery marier', 'julieta', 'montserrat', 'buenos aires'],
    399: ['fantom', 'byung'], 514: ['fabriano', 'watermark', 'filigrana'],
    571: ['gruzman'], 660: ['glover'], 682: ['ted alexander', 'theodore alexander'],
    780: ['sterling'], 865: ['red suitcase'], 1016: ['fort columbia'],
    1185: ['canada'], 1204: ['islamic university', 'iut'], 1264: ['kristen bell'],
}


def matches(s, aliases):
    s = ' '.join(re.findall(r'\w+', s.casefold()))
    return any(re.search(r'\b'+re.escape(a)+r'\b', s) for a in aliases)


def main():
    rows = []
    for qid, aliases in ALIASES.items():
        p = RUN/f'q{qid:05}'
        trees = json.loads((p/'explorer.json').read_text(encoding='utf-8'))
        indexed = {}
        for tree in trees:
            stack = list(tree.get('opened', []))
            while stack:
                node = stack.pop()
                indexed[(tree.get('search_id'), node['urls'][0])] = node
                stack.extend(node.get('opened', []))
        requests, scores = [], {}
        for line in (p/'trace.jsonl').open(encoding='utf-8'):
            h = line[:650]
            if not any(s in h for s in ['run.start', 'jev.request', 'jevtree.entry_scores']):
                continue
            d = json.loads(line)
            if d['event'] == 'run.start':
                requests, scores = [], {}
            elif d['event'] == 'jev.request' and d.get('context', {}).get('phase') == 'entry':
                requests.append(d)
            elif d['event'] == 'jevtree.entry_scores':
                scores[d['search_id']] = d['scores']
        hits = []
        for req in requests:
            sid = req['context']['search_id']
            for result in req['body']['state'].get('search_results', []):
                if not matches(' '.join(str(result.get(k, '')) for k in ['title', 'url', 'snippet']), aliases):
                    continue
                node = indexed.get((sid, result['url']))
                ranked = scores.get(sid, [])
                rank = next((i+1 for i,x in enumerate(ranked) if x[1] == result['url']), None)
                score = next((x[0] for x in ranked if x[1] == result['url']), None)
                hits.append({'query': req['context']['query'], 'sid': sid, **result,
                             'entry_rank': rank, 'entry_score': score,
                             'visited': node is not None, 'read': node.get('read') if node else False,
                             'error': node.get('error') if node else None,
                             'direct': node.get('identification_score') if node else None,
                             'likely': node.get('verification_score') if node else None,
                             'notes': node.get('information', '') if node else ''})
        rows.append({'qid': qid, 'aliases': aliases, 'entry_requests': len(requests), 'hits': hits})
        print('Q', qid, 'candidate_hits', len(hits))
        for h in hits[:6]:
            print(json.dumps({k:v for k,v in h.items() if k not in ['sid','notes']}, ensure_ascii=False))
    (ROOT/'analysis/baseline_only_entry_audit.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
