# search_gym

웹 검색 에이전트에서 **탐색량과 컨텍스트 소비를 분리**하면 어떻게 되는가. 세 방법을
공통 실행기에서 비교한다. 현재는 GEPA 없이 프롬프트·문서 처리·재귀 정책을 개선한다.

| | 메인 모델의 도구 | 페치 결정 | 페치 결과가 메인 컨텍스트에 | 깊이 |
|---|---|---|---|---|
| **RAgent** | `search` + `fetch` | 메인 모델이 선별 | 원문 (jina 마크다운) | 1 |
| **DepthSearch** | `search` | 하위 읽기 노드가 선택 후 재귀 | 출처별 근거·관계·미확인 항목 | N |
| **Search-o1** | `search` | 검색당 상위 k개 자동 | 페이지별 explorer 요약 | 1 |

RAgent와 DepthSearch는 같은 웹 검색·페치 도구를 사용하고 검색 결과에서 진입 페이지를
고른다. DepthSearch에는 검색과 읽기의 역할 분리, 재귀 reader, 출처별 근거 보존과
전용 프롬프트가 추가된다. 현재 비교는 이 구성 전체의 비교이며, 재귀만의 효과를
측정하려면 다른 기능을 고정한 depth 1 대 depth 3 실험이 별도로 필요하다.

```
RAgent            → DepthSearch(depth 1)    원문 vs 요약      컨텍스트 축
DepthSearch(1)    → DepthSearch(3)          평면 vs 재귀      깊이 축
Search-o1                                   선행연구 참조점
```

Search-o1 은 원 논문대로 페치를 모델 선택으로 두지 않으므로 도구가 하나 적다. 그래서
숫자 비교의 축이 아니라 인용 참조점으로 둔다. 같은 검색 예산을 쓴다. 현재 DepthSearch는
근거 보존에 맞춘 전용 메인 프롬프트를 사용하므로, 방법별 정책까지 포함한 비교다.

## DepthSearch: 관계를 따라 읽고 근거를 부모에게 반환

현재 `relational_reading: true`에서는 메인이 검색을 계획하고, 검색 결과를 받은 하위
노드는 native `web_fetch`로 필요한 페이지를 읽는다. 페이지 내부 링크는 기존 explorer가
재귀로 따라간다. 반환 근거를 본 하위 노드는 같은 검색 결과의 다른 페이지를 읽거나
일반 응답으로 종료한다. 검색당 진입 페이지 하나로 고정하지 않으며, 종료 후 메인이
반드시 다시 호출되어 다음 검색이나 답변을 결정한다. 독립 A/B 고정 검색은 꺼져 있다.

출처 등록과 노트 저장은 코드로 수행하며 별도의 상태 갱신 LLM 호출은 없다. 페이지마다
독립 controller를 추가하지 않는다. 진입 판단과 재귀 탐색에는 모델 호출이 필요하므로
v6보다 호출 수가 늘 수 있다. 역할 분리·범위 제한·중복 추출 방지를 구조로 적용하며,
유용한 출처 선택과 관계 완성 여부는 모델 판단이다. 정확도 상승은 실험으로 확인해야 한다.

- 진입 후보는 현재 검색 결과의 미방문 페이지다. 하위 읽기 노드는 URL 또는 출처 ID를
  `url` 인자로 넣는다. 이미 읽었거나 실패한 페이지는 선택지에서 제외한다. 과거 결과는
  메인 이력과 출처 기록에 보존하지만 현재 진입 메뉴에 전부 반복 삽입하지 않는다.
- 페이지 내부에서만 발견한 링크는 진입 대상으로 승격하지 않는다. 해당 reader의
  재귀 경로를 따르며 depth 2 이상 노드 예산·부모별 자식 제한을 적용한다.
- 진입 페이지는 depth 1이며 자식 2개 제한이나 전체 확장 노드 12개를 차감하지 않는다.
  문서 최대 깊이는 3이다. 한 진입 페이지의 확장은 최대 6개다.
