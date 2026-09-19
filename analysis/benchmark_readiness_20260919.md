# BrowseComp / EvoBrowseComp 실행 전 점검 — 2026-09-19

## 판단

현재 세 방법을 고정하고 새 벤치마크 평가를 시작할 수 있다. 비교의 단위는
동일 모델·동일 검색 호출 한도 아래의 **방법 전체**다. 전용 프롬프트, 문서 처리,
재귀, 최종 검토 정책을 포함한 DS를 비교하는 것으로 기술해야 한다.
동일 총 계산량 실험, 재귀 하나만의 인과 효과, 공식 구현의 완전 재현은 아니다.

이번 점검에서는 실행 코드·설정·프롬프트·기존 결과를 수정하지 않았으며, 모델/
검색/채점 실행도 하지 않았다. 오프라인 테스트 83개가 통과했다.
점검 시 Git HEAD: `031f33a1b2b2b3178826a81bc1a7575d22fe60e8`.

## 1. 재시도 후 DeepSearchQA

| 방법 | F1 | 0점 | 부분정답 | 만점 | 빈 응답 |
|---|---:|---:|---:|---:|---:|
| RAgent | .3919 | 135 | 102 | 63 | 1 |
| search-o1 | .4424 | 124 | 102 | 74 | 0 |
| DS 최초 실행 | .4406 | 134 | 80 | 86 | 13 |
| DS 재시도 반영 | .4550 | 127 | 87 | 86 | 1 |

정상 완료 287문항의 기록은 바뀌지 않았다. 최초 빈 응답 13문항에 대해
5차례 retry 명령에서 총 20개 문항 실행이 추가됐다(13+3+2+1+1).
q00093은 여전히 빈 응답이다. 최종 집합형 F1=.4835, 단일 정답 F1=.4118.
search-o1과의 평균 F1 차이 +.012657의 문항별 paired bootstrap 95% 구간은
[-.0372, +.0627](20,000회, Python random seed 0)이다. 독립 반복실험 또는
검색/생성/판정 변동까지 포함한 구간은 아니다.

이 결과를 '재시도 없는 단일 실행의 우위'로 제시하면 안 된다. 오류 선택에
정답 점수는 쓰지 않았으나, 빈 답변을 조건으로 전체 탐색을 다시 수행했으므로
방법별 추가 시도 기회가 달라진다. 기존 baseline 전체를 다시 돌릴 필요 없이,
최초 실행 결과와 복구 결과를 별도로 보존하고 보고할 수 있다.

### 비용 회계

현재 summary는 교체 후 최종 문항 결과의 합이며, 폐기된 시도의 비용이 빠진다.
retry_history의 각 completed 문항에 대응하는 이전 기록을 합치면 다음과 같다.

| 항목 | 현재 summary | 교체되어 빠진 시도 | 합계 |
|---|---:|---:|---:|
| 입력 토큰 | 191,881,194 | 7,743,210 | 199,624,404 |
| 출력 토큰 | 8,162,378 | 280,913 | 8,443,291 |
| LLM 호출 | 12,626 | 909 | 13,535 |
| 검색 | 2,370 | 190 | 2,560 |
| 기록된 fetch 시도 | 4,943 | 596 | 5,539 |

이는 기록된 사용량 합계이며 서버 오류 중 사용량이 미반환된 호출까지 보장하지
않는다. fetch 시도는 고유 성공 다운로드 수와 다르다. summary.cache는 마지막
retry 실행의 카운터이므로 전체 실행의 캐시 이용률로 해석하면 안 된다.

## 2. 통제된 것과 방법별 차이

| 항목 | RAgent | search-o1 재구현 | DS |
|---|---|---|---|
| 모델 | gpt-oss-20b | 동일 | 동일 |
| 생성 설정 | temperature=1, top_p=1, Reasoning=medium | 동일 | 동일 |
| 검색 호출 / 결과 수 | 10 / 10 | 10 / 10 | 10 / 10 |
| 원문 페이지 상한 | 32,768 토큰 | 동일 | 동일 |
| 호출당 생성 상한 | 8,192 토큰 | 동일 | 동일 |
| 세션 컨텍스트 상한 | 122,880 토큰 | 동일 | 동일 |
| 메인 턴 상한 | 40 | 40 | 40 |
| 메인 도구 | search + fetch | search | search + fetch |
| fetch 선택 | 메인 선택 | 검색 top-10 자동 fetch | 메인 선택 + 하위 링크 탐색 |
| 메인에 전달 | 원문 | 페이지별 추출 노트 | 출처별 노트 + 짧은 구조화 원문 |
| 재귀 | 없음 | 없음 | 최대 depth 3 |
| 정상 완료 후 별도 검토 | 없음 | 없음 | 초안 보존 검토 |
| 예산 소진 도구 동적 제거 | 기존 거절 방식 | 기존 거절 방식 | 적용 |

