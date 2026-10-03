"""Build an outcome-stratified diagnostic set, not an accuracy-estimation set."""
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261003
EXCLUDE = {3, 7, 8, 13, 15, 21, 22, 26, 27, 32}


def main():
    source = json.loads((ROOT / 'data/browsecomp/test.json').read_text(encoding='utf-8'))
    by_id = {int(row['index']): row for row in source}
    runs, partial = {}, {}
    for directory in sorted((ROOT / 'runs/test').glob('*browsecomp*')):
        path = directory / 'records.jsonl'
        if 'jevtree' in directory.name or not path.exists():
            continue
        rows = {int(e['index']): e for line in path.open(encoding='utf-8') if (e := json.loads(line))}
        (runs if len(rows) == 300 else partial)[directory.name] = rows
    valid = lambda e: not e.get('error') and not e.get('judge_error') and e.get('score') is not None
    universe = set(by_id) - EXCLUDE
    for rows in runs.values():
        universe &= {i for i, e in rows.items() if valid(e)}
    correct = {name: {i for i in universe if rows[i]['score'] == 1} for name, rows in runs.items()}
    ra_name = next(name for name in runs if '_ragent_' in name)
    o1_name = next(name for name in runs if '_search-o1_' in name)
    ds_names = [name for name in runs if '_depthsearch_' in name]
    intersection = set.intersection(*correct.values())
    union = set.union(*correct.values())
    ra, o1 = correct[ra_name], correct[o1_name]
    ds = set.union(*(correct[name] for name in ds_names))
    pools = {
        'all_correct': (intersection, 5),
        'ragent_yes_search_o1_no': (ra - o1, 1),
        'search_o1_yes_ragent_no': (o1 - ra, 1),
        'both_baselines_yes_some_ds_no': ((ra & o1) - intersection, 1),
        'only_ds_versions_yes': (ds - (ra | o1), 2),
    }
    rng = random.Random(SEED)
    groups = {group: sorted(rng.sample(sorted(pool), count)) for group, (pool, count) in pools.items()}
    ids = sorted(i for values in groups.values() for i in values)
    assert len(ids) == len(set(ids)) == 10 and not (set(ids) & EXCLUDE)
    for name in runs:
        for i in ids:
            response = json.loads((ROOT / 'runs/test' / name / f'q{i:05d}/response.json').read_text(encoding='utf-8'))
            assert response['question'] == by_id[i]['question'], (name, i, 'question mismatch')
            gold = by_id[i].get('gold_answer', by_id[i].get('answer'))
            assert response['gold_answer'] == gold, (name, i, 'gold mismatch')
    dataset = ROOT / 'data/browsecomp/test_diagnostic10.json'
    dataset.write_text(json.dumps([by_id[i] for i in ids], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    matrix = {name: {str(i): ('correct' if rows[i]['score'] == 1 else 'incorrect')
                       if i in rows and valid(rows[i]) else ('error' if i in rows else 'not_run')
                       for i in ids} for name, rows in {**runs, **partial}.items()}
    manifest = dict(purpose='Outcome-stratified comparative diagnosis; not population accuracy estimation',
                    seed=SEED, excluded_ids=sorted(EXCLUDE), eligible_count=len(universe),
                    intersection_ids=sorted(intersection), union_minus_intersection_ids=sorted(union-intersection),
                    groups=groups, selected_ids=ids, primary_runs=list(runs),
                    partial_runs_excluded_from_stratification={k: len(v) for k, v in partial.items()},
                    outcomes=matrix, question_gold_match_verified=True)
    (ROOT / 'analysis/jevtree_diagnostic10_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    labels = ['search-o1', 'RAgent', 'DS frozen', 'DS v3', 'DS v4', 'DS v6', 'DS v8']
    assert len(labels) == len(runs)
    lines = ['# JEV 비교 진단용 10문항', '',
             '300문항 완료 실행 7개 기준. 기존 JEV 10개 제외. 전원 정답 5개 + 일부 정답 5개.',
             f'고정 난수 seed={SEED}. 일부 정답은 RA만/o1만/두 baseline 모두/DS만으로 나눠 1/1/1/2개 추출.',
             'RA만/o1만은 두 베이스라인 사이의 구분이며 DS 정답 여부는 제한하지 않는다.',
             '전체 성능 추정용이 아니다. 짧은 실행의 미실행 문항은 오답으로 취급하지 않는다.', '',
             '| ID | 그룹 | ' + ' | '.join(labels) + ' |',
             '|---|---|' + '---|' * len(labels)]
    for i in ids:
        group = next(k for k, values in groups.items() if i in values)
        lines.append(f'| {i} | {group} | ' + ' | '.join('O' if matrix[name][str(i)] == 'correct' else 'X' for name in runs) + ' |')
    lines += ['', '실행별 정확한 경로와 짧은 실행의 추가 결과는 `jevtree_diagnostic10_manifest.json` 참조.',
              '실행 코드/프롬프트/reader/트리 설정은 변경하지 않았다.']
    (ROOT / 'analysis/jevtree_diagnostic10.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps(dict(groups=groups, intersection=len(intersection), some_correct=len(union-intersection), ids=ids)))


if __name__ == '__main__':
    main()