- 부모의 `Next links`에서 선택 URL에 해당하는 한 줄 설명을 찾아 자식의 탐색 작업으로
  전달한다. 도구 인자는 늘리지 않는다. 매칭되는 설명이 없으면 원 질문을 사용한다.
  검색어를 추출 조건으로 사용하는 fallback과 선택적 `Check:` 의존은 제거했다.
- 추출은 원 질문과 현재 페이지를 기준으로 한다. 링크 목적과 부모 가설은 추출 입력에
  넣지 않는다. 탐색은 맡은 관계가 확인/반박됐거나 유효 경로가 없으면 종료하도록 지시한다.
- `Connections`와 `Missing`을 출처별로 모아 반환 앞부분에 보여준다. 이는 reader의
  해석이며 원문 근거와 구분한다. 코드가 새로운 관계를 추론하거나 검증하지는 않는다.
- 메인 턴 상한은 40, reader 탐색 턴 상한은 6이다. 검색 10회 소진 후에는 도구를 제거하고
  `tool_choice="none"`으로 답을 요청하며, 빈 답이면 한 번 더 요청한다. 마지막 검색도
  하위 읽기 세션을 마친 다음 최종화한다. 검색 소진으로 마지막 결과의 읽기를 생략하지 않는다.
- 검색 한도 10회·결과 수 10개는 그대로다. 읽기 폭과 탐색 정책 변화도 방법의 일부이므로
  재귀만의 효과로 해석하지 않으며 fetch 수·모델 호출 수·시간을 함께 보고한다.

`relational_reading: false`, `independent_clues: false`, `depthsearch_control: true`는
이전 선택·상태 갱신 모드다. `relational_reading: false`, `independent_clues: true`는 v6 모드다.
`python probe_entry_decisions.py`는 **이전 선택기 전용**이며 현재 정책의 검사가 아니다.
이전 실행의 fetch/skip/invalid 사례 9개를 메뉴
크기별로 뽑아 선택과 오류 복구만 진단한다. 최대 27회 모델 호출이며 검색·fetch·채점은
실행하지 않는다. `--dry-run`은 외부 호출 없이 사례만 표시한다. 정확도 측정은 아니다.

`configs/depthsearch.yaml`의 `extract_before_expand: true`가 기본이다.

1. 현재 페이지의 관련 사실·전체 목록·표 행을 추출 호출로 먼저 저장한다.
   추출 입력에는 현재 페이지 원문을 제공하며 도구는 없다.
   현재 관계 탐색 모드는 원 질문·현재 원문만 전달한다. 검색어·부모의 확인 작업·부모
   노트·누적 추론은 추출 입력에서 제외한다.
2. reader 본문의 링크(메뉴 밖 링크 포함), 또는 읽고 있는 사이트 내부를 따라 확장한다.
3. 부모와 자식의 페이지별 노트를 코드로 합쳐 메인에 반환한다. 부모의 최종 요약에
   자식 내용을 다시 적어야만 살아남는 구조가 아니다.

노트는 Page / Evidence / Missing / Next links로 출처·값·누락 항목을 구분한다.
`Expand: yes/no`는 별도의 탐색 제어 값으로 파싱하며 근거 본문에서 제거한다.
`prune_unhelpful_branches: true`에서는 유용한 다음 경로가 없거나 내용이 그대로
반복되는 페이지의 하위 확장을 중단한다. 정답 사실이 없는 색인이라도 관련 레코드로
가는 경로가 있으면 확장할 수 있다. 연도 불일치는 일괄 URL 차단 규칙으로 처리하지
않으며, 요청한 연도로 가는 링크가 있는지 reader가 판단한다.
완료된 페이지의 중복 요청은 저장된 노트를 재사용하며 확장 노드를 차감하지 않는다.
다른 URL의 동일 원문도 추출 호출 전에 감지한다. 완전하게 끝난 자기 페이지의 추출만
재사용하며 원래 출처 URL을 유지한다. 별도 출처의 독립된 뒷받침으로 세지 않는다.
실패하거나 잘린 추출은 동일 원문 캐시에 넣지 않는다. 동일 판정은 공백·표 행을 보존한
본문의 정확한 일치로 하며 Reader의 URL 메타데이터만 제외한다.
진행 중인 조상은 다시 열지 않는다. 링크 확장 범위는 그대로 유지한다.

