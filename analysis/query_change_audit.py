"""Offline query overlap audit; no model calls or application changes."""
import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = {
    'jev': '20261004-1329_jevtree_gpt-oss-20b_browsecomp_jevtree_v66_diagnostic10',
    'search_o1': '20260919-1621_search-o1_gpt-oss-20b_browsecomp_paper_frozen_v1',
}
STOP = set('a an the of in on at for to and or is was were are by with from who what which when where how as that this it its be been'.split())


def tokens(q):
    return set(re.findall(r'\w+', q.casefold())) - STOP


def overlap(a, b):
    return len(a & b) / len(a | b) if a | b else 1.0


def normalized(q):
    return ' '.join(re.findall(r'\w+', q.casefold()))


def stats(pairs):
    n = len(pairs)
    return {
        'transitions': n,
        'mean_jaccard': statistics.mean(p['jaccard'] for p in pairs) if n else None,
        'median_jaccard': statistics.median(p['jaccard'] for p in pairs) if n else None,
        'bins': {name: sum(lo <= p['jaccard'] < hi for p in pairs) for name, lo, hi in [
            ('below_0.2', 0, .2), ('0.2_to_0.4', .2, .4), ('0.4_to_0.6', .4, .6),
            ('0.6_to_0.8', .6, .8), ('0.8_plus', .8, 1.01)]},
        'normalized_exact_repeat_previous': sum(p['exact_previous'] for p in pairs),
        'same_words_previous': sum(p['same_words'] for p in pairs),
        'same_nonnumeric_words_previous': sum(p['same_nonnumeric'] for p in pairs),
        'mean_previous_word_retention': statistics.mean(p['retention'] for p in pairs) if n else None,
        'mean_new_word_fraction': statistics.mean(p['new_fraction'] for p in pairs) if n else None,
        'similar_to_any_earlier_0.6': sum(p['max_prior_jaccard'] >= .6 for p in pairs),
        'exact_repeat_any_earlier': sum(p['exact_any_prior'] for p in pairs),
    }


def main():
    result = {}
    for name, run in RUNS.items():
        path = ROOT / 'runs/test' / run
        records = {r['index']: r for r in map(json.loads, (path/'records.jsonl').read_text(encoding='utf-8').splitlines())}
        rows, pairs = [], []
        for qid, rec in records.items():
            response = json.loads((path/rec['dir']/'response.json').read_text(encoding='utf-8'))
            queries = []
            for step in response['steps']:
                for c in step.get('tool_calls', []):
                    if c.get('name') != 'web_search' or c.get('refused'):
                        continue
                    args = c.get('arguments', {})
                    if isinstance(args, str):
                        args = json.loads(args)
                    if isinstance(args.get('query'), str):
                        queries.append(args['query'])
            sets = [tokens(q) for q in queries]
            local = []
            for i in range(1, len(queries)):
                a, b = sets[i-1:i+1]
                pair = {
                    'qid': qid, 'search_number': i+1, 'correct': bool(rec['accuracy']),
                    'previous': queries[i-1], 'query': queries[i], 'jaccard': overlap(a, b),
                    'retention': len(a & b)/len(a) if a else 0,
                    'new_fraction': len(b-a)/len(b) if b else 0,
                    'same_words': a == b,
                    'same_nonnumeric': {w for w in a if not w.isnumeric()} == {w for w in b if not w.isnumeric()},
                    'exact_previous': normalized(queries[i-1]) == normalized(queries[i]),
                    'exact_any_prior': normalized(queries[i]) in [normalized(q) for q in queries[:i]],
                    'max_prior_jaccard': max(overlap(b, old) for old in sets[:i]),
                }
                local.append(pair)
            pairs.extend(local)
            rows.append({'qid': qid, 'correct': bool(rec['accuracy']), 'question': response['question'],
                         'gold': response['gold_answer'], 'queries': queries,
                         'mean_jaccard': statistics.mean(p['jaccard'] for p in local) if local else None,
                         'high_overlap_transitions': sum(p['jaccard'] >= .6 for p in local)})
        summary = stats(pairs)
        summary.update({'questions': len(rows), 'queries': sum(len(r['queries']) for r in rows),
                        'questions_with_high_overlap': sum(r['high_overlap_transitions'] > 0 for r in rows),
                        'questions_with_3_high_overlap': sum(r['high_overlap_transitions'] >= 3 for r in rows)})
        result[name] = {'summary': summary,
                        'by_correct': {str(c): stats([p for p in pairs if p['correct'] == c]) for c in [True, False]},
                        'by_search_number': {str(i): stats([p for p in pairs if p['search_number'] == i]) for i in range(2, 11)},
                        'questions': rows, 'transitions': pairs}
    result['method'] = 'Word-set Jaccard after lowercasing, punctuation removal and English stopword removal; no semantic classification. Search calls exclude refused calls. Attempts with retrieval errors are retained.'
    out = ROOT/'analysis/query_change_audit.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: {'summary': v['summary'], 'by_correct': v['by_correct'], 'by_search_mean': {i: x['mean_jaccard'] for i,x in v['by_search_number'].items()}} for k,v in result.items() if k != 'method'}, indent=2))


if __name__ == '__main__':
    main()
