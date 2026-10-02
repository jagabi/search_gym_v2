# DepthSearch / search_gym

**연구 상태: 2026-09-27. 목표 저널: IEEE Access.** 이 문서는 이 대화에서 합의한 연구 목적,
실험 통제값, 성공·실패 기록과 다음 작업을 이어가기 위한 기준이다. 점수는 저장된
`records.jsonl`을 문항 ID별로 집계했다. 과거 설정과 현재 설정을 혼동하지 않는다.

- [연구 목적과 정체성](#연구-목적과-정체성)
- [모델·벤치마크·통제값](#모델벤치마크통제값)
- [확인된 전체 실험 결과](#확인된-전체-실험-결과)
- [개선 시도와 실패에서 배운 점](#개선-시도와-실패에서-배운-점)
- [현재 구현과 진행 상태](#현재-구현과-진행-상태)
- [실행·재개·재현](#실행재개재현)
- [전체 실행 목록](#전체-실행-목록)

## 연구 목적과 정체성

### 무엇을 보이려는가

고정된 검색 자원에서 **문서를 선택하고, 문서의 링크를 재귀적으로 따라가며, 찾은 근거를
부모에게 반환하는 탐색 방식**이 웹 연구 문제의 정답률을 높일 수 있는지 연구한다.
RAgent와 search-o1 모두 비교 대상이다. 최종 목표는 벤치마크 성능의 개선이며,
모델 호출·입출력 토큰·fetch·실행 시간도 함께 보고한다. 검색 횟수가 같다고 총 계산량까지
같다고 주장하지 않는다.

이 연구는 제품 기능 확장이 아니다. GEPA는 현재 사용하지 않는다. 계산기, 별도 find/
재독해 도구, 표 연산, Excel 전용 도구 등을 추가하지 않는다. 이미 구현된 PDF·CSV 파싱은
공통 `web_fetch` 내부에 유지한다. 기반 모델의 계산·일반 추론 능력은 통제된 조건으로 두고,
탐색 정책·근거 전달·실행 구조를 개선한다.

**기여는 재귀 하나만의 효과로 한정하지 않는다.** 도구 구조에 맞는 전용 프롬프트와
탐색·반환 정책을 포함한 방법 전체를 비교한다. 재귀만의 인과 효과를 주장하지 않는 한
재귀를 끈 실험을 필수 다음 작업으로 두지 않는다. 프롬프트는 짧고 핵심적인 지시를 유지한다.
확인한 답 항목과 근거 있는 추론은 불완전한 조사에서도 보존하되, 부분점수만을 위해
없는 사실이나 정답을 꾸며내도록 지시하지 않는다.

### 유지할 DepthSearch의 정체성

1. 메인은 전역 검색과 최종 판단을 담당한다. 현재 DS 메인 도구는 `web_search`다.
2. 하위 읽기 단계는 검색 결과에서 유용한 진입 페이지를 선택한다.
3. 문서 reader/explorer는 현재 페이지의 링크나 관찰한 사이트의 주소 구조를 이용해
   `web_fetch`로 자식을 열고 재귀한다. URL 추론의 자유를 일괄 제거하지 않는다.
4. 자식의 근거가 부모에게 돌아오고, 부모는 계속 탐색하거나 반환한다. 읽기 단계 종료 후
   **메인을 반드시 다시 호출**해 다음 검색 또는 답변을 결정한다.
5. 자기 페이지 근거와 자식 근거는 출처별로 보존한다. 부모의 가설을 자식 페이지의 사실로
   재포장하지 않는다. 전체 검색 결과를 자동으로 전부 fetch하는 방식은 마지막 비교 후보이며
   현재 기본 정책이 아니다.

`fetch`는 문서를 가져오는 도구 실행이고, `reader 호출`은 그 문서를 읽거나 후속 링크를
판단하는 **같은 기반 모델의 LLM 호출**이다. 별도의 비공개 검색 도구가 아니다.

| 방법 | 메인 도구 | 진입 문서 선택 | 메인으로 전달 | 문서 재귀 |
|---|---|---|---|---|
| RAgent | search + fetch | 메인 모델 | 원문 | 없음 |
| search-o1 | search | 검색 결과 상위 10개 자동 fetch | 페이지별 reader 요약 | 없음 |
| DepthSearch | search | 하위 모델의 선택적 fetch | 출처별 근거와 읽기 결과 | 있음 |

현재 DS의 흐름:

```text
메인 web_search
  → 진입 모델 web_fetch(urls=[관측 URL 또는 출처 ID, ...]) 또는 생략
  → 선택한 루트를 순서대로 읽기(depth 1)
      → 문서 링크 web_fetch(url) → 자식(depth 2) → 자식(depth 3)
      ← 출처별 근거 반환; 부모가 후속 판단
  → 도구 없는 읽기 마무리 응답
  → 메인 재호출 → 다음 검색 또는 최종 답변
```

## 모델·벤치마크·통제값

### 목표 모델과 현재 실행 환경

| 항목 | 설정 / 상태 |
|---|---|
| 주 실험 모델 | `openai/gpt-oss-20b` (`--model gpt-oss`) |
| 두 번째 목표 모델 | Qwen-3.5, 현재 프로파일 `Qwen/Qwen3.5-9B` (`--model qwen`) |
| gpt-oss sampling | temperature 1.0, top_p 1.0, reasoning `medium` |
| Qwen sampling | temperature 1.0, top_p 0.95, presence_penalty 1.5, top_k 20, thinking 활성화 |
| 역할별 모델 | 메인·진입·reader 모두 선택한 동일 기반 모델; 더 큰 모델을 숨겨 쓰지 않음 |
| 서빙 | 외부 vLLM의 OpenAI 호환 API. 모델별 parser 설정은 `searchgym/serving.py` |
| 도구 | 로컬 MCP, Serper 검색, Jina 읽기 및 공통 PDF/CSV 파싱 |
| 판정 | `gemini-3.6-flash`, thinking low, temperature 0.0; 현재 주요 저장 실행 공통 |
| 실행 | workers 4, run seed 0, 캐시 활성화. 생성의 완전한 결정성을 뜻하지 않음 |
| 실행 범위 | 자율 개선 실험은 `--limit 10`; 300개 전체 실행을 자동 시작하지 않음 |

아래 점수는 **gpt-oss-20b** 결과다. 현재 `runs/test`에 Qwen의 대응 본 실험 결과는 없다.
Qwen-3.5와 EvoBrowseComp는 연구 대상이며, 미실행 결과를 검증 완료로 적지 않는다.
코드에 Gemma/K-BrowseComp 프로파일도 있지만 이 연구의 합의된 주 대상은 위 두 모델과
아래 세 벤치마크다. GPU·vLLM 이미지/빌드·모델 revision은 논문 실행별로 별도 고정·기록해야 하며,
현재 모델 이름만으로 과거 실행의 하드웨어까지 같았다고 추정하지 않는다.

### 벤치마크 3개

| 벤치마크 | 현재 로컬 데이터 | 주요 지표 | 실행 상태 |
|---|---|---|---|
| DeepSearchQA | train 30 / validation 30 / test 300; 원본을 그대로 전부 쓴 수치가 아님 | 문항 평균 F1, 완전정답, 0점·부분정답 | 세 방법 300개 및 DS evidence_completion 완료 |
| BrowseComp | `data/browsecomp/test.json` 300문항; 원본 1,266 전체 결과가 아님 | 정답 수/정확도; 현재 판정기에서는 F1=accuracy | 세 방법 및 여러 DS 버전 완료; 10개 개발 코호트 실험 중 |
| EvoBrowseComp | `data/evobrowsecomp/test.json` 현재 400문항 | 단일 정답 정확도 | 데이터·실행기 준비, 이 저장소의 완료 본 실험 결과 없음 |

DeepSearchQA 분할은 `split_meta.json`의 seed 0, 범주 층화, 분할 간 중복 0을 따른다.
BrowseComp 300개 비교는 10개 범주 각 30개다. EvoBrowseComp를 50/50/300으로 재분할하는
예전 예제는 **현재 파일 상태가 아니다**. 재현 중 데이터 분할을 다시 생성하지 않는다.

반복적으로 살펴본 30개/10개 표본과 기존 test 사례는 이미 개발에 사용됐다.
이 결과를 새로운 미관측 평가 결과로 표현하지 않는다. 최종 보고에서는 개발 사용 범위와
평가 범위를 명시한다. gold는 judge·사후 분석에만 쓰며 검색/모델 프롬프트에 넣지 않는다.

### 실제 통제값

`conf.yaml`, `configs/*.yaml`보다 **각 run에 저장된 `config.json`이 그 실행의 기준**이다.
주요 300개 비교 실행과 현재 설정에서 직접 확인한 값:

| 항목 | 값 |
|---|---:|
| 세 방법 검색 최대 횟수 | 10 |
| 검색 반환 결과 수 | 10 |
| search-o1 자동 fetch 상위 수 | 10 |
| 메인 턴 상한 | 40 |
| 호출당 생성 상한 | 8,192 tokens |
| 공통 페이지 입력 상한 | 32,768 tokens |
| 메인/현재 DS reader context 상한 | 122,880 tokens |
| DS 문서 깊이 | 3 |
| DS 문항 전체 depth ≥ 2 확장 노드 | 12 |
| reader의 직접 자식 상한 | 2 |
| 진입 페이지 하나가 사용할 재귀 노드 | 6 |
| reader 탐색 턴 / 진입 단계 호출 상한 | 6 |
| 현재 배치 루트 선택 개수 상한 | 기존 진입 턴 상한에서 가져온 6 |
| 도구 프로토콜 복구 상한 | 2 |

대화 초반의 “max result 5”와 예전 README의 `search_top_k=5` 설명은 현재 저장된 주요
비교와 다르다. 검색 10/결과 10을 바꾸지 않는다. depth 1 루트는 자식 2개·확장 노드 12개를
차감하지 않는다. 따라서 재귀 노드 12개가 총 fetch/LLM 비용의 상한은 아니다.
선택된 루트는 공유 예산 아래 순차 독해하며, 실패 fetch는 성공한 확장 노드로 세지 않는다.

기존 RAgent/search-o1 실행·설정·캐시는 DS 개선 때문에 다시 돌리거나 수정하지 않는다.
공통 도구/파서 변경이 생기면 대응 실행의 차이를 먼저 확인한다. 예산이 같아도 fetch 수,
호출 수, 토큰, 프롬프트, 검색 시점이 달라질 수 있으므로 함께 공개한다.

## 확인된 전체 실험 결과

### DeepSearchQA 300개

| 실행 | 평균 F1 | 완전정답 | 0점 | 부분정답 | LLM 호출 | 시간 중앙값(초) |
|---|---:|---:|---:|---:|---:|---:|
| RAgent `main` | 0.3919 | 63 | 135 | 102 | 4,783 | 120.8 |
| search-o1 `main` | 0.4424 | 74 | 124 | 102 | 15,959 | 1,064.4 |
| DS `main` | 0.4148 | 86 | 151 | 63 | 10,334 | 352.4 |
| DS `ds_evidence_completion` | **0.4550** | 86 | 127 | 87 | 12,626 | 486.0 |

관측된 개선은 DS의 0점 24개 감소와 부분정답 24개 증가이며 만점 수는 유지됐다.
다만 전후 탐색 전체를 재실행했으므로 특정 프롬프트 하나의 효과로 단정하지 않는다.
`main`의 초과 0점은 특히 집합형에 집중됐다: single 119개 0점은 RA/o1/DS=79/74/73,
set 181개 0점은 56/50/78, set 만점은 24/31/41이었다.

핵심 교훈은 **조사한 사실 수보다 조건을 충족한 답 항목의 완성**이다. 전체 후보 목록만
계속 늘리기보다 유망한 후보의 미확인 조건을 채우고, 원문 행·정상 초안·완성된 답 항목을
반환 과정에서 잃지 않게 하는 방향이 실제 개선과 연결됐다.

근거: [300개 교차 비교](analysis/comparison_300_diagnosis.md),
[0점·부분정답 사례](analysis/zero_partial_300_diagnosis.md),
[실행별 원자료 목록](analysis/experiments/run_inventory.json).

### BrowseComp 300개

| 실행 | 정답 | 정확도 | LLM 호출 | 입력 토큰 | 출력 토큰 | 시간 중앙값(초) |
|---|---:|---:|---:|---:|---:|---:|
| RAgent frozen | 32 | 10.67% | 4,376 | 37,115,672 | 2,734,045 | 102.7 |
| search-o1 frozen | 43 | 14.33% | 20,872 | 274,042,815 | 21,186,368 | 1,282.9 |
| 최초 DS frozen | 30 | 10.00% | 13,121 | — | — | 609.1 |
| DS search-main v3 | 37 | 12.33% | 9,980 | — | — | 355.0 |
| DS answer-phase v4 | 38 | 12.67% | 9,786 | 99,245,977 | 7,786,562 | 371.7 |
| DS independent-clues v6 | 28 | 9.33% | 3,930 | 39,295,917 | 2,323,121 | 112.8 |
| DS directed v8 | **44** | **14.67%** | 26,609 | 242,088,528 | 25,262,552 | 1,305.2 |

`—`는 위 표에서 생략한 값이며 0이 아니다. 전체 수치는 아래 실행 목록/JSON에 있다.
v8은 o1보다 정답 1개 많지만 대응 승/패가 18/17이고 호출은 27.5% 많았다.
“안정적인 정확도 우위”나 “토큰·속도 모두 우위”가 확인된 상태가 아니다.
출력 토큰에 추정 reasoning_tokens를 다시 더하지 않는다. latency는 기록된 문항별 시간이며
동시 실행 전체 wall time 또는 동일 하드웨어의 순수 모델 속도가 아니다.

근거: [최초 BrowseComp 진단](analysis/browsecomp_300_diagnosis.md),
[v4](analysis/answer_phase_v4_diagnosis.md), [v6](analysis/independent_clues_v6_diagnosis.md),
[v8 비용·대응 비교](analysis/directed_v8_diagnosis.md).

## 개선 시도와 실패에서 배운 점

### 주요 변경 이력

버전 숫자는 벤치마크/시기마다 재사용됐다. 반드시 **benchmark + tag + 실행 폴더**로 구분한다.

| 시도 | 관측 결과 | 판단 / 남긴 교훈 |
|---|---|---|
| DeepSearchQA 초기 30개 프롬프트·링크 메뉴·정책 변경 | RAgent F1 0.3804; DS menu 0.3825, var1 0.3833 | 작고 혼재된 차이. 태그만 보고 확실한 상승이라 하지 않음 |
| 검색 예산 20회 실험 `s20` | 저장 기록 F1 0.3132/30 | 채택하지 않음. 현재 검색 10회 고정; 어려운 문항의 많은 검색을 인과적 악영향으로 해석하지 않음 |
| `evidence-v1 / v2-fix / v3 / v4` (DeepSearchQA 30개) | F1 0.4040 / 0.3567 / 0.4166 / 0.4171 | 출처 격리·근거 보존 개선과 기능 과잉/비용 문제를 함께 경험. 과거 공통 파서 차이도 있음 |
| `ds_evidence_completion` (DeepSearchQA 300개) | 0.4148 → 0.4550, 만점 86 유지 | 후보별 조건 완성, 원문 행과 정상 초안 보존을 유지할 이유 |
| JSON 선택기와 자유 텍스트 제어 | 초기 선택 probe 14회 모두 선택 없음, invalid 13 | 문법 실패를 탐색 무가치로 오인하지 말 것. native fetch 도구 + 일반 응답 종료로 전환 |
| search-main v3 | 37/300, 빈 답 48 | 검색 후 읽기 단계 분리만으로 종료가 보장되지 않음 |
| answer-phase v4 | 38/300, 빈 답 2 | 도구 없는 최종 작성·재시도는 유지. 출력 복구가 곧 내용 정확도 개선은 아님 |
| fetch-session v5 | 완료 8개 0정답, 463호출, 중앙값 655.5초; 중단 | 반복 선택/독해 비용 급증. 8개 표본으로 전체 정확도 추정 금지 |
| independent-clues v6 | 28/300, 매우 빠르지만 210개에서 실제 페이지 요청 없음 | 초기 A/B 검색 분리만으로 고착을 해결하지 못함. 읽기를 생략해 얻은 속도를 성공으로 삼지 않음 |
| relational v7 | 완료 77개 8정답, 7,550호출, 중앙값 1,532.5초 | 같은 77개 v4는 9정답/2,483호출. 루트마다 반복하는 선택·독해가 비용을 지배 |
| directed v8 | 44/300 | 첫 Next link 직접 실행, 탐색 문맥 전달, 중복 원문 입력 축소. 성능 회복은 있었으나 비용 문제가 남음 |
| batch v9 | 코호트 A 1/10, 427호출 | 복수 native 호출이 실제 서버에서 하나만 나옴. 의도한 일괄 선택이 실행되지 않음 |
| array batch v10 | A 1/10, 401호출 | 진입만 URL 배열, 마무리 전용 대화. 프로토콜 개선을 유지하되 정확도 상승으로 포장하지 않음 |
| notes-only v11 | A 0/10, 428호출 | 진입 해석 제거가 도움 되지 않아 되돌림 |
| balanced URL v12 | B 2/10, 362호출 | 괄호 포함 URL 훼손 수정 유지. 이 점수를 URL 수정만의 인과 효과로 보지 않음 |
| access recovery v13 | B 2/10, 331호출 | 모든 루트 접근 실패 시 대체 루트 선택. 정답 문항만 교체됐고 추가 정책 이득 불명확하여 되돌림 |
| scoped handoff v14 | B 2/10, 382호출 | 짧은 관측/미확인 반환. v12와 같은 정답, 더 높은 비용이라 되돌림 |
| extractive passages v15 | B 2/10, 454호출; v12 대비 호출 +25.4% | 정답 증가 없이 비용 증가. 문단 선택이 부분 단서를 버리는 문제를 확인하고 기본값에서 제외 |

코호트 A: `[3,7,8,13,15,21,22,26,27,32]`.
코호트 B: `[173,240,265,510,716,865,954,1073,1128,1264]`.
B는 A를 제외한 표본에서 점수 확인 전 seed 20260925로 추출했다. 이제 두 코호트 모두 개발 표본이다.
코호트/문항 수가 다른 점수를 직접 순위로 비교하지 않는다.

| 동일 10문항 | RA | o1 | DS v4 | v8 | v9 | v10 | v11 | v12 | v13 | v14 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A 정답 수 | 1 | 1 | 1 | 2 | 1 | 1 | 0 | — | — | — |
| B 정답 수 | 3 | 3 | 1 | 3 | — | — | — | 2 | 2 | 2 |

### 사례 수준에서 확인한 실패 경로

- **읽은 사실의 소실:** q00344의 장학생 PDF에서 필요한 대학 행이 반환 요약에서 생략됨.
  q00026에서도 후보 선수 이름이 원문에 있었지만 반환되지 않음. “없음”과 “선택/요약에서 누락”을 구분한다.
- **후보 하나도 완성하지 못함:** q00838에서 같은 대학 순위 목록의 URL 매개변수만 바꾸며
  개별 대학의 학생 수·국제학생 비율 검증을 미룸. q00158은 정답 도시를 언급해도 추가 조건이 미확인.
- **발견한 입구를 사용하지 않음:** q00687 정부 문서 입구, BrowseComp q00326 인터뷰 URL을
  찾고도 재검색하거나 훼손한 URL로 접근. URL 보존과 선택적 진입을 실제 실행해야 함.
- **잘못된 후보에 고착:** q00975 등에서 모순이 있어도 기존 인물을 계속 검증.
  초기 A/B 검색이나 반환 문구 변경만으로 해결되지 않음.
  현재 메인의 assistant 이력에는 `reasoning_content`를 그대로 넣지 않는다
  (`agent.py::_assistant_message`). 따라서 과거 CoT를 지우는 것만으로 해결된다고 가정하지 않는다.
  검색어·일반 응답·도구 반환 해석은 남고, 직전 reasoning은 하위 탐색 작업의 가설로 전달된다.
- **최종 단계에서 결론 손실:** q00583에서 정상 초안이 최종 재작성 중 사라짐.
  정상 초안은 보존하고, 검색 소진 시 도구 제거+최종 답 요청+빈 답 한 번 재시도를 적용.
- **출처 혼동:** 자식이 부모 사실을 자기 페이지 사실처럼 작성하거나 서로 다른 인물·지역 관계를 합침.
  추출에는 원 질문+현재 원문만, 탐색에는 부모의 가설/하위 작업을 별도로 전달.
- **접근 실패와 내용 실패:** 404/접근 차단/연령 확인/무관한 페이지, 모델 형식 오류, judge 오류는
  다른 실패다. 빈 답을 전부 후처리 버그로 설명하거나 invalid를 전부 환각으로 세지 않음.
- **정답 점수와 근거 품질의 차이:** 일부 baseline 부분점수는 범위를 넘긴 답에서도 발생.
  query를 닮은 spam snippet에서 얻은 정답도 있음. 공식 점수는 유지하되 대표 성공 사례는 원문을 점검.

### 모델-only probe의 역할과 한계

- 복수 native 호출·배열·마무리 진단: 27회, 입력 109,517 / 출력 28,732, 웹·fetch·judge 0회.
  복수 native 호출은 실서버에서 한 개만 반환. 배열 형식은 가능했지만 실제 선택 입력 6개는 모두 단일 URL.
  추출 문구 변경으로 원문에 없는 행이 생성된 변형은 채택하지 않음.
- handoff 비교 24회: 정상 응답 형식은 개선됐지만 사실 혼동이 남았고 실제 v14는 2/10으로 정체.
- 문단 선택: 혼합 지시 16회 후 일관된 계약 8회. 후자는 유효 문단 선택 6회/none 2회/잘못된 ID 0회.
  같은 저장 페이지 8회의 출력 토큰은 20,501 → 9,962. **문단 선택 정확도·전체 비용·정답률 개선의 증거는 아님.**

상세: [실험 일지](analysis/experiments/20260925_iteration_log.md),
[실서버 프로토콜 진단](analysis/batch_protocol_live_diagnosis.md),
[v7 진단](analysis/relational_v7_diagnosis.md), [v9 진단](analysis/batch_v9_diagnosis.md).

## 현재 구현과 진행 상태

### 추가 개발 실험 (2026-09-27)

- **v16 source return:** B 2/10, 411호출, 입력 7,736,649 / 출력 345,087토큰, 중앙 지연 630.4초. 정답은 510/1073으로 바뀌었지만 총점은 개선되지 않았다. 재귀 반환 73회, 컨텍스트 소진 2문항. 원문 자동 반환을 기본값으로 채택하지 않음.
- **v17 dual route:** B 1/10, 469호출, 입력 3,776,090 / 출력 472,448토큰, 중앙 지연 615.2초. 검색 10회를 두 독립 경로에 나눠도 개선되지 않아 제외했다. [스냅샷](analysis/experiments/v17_dual_route/experiment.json).
- **v18 adaptive entry:** 실행 중. 현재 작업 설정은 이 개발 실험이다. v12 압축 reader와 단일 메인 탐색을 유지하며, 진입 모델이 재귀 결과를 받은 뒤 다른 미방문 결과를 추가로 선택할 수 있다. 배치 전체 루트 6개·진입 호출 6회·검색 10회·결과 10개·재귀 노드 12개는 그대로다. 도구 없는 최종 반환 또는 일반 응답 후 메인이 계속한다. baseline은 변경하지 않았다.
- 현재 cache `agent/57-ds-adaptive-entry`, 오프라인 검사 174개 통과. [스냅샷](analysis/experiments/v18_adaptive_entry/experiment.json). 아래 v15 복귀 기록은 이전 상태다.


<!-- LIVE_EXPERIMENT_START -->

**2026-09-27: v15 코호트 B 10개 완료, 기본값 채택 기각.**

| 동일 코호트 B | 정답 | LLM 호출 | 입력 토큰 | 출력 토큰 | 시간 중앙값(초) |
|---|---:|---:|---:|---:|---:|
| RAgent | 3/10 | 140 | 859,420 | 97,147 | 107.4 |
| search-o1 | 3/10 | 566 | 7,024,631 | 595,278 | 957.5 |
| DS v12 | 2/10 | 362 | 2,729,761 | 328,239 | 419.1 |
| DS v15 | 2/10 | 454 | 3,575,929 | 363,631 | 489.5 |

v15 정답은 v12와 같은 240/510이다. 호출 +25.4%, 입력 +31.0%, 출력 +10.8%로,
원문 문단 선택을 기본값으로 채택할 관측 이득이 없다. 재귀 반환은 38회로 v12의 7회보다
많았지만 추가 정답으로 연결되지 않았다. 문단 선택 기록 113회 중 60회가 빈 선택이며
여기에는 알려진 접근 화면을 모델 호출 없이 처리한 8회도 포함된다. 잘못된 ID는 0회,
반환 원문 절단은 2회였다. 유효한 형식이 유용한 근거 선택을 보장하지 않았다.

첫 실행은 5개 완료 후 중단됐다. 당시 코드/설정 해시를 확인하고 미완료 네 문항의 로그를
`interrupted_20260926/`에 보존한 뒤 나머지 5개를 재개했다. 위 비용은 완료 문항 기록의
합계이며 중단된 시도의 비용은 별도다. 재개 날짜·라이브 웹·생성 변동 때문에 이 작은
비교를 방법 전체의 확정적 열세나 순수 지연 시간 효과로 주장하지 않는다.

현재 기본값은 **v12 계열 독해 프롬프트 + 괄호 URL 등록 보존 수정**이다.
`extractive_evidence: false`; 실험 구현·스냅샷은 유지한다. DS cache는
`agent/54-ds-link-registry`, baseline cache는 `agent/35` 그대로다. 복귀 후 165개
오프라인 검사 통과. 이 기본값으로 새 전체 벤치마크를 실행한 것은 아니다.

<!-- LIVE_EXPERIMENT_END -->

실행: [ds_extractive_v15_b](runs/test/20260926-1716_depthsearch_gpt-oss-20b_browsecomp_ds_extractive_v15_b).
최종 진단: [v15 실패 분석](analysis/experiments/v15_diagnosis.md).
스냅샷: [v15_extractive_passages](analysis/experiments/v15_extractive_passages/experiment.json).
기본 계보는 v10 + v12이며 v11/v13/v14와 v15 기본 설정은 되돌렸다.

v15는 `extractive_evidence: true`로 reader의 사실 재작성 대신 `[P#]` 원문 문단 선택을 사용한다.
코드가 ID 범위를 검증하고 해당 문단을 출처와 함께 반환한다. Evidence에 덧붙인 설명과
Connections는 사실 근거로 전달하지 않고, Coverage/Missing/Next links는 탐색 가설로 표시한다.
자식 원문도 자동 병합하며 추가 모델 단계·도구는 없다. 기존 8192토큰 반환 원문 상한과
절단 표시를 유지한다. 유효한 번호라도 필요한 문단을 놓칠 수 있으며, 인터뷰 답변 대신
질문 문장만 고른 실제 사례가 있다. 이 기능은 현재 기본값에서 꺼져 있다.

v15 재개 후 확인한 q01073에서는 원문 P65에 `Puerto Viejo`가 있었지만 reader가
질문의 모든 조건을 충족하는 마을을 확정할 수 없다는 이유로 `Evidence: none`을 반환했다.
이 문단은 정답을 증명하지 않지만 후속 조사할 후보 단서다. 원문 복사 경로가 정확해도
**복사할 부분을 고르는 모델이 불완전한 단서를 버리는 문제**는 남는다. 단순 포맷 성공률로
근거 보존이나 정확도 개선을 주장하지 않는 직접 사례다.

다음 판단 순서:

1. 완료된 v15는 실패 이력으로 보존한다. 요약 문구나 문단 번호 형식만 바꾸는 반복 실험은 중단한다.
2. 접근/후보 발견 실패, 원문→반환 손실, 반환→다음 검색 고착, 최종 답 실패를 분리한다.
3. 다음 구조 가설은 reader의 근거 선별과 링크 탐색 역할을 분리하는 것이다. 예를 들어 선별 요약 없이 원문을 반환하고 reader는 재귀 경로만 고르게 할 수 있으나, 컨텍스트 비용과 절단 손실이 커질 수 있다. 아직 구현·검증된 성과가 아니다.
4. 다음 구조 변경은 확인된 병목 하나를 겨냥한다. 검증 없이 깊이·검색 예산을 늘리거나
   과거 실패한 A/B 강제 검색·반복 선택 구조로 되돌아가지 않는다.
5. 논문용 결과는 모델 2개 × 벤치마크 3개의 실제 완료 상태를 구분하고 정확도와 비용을 함께 보고한다.

## 실행·재개·재현

### 설치와 서버

```powershell
conda activate search_gym
pip install -r requirements.txt
Copy-Item .env.example .env
```

API 키는 `.env`에 로컬로 설정한다. vLLM은 별도 서버에서 실행하고 `conf.yaml`의
`base_url`/`served_model_name`을 실제 서버와 맞춘다. 키나 로컬 endpoint를 논문에 복사하지 않는다.

| 모델 | 현재 코드 프로파일의 서버 파서 |
|---|---|
| gpt-oss | `--enable-auto-tool-choice --tool-call-parser openai --reasoning-parser openai_gptoss` |
| Qwen | `--enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3` |

이는 현재 저장소 프로파일이며 모든 vLLM 버전의 호환성을 보장하는 표가 아니다.
구체적인 서버 문제·sampling은 [serving.py](searchgym/serving.py),
기존 운영 메모는 [이전 README 보존본](analysis/experiments/README_before_research_summary_20260927.md)에 있다.
보존본의 과거 도구/예산 설명보다 이 문서와 해당 run 스냅샷을 우선한다.

### 작은 실험과 재개

```powershell
python test.py --benchmark browsecomp --split test --limit 10 --method depthsearch --tag NEW_TAG
python test.py --benchmark deepsearchqa --split validation --limit 10 --method depthsearch --tag NEW_TAG
python test.py --benchmark evobrowsecomp --split test --limit 10 --method depthsearch --tag NEW_TAG
```

중단된 v15를 재개할 때 실제 사용한 명령(실행 이력):

```powershell
python test.py --benchmark browsecomp --path analysis/experiments/browsecomp_cohort_b_seed20260925.json --limit 10 --method depthsearch --tag ds_extractive_v15_b --resume runs/test/20260926-1716_depthsearch_gpt-oss-20b_browsecomp_ds_extractive_v15_b
```

위 v15 실행은 완료됐으며 현재 기본 프롬프트와 다르다. 위 명령을 현재 설정으로 이어 실행하지 않는다.

- `--resume`: 완료된 문항을 유지하고 중단된 실행을 이어감. **같은 코드·프롬프트·설정일 때만** 사용.
- `--resume --retry-errors`: 빈 답변·실행 오류·판정 오류를 대상으로 재시도하고 전체 결과를 재집계.
  정상적으로 생성된 0점 답을 몰래 재시도하는 옵션이 아님.
- 다른 방법 변경은 새 tag와 DS cache version으로 격리한다. `--resume`과 `--no-cache`는 함께 쓰지 않음.
- `answered`는 정상 탐색 종료 답변, `finalized`는 최종 작성 경로를 거친 상태다. 정답 여부와 별개다.
- 형식/연결 확인: `python -m unittest discover -s tests`; 이 검사는 실제 웹·모델·judge를 호출하지 않음.
- `tests/model.py`와 `probe_*.py`는 실서버를 호출할 수 있다. probe의 형식 성공률은 벤치마크 점수가 아님.

### JevTree 전체 요청·응답 로그 (2026-10-02 추가)

새로 시작하는 `jevtree` 실행은 문항별 `q*/trace.jsonl`에 다음을 저장한다.
탐색 설정과 JEV 평가 문구는 그대로이며, 로그를 위한 추가 API 호출은 없다.

| 이벤트 | 저장 내용 |
|---|---|
| `jev.request` | 실제 요청 `body` 전체: model, state(원 질문·본문/검색 결과), questions(평가 문구·criteria). 인증 헤더는 저장하지 않음 |
| `jev.attempt` | HTTP 시도 시작; 같은 요청의 재시도는 같은 `request_id`, 0부터 시작하는 `attempt`로 연결 |
| `jev.response` | HTTP 상태, 잘리지 않은 `response_text`, 해당 시도 소요시간. 오류 응답·잘못된 JSON도 보존 |
| `jev.error` | 연결/파싱/HTTP 오류, 재시도 여부와 소요시간 |
| `jev.result` | 파싱한 전체 점수, 서버 usage, 성공/실패, 재시도 대기를 포함한 총 소요시간 |
| `jevtree.scored` | 기존 상위 8개 요약과 함께 **평가한 모든 링크**의 `id`, URL, anchor, score를 `link_scores`에 저장 |
| `jevtree.search_end` | 검색별 사용량과 탐색 집계 |

`jev.request.context`의 `search_id`, phase, page_url, parent_url, depth,
chunk_index/chunks로 검색·부모·페이지·링크 배치를 연결한다. state에는 JEV에 실제 보낸
절단 후 텍스트가 저장된다. API 원본 JSON 응답은 `response_text`를 JSON으로 파싱하면 된다.

`reader_stats.jev_requests`는 성공적으로 파싱한 요청 수, `jev_attempts`는 재시도를 포함한
HTTP 시도 수, `jev_failures`는 최종 실패한 요청 수다. 사용량은 검색별로 집계하므로
동시 실행 문항의 호출·입력 토큰이 섞이지 않는다. JEV 캐시 버전은 63으로 구분한다.
버전 63부터 진입·페이지·링크 평가 입력에서 메인 추론을 제거했다. JEV는 원 질문과
검색 결과 또는 현재 페이지로 평가하며, reader에는 기존처럼 메인 추론을 전달한다.
이미 실행 중인 프로세스나 과거 로그에는 소급 적용되지 않는다.

### 저장·분석 규칙

`runs/test/<timestamp>_<method>_<model>_<benchmark>_<tag>/`의 주요 파일:

| 파일 | 용도 |
|---|---|
| `config.json`, 저장 prompt/schema | 당시 실제 조건 |
| `records.jsonl`, `summary.json` | 문항 점수·비용과 집계 |
| `q*/response.json` | 최종 답, 실행 상태, usage |
| `q*/trace.jsonl` | 실제 모델·도구·재귀 사건 |
| `q*/explorer.json`, `tree.svg` | 문서 탐색과 반환 경로 |
| `runs/_cache` | 답변·판정 캐시; 변경한 DS와 baseline을 섞지 않음 |

JSONL은 **literal LF `split('\n')`**로 읽는다. 응답 내부 Unicode 줄 구분자를 자르는
`splitlines()`로 유효 JSON을 손상된 trace로 오인했던 분석 오류가 있었다.
빈 답/오류를 분모에서 제외한 지표와 전체 문항 지표를 혼동하지 않는다.
판정 오류를 정답으로 임의 치환하지 않는다. 손실 사례의 gold 문자열 출현은 사실 검증이 아니며,
짧은 단어·URL·spam·동명이인 출현을 유효 근거로 자동 집계하지 않는다.

```powershell
python analysis/experiments/build_run_inventory.py
python analysis/experiments/compare_runs.py RUN_DIRECTORY --out analysis/experiments/comparison.json
python analysis/experiments/audit_passage_handoff.py RUN_DIRECTORY --out analysis/experiments/passages.json
```

### 코드 지도

- `test.py`: 설정·벤치마크·resume 실행. `conf.yaml`은 모델/데이터/작업 선택.
- `configs/{ragent,search-o1,depthsearch}.yaml`: 방법별 정책·프롬프트·예산.
- `searchgym/agent.py`: 메인 루프, 선택적 진입, 도구 회수, 최종 작성.
- `searchgym/explorer.py`: 자기 페이지 추출, 재귀, 노드 예산, 출처 병합·문단 반환.
- `searchgym/research_state.py`: 관측 출처, 진입/반환 프롬프트·스키마.
- `searchgym/tools/`: MCP 검색·fetch와 파싱. `llm.py`: 모델 호출·프로토콜 처리.
- `searchgym/benchmarks/`, `judge.py`, `scoring.py`: 데이터·판정·점수.
- `runner.py`, `trace.py`, `report.py`: 저장·캐시·계측.
- `analysis/`: 사후 진단. `analysis/experiments/`: 작은 실험 스냅샷·실패 기록.
- `train.py`/GEPA 코드는 남아 있지만 현재 연구 개선 루프에서는 사용하지 않음.

## 전체 실행 목록

아래는 소규모 실패·중단·과거 설정을 숨기지 않기 위한 저장 기록 목록이다.
서로 다른 표본·프로토콜의 단순 순위표가 아니다. 완료된 고유 문항 기준으로 집계한다.
완료 0개 디렉터리까지 포함한 기계 판독 목록은 [run_inventory.json](analysis/experiments/run_inventory.json).

<!-- RUN_INVENTORY_START -->

<details>
<summary>완료 기록이 있는 전체 실행 펼치기 (59개; 초기 smoke·중단 실행 포함)</summary>

| 실행 폴더 | 완료 n | 평균 F1 | 정답 수 | 호출 | 시간 중앙값(초) |
|---|---:|---:|---:|---:|---:|
| [20260907-1935_depthsearch_deepsearchqa_smoke-gptoss](runs/test/20260907-1935_depthsearch_gpt-oss-20b_deepsearchqa_smoke-gptoss) | 1 | 0.0000 | 0 | 0 | 2.8 |
| [20260912-1637_depthsearch_deepsearchqa_smoke](runs/test/20260912-1637_depthsearch_gpt-oss-20b_deepsearchqa_smoke) | 1 | 1.0000 | 1 | 33 | 145.3 |
| [20260912-1642_depthsearch_deepsearchqa_smoke2](runs/test/20260912-1642_depthsearch_gpt-oss-20b_deepsearchqa_smoke2) | 5 | 0.5000 | 2 | 118 | 101.7 |
| [20260912-1707_depthsearch_deepsearchqa_v2](runs/test/20260912-1707_depthsearch_gpt-oss-20b_deepsearchqa_v2) | 5 | 0.4500 | 2 | 285 | 345.9 |
| [20260912-1737_depthsearch_deepsearchqa_v2](runs/test/20260912-1737_depthsearch_gpt-oss-20b_deepsearchqa_v2) | 5 | 0.4400 | 1 | 126 | 117.1 |
| [20260912-1750_depthsearch_deepsearchqa_v4](runs/test/20260912-1750_depthsearch_gpt-oss-20b_deepsearchqa_v4) | 5 | 0.4571 | 2 | 96 | 82.9 |
| [20260912-1757_depthsearch_deepsearchqa_v5](runs/test/20260912-1757_depthsearch_gpt-oss-20b_deepsearchqa_v5) | 5 | 0.3000 | 1 | 108 | 107.0 |
| [20260912-1804_depthsearch_deepsearchqa_v6](runs/test/20260912-1804_depthsearch_gpt-oss-20b_deepsearchqa_v6) | 5 | 0.4714 | 1 | 236 | 319.5 |
| [20260912-1813_depthsearch_deepsearchqa_v7](runs/test/20260912-1813_depthsearch_gpt-oss-20b_deepsearchqa_v7) | 5 | 0.2000 | 1 | 225 | 188.9 |
| [20260912-1829_depthsearch_deepsearchqa_v8](runs/test/20260912-1829_depthsearch_gpt-oss-20b_deepsearchqa_v8) | 5 | 0.4000 | 2 | 176 | 182.6 |
| [20260912-1838_depthsearch_deepsearchqa_v9](runs/test/20260912-1838_depthsearch_gpt-oss-20b_deepsearchqa_v9) | 5 | 0.4000 | 2 | 244 | 284.2 |
| [20260912-1851_ragent_deepsearchqa_n30](runs/test/20260912-1851_ragent_gpt-oss-20b_deepsearchqa_n30) | 30 | 0.3306 | 7 | 454 | 102.9 |
| [20260912-1909_ragent_deepsearchqa_n30b](runs/test/20260912-1909_ragent_gpt-oss-20b_deepsearchqa_n30b) | 14 | 0.1405 | 0 | 205 | 65.6 |
| [20260912-1913_ragent_deepsearchqa_n30c](runs/test/20260912-1913_ragent_gpt-oss-20b_deepsearchqa_n30c) | 30 | 0.2650 | 4 | 619 | 95.4 |
| [20260912-1933_search-o1_deepsearchqa_n30d](runs/test/20260912-1933_search-o1_gpt-oss-20b_deepsearchqa_n30d) | 30 | 0.0997 | 0 | 642 | 226.8 |
| [20260912-2023_depthsearch_deepsearchqa_n30e](runs/test/20260912-2023_depthsearch_gpt-oss-20b_deepsearchqa_n30e) | 30 | 0.1452 | 2 | 588 | 85.5 |
| [20260912-2055_ragent_deepsearchqa_f1](runs/test/20260912-2055_ragent_gpt-oss-20b_deepsearchqa_f1) | 30 | 0.3804 | 7 | 463 | 127.0 |
| [20260912-2115_search-o1_deepsearchqa_f1](runs/test/20260912-2115_search-o1_gpt-oss-20b_deepsearchqa_f1) | 30 | 0.2645 | 5 | 697 | 629.7 |
| [20260912-2236_depthsearch_deepsearchqa_f1](runs/test/20260912-2236_depthsearch_gpt-oss-20b_deepsearchqa_f1) | 30 | 0.3486 | 6 | 1,424 | 313.7 |
| [20260914-1146_search-o1_deepsearchqa_f2](runs/test/20260914-1146_search-o1_gpt-oss-20b_deepsearchqa_f2) | 30 | 0.3267 | 6 | 1,214 | 457.4 |
| [20260914-1311_depthsearch_deepsearchqa_e4](runs/test/20260914-1311_depthsearch_gpt-oss-20b_deepsearchqa_e4) | 30 | 0.3462 | 5 | 970 | 214.8 |
| [20260914-1407_depthsearch_deepsearchqa_menu](runs/test/20260914-1407_depthsearch_gpt-oss-20b_deepsearchqa_menu) | 30 | 0.3825 | 8 | 1,006 | 237.4 |
| [20260914-1510_depthsearch_deepsearchqa_menu2](runs/test/20260914-1510_depthsearch_gpt-oss-20b_deepsearchqa_menu2) | 30 | 0.2709 | 4 | 1,359 | 291.8 |
| [20260914-1621_depthsearch_deepsearchqa_var1](runs/test/20260914-1621_depthsearch_gpt-oss-20b_deepsearchqa_var1) | 15 | 0.2660 | 2 | 797 | 346.2 |
| [20260914-1745_depthsearch_deepsearchqa_var1](runs/test/20260914-1745_depthsearch_gpt-oss-20b_deepsearchqa_var1) | 30 | 0.3833 | 8 | 1,476 | 329.9 |
| [20260914-1957_depthsearch_deepsearchqa_s20](runs/test/20260914-1957_depthsearch_gpt-oss-20b_deepsearchqa_s20) | 30 | 0.3132 | 5 | 1,159 | 259.0 |
| [20260914-2108_depthsearch_deepsearchqa_stop](runs/test/20260914-2108_depthsearch_gpt-oss-20b_deepsearchqa_stop) | 30 | 0.2758 | 4 | 1,027 | 228.1 |
| [20260915-1002_depthsearch_deepsearchqa_keep](runs/test/20260915-1002_depthsearch_gpt-oss-20b_deepsearchqa_keep) | 30 | 0.3664 | 7 | 1,005 | 250.1 |
| [20260915-1045_depthsearch_deepsearchqa_policy](runs/test/20260915-1045_depthsearch_gpt-oss-20b_deepsearchqa_policy) | 21 | 0.3515 | 5 | 679 | 221.3 |
| [20260915-1111_depthsearch_deepsearchqa_flow](runs/test/20260915-1111_depthsearch_gpt-oss-20b_deepsearchqa_flow) | 20 | 0.1967 | 2 | 437 | 106.8 |
| [20260915-1125_depthsearch_deepsearchqa_flow](runs/test/20260915-1125_depthsearch_gpt-oss-20b_deepsearchqa_flow) | 17 | 0.3193 | 4 | 483 | 187.9 |
| [20260915-1141_depthsearch_deepsearchqa_probe](runs/test/20260915-1141_depthsearch_gpt-oss-20b_deepsearchqa_probe) | 30 | 0.2751 | 4 | 968 | 195.0 |
| [20260915-1431_depthsearch_deepsearchqa_evidence-v1](runs/test/20260915-1431_depthsearch_gpt-oss-20b_deepsearchqa_evidence-v1) | 30 | 0.4040 | 8 | 968 | 296.9 |
| [20260915-1557_depthsearch_deepsearchqa_evidence-v2](runs/test/20260915-1557_depthsearch_gpt-oss-20b_deepsearchqa_evidence-v2) | 1 | 0.0000 | 0 | 2 | 8.2 |
| [20260915-1602_depthsearch_deepsearchqa_evidence-v2-fix](runs/test/20260915-1602_depthsearch_gpt-oss-20b_deepsearchqa_evidence-v2-fix) | 30 | 0.3567 | 8 | 851 | 337.5 |
| [20260915-2139_depthsearch_deepsearchqa_evidence-v3](runs/test/20260915-2139_depthsearch_gpt-oss-20b_deepsearchqa_evidence-v3) | 30 | 0.4166 | 8 | 1,036 | 366.6 |
| [20260916-1108_depthsearch_deepsearchqa_evidence-v4](runs/test/20260916-1108_depthsearch_gpt-oss-20b_deepsearchqa_evidence-v4) | 30 | 0.4171 | 9 | 1,091 | 402.6 |
| [20260916-1542_depthsearch_deepsearchqa_smoke](runs/test/20260916-1542_depthsearch_gpt-oss-20b_deepsearchqa_smoke) | 3 | 0.6667 | 2 | 65 | 259.2 |
| [20260916-1543_ragent_deepsearchqa_main](runs/test/20260916-1543_ragent_gpt-oss-20b_deepsearchqa_main) | 300 | 0.3919 | 63 | 4,783 | 120.8 |
| [20260916-1846_search-o1_deepsearchqa_main](runs/test/20260916-1846_search-o1_gpt-oss-20b_deepsearchqa_main) | 300 | 0.4424 | 74 | 15,959 | 1064.4 |
| [20260918-0747_depthsearch_deepsearchqa_main](runs/test/20260918-0747_depthsearch_gpt-oss-20b_deepsearchqa_main) | 300 | 0.4148 | 86 | 10,334 | 352.4 |
| [20260919-0052_depthsearch_deepsearchqa_ds_evidence_completion](runs/test/20260919-0052_depthsearch_gpt-oss-20b_deepsearchqa_ds_evidence_completion) | 300 | 0.4550 | 86 | 12,626 | 486.0 |
| [20260919-1621_search-o1_browsecomp_paper_frozen_v1](runs/test/20260919-1621_search-o1_gpt-oss-20b_browsecomp_paper_frozen_v1) | 300 | 0.1433 | 43 | 20,872 | 1282.9 |
| [20260920-2130_ragent_browsecomp_paper_frozen_v1](runs/test/20260920-2130_ragent_gpt-oss-20b_browsecomp_paper_frozen_v1) | 300 | 0.1067 | 32 | 4,376 | 102.7 |
| [20260921-0016_depthsearch_browsecomp_paper_frozen_v1](runs/test/20260921-0016_depthsearch_gpt-oss-20b_browsecomp_paper_frozen_v1) | 300 | 0.1000 | 30 | 13,121 | 609.1 |
| [20260921-2144_depthsearch_browsecomp_ds_search_main_v3](runs/test/20260921-2144_depthsearch_gpt-oss-20b_browsecomp_ds_search_main_v3) | 300 | 0.1233 | 37 | 9,980 | 355.0 |
| [20260922-0859_depthsearch_browsecomp_ds_answer_phase_v4](runs/test/20260922-0859_depthsearch_gpt-oss-20b_browsecomp_ds_answer_phase_v4) | 300 | 0.1267 | 38 | 9,786 | 371.7 |
| [20260922-1904_depthsearch_browsecomp_ds_fetch_session_v5](runs/test/20260922-1904_depthsearch_gpt-oss-20b_browsecomp_ds_fetch_session_v5) | 8 | 0.0000 | 0 | 463 | 655.5 |
| [20260923-1815_depthsearch_browsecomp_ds_independent_clues_v6](runs/test/20260923-1815_depthsearch_gpt-oss-20b_browsecomp_ds_independent_clues_v6) | 5 | 0.2000 | 1 | 87 | 120.7 |
| [20260923-1829_depthsearch_browsecomp_ds_independent_clues_v6](runs/test/20260923-1829_depthsearch_gpt-oss-20b_browsecomp_ds_independent_clues_v6) | 300 | 0.0933 | 28 | 3,930 | 112.8 |
| [20260923-2239_depthsearch_browsecomp_ds_relational_v7](runs/test/20260923-2239_depthsearch_gpt-oss-20b_browsecomp_ds_relational_v7) | 77 | 0.1039 | 8 | 7,550 | 1532.5 |
| [20260924-0737_depthsearch_browsecomp_ds_directed_v8](runs/test/20260924-0737_depthsearch_gpt-oss-20b_browsecomp_ds_directed_v8) | 300 | 0.1467 | 44 | 26,609 | 1305.2 |
| [20260925-1231_depthsearch_browsecomp_ds_batch_v9-2](runs/test/20260925-1231_depthsearch_gpt-oss-20b_browsecomp_ds_batch_v9-2) | 10 | 0.1000 | 1 | 427 | 440.5 |
| [20260925-1337_depthsearch_browsecomp_ds_batch_v9](runs/test/20260925-1337_depthsearch_gpt-oss-20b_browsecomp_ds_batch_v9) | 10 | 0.1000 | 1 | 401 | 594.2 |
| [20260925-1701_depthsearch_browsecomp_ds_notes_v11](runs/test/20260925-1701_depthsearch_gpt-oss-20b_browsecomp_ds_notes_v11) | 10 | 0.0000 | 0 | 428 | 475.3 |
| [20260925-1728_depthsearch_browsecomp_ds_links_v12_b](runs/test/20260925-1728_depthsearch_gpt-oss-20b_browsecomp_ds_links_v12_b) | 10 | 0.2000 | 2 | 362 | 419.1 |
| [20260925-2245_depthsearch_browsecomp_ds_access_v13_b](runs/test/20260925-2245_depthsearch_gpt-oss-20b_browsecomp_ds_access_v13_b) | 10 | 0.2000 | 2 | 331 | 361.0 |
| [20260925-2313_depthsearch_browsecomp_ds_handoff_v14_b](runs/test/20260925-2313_depthsearch_gpt-oss-20b_browsecomp_ds_handoff_v14_b) | 10 | 0.2000 | 2 | 382 | 454.9 |
| [20260926-1716_depthsearch_browsecomp_ds_extractive_v15_b](runs/test/20260926-1716_depthsearch_gpt-oss-20b_browsecomp_ds_extractive_v15_b) | 10 | 0.2000 | 2 | 454 | 489.5 |

</details>

<!-- RUN_INVENTORY_END -->