빈 reader 출력·잘린 출력·오류는 관련 근거 없음과 구분하고, 원문으로 한 번 복구한다.
부분 결과는 복구 실패나 자식 실패에도 보존된다. 추출을 먼저 하므로 확장 가능한
페이지에는 추가 모델 호출이 생길 수 있다. 실제 성능과 비용은 다음 실행에서 비교한다.

DepthSearch의 검색 정책은 출처·주제와 소수의 식별어로 진입 페이지를 먼저 찾고,
세부 조건은 reader로 확인하도록 바뀌었다. 검색 결과가 빗나가면 제약을 줄이거나
출처를 바꾸고, 확인된 누락 항목에 대해서만 검색을 좁힌다. 비교·교집합의 작업용
근거표에는 값·연도·단위·대상/규격·출처·누락을 유지하도록 프롬프트를 구성했다.
최종 답에서는 사용자가 요청한 형식을 따른다. 이는 모델 정책이며 사실 검증을
코드로 보장한다는 뜻은 아니다.

최종 답변의 특수 토큰을 제거할 때 길이로 답을 버리지 않는다. 실제 도구 호출
헤더와 추론 채널을 구분하고, 원문과 정리 결과를 함께 기록한다.
서버가 `tool_calls` 대신 본문에 Harmony 호출을 반환하면, 제공된 도구 이름과
완전한 JSON 객체가 확인되는 단일 호출만 정상 도구 경로로 복구한다. 인자·예산
검사는 그대로 적용한다. DepthSearch의 복구할 수 없는 빈 턴은 문항당 두 번까지 도구를 유지한 채
재시도한 뒤 최종 답변 복구로 넘어간다. `recovered_tool_call`과 `run.resume_tools`
로그로 각각의 경로를 확인할 수 있다.

```bash
python test.py --benchmark browsecomp --split test --limit 10 --method depthsearch --tag ds_relational_v7
python -m unittest discover -s tests -p "test_*.py" -v
```

두 번째 명령은 가짜 모델·도구·판정만 사용하는 회귀 검사다. 외부 API를 호출하지 않는다.
캐시 버전을 올렸으므로 첫 번째 명령에서 이전 구현의 실행 결과는 재사용되지 않는다.
기존 run 기록은 변경하지 않는다.

### v4: 출처별 추출과 재귀 reader에 집중

- 메인 도구는 `web_search`, `web_fetch`뿐이다. 별도 계산·표 연산·문서 재조회·상태 관리·
  가지 재개 도구는 제거했다. Reader는 추출 단계에서 도구 없이 현재 원문만 읽고,
  탐색 단계에서 `web_fetch`로 페이지 링크 또는 관찰한 같은 사이트의 주소를 연다.
- 검색 통제값은 **세 방법 모두 최대 10회, 반환 결과 10개**다.
  `search_top_k: 5`는 search-o1의 자동 페치 수다. 차단 결과를 추가 검색으로 보충하지 않는다.
- CSV/PDF 읽기는 공통 `web_fetch` 내부에 유지한다. CSV 헤더·빈 셀·행 순서를 보존하고,
  PDF는 페이지 번호와 텍스트를 추출하며 과도한 배치 공백을 줄인다. 네이티브 파싱 실패 시
  기존 Jina 경로로 한 번 전환한다. Excel 전용 파서는 제거했다.
- 공통 원문 토큰 상한은 32768이다. 넘으면 절단 사실을 표시하며 꼬리 부분을 읽었다고
  가정하지 않는다. 스캔 PDF나 큰 표 전체의 정합성을 자동으로 해결하는 기능은 없다.
- 재귀 깊이 3, 문항 전체 확장 노드 12, 진입 페이지당 6, reader당 자식 2 제한을 유지한다.
  링크 개수에 따른 자식 수 확대와 자식별 사전 균등 분배를 제거했다. 분배 때문에 깊이 2에서
  자식의 재귀 예산이 소진되던 문제를 고쳤다. 실패한 페치는 노드를 돌려준다.
