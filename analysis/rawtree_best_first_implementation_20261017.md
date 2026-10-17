# RawTree best-first 구현 — 2026-10-17

현재 `configs/jevtree.yaml`은 `jev_strategy=raw`, `jev_traversal=best_first`를 사용한다.
구현 버전은 `raw-browser-best-first-docling/8`다. 이전 수집·탐색·평가 전송 정책과 캐시를 구분한다.
`conf.yaml`의 기본 실행 방법은 바꾸지 않았다. RawTree 실행에는 `--method jevtree`를 지정한다.

## 탐색과 근거 전달

1. 검색 결과에서 유효하고 중복되지 않는 진입 페이지를 최대 10개 연다. 진입 페이지 깊이는 1이다.
2. 모든 페이지를 로컬 Jina `engine=browser`로 수집한다. 앞부분 약 5,000토큰에서 페이지의 direct/query 가치와 링크를 평가한다.
3. best-first는 평가한 모든 링크를 전역 우선순위 큐에 유지한다. 최대 4개의 페이지 작업을 진행하고, 하나가 완료되면 빈자리를 보충한다. 대기 중인 진입 페이지를 먼저 처리하고, 이후 현재 평가가 완료된 후보 중 높은 점수를 선택한다. 깊이가 다른 후보도 함께 비교하며 중복 URL을 건너뛰면 다음 후보로 자리를 채운다.
4. 최대 깊이 5, 검색 한 번당 논리적 페이지 방문 50회를 지킨다. 캐시 재사용과 실패도 방문 예산에 포함된다. 느린 페이지를 기다리는 동안에도 다른 페이지의 탐색을 진행한다. 근거 최종 선별은 시작한 탐색 작업이 종료된 뒤 수행한다.
5. 페이지 순위에서 원질문용 2개, 나머지에서 현재 쿼리용 4개를 고른다. 저장한 전체 본문을 사용하므로 다시 fetch하지 않는다. 부족한 몫을 다른 몫으로 이월하지 않는다.
6. 선택한 문서만 Docling으로 청킹한다. 5,000토큰 번들을 먼저 평가하고, 선별된 번들에 포함된 512토큰 청크를 평가한다. 번들은 임계값 0.15 이상과 각 목적의 최고 번들을 유지한다.
7. 청크는 원질문용 최대 4개와 쿼리용 최대 8개를 선별하고, 예산이 허용하면 앞뒤 이웃 1개를 붙인다. 총 반환 상한은 16,000토큰이며 생성 요약은 만들지 않는다.

부모별 `jev_branch=2`와 깊이별 `jev_frontier_width=10`은 **beam 비교 모드에서만** 적용한다.
best-first에서는 기존 설정 키 `jev_expand_batch=4`를 동시 진행 페이지 작업 상한으로 사용한다. HTTP 동시 요청 제한 `jev_concurrency=4`와 별도 설정이다.
동일 점수는 얕은 깊이, URL, 삽입 순서로 정렬한다. 같은 시점에 완료된 작업은 노드 순서로 반영한다.
완료 순서에 따라 당시 알려진 후보가 달라지므로 방문 순서와 결과도 달라질 수 있다. 아직 평가되지 않은 후보까지 비교하는 순차 best-first와 같지는 않다.
trace의 frontier 이벤트에 `completed`, `active_pages`, `queued_roots`를 기록한다.

## 평가 요청과 실패 처리

