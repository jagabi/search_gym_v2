# search_gym

검색 에이전트의 **시스템 프롬프트**를 GEPA로 최적화하고, 학습에 쓰지 않은 벤치마크에서 일반화를 확인한다.

- **학생** — vLLM으로 띄운 로컬 오픈 모델. `web_search`(Serper) + `web_fetch`(Jina) 두 도구를 쓴다.
- **교사** — GEPA reflection LM. 실행 궤적을 읽고 프롬프트를 고쳐 쓴다.
- **판정** — Gemini. structured output으로 정답 파트별 boolean을 받는다.

도구 루프가 **우리 프로세스 안에** 있다. 그래서 벤더 서버측 검색으로는 불가능했던 두 가지를 한다 — 검색 예산 하드캡, 그리고 페치 원문을 메인 컨텍스트에 넣기 전 압축(Search-o1의 Reason-in-Documents).

## 구조

```
searchgym/
  benchmarks/     문항 로딩 + 판정 프롬프트·스키마   (통일 레코드 형식)
  tools/          Serper·Jina를 MCP 도구로 노출 + 클라이언트
  agent.py        vLLM OpenAI 호환 서버 위의 도구 루프
  serving.py      모델별 vllm serve 프로파일 (파서·샘플링·주의사항)
  judge.py        Gemini structured-output 판정
  runner.py       실행 + 채점 + 디스크 캐시 + 기록
  gepa.py         dspy 메트릭과 instruction proposer
  config.py       YAML -> 데이터클래스 (알 수 없는 키는 시작 전에 실패)
  scoring.py      Judgement -> precision/recall/f1/accuracy
  report.py       콘솔 표와 summary.json
configs/          train.yaml · eval.yaml
data/<벤치>/      raw.* -> source/train/validation/test.json
models/           모델 가중치를 여기에 clone
scripts/          build_splits.py · serve.py · smoke.py
train.py  eval.py
```

## 설치

```bash
pip install -r requirements.txt
cp .env.example .env      # SERPER / JINA / GOOGLE / ANTHROPIC 키를 채운다
```

모델 가중치는 `models/` 아래에 받아 둔다. 있으면 로컬 경로로, 없으면 HF에서 스트리밍한다.

```bash
git lfs install
git clone https://huggingface.co/Qwen/Qwen3.5-9B models/Qwen3.5-9B
```

## 서빙

세 모델 모두 vLLM의 OpenAI 호환 서버로 띄운다. 그래서 에이전트 코드는 하나다.

```bash
python scripts/serve.py              # 세 모델의 serve 명령과 주의사항 출력
python scripts/serve.py qwen         # 하나만
```

| 키 | 모델 | tool parser | reasoning parser |
|---|---|---|---|
| `qwen` | Qwen/Qwen3.5-9B | `qwen3_coder` | `qwen3` |
| `gemma` | google/gemma-4-12B-it | `gemma4` | `gemma4` |
| `gpt-oss` | openai/gpt-oss-20b | `openai` | `openai_gptoss` |

주의할 점은 `serving.py`의 `notes`에 모델별로 적어 두었다. 요약하면 — gemma-4-12B Unified는 아직 stable 릴리스에 없어 nightly나 핀된 도커 이미지가 필요하고, gpt-oss는 harmony 포맷 전용이지만 vLLM이 변환을 처리하므로 `/v1/chat/completions`를 그대로 쓰면 된다.

## 데이터

모든 벤치마크가 **같은 레코드 형식**을 쓴다. 새 벤치마크는 원본을 이 형식으로 바꾸기만 하면 실행·채점 경로를 건드릴 필요가 없다.

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

`answer_type`이 판정 방식을 정한다. `single`이면 boolean 하나(→ f1 == accuracy), `set`이면 파트별 boolean + 여분 답 목록(→ f1이 부분점수로 움직인다).

```bash
python scripts/build_splits.py deepsearchqa --force                        # 30/30/300
python scripts/build_splits.py evobrowsecomp --train 50 --val 50 --force   # 50/50/300
```

카테고리를 라운드로빈으로 뽑아 균등하게 채운다. DeepSearchQA는 카테고리가 심하게 치우쳐 있어서(Politics 148건 대 Linguistics 1건) 무작위로 뽑으면 30문항 valset이 두 분야로 채워진다.

`browsecomp` / `kbrowsecomp`는 레지스트리에 등록만 되어 있고 데이터는 비어 있다. `data/<이름>/raw.jsonl`에 `{"question": ..., "answer": ...}` 형식으로 넣고 같은 스크립트를 돌리면 된다.

> 한국어 벤치마크는 `.env`의 `SEARCH_REGION=kr`, `SEARCH_LANGUAGE=ko`를 바꿔야 한다. 안 바꾸면 영어 결과만 와서 점수가 바닥난다.

## 실행

```bash
python scripts/smoke.py --offline    # 설정·데이터 배선만
python scripts/smoke.py              # 도구와 판정까지 실제로 한 번씩 호출

python train.py --config configs/train.yaml --tag seed0
python eval.py  --prompt runs/train/<런>/prompt.txt --tag optimized
python eval.py  --tag baseline                        # 프롬프트 없이 대조군
```

산출물은 실행 디렉터리 하나다. 이름만 보고 무엇을 돌린 것인지 알 수 있다.

```
runs/train/20260811-2104_qwen3.5-9b_deepsearchqa_seed0/
  prompt.txt          최적화된 시스템 프롬프트   <- 결과물
  initial_prompt.txt  출발점
  candidates.json     GEPA가 만든 후보 전부
  summary.json        점수 · 검색 예산 사용량 · 캐시 통계
  records.jsonl       문항별 한 줄 요약
  <stage>/q00022/     문항 하나 = 디렉터리 하나
    trace.jsonl         이벤트 로그 (llm.request / tool.call / budget.* / run.end)
    response.json       추론 · 응답 · 도구 호출 · 도구 결과 (턴별)
    search_o1.json      페치 정제: 직전 추론 + 검색어 + jina 원문 -> 정제 결과
```

## 검색 예산이 핵심 손잡이다

`agent.max_searches` / `max_fetches`가 이 저장소에서 가장 중요한 설정이다. 이전 실험에서 상한 없이 두었더니 한 문항에 검색 141회가 나왔고, 검색 횟수와 정답률이 이렇게 갈렸다.

| 검색 횟수 | 정답률 |
|---|---:|
| 0–19 | 0.62 |
| 20–39 | 0.50 |
| 40–59 | 0.13 |
| 80+ | 0.06 |

더 검색할수록 더 틀린다. 상한을 넘으면 도구를 뺏는 대신 "한도 초과, 이제 답하라"를 도구 결과로 돌려준다 — 모델이 스스로 마무리하게 두는 쪽이 안전하다. `agent.context_limit`은 별개 안전장치로, 대화 토큰이 그 선에 닿으면 도구 결과를 남은 만큼만 잘라 넣는다. `summary.json`의 `by_search_count`가 매 실행마다 이 표를 다시 그려 준다.

## 캐시

`runs/_cache/` 아래에 (모델, 에이전트 설정, 시스템 프롬프트, 질문) 해시로 실행 결과를, (판정 모델, 벤치, 질문, 응답) 해시로 판정을 캐시한다. GEPA는 같은 조합을 여러 번 평가하므로 이 중복이 그대로 비용이다.

프롬프트가 한 글자라도 바뀌면 캐시는 당연히 빗나간다. 실패한 실행과 빈 응답은 캐시하지 않아 다시 돌리면 재시도된다.