- 현재 페이지 근거는 먼저 저장하고, 자식 근거는 출처별로 병합한다. 부모의 추론은 자식의
  추출 입력에 들어가지 않는다. 반환 형식은 Evidence / Coverage / Missing / Next links로,
  확인한 사실과 목록의 범위, 미확인 조건, 다음 링크를 구분한다.
- 메인 프롬프트는 후보 범위 확인, 한 번에 하나의 검색 목적, 조건별 근거 비교를 지시한다.
  후보를 찾지 못한 것과 탈락을 구분하며, 최종 답변 호출에는 수집한 근거를 전달한다.
  유효한 짧은 답은 보존하고 계획문·도구 호출 잔해는 답으로 인정하지 않는다.

파일 파서·도구 프로토콜·오염 필터는 공통 변경이다. 최종 비교용 RAgent/Search-o1은 같은
코드 버전으로 다시 실행해야 한다. 검색 예산은 같지만 총 페치·추론 비용까지 같다는 주장은
하지 않는다. F1과 비용을 함께 보고하며, 성능 향상 여부는 다음 실제 실행으로 확인한다.

새 결과를 볼 때:

- `summary.json`의 **f1은 전체 문항 기준**이다. 빈 응답·판정 실패도 0점으로 포함한다.
  이전처럼 유효한 판정만 평균한 값은 `f1_valid_only`이며 `score_denominator`도 남긴다.
- `reader_stats`에서 `empty_output`, `truncated`, `reader_error`, `navigation_errors`,
  `no_relevant_evidence`, `recovery_attempts`, `pruned_branches`, `repeated_content`를
  확인한다. 발생하지 않은 키는 없을 수 있다.
- `explorer.json`에는 페이지 자체의 `own_information`과 자식까지 합친 `information`이
  따로 남는다. `extraction_state`는 reader의 완료 여부이며 정답 여부가 아니다.
- `trace.jsonl`의 `explorer.input`은 탐색 문맥, `explorer.extract_input`은 각 추출·복구
  요청의 실제 입력이다. `explorer.response`는 파싱 전 본문·사고·`finish_reason`이다.
  `expand.pruned`와 `explorer.json`의 `expansion_stop_reason`에서 가지 중단 사유를
  확인한다. `llm.response`와 `run.final_response`의 `raw_text`, `cleanup_changed`로
  원래 빈 답인지 정리 중 바뀐 답인지 구분한다. 원본 입력 로그는 용량이 클 수 있다.
- 깊이별 `not_found` 비율은 모델이 붙인 상태의 대용 지표다. 상태 프롬프트를 바꾼
  실행끼리 이 수치만으로 확장의 품질이 좋아졌다고 해석하지 않는다.

- **학생** — vLLM으로 띄운 로컬 오픈 모델. 확장 사고는 항상 켠다.
- **explorer** — 같은 모델. 페치한 문서를 읽고 요약하며, 필요하면 링크를 따라 재귀한다.
- **교사** — GEPA reflection LM. 실행 궤적을 읽고 프롬프트를 고쳐 쓴다.
- **판정** — Gemini. structured output으로 정답 파트별 boolean을 받는다.

## 구조

```
conf.yaml               무엇을 돌릴지만 — 방법 · 모델 · 벤치마크
configs/
  ragent.yaml           방법별 예산과 프롬프트
  search-o1.yaml
  depthsearch.yaml
  gepa.yaml             교사 · 컴포넌트별 메타프롬프트 · 피드백 · GEPA 예산
test.py                 평가
train.py                GEPA 최적화
tests/                  단위 확인 — search · fetch · model · explorer
                                  judge · reflection · tree
searchgym/
  llm.py                vLLM 래퍼 (생성 + /tokenize)
  agent.py              메인 추론 루프. 방법에 따라 도구와 검색 결과 가공이 갈린다
  explorer.py           문서 읽기 + 요약 + 재귀 확장 + 노드 예산
  tools/                Serper·Jina를 MCP로 노출 + 클라이언트(자동 페치 포함)
  benchmarks/           문항 로딩 + 판정 프롬프트·스키마 (통일 레코드 형식)
  serving.py            모델별 vllm serve 프로파일
  tree.py               문항별 탐색 궤적 그림 (tree.svg)
  judge.py · scoring.py · runner.py · report.py · gepa.py · config.py · trace.py
data/<벤치>/            raw.* -> source/train/validation/test.json
scripts/                build_splits.py · contamination.py
```

