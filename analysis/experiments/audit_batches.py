"""Offline batch/recursion accounting. Trace records are delimited by LF, not Unicode line breaks."""
import argparse
from collections import Counter
import json
from pathlib import Path


def rows(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').split('\n') if line.strip()]


def audit(run):
    output = {'run': str(run), 'cases': [], 'totals': {}}
    totals = Counter()
    for record in rows(run / 'records.jsonl'):
        trace = rows(run / record['dir'] / 'trace.jsonl')
        counts = Counter()
        batches = {}
        recovery_turns = set()
        recovered_turns = set()
        for event in trace:
            kind = event['event']
            if kind == 'search.batch_plan':
                counts['selection_rounds'] += 1
                counts['selected_slots'] += len(event['sources'])
                if len(event['sources']) > 1:
                    counts['multi_root_rounds'] += 1
                if not event['sources']:
                    counts['empty_plans'] += 1
                batches.setdefault(event['turn'], []).append(event)
            elif kind == 'search.entry_access_recovery':
                counts['access_recovery_rounds'] += 1
                recovery_turns.add(event['turn'])
            elif kind == 'search.selected_result':
                counts['failed_root_fetches' if event['is_error'] else 'successful_root_fetches'] += 1
                if event['turn'] in recovery_turns:
                    counts['recovery_failed_fetches' if event['is_error'] else 'recovery_successful_fetches'] += 1
                    if not event['is_error']:
                        recovered_turns.add(event['turn'])
            elif kind == 'explorer.access_only':
                counts['access_screen_notes'] += 1
            elif kind == 'expand.return':
                counts['recursive_returns'] += 1
                counts['recursive_' + event['status']] += 1
            elif kind == 'expand.failed':
                counts['recursive_access_failures'] += 1
        for turn in batches:
            results = [e for e in trace if e['event'] == 'search.selected_result' and e['turn'] == turn]
            if results and all(e['is_error'] for e in results):
                counts['all_access_failed_batches'] += 1
        counts['search_batches'] = len(batches)
        counts['recovery_batches_with_opened_page'] = len(recovered_turns)
        totals.update(counts)
        output['cases'].append({'index': record['index'], 'accuracy': record['accuracy'],
            'calls': record['llm_calls'], 'nodes_by_depth': record['nodes_by_depth'], **counts})
    output['totals'] = dict(totals)
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('run', type=Path)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = audit(args.run)
    print(json.dumps(result['totals'], indent=2))
    if args.out:
        args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
