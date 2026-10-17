# RawTree best-first 구현 — 2026-10-17

현재 `configs/jevtree.yaml`은 `jev_strategy=raw`, `jev_traversal=best_first`를 사용한다.
구현 버전은 `raw-browser-best-first-docling/5`다. 기존 curl 기반 구현과 캐시를 구분한다.
`conf.yaml`의 기본 실행 방법은 바꾸지 않았다. RawTree 실행에는 `--method jevtree`를 지정한다.

## 탐색과 근거 전달

1. 검색 결과에서 유효하고 중복되지 않는 진입 페이지를 최대 10개 연다. 진입 페이지 깊이는 1이다.
2. 모든 페이지를 로컬 Jina `engine=browser`로 수집한다. 앞부분 약 5,000토큰에서 페이지의 direct/query 가치와 링크를 평가한다.
3. best-first는 평가한 모든 링크를 전역 우선순위 큐에 유지한다. 높은 점수부터 최대 4페이지씩 선택하며, 깊이가 다른 후보도 함께 비교한다. 중복 URL을 건너뛰면 다음 후보로 자리를 채운다.
4. 최대 깊이 5, 검색 한 번당 논리적 페이지 방문 50회를 지킨다. 캐시 재사용과 실패도 방문 예산에 포함된다. 같은 배치의 평가가 모두 끝난 뒤 다음 배치를 선택한다.
5. 페이지 순위에서 원질문용 2개, 나머지에서 현재 쿼리용 4개를 고른다. 저장한 전체 본문을 사용하므로 다시 fetch하지 않는다. 부족한 몫을 다른 몫으로 이월하지 않는다.
6. 선택한 문서만 Docling으로 청킹한다. 5,000토큰 번들을 먼저 평가하고, 선별된 번들에 포함된 512토큰 청크를 평가한다. 번들은 임계값 0.15 이상과 각 목적의 최고 번들을 유지한다.
7. 청크는 원질문용 최대 4개와 쿼리용 최대 8개를 선별하고, 예산이 허용하면 앞뒤 이웃 1개를 붙인다. 총 반환 상한은 16,000토큰이며 생성 요약은 만들지 않는다.

부모별 `jev_branch=2`와 깊이별 `jev_frontier_width=10`은 **beam 비교 모드에서만** 적용한다.
best-first에서는 `jev_expand_batch=4`가 다음 배치 크기다. HTTP 동시 요청 제한 `jev_concurrency=4`와 별도 설정이다.
동일 점수는 얕은 깊이, URL, 삽입 순서로 정렬한다. 네트워크 완료 순서가 다음 방문 순서를 바꾸지 않는다.
배치 내 미완료 페이지의 자식은 다음 배치부터 경쟁하므로 순차 best-first와 완전히 같지는 않다.

## 평가 요청과 실패 처리

- 평가 비용 절감을 위한 링크 생략은 추가하지 않았다. 한 요청의 질문은 최대 64개다. 첫 요청에는 페이지 점수 2개와 링크 최대 62개가 들어가며, 남은 링크는 64개씩 후속 요청한다.
- 질문 하나의 검색들 사이에서 성공한 원문을 재사용한다. 방문 집합은 검색마다 초기화하고 쿼리에 따른 평가는 다시 한다. 실패한 fetch는 캐시하지 않는다.
- 페이지·번들·청크 평가 실패는 실패로 기록하고, 다른 성공한 근거를 계속 반환한다. 실패 점수를 0으로 만들지 않는다.
- 후속 링크 패킷만 실패하면 먼저 검증된 패킷의 페이지 점수와 링크 점수는 유지한다. 평가되지 않은 링크는 `score=null`, `evaluated=false`로 남는다.
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

실제 외부 모델/수집 호출을 모킹한 회귀 테스트 **73개 통과**:
`test_rawtree*.py`, `test_jevtree*.py`, `test_lds.py`, `test_retry_errors.py`, `test_local_reader_guard.py`.
전역 후보 유지, 깊이 간 경쟁, 중복 보충, 완료 순서 독립성, 임계값/깊이 제한,
본문 재사용과 재평가, 부분 패킷 복구, 번들/청크 실패 격리, CLI 설정 검증을 포함한다.

이번 구현 작업에서 실제 정답률 벤치마크는 실행하지 않았다.
`probe_rawtree_search_policy.py` 및 기존 분석 파일은 수정 전 구현의 진단 기록이다.