## 설치

```bash
conda activate search_gym
pip install -r requirements.txt
cp .env.example .env      # SERPER / JINA / GOOGLE / ANTHROPIC 키를 채운다
```

`openai` 는 1.60 이상이어야 한다(`AsyncOpenAI`). 구버전이 깔려 있으면 import 단계에서 죽는다.

## 모델은 팟에서, 나머지는 전부 로컬에서

**이 저장소는 모델을 띄우지 않는다.** vLLM 은 RunPod 등의 기성 이미지로 팟에서 돌고,
도구·판정·교사·로그는 전부 로컬이다.

```
로컬                                              팟(GPU)
────────────────────────────────────────          ──────────────
MCP 서버(stdio 서브프로세스)
  └ web_search / web_fetch 스키마
        │
        ▼  스키마를 OpenAI tools=[...] 로 변환
   test.py / train.py ── POST /v1/chat/completions ──▶  vLLM
                          { messages, tools: [...] }      │
        ◀───────── { tool_calls: [...] } ─────────────────┘
        │
        ▼  ← 여기서 **우리가** MCP 로 실제 실행
   {"role":"tool", "content": 결과}  →  다시 POST
```

**팟은 MCP 도, Serper·Jina 키도 모른다.** 도구는 요청 본문의 `tools` 로만 전달되고,
실행은 로컬에서 한다. 덕분에 검색 예산 하드캡과 Search-o1 정제가 가능하다.

대신 팟의 vLLM 실행 인자에 아래가 반드시 있어야 한다. 없으면 툴콜이 파싱되지 않아
모델이 도구 호출을 평문으로 뱉고 **조용히 망가진다.**

| 키 | 모델 | 필수 인자 |
|---|---|---|
| `qwen` | Qwen/Qwen3.5-9B | `--enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3` |
| `gpt-oss` | openai/gpt-oss-20b | `--enable-auto-tool-choice --tool-call-parser openai --reasoning-parser openai_gptoss` |
| `gemma` | google/gemma-4-12B-it | `--enable-auto-tool-choice --tool-call-parser gemma4 --reasoning-parser gemma4` |

팟이 다른 이름으로 서빙하면 `conf.yaml` 의 `served_model_name` 으로 맞춘다.

엔드포인트는 SSH 터널로 붙이는 것을 권한다 — `base_url` 을 그대로 둘 수 있고, 프록시
타임아웃과 공개 노출을 둘 다 피한다.

```bash
ssh -N -L 8000:localhost:8000 root@<pod-ip> -p <pod-ssh-port>
```

**확장 사고는 항상 켠다.** 모델마다 기본값이 반대라 명시하지 않으면 비교가 성립하지
않고, Search-o1 의 결과가 추론 모델을 전제로 하기 때문이다(논문 §4.4: *ordinary LLMs
cannot effectively utilize search as a tool*). gpt-oss 만 시스템 프롬프트 한 줄로 강도를
받고 나머지는 `chat_template_kwargs` 로 받는다 — 이 분기는 `serving.py` 의 프로파일에
있고 설정에는 없다.

gemma-4 는 사고와 툴콜을 동시에 켜려면 팟 템플릿에 셋이 더 필요하다 —
`VLLM_USE_V2_MODEL_RUNNER=0`, vLLM 저장소의 `tool_chat_template_gemma4.jinja`,
그리고 `transformers==5.14.*`. 앞뒤 사정은 `serving.py` 의 `notes` 에 적어 두었다.

## 확인

모델을 태우기 전에 도구와 엔드포인트부터 본다. **출력은 가공하지 않는다 — 화면에
나오는 것이 곧 모델이 받는 문자열이다.**

