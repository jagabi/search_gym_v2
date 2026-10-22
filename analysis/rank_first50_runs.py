"""Compare completed BrowseComp runs using the first 50 distinct question indices."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rows = []
for folder in (ROOT/'runs/test').iterdir():
    records = folder/'records.jsonl'
    if not folder.is_dir() or 'browsecomp' not in folder.name or not records.exists():
        continue
    by_index = {}
    for line in records.read_text(encoding='utf-8').splitlines():
        if line.strip():
            item = json.loads(line)
            by_index[item['index']] = item
    if len(by_index) < 50:
        continue
    ordered = sorted(by_index.values(), key=lambda r: r['index'])
    first = ordered[:50]
    config = json.loads((folder/'config.json').read_text(encoding='utf-8')) if (folder/'config.json').exists() else {}
    row = {'run': folder.name, 'completed': len(ordered),
           'correct50': sum(r.get('score', 0) == 1 for r in first),
           'score50': sum(r.get('score', 0) or 0 for r in first),
           'first50_indices': [r['index'] for r in first],
           'total_correct': sum(r.get('score', 0) == 1 for r in ordered),
           'mean_latency50_s': sum(r.get('latency_s', 0) or 0 for r in first)/50,
           'mean_searches50': sum(r.get('searches', 0) or 0 for r in first)/50,
           'errors50': sum(bool(r.get('error')) for r in first),
           'judge_errors50': sum(bool(r.get('judge_error')) for r in first),
           'config_keys': list(config)}
    rows.append(row)
rows.sort(key=lambda r: (-r['correct50'], r['run']))
(ROOT/'analysis/first50_run_ranking.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
for row in rows:
    print(json.dumps({k:v for k,v in row.items() if k not in ('first50_indices', 'config_keys')}, ensure_ascii=False))
dataset = json.loads((ROOT/'data/browsecomp/test.json').read_text(encoding='utf-8'))
expected = [item['index'] for item in dataset[:50]]
print('ALL_MATCH_DATASET_FIRST50', all(r['first50_indices'] == expected for r in rows))
for row in rows[:2]:
    items = [json.loads(s) for s in (ROOT/'runs/test'/row['run']/'records.jsonl').read_text(encoding='utf-8').splitlines()]
    by_index = {item['index']: item for item in items}
    print('WINNER_AUDIT', row['run'], 'correct_indices', [i for i in expected if by_index[i]['score'] == 1],
          'first50_cache_hits', sum(bool(by_index[i].get('cached')) for i in expected))
