# DS selective entry — 구현 및 실행

## 적용 범위

`configs/depthsearch.yaml`의 `agent.depthsearch_control: true`로 활성화한다.
RAgent/search-o1 실행 경로와 설정은 그대로이며, 비활성 상태의 기존 agent 설정
fingerprint도 유지한다. 새 DS 캐시 버전은 `agent/41-ds-answer-phase`다.

검색 한도 10회, 검색 결과 수 10, 재귀 깊이 3, 전체 확장 노드 12,
루트별 확장 노드 6, 자식 수 2, 메인 40턴은 변경하지 않았다.
계산기 등 새로운 외부 도구는 추가하지 않았다.

## 실행 순서

1. 검색 결과를 기존 오염 필터에 통과시키고 각 실제 URL에 S1, S2 등의 ID를 부여한다.
2. 같은 모델에 질문·검색 결과·출처에 연결된 후보 상태를 제공한다. 긴 메인 추론
   이력은 이 선택 요청에 넣지 않는다. `web_fetch(url)` 하나만 제공하며 tool_choice는
   auto다. 페이지를 읽으려면 호출하고, 필요 없으면 짧은 일반 응답으로 종료한다.
3. 한 개의 유효한 호출이면 미방문 출처에 등록된 정확한 URL을 열고 기존 explorer
   재귀를 수행한다. 선택 단계에는 후보 갱신 JSON이나 추가 자유 텍스트 인자가 없다.
4. 페이지별 노트와 보존된 구조화 원문에서 후보 상태와 잠정 답을 갱신한다.
5. 메인은 모든 원래 검색 결과, 선택한 재귀 결과, 최신 후보 상태를 받고 다시 호출된다.
   메인 도구는 web_search뿐이다. 이전 미방문 링크도 다음 검색의 fetch 전용 단계에서
   선택할 수 있다. 마지막 검색에서도 읽기를 마친 뒤 메인을 도구 없이 호출해 답한다.

검색 소진 시에는 탐색용 시스템 프롬프트와 도구 호출 이력을 제외하고, 답변 전용
시스템 프롬프트·원 질문·전체 도구 결과·출처에 연결된 상태로 최종 작성한다.
최종 본문이 없거나 도구 호출/계획이면 한 번만 재요청한다. 두 번 모두 실패하면
빈 응답으로 기록한다. 일반적인 정상 초안 검토와 baseline 경로는 유지한다.
`run.final_request`에 실제 작성 입력, `run.final_response`에 본문과 reasoning을 저장한다.

저장된 빈 응답 8개의 최종 작성만 확인하려면 `python probe_final_answer.py`를 실행한다.
최대 16회 모델 호출이며 검색/fetch/채점 호출과 원래 실행 결과 수정은 없다.
이는 본문 반환 안정성 검사이며 정답률 개선 평가가 아니다.

선택은 fetch 도구를 제공하는 내부 호출이고, 읽은 뒤 상태 갱신은 별도의 도구 없는
JSON 호출로 유지한다. 메인의 search 인자는 query 하나, 내부 fetch 인자는 url
하나다. 선택 단계와 자식 explorer는 실제 URL을 사용한다.

## 상태와 실패 처리

- 출처 ID·URL·검색 snippet·페이지 노트는 보존하고, 후보의 지지 근거·반대 근거·
  미확인 항목을 분리한다. snippet과 페이지 노트는 입력에서 별도로 표시한다.
- 근거 인용은 실제 등록된 snippet/노트의 문자열과 대조한다. 없는 출처, 만들어 낸
  인용은 상태에 추가하지 않는다. 이는 의미적 정답 검증을 대신하지 않는다.
- 잠정 답은 유효한 지지 근거를 가진 후보에 연결된 출처를 요구한다. 후보 기각과
  명시적 withdraw로 철회할 수 있다. 이전 근거는 후보 갱신 때 삭제하지 않는다.
- 선택 단계의 잘린 출력·잘못된 도구/인자·복수 호출·미등록 URL은 실행하지 않는다.
  빈 본문은 실패, 도구 없는 일반 응답은 정상 건너뛰기로 구분한다. reasoning에서
  URL을 추측하거나 실패 시 첫 결과를 자동 선택하지 않으며 추가 재시도도 없다.
  기존 자식 reader와 같은 도구 envelope 처리만 공유한다. 상태 갱신의 잘못된
  JSON은 무시한다. 기존 유효 상태와 원래 검색 결과를 유지해 메인이 계속할 수 있다.