```bash
python tests/model.py                      # /v1/models · /tokenize · 사고 분리 · 툴콜
python tests/search.py "검색어"
python tests/fetch.py <url>                # 링크 없이 몇 자인가
python tests/fetch.py <url> --links        # 링크 목록 켜면 몇 자가 되는가
python tests/explorer.py "검색어" --tree   # search -> 페치 -> explorer 전 경로
python tests/judge.py --prompt             # 판정 모델이 정답/오답/회피를 어떻게 찍나
python tests/reflection.py --dry           # GEPA 교사에게 가는 텍스트 (교사 호출 없이)
python tests/reflection.py                 # 실제로 한 번 제안받아 본다
python tests/tree.py --demo                # 궤적 그림 예시
```

`tests/judge.py` 는 같은 문항에 정답·오답·"못 찾았다" 셋을 넣어 본다. 여기서 정답이
오답으로 찍히면 채점 프롬프트나 `answer_parts` 문제지 에이전트 문제가 아니다.

`tests/reflection.py` 는 **GEPA 예산을 태우기 전에** 교사가 실제로 무엇을 보는지
읽어 보는 용도다. 피드백 텍스트가 부실하면 GEPA 는 눈감고 최적화한다.

`--links`(Jina 의 `X-With-Links-Summary`)는 **기본 off 로 둔다.** 본문 마크다운에 이미
인라인 링크가 들어 있어 explorer 가 그걸로 확장하고, 링크 요약은 그것을 맥락 없이 한 번
더 모아둔 중복이기 때문이다. 실측으로 위키 페이지 하나에 링크가 1,182개 · 28K 토큰이라
켜면 문서 예산을 통째로 먹는다.

> 실측 크기: iana 5.5K자 · bbc 24K · python docs 75K · **wikipedia 233~313K자**.
> 위키 한 장이 이미 `max_document_tokens`(50K 토큰)의 1.5배다. 절단은 앞에서부터
> 남기는 단순 절단이다. DepthSearch v3에서는 저장 원문 조회로 꼬리를 다시 읽을 수 있다.

## 데이터

모든 벤치마크가 **같은 레코드 형식**을 쓴다. 새 벤치마크는 원본을 이 형식으로 바꾸기만
하면 실행·채점 경로를 건드릴 필요가 없다.

```json
{
  "index": 0,
  "question": "...",
  "answer": "...",
  "answer_type": "single" | "set",
  "category": "Sports",
  "answer_parts": ["...", "..."]
}
```

`answer_type` 이 판정 방식을 정한다. `single` 이면 boolean 하나(→ f1 == accuracy),
`set` 이면 파트별 boolean + 여분 답 목록(→ f1이 부분점수로 움직인다). 부분점수는 GEPA의
Pareto 선택에도 중요하다 — 점수가 0/1로만 움직이면 valset 30문항에서 동점이 쏟아져
frontier가 뭉개진다.

```bash
python scripts/build_splits.py deepsearchqa --force                        # 30/30/300
python scripts/build_splits.py evobrowsecomp --train 50 --val 50 --force   # 50/50/300
python scripts/build_splits.py browsecomp --force                          # 30/30/300
```

BrowseComp 원본은 canary XOR 로 암호화된 CSV 라서 먼저 내려받아 복호화해야 한다.
`scripts/decrypt_browsecomp.py` 가 OpenAI simple-evals 와 같은 방식으로 풀어
`data/browsecomp/raw.jsonl`(1,266행)을 만든다.

```bash
curl -sSL -o browse_comp_test_set.csv   https://openaipublic.blob.core.windows.net/simple-evals/browse_comp_test_set.csv
python scripts/decrypt_browsecomp.py browse_comp_test_set.csv data/browsecomp/raw.jsonl
```

`kbrowsecomp` 는 레지스트리에 등록만 되어 있고 데이터는 비어 있다.
`data/<이름>/raw.jsonl` 에 `{"question": ..., "answer": ...}` 형식으로 넣고 같은
스크립트를 돌리면 된다.

