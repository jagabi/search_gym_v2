"""GEPA 연결부 — gepa.optimize() 에 넣는 adapter.

최적화 대상은 방법에 따라 이 중 일부다.

    agent      메인 추론 모델의 시스템 프롬프트  (검색 정책)
    explorer   explorer 의 시스템 프롬프트       (추출 + 확장 정책)
    decision   decision 모델의 evidence 지시문   (어느 원문 bundle 을 넘길지)

dspy 를 거치지 않는다. dspy 는 reflective dataset 을 predictor 호출 trace 로 만드는데,
여기서는 실행이 dspy 밖(Runner)에서 일어나 그 trace 가 비고, side_info 도 정할 수 없다.
그래서 adapter 가 세 가지를 직접 한다.

    evaluate                 후보 프롬프트로 문항을 실행하고 점수를 낸다.
    make_reflective_dataset  컴포넌트별로 교사에게 보여 줄 문항별 기록을 만든다.
    propose_new_texts        컴포넌트별 reflection_prompt 의 <curr_param> / <side_info> 를
                             채워 교사(Anthropic API)에게 새 텍스트를 받는다.

side_info (RawTree 방법)
    agent     문항 · 기대 답 · 최종 답과 점수, 검색마다 쿼리와 넘겨받은 발췌 원문.
    decision  문항 · 기대 답 · 점수, 검색마다 점수 상위 5개 발췌 원문과 점수.
그 밖의 방법·컴포넌트는 feedback.template 을 채운 텍스트를 쓴다.
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import json
import sys
import threading
from pathlib import Path
from typing import Any

from .benchmarks import Benchmark, Item
from .config import FeedbackConfig, TeacherConfig
from .runner import Record, Runner
from .scoring import Judgement

__all__ = ["SearchAdapter", "Teacher", "rollout_searches"]

_NONE = "(none)"
DECISION_TOP_K = 5


# --- 실행 ---------------------------------------------------------------------


class _Loop:
    """비동기 Runner 를 동기 adapter 에서 부르기 위한 상주 이벤트 루프.

    LLM · decision 클라이언트는 처음 쓴 루프에 묶인다. 호출마다 asyncio.run 으로 새 루프를
    만들면 두 번째 평가부터 닫힌 루프를 쓰게 되므로, 루프 하나를 스레드에 띄워 둔다.
    """

    def __init__(self) -> None:
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.loop.run_forever, daemon=True).start()

    def run(self, coro: Any) -> Any:
        # 시간 제한 없이 .result() 로 막혀 있으면 Windows 에서 Ctrl+C 가 전달되지 않는다.
        # 짧게 끊어 기다리고, 끊기면 돌던 rollout 을 취소한 뒤 KeyboardInterrupt 를 올린다.
        future = asyncio.run_coroutine_threadsafe(coro, self.loop)
        try:
            while True:
                try:
                    return future.result(timeout=0.5)
                except concurrent.futures.TimeoutError:
                    continue
        except KeyboardInterrupt:
            future.cancel()
            try:
                future.result(timeout=10)
            except BaseException:
                pass
            raise


class SearchAdapter:
    """gepa.GEPAAdapter. DataInst = Item, Trajectory = Record."""

    def __init__(
        self,
        runner: Runner,
        benchmark: Benchmark,
        items: dict[int, Item],
        feedback: FeedbackConfig,
        templates: dict[str, str],
        teacher: "Teacher",
        native_side_info: bool,
    ) -> None:
        self.runner = runner
        self.benchmark = benchmark
        self.items = items
        self.feedback = feedback
        self.templates = templates
        self.teacher = teacher
        # RawTree 방법이면 trace 에서 검색별 발췌를 읽어 side_info 를 만든다.
        self.native = native_side_info
        self.records: list[Record] = []
        self.stage = "optimize"
        self._loop = _Loop()
        self._lock = threading.Lock()

    # gepa 규약 ------------------------------------------------------------------

    # 이어 돌릴 때 건너뛸 시드 valset 평가: (시드 후보, valset 문항 수). train.py 가 채운다.
    skip_seed_eval: tuple[dict[str, str], int] | None = None

    def evaluate(self, batch: list[Item], candidate: dict[str, str], capture_traces: bool = False):
        from gepa import EvaluationBatch

        # gepa 는 이어 돌릴 때도 시드를 valset 전체로 먼저 평가한 뒤, 저장된 상태를 불러오면서
        # 그 결과를 버린다(engine.run -> initialize_gepa_state). 실행하지 않고 빈 점수를 준다.
        if self.skip_seed_eval is not None:
            seed, size = self.skip_seed_eval
            if candidate == seed and len(batch) == size and not capture_traces:
                self.skip_seed_eval = None
                print("[resume] 시드 valset 평가는 저장된 상태로 대체합니다(실행 안 함).")
                return EvaluationBatch(outputs=[""] * size, scores=[0.0] * size,
                                       trajectories=None)

        records = self._loop.run(
            self.runner.run_all(
                self.benchmark,
                batch,
                candidate["agent"],
                explorer_prompt=candidate.get("explorer") or None,
                score_field=self.feedback.score,
                stage=self.stage,
                decision_prompt=candidate.get("decision") or None,
            )
        )
        with self._lock:
            self.records.extend(records)
        return EvaluationBatch(
            outputs=[r.result.answer for r in records],
            scores=[r.score for r in records],
            trajectories=records if capture_traces else None,
        )

    def make_reflective_dataset(self, candidate, eval_batch, components_to_update):
        records: list[Record] = list(eval_batch.trajectories or [])
        searches = [rollout_searches(r, self.runner.run_dir) if self.native else None for r in records]
        out: dict[str, list[dict[str, str]]] = {}
        for name in components_to_update:
            rows = []
            for n, record in enumerate(records, 1):
                item = self.items[record.index]
                if self.native and name == "agent":
                    text = render_agent_example(n, item, record, searches[n - 1])
                elif self.native and name == "decision":
                    text = render_decision_example(n, item, record, searches[n - 1])
                else:
                    text = f"# Example {n}\n" + self._render_template(item, record, name)
                rows.append({"text": text})
            out[name] = rows
        return out

    def propose_new_texts(self, candidate, reflective_dataset, components_to_update):
        out: dict[str, str] = {}
        for name in components_to_update:
            current = candidate[name]
            template = self.templates.get(name, "")
            if not template.strip():
                out[name] = current  # 메타 프롬프트가 없으면 손대지 않는다
                continue
            side_info = "\n\n".join(r["text"] for r in reflective_dataset.get(name, []))
            prompt = template.replace("<curr_param>", current).replace("<side_info>", side_info)
            proposed = self.teacher.propose(name, prompt)
            out[name] = proposed if proposed else current
        return out

    # 내부 ------------------------------------------------------------------------

    def _render_template(self, item: Item, record: Record, component: str) -> str:
        """RawTree 가 아닌 방법의 피드백. feedback.template(explorer 는 explorer_template)."""
        result, judgement = record.result, record.judgement
        metrics = judgement.metrics()
        missed = [text for text, ok in judgement.parts if not ok]
        own = self.feedback.explorer_template if component == "explorer" else ""
        template = own if own.strip() else self.feedback.template
        return template.format(
            question=item.question.strip(),
            gold_answer=item.answer.strip(),
            answer=_clip(result.answer, self.feedback.max_answer_chars) or _NONE,
            score=record.score,
            precision=metrics["precision"],
            recall=metrics["recall"],
            f1=metrics["f1"],
            verdict=_verdict(judgement),
            failure_mode=_failure_mode(judgement, result.answer),
            missed_parts=_bullets(missed),
            excessive_answers=_bullets(judgement.excessive),
            searches=result.searches,
            fetches=result.fetches,
            queries=_numbered(result.queries) or "(no search)",
            urls=_bullets(result.urls),
            trajectory=_clip(result.render_trajectory(), self.feedback.max_trajectory_chars),
            stop_reason=result.stop_reason,
            turns=result.turns,
            latency_s=round(result.latency_ms / 1000, 1),
            error=result.error or "none",
            expansion_nodes=result.expansion_nodes,
            max_depth_reached=result.max_depth_reached,
            explorer_calls=result.explorer_calls,
            dead_dives=result.dead_dives,
            budget_exhausted="yes" if result.budget_exhausted else "no",
            context_exhausted="yes" if result.context_exhausted else "no",
            explorer_log=result.render_explorer_log(self.feedback.max_trajectory_chars),
        )


class Utf8Logger:
    """gepa LoggerProtocol. 콘솔에 찍고 run_log.txt 에 UTF-8 로 덧붙인다.

    gepa 기본 Logger 는 파일을 시스템 인코딩으로 열고 sys.stdout 까지 바꿔 끼운다.
    한국어 Windows(cp949)에서는 교사 제안의 '—' 하나로 최적화 전체가 죽는다.
    """

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.handle = path.open("a", encoding="utf-8")

    def log(self, message: str) -> None:
        try:
            print(message)
        except UnicodeEncodeError:
            enc = sys.stdout.encoding or "utf-8"
            print(message.encode(enc, "replace").decode(enc))
        self.handle.write(message + "\n")
        self.handle.flush()


# --- 교사 ---------------------------------------------------------------------


class Teacher:
    """reflection 모델. Anthropic API 를 직접 부르고, 호출마다 프롬프트와 응답을 남긴다."""

    def __init__(self, config: TeacherConfig, log_dir: Path) -> None:
        import anthropic

        self.config = config
        self.model = config.model.removeprefix("anthropic/")
        self.client = anthropic.Anthropic(max_retries=5)
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        # 이어 돌릴 때 이전 호출 기록을 덮어쓰지 않도록 번호를 이어 간다.
        self.calls = len(list(self.log_dir.glob("*.json")))

    def propose(self, component: str, prompt: str) -> str | None:
        """새 텍스트. 잘렸거나 거절됐거나 코드펜스가 없으면 None(= 현재 텍스트 유지)."""
        self.calls += 1
        with self.client.messages.stream(
            model=self.model,
            max_tokens=self.config.max_tokens,
            output_config={"effort": self.config.effort},
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            message = stream.get_final_message()
        text = "".join(b.text for b in message.content if b.type == "text")
        proposed = _fenced(text)

        problem = None
        if message.stop_reason == "refusal":
            problem = "refused"
        elif message.stop_reason == "max_tokens":
            problem = "truncated (teacher.max_tokens)"
        elif proposed is None:
            problem = "no fenced block"

        stem = self.log_dir / f"{self.calls:03d}_{component}"
        stem.with_suffix(".prompt.md").write_text(prompt, encoding="utf-8")
        stem.with_suffix(".response.md").write_text(text, encoding="utf-8")
        stem.with_suffix(".json").write_text(json.dumps({
            "component": component, "model": message.model, "stop_reason": message.stop_reason,
            "usage": message.usage.model_dump(), "problem": problem,
        }, ensure_ascii=False, indent=1), encoding="utf-8")

        if problem:
            print(f"[warn] teacher {component}: {problem}. 이번 제안은 버립니다.", file=sys.stderr)
            return None
        return proposed


def _fenced(text: str) -> str | None:
    """첫 ``` 와 마지막 ``` 사이. 여는 줄의 언어 표기는 뗀다(gepa 기본 추출과 같은 규칙)."""
    start, end = text.find("```"), text.rfind("```")
    if start < 0 or end <= start:
        return None
    body = text[start + 3:end]
    first, _, rest = body.partition("\n")
    if first.strip() and " " not in first.strip() and rest:
        body = rest  # ```markdown 같은 언어 표기
    body = body.strip()
    return body or None


# --- trace -> 검색별 발췌 -------------------------------------------------------


def rollout_searches(record: Record, runner_dir: Path | None = None) -> list[dict[str, Any]] | None:
    """이 rollout 의 검색마다 쿼리와, 점수가 매겨진 발췌 전부(점수 내림차순).

    [{"query": str, "excerpts": [{"score", "title", "text", "passed"}...]}...]
    trace 를 찾을 수 없으면 None.
    """
    path = Path(record.trace_path) if record.trace_path else (
        runner_dir / record.dir / "trace.jsonl" if runner_dir and record.dir else None)
    if path is None or not path.exists():
        return None

    order: list[str] = []
    queries: dict[str, str] = {}
    scores: dict[str, dict[tuple[str, int], float]] = {}
    texts: dict[tuple[str, str, int], tuple[str, str]] = {}
    passed: dict[str, dict[tuple[str, int], str]] = {}
    run_id = record.trace_id
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if run_id and run_id not in line:
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            if run_id and e.get("run_id") != run_id:
                continue
            kind, sid = e.get("event"), e.get("search_id", "")
            if kind == "rawtree.start":
                order.append(sid)
                queries[sid] = e.get("query", "")
            elif kind == "rawtree.bundles":
                rows = scores.setdefault(sid, {})
                for b in e.get("bundles") or []:
                    if isinstance(b.get("evidence_value"), (int, float)):
                        rows[(e.get("node_id", ""), b.get("id"))] = float(b["evidence_value"])
            elif kind == "jev.request":
                ctx = e.get("context") or {}
                state = (e.get("body") or {}).get("state") or {}
                if ctx.get("phase") == "bundle" and state:
                    texts[(ctx.get("search_id", ""), ctx.get("node_id", ""), ctx.get("bundle_id"))] = (
                        state.get("page_title", ""), state.get("page_text", ""))
            elif kind == "rawtree.return":
                out = passed.setdefault(sid, {})
                for s in e.get("selected") or []:
                    node, _, bundle = str(s.get("id", "")).partition(":bundle:")
                    out[(node, int(bundle) if bundle.isdigit() else -1)] = s.get("text", "")

    searches = []
    for sid in order:
        chosen = passed.get(sid, {})
        excerpts = []
        for (node, bundle), score in scores.get(sid, {}).items():
            title, text = texts.get((sid, node, bundle), ("", ""))
            excerpts.append({"score": score, "title": title, "text": text or chosen.get((node, bundle), ""),
                             "passed": (node, bundle) in chosen})
        excerpts.sort(key=lambda x: -x["score"])
        searches.append({"query": queries[sid], "excerpts": excerpts})
    return searches


# --- side_info ----------------------------------------------------------------


def _excerpt(title: str, text: str) -> str:
    title = " ".join((title or "untitled").split()).replace('"', "'")
    return f'<excerpt title="{title}">\n{text.strip()}\n</excerpt>'


def _head(n: int, item: Item) -> list[str]:
    return [f"# Example {n}", "## Question", item.question.strip(), "", "## Expected answer",
            item.answer.strip(), ""]


def render_agent_example(n: int, item: Item, record: Record, searches: list | None) -> str:
    result = record.result
    lines = _head(n, item)
    lines += [f"## Final answer — grade {record.score:.2f}", result.answer.strip() or "(no answer)"]
    ended = f"({result.searches} searches; ended: {result.stop_reason}"
    lines += [ended + (f"; error: {result.error}" if result.error else "") + ")", ""]
    if searches is None:
        lines.append("(search log unavailable for this run)")
        return "\n".join(lines)
    for k, s in enumerate(searches, 1):
        lines += [f"## Search {k}", f'query: "{s["query"]}"']
        given = [x for x in s["excerpts"] if x["passed"]]
        if not given:
            lines.append("(no page could be read; nothing was passed on)")
        lines += [_excerpt(x["title"], x["text"]) for x in given]
        lines.append("")
    return "\n".join(lines).rstrip()


def render_decision_example(n: int, item: Item, record: Record, searches: list | None) -> str:
    lines = _head(n, item)
    lines += [f"## Grade {record.score:.2f}", ""]
    if searches is None:
        lines.append("(search log unavailable for this run)")
        return "\n".join(lines)
    for k, s in enumerate(searches, 1):
        lines.append(f'## Search {k} — query: "{s["query"]}"')
        rows = s["excerpts"]
        if not rows:
            lines += ["(no page could be scored)", ""]
            continue
        for rank, x in enumerate(rows[:DECISION_TOP_K], 1):
            mark = " (passed on)" if x["passed"] else ""
            lines += [f"### Rank {rank} of {len(rows)} — {x['score']:.2f}{mark}",
                      _excerpt(x["title"], x["text"])]
        lines.append("")
    return "\n".join(lines).rstrip()


# --- 템플릿 피드백 도우미 (RawTree 가 아닌 방법) ---------------------------------


def _verdict(judgement: Judgement) -> str:
    if judgement.error:
        return f"NOT GRADED - {judgement.error}"
    found = [text for text, ok in judgement.parts if ok]
    missed = [text for text, ok in judgement.parts if not ok]
    lines = [f"The judge marked this {judgement.category.replace('_', ' ')}."]
    if judgement.explanation:
        lines.append(judgement.explanation.strip())
    if judgement.extracted:
        lines.append(f"Extracted final answer: {judgement.extracted}")
    lines.append(f"Found {len(found)} of {len(found) + len(missed)} expected part(s).")
    return "\n".join(lines)


def _failure_mode(judgement: Judgement, answer: str) -> str:
    if judgement.error:
        return f"NOT GRADED - {judgement.error} (this is a harness failure, not agent behaviour)"
    if not answer.strip():
        return "NO ANSWER - the agent finished without producing an answer"
    tp, fn, fp = judgement.tp, judgement.fn, judgement.fp
    total = tp + fn
    if fn and not tp:
        return f"COMPLETELY WRONG - none of the {total} expected part(s) were found" + (
            f", and {fp} wrong one(s) were given" if fp else ""
        )
    if fn and fp:
        return f"BOTH - missed {fn} of {total} part(s) AND gave {fp} wrong answer(s)"
    if fn:
        return f"MISSED - found {tp} of {total} part(s); {fn} were not in the answer"
    if fp:
        return f"OVER-ANSWERED - all {total} part(s) found, but {fp} wrong answer(s) added"
    return "CORRECT"


def _bullets(values: list[str]) -> str:
    return "\n".join(f"- {v}" for v in values) if values else _NONE


def _numbered(values: list[str]) -> str:
    return "\n".join(f"{i}. {v}" for i, v in enumerate(values, 1))


def _clip(text: str, limit: int) -> str:
    text = text.strip()
    if limit <= 0 or len(text) <= limit:
        return text
    return text[:limit] + f"\n... (truncated, {len(text):,} chars total)"
