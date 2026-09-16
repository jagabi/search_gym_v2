"""GEPA 연결부 — dspy 메트릭과 instruction proposer.

최적화 대상이 둘이다.

    agent      메인 추론 모델의 시스템 프롬프트  (검색 정책)
    explorer   explorer 의 시스템 프롬프트       (추출 + 확장 정책)

GEPA 는 모듈을 라운드로빈으로 고르고(논문 Alg.1 line 8), 어느 모듈을 고쳤는지
`pred_name` 으로 알려 준다. 그래서 **피드백도 컴포넌트별로 다르게** 준다 — 최종
f1 만 주면 explorer 프롬프트는 신호가 너무 멀어 거의 랜덤워크가 된다.

**proposer** 는 GEPA 기본 메타 프롬프트를 갈아끼운다. 기본값에는 이런 문장이 있다 —
"Identify all niche and domain specific factual information about the task and include
it in the instruction." 수학처럼 사실이 전이되는 과제를 겨냥한 설계라, 사실을
찾아오는 것이 일인 검색 에이전트에서는 교사가 학습 문항의 **정답을 프롬프트에
그대로 써 넣는다**(미니배치만 1.0 이 되고 valset 은 떨어진다).
"""

from __future__ import annotations

import asyncio
import sys
import threading
from typing import Any

import dspy

from .benchmarks import Benchmark, Item
from .config import FeedbackConfig
from .runner import Record, Runner
from .scoring import Judgement

__all__ = ["BUDGET", "PolicyProposer", "SearchMetric", "SearchProgram"]

BUDGET = "<budget>"
_NONE = "(none)"


class SearchProgram(dspy.Module):
    """최적화 단위를 담는 그릇.

    dspy 는 `predictor.signature.instructions` 를 최적화 대상으로 본다. 실제 실행은
    metric 이 담당하므로 이 모듈은 프롬프트 두 개를 들고 있기만 한다. 속성 이름이
    곧 컴포넌트 이름이다("agent", "explorer").
    """

    def __init__(self, agent_prompt: str, explorer_prompt: str = "") -> None:
        super().__init__()
        self.agent = dspy.Predict(
            dspy.Signature("question -> answer").with_instructions(agent_prompt)
        )
        if explorer_prompt:
            self.explorer = dspy.Predict(
                dspy.Signature("documents -> information").with_instructions(explorer_prompt)
            )

    @property
    def agent_prompt(self) -> str:
        return self.agent.signature.instructions

    @property
    def explorer_prompt(self) -> str:
        predictor = getattr(self, "explorer", None)
        return predictor.signature.instructions if predictor is not None else ""

    def forward(self, question: str, **_: Any) -> dspy.Prediction:  # pragma: no cover
        return dspy.Prediction(answer="")


class SearchMetric:
    """dspy 메트릭. 문항 하나를 실제로 실행하고 점수 + 피드백을 돌려준다."""

    def __init__(
        self,
        runner: Runner,
        benchmark: Benchmark,
        items: dict[int, Item],
        feedback: FeedbackConfig,
        seed_prompts: dict[str, str],
    ) -> None:
        self.runner = runner
        self.benchmark = benchmark
        self.items = items
        self.feedback = feedback
        self.seed_prompts = seed_prompts
        self.records: list[Record] = []
        self._lock = threading.Lock()
        self._stage = "eval"
        self.__name__ = "search_metric"  # 일부 도구가 metric을 함수로 보고 읽는다

    def stage(self, name: str) -> None:
        self._stage = name

    def __call__(
        self,
        example: dspy.Example,
        prediction: Any = None,
        trace: Any = None,
        pred_name: Any = None,
        pred_trace: Any = None,
    ) -> dspy.Prediction:
        item = self.items[example.index]
        prompts = _prompts(prediction, self.seed_prompts)

        record = _run_sync(
            self.runner.run_all(
                self.benchmark,
                [item],
                prompts["agent"],
                explorer_prompt=prompts.get("explorer") or None,
                score_field=self.feedback.score,
                stage=self._stage,
            )
        )[0]
        with self._lock:
            self.records.append(record)

        return dspy.Prediction(
            score=record.score,
            feedback=self._render(item, record, str(pred_name or "agent")),
        )

    def _render(self, item: Item, record: Record, component: str) -> str:
        """컴포넌트별 피드백. 교사는 여기 적힌 텍스트만 보고 프롬프트를 고친다."""
        result, judgement = record.result, record.judgement
        metrics = judgement.metrics()
        missed = [text for text, ok in judgement.parts if not ok]

        template = (
            self.feedback.explorer_template
            if component == "explorer" and self.feedback.explorer_template.strip()
            else self.feedback.template
        )
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