> 한국어 벤치마크는 `.env` 의 `SEARCH_REGION=kr`, `SEARCH_LANGUAGE=ko` 를 바꿔야 한다.

## 실행

```bash
python test.py                                  # conf.yaml 그대로
python test.py --method ragent    --tag b0
python test.py --method search-o1 --tag b1
python test.py --limit 5                        # 배선 확인
python test.py --split test                     # 300문항. 마지막에만
python test.py --tag b1 --resume                # 멈춘 실행 이어서

python train.py --tag g1                        # GEPA
```

평소에는 **validation** 으로 돈다. `--limit 100` 으로 먼저 보고 격차가 8점 미만이면
`--split test --resume` 으로 늘리는 것을 권한다. 캐시 키가 문항 단위라 앞 100문항은
그대로 재사용된다.

`--resume` 은 새 디렉터리를 만들지 않고 같은 조건의 **가장 최근 실행에 이어 붙인다**
(디렉터리를 직접 줄 수도 있다). 끝난 문항은 캐시에서 집으므로 모델도 판정도 다시
부르지 않는다.

산출물은 실행 디렉터리 하나다. 이름만 보고 무엇을 돌린 것인지 알 수 있다.

```
runs/test/20260902-2104_depthsearch_qwen3.5-9b_deepsearchqa_g1/
  config.json         무엇을 돌렸는가
  prompt.txt          메인 시스템 프롬프트
  explorer_prompt.txt explorer 시스템 프롬프트
  summary.json        점수 · 탐색 행동 · 예산 사용량 · 구간별 정확도
  records.jsonl       문항별 한 줄 요약
  q00022/
    trace.jsonl         이벤트 로그
    response.json       추론 · 응답 · 도구 호출 · 도구 결과 (턴별)
    explorer.json       explorer 호출 트리 (읽은 문서 · 확장 · 반환 요약)
    documents/doc-*.json DepthSearch가 재조회한 전체 필터링 원문
    tree.svg            탐색 궤적 그림 — 세 방법 모두 그린다
```

`tree.svg` 는 문항 하나가 웹을 어떻게 훑었는지를 트리로 보여 준다. 파랑 `search` ·
초록 `fetch`(메인 모델이 고른 것) · 주황 `expand`(explorer 의 재귀, depth≥2) · 회색
`auto doc`(search-o1 의 자동 페치), 빨간 테두리는 실패·거절이다. ragent 와 search-o1
은 평면으로 나오는데, **평면이라는 것을 눈으로 확인할 수 있어야** depthsearch 의
트리가 의미를 갖는다.

```bash
python tests/tree.py --demo                      # 세 방법의 예시 그림
python tests/tree.py runs/test/<런> --all         # 지난 실행 다시 그리기
```

## 예산이 이 저장소의 손잡이다

세 방법이 **같은 값을 써야** 비교가 성립한다. 이전 실험에서 검색 상한 없이 두었더니 한
문항에 검색 141회가 나왔고, 검색 횟수와 정답률이 이렇게 갈렸다.

| 검색 횟수 | 정답률 |
|---|---:|
| 0–19 | 0.62 |
| 20–39 | 0.50 |
| 40–59 | 0.13 |
| 80+ | 0.06 |

```yaml
max_searches: 10          # 세 방법 공통
search_results: 10        # 세 방법 공통. 자동 페치 5개와 다른 값
max_fetches: 0            # 메인 모델의 페치. 무제한 (ragent / depthsearch 공통)
search_top_k: 5           # 검색당 자동 페치. search-o1 만
fetch_max_tokens: 32768   # 페이지 하나의 토큰 상한. **세 방법 공통**
context_limit: 122880     # 131072 모델 길이에서 출력 8192 제외
max_expansion_nodes: 12   # 문항당 depth>=2 노드 총량 (depthsearch)
max_subtree_children: 2   # explorer 하나가 열 수 있는 자식 수
max_depth: 3
```

`fetch_max_tokens`는 세 방법의 첫 페이지 입력 상한이다. DepthSearch의 추가 원문 조회는
별도의 읽기 예산으로 기록한다. 동일한 검색 예산이 동일한 전체 문서 읽기량을 뜻하지는 않는다.

