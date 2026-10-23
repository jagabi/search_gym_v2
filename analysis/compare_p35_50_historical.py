"""Match all five requested historical settings to the exact latest fifty items."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RUNS=ROOT/'runs/test'
CURRENT=RUNS/'20261022-2100_jevtree_gpt-oss-20b_browsecomp_raw_browser_p35_unified_score_50'
NAMES={
    'DepthSearch ds_directed_v8':'20260924-0737_depthsearch_gpt-oss-20b_browsecomp_ds_directed_v8',
    'JevTree v66':'20261004-1329_jevtree_gpt-oss-20b_browsecomp_jevtree_v66_diagnostic10',
    'DepthSearch ds_answer_phase_v4':'20260922-0859_depthsearch_gpt-oss-20b_browsecomp_ds_answer_phase_v4',
    'search-o1 baseline':'20260919-1621_search-o1_gpt-oss-20b_browsecomp_paper_frozen_v1',
    'ragent baseline':'20260920-2130_ragent_gpt-oss-20b_browsecomp_paper_frozen_v1',
}
OUT=ROOT/'analysis/p35_50_historical_comparison';OUT.mkdir(exist_ok=True)
def records(run):
    rows=[json.loads(l) for l in (run/'records.jsonl').read_text(encoding='utf-8').split('\n') if l.strip()]
    assert len(rows)==len({r['index'] for r in rows})
    return {r['index']:r for r in rows}
current=records(CURRENT);ids=set(current);assert len(ids)==50
correct={q for q,r in current.items() if r['score']==1}
responses={q:json.loads((CURRENT/r['dir']/'response.json').read_text(encoding='utf-8')) for q,r in current.items()}
settings={};all_correct=set();matrix={q:{'index':q,'question':responses[q]['question'],
    'gold':responses[q]['gold_answer'],'p35':q in correct,'historical':{}} for q in sorted(ids)}
normalize=lambda text:' '.join(text.split())
for label,name in NAMES.items():
    run=RUNS/name;rows=records(run);assert ids<=rows.keys()
    cs={q for q in ids if rows[q]['score']==1};all_correct|=cs
    for q in sorted(ids):
        r=rows[q];response=json.loads((run/r['dir']/'response.json').read_text(encoding='utf-8'))
        assert normalize(response['question'])==normalize(responses[q]['question']),(label,q)
        matrix[q]['historical'][label]=q in cs
    settings[label]={'run':str(run),'matched':50,'correct_ids':sorted(cs),
        'total_correct_300':sum(r.get('score')==1 for r in rows.values()),
        'both_correct':sorted(cs&correct),'historical_only':sorted(cs-correct),
        'p35_only':sorted(correct-cs),'both_wrong':sorted(ids-(cs|correct)),
        'cached_in_50':sum(bool(rows[q].get('cached')) for q in ids),
        'judge_errors':[{k:rows[q].get(k) for k in ['index','score','judge_error']} for q in sorted(ids) if rows[q].get('judge_error')]}
result={'current_run':str(CURRENT),'matched':50,'p35_correct_ids':sorted(correct),'settings':settings,
        'p35_only_against_all_historical':sorted(correct-all_correct),
        'historical_any_correct_p35_wrong':sorted(all_correct-correct),
        'all_six_wrong':sorted(ids-(all_correct|correct)),'rows':list(matrix.values())}
(OUT/'comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# 기존 5개 설정과 최신 p35의 동일 50문항 비교','',
       '모든 실행의 문항 ID와 질문 본문을 공백 정규화하여 대조했다. 50개 모두 일치한다.',
       '표의 숫자는 실행 순서가 아닌 데이터셋 문항 ID다. p35 정답은8/50이다.','',
       '|기존 설정|기존 정답|공통 정답|기존만 정답|p35만 정답|둘 다 오답 수|',
       '|---|---:|---|---|---|---:|']
show=lambda values:', '.join(map(str,values)) or '없음'
for label,s in settings.items():
    lines.append(f'|{label}|{len(s["correct_ids"])}/50|{show(s["both_correct"])}|{show(s["historical_only"])}|{show(s["p35_only"])}|{len(s["both_wrong"])}|')
lines+=['','기존5개 설정 중 어느 것도 못 맞히고p35만 맞힌 문항: '+show(result['p35_only_against_all_historical']),
        '기존 중 하나 이상이 맞혔지만p35가 틀린 문항: '+show(result['historical_any_correct_p35_wrong']),
        '모든6개 설정이 틀린 문항: '+show(result['all_six_wrong']),'',
        'v66의 해당50문항은 전부 캐시 결과다. ds_answer_phase_v4의15번은 empty_response 실패이며 기록상0점으로 분류했다.','',
        '## 정답이 하나라도 있는 문항','',
        '|ID|정답|ds_directed_v8|v66|ds_answer_phase_v4|search-o1|ragent|최신 p35|',
        '|---|---|:---:|:---:|:---:|:---:|:---:|:---:|']
for q,row in matrix.items():
    if q not in all_correct|correct:continue
    marks=['O' if row['historical'][label] else 'X' for label in NAMES]+['O' if row['p35'] else 'X']
    lines.append('|'+str(q)+'|'+str(row['gold']).replace('|','/')+'|'+'|'.join(marks)+'|')
lines+=['','## 실행 경로','',str(CURRENT),'']+[f'{label}: {RUNS/name}' for label,name in NAMES.items()]
(OUT/'comparison.md').write_text('\n'.join(lines),encoding='utf-8')
print('MATCHED_AND_QUESTION_VERIFIED',50)
print('CURRENT',sorted(correct))
print('LATEST_UNIQUE',result['p35_only_against_all_historical'])
print('LOST_AGAINST_ANY',result['historical_any_correct_p35_wrong'])
print('ALL_SIX_WRONG',result['all_six_wrong'])
for label,s in settings.items():print(label,{k:v for k,v in s.items() if k not in ['run','both_wrong']})
for q,row in matrix.items():
    if q in correct-all_correct or q in all_correct-correct:print('FOCUS_ITEM',q,row['gold'])
