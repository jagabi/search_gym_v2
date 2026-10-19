"""Extract compact, reproducible source-reachability evidence from the p11 run."""
import json
from pathlib import Path
from inspect_run import events, read

RUN = Path('runs/test/20261019-1506_jevtree_gpt-oss-20b_browsecomp_raw_browser_p11_beam10')
OUT = Path('analysis/audit_20261019-1506/reachability.json')
TERMS = {
    57: ['PMC7227421', '1685381'],
    516: ['Peter_Nzioki', 'Peter Nzioki', 'fullcredits'],
    598: ['RRS_10_2013', 'Jaba', 'paperzz.com/doc/7110186'],
    746: ['rockefeller', '42561966', 'chelminski'],
    1230: ['mumbai', 'Regal_Cinema'],
}


def match(value, terms):
    return any(t.lower() in value.lower() for t in terms)


def walk(node, path=()):
    path = (*path, node['urls'][0])
    yield node, path
    for child in node.get('opened', []):
        yield from walk(child, path)


def main():
    result = []
    for q, terms in TERMS.items():
        folder = RUN / f'q{q:05d}'
        response = read(folder / 'response.json')
        row = {'question': q, 'search_leads': [], 'nodes': [], 'links': [], 'fetches': []}
        for step in response['steps']:
            for call in step.get('tool_calls', []):
                if call['name'] != 'web_search':
                    continue
                try:
                    payload, _ = json.JSONDecoder().raw_decode(call.get('result', ''))
                except ValueError:
                    continue
                for rank, item in enumerate(payload.get('organic', []), 1):
                    if match(json.dumps(item, ensure_ascii=False), terms):
                        row['search_leads'].append({'turn': step['turn'], 'rank': rank,
                            'query': call['arguments']['query'], **item})
        for tree in read(folder / 'explorer.json'):
            for node, path in walk(tree):
                if match(node['urls'][0], terms):
                    row['nodes'].append({'path': path, **{k: node.get(k) for k in
                        ['node_id', 'depth', 'direct_answer', 'query_answer', 'read', 'error']}})
        nodes = {}
        for event in events(folder / 'trace.jsonl'):
            name = event['event']
            if name == 'rawtree.preview':
                nodes[event['search_id'], event['node_id']] = event['url']
            elif name == 'rawtree.links':
                links = sorted((x for x in event['links'] if x.get('score') is not None),
                               key=lambda x: (-x['score'], x['url']))
                for rank, link in enumerate(links, 1):
                    if match(link['url'] + ' ' + link['anchor'], terms):
                        row['links'].append({'search_id': event['search_id'],
                            'parent': nodes.get((event['search_id'], event['node_id'])),
                            'parent_rank': rank, **link,
                            'top_two': [{'url': x['url'], 'score': x['score']} for x in links[:2]]})
            elif name == 'fetch.raw' and match(event['url'], terms):
                row['fetches'].append({'url': event['url'], 'is_error': event['is_error'],
                    'minute': round(event['elapsed_ms']/60000, 2),
                    'chars': len(event['content']), 'lead': event['content'][:350]})
        result.append(row)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps([{'question': r['question'], **{k: len(r[k]) for k in
        ['search_leads', 'nodes', 'links', 'fetches']}} for r in result]))


if __name__ == '__main__':
    main()