**확장 예산은 depth 2 이상만 센다.** 메인 모델이 고른 페치(depth 1)는 RAgent 에도
똑같이 있으므로 차감하면 두 조건의 행동 자체가 달라진다.

제약은 프롬프트가 아니라 **구조**로 건다. explorer는 깊이 상한에 닿거나 예산이
소진되면 fetch 도구를 **아예 받지 않는다**. explorer는 매번 새 세션이라 "쓰던 도구를
뺏기는" 혼란이 없다 — 대화 도중인 메인 모델은 반대로, 상한을 넘으면 도구를 뺏는 대신
"한도 초과, 이제 답하라"를 도구 결과로 돌려준다.

`agent.context_limit` 은 별개 안전장치다. 대화 토큰이 그 선에 닿으면 도구 결과를 남은
만큼만 잘라 넣는다. **어느 조건이 이 선에 얼마나 자주 닿는지가 이 실험의 직접 증거다** —
`summary.json` 의 `context_exhausted_rate` 를 정확도와 나란히 본다.

## 오염

라이브 웹을 검색하는 에이전트는 벤치마크의 문항·정답을 그대로 긁어올 수 있다(Search-Time
Contamination). 그러면 점수가 실력이 아니라 유출을 측정한다. 두 겹으로 막는다.

- 도구 서버가 이름으로 막는다(`BLOCKED_TERMS`). 도메인을 통째로 막지는 않는다 — 정당한
  자료 조회까지 죽는다.
- 에이전트가 문항과의 **8-gram 겹침**으로 걷어낸다. 미러는 이름이 무관해도 스니펫이나
  본문에 문항이 통째로 들어 있다. **검색 결과만이 아니라 모든 페치(확장 노드 포함)에
  적용한다** — 깊이가 깊어질수록 미러에 닿을 확률이 오른다.

```bash
python scripts/contamination.py            # 깊이별 URL 수 · 필터가 실제로 걷어낸 건수
```

막혔다는 사실 자체가 보고할 수치다. 조건마다 돌려 표에 같이 싣는다.

## 캐시

`runs/_cache/` 아래에 (방법, 모델, 에이전트·explorer 설정, 프롬프트 둘, 질문) 해시로 실행
결과를, (판정 모델, 벤치, 질문, 응답) 해시로 판정을 캐시한다. GEPA는 같은 조합을 여러 번
평가하므로 이 중복이 그대로 비용이다.

**깊이와 예산이 키에 들어간다.** 안 들어가면 depth 1 결과를 depth 3 실행이 조용히
재사용한다. 프롬프트가 한 글자라도 바뀌면 캐시는 당연히 빗나간다. 실패한 실행과 빈
응답은 캐시하지 않아 다시 돌리면 재시도된다.

## GEPA

최적화 대상이 둘이다.

| 컴포넌트 | 지시하는 것 | 관찰되는 행동 |
|---|---|---|
| `agent` | 검색 정책 | searches, turns |
| `explorer` | 추출 + 확장 정책 | expansion nodes, depth 분포 |

`depthsearch` 가 아니면 `explorer` 는 자동으로 빠진다 — ragent는 explorer가 없고,
search-o1은 확장 결정이 없어 최적화할 정책이 없다. GEPA는 모듈을 라운드로빈으로 고르므로
(논문 Alg.1 line 8) 컴포넌트가 둘이면 예산도 대략 2배가 필요하다.

피드백도 컴포넌트별로 다르게 준다. 최종 f1만 주면 explorer 프롬프트는 신호가 너무 멀어
거의 랜덤워크가 된다.

예산은 `auto` 대신 `max_metric_calls` 로 직접 건다. rollout 하나가 논문 설정보다 훨씬
비싸기 때문이다. `track_stats` 가 남기는 `val_scores` 곡선을 보고 다음 값을 정한다.
crossover(`merge`)는 끈다 — 논문 Table 1에서 Qwen3-8B는 merge로 오히려 떨어졌다.
