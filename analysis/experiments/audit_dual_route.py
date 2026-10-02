"""Offline route isolation/accounting audit; no model or tool execution."""
import argparse
import json
from pathlib import Path


def rows(path):
    return [json.loads(s) for s in path.read_text(encoding='utf-8').split('\n') if s]


def audit(run):
    cases = []
    for record in rows(run / 'records.jsonl'):
        route = 'A'
        data = {'index': record['index'], 'accuracy': record['accuracy'],
                'queries': {'A': [], 'B': []}, 'reads': {'A': 0, 'B': 0},
                'recursive_returns': {'A': 0, 'B': 0}}
        for e in rows(run / record['dir'] / 'trace.jsonl'):
            if e['event'] == 'research.route_switch':
                route = 'B'
                data['switch_at_search'] = e['searches_used']
                data['route_a_draft'] = e.get('route_a_draft', '')
            if e['event'] == 'tool.result' and e.get('tool') == 'web_search':
                data['queries'][route].append(e['arguments'].get('query', ''))
            if e['event'] == 'search.selected_result' and not e.get('is_error'):
                data['reads'][route] += 1
            if e['event'] == 'expand.return':
                data['recursive_returns'][route] += 1
        cases.append(data)
    return {'run': str(run), 'cases': cases}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('run', type=Path); p.add_argument('--out', type=Path)
    a = p.parse_args(); result = audit(a.run)
    if a.out:
        a.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print([(r['index'], r['accuracy'], {k: len(v) for k, v in r['queries'].items()})
           for r in result['cases']])
