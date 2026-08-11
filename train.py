"""GEPA로 검색 에이전트의 시스템 프롬프트를 최적화한다.

    python train.py --config configs/train.yaml
    python train.py --tag seed0

산출물은 실행 디렉터리 하나다.

    runs/train/20260811-2104_qwen3.5-9b_deepsearchqa_seed0/
      prompt.txt          최적화된 시스템 프롬프트  <- 이것이 결과물
      initial_prompt.txt  출발점
      candidates.json     GEPA가 만든 후보 전부
      summary.json        점수와 예산 사용량
      records.jsonl       문항별 한 줄 요약
      traces/<stage>/     문항별 JSONL 트레이스
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import dspy

from searchgym.benchmarks import load_benchmark
from searchgym.config import load_train
from searchgym.gepa import PolicyProposer, SearchMetric, SearchProgram
from searchgym.judge import Judge
from searchgym.paths import load_env, run_dir
from searchgym.report import enable_utf8, summarize, table, write_json
from searchgym.runner import Runner
from searchgym.serving import profile_for


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GEPA 프롬프트 최적화")
    parser.add_argument("--config", default="configs/train.yaml")
    parser.add_argument("--tag", default=None, help="실행 디렉터리 이름에 붙일 꼬리표")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--no-cache", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    enable_utf8()
    load_env()
    args = parse_args(argv)

    config = load_train(args.config)
    if args.tag:
        config.run.tag = args.tag
    if args.seed is not None:
        config.run.seed = args.seed
    if not config.run.tag:
        config.run.tag = f"seed{config.run.seed}"

    profile = profile_for(config.model)
    benchmark = load_benchmark(config.data.benchmark, config.data.trainset)
    trainset = benchmark.load()
    valset = load_benchmark(config.data.benchmark, config.data.valset).load()

    out = run_dir("train", profile.repo, config.data.benchmark, config.run.tag, config.run.output_dir)
    table(
        "설정",
        {
            "model": f"{profile.key}  ({profile.repo})",
            "weights": "local" if profile.is_local else "hub",
            "endpoint": config.agent.base_url,
            "benchmark": config.data.benchmark,
            "train / val": f"{len(trainset)} / {len(valset)}",
            "budget": f"search {config.agent.max_searches} / fetch {config.agent.max_fetches}",
            "refine": config.agent.refine_fetched,
            "teacher": config.teacher.model,
            "judge": config.judge.model,
            "gepa": f"auto={config.gepa.auto} minibatch={config.gepa.reflection_minibatch_size}",
            "seed": config.run.seed,
            "run_dir": out,
        },
    )

    if not config.initial_prompt.strip():
        print("initial_prompt가 비어 있습니다.", file=sys.stderr)
        return 1
    if not config.feedback.template.strip():
        print("feedback.template이 비어 있습니다.", file=sys.stderr)
        return 1

    (out / "initial_prompt.txt").write_text(config.initial_prompt.strip(), encoding="utf-8")
    write_json(
        out / "config.json",
        {
            "source": config.source,
            "model": profile.repo,
            "agent": vars(config.agent),
            "teacher": {**vars(config.teacher)},
            "judge": vars(config.judge),
            "gepa": vars(config.gepa),
            "data": vars(config.data),
            "seed": config.run.seed,
        },
    )

    # --- 구성 ---------------------------------------------------------------

    judge = Judge(config.judge)
    runner = Runner(
        profile=profile,
        agent_config=config.agent,
        judge=judge,
        run_dir=out,
        use_cache=config.run.cache and not args.no_cache,
        workers=config.run.workers,
    )
    items = {item.index: item for item in trainset + valset}
    metric = SearchMetric(runner, benchmark, items, config.feedback)

    to_example = lambda item: dspy.Example(  # noqa: E731
        index=item.index, question=item.question
    ).with_inputs("index", "question")

    teacher = dspy.LM(
        model=config.teacher.model,
        temperature=1.0,
        max_tokens=config.teacher.max_tokens,
        **config.teacher.extra,
    )

    optimizer_kwargs: dict[str, Any] = {
        "metric": metric,
        "reflection_lm": teacher,
        "auto": config.gepa.auto,
        "reflection_minibatch_size": config.gepa.reflection_minibatch_size,
        "num_threads": config.gepa.num_threads,
        "track_stats": config.gepa.track_stats,
        "failure_score": config.gepa.failure_score,
        "seed": config.run.seed,
        **config.gepa.extra,
    }
    if config.teacher.reflection_prompt.strip():
        optimizer_kwargs["instruction_proposer"] = PolicyProposer(
            config.teacher.reflection_prompt, config.teacher.prompt_token_budget
        )

    program = SearchProgram(config.initial_prompt.strip())
    optimizer = dspy.GEPA(**optimizer_kwargs)

    # --- 최적화 -------------------------------------------------------------

    print("\n최적화 시작. Ctrl+C로 끊어도 지금까지의 기록은 남습니다.\n")
    metric.stage("optimize")
    optimized = optimizer.compile(
        program,
        trainset=[to_example(i) for i in trainset],
        valset=[to_example(i) for i in valset],
    )

    prompt = optimized.prompt
    (out / "prompt.txt").write_text(prompt, encoding="utf-8")

    detailed = getattr(optimized, "detailed_results", None)
    candidates = [c.prompt for c in getattr(detailed, "candidates", [])] if detailed else []
    if candidates:
        write_json(out / "candidates.json", candidates)

    summary = {
        "model": profile.repo,
        "benchmark": config.data.benchmark,
        "teacher": config.teacher.model,
        "judge": config.judge.model,
        "seed": config.run.seed,
        "initial_prompt_chars": len(config.initial_prompt.strip()),
        "final_prompt_chars": len(prompt),
        "candidates": len(candidates) or 1,
        "metric_calls": len(metric.records),
        "cache": runner.cache_stats(),
        "budget": {"searches": config.agent.max_searches, "fetches": config.agent.max_fetches},
        "behaviour": summarize(metric.records),
    }
    if detailed is not None:
        summary["val_scores"] = list(getattr(detailed, "val_aggregate_scores", []) or [])
        summary["best_index"] = getattr(detailed, "best_idx", None)
    write_json(out / "summary.json", summary)

    table("결과", {k: v for k, v in summary.items() if not isinstance(v, dict)})
    print(f"\n프롬프트: {out / 'prompt.txt'}")
    print(f"저장됨:   {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
