"""Match the completed p35 fifty questions to the frozen search-o1 baseline."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CURRENT=ROOT/'runs/test/20261022-2100_jevtree_gpt-oss-20b_browsecomp_raw_browser_p35_unified_score_50'
BASELINE=ROOT/'runs/test/20260919-1621_search-o1_gpt-oss-20b_browsecomp_paper_frozen_v1'
OUT=ROOT/'analysis/p35_50_comparison';OUT.mkdir(exist_ok=True)
def read_records(run):
    return [json.loads(l) for l in (run/'records.jsonl').read_text(encoding='utf-8').split('\n') if l.strip()]
current=read_records(CURRENT);baseline={r['index']:r for r in read_records(BASELINE)}
assert len(current)==len({r['index'] for r in current})==50
groups={'both_correct':[],'search_o1_only':[],'jevtree_only':[],'both_wrong':[]}
rows=[];mismatches=[]
for c in current:
    b=baseline[c['index']]
    assert c.get('judge_error') is None and b.get('judge_error') is None
    assert c['score'] in (0,1) and b['score'] in (0,1)
    cr=json.loads((CURRENT/c['dir']/'response.json').read_text(encoding='utf-8'))
    br=json.loads((BASELINE/b['dir']/'response.json').read_text(encoding='utf-8'))
    normalize=lambda t:' '.join(t.split())
    if normalize(cr['question'])!=normalize(br['question']):mismatches.append(c['index'])
    group=('both_correct' if c['score']==b['score']==1 else 'search_o1_only' if b['score']==1 else
           'jevtree_only' if c['score']==1 else 'both_wrong')
    groups[group].append(c['index'])
    rows.append({'index':c['index'],'group':group,'question':cr['question'],'gold':cr['gold_answer'],
                 'search_o1_score':b['score'],'jevtree_score':c['score'],
                 'search_o1_answer':br['answer'],'jevtree_answer':cr['answer'],
                 'search_o1_response':str(BASELINE/b['dir']/'response.json'),
                 'jevtree_response':str(CURRENT/c['dir']/'response.json')})
assert not mismatches, mismatches
result={'jevtree_run':str(CURRENT),'search_o1_run':str(BASELINE),'matched':50,'question_mismatches':mismatches,
        'groups':groups,'search_o1_correct':sum(r['search_o1_score'] for r in rows),
        'jevtree_correct':sum(r['jevtree_score'] for r in rows),'rows':rows}
(OUT/'comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
labels={'both_correct':'둘 다 정답','search_o1_only':'search-o1만 정답','jevtree_only':'jevtree만 정답','both_wrong':'둘 다 오답'}
lines=['# 동일 50문항: search-o1 대 p35 jevtree','',
       '기준 jevtree: '+CURRENT.name,'기준 search-o1: '+BASELINE.name,'',
       '문항 ID 50개 모두 일치하고, 질문 본문도 공백 정규화 후 모두 같다. 두 실행 모두 해당 문항들의 채점 오류는 없다.',
       'search-o1은 전체300개 중 이번50개 ID에 해당하는 결과만 추렸다.','','|분류|개수|문항 ID|','|---|---:|---|']
for group,ids in groups.items():lines.append(f'|{labels[group]}|{len(ids)}|'+', '.join(map(str,ids))+'|')
lines+=['','search-o1:5/50(10%). jevtree:8/50(16%). 정답 합집합:9/50(18%).','',
        '## 서로 다른 결과와 공통 정답','', '|ID|분류|정답|질문|','|---|---|---|---|']
for r in rows:
    if r['group']=='both_wrong':continue
    clean=lambda s:str(s).replace('|','/').replace('\n',' ')
    lines.append(f'|{r["index"]}|{labels[r["group"]]}|{clean(r["gold"])}|{clean(r["question"])}|')
lines+=['','## 전체50개','', '|ID|search-o1|jevtree|분류|','|---|:---:|:---:|---|']
for r in rows:lines.append(f'|{r["index"]}|{"O" if r["search_o1_score"] else "X"}|{"O" if r["jevtree_score"] else "X"}|{labels[r["group"]]}|')
(OUT/'comparison.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},ensure_ascii=False,indent=2))
for r in rows:
    if r['group']!='both_wrong':print('ITEM',r['index'],labels[r['group']],'GOLD',r['gold'])