- 평가 비용 절감을 위한 링크 생략은 추가하지 않았다. 기본 `jev_packet_questions=1`로 **평가 항목 하나당 HTTP 요청 하나**를 보낸다. 페이지의 direct/query 점수와 각 링크 점수도 개별 요청이며 같은 원문 state를 유지한다. 기존 동시성 측정의 요청 단위와 맞춘 것이다.
- `jev_concurrency=4`, `jev_inflight_questions=4`로 실제 HTTP 요청을 최대 4개씩 묶는다. **현재 묶음의 모든 요청이 완료되어야 다음 묶음을 전송한다.** 하나가 빨리 끝나도 새 요청으로 보충하지 않는다. 모든 문항·문서 작업이 공유하는 LocalDecision에서 이 경계를 적용한다.
- 페이지 하나만 남아 있어도 그 페이지의 평가 항목을 최대 4개 동시에 보낸다. 각 문서는 최대 4개 요청씩 대기열에 올리고, 다음 묶음에서는 먼저 대기하던 다른 문서도 FIFO 순서로 처리한다. 준비된 요청이 4개보다 적으면 남은 요청만 처리하므로 마지막 묶음 때문에 멈추지 않는다.
- 페이지 탐색 작업은 계속 최대 4개까지 준비할 수 있지만 HTTP 전송 묶음과는 별개다. 요청별 `jev.attempt`의 `batch_id`로 묶음을 구분하고, 앞 묶음의 마지막 result/error/cancelled 이후에만 다음 묶음의 attempt가 나오는지 검증한다.
- `jev.attempt`에 `question_count`, `inflight_questions`, `question_budget`, `queue_ms`도 남긴다. 이 상한은 이 클라이언트의 응답 대기 중인 평가량이다. 타임아웃·연결 취소 후 서버가 내부 작업을 중지하는지는 별개이며, 다른 클라이언트가 보내는 부하는 포함하지 않는다.
- 질문 하나의 검색들 사이에서 성공한 원문을 재사용한다. 방문 집합은 검색마다 초기화하고 쿼리에 따른 평가는 다시 한다. 실패한 fetch는 캐시하지 않는다.
- 페이지·번들·청크 평가 실패는 실패로 기록하고, 다른 성공한 근거를 계속 반환한다. 실패 점수를 0으로 만들지 않는다.
- 묶음 내 일부 평가가 실패해도 나머지 응답을 기다리고 성공한 점수를 보존한다. 해당 문서의 후속 묶음은 중단한다. 실패하거나 평가되지 않은 링크는 `score=null`, `evaluated=false`로 남는다.
- 반환 텍스트에 수집/평가 실패로 불완전한 검색임을 표시한다. 프로그래밍 오류와 취소까지 무조건 삼키지는 않는다.
- trace의 `rawtree.frontier`, `rawtree.traversal_end`, `rawtree.fetch_reused`, `rawtree.evaluation_failed`와 통계의 `page_visits`, `document_reuses`, 단계별 `*_eval_failures`로 확인할 수 있다.

## 유지한 제한

- 기본 링크 임계값은 **0.0**이다. 좋은 후보가 소진되면 낮은 점수의 링크도 예산 내에서 확장한다. 이를 없앴다고 해석하지 않는다. `0.01`은 별도 비교 실험 값이며 보정된 확률이라는 보장은 없다.
- 탐색 링크와 페이지 순위는 앞부분 5,000토큰에 의존한다. 뒤쪽 근거는 해당 페이지가 청킹 대상으로 선택되어야 읽힌다.
- 모든 방문 문서의 모든 청크를 평가하지 않는다. 페이지 선별과 번들 선별을 유지한다.
- 제목 보존은 Docling의 `always_emit_headings=True` 옵션을 사용한다. 긴 Markdown 표의 헤더 반복 문제에 별도 규칙 기반 파서를 추가하지 않았다.
- best-first가 정답률이나 최적 경로를 보장하지 않는다. 실측 전에는 현재 값을 최적값으로 부르지 않는다.

## 비교 실험 순서

동일한 진단 10문항과 공통 설정에서 아래 실험을 순차적으로 비교한다. `--no-cache`는 실행 결과 캐시를 끄며, 한 문항 안의 원문 재사용은 유지한다. 실행 설정과 파라미터는 각 실행 디렉터리에 저장된다.

### 1. browser beam 대 browser best-first

```powershell
.\.venv\Scripts\python.exe test.py --method jevtree --model gpt-oss --benchmark browsecomp --path data/browsecomp/test_diagnostic10.json --limit 10 --raw-traversal beam --raw-link-floor 0 --tag raw_browser_beam10 --no-cache
.\.venv\Scripts\python.exe test.py --method jevtree --model gpt-oss --benchmark browsecomp --path data/browsecomp/test_diagnostic10.json --limit 10 --raw-traversal best_first --raw-link-floor 0 --tag raw_browser_best10 --no-cache
```

