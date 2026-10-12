"""Offline audit of observed JEV trees. No model calls and no application changes."""
import json
import re
import statistics
import sys
import unicodedata
from functools import lru_cache
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'runs/test/20261004-1329_jevtree_gpt-oss-20b_browsecomp_jevtree_v66_diagnostic10'
OUT = ROOT / 'analysis/jev_cross_parent_audit.json'


def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).casefold()
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return ' '.join(re.findall(r'[a-z0-9]+', s))


ALIASES = {
    40: ['26 august 1999', 'august 26 1999', '26 aug 1999', 'aug 26 1999'],
    79: ['johan human', 'john human'],
    128: [('bacon', 'bubblegum', 'cinnamon', 'wasabi')],
    131: ['world of the dream merchants'],
    240: ['marie of romania'],
    386: ['5tb', '5 tb', '5 terabytes'],
    392: ['alexander yarin', 'alexander l yarin'],
    680: ['6187', '6 187'],
    685: ['lola s cafe', 'lolas cafe'],
    905: [('pfaff', 'henzi')],
    972: ['january 23 1989', '23 january 1989', '23 01 1989'],
    1100: ['70', 'seventy percent'],
    1196: ['thiruvananthapuram', 'trivandrum'],
}


@lru_cache(maxsize=1024)
def pattern(word):
    accents = {'a': '[aàáâäãåāăą]', 'e': '[eèéêëēęě]', 'i': '[iìíîïī]',
               'o': '[oòóôöõōø]', 'u': '[uùúûüū]', 'c': '[cçćč]', 'n': '[nñń]'}
    words = norm(word).split()
    parts = [''.join(accents.get(c, re.escape(c)) for c in w) for w in words]
    return re.compile(r'(?<!\w)' + r'[\W_]*'.join(parts) + r'(?!\w)', re.I)


def match(text, aliases):
    return any(all(pattern(w).search(text) for w in (a if isinstance(a, (tuple, list)) else [a])) for a in aliases)


def snippets(text, aliases, limit=2):
    # Human review excerpts; selection labels are NOT automatic ground truth.
    words = [w for a in aliases for w in (a if isinstance(a, (list, tuple)) else [a])]
    found = []
    for w in words:
        tokens = re.findall(r'\w+', w)
        if not tokens:
            continue
        pat = r'\W*'.join(re.escape(t) for t in tokens)
        for m in re.finditer(pat, text, re.I):
            found.append(text[max(0, m.start()-160):m.end()+300])
            if len(found) >= limit:
                return found
    return found


def ranking(score, pool):
    if score is None:
        return None
    vals = list(pool.values())
    return {'best': 1 + sum(v > score for v in vals),
            'worst': sum(v >= score for v in vals), 'n': len(vals)}


