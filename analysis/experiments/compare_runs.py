"""Read-only matched-question experiment accounting; no model/web/judge calls."""
import argparse
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'runs/test'
PATTERNS = {
    'RAgent': '*ragent*browsecomp*paper_frozen_v1',
    'search-o1': '*search-o1*browsecomp*paper_frozen_v1',
    'DS v4': '*ds_answer_phase_v4',
    'DS v8': '*ds_directed_v8',
    'DS v9': '20260925-1231*ds_batch_v9-2',
    'DS v12': '*ds_links_v12_b',
    'DS v13': '*ds_access_v13_b',
    'DS v14': '*ds_handoff_v14_b',
    'DS v10': '20260925-1337*ds_batch_v9',
}

def records(path):
    rows = {}
    for line in (path/'records.jsonl').read_text(encoding='utf-8').split('\n'):
        if line.strip():
            row = json.loads(line)
            rows[row['index']] = row
    return rows

def compare(target):
    current = records(target)
    ids = set(current)
    paths = {label: next(BASE.glob(pattern)) for label, pattern in PATTERNS.items()}
    paths['current'] = target
    out = {'target': str(target), 'ids': sorted(ids), 'runs': {}}
    for label, path in paths.items():
        source = records(path)
        rows = [source[i] for i in sorted(ids & source.keys())]
        if not rows:
            continue
        stats = {'path': str(path), 'n': len(rows), 'correct': sum(r['accuracy'] for r in rows),
                 'median_s': statistics.median(r['latency_s'] for r in rows),
                 'errors': sum(bool(r.get('error') or r.get('judge_error')) for r in rows),
                 'correct_ids': [r['index'] for r in rows if r['accuracy']],
                 'current_only_correct': [r['index'] for r in rows if current[r['index']]['accuracy'] and not r['accuracy']],
                 'other_only_correct': [r['index'] for r in rows if not current[r['index']]['accuracy'] and r['accuracy']]}
        for key in ['llm_calls','input_tokens','output_tokens','searches','auto_fetches','expansion_nodes']:
            stats[key] = sum(r.get(key,0) for r in rows)
        stats['control'] = {}
        for row in rows:
            for key, value in row.get('control_stats',{}).items():
                stats['control'][key] = stats['control'].get(key,0) + value
        out['runs'][label] = stats
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('run');parser.add_argument('--out')
    args=parser.parse_args();path=Path(args.run)
    if not path.is_absolute():path=ROOT/path
    data=compare(path)
    print('| Method | Correct/n | Calls | Input | Output | Median seconds |')
    print('|---|---:|---:|---:|---:|---:|')
    for label,r in data['runs'].items():
        print(f"| {label} | {r['correct']:g}/{r['n']} | {r['llm_calls']:,} | {r['input_tokens']:,} | {r['output_tokens']:,} | {r['median_s']:.1f} |")
    if args.out:
        Path(args.out).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