이 beam은 이전 curl 실행의 재현이 아니라, browser 수집·본문 재사용·실패 복구를 공유하는 탐색 정책 비교군이다.

### 2. best-first 링크 임계값 0 대 0.01

앞 단계의 best-first 결과를 기준으로 다음 결과를 비교한다.

```powershell
.\.venv\Scripts\python.exe test.py --method jevtree --model gpt-oss --benchmark browsecomp --path data/browsecomp/test_diagnostic10.json --limit 10 --raw-traversal best_first --raw-link-floor 0.01 --tag raw_browser_best_floor001_10 --no-cache
```

### 3. 청킹 페이지 6 대 8

정책과 링크 임계값을 선택한 다음 같은 명령에 `--raw-query-pages 6`을 추가한다.
원질문 2 + 쿼리 6 = 총 8페이지로 바뀌며, 기존 2 + 4 = 6페이지와 비교한다.
깊이·방문 예산·청크 선별 개수·출력 상한은 고정한다.

정답률 외에도 수집/평가 실패율, 방문 수, 실제 browser 수집 수, 평가 요청 수,
반환에 기여한 페이지 수, 반환 청크/토큰 수와 문항 시간을 함께 확인한다.
진단 10문항 결과만으로 전체 벤치마크의 개선을 확정하지 않는다.

## 검증 결과

실제 외부 모델/수집 호출을 모킹한 회귀 테스트 **78개 통과**:
`test_rawtree*.py`, `test_jevtree*.py`, `test_lds.py`, `test_retry_errors.py`, `test_local_reader_guard.py`.
전역 후보 유지, 깊이 간 경쟁, 중복 보충, HTTP 요청 4개 단위 완료 경계, 취소 시 작업 정리, 임계값/깊이 제한,
본문 재사용과 재평가, 부분 패킷 복구, 번들/청크 실패 격리, CLI 설정 검증을 포함한다.
작은 묶음의 모든 키 보존, HTTP와 평가 항목 수 이중 제한, 제한 대기 중 취소,
전송 중 취소·실패 후 용량 복구, 파라미터 검증도 포함한다.
두 문서가 동시에 평가를 요청하고 첫 묶음의 3개만 끝난 상태에서, 다른 문서의 요청도
추가 전송되지 않는 회귀 테스트를 포함한다. 한 문서의 8개 평가와 다른 문서의 5개 평가를
모두 반환하며, 마지막 4개 미만 묶음도 종료하는지 검증한다.

v5 실행에서 q40 첫 검색에 약 31분이 소요됐고, 페이지 평가 11건이 180초 타임아웃으로 실패했다.
v6는 전체 배치 대기를 제거했지만, q40 재실행은 첫 검색 중 20.6분에 취소됐다.
HTTP 4개가 서버 내부 평가 작업 최대 256개를 유발할 수 있어 v7에서 작은 묶음과 공유 평가량 상한을 추가했다.
전체 정답률과 문항 시간 개선은 별도 벤치마크로 확인해야 한다.
v7 실제 서버 소규모 재현에서는 저장된 요청 4건(5/64/13/22항목)의 **104항목 전부**를
8항목 이하의 HTTP 요청 14건으로 처리했다. 최대 동시 HTTP 4개, 관측된 최대 동시 평가량 29항목,
실패 0건이었다. 총 100.25초, 가장 느린 HTTP 응답은 54.12초로 서버 지연은 여전히 남았다.
서로 다른 시점의 한 번씩 측정이므로 전체 실행 속도 향상을 입증한 실험은 아니다.
원본 결과는 `analysis/d3_rolling_diagnosis_20261017/backpressure_20261017-175032/summary.json`에 있다.
`probe_rawtree_search_policy.py` 및 기존 분석 파일은 수정 전 구현의 진단 기록이다.
