"""GEPA 교사에게 실제로 무엇이 가고 무엇이 돌아오는지 본다 — GEPA 를 돌리지 않고.

    python tests/reflection.py                       # agent 컴포넌트
    python tests/reflection.py --component explorer
    python tests/reflection.py --dry                 # 교사 호출 없이 입력만 출력
    python tests/reflection.py --from runs/test/<런>/q00003/response.json

교사는 `feedback` 템플릿이 만든 텍스트만 보고 프롬프트를 고친다. 그 텍스트가 부실하면
GEPA 는 눈감고 최적화한다. 그래서 **한 번 눈으로 읽어 보는 것**이 GEPA 예산을 태우기
전에 할 수 있는 가장 싼 확인이다.

기본은 합성 실행 결과를 쓴다(모델도 도구도 필요 없다). `--from` 으로 실제 실행의
response.json 을 주면 그걸로 피드백을 만든다.

교사 호출에는 ANTHROPIC_API_KEY 와 dspy 가 필요하다. `--dry` 면 둘 다 필요 없다.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from searchgym.agent import RunResult, Step  # noqa: E402
from searchgym.benchmarks import load_benchmark  # noqa: E402
from searchgym.config import load_train  # noqa: E402
from searchgym.llm import Usage  # noqa: E402
from searchgym.paths import load_env, resolve  # noqa: E402
from searchgym.report import enable_utf8, table  # noqa: E402
from searchgym.runner import Record  # noqa: E402
from searchgym.scoring import Judgement  # noqa: E402
from searchgym.trace import ToolCall  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GEPA reflection 점검")
    parser.add_argument("--conf", default="conf.yaml")
    parser.add_argument("--gepa", default="configs/gepa.yaml")
    parser.add_argument("--method", default=None)
    parser.add_argument("--component", default=None, choices=["agent", "explorer"])
    parser.add_argument("--index", type=int, default=0, help="trainset 에서 몇 번째 문항인가")
    parser.add_argument("--from", dest="source", default=None, help="실제 실행의 response.json")
    parser.add_argument("--dry", action="store_true", help="교사를 부르지 않고 입력만 본다")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    enable_utf8()
    load_env()
    args = parse_args(argv)

    config = load_train(args.conf, args.gepa, method=args.method)
    components = config.component_names
    component = args.component or components[-1]
    if component not in components:
        print(
            f"'{config.base.method}' 에서 최적화하는 컴포넌트는 {components} 뿐입니다.",
            file=sys.stderr,
        )
        return 1

    benchmark = load_benchmark(config.data.benchmark, config.data.trainset)
    items = benchmark.load()
    item = items[min(args.index, len(items) - 1)]

    result = _from_file(args.source) if args.source else _synthetic(item.answer)
    judgement = _judgement(item)
    record = Record(
        index=item.index, category=item.category, score=0.25,
        judgement=judgement, result=result, dir="",
    )

    table(
        "설정",
        {
            "method": config.base.method,
            "components": ", ".join(components),
            "이번 컴포넌트": component,
            "teacher": config.teacher.model,
            "prompt_token_budget": config.teacher.prompt_token_budget,
            "실행 결과": args.source or "(합성)",
        },
    )

    # --- 1) 교사가 보는 피드백 --------------------------------------------
    from searchgym.gepa import SearchMetric

    seed = {"agent": config.base.system_prompt, "explorer": config.base.explorer_prompt}
    metric = SearchMetric(None, benchmark, {item.index: item}, config.feedback, seed)  # type: ignore[arg-type]
    feedback = metric._render(item, record, component)

    print(f"\n=== 교사가 보는 피드백 ({component}) " + "=" * 30)
    print(feedback)

    # --- 2) 교사에게 가는 메타 프롬프트 ------------------------------------
    from searchgym.gepa import PolicyProposer

    templates = {n: config.components[n].reflection_prompt for n in components}
    proposer = PolicyProposer(templates, config.teacher.prompt_token_budget)
    current = seed[component]
    rendered = proposer._render(templates[component], current)

    print(f"\n=== 메타 프롬프트 ({component}) " + "=" * 34)
    print(rendered.replace("<curr_param>", "\n" + current + "\n"))

    if args.dry:
        print("\n(--dry: 교사는 부르지 않았습니다)")
        return 0

    # --- 3) 실제로 한 번 제안받기 ------------------------------------------
    import dspy

    teacher = dspy.LM(
        model=config.teacher.model,
        temperature=1.0,
        max_tokens=config.teacher.max_tokens,
        **config.teacher.extra,
    )
    print(f"\n=== 교사 호출 ({config.teacher.model}) " + "=" * 28)
    with dspy.context(lm=teacher):
        proposed = proposer(
            candidate={component: current},
            reflective_dataset={component: [{"Feedback": feedback}]},
            components_to_update=[component],
        )

    new_prompt = proposed[component]
    print(new_prompt)
    table(
        "결과",
        {
            "이전 길이": f"{len(current):,}자",
            "새 길이": f"{len(new_prompt):,}자",
            "바뀌었는가": "아니오 (제안이 버려졌거나 동일)" if new_prompt == current else "예",
        },
    )
    if new_prompt == current:
        print("교사 출력이 잘렸을 수 있습니다 — teacher.max_tokens 를 확인하세요.")
    return 0


# --- 합성 실행 결과 ----------------------------------------------------------


def _synthetic(gold: str) -> RunResult:
    """모델 없이 만든 그럴듯한 실패 궤적. 피드백 렌더링을 보기에 충분하다."""
    search = ToolCall(name="web_search", arguments={"query": "when was the treaty signed"})
    fetch = ToolCall(name="web_fetch", arguments={"url": "https://example.org/treaty"})
    fetch.exploration = {
        "depth": 1, "query": "when was the treaty signed", "entry": "fetch",
        "urls": ["https://example.org/treaty"], "turns": 2, "status": "partial",
        "information": "The page lists the treaty but gives no signing date.",
        "nodes": 1, "error": None,
        "opened": [
            {
                "depth": 2, "urls": ["https://example.org/treaty/footnote-3"],
                "turns": 1, "status": "not_found",
                "information": "", "nodes": 0, "error": None, "opened": [],
            }
        ],
    }
    refused = ToolCall(
        name="web_search", arguments={"query": "treaty signing date"}, refused=True
    )

    return RunResult(
        answer="I could not determine the exact date from the sources I found.",
        steps=[
            Step(turn=1, reasoning="I need the signing date. Searching first.",
                 tool_calls=[search]),
            Step(turn=2, reasoning="The second result looks official. Opening it.",
                 tool_calls=[fetch]),
            Step(turn=3, reasoning="Still no date. Trying another search.",
                 tool_calls=[refused]),
            Step(turn=4, text="I could not determine the exact date."),
        ],
        explorations=[fetch.exploration],
        usage=Usage(input_tokens=41_000, output_tokens=2_100, reasoning_tokens=1_400, calls=6),
        turns=4, stop_reason="answered", latency_ms=182_000, context_tokens=44_000,
        budget={"total": 16, "used": 1, "refused": 0, "duplicates": 0, "visited": 2},
        expansion_nodes=1, max_depth_reached=2, explorer_calls=2, dead_dives=1,
    )


def _from_file(path: str) -> RunResult:
    payload = json.loads(resolve(path).read_text(encoding="utf-8"))
    from searchgym.runner import _result_from

    result = _result_from(payload)
    result.explorations = [
        c["exploration"]
        for s in payload.get("steps") or []
        for c in s.get("tool_calls") or []
        if c.get("exploration")
    ]
    return result


def _judgement(item) -> Judgement:
    parts = item.answer_parts or [item.answer]
    # 첫 파트만 맞고 나머지는 놓친 상태 — 피드백의 failure_mode 를 보기 좋다.
    pairs = [(p, i == 0) for i, p in enumerate(parts)]
    return Judgement(
        parts=pairs,
        excessive=[],
        explanation="The response names the entity but never commits to a date.",
        extracted="(none)",
    )


if __name__ == "__main__":
    raise SystemExit(main())