공통: Serper 검색, Jina 읽기, PDF/CSV 네이티브 파싱, 문항/벤치마크 유출 필터,
같은 웹 도구 구현. 계산기나 별도 추가 탐색 도구 없음.

DS 확장: depth>=2 전체 12노드, 한 root의 확장 6노드, 노드당 자식 2개,
reader 탐색 6턴. root fetch는 12노드에 포함되지 않는다. 메인 fetch의 별도
개수 상한은 없으며 메인 턴·컨텍스트 한도에 제한된다. 하위 노드는 search를
받지 않는다. 본문 링크 및 관찰한 사이트 내 URL 추론 경로를 사용할 수 있다.

8,192는 전체 문항 출력 토큰 예산이 아니며, 메인 40턴도 총 LLM 호출 수가
아니다. search-o1에는 자동 문서 읽기 호출이, DS에는 재귀 읽기와 최종 검토
호출이 추가된다. 논문에는 검색 예산 통제와 실제 토큰/호출 비용을 함께 보고한다.

## 3. baseline 재현 범위

[Search-o1 원 논문](https://arxiv.org/html/2501.05366)의 RAgent는 top-10 snippet 후
모델이 문서를 선택하고, Search-o1은 검색 문서를 Reason-in-Documents로 정제한다.
현재 구현은 이 구분을 유지한다. 다만 원 논문은 QwQ, Bing, 특수 토큰을 통한
추론 연속 생성 및 별도의 fallback을 사용한다. 현재는 GPT-OSS, Serper,
chat tool calls, 페이지별 reader 및 공통 복구 경로를 사용한다.

특히 search-o1은 YAML의 reader 프롬프트뿐 아니라 공통 `_EXTRACT_NOW`의
Page/Evidence/Coverage/Missing/Next links/Status 지침도 받는다. 따라서
'원 논문 프롬프트 그대로'라고 쓰지 말고, 공통 도구 환경에 맞춘 재구현이라고
기술하며 실제 시스템/사용자/도구 템플릿을 함께 공개한다. DS를 구성하는 정책
전체가 비교 대상이므로 프롬프트를 억지로 동일하게 만들 필요는 없다.

## 4. 데이터 준비 상태

| 항목 | BrowseComp | EvoBrowseComp |
|---|---|---|
| 로컬 raw 크기 | 1,266 | 400 |
| 실행 test 크기 | 300 | 400 |
| 언어 | 영어 | 영어 |
| 선택 방식 | seed=0, 10분야 각 30개 | 로컬 영어 raw 전체 |
| 중복 ID/질문, 빈 질문/정답 | 없음 | 없음 |
| test의 질문·정답이 raw와 일치 | 확인 | 확인 |
| 실제 로더/질문 입력 확인 | 통과 | 통과 |

BrowseComp test는 기존 stratified 함수로 seed=0을 주어 만든 300개와 정확히
일치한다. 원본 전체 1,266개의 공식 결과가 아니므로 논문에는
**BrowseComp balanced 300-question subset**으로 명시한다.
EvoBrowseComp는 **EvoBrowseComp-EN 400**으로 명시한다. `--limit 300`을 주면
400개 중 앞의 300개만 실행하므로, 전체 영어 평가에는 400을 명시한다.

SHA-256:

- BrowseComp test.json: `6903293182dad41cae283826b6a8262f78a10e52f8f3b63dece1a9857f7b84a4`
- EvoBrowseComp test.json: `bded22d750e2bead47957b16721d95c04090a44f1600d8c030413d1681c59266`

공식 [BrowseComp 자료](https://openai.com/index/browsecomp/)와
[EvoBrowseComp 저장소](https://huggingface.co/datasets/Krystalan/EvoBrowseComp)를
확인했다. 위 검증은 로컬 raw와 실행 파일 사이의 검증이다. 셸의 네트워크
제한으로 공식 암호화 파일을 내려받아 현재 로컬 raw와 전수 대조하지는 못했다.
데이터 공개 시 복호화 문항 원문 대신 선택 ID·해시·복호화/선택 절차를 보존한다.

## 5. 채점 프로토콜

현재 `_single.py`는 최종 정답을 추출해 Gemini로 의미 일치를 판정한다.
단일 정답에서 accuracy=F1=precision=recall이며 주 지표는 accuracy로 쓴다.
정답은 judge에만 제공하며 수행 모델의 입력은 질문뿐이다.

[BrowseComp 공식 evaluator](https://github.com/openai/simple-evals/blob/main/browsecomp_eval.py)는
Explanation/Exact Answer/Confidence 형식과 자체 grader prompt를 쓴다.
현재 질문 입력과 grader는 그대로의 공식 evaluator가 아니다. 수치 오차 등
판정 지침에도 차이가 있다. 자체 동일 환경의 세 방법 비교로는 사용 가능하나
공식 점수와 직접 같은 조건이라고 주장할 수 없다.

[EvoBrowseComp 논문 §2.4, §3.1](https://arxiv.org/html/2606.13120v1)은 GLM-5-Chat
판정, search/visit 전체 도구 호출 40회, 세 번의 독립 평가 평균을 사용한다.
현재 설정은 Gemini 판정, search 10회, 메인 40턴과 추가 reader 호출이다.
따라서 동일한 benchmark questions를 사용하는 별도 통제 실험으로 기술한다.

공식 프로토콜과 동일하다고 주장할 계획이 없다면 현 판정으로 세 방법을
동일하게 평가할 수 있다. 공식 지표 재현이 필요하면 생성 전에 공통 질문
포맷/판정 템플릿을 정하고 고정한다. 결과를 본 뒤 방법별로 판정 지침을 바꾸지 않는다.

## 6. 본 실험 전에 고정할 최소 규칙

1. 새 두 데이터셋 결과를 보고 프롬프트를 다시 튜닝하지 않는다. 이미 반복
   분석한 DeepSearchQA 300개는 방법 개발에 사용한 데이터로 취급하고,
   그 사실을 숨긴 채 최종 미사용 test라고 부르지 않는다.
2. 세 방법에 같은 시도 규칙을 적용한다. 가장 단순한 주 결과는 현재 내부
   복구만 포함한 최초 전체 실행이며, 빈 답변과 턴 소진도 0점에 포함한다.
   외부 `--retry-errors`는 복구 결과로 별도 보고하거나, 사전에 세 방법 공통
   횟수를 정한 프로토콜로 사용한다. 성공할 때까지의 수동 반복을 기본으로 삼지 않는다.
3. 결과 캐시는 태그와 무관하다. 새 독립 실행에는 `--no-cache`를 사용한다.
   이는 agent와 judge 캐시 모두를 끈다. 중단된 실행을 일반 `--resume`으로
   이어갈 계획이면 캐시를 켜되 agent_hits가 실제 재사용임을 기록하고 새 seed
   실험으로 세지 않는다. 현재 `--no-cache`와 `--resume`은 동시 사용 불가다.
4. `run.seed=0`은 LLM 요청의 generation seed로 전달되지 않는다. temperature=1의
   생성은 확률적이며 설정의 seed만으로 완전 재현된다고 주장하면 안 된다.
   모델 revision, vLLM 버전/파서/서버 인자, 현재 commit, sampling, 데이터 해시,
   judge 이름, 실제 프롬프트, 웹 도구 환경변수를 기록한다.
5. 최초/재시도 결과와 비용을 구분해 유지한다. 시간 비교는 캐시·동시성·실행일
   영향을 받으므로 토큰/호출량과 함께 제시한다.

이는 실험 운영 규칙이며, 별도의 새 검색 도구나 baseline 전면 재실행을 요구하지 않는다.
기존 DS의 단일 정답 강점은 새 벤치마크 평가의 동기는 되지만 성능 보장은 아니다.

## 7. 실행 명령

두 데이터셋은 validation.json이 없으므로 `--split test`를 명시한다.
아래는 기본 캐시를 켠 첫 평가 명령이다. 현재 작업공간에서 각 데이터셋의
세 방법별 실제 cache_key를 계산해 확인했으며, 여섯 조건 모두 일치하는
기존 agent 캐시 파일은 0개다. 이후 독립 반복실험에는 `--no-cache`를 붙인다.

```powershell
python test.py --benchmark browsecomp --split test --limit 300 --method ragent --tag paper_frozen_v1
python test.py --benchmark browsecomp --split test --limit 300 --method search-o1 --tag paper_frozen_v1
python test.py --benchmark browsecomp --split test --limit 300 --method depthsearch --tag paper_frozen_v1

python test.py --benchmark evobrowsecomp --split test --limit 400 --method ragent --tag paper_frozen_v1
python test.py --benchmark evobrowsecomp --split test --limit 400 --method search-o1 --tag paper_frozen_v1
python test.py --benchmark evobrowsecomp --split test --limit 400 --method depthsearch --tag paper_frozen_v1
```

## 우선순위

지금은 또 다른 성능 기능을 넣기보다 위 설정을 고정하고 새 두 벤치마크에서
검증하는 편이 타당하다. 단, 비용/재시도 집계와 공식 평가와의 차이를 명시하지
않은 채 현재 summary만 논문 표로 옮기는 것은 권하지 않는다.