def main():
    records = {d['index']: d for d in map(json.loads, (RUN/'records.jsonl').open(encoding='utf-8'))}
    output = OUT
    if len(sys.argv) > 1:
        wanted = {int(x) for x in sys.argv[1:]}
        records = {k:v for k,v in records.items() if k in wanted}
        output = OUT.with_name(OUT.stem + '_subset.json')
    all_questions = []
    corpus = Counter()
    for pos, (qid, rec) in enumerate(records.items(), 1):
        folder = RUN / rec['dir']
        response = json.loads((folder/'response.json').read_text(encoding='utf-8'))
        aliases = ALIASES.get(qid, [response['gold_answer']])
        forest = json.loads((folder/'explorer.json').read_text(encoding='utf-8'))
        scores, raw_hits, full_hits = {}, {}, {}
        active_search = None
        # Select the last appended attempt only.
        with (folder/'trace.jsonl').open(encoding='utf-8') as f:
            for line in f:
                h = line[:650]
                event = re.search(r'"event":\s*"([^"]+)"', h)
                if not event:
                    continue
                event = event[1]
                if event == 'run.start':
                    scores, raw_hits, full_hits = {}, {}, {}
                    active_search = None
                elif event == 'jevtree.scored':
                    d = json.loads(line)
                    scores[(d['search_id'], d['url'])] = d
                    active_search = d['search_id']
                elif event == 'jev.request':
                    d = json.loads(line)
                    st = d.get('body', {}).get('state', {})
                    ctx = d.get('context', {})
                    if ctx.get('phase') == 'page':
                        text = st.get('page_text', '')
                        if match(text, aliases):
                            raw_hits[(ctx['search_id'], st.get('page_url'))] = snippets(text, aliases)
                elif event == 'jevtree.reader_request':
                    d = json.loads(line)
                    try:
                        st = json.loads(d['messages'][-1]['content'])
                    except (ValueError, KeyError, IndexError, TypeError):
                        continue
                    text = st.get('page_text', '')
                    if match(text, aliases):
                        full_hits[(active_search, d['url'])] = snippets(text, aliases)
        qs = {'qid': qid, 'correct': bool(rec['accuracy']), 'gold': response['gold_answer'],
              'question': response['question'], 'answer': response['answer'][:2000], 'searches': [], 'hits': []}
        for si, tree in enumerate(forest, 1):
            sid = tree.get('search_id')
            if not sid:
                continue
            flat = []
            def visit(node, ancestors, root_rank, root_url):
                url = node['urls'][0]
                item = {'url': url, 'depth': node['depth'], 'link_score': node.get('link_score'),
                        'root_rank': root_rank, 'root_url': root_url, 'ancestors': list(ancestors),
                        'read': node.get('read', False), 'error': node.get('error'),
                        'notes': node.get('information', ''), 'score': scores.get((sid, url), {})}
                flat.append(item)
                for ch in node.get('opened', []):
                    visit(ch, ancestors + [url], root_rank, root_url)
            successful_roots = [n for n in tree.get('opened', []) if not n.get('error')]
            for root in tree.get('opened', []):
                rank = next((i+1 for i, r in enumerate(successful_roots) if r is root), None)
                visit(root, [], rank, root['urls'][0])
            by_url = {n['url']: n for n in flat}
            pools = {}
            for depth in [1, 2]:
                parents = [n for n in flat if n['depth'] == depth and not n['error']]
                allpool, top5pool = {}, {}
                for node in parents:
                    links = sorted(node['score'].get('link_scores', []), key=lambda l: l.get('score') or 0, reverse=True)
                    for k, link in enumerate(links):
                        value = link.get('score') or 0
                        u = link['url']
                        allpool[u] = max(allpool.get(u, -1), value)
                        if k < 5:
                            top5pool[u] = max(top5pool.get(u, -1), value)
                pools[depth] = (allpool, top5pool)
                corpus[f'depth{depth}_parents'] += len(parents)
                corpus[f'depth{depth}_candidate_links'] += len(allpool)
            hits = []
            for n in flat:
                corpus['nodes'] += 1
                corpus['failed_or_duplicate_nodes'] += bool(n['error'])
                ng = n['read'] and match(n['notes'], aliases)
                pg = (sid, n['url']) in raw_hits
                fg = (sid, n['url']) in full_hits
                if not (ng or pg or fg):
                    continue
                path = n['ancestors'] + [n['url']]
                edges = []
                for parent_url, child_url in zip(path, path[1:]):
                    parent = by_url[parent_url]
                    child = by_url[child_url]
                    links = sorted(parent['score'].get('link_scores', []), key=lambda l: l.get('score') or 0, reverse=True)
                    own = {l['url']: l.get('score') or 0 for l in links}
                    score = own.get(child_url, child['link_score'])
                    ap, tp = pools[parent['depth']]
                    global_score = tp.get(child_url)
                    edges.append({'parent': parent_url, 'child': child_url, 'parent_depth': parent['depth'],
                                  'score': score, 'local_rank': ranking(score, own),
                                  'top5_pool_rank': ranking(global_score, tp),
                                  'all_pool_rank': ranking(ap.get(child_url), ap),
                                  'parent_page_direct': parent['score'].get('direct_answer'),
                                  'parent_page_likelihood': parent['score'].get('answer_likelihood')})
                hit = {k: n[k] for k in ['url','depth','root_rank','root_url','read','error']}
                hit.update(search=si, search_id=sid, query=tree.get('query'), notes_gold=ng,
                           prefix_gold=pg, full_input_gold=fg, notes=n['notes'][:8000] if ng else '',
                           source_snippets=full_hits.get((sid,n['url']), raw_hits.get((sid,n['url']), [])),
                           edges=edges, page_direct=n['score'].get('direct_answer'),
                           page_likelihood=n['score'].get('answer_likelihood'))
                hits.append(hit)
                qs['hits'].append(hit)
            qs['searches'].append({'search': si, 'id': sid, 'roots': len(successful_roots),
                                   'successful_nodes': sum(not n['error'] for n in flat),
                                   'pools': {d: {'all': len(v[0]), 'top5': len(v[1])} for d,v in pools.items()}})
            corpus['searches'] += 1
        all_questions.append(qs)
        if pos % 50 == 0:
            print(f'Processed {pos}/300', flush=True)
    out = {'method': 'Lexical answer occurrences are candidates for human review, not verified answer-bearing pages. Rankings use observed parents only; ties retain best/worst intervals. Deduplicate pooled URLs by maximum score. No counterfactual fetches.',
           'corpus': dict(corpus), 'questions': all_questions}
    output.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Saved', output, flush=True)
    for q in all_questions:
        if q['correct']:
            hs = [h for h in q['hits'] if h['notes_gold']]
            print(q['qid'], q['gold'], 'notes',len(hs),'source-backed',sum(h['full_input_gold'] for h in hs),
                  'depths',dict(Counter(h['depth'] for h in hs)))


if __name__ == '__main__':
    main()