class PolicyProposer:
    """컴포넌트별 메타 프롬프트로 새 시스템 프롬프트를 제안한다.

    dspy 의 ProposalFn 규약: (candidate, reflective_dataset, components_to_update)를
    받아 {컴포넌트 이름: 새 텍스트}를 돌려준다. 호출 시점에 dspy 컨텍스트의 LM이
    교사로 설정되어 있다.
    """

    def __init__(self, templates: dict[str, str], token_budget: int = 0) -> None:
        self.templates = templates
        self.token_budget = token_budget
        self._truncated = False

    def __call__(
        self,
        candidate: dict[str, str],
        reflective_dataset: dict[str, list[dict[str, Any]]],
        components_to_update: list[str],
    ) -> dict[str, str]:
        from gepa.strategies.instruction_proposal import InstructionProposalSignature

        out: dict[str, str] = {}
        for name in components_to_update:
            current = candidate[name]
            template = self.templates.get(name, "")
            if not template.strip():
                out[name] = current  # 메타 프롬프트가 없으면 손대지 않는다
                continue

            self._truncated = False
            raw = InstructionProposalSignature.run(
                lm=self._call,
                input_dict={
                    "current_instruction_doc": current,
                    "dataset_with_feedback": reflective_dataset[name],
                    "prompt_template": self._render(template, current),
                },
            )
            # 출력이 잘렸으면 반쪽짜리 프롬프트가 후보로 들어간다. 그건 개선이
            # 아니라 손상이므로 현재 프롬프트를 그대로 둔다(= 이번엔 제안 없음).
            if self._truncated:
                print(
                    f"[warn] 교사 출력이 잘렸습니다({name}, teacher.max_tokens). "
                    "이번 제안은 버립니다.",
                    file=sys.stderr,
                )
                out[name] = current
            else:
                out[name] = raw["new_instruction"]
        return out

    def _render(self, template: str, current: str) -> str:
        """<budget> 자리를 현재 토큰 수와 상한으로 바꾼다.

        "같은 길이로 유지하라"는 정성적 지시는 잘 무시된다. 지금 몇 토큰인지와
        상한을 숫자로 알려줘야 규칙을 덧붙이는 대신 갈아 끼운다.
        """
        if BUDGET not in template:
            return template
        if self.token_budget <= 0:
            return template.replace(BUDGET, "")

        now = _count_tokens(current)
        budget = self.token_budget
        if now > budget:
            line = (
                f"**The current prompt is {now:,} tokens, over the {budget:,} token limit — "
                f"past the length where the model starts following rules less reliably.** "
                f"Append nothing. Merge overlapping rules, cut the ones the feedback does "
                f"not support, and compress until it fits in {budget:,} tokens."
            )
        else:
            line = (
                f"**The current prompt is {now:,} tokens; the new one must stay within "
                f"{budget:,}.** That is a ceiling after many rounds, not a target to fill "
                f"now — shorter still wins. Make room by merging and compressing rather "
                f"than appending. Emit a complete prompt, never one cut off mid-sentence."
            )
        return template.replace(BUDGET, line)

    def _call(self, prompt: str | list[dict[str, Any]]) -> str:
        lm = dspy.settings.lm
        if lm is None:
            raise RuntimeError("reflection LM이 설정되지 않았습니다.")
        outputs = lm(prompt) if isinstance(prompt, str) else lm(messages=prompt)
        first = outputs[0]
        if isinstance(first, dict):
            first = first.get("text", "")
        text = str(first)
        # 코드 펜스가 열리기만 하고 닫히지 않았으면 중간에서 끊긴 것이다.
        self._truncated = text.count("```") < 2
        return text


# --- 렌더 도우미 -------------------------------------------------------------


def _prompts(prediction: Any, fallback: dict[str, str]) -> dict[str, str]:
    """GEPA 가 넘긴 후보 프로그램에서 컴포넌트별 프롬프트를 꺼낸다."""
    out = dict(fallback)
    for holder in (prediction, getattr(prediction, "program", None)):
        if holder is None:
            continue
        for name in ("agent", "explorer"):
            predictor = getattr(holder, name, None)
            signature = getattr(predictor, "signature", None)
            if signature is not None and getattr(signature, "instructions", None):
                out[name] = str(signature.instructions)
    return out


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
    """실패의 '종류'를 한 줄로 못박는다.

    못 찾은 것(recall)과 엉뚱하게 덧붙인 것(precision)은 프롬프트에서 정반대
    처방을 요구하므로, 둘 중 무엇이 깎였는지는 우리가 계산해서 알려 준다.
    """
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


def _count_tokens(text: str) -> int:
    try:
        import tiktoken

        return len(tiktoken.get_encoding("o200k_base").encode(text))
    except Exception:
        return max(1, len(text) // 4)  # tiktoken이 없으면 대략치


def _run_sync(coro: Any) -> Any:
    """dspy는 메트릭을 동기 함수로 부른다. 스레드마다 루프를 따로 쓴다."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    # 이미 루프 안이면(드물다) 별도 스레드에서 돌린다.
    box: dict[str, Any] = {}

    def work() -> None:
        box["value"] = asyncio.run(coro)

    thread = threading.Thread(target=work)
    thread.start()
    thread.join()
    return box["value"]