- 이미 읽었거나 실패한 정확한 URL은 선택 후보에서 제외한다. 메인의 직접 fetch는
  제공하지 않으며 잘못 생성된 호출도 실행하지 않는다. 검색 소진 후 메인 도구를
  제거한다. 그 전에 마지막 검색에 연결된 재귀 읽기는 기존 노드 예산 안에서 완료한다.
- Google/Bing/DDG 등 알려진 검색 엔진의 query endpoint는 DS의 문서 fetch에서
  차단한다. 사이트 내부 탐색(예: Wikipedia 검색)은 유지한다. 모든 웹 검색 우회
  가능성을 포괄적으로 차단하는 일반 검색 엔진 분류기는 아니다.
- 최대 턴·오류 복구에서도 후보·인용·잠정 답 및 최근 판단을 전달한다. 컨텍스트가
  넘으면 질문과 근거 인용을 포함한 상태를 우선한다. 잘못된 작업 계획은 답으로
  채택하지 않고 기존 최종 작성 재시도 안에서 복구한다.

## 비용과 재현

선택 시 내부 모델 호출 1회, 새 페이지 묶음 처리 후 상태 갱신 1회가 추가될 수 있다.
모두 기존 모델·샘플링 설정을 사용하며 Usage의 calls/input/output tokens에 포함한다.
총비용 감소나 성능 상승은 실제 실행 전에는 주장할 수 없다.

- `response.json`: `research_state`, `auto_fetches`, 기존 모든 도구 결과와 재귀 트리.
- `trace.jsonl`: `control.request/response/state/error`, `search.selected_entry/result`,
  `fetch.no_progress`, `fetch.search_endpoint_blocked` 등.
- `records.jsonl`: `auto_fetches`, `control_stats` 및 전체 LLM 호출·토큰.
- `summary.json`: 선택적 진입 총량과 control_stats, 기존 전체 비용 지표.
- 실행 폴더의 `controller_prompt.txt`: 상태 갱신 프롬프트 원문.
- `selector_prompt.txt`, `selector_tool.json`: 선택 프롬프트와 fetch 도구 정의.

`fetches`는 계속 메인의 명시적 fetch 호출 수다. 선택적 진입은 `auto_fetches`,
자식 포함 실제 페이지 요청은 `fetch_attempts`로 구분한다. 새 구조에서 메인 fetch는
0이며 유한 max_fetches 설정은 선택적 진입에 적용한다. 현재 설정은 별도 한도가 없다.

## 검증과 명령어

전체 실행 전 짧은 선택기 진단:

```powershell
python probe_selective_entry.py
```

저장된 BrowseComp 검색 배치 7개를 각각 2번, 총 14회의 선택기 모델 호출로
독립적으로 재생한다. 새 검색/fetch/재귀/채점은 하지 않는다. `--dry-run`은
모델 호출도 하지 않고 입력 목록만 확인한다. 결과는 `runs/selector_probe/`에
저장한다. 5개 오답 사례와 2개 정답 사례를 고른 진단 패널이며 전체 정확도나
전체 궤적의 개선량을 추정하는 평가가 아니다. reference_hit은 미리 확인한
유용한 입구와의 일치 여부다. 다른 출처 선택도 유효할 수 있어 불일치를 곧
오답으로 간주하지 않는다. 입력에는 비교용 reference/gold/성공 여부를 넣지 않는다.

오프라인 회귀 테스트는 네트워크·실제 모델·채점기를 사용하지 않는다.
정확한 URL 선택, 잘못된 상태 거절, 재귀 예산, 전체 사용량, 답 보존, 캐시 복원,
baseline의 비변경을 확인한다. 실제 모델이 올바른 입구를 고르는지는 벤치마크에서
확인해야 한다.

```powershell
python -m unittest discover -s tests -p "test_*.py" -q
```

BrowseComp 기존 test 표본 300문항 비교:

```powershell
python test.py --method depthsearch --benchmark browsecomp --split test --limit 300 --tag ds_search_main_v3
```

중단된 **새 태그의 실행** 이어 돌리기:

```powershell
python test.py --method depthsearch --benchmark browsecomp --split test --limit 300 --tag ds_search_main_v3 --resume
```

기존 `paper_frozen_v1` 실행을 resume하거나 그 결과에 새 방법을 섞지 않는다.
기존 baseline 전체 재실행은 이 변경의 일부가 아니다.
