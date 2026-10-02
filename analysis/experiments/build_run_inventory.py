"""Offline inventory from saved records; never invokes models, retrieval or judges."""
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def inventory():
    output = []
    for run in sorted((ROOT/'runs/test').iterdir()):
        if not run.is_dir():
            continue
        config = json.loads((run/'config.json').read_text(encoding='utf-8')) if (run/'config.json').exists() else {}
        records = {}
        if (run/'records.jsonl').exists():
            for line in (run/'records.jsonl').read_text(encoding='utf-8').split('\n'):
                if line.strip():
                    row = json.loads(line)
                    records[row['index']] = row
        rows = list(records.values())
        output.append({'run':run.relative_to(ROOT).as_posix(), 'n':len(rows),
            'requested_items':config.get('items'), 'method':config.get('method'), 'model':config.get('model'),
            'dataset':config.get('dataset'), 'judge':config.get('judge'),
            'f1':sum(r.get('f1',0) for r in rows)/len(rows) if rows else None,
            'correct':sum(r.get('accuracy',0) for r in rows),
            'zero':sum(r.get('f1',0)==0 for r in rows),
            'partial':sum(0<r.get('f1',0)<1 for r in rows),
            'full':sum(r.get('f1',0)==1 for r in rows),
            'calls':sum(r.get('llm_calls',0) for r in rows),
            'input_tokens':sum(r.get('input_tokens',0) for r in rows),
            'output_tokens':sum(r.get('output_tokens',0) for r in rows),
            'median_s':statistics.median(r['latency_s'] for r in rows) if rows else None,
            'ids':sorted(records),
            'controls':{k:config.get('agent',{}).get(k) for k in (
                'max_searches','search_results','search_top_k','fetch_max_tokens','max_turns')}})
    return output


if __name__ == '__main__':
    rows = inventory()
    out = ROOT/'analysis/experiments/run_inventory.json'
    out.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(rows)} run directories, {sum(bool(r["n"]) for r in rows)} with completed records; saved {out}')
