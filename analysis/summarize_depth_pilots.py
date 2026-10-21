"""Summarize observed pilot outputs; expected facts never enter model inputs."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOTS = ROOT/'analysis/pilots'
CASES = ['direct','route','siblings','article','tailroute','nobel']
EXPECTED = {
    'direct': ['April 2, 2024'], 'siblings': ['April 2, 2024'],
    'route': ['Zac Hatfield-Dodds','20-Dec-2021'],
    'article': ['Zac Hatfield-Dodds','20-Dec-2021'],
    'tailroute': ['Taneli Hukkinen','Shantanu Jain','01-Jan-2022'],
    'nobel': ['14 March 1879','Ulm'],
}
rows=[]
for case in CASES:
    before='p17_baseline' if case in CASES[:4] else 'p17_holdout'
    for stage in [before,'p18_final']:
        folder=PILOTS/stage
        report=json.loads((folder/f'{case}.summary.json').read_text(encoding='utf-8'))
        events=[json.loads(s) for s in (folder/f'{case}.jsonl').read_text(encoding='utf-8').splitlines()]
        returned=next(r for r in events if r['event']=='rawtree.return')
        # Inspect selected original evidence, excluding notices and search leads.
        evidence='\n'.join(text for item in returned['returned'] for text in item['texts'].values())
        rows.append(dict(stage=stage,case=case,expected_fact_checks={v:v in evidence for v in EXPECTED[case]},
                         complete=all(v in evidence for v in EXPECTED[case]),
                         seconds=round(report['seconds'],2),pages=report['stats']['page_visits'],
                         depth=report['stats']['max_depth'],reads=report['stats']['reads'],
                         d3_calls=report['stats']['jev_requests'],d3_tokens=report['stats']['jev_input_tokens'],
                         live_fetches=sum(not r['cached'] for r in report['fetches']),
                         failures=report['stats']['jev_failures']+report['stats']['fetch_failed']))
(PILOTS/'comparison.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
for row in rows:
    print(json.dumps(row,ensure_ascii=True))

labels=dict(direct='배포일 직접 확인',route='목차 → 설명 → PEP 678',siblings='무관한 형제 페이지 포함',
            article='설명 → PEP 678',tailroute='설명 → PEP 680',nobel='Nobel 수상자 → 인물 사실')
lines=[
    '# Jina·d3 경로 파일럿 결과 — 2026-10-21', '',
    '환경: conda `search`, Python 3.11.17 (Windows x64). 실제 Jina 16개 문서를 수집했고, '
    '반복 비교에서는 저장 본문을 재사용했다. d3 판단은 매번 실제 서버에 새로 요청했다. '
    '메인 추론모델·정답 판정모델·Serper 검색은 호출하지 않았다.', '',
    '고정 URL 진입점으로 6개 시나리오(서로 다른 질문은 4개)를 비교했다. '
    '검색 순위·진입점 선별 효과를 분리하기 위해 파일럿에서만 entry ranking을 껐다. '
    '예상 사실은 출력 검사에만 사용했고 d3 입력에는 주지 않았다. '
    '여기서 성공은 요청한 사실이 선택된 원문 청크에 포함됐다는 뜻이며, '
    'BrowseComp 정답률이나 메인모델의 최종 답변 성공률이 아니다.', '',
    '| 사례 | 필요한 근거: p17→p18 | 방문 수 | 최대 depth | 실제 문서 읽기 | d3 HTTP 호출 |',
    '|---|---|---|---|---|---|',
]
for case in CASES:
    a,b=[r for r in rows if r['case']==case]
    pair=lambda key:f"{a[key]}→{b[key]}"
    lines.append(f"| {labels[case]} | {'충족' if a['complete'] else '누락'}→{'충족' if b['complete'] else '누락'} | "
                 f"{pair('pages')} | {pair('depth')} | {pair('reads')} | {pair('d3_calls')} |")
lines += ['', '실행 시간과 입력량도 함께 남긴다. p17에는 실제 Jina 수집 시간이 섞였고 '
          'p18 최종 비교는 모두 저장 본문이다. 서버 부하도 통제하지 않았으므로 '
          '아래 시간을 동일 조건의 속도 향상률로 해석하면 안 된다.', '',
          '| 사례 | p17 초 | p18 초 | p17 d3 입력 토큰 | p18 d3 입력 토큰 |',
          '|---|---:|---:|---:|---:|']
for case in CASES:
    a,b=[r for r in rows if r['case']==case]
    lines.append(f"| {labels[case]} | {a['seconds']} | {b['seconds']} | {a['d3_tokens']:,} | {b['d3_tokens']:,} |")
lines += ['',
    '실제 실패: p17은 목차에서 depth 3의 PEP 원문까지 도달했지만, 저자 이름을 담은 '
    '설명 문서를 읽은 뒤 PEP 원문은 RETURN으로 닫았다. 원문 첫머리에 작성일이 있었음에도 '
    '반환 근거에는 빠졌다. 이미 확보한 이름 때문에 아직 필요한 다른 속성을 새 근거로 '
    '충분히 평가하지 못했다는 가설이다. 내부 모델의 사고를 관찰한 결과는 아니다.', '',
    '프롬프트를 늘린 1·2차 수정은 같은 저장 입력에서 실패했다. 읽기 기준을 짧게 바꾼 '
    '3차 수정은 동일 입력의 읽기 점수를 약 0.41에서 0.88로 올려 RETURN 0.75보다 높였다. '
    '전체 경로 재실행에서는 두 번 읽어 작성일까지 확보했다. 이후 URL 대응표와 확장 순서를 '
    '함께 수정하자 설명 문서 읽기를 미루고 원문을 한 번만 읽는 경로가 나왔다. '
    '각 수정의 독립적인 기여도까지 분리해 측정한 것은 아니다.', '',
    '반영한 구조 변경:', '',
    '- READ 요청이 하나라도 있으면 무조건 먼저 읽던 순서를 고쳤다. 더 높은 EXPAND 제안이 있으면 먼저 자식 후보를 연다.',
    '- 마지막 읽기 슬롯은 읽고 현재 검색을 끝내는 선택임을 d3에 알려준다. 사용 뒤에는 가짜 RETURN 재판정을 만들지 않는다.',
    '- 번호로 가린 링크의 실제 목적지 URL을 간결한 대응표로 함께 제공한다.',
    '- 선택된 원문 청크에서 새 링크가 관찰되면 기존 확장 입력에 합친다. 읽지 않은 본문 전체의 링크는 훑지 않는다.',
    '- 최소 한 번 읽는 보완 동작을 종료 직전에서 경로 판단 안으로 옮겼다. 새 관찰이 생기면 그 출처의 경로를 다시 평가한다.',
    '- 방문 예산을 소진한 뒤 과거 링크가 EXPAND 후보로 남아 읽기를 가로막던 경계도 막았다.', '',
    '검증: RawTree 오프라인 회귀검사 79개 통과. 확장이 형제 읽기에 선점되는 경우, '
    '첫 읽기 뒤 depth 3까지 들어가는 경우, 앞부분 밖 링크가 선택 청크에서 발견되는 경우, '
    '형제 RETURN·마지막 슬롯·부분 실패·방문 예산·HTTP wave 경계를 포함한다. '
    '새로 추가한 순서·청크 링크 회귀는 p17에서 실패함도 확인했다. '
    '선택 청크 뒤쪽 링크 연결 자체는 합성 그래프 검증이며 실제 웹에서 해당 패턴을 '
    '검증했다고 주장하지 않는다. `tailroute`라는 파일럿 이름의 PEP 680 링크는 '
    '실제 수집 본문의 최초 관찰 범위에도 있었으므로 뒤쪽 링크 성공 사례로 세지 않는다.', '',
    '남은 한계: d3의 행동별 점수는 보정된 공동 확률이 아니므로 잘못된 읽기·확장 선택은 '
    '여전히 가능하다. 앞부분과 선별 청크 사이의 미관찰 근거도 놓칠 수 있다. '
    '읽기가 세 번 필요한 경로는 두 번 예산으로 보장할 수 없다. 목적지 대응표가 '
    '입력량을 늘려 쉬운 사례나 PEP 680 사례는 비용상 이득이 없다. '
    '기존 10문항의 누락 진입점, 접근 실패, 메인모델 오판이 해결됐다는 증거도 없다.', '',
    '재현:', '', '```cmd', 'conda activate search',
    'python analysis/pilot_depth_routes.py --label p18_recheck --cases direct route siblings article tailroute nobel',
    'python -m unittest discover -s tests -p "test_rawtree*.py"', '```', '',
    '본문을 실제 Jina에서 다시 받으려면 파일럿 명령에 `--fresh`를 붙인다. '
    '기존 코드 비교는 `--baseline`을 사용하되, 이는 실행 시점 Git HEAD의 rawtree 코드다. '
    '수정본이 커밋된 뒤에도 p17이 선택된다는 뜻은 아니다.', '',
    '서버 10문항 명령(이번 작업에서 실행하지 않음):', '', '```cmd',
    'python test.py --method jevtree --model gpt-oss --benchmark browsecomp --path data/browsecomp/test_diagnostic10.json --split test --limit 10 --tag raw_browser_p18_pilot --expect-raw-traversal beam --no-cache',
    '```', '',
    '원시 기록은 `analysis/pilots/`에 있다. `p17_baseline`, `p17_holdout`은 기존 코드, '
    '`p18_prompt`는 프롬프트 수정 단계, `p18_structural`·`p18_holdout`은 중간 구조 수정, '
    '`p18_final`은 최종 코드다. 최종 summary에는 rawtree 코드 SHA256도 저장했다. '
    '`pep_prompt_r1.jsonl`~`pep_prompt_r3.jsonl`은 실패를 포함한 동일 입력 재판정 기록이다.',
]
(ROOT/'analysis/depth_pilot_findings_20261021.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
